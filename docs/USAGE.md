# Usage and customisation

[English](USAGE.md) · [简体中文](USAGE.zh.md) · [Home](../README.md)

## Supported document setup

```latex
\documentclass[aspectratio=169,11pt,t]{beamer}
\usetheme{CityU}
```

Use XeLaTeX and a 16:9 slide. Other aspect ratios stretch the original artwork and are outside the tested layout. The examples use 11 pt body text; other sizes and unusually dense slides need their own visual checks. pdfLaTeX and LuaLaTeX are intentionally not supported by this theme.

The fonts are selected from TeX Live by filename: TeX Gyre Heros (sans), Termes (serif), Cursor (monospace), and Latin Modern mathematics. No Arial, Microsoft YaHei, or other operating-system font is required. All images have relative paths. No SVG conversion, shell escape, external diagram generator, or bibliography processor is needed for the examples.

## Importing into Overleaf

1. Choose **New Project → Upload Project** and upload `cityu-beamer-overleaf.zip`.
2. Select **XeLaTeX** in the project settings and use the newest stable TeX Live version available to your account.
3. Set the main document to [main.tex](../main.tex) for English, [example-zh.tex](../example-zh.tex) for Chinese, or [minimal.tex](../minimal.tex) for a short starting point.
4. Recompile. References and total frame numbers may need more than one pass; recompile again if they have not settled.
5. Check logos, long titles, Chinese characters, equations, and counters. The English example has 18 PDF pages and 11 numbered frames; the Chinese example has 11 pages and 7 numbered frames; the minimal example has 4 pages and 1 numbered frame.

The ZIP has a root-level main document, theme, `latexmkrc`, four backgrounds in `assets/`, both usage guides, and license notices. Its READMEs are dedicated import instructions. You do not need the original PPT, repository previews, Python tools, or a local TeX installation to compile on Overleaf.

Clean local import builds have been checked with TeX Live 2026. Actual Overleaf cloud compilation and older TeX Live versions have not been verified. The [Gallery submission policy](https://docs.overleaf.com/templates/submitting-to-the-overleaf-template-gallery) excludes unofficial university presentation templates; this community adaptation does not become eligible merely by compiling successfully. Official status and artwork permissions must be established separately.

## Local compilation

Keep `beamerthemeCityU.sty`, `latexmkrc`, and the complete `assets/` directory beside the main document. Use a TeX Live installation with Beamer, fontspec, Latin Modern, TeX Gyre, TikZ, and booktabs; the Chinese example also needs ctex and Fandol. Run from that directory:

```sh
latexmk -xelatex -outdir=build main.tex
latexmk -xelatex -outdir=build example-zh.tex
latexmk -xelatex -outdir=build minimal.tex
```

The supplied `latexmkrc` also selects XeLaTeX when you run `latexmk main.tex`. Python is only used by repository maintenance tools, not by the theme or these examples.

## Metadata and footer

```latex
\title[Short footer title]{A longer presentation title}
\subtitle{An optional subtitle}
\author{Your Name}
\institute{Department / Research Group\\City University of Hong Kong}
\date{\today}
\cityufooter{A custom footer, if preferred}
```

The short title defaults to the footer text and links back to the start of the presentation. Use the optional short argument when the full title is long. `\cityufooter{...}` replaces that text; `\cityufooter{}` leaves only the rule and counter. To hide the entire footer, use the `footer=false` theme option.

Keep the footer on one line. The cover is designed for a title of up to two lines, a short subtitle, and about four lines of author/institute/date metadata. It does not automatically shrink long text: split or shorten it, or adjust the corresponding Beamer font size. Check long author lists and `\and` layouts yourself.

## Page commands

| Command | Behaviour |
| --- | --- |
| `\cityutitlepage` | Creates a plain, unnumbered cover using the document metadata. |
| `\section{Title}` | Creates an automatic unnumbered section divider by default. |
| `\section*{Title}` | Does not create an automatic divider. |
| `\cityusectionpage` | Creates an unnumbered divider for the current section. |
| `\cityuclosing{Thank you}` | Creates a plain, unnumbered closing page. |
| `\cityuclosing[Questions and discussion]{Thank you}` | Adds a subtitle to the closing page. |

These commands create complete frames; do not put them inside another `frame`. Only the helper commands automatically set `plain,noframenumbering`. The native templates can also be used explicitly:

```latex
\begin{frame}[plain,noframenumbering]
  \titlepage
\end{frame}
```

The same pattern works with `\sectionpage`. If you create manual section dividers, disable automatic ones to avoid duplicates:

```latex
\usetheme[sectionpages=false]{CityU}
% Later, outside any frame:
\section{Methods}
\cityusectionpage
```

The theme uses Beamer's `\AtBeginSection` hook. Installing another hook after loading the theme replaces the automatic-divider behaviour. Subsections do not add divider pages.

## Theme options

| Option | Default | Effect |
| --- | --- | --- |
| `sectionpages=true` / `false` | `true` | Enable or disable automatic section dividers. |
| `footer=true` / `false` | `true` | Show or hide the footer on ordinary frames. |
| `assetspath=directory` | `assets` | Use a relative directory containing all four named PNGs. |

Example:

```latex
\usetheme[sectionpages=false,footer=true,assetspath=brand]{CityU}
```

The custom directory must contain `title.png`, `section.png`, `content.png`, and `closing.png`. Use forward slashes, exact filename case, and preferably an ASCII directory name without spaces for cross-platform builds. Keep the images at 16:9 and confirm the right to use any replacement artwork.

## Chinese and bilingual documents

Load ctex before the theme, as in `example-zh.tex`:

```latex
\usepackage[UTF8,fontset=fandol]{ctex}
\usetheme{CityU}
```

This uses Fandol Chinese fonts and Chinese figure/table labels. Add `scheme=plain` to the ctex options if you want Chinese text with English-style labels. Fandol is not a complete collection of every rare CJK character; check the log when adding unusual names or characters.

## Ordinary Beamer content

Use standard `frame`, `columns`, `itemize`, `enumerate`, `block`, `alertblock`, and `exampleblock` environments. Mathematics, `booktabs` tables, native TikZ figures, and `thebibliography` are demonstrated in `main.tex`. Frames containing `verbatim` require `[fragile]`.

The footer counts frames, not physical PDF pages. Overlays such as `<+->` retain one frame number. Cover, divider, and closing helper pages are excluded. User-created frames remain counted unless they specify `noframenumbering`; there is no special appendix-numbering feature or extra appendix package dependency.

Normal frame titles reserve space for the top-right logo and wrap with a ragged right edge. Keep titles to two lines where possible. Avoid placing large images or manual overlays over the logo or footer; the theme cannot prevent arbitrary user-drawn content from covering them. Use `width=\linewidth` inside columns instead of the full paper width.

## Small visual adjustments

After loading the theme, standard Beamer customisation remains available:

```latex
\setbeamerfont{title}{size=\fontsize{22}{26},series=\bfseries}
\setbeamerfont{frametitle}{size=\fontsize{18}{21},series=\bfseries}
\setbeamercolor{alerted text}{fg=CityURed}
```

Available colours are `CityURed`, `CityUInk`, `CityUMuted`, `CityULine`, `CityUPaper`, and `CityUTeal`. Changes to the theme's typesetting are separate from permission to modify university branding.

## Troubleshooting

- **"This theme requires XeLaTeX"**: change the project compiler; do not convert the source to pdfLaTeX.
- **Missing `beamerthemeCityU.sty`**: restore/upload the supplied theme file beside the main document and compile from that directory; it is not a TeX Live package.
- **Missing dependency `.sty` or font files**: install the named TeX Live package, not a Windows font. A complete Overleaf TeX Live image normally supplies these dependencies.
- **Missing background**: compile from the project root; check `assetspath`, filenames, and case. Upload all four PNGs.
- **Incorrect total / unresolved citation**: run `latexmk` or compile again so Beamer's auxiliary files settle.
- **Overflow or crowded slide**: shorten the content or split the frame; do not assume a successful build guarantees good layout.
- **No automatic divider**: check `sectionpages`, starred sections, and any later `\AtBeginSection` hook.

For artwork provenance and reuse terms, see [NOTICE.md](../NOTICE.md).
