# Changelog

Changes to the theme and its supporting files.

## 1.0.1 — 2026-09-10

First public release. Retains the version number already used by the theme and documentation; earlier version labels were local development milestones, not published GitHub releases.

### Added

- A XeLaTeX / 16:9 Beamer adaptation of the supplied January 2025 CityUHK PPT, with four original backgrounds and editable LaTeX content.
- English, Chinese, and minimal examples; configurable section dividers, footer, and artwork directory; overlay-aware frame numbering.
- Language-specific README overviews and complete PDF examples in `previews/`, kept separate from the Overleaf ZIP.
- Complete English and Chinese usage guides, including Overleaf import instructions; contributor and maintenance documentation in English.
- MIT licensing for original code and documentation, with CityU artwork explicitly excluded and its provenance and rights documented in `NOTICE.md`.
- A reproducible, source-only 16-file Overleaf ZIP, dedicated package READMEs, SHA-256 output, and explicit overwrite protection.
- Packaging regression checks for dedicated instructions, independence from repository-only files, and working documentation links inside the actual ZIP.
- A read-only Ubuntu CI workflow covering compilation, PDF layout, frame numbering, custom artwork paths, and clean-ZIP imports. Releases are published manually, not on each push.

### Refined during development

- Moved content frame titles down by 3.7 mm.
- Removed the extra gap below the title to preserve space on dense slides.
- Preserved all example text, fonts, logo placement, and special-page layouts.
- Kept the repository lean, with contribution guidance and automated checks but no redundant issue or pull request templates.

### Fixed

- Explicitly install the separate TeX Gyre OpenType font package in Ubuntu CI.
- Declare fontspec's `no-math` option before ctex in the Chinese example, READMEs, and usage guides to avoid option clashes on older TeX Live versions.
