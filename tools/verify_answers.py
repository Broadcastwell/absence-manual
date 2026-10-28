"""Validate answer pages and their served research links once per build."""

import argparse
import json
from pathlib import Path
import sys
from urllib.request import Request, urlopen

try:
    from tools.library_answers import external_evidence_links, leaf_answers, split_markdown, validate_collection
except ModuleNotFoundError:
    from library_answers import external_evidence_links, leaf_answers, split_markdown, validate_collection

ROOT = Path(__file__).resolve().parents[1]


def check_external_links(docs, opener=urlopen):
    links = set()
    for path in leaf_answers(docs):
        _, body = split_markdown(path.read_text(encoding="utf8"))
        links.update(external_evidence_links(body))
    results, errors = {}, []
    # A set deduplicates URLs for this build; an old successful request is never
    # reused as current proof. HEAD is often blocked, so check a small GET.
    for url in sorted(links):
        try:
            request = Request(url, headers={"User-Agent": "Broadcastwell-library-link-check/1.0"})
            with opener(request, timeout=30) as response:
                status = response.status
                response.read(1)
            results[url] = status
            if status != 200:
                errors.append(f"Evidence URL returned {status}: {url}")
        except Exception as exc:
            results[url] = str(exc)
            errors.append(f"Evidence URL could not be verified: {url}: {exc}")
    return results, errors


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-external", action="store_true")
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    errors = validate_collection(ROOT / "docs")
    results = {}
    if args.check_external:
        results, link_errors = check_external_links(ROOT / "docs")
        errors.extend(link_errors)
    if args.receipt:
        args.receipt.write_text(json.dumps({"results": results, "errors": errors}, indent=2), encoding="utf8")
    if errors:
        print("Answer verification failed:\n" + "\n".join(errors))
        return 1
    print(f"Answer verification passed: {len(leaf_answers(ROOT / 'docs'))} question pages; {len(results)} unique evidence URLs checked.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
