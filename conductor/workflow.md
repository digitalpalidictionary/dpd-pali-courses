# Project Workflow

## Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **Single Commit per Track:** Do NOT commit per task. Do NOT use git notes per task. Record task completion only in plan.md status markers.
3. **Task Sequentiality:** Choose the next available task from `plan.md` in sequential order
4. **Test-Driven Development:** Write tests before implementation

<!-- LOCAL-START: Local Principles -->
5. **Data Preservation:** Never remove data from `docs/` folder. Only rearrange content without loss. And never edit `docs/` files directly. All changes must be made via scripts or build hooks to ensure data integrity.
6. **Clean Markdown Sources:** Keep `.md` files extremely user-friendly and focused on content
<!-- LOCAL-END: Local Principles -->

## Task Lifecycle (TDD)

All tasks follow a strict lifecycle:

1. **Mark In Progress:** Change task status from `[ ]` to `[~]` in `plan.md`
2. **Red Phase (Failing Tests):**
   - Create a new test file or add cases to existing ones in `tests/`
   - Run `uv run pytest --tb=short -q` and confirm failure
3. **Green Phase (Implementation):**
   - Write minimum code to pass tests
   - Confirm `uv run pytest` passes and `uv run pyright <file>` has no errors
4. **Refactor Phase:**
   - Clean up implementation and test code while keeping tests green
5. **Validation:**
   - Run `uv run pytest --tb=short -q`
   - Run `uv run pyright <file>` for type checking
   - If UI/content changes: run `uv run mkdocs build` and verify `site/` output
6. **Completion:**
   - Mark task as complete `[x]` in `plan.md`
   - Do NOT commit yet
   - Once user says "track finished", move it to `conductor/archive/` and remove from `tracks.md`

## Quality Gates

Before marking any task complete, verify:

- [ ] All tests pass via `uv run pytest`
- [ ] No type errors via `uv run pyright`
- [ ] Code follows project style guides (see `conductor/code_styleguides/`)
- [ ] No security vulnerabilities introduced
- [ ] Documentation updated if needed
- [ ] Data integrity preserved (no data removed from `docs/`)
- [ ] No linting or static analysis errors

## Review Protocol

When reviewing a track's implementation:

1. Read `spec.md` and `plan.md` — does code match intent?
2. Check against `conductor/code_styleguides/` files (Python, HTML/CSS, general)
3. Run the full test suite: `uv run pytest`
4. Run type checking: `uv run pyright`
5. Run external review tool if available: `coderabbit --prompt-only`
6. Output findings with severity levels (Critical/High/Medium/Low)
7. Propose fixes or ask user for guidance

## Revert Protocol

Since `conductor/` is version-controlled, revert via git:

1. Identify scope (whole track, single phase, or single task)
2. Use `git revert <commit>` for the relevant changes or `git checkout <ref> -- <path>` for specific files
3. Update `plan.md` to reflect reverted state
4. Document reason in `handoff.md` with date and explanation

## Track File Set (Canonical)

Every track folder must contain:

- **metadata.json** — track ID, type, status, timestamps, description
- **index.md** — links to other track files
- **spec.md** — specification / requirements
- **plan.md** — implementation plan with `[ ]`/`[~]`/`[x]` status markers
- **handoff.md** — cross-session state (created on first session end)

## Definition of Done

A track is complete when:

1. All tasks marked `[x]` in `plan.md`
2. All tests passing via `uv run pytest`
3. All type errors fixed via `uv run pyright`
4. Code reviewed (internal or external tools)
5. User has approved all changes
6. Single atomic commit created with "now commit"
7. Track archived to `conductor/archive/`, this folder NEVER committed to git, it is only for internal record keeping.

## Skills

Suggest appropriate skill to run for user's current context and workflow stage. For example:

| Skill | Description |
|---|---|
| `/conductor-new-track` | Create a new track for planning a feature or task |
| `/conductor-continue` | Resume work on an in-progress track |
| `/conductor-review` | Review implementation against spec and quality gates |
| `/conductor-complete` | Finish, archive, and close a track (coderabbit → fix → test → archive) |
| `/conductor-goodnight` | End-of-session protocol — write session log, optionally update handoff |
| `/conductor-sync` | Sync Conductor workflow across all registered projects |
| `/conductor-fix` | Run ruff and pyright on a script, then fix all reported errors |
