# Kamma Workflow

This workflow defines the lifecycle of a thread in this project.

---

## Phase 1: Research & Strategy
1.  **Analyze Request:** Understand the goal and context.
2.  **Research Codebase:** Map relevant files and dependencies.
3.  **Propose Solution:** Outline 2-3 approaches (Simple -> Complex).
4.  **Wait for Approval:** Get user confirmation on the chosen approach.

## Phase 2: Implementation (The "Do" Phase)
For each task in the plan:
1.  **Plan:** Define the implementation and testing strategy.
2.  **Act:** Apply targeted, surgical changes.
3.  **Validate:** Run tests and check workspace standards.

## Phase 3: Verification & Finalization
1.  **Cross-Format Check:** Ensure consistency across Website, PDF, and DOCX.
2.  **Linter/Type Check:** Run `ruff` and `pyright` on modified Python files.
3.  **User Verification:** Request manual verification from the user.
4.  **Handoff:** Log progress and prepare for the next session.
