# Project Rules

Apply these in addition to your baseline global instructions `~/.claude/CLAUDE.md`.

## Project: DPD Pāḷi Courses

This project contains materials for Pāḷi language courses, specifically the DPD Beginner Pāḷi Course (BPC) and the DPD Intermediate Pāḷi Course (IPC).

**CRITICAL: DATA PRESERVATION:** Never remove data from the `docs/` folder. Only rearrange content without any loss. This is the MOST essential principle of this repository.

## Project Principles
- **Clean Markdown Sources:** Keep `.md` files extremely user-friendly and focused on content. NEVER use raw HTML, special symbols like `&nbsp;`, or complex `<div>` wraps in the source files. All necessary formatting fixes or UI elements (like navigation buttons or table adjustments) MUST be implemented via scripts or build hooks.
- **Data Integrity:** All automated changes must be verified against original meaning and structure.

## Project Structure
- `docs/bpc/`: Beginner Pāḷi Course materials.
- `docs/bpc_ex/`: Beginner Pāḷi Course exercises.
- `docs/bpc_key/`: Beginner Pāḷi Course keys.
- `docs/ipc/`: Intermediate Pāḷi Course materials.
- `docs/ipc_ex/`: Intermediate Pāḷi Course exercises.
- `docs/ipc_key/`: Intermediate Pāḷi Course keys.

## GitHub (upstream repository)
- Unless otherwise specified the repository in question is https://github.com/digitalpalidictionary/dpd-pali-courses.

## Script Registry
If a script is intended to be run regularly (e.g., generators, verifiers, cleanup tools), it MUST be added to the project's root README.md with a brief explanation of how to use it.

## CLI Scripts (`scripts/cl/`)
All files placed in `scripts/cl/` MUST be made executable with `chmod +x` immediately after creation.

## Output & Debugging
- Use `tools/printer.py` for all script output: `pr.green("task")` → `pr.yes("ok")` on success, `pr.no(f"{n} files")` + `pr.warning(f)` per item on failure. No bare `print()`. Shell scripts have no `echo` step labels.
- Use `icecream` (`from icecream import ic`) for debug output, not `print()`.

## Useful Links
- [GitHub Project](https://github.com/orgs/digitalpalidictionary/projects/2)

## Pre-Completion Validation (MANDATORY)

**Before reporting ANY Python code changes as complete, run ALL of:**

1. `uv run ruff check --fix <file>`
2. `uv run ruff format <file>`
3. `uv run pyright <file>`
4. `uv run --with pyrefly pyrefly check --min-severity warn <file>`
5. `uv run pytest tests/test_<feature>.py -v` (for affected tests)

**Do NOT report completion until all checks pass.** This is non-negotiable. Do not skip or defer these. Pyrefly warnings count as failures unless explicitly approved by the user. Type safety is mandatory, not optional.
- **Verification:** Write tests for accurate data output (not UI components). Readme MUST be updated.
- **Research:** Always perform Google Search for framework/OS quirks.
- **Sync Tracking:** Only track and update exporters in the sync registry that contain localized data (Russian, SBS, or DPS-specific).
