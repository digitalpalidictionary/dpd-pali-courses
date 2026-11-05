# Creating a new key-validation thread (instructions for the agent)

Rules throughout: run on Sonnet; sub-agents get `model: "sonnet"` set explicitly; never run the full
pytest suite (target files only); do not run git (the user commits); nothing in `docs/` changes before the
user has edited and confirmed the approval file.

## 1. Preconditions
- `uv run python scripts/verify_key.py` exits 0.
- The DPD DB exists (see `verifier.md`). If not, stop and tell the user.

## 2. Regenerate the report and note the counts
`uv run python scripts/verify_key.py --course all --dpd --report temp/key_dpd_report.tsv`
Count rows per course and bucket:
`awk -F'\t' 'NR>1{c[$2" "$16]++} END{for(k in c) print k, c[k]}' temp/key_dpd_report.tsv | sort`
These numbers go into the new spec.

## 3. Create the thread from the drafts
Thread dir: `kamma/threads/<YYYYMMDD>_key_sentence_review/`. Copy `draft_spec.md` and `draft_plan.md` from
this folder into it as `spec.md` / `plan.md` and fill every `<…>` placeholder (date, counts). Present the
spec and plan to the user inline for approval before starting (via `/kamma:1-plan` or by hand).

## 4. Run the thread (summary; the plan has the tasks)
1. Small buckets (IMPOSSIBLE, NOT-FOUND, ROOT-MISMATCH): one Sonnet sub-agent per course, rows from
   `awk -F'\t' 'NR>1 && $2=="<course>" && $16!="AMBIGUOUS"' temp/key_dpd_report.tsv`.
2. AMBIGUOUS: split per class file (bpc 1–15, ipc 16–29), one sub-agent each, ≤4 in parallel.
   Make packets in the scratchpad:
   `awk -F'\t' -v S=<scratch>/amb 'NR==1{h=$0;next} $16=="AMBIGUOUS"{n=split($3,p,"/"); f=S"/"$2"_"p[n]".tsv"; if(!(f in s)){print h > f; s[f]=1} print $0 >> f}' temp/key_dpd_report.tsv`
   Each agent writes `parts/<course>_<N>_class.tsv` (no header, 11 columns), so there are no concurrent
   appends. The orchestrator merges the parts into `checklist_<course>.tsv` after each batch.
3. Coverage: `comm -3` of sorted report row_keys vs sorted checklist row_keys is empty; no duplicate
   row_keys in the checklist (`cut -f1 | sort | uniq -d`; report-side duplicates are known and harmless).
4. Build `approval_<course>.md` from CORRECT rows only. STOP and hand it to the user.
5. After the user confirms: apply, re-run the verifier, report.

## 5. Sub-agent prompt (use verbatim; add the rows)
> Judge EVERY row individually against its Pāli sentence, English translation, gloss and DPD readings.
> Do not script verdicts. Verdicts: `CONFIRMED` (the key tag is a valid reading in context — this includes
> cases where other readings also fit; **when in doubt, CONFIRMED**), `CORRECT` (a definite error: context
> clearly demands another tag; give new_pos, new_grammar, optionally new_root/new_gloss, and a one-line
> reason naming the deciding evidence), `FALSE-POSITIVE` (small buckets only: the key is right, DPD or the
> matcher is the gap). CONFIRMED needs a short reason naming the deciding evidence. Never guess: an
> unprovable alternative is CONFIRMED, not CORRECT. For a clearly wrong translation prefix the reason with
> `TRANSLATION:` (report only, never fix). Write `parts/<course>_<N>_class.tsv`: no header, 11
> tab-separated columns `row_key bucket word pos grammar verdict new_pos new_grammar new_root new_gloss
> reason`, one row per input row, no tabs/newlines inside fields. Verify row_keys with `comm`. Edit nothing
> under `docs/`. Reply with counts only.

Hints to give the agents: a sentence column that is empty or holds only a title (some sutta rows) — judge
from the key file itself and mark such CORRECTs low confidence; 1st/2nd-person pronouns have no gender
(`1st.gen.sg`, `2nd.instr.sg`); the last member of a compound takes the case of the whole compound; an
`-aṃ` ending cannot be masc nom.sg; check gender against neighbouring words in the same sentence.

## 6. Approval file format
One file per course, grouped by class file in numeric order (`## ipc 16_class.md`), with a header stating
the count and "delete lines you reject, edit targets if needed". One line per CORRECT row:
`` - `<row_key>` <word> | <pos> | <grammar> → <new_pos> | <new_grammar> [| root: X] [| gloss: Y] — <reason> ``
Only definite errors appear here. No notes files, no Undecided list. The user edits the file by deleting
lines, then confirms.

## 7. Applying the confirmed items
- Read the approval file as it is at that moment (the user's edits are authoritative). Items = lines
  starting `- `.
- Regenerate the report first so `line` numbers are current. Write a throwaway script in the scratchpad
  (not in the repo): for each item, locate the row by `row_key` → report `line`; read the file from
  `git show HEAD:<file>` (so a rerun is idempotent); assert the old word/pos/grammar match; edit only the
  named cells; write the file back with every other line unchanged. Cell gotchas: `verifier.md`.
- Parse targets carefully: the reason follows the first ` — `. Explanatory words inside a target
  (e.g. "masc.loc.sg (loc abs) with …") are a note, not a value — apply the value only and tell the user.
  Malformed targets (e.g. POS `nt`) and hand-edited items without an arrow: interpret conservatively and
  flag each interpretation to the user.
- A request to delete or renumber exercises/examples goes beyond cell edits and conflicts with the
  data-preservation rule (and touches `docs/*_ex/`): hold it and ask for explicit confirmation.
- Verify: `git diff --stat docs/` shows one changed line per applied item; `uv run python
  scripts/verify_key.py` exits 0; the `--dpd --report` run exits 0; no applied `row_key` is IMPOSSIBLE
  (if one is, the user approved a reading DPD lacks — report it, do not revert).
- Tell the user the work is ready to commit. Suggested message:
  `Apply <BPC|IPC> key sentence-review corrections (docs/<course>_key/): …`.
- Hindi copies (`docs/bpc_hi_key/`, `docs/bpc_hi_ex/`) are out of scope; mention they may need mirroring.
