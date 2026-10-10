# Workflow

Phases follow the execution graph in `workflow.mmd`; machine gate definitions live in `gates.yaml`.

## 1. Scope
scope.md: site, permission basis, boundaries (pages, depth, request budget), target market, conversion goal, mode (live | offline-artifact), tools, start timestamp. Nothing is collected before this exists.

## 2. Evidence
evidence-register.csv columns: evidence_id, url, type (automated|manual), source_file, captured_at (YYYY-MM-DD). Live mode only with authorized, rate-limited tools. Offline mode reads supplied exports and must state exactly what was not covered in coverage-limitations.md.

## 3. Analysis
Six dimension files. Every statement cites an evidence_id or is prefixed `Hypothesis:`.

## 4. Findings
findings.csv columns: finding_id, dimension, url, observation, evidence_id, impact, confidence, effort, reproduction, proposed_fix. evidence_id is an existing register id or the literal HYPOTHESIS. impact/confidence/effort are integers 1-5. Never invent measurements: a metric without an evidence row is a hypothesis.

## 5. Priorities
priority_score = (impact * confidence) / effort, one decimal. prioritized-backlog.csv is sorted by priority_score descending. See references/scoring-formula.md.

## 6. Tickets
One implementation-briefs/<finding_id>.md per finding with `## Acceptance criteria` and `## Verification`. Finish with coverage-limitations.md listing untested pages, devices, metrics and why.

## Failure and resume
Missing permission, invented measurements, or claimed-but-missing evidence set state.json to blocked/needs_review. Resume from the last human-reviewed artifact.
