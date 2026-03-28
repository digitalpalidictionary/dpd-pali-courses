# Project Workflow

## Principles

1. **The Plan is the Source of Truth:** All work must be tracked in `plan.md`
2. **Single Commit per Track:** Do NOT commit per task. Do NOT use git notes per task. Record task completion only in plan.md status markers.
3. **Task Sequentiality:** Choose the next available task from `plan.md` in sequential order
4. **Test-Driven Development:** Write tests before implementation
5. **Data Preservation:** Never remove data from `docs/` folder. Only rearrange content without loss.

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

## Track Completion

Once ALL tasks in a track are complete:

1. **Final Verification:** Run full test suite: `uv run pytest`
2. **Manual Review:** Ask the user for final manual review of all changes
3. **"Now Commit" Protocol:** Perform the single commit ONLY after user explicitly says **"now commit"**
   ```bash
   git add .
   git commit -m "conductor: <description of track>"
   ```
4. **Archive:** Move completed track to `conductor/archive/`
5. **Update Registry:** Remove track from `tracks.md`

## Cross-Agent Handoff

When ending a session where another agent will continue:

1. Run any verification scripts relevant to the work done this session. Document failures, noise, or known mismatches in `handoff.md` — do not leave the next agent to discover them.
2. Update `handoff.md` with:
   - What was done this session
   - Code state (all tests passing? uncommitted changes?)
   - Current task in `plan.md`
   - Any blockers or gotchas for next agent
3. Update session log: `conductor/sessions/YYYY-MM-DD-{agent}.md` with summary, including an `## Issues & AI Feedback` section (see format below)
4. Note in handoff which agent is expected to continue (Claude or Gemini)

### Session Log — Issues Section Format

Every session log must include this section:

```markdown
## Issues & AI Feedback
- [REPEATED] User had to remind AI not to commit without permission
- [WORKFLOW] AI skipped reading NOTES.md at session start
- [CONFUSION] AI misread track status markers
- [BEHAVIOR] AI added comments to code it didn't change
- [POSITIVE] Fish wrapper approach worked well — worth propagating
```

Tags: `[REPEATED]` re-stated rule · `[WORKFLOW]` process friction · `[CONFUSION]` misunderstanding · `[BEHAVIOR]` rule violation or missed action · `[POSITIVE]` something that worked well

Write `- None this session` if there were no issues.

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

## Development Commands

### Testing & Validation
```bash
uv run pytest                    # Run tests
uv run pytest --tb=short -q     # Run tests (short output)
uv run pyright <file>           # Type checking for a file
uv run mkdocs build             # Build documentation, output to site/
```

### Building
```bash
uv run mkdocs serve             # Serve docs locally for review (http://localhost:8000)
```

## Definition of Done

A track is complete when:

1. All tasks marked `[x]` in `plan.md`
2. All tests passing via `uv run pytest`
3. All type errors fixed via `uv run pyright`
4. Code reviewed (internal or external tools)
5. User has approved all changes
6. Single atomic commit created with "now commit"
7. Track archived to `conductor/archive/`
