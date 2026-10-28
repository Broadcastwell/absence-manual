"""Regenerate only the Answers section, preserving every other llms.txt byte."""

from pathlib import Path
import re
import sys

try:
    from tools.library_answers import page_url, split_markdown
except ModuleNotFoundError:
    from library_answers import page_url, split_markdown

ROOT = Path(__file__).resolve().parents[1]
ANSWERS_HEADING = re.compile(rb"(?m)^## Answers\r?$\n?")


def answers_section(docs):
    docs = Path(docs)
    entries = []
    for source in (docs / "answers").rglob("*.md"):
        meta, _ = split_markdown(source.read_text(encoding="utf8"))
        relative = source.relative_to(docs)
        order = (0 if len(relative.parts) == 2 else 1 if source.name == "index.md" else 2,
                 int(meta.get("library_order", 999999)), relative.as_posix())
        entries.append((order, meta, relative))
    lines = ["## Answers", ""]
    for _, meta, relative in sorted(entries, key=lambda item: item[0]):
        title = " ".join(str(meta["title"]).split()).replace("[", "").replace("]", "")
        answer = " ".join(str(meta["description"]).split())
        lines.append(f"- [{title}]({page_url(relative)}): {answer}")
    return "\n".join(lines) + "\n"


def regenerate(original, section):
    """Operate on bytes so the dated price block and line endings cannot drift."""
    headings = list(ANSWERS_HEADING.finditer(original))
    if len(headings) > 1:
        raise ValueError("The Answers heading is repeated")
    encoded = section.encode("utf8")
    if not headings:
        return original + (b"" if original.endswith(b"\n\n") else b"\n" if original.endswith(b"\n") else b"\n\n") + encoded
    left = headings[0].start()
    following = re.search(rb"(?m)^## ", original[headings[0].end():])
    right = headings[0].end() + following.start() if following else len(original)
    return original[:left] + encoded + (b"\n" if following else b"") + original[right:]


def main():
    path = ROOT / "docs" / "llms.txt"
    if not (ROOT / "docs" / "answers").exists():
        print("No Answers source section exists yet; llms.txt is unchanged.")
        return
    original = path.read_bytes()
    generated = regenerate(original, answers_section(ROOT / "docs"))
    if "--check" in sys.argv:
        if generated != original:
            raise SystemExit("llms.txt Answers section needs regeneration")
        print("llms.txt Answers section matches the source pages.")
    else:
        path.write_bytes(generated)
        print("Regenerated the Answers section; all other llms.txt bytes preserved.")


if __name__ == "__main__":
    main()
