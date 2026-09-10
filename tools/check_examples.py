# SPDX-License-Identifier: MIT
"""Check example frame numbering and the real option fixtures after compilation."""

import re
from pathlib import Path

import pymupdf


def main() -> None:
    # Each position represents a physical PDF page. None means no frame counter.
    cases = [
        ("minimal", 1, [None, None, 1, None]),
        ("main", 11, [None, 1, None, 2, 3, 4, 4, 4, None, 5, 6, 7, 8, None, 9, 10, 11, None]),
        ("example-zh", 7, [None, 1, None, 2, 3, None, 4, 5, 6, 7, None]),
        ("options", 2, [None, None, None, None]),
        ("sections", 2, [None, None, 1, 2, None]),
        ("assetspath-check/build/manual-pages", 2, [None, None, 1, 2, None]),
    ]
    failures = []
    for name, total, numbers in cases:
        path = Path("build") / f"{name}.pdf"
        expected = [None if number is None else (number, total) for number in numbers]
        with pymupdf.open(path) as document:
            observed = []
            texts = []
            for page in document:
                text = page.get_text()
                texts.append(text)
                matches = re.findall(r"(?m)^\s*(\d+)\s*/\s*(\d+)\s*$", text)
                observed.append(tuple(map(int, matches[0])) if len(matches) == 1 else None)
                if len(matches) > 1:
                    failures.append(f"{name}: multiple counters on one page")
            if observed != expected:
                failures.append(f"{name}: counter sequence {observed!r}, expected {expected!r}")
            if name == "options" and any("HIDDEN FOOTER SENTINEL" in text for text in texts):
                failures.append("options: disabled footer is visible")
            if name.endswith("manual-pages"):
                presence = ["CUSTOM FOOTER SENTINEL" in text for text in texts]
                if presence != [False, False, True, True, False]:
                    failures.append("manual-pages: custom footer leaks or is missing")
            print(f"CHECK: {path} ({len(document)} pages)")
    for failure in failures:
        print(f"FAIL: {failure}")
    if not failures:
        print("PASS: all six PDF fixtures have the expected frame counts and footer behaviour")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
