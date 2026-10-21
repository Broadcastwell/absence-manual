"""Keep source URLs intact while reducing article image and CSS transfer work."""

from hashlib import sha256
from html import escape
from html.parser import HTMLParser
from pathlib import Path
import posixpath
import re
from urllib.parse import urlsplit

from PIL import Image


class TagAttributes(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)


def local_file(site, page, url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    candidate = (site / parsed.path.lstrip('/')) if parsed.path.startswith('/') else (page.parent / parsed.path)
    candidate = candidate.resolve()
    return candidate if candidate.is_relative_to(site) and candidate.is_file() else None


def relative_url(page, target):
    return posixpath.relpath(target.as_posix(), page.parent.as_posix())


def on_post_build(config, **kwargs):
    site = Path(config['site_dir']).resolve()
    generated = site / 'assets' / 'performance'
    generated.mkdir(parents=True, exist_ok=True)
    styles = site / 'assets' / 'stylesheets'
    styles.mkdir(parents=True, exist_ok=True)
    css_cache = {}
    image_cache = {}
    stats = {'pages': 0, 'stylesheet_bundles': 0, 'responsive_images': 0, 'variants': 0}

    for page in sorted(site.rglob('*.html')):
        text = page.read_text(encoding='utf-8')
        links = []
        for match in re.finditer(r'<link\b[^>]*>', text):
            parser = TagAttributes()
            parser.feed(match.group())
            attrs = parser.attrs
            if attrs.get('rel') == 'stylesheet' and set(attrs) <= {'rel', 'href'}:
                source = local_file(site, page, attrs.get('href', ''))
                if source and source.suffix == '.css':
                    links.append((match, source))
        if len(links) > 1:
            sources = tuple(source for _, source in links)
            if sources not in css_cache:
                chunks = []
                for source in sources:
                    css = source.read_text(encoding='utf-8')
                    def rebase(match):
                        raw = match.group(1).strip().strip('"\'')
                        parsed = urlsplit(raw)
                        if not raw or raw.startswith(('/', '#', 'data:')) or parsed.scheme or parsed.netloc:
                            return match.group()
                        target = (source.parent / parsed.path).resolve()
                        if not target.is_relative_to(site):
                            raise ValueError(f'CSS asset escapes site: {raw}')
                        new = posixpath.relpath(target.as_posix(), styles.as_posix())
                        if parsed.query:
                            new += '?' + parsed.query
                        if parsed.fragment:
                            new += '#' + parsed.fragment
                        return 'url("' + new + '")'
                    css = re.sub(r'url\(\s*([^)]*?)\s*\)', rebase, css)
                    css = re.sub(r'@charset\s+[^;]+;', '', css)
                    chunks.append(css)
                combined = '\n'.join(chunks)
                output = styles / ('combined-' + sha256(combined.encode()).hexdigest()[:16] + '.css')
                output.write_text(combined, encoding='utf-8')
                css_cache[sources] = output
                stats['stylesheet_bundles'] += 1
            for index, (match, _) in reversed(list(enumerate(links))):
                replacement = '<link rel="stylesheet" href="' + escape(relative_url(page, css_cache[sources]), quote=True) + '">' if index == 0 else ''
                text = text[:match.start()] + replacement + text[match.end():]

        article = re.search(r'(<article\b[^>]*>)(.*?)(</article>)', text, flags=re.S)
        if article:
            count = 0
            def improve_image(match):
                nonlocal count
                parser = TagAttributes()
                parser.feed(match.group())
                attrs = parser.attrs
                source = local_file(site, page, attrs.get('src', ''))
                if not source or source.suffix.lower() not in {'.png', '.jpg', '.jpeg'}:
                    return match.group()
                with Image.open(source) as image:
                    width, height = image.size
                    if width < 800:
                        return match.group()
                    if source not in image_cache:
                        variants = []
                        digest = sha256(source.read_bytes()).hexdigest()[:16]
                        for size in sorted({min(width, size) for size in (400, 800, 1320)}):
                            output = generated / (digest + '-' + str(size) + '.webp')
                            resized = image.convert('RGB' if image.mode not in {'RGBA', 'LA'} else 'RGBA').resize((size, round(height * size / width)), Image.Resampling.LANCZOS)
                            resized.save(output, 'WEBP', lossless=True, method=6)
                            variants.append((size, output))
                            stats['variants'] += 1
                        image_cache[source] = variants
                    attrs['width'] = str(width)
                    attrs['height'] = str(height)
                    attrs['decoding'] = 'async'
                    attrs['srcset'] = ', '.join(relative_url(page, output) + ' ' + str(size) + 'w' for size, output in image_cache[source])
                    attrs['sizes'] = '(max-width: 720px) calc(100vw - 48px), 661px'
                    if count > 0 and 'loading' not in attrs:
                        attrs['loading'] = 'lazy'
                    count += 1
                    stats['responsive_images'] += 1
                    return '<img' + ''.join(' ' + key + ('' if value is None else '="' + escape(value, quote=True) + '"') for key, value in attrs.items()) + '>'
            content = re.sub(r'<img\b[^>]*>', improve_image, article.group(2))
            text = text[:article.start(2)] + content + text[article.end(2):]
        page.write_text(text, encoding='utf-8')
        stats['pages'] += 1
    import json
    print('Performance assets: ' + json.dumps(stats, sort_keys=True))
