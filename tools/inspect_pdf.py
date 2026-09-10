# SPDX-License-Identifier: MIT
"""Render a Beamer PDF for local visual QA (optional dependency: PyMuPDF)."""

import argparse
import json
import math
import sys
from pathlib import Path

import pymupdf


def inspect_pdf(pdf_path: Path, output_dir: Path, dpi: int) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = {"file": pdf_path.name, "pages": [], "issues": []}
    with pymupdf.open(pdf_path) as document:
        for existing in output_dir.glob("page-*.png"):
            suffix = existing.stem.removeprefix("page-")
            if suffix.isdigit() and int(suffix) > len(document):
                report["issues"].append(f"Stale preview {existing.name}; use a new output directory")
        checked_fonts = set()
        for index, page in enumerate(document):
            page_number = index + 1
            page.get_pixmap(dpi=dpi, alpha=False).save(
                output_dir / f"page-{page_number:02}.png"
            )
            text = page.get_text()
            report["pages"].append(
                {
                    "page": page_number,
                    "width_pt": round(page.rect.width, 3),
                    "height_pt": round(page.rect.height, 3),
                    "text": text.strip(),
                }
            )
            if abs(page.rect.width / page.rect.height - 16 / 9) > 0.002:
                report["issues"].append(f"Page {page_number}: not 16:9")
            if not text.strip():
                report["issues"].append(f"Page {page_number}: no selectable text")
            safe_page = page.rect + (-1, -1, 1, 1)
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        if not safe_page.contains(pymupdf.Rect(span["bbox"])):
                            report["issues"].append(
                                f"Page {page_number}: text outside page: {span['text']!r}"
                            )
            for font in page.get_fonts():
                xref = font[0]
                if xref not in checked_fonts:
                    checked_fonts.add(xref)
                    if not document.extract_font(xref)[3]:
                        report["issues"].append(f"Font is not embedded: {font[3]}")

        columns = 2 if len(document) <= 8 else 3
        tile_width, tile_height = 480, 270
        gap, label_height = 16, 22
        rows = math.ceil(len(document) / columns)
        with pymupdf.open() as contact:
            sheet = contact.new_page(
                width=columns * (tile_width + gap) + gap,
                height=rows * (tile_height + label_height + gap) + gap,
            )
            for index in range(len(document)):
                x = gap + (index % columns) * (tile_width + gap)
                y = gap + (index // columns) * (tile_height + label_height + gap)
                sheet.insert_text((x, y + 12), f"{pdf_path.stem} / {index + 1:02}", fontsize=10)
                box = pymupdf.Rect(x, y + label_height, x + tile_width, y + label_height + tile_height)
                sheet.show_pdf_page(box, document, index)
                sheet.draw_rect(box, color=(0.82, 0.82, 0.84), width=0.5)
            sheet.get_pixmap(alpha=False).save(output_dir / "contact-sheet.png")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return report


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()
    report = inspect_pdf(args.pdf, args.output, args.dpi)
    raise SystemExit(1 if report["issues"] else 0)


if __name__ == "__main__":
    main()
