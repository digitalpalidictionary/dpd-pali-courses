# Project Rules

> **Both files are always active.** The agent loads the global `~/.config/agents/AGENTS.md` and this file simultaneously. Global rules apply here too — this file only adds project-specific rules on top.

These rules are specific to the DPD Pāḷi Courses project. Universal rules (security, testing, git, conductor, debugging, etc.) are now in the global `/Users/deva/.config/agents/AGENTS.md`.

## Project: DPD Pāḷi Courses

This project contains materials for Pāḷi language courses, specifically the DPD Beginner Pāḷi Course (BPC) and the DPD Intermediate Pāḷi Course (IPC).

**CRITICAL: DATA PRESERVATION:** Never remove data from the `docs/` folder. Only rearrange content without any loss. This is the MOST essential principle of this repository.

## Project Principles
- **Clean Markdown Sources:** Keep `.md` files extremely user-friendly and focused on content. NEVER use raw HTML, special symbols like `&nbsp;`, or complex `<div>` wraps in the source files. All necessary formatting fixes or UI elements (like navigation buttons or table adjustments) MUST be implemented via scripts or build hooks.
- **Data Integrity:** All automated changes must be verified against original meaning and structure.

## Project Structure
- `conductor/`: Project orchestration files.
- `docs/bpc/`: Beginner Pāḷi Course materials.
- `docs/bpc_ex/`: Beginner Pāḷi Course exercises.
- `docs/bpc_key/`: Beginner Pāḷi Course keys.
- `docs/ipc/`: Intermediate Pāḷi Course materials.
- `docs/ipc_ex/`: Intermediate Pāḷi Course exercises.
- `docs/ipc_key/`: Intermediate Pāḷi Course keys.

## GitHub (upstream repository)
- Unless otherwise specified the repository in question is https://github.com/digitalpalidictionary/dpd-pali-courses.

## Tools/printer.py
Colored console output with timing. Import: `from tools.printer import printer as pr`

## Script Registry
If a script is intended to be run regularly (e.g., generators, verifiers, cleanup tools), it MUST be added to the project's root README.md with a brief explanation of how to use it.

## CLI Scripts (`scripts/cl/`)
All files placed in `scripts/cl/` MUST be made executable with `chmod +x` immediately after creation.

## Useful Links
- [GitHub Project](https://github.com/orgs/digitalpalidictionary/projects/2)
