# Changelog

Changes to the theme and its supporting files.

## Unreleased

### Changed

- Aligned English and Chinese READMEs and added a complete Chinese usage guide.
- Integrated Overleaf import instructions into both usage guides.
- Standardised contributor and maintenance documentation in English; consolidated artwork provenance and rights in `NOTICE.md`.
- Removed first-upload tutorials and historical execution records from public documentation.
- Reduced the Overleaf ZIP to compilation inputs, license notices, and user documentation, with dedicated package READMEs instead of repository previews.
- Removed redundant issue and pull request templates; retained contribution guidance and automated compilation checks.

### Added

- Packaging regression checks for dedicated instructions, independence from repository-only files, and working documentation links inside the actual ZIP.

### Fixed

- Explicitly install the separate TeX Gyre OpenType font package in Ubuntu CI.
- Declare fontspec's `no-math` option before ctex in the Chinese example, READMEs, and usage guides to avoid option clashes on older TeX Live versions.

## 1.0.1 — 2026-09-08

### Changed

- Moved content frame titles down by 3.7 mm.
- Removed the extra gap below the title to preserve space on dense slides.
- Preserved all example text, fonts, logo placement, and special-page layouts.

### Added

- Repository ignore and line-ending rules, and contribution guidance.
- Explicit artwork provenance and licensing notices.
- A Linux GitHub Actions compilation workflow and optional pinned PDF-check dependencies.
- A source-only Overleaf packager with an explicit file list, SHA-256 output, overwrite protection, and regression tests.
- Language-specific README overviews and versioned curated PDFs/contact sheets in `previews/`, kept separate from the lean Overleaf ZIP.

## 1.0.0 — 2026-09-08

- Initial XeLaTeX / 16:9 Beamer adaptation of the supplied January 2025 PPT.
- Four original backgrounds with editable LaTeX content.
- English, Chinese, and minimal examples; configurable dividers, footer and asset directory.
- MIT license for original code and documentation, with CityU branding explicitly excluded.
- Compilation, PDF-layout, frame-numbering, and clean-ZIP checks.
