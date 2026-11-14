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
- `docs/bpc_hi/`, `docs/bpc_hi_ex/`, `docs/bpc_hi_key/`: Hindi BPC translation (in progress, unpublished). See `kamma/tech.md` → Multi-language support.

**HINDI IS ALWAYS OUT OF SCOPE.** The Hindi sources live on the separate `hindi` branch, not on `main`. Never include `bpc_hi*` in a thread's scope, spec, plan, conversion, audit or verification, and never ask whether to include it. Work on `main` covers the English folders only.

## GitHub (upstream repository)
- Unless otherwise specified the repository in question is https://github.com/digitalpalidictionary/dpd-pali-courses.

## Script Registry
If a script is intended to be run regularly (e.g., generators, verifiers, cleanup tools), it MUST be added to the project's root README.md with a brief explanation of how to use it.

## CLI Scripts (`scripts/cl/`)
All files placed in `scripts/cl/` MUST be made executable with `chmod +x` immediately after creation.

## Output & Debugging
- Use `tools/printer.py` for all script output: `pr.green_tmr("task")` → `pr.yes("ok")` on success (`green_tmr` keeps "ok" and the timing on the same line; plain `pr.green` adds a newline and never starts the timer), `pr.no(f"{n} files")` + `pr.amber(f)` per item on failure. Collect per-item warnings during the step and print them after `pr.yes`/`pr.no`, never between `green_tmr` and the result. No bare `print()`. Shell scripts have no `echo` step labels.
- Use `icecream` (`from icecream import ic`) for debug output, not `print()`.

## Key Verification
- Before any commit touching `docs/bpc_key/`, `docs/bpc_ex/`, `docs/ipc_key/` or `docs/ipc_ex/`, run `uv run python scripts/verify_key.py`; it must exit 0. `--dpd` is optional, local-only and advisory.

## Course Audits (`kamma/audit/`)
- Read-only audits of course folders (findings lists, never edit `docs/`). Follow `kamma/audit/audit-guide.md` (process, row format, categories, limits). Output: `kamma/audit/<course>-audit.md`; work in progress and handoff state in `kamma/audit/scratch/STATE.md`.
- Check every suspicious Pāli form, grammar tag, root or gloss in DPD with `uv run python kamma/audit/scripts/dpd_lookup.py <lemma> …` before reporting it.

## Sutta Links
- Every sutta/Vinaya reference must use `https://s.dhamma.gift/...`; the old `find.dhamma.gift/bw/` host is dead (GitHub #9). Never hand-write a URL shape — the mapping rules (mn/dn page-per-sutta, sn/an `#<id>`, `/kn/...` for snp/ud/kp/dhp/thag/thig/iti, and the Vinaya renames sn→ss, an→as, `bu-pt` → `pm3..pm9`) live in `kamma/tech.md` → Sutta links and in `scripts/rewrite_sutta_links.py`. Re-verify with `uv run python scripts/check_sutta_links.py` (network; cached in `temp/`).

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
