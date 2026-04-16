# Project Workflow

## Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`.
2. **Task Sequentiality:** Choose the next available task from `plan.md` in sequential order.

<!-- LOCAL-START: Local Principles -->
3. **Data Preservation:** Never remove data from `docs/` folder. Only rearrange content without loss. Never edit `docs/` files directly.
4. **Clean Markdown Sources:** Keep `.md` files extremely user-friendly and focused on content.
<!-- LOCAL-END: Local Principles -->

## Task Lifecycle

All tasks follow a strict lifecycle:

1. **Mark In Progress:** Change task status from `[ ]` to `[~]` in `plan.md`.
2. **Red Phase (Failing Tests):**
   - Create a new test file or add cases to existing ones in `tests/`.
   - Run tests and confirm failure (see **Quality Gates** for commands).
3. **Green Phase (Implementation):** Write minimum code to pass tests.
4. **Refactor Phase:** Clean up code while keeping tests green.
5. **Validation:** Confirm all **Quality Gates** pass.
6. **Completion:** Mark task as complete `[x]` in `plan.md`. Do NOT commit yet.

## Quality Gates

Before marking any task complete, verify:

- [ ] All tests pass via `uv run pytest {file-name}`.
- [ ] Code follows project style guides (see `conductor/code_styleguides/`).
- [ ] No security vulnerabilities introduced.
- [ ] Documentation updated if needed.
- [ ] Data integrity preserved (no data removed from `docs/`).

## Review Protocol

When reviewing a track's implementation:

1. Read `spec.md` and `plan.md` — does code match intent?
2. Check against `conductor/code_styleguides/` files.
3. Verify all **Quality Gates** pass.
4. Run external review tool if available: `coderabbit --prompt-only`.
5. Output findings with severity levels (Critical/High/Medium/Low).

## Revert Protocol

Since `conductor/` is version-controlled, revert via git:

1. Identify scope (whole track, single phase, or single task).
2. Use `git revert` or `git checkout` for the relevant changes.
3. Update `plan.md` to reflect reverted state.
4. Document reason in `handoff.md`.

## Track File Set (Canonical)

Every track folder must contain:

- **metadata.json** — track ID, type, status, timestamps, description.
- **index.md** — links to other track files.
- **spec.md** — specification / requirements.
- **plan.md** — implementation plan with status markers.
  - **Plan Mode Target Enforcement:** The generated plan MUST be written directly to `conductor/tracks/<track_id>/plan.md`.
- **handoff.md** — cross-session state.

## Definition of Done

A track is complete when:

1. All tasks marked `[x]` in `plan.md`.
2. All **Quality Gates** pass.
3. User has approved all changes.
4. Single atomic commit prepared by AI and manually committed by user.
5. Track archived to `conductor/archive/` (this folder is never committed).
