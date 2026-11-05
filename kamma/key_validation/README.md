# Key validation — how to re-run the sentence-level review of the BPC/IPC answer keys

Self-contained instructions. Nothing here depends on any earlier thread.

| File | For | Content |
|---|---|---|
| `verifier.md` | anyone running the Python tool | `scripts/verify_key.py`: what it checks, flags, DPD report columns, buckets |
| `new_thread.md` | the agent creating the thread | step-by-step: regenerate report, create the thread from the drafts, run it |
| `draft_spec.md` | the agent | copy to `kamma/threads/<date>_key_sentence_review/spec.md` and fill the placeholders |
| `draft_plan.md` | the agent | copy to `.../plan.md` and fill the placeholders |

Goal of a review: find **definite tagging errors** in the POS/Grammar/Root cells of `docs/bpc_key/` and
`docs/ipc_key/`, show them to the user in one approval file, apply only what the user leaves in it.
The user wants errors only — never lists of "could be read either way".
