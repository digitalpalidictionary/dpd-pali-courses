# IPC audit — handoff

Written: 2026-11-11. Task: full audit of `docs/ipc/` (data consistency, format, grammar, syntax), saved to `kamma/draft/audit/ipc-audit.md`, modelled on `bpc-audit.md` (categories A–H, tables of `Location | Current | Problem | Suggested | Conf.`).

## State

| Part | Status |
| --- | --- |
| Mechanical checks, all 136 files | **Done.** Results in `ipc-audit.md` section M |
| Sutta link check | **Done.** 37 links / 23 pages, all pass |
| External link check | **Done.** 1 dead (`class_28/3_home_work.md:17`, 404), 1 ok |
| Line-by-line read, `class_28` | **Done** by a subagent; findings saved in `ipc-audit.md`. **Not grep-verified** by me |
| Line-by-line read, `index.md` + `class_16` | **Not done.** Agent hit the usage limit, output lost |
| Line-by-line read, `class_17`, `class_18` | **Not done.** Same |
| Line-by-line read, `class_19`, `class_20`, `class_21` | **Not done.** Same |
| Line-by-line read, `class_22`, `class_23`, `class_24` | **Not done.** Agent hit the limit ("out of usage credits") |
| Line-by-line read, `class_25`, `class_26`, `class_27` | **Not done.** Same |
| Verification of findings against the files | **Not done** (including class 28) |
| Final merged `ipc-audit.md` (summary table, overall confidence, cross-class drift) | **Not done.** The file is a partial draft |
| DPD lookups for Pāli forms with confidence below 8 | **Not done** (class 28 has about 15 such rows) |

## Files touched

All new, all under `kamma/draft/audit/`:

- `ipc-audit.md` — partial audit (section M plus class 28)
- `ipc-audit-mech.py` — the mechanical-check script, recreated from the session (not re-run after saving; it is a draft, not registered in README, not under `scripts/`)
- `ipc-audit-handoff.md` — this file

No file under `docs/` was modified. Nothing was staged or committed. `kamma/draft/` was already untracked at session start.

## What was lost

- Five reader subagents (slices: index + 16; 17–18; 19–21; 22–24; 25–27) terminated on the usage limit (four on "5-hour limit", one on "out of usage credits"). Their findings files were never written, and the scratchpad and task transcripts no longer exist (scratchpad directory was empty on 2026-11-11). Whatever they had read is gone; those slices must be redone from scratch.
- The class 28 reader could not write to the scratchpad either (subagent write refused), so its report was returned as text and is what was saved.

## Failed attempts / lessons

- Six parallel `fork` readers on the strongest model exhausted the usage limit within one session. Subagents also cannot reliably write files; instruct them to return findings as text, in the table format, and keep each slice small.
- Suggested restart: run slices one or two at a time (class 16, 17, 18, 19 … separately), ask each to reply with the tables as text, append to `ipc-audit.md` immediately after each returns. Consider a cheaper model for first-pass reading, and keep the strong model for verification and grammar judgement.

## Process rules for the next run (prevent a repeat)

Why the scratchpad was empty: not verified. Observed on 2026-11-11: the session temp folder had been recreated at 06:52 (scratchpad empty, `tasks/` with the agent transcripts gone) after the limit hit and the model was switched. Probable cause is that the session temp folder is cleared on resume. Also, the class 28 agent reported its scratchpad write was refused, so agent-written files are not reliable either.

1. **Never keep audit data only in the scratchpad or in agent transcripts.** They do not survive a limit or resume. Write every result into `kamma/draft/audit/` immediately.
2. **Do not run many subagents in parallel.** Six strong-model readers launched at once drained the usage limit within one session and killed five of the six before any output was saved. Run one slice at a time (at most two), wait for it to finish, save its output, then start the next.
3. **Agents return findings as text; the main session saves them.** Do not rely on agents writing files. Append each returned slice to `ipc-audit.md` straight away, before launching the next.
4. **Keep slices small** (about 1 000–1 500 lines, e.g. one class per agent, class 28 split into its two files) so a failure loses little.
5. **Checkpoint in this file.** After each slice, update the State table above (Done / Not done) so a restart knows exactly where to resume.
6. If a limit message appears, stop launching work, save what exists, and update this handoff before anything else.

## Remaining work, in order

1. Read `index.md` and classes 16–27 line by line (about 8 400 lines minus class 28's 1 281).
2. Append each slice's tables to `ipc-audit.md` as it returns, under the same A–H headings.
3. Grep-verify every `Current` excerpt against the file (class 28 included).
4. Check cross-class convention drift once all slices are in (arrow `\>`, `√` use, `saṃ`/`sam`, bold-suffix style, quote style, `Pāli` spelling, `# Homeless work`).
5. Add the summary table and overall confidence to the top of `ipc-audit.md`; remove the "PARTIAL DRAFT" banner and the "NOT AUDITED" section.
6. Optional: DPD lookups for the low-confidence forms.

## Next decision for the owner

- Is `# Homeless work` intentional? It appears in 13 IPC and 26 BPC pages and in the indexes. If not, it is a one-line fix repo-wide, but the owner must decide; no change was made.
- Are `<br>` tags in table cells acceptable given the "no raw HTML in sources" rule? The PDF script handles them, so they look like an established convention.
- Fix the dead link at `class_28/3_home_work.md:17` (`pali-class-adv.html`, 404) once the correct URL is known.
- Fix `class_17/2_cons.md` and `class_19/1_comp.md` H1s (misplaced `*` closing italics after the bracket).
- Whether to rerun the readers on the same model or a cheaper one, and whether to resume the five dead agents after the 1:30am limit reset (their work was lost, so a fresh run is needed).

Confidence in what is saved: 8/10 for section M (scripted, directly observed); 6/10 for class 28 pali findings (reader's judgement, unverified, many need DPD).
