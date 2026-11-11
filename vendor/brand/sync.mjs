// Copies the Broadcastwell brand package files this repository uses from a bw-client-data
// checkout into vendor/brand/, byte for byte, and records the version they came from.
//
//   node vendor/brand/sync.mjs <path to a bw-client-data checkout>
//
// vendor/brand/VERSION.json is the package's own manifest, copied unchanged.
// vendor/brand/VENDORED.json lists each vendored file, the package path it came from, its
// sha256 and the source commit. The vendor test fails when any copy's hash differs from
// VERSION.json, so a hand edit or a partial sync cannot ship.
import { readFileSync, writeFileSync, mkdirSync, copyFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

// The files the docs carry: vendored name -> path inside bw-client-data. The docs draw no answer
// record, so answer-record.js and answer-record.mjs are not vendored here.
// Generated files are checked against VERSION.json "files"; source modules against "sources".
export const FILES = {
  'tokens.css': 'public/assets/brand/tokens.css',
  'components.css': 'public/assets/brand/components.css',
  'nav.js': 'public/assets/brand/nav.js',
  'nav.json': 'brand/nav.json',
  'nav-render.mjs': 'brand/nav-render.mjs',
  'fonts/geist-latin-var.woff2': 'public/assets/brand/fonts/geist-latin-var.woff2',
  'fonts/geist-mono-latin-var.woff2': 'public/assets/brand/fonts/geist-mono-latin-var.woff2',
  'fonts/newsreader-headline-latin.woff2': 'public/assets/brand/fonts/newsreader-headline-latin.woff2',
  'fonts/newsreader-text-latin.woff2': 'public/assets/brand/fonts/newsreader-text-latin.woff2',
  'fonts/LICENSE-Geist-OFL.txt': 'public/assets/brand/fonts/LICENSE-Geist-OFL.txt',
  'fonts/LICENSE-Newsreader-OFL.txt': 'public/assets/brand/fonts/LICENSE-Newsreader-OFL.txt'
};

// The copies MkDocs serves (docs_dir is docs/): served path -> vendored name. The sync writes them
// from the vendored bytes, and the vendor test checks they stay identical. tokens.css and
// components.css are served inside docs/assets/brand/docs.css, byte for byte, ahead of the docs'
// own layer (tools/brand_chrome.mjs writes it; the vendor test checks the embedded bytes).
export const SERVED = {
  'docs/assets/brand/nav.js': 'nav.js',
  'docs/assets/brand/fonts/geist-latin-var.woff2': 'fonts/geist-latin-var.woff2',
  'docs/assets/brand/fonts/geist-mono-latin-var.woff2': 'fonts/geist-mono-latin-var.woff2',
  'docs/assets/brand/fonts/newsreader-headline-latin.woff2': 'fonts/newsreader-headline-latin.woff2',
  'docs/assets/brand/fonts/newsreader-text-latin.woff2': 'fonts/newsreader-text-latin.woff2',
  'docs/assets/brand/fonts/LICENSE-Geist-OFL.txt': 'fonts/LICENSE-Geist-OFL.txt',
  'docs/assets/brand/fonts/LICENSE-Newsreader-OFL.txt': 'fonts/LICENSE-Newsreader-OFL.txt'
};

export function expectedHash(version, from) {
  return (version.files[from] && version.files[from].sha256) || version.sources[from] || null;
}

export function sha256(file) {
  return createHash('sha256').update(readFileSync(file)).digest('hex');
}

const here = dirname(fileURLToPath(import.meta.url));

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  const source = process.argv[2];
  if (!source || !existsSync(join(source, 'brand', 'VERSION.json'))) {
    console.error('usage: node vendor/brand/sync.mjs <path to bw-client-data>');
    process.exit(2);
  }
  const version = JSON.parse(readFileSync(join(source, 'brand', 'VERSION.json'), 'utf8'));
  let commit = '';
  try { commit = execFileSync('git', ['-C', source, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(); } catch { commit = 'unknown'; }
  const record = { package: version.name, version: version.version, built_at: version.built_at, source_commit: commit, synced_by: 'vendor/brand/sync.mjs', files: {} };
  for (const [name, from] of Object.entries(FILES)) {
    const want = expectedHash(version, from);
    if (!want) throw new Error(`VERSION.json does not list ${from}`);
    const target = join(here, name);
    mkdirSync(dirname(target), { recursive: true });
    copyFileSync(join(source, from), target);
    const got = sha256(target);
    if (got !== want) throw new Error(`${from} in the checkout does not match VERSION.json (${got} != ${want})`);
    record.files[name] = { from, sha256: got };
  }
  copyFileSync(join(source, 'brand', 'VERSION.json'), join(here, 'VERSION.json'));
  const repo = join(here, '..', '..');
  for (const [served, name] of Object.entries(SERVED)) {
    mkdirSync(dirname(join(repo, served)), { recursive: true });
    copyFileSync(join(here, name), join(repo, served));
  }
  writeFileSync(join(here, 'VENDORED.json'), JSON.stringify(record, null, 2) + '\n');
  console.log(`vendored brand ${version.version} (${commit.slice(0, 7)}): ${Object.keys(FILES).length} files`);
}
