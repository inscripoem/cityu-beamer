---
name: cityu-beamer
description: Create CityU Beamer PDF presentations and editable LaTeX source from an outline in this repository. Use for English, Chinese, or bilingual slides based on the existing CityU theme.
---

# CityU Beamer

Use the existing CityU theme to turn an outline into a presentation. This initial instruction-only skill requires the complete repository checkout; standalone packaging and automated helpers are still being developed in [issue #2](https://github.com/inscripoem/cityu-beamer/issues/2).

## Locate the template

Resolve paths relative to this skill directory: the repository root is `../../..`. Read [the usage guide](../../../docs/USAGE.md) for the supported setup and theme commands. Start from [minimal.tex](../../../minimal.tex); consult [example-zh.tex](../../../example-zh.tex) when Chinese text is needed and [main.tex](../../../main.tex) for richer layouts.

## Prepare the presentation

- Use the supplied outline and optional metadata, language, slide count, duration, and source materials. An outline alone is enough for a draft; leave missing author details blank and mark missing evidence or citations for the user to supply.
- Create a fresh presentation directory under the repository's `build/` directory, or use the user's requested output location. Keep generated work separate from the original examples and avoid replacing existing user files.
- Place the generated `main.tex`, `beamerthemeCityU.sty`, `latexmkrc`, and the complete `assets/` directory together in that presentation directory. Reuse the repository resources and preserve the existing artwork.
- Preserve XeLaTeX, 16:9, 11 pt, and the portable TeX Live fonts. For Chinese text, pass `no-math` to fontspec before loading ctex, following the Chinese example's preamble.
- Use the theme's title, section, content, and closing pages. The title and closing helpers create complete frames; do not nest them inside a `frame`. Automatic section dividers are enabled by default.
- Split dense content into additional frames and keep images within the available column width, clear of the logo and footer. Replace example content with the user's material; do not treat sample research data as real evidence.

## Compile and inspect

Check that `latexmk`, XeLaTeX, and the dependencies in the usage guide are available. Run from the generated presentation directory:

```sh
latexmk -xelatex -latexoption=-no-shell-escape -interaction=nonstopmode -halt-on-error -file-line-error -outdir=build main.tex
```

Use the log to identify compilation errors, missing glyphs, unresolved references, and overflowing content. If dependencies are unavailable or compilation cannot be repaired, preserve the source and report the specific blocker instead of claiming a finished PDF.

For rendered previews, use `tools/inspect_pdf.py` from the repository as documented in [the PDF inspection guide](../../../docs/VALIDATION.md#pdf-checks-and-visual-review). Inspect the generated slides for clipping, overlap, and unreadable content. The guide's `check_examples.py` checks fixed repository fixtures, not arbitrary generated presentations.

Deliver the PDF when compilation succeeds, editable source with its required resources, and available previews. State which checks were actually completed. This workflow produces PDF and LaTeX; if the user requires editable `.pptx`, explain that this output needs a separate implementation rather than silently substituting a PDF or slide screenshots.
