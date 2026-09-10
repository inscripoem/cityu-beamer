# Testing and maintenance

[Home](../README.md) · [Contributing](../CONTRIBUTING.md)

Run these checks when changing the theme, examples, documentation, or package contents. The supported layout is XeLaTeX, 16:9, and 11 pt; use TeX Live 2026 as the reference environment. Checks on older TeX Live versions or other layouts must be reported separately.

## Prerequisites

Use Python 3.10 or later. Packaging tests require only the standard library. PDF inspection additionally requires the pinned dependency in [requirements-dev.txt](../requirements-dev.txt); install it into a virtual environment:

```sh
python -m pip install -r requirements-dev.txt
```

Use that environment's Python for the commands below. Compilation needs `latexmk`, XeLaTeX, and the TeX packages listed in the [usage guide](USAGE.md). Run commands from the repository root unless stated otherwise.

## Packaging tests

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
```

The tests build real temporary archives. They check the payload and file bytes, dedicated package READMEs, independence from repository-only files, local documentation links inside the actual ZIP, checksums, reproducibility, overwrite protection, safe failure on missing inputs, and invocation from another working directory.

## Compile the fixtures

```sh
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build minimal.tex
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build example-zh.tex
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build tests/options.tex
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build tests/sections.tex
```

The sixth fixture tests relocated artwork. In a fresh `build/assetspath-check/` directory, place `beamerthemeCityU.sty`, `latexmkrc`, and `tests/manual-pages.tex`. Copy the four PNGs from `assets/` into its `brand/` subdirectory. Do not create an `assets/` directory there. From `build/assetspath-check/`, run:

```sh
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build manual-pages.tex
```

Expected fixture behaviour:

| Source | PDF pages | Main check |
| --- | ---: | --- |
| `minimal.tex` | 4 | One numbered content frame and all four page types |
| `main.tex` | 18 | Eleven numbered frames; overlays retain a single frame number |
| `example-zh.tex` | 11 | Seven numbered frames; Chinese text and layouts |
| `tests/options.tex` | 4 | Disabled automatic dividers and footer |
| `tests/sections.tex` | 5 | Ordinary sections create dividers; starred sections do not |
| `tests/manual-pages.tex` | 5 | Native page templates, custom footer, and `assetspath=brand` |

Review compiler errors, missing-character diagnostics, warnings, and overfull/underfull boxes. Font information mentioning the word "warning" is not itself a compiler diagnostic. Do not use a successful exit code alone as proof of a clean layout.

## PDF checks and visual review

Return to the repository root and run:

```sh
python tools/check_examples.py
python tools/check_layout.py build/minimal.pdf --page 3
python tools/check_layout.py build/main.pdf --page 13
python tools/check_layout.py build/example-zh.pdf --page 5
python tools/inspect_pdf.py build/main.pdf --output build/preview-main
python tools/inspect_pdf.py build/example-zh.pdf --output build/preview-zh
python tools/inspect_pdf.py build/minimal.pdf --output build/preview-minimal
```

`check_examples.py` checks page and frame-number expectations across all six PDFs. `check_layout.py` checks logo visibility, title placement, and footer margins on representative content pages. `inspect_pdf.py` renders pages and a contact sheet, and reports dimensions, text bounds, and embedded fonts. Review the affected pages for long titles, Chinese text, overlays, columns, equations, tables, and logo/footer overlap.

Use fresh render directories when necessary. The inspector rejects stale page images beyond the new PDF's page count; it does not delete old previews. These checks complement visual inspection and do not prove that arbitrary future slides are unclipped or accessible.

## Maintain the curated previews

When a visual change is intentional and the checks pass, refresh the corresponding complete PDF and overview together:

| Built example | PDF in `previews/` | Contact sheet in `previews/` |
| --- | --- | --- |
| `build/main.pdf` | `cityu-beamer-en.pdf` | `overview-en.png` from `build/preview-main/contact-sheet.png` |
| `build/example-zh.pdf` | `cityu-beamer-zh.pdf` | `overview-zh.png` from `build/preview-zh/contact-sheet.png` |
| `build/minimal.pdf` | `cityu-beamer-minimal.pdf` | `overview-minimal.png` from `build/preview-minimal/contact-sheet.png` |

Keep the English and Chinese README images language-specific. Individual page renders remain in `build/`; new curated filenames must be explicitly allowed in `.gitignore`. See the [preview index](../previews/README.md) for the maintained set and [NOTICE.md](../NOTICE.md) for artwork rights.

## Build and inspect the Overleaf ZIP

```sh
python tools/package.py
```

This produces `dist/cityu-beamer-overleaf.zip` and its `.zip.sha256` sidecar. The script refuses existing output unless you intentionally use `python tools/package.py --force`.

The explicit source-to-archive mapping in [tools/package.py](../tools/package.py) includes only the theme, three examples, build configuration, four backgrounds, artwork index, license notices, and both usage guides. The dedicated [English](../overleaf/README.md) and [Chinese](../overleaf/README.zh.md) import instructions become `README.md` and `README.zh.md` at the archive root. Paths written in those instructions refer to the extracted project root. Repository READMEs, previews, maintenance documents, tests, tools, original PPTs, caches, and local notes are not shipped.

Entries use forward slashes, sorted names, and fixed timestamps. Identical inputs with the same Python/zlib environment produce identical ZIP bytes. Keep the checksum with the ZIP and verify it after copying or downloading.

Before distributing a package, extract it into a new empty directory. The example below assumes `build/zip-import/` does not already exist; otherwise choose a fresh destination:

```sh
python -m zipfile -e dist/cityu-beamer-overleaf.zip build/zip-import
cd build/zip-import
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build example-zh.tex
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build minimal.tex
```

Check all three final logs and the generated PDFs, as well as the package's documentation links. A clean local import checks the package's self-contained compilation inputs; it is not an actual Overleaf cloud test. See the usage guide for cloud verification limits and Gallery eligibility.

## Continuous integration

[The GitHub workflow](../.github/workflows/latex.yml) runs packaging tests, all six fixtures, PDF checks, and fresh ZIP-import builds on Ubuntu. It has read-only repository permissions and does not publish artifacts or releases. Inspect the run for the relevant commit rather than inferring success from the presence of a workflow file.

Keep user-facing instructions aligned in English and Chinese, check repository links separately from ZIP links, and record test evidence in the pull request. Do not put machine-specific paths, first-upload walkthroughs, or historical execution logs into public user documentation.
