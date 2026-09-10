# CityU Beamer — Overleaf package

[English](README.md) · [简体中文](README.zh.md)

Theme v1.0.1 · XeLaTeX · 16:9 · January 2025 PPT artwork

A community adaptation of the City University of Hong Kong PowerPoint template, not an officially endorsed university template. All paths below refer to the extracted project root.

## Compile

1. Upload `cityu-beamer-overleaf.zip` using Overleaf's **New Project → Upload Project**.
2. Select **XeLaTeX** in the project settings and use the newest stable TeX Live version available to your account.
3. Set the main document to `main.tex` (English), `example-zh.tex` (Chinese), or `minimal.tex` (a short starting point).
4. Recompile and check the text, logos, and frame numbers. If references or totals have not settled, recompile again.

Keep `beamerthemeCityU.sty`, `latexmkrc`, and the complete `assets/` directory beside the main document. The original PPT, preview PDFs, and Python tools are not needed.

Full usage and customisation: `docs/USAGE.md` (English) and `docs/USAGE.zh.md` (Chinese). For local builds, run `latexmk -xelatex -outdir=build main.tex` from the project root.

## Status and licensing

Clean local import builds have been checked with TeX Live 2026; actual Overleaf cloud compilation has not been verified. Gallery eligibility is separate from compilation compatibility; see the usage guide.

Original code and documentation use the MIT license in `LICENSE`. CityU artwork is excluded; read `NOTICE.md` for provenance and rights before sharing the branded package.
