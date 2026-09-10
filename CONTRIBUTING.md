# Contributing

Bug reports, documentation improvements, and focused pull requests are welcome in English or Chinese. This is a community-maintained adaptation, not an officially endorsed university project.

## Reporting a problem

Include the compiler and TeX Live versions, operating system or Overleaf setting, a minimal `.tex` example, and the relevant error text. For layout issues, name the affected page and describe the expected result. Remove names, student IDs, private research, local account paths, and credentials from attachments and logs. Only attach artwork or screenshots you are permitted to share.

## Making a change

1. Keep one purpose per pull request and explain the visible effect.
2. Preserve the supported XeLaTeX / 16:9 / 11 pt setup and portable TeX Live fonts.
3. Keep original artwork unchanged unless the replacement and its permissions are explicitly reviewed. Do not claim newer branding or official endorsement without evidence.
4. Update the corresponding English and Chinese user documents when a public interface changes.
5. Do not commit `build/`, `dist/`, scratch exports, original PPTs, local environments, or private data. The curated PNGs and example PDFs listed in `previews/README.md` are documentation and should be refreshed with relevant visual changes.

## Documentation language

Maintain complete English and Chinese versions of the repository READMEs, `docs/USAGE.md` / `docs/USAGE.zh.md`, and `overleaf/README.md` / `overleaf/README.zh.md`. Keep corresponding instructions and options aligned; examples and previews may use their own language.

Contributor documentation, testing instructions, the changelog, and directory indexes use English. `LICENSE` retains the original English MIT text; `NOTICE.md` is the canonical artwork-rights and provenance reference. Reports and contributions in either English or Chinese are welcome.

## Verification

Packaging tests need only Python 3.10 or later:

```sh
python -m unittest discover -s tests -p 'test_*.py' -v
```

For layout or example changes, compile all six fixtures and run the PDF checks in [docs/VALIDATION.md](docs/VALIDATION.md). Optional QA dependencies can be installed into a virtual environment with:

```sh
python -m pip install -r requirements-dev.txt
```

The GitHub workflow repeats compilation and PDF checks on Linux. Passing CI is not a substitute for inspecting the affected pages, and is not evidence of Overleaf cloud verification or artwork permission.

Changes to release contents must update the explicit source-to-archive mapping in `tools/package.py` and the packaging tests. The ZIP uses the dedicated READMEs from `overleaf/`, not the repository's preview-rich READMEs. Build it, check its documentation links, extract it into a fresh directory, and compile from that directory before distributing a release. Details, including preview maintenance, are in [docs/VALIDATION.md](docs/VALIDATION.md).

## Contribution licensing

By submitting original code or documentation for inclusion, you agree to license those contributions under the project's [MIT License](LICENSE). Do not submit third-party content unless you can document permission to include and redistribute it. CityU artwork is separately governed by [NOTICE.md](NOTICE.md); the code license does not cover it. You retain ownership of your contributions.
