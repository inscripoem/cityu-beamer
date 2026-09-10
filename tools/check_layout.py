# SPDX-License-Identifier: MIT
"""Regression checks for content-title spacing, logo and footer (requires PyMuPDF)."""

import argparse
import re

import pymupdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf")
    parser.add_argument("--page", type=int, default=3, help="1-based content page")
    parser.add_argument("--background", default="assets/content.png")
    args = parser.parse_args()
    failures = []
    with pymupdf.open(args.pdf) as document, pymupdf.open() as reference:
        page = document[args.page - 1]
        width, height = page.rect.width, page.rect.height
        layout = page.get_text("dict")
        title_spans = [
            span
            for block in layout["blocks"]
            for line in block.get("lines", [])
            for span in line["spans"]
            if span["text"].strip() and span["size"] >= 18
            and span["bbox"][1] < height * 0.35
        ]
        if not title_spans:
            failures.append("Expected a standard-size content frame title")
        else:
            title_top_mm = min(span["bbox"][1] for span in title_spans) * 25.4 / 72
            # Allow for the different Latin/CJK font bounding boxes around 7-8 mm.
            if not 6.5 <= title_top_mm <= 8.5:
                failures.append(f"Content title has insufficient or excessive top space ({title_top_mm:.2f} mm)")
            else:
                print(f"PASS: content title has {title_top_mm:.2f} mm top space")
        expected = reference.new_page(width=width, height=height)
        expected.insert_image(expected.rect, filename=args.background)
        logo = pymupdf.Rect(width * 0.83, height * 0.045, width * 0.97, height * 0.21)
        actual_pixels = page.get_pixmap(clip=logo, dpi=144, alpha=False).samples
        expected_pixels = expected.get_pixmap(clip=logo, dpi=144, alpha=False).samples
        mean_difference = sum(abs(a - b) for a, b in zip(actual_pixels, expected_pixels)) / len(expected_pixels)
        changed_fraction = sum(abs(a - b) > 10 for a, b in zip(actual_pixels, expected_pixels)) / len(expected_pixels)
        if len(actual_pixels) != len(expected_pixels) or mean_difference > 2.5 or changed_fraction > 0.005:
            failures.append(
                f"Logo is obscured (mean difference {mean_difference:.2f}; "
                f"changed channels {changed_fraction:.2%})"
            )
        else:
            print(f"PASS: content logo matches original artwork ({mean_difference:.2f})")

        counters = []
        for block in layout["blocks"]:
            for line in block.get("lines", []):
                text = "".join(span["text"] for span in line["spans"])
                if re.fullmatch(r"\s*\d+\s*/\s*\d+\s*", text):
                    counters.append(line["bbox"])
        if len(counters) != 1:
            failures.append(f"Expected one footer counter, found {len(counters)}")
        else:
            right_margin_mm = (width - counters[0][2]) * 25.4 / 72
            if not 9.5 <= right_margin_mm <= 10.5:
                failures.append(f"Footer counter is not at its 10 mm margin ({right_margin_mm:.2f} mm)")
            else:
                print(f"PASS: footer counter has {right_margin_mm:.2f} mm right margin")

    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(bool(failures))


if __name__ == "__main__":
    main()
