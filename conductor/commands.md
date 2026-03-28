# Conductor Commands Reference

Quick reference for invoking conductor actions across different agents.

## Command Matrix

| Action | Gemini CLI | Claude Code | How It Works |
|--------|-----------|------------|---|
| **New Track** | `/conductor:newTrack <desc>` | "plan <description>" | Auto-creates track, generates spec & plan |
| **Implement** | `/conductor:implement` | "resume" or "continue" | Loads in-progress track from tracks.md |
| **Review** | `/conductor:review` | "review" or "conductor review" | Tests + code review against spec |
| **Revert** | `/conductor:revert` | "revert" or "undo" | Uses git revert (conductor/ is versioned) |
| **Good Night** | manual + `handoff.md` | "good night" | Session summary → session log + handoff |

## Default Behavior

When you ask ANY agent to:
- **"plan something"** → Auto-creates new track (no explicit "conductor" keyword needed)
- **"resume"** → Auto-loads from tracks.md
- **"review"** → Runs review protocol

## Files to Know

- `conductor/index.md` — entry point, links to product definition, tech stack, workflow
- `conductor/workflow.md` — project-specific workflow rules (phases, TDD, commit strategy)
- `conductor/tracks.md` — registry of all tracks with status
- `conductor/tracks/<track_id>/plan.md` — the implementation plan (source of truth)
- `conductor/sessions/YYYY-MM-DD-{agent}.md` — immutable daily log per agent

## Tips

1. **Plan is the source of truth** — all work tracked in plan.md with `[ ]`/`[~]`/`[x]` markers
2. **Single commit per track** — never commit per task, only when user says "now commit"
3. **Cross-agent handoff** — read handoff.md at session start if resuming mid-track
4. **Revert is safe** — conductor/ is version-controlled, use git to undo changes
