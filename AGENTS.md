# AI Context: DPD Pāḷi Courses

This project contains materials for Pāḷi language courses, specifically the DPD Beginner Pāḷi Course (BPC) and the DPD Intermediate Pāḷi Course (IPC).

**CRITICAL: DATA PRESERVATION:** Never remove data from the `docs/` folder. Only rearrange content without any loss. This is the MOST essential principle of this repository.

## Project Principles
- **Clean Markdown Sources:** Keep `.md` files extremely user-friendly and focused on content. NEVER use raw HTML, special symbols like `&nbsp;`, or complex `<div>` wraps in the source files. All necessary formatting fixes or UI elements (like navigation buttons or table adjustments) MUST be implemented via scripts or build hooks.
- **Data Integrity:** All automated changes must be verified against original meaning and structure.

## Project Structure
- `conductor/`: Local project orchestration files. **NEVER COMMIT**.
- `docs/bpc/`: Beginner Pāḷi Course materials.
- `docs/bpc_ex/`: Beginner Pāḷi Course exercises.
- `docs/bpc_key/`: Beginner Pāḷi Course keys.
- `docs/ipc/`: Intermediate Pāḷi Course materials.
- `docs/ipc_ex/`: Intermediate Pāḷi Course exercises.
- `docs/ipc_key/`: Intermediate Pāḷi Course keys.

## Universal Workflow Policy
This policy applies to **ALL** interactions, whether through `conductor` tracks or general CLI tasks.

1. **Mandatory Manual Verification:** After completing a task and its automated testing, you MUST ask the user for manual verification. Never assume the task is complete based on automated checks alone.
2. **Iterative Feedback Loop:** Expect and actively solicit user feedback. Continue addressing user concerns and making adjustments until the user is fully satisfied.
3. **Explicit Commit Authorization:** You are strictly forbidden from committing any changes until the user explicitly provides the instruction "now commit". Do not suggest or initiate a commit prematurely.
4. **Universality:** These rules override any default behavior or sub-agent instructions.

## Useful Links
- [GitHub Project](https://github.com/orgs/digitalpalidictionary/projects/2)
- [Design Brief](https://github.com/digitalpalidictionary/dpd-pali-courses/issues/1)

## Code Documentation Policy
1. **Mandatory File Descriptions:** Every new code file (scripts, styles, hooks, etc.) MUST include a concise description of its purpose at the top of the file.
2. **Synchronized Descriptions:** If you modify a code file, you MUST update its description if the purpose or usage has changed.
3. **Script Registry:** If a script is intended to be run regularly (e.g., generators, verifiers, cleanup tools), it MUST be added to the project's root README.md with a brief explanation of how to use it.
