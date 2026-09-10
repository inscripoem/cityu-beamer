# Shared agent skills

Contribute the OpenCode and Codex workflow for [issue #2](https://github.com/inscripoem/cityu-beamer/issues/2) in **`.agents/skills/cityuhk-beamer/`**. This is the canonical source for both tools; keep their core instructions and helpers together.

## Current scope

[cityuhk-beamer/SKILL.md](cityuhk-beamer/SKILL.md) provides an initial, instruction-only entry point using this repository's existing theme, examples, and tools. It requires a complete repository checkout. Automated generation helpers, standalone installation, editable PowerPoint export, and validation in both agent hosts remain follow-up work in issue #2.

Both [Codex](https://learn.chatgpt.com/docs/build-skills) and [OpenCode](https://opencode.ai/docs/skills/) document project-local discovery under `.agents/skills/`. Start the agent in this repository and request the `cityuhk-beamer` skill. Record the host and version when testing discovery or generation; the directory layout alone is not evidence of an end-to-end test.

## Naming

Use **CityUHK** in prose and display names and **cityuhk** in lowercase names. The shared skill name and directory are `cityuhk-beamer`. Follow the repository [naming convention](../../CONTRIBUTING.md#naming) when referencing existing template interfaces.

## Where to contribute

Paths below are relative to the repository root. Create the optional directories only when adding their first working resource.

| Location | Contribution |
| --- | --- |
| `.agents/skills/cityuhk-beamer/SKILL.md` | Shared discovery metadata and concise instructions for the generation workflow. |
| `.agents/skills/cityuhk-beamer/references/` (as needed) | Detailed input conventions, layout guidance, and example outlines linked from the skill. |
| `.agents/skills/cityuhk-beamer/scripts/` (as needed) | Working helpers used specifically by the skill for generation, compilation, or validation. |
| `tests/skills/` (as needed) | Behavioral tests and fixtures for those helpers and their delivered output. |
| `beamerthemeCityU.sty`, `assets/`, and the root `.tex` examples | The existing template sources; reuse these rather than maintaining another copy inside the skill. |
| `tools/` | Utilities shared with ordinary template maintenance, such as PDF inspection. |

Keep the skill name and folder name `cityuhk-beamer` aligned. Resolve repository resources relative to the skill's location, and put generated presentations and scratch files in a fresh directory under `build/` or a user-selected output location. A future standalone package must explicitly address resource bundling and versioning before claiming to work outside this checkout.

## Contribution and review conventions

- Keep shared instructions in English. Maintain the repository's paired English and Chinese user documentation when adding public usage or installation steps.
- Keep `SKILL.md` concise; link detailed references and executable helpers when they are introduced. Add complete resources rather than empty placeholder directories.
- Link incremental PRs with `Related to #2`; reserve closing keywords for a change that completes the agreed issue scope.
- Follow [CONTRIBUTING.md](../../CONTRIBUTING.md) and the applicable checks in [docs/VALIDATION.md](../../docs/VALIDATION.md). For new helpers, validate their observable behavior and include the commands and results in the PR.
- Report compilation, visual inspection, and agent-host checks separately. Do not describe PDF output as editable `.pptx` output.

The Overleaf archive uses an explicit file list in `tools/package.py`; these repository-only skill files are not part of that archive. Resource reuse and any future distribution must preserve the existing [LICENSE](../../LICENSE) and [NOTICE.md](../../NOTICE.md) boundaries.
