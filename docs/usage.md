# Usage
1. Copy templates/ to runs/<run_id>/. Write scope.md (permission, boundaries, mode, goal) before anything else.
2. evidence-register.csv: evidence_id, url, type (automated|manual), source_file, captured_at. source_file paths are relative to the run directory.
3. Six dimension files; cite evidence ids or prefix `Hypothesis:`.
4. findings.csv: finding_id, dimension, url, observation, evidence_id (or HYPOTHESIS), impact, confidence, effort (1-5), reproduction, proposed_fix.
5. prioritized-backlog.csv: rank, finding_id, priority_score = (impact*confidence)/effort rounded to 1 decimal, sorted desc, covering exactly the findings set.
6. implementation-briefs/<finding_id>.md with `## Acceptance criteria` and `## Verification`.
7. coverage-limitations.md must state what is not covered (or `no known gaps`).
Run `python3 scripts/validate.py runs/<run_id>` after each phase.
