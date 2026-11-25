Apply the IPC audits: kamma/audit/ipc-audit.md

Rules:
1. Rows with conf 8, 9, 10: re-verify each one, then apply it if it still holds at 8+.
2. Rows with conf 7: check with extra care. Apply only if after checking you would score it 8+.
3. Conf 6 and below: don't touch.
4. SKIP, and leave in the audit for me, any row whose suggestion:
   - offers alternatives ("or", "Either", "owner decision"), or
   - names no target ("Reword", "Confirm", "DPD lookup"), or
   - needs a canonical reading you cannot confirm.
5. Verify before applying:
   - DPD: `uv run python kamma/audit/scripts/dpd_lookup.py <lemma>`, or sqlite on /Users/deva/Documents/dpd-db/dpd.db (`dpd_headwords.inflections` for forms, `dpd_roots` for root group, sign and meaning).
   - Canonical text: grep the local CST text in /Users/deva/Documents/dpd-db/resources/dpd_submodules/cst/romn_txt/ (e.g. s0101m.mul.txt = DN vol 1). Never fix a citation or reading from memory.
   - Audit line numbers may have drifted; find each place by its content.
6. NEVER remove data from docs/: no deleting derivations, notes or alternative readings. A fix that would delete content stays in the audit.
7. GOLDEN RULE: whenever a sentence, sync docs/ipc_ex and docs/ipc_key for the same class, check whether a changed example also appears in ipc_key/ipc_ex, and sync it there too.

Workflow (this worked for BPC):
- Fork parallel agents by class group, each owning a disjoint set of files (key + exercise for its classes). No agent edits the audit file.
- A row that spans several classes: each fork applies its own part; the row is removed only when every part is done.
- Each fork reports a table: row Location | first word | APPLIED/SKIPPED | reason. Include a one-line reason for each conf-7 row it upgraded.
- When all forks are done:
  - Review risky reports yourself (deleted content, citations, links).
  - Run `uv run python scripts/verify_key.py` (must exit 0), `uv run python scripts/check_sutta_links.py <folders>`, `uv run python kamma/audit/scripts/mech_checks.py <folders>` and `git diff --check`.
- Remove applied rows from the audit with a scratchpad script that matches location + a Current-cell fragment and asserts exactly one hit per row. Back up the audit first. Afterwards, check that no blank lines were left inside tables.
- For partly done rows, append "Done <date> in …; left: …" to the Suggested cell. For rows where DPD contradicts the suggestion, write the DPD finding into the row.
- Run `git status --short docs/` right before reporting. Don't commit; I'll ask.

Goal: the audits shrink to only the rows that need my judgement.
