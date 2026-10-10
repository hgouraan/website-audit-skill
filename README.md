# Website Audit Agent
A file-first workflow for evidence-based website audits: scope first, register every piece of evidence, link every finding to it, prioritize with an exposed formula, and ship testable implementation tickets. Live mode is optional; offline-artifact mode is fully supported with stated coverage gaps.

**v0.1.0 pre-release built and validated; publication pending.** Experimental: the synthetic fixture audit and deterministic checks pass, but the workflow has not audited a real production site. Licensed under MIT.

## Five-minute sample
Requirements: a Markdown reader; optional Python 3.10+ standard library.

```sh
python3 scripts/validate.py examples/synthetic-sample
python3 -m unittest discover -s tests -v
```
The fictional sample audits a 5-page static export with seeded defects (missing alt, unlabeled form input, missing title/h1, missing meta description, no submit states, no analytics). Output: evidence register, six dimension files, findings.csv, prioritized backlog via priority = (impact x confidence) / effort, one ticket per finding, and honest coverage limits.

## Workflow
Scope and permission -> bounded evidence collection (or offline mode) -> six-dimension analysis -> evidence-linked findings -> reproducible prioritization -> implementation tickets -> coverage report. Mermaid: [workflow/workflow.mmd](workflow/workflow.mmd); gates: [workflow/workflow.md](workflow/workflow.md).

## Start a real run
1. Read [SKILL.md](SKILL.md) and [docs/usage.md](docs/usage.md). Copy templates to `runs/your-run/`.
2. Write scope.md before collecting anything: permission, boundaries, request budget, mode.
3. Log every observation in evidence-register.csv. Findings cite an evidence_id or the literal HYPOTHESIS - never invent measurements.
4. Compute priority_score with the documented formula; keep the backlog sorted.
5. Validate with `python3 scripts/validate.py runs/your-run`.

## What this does not do
No penetration testing, exploit attempts, automatic production changes, high-volume crawling, or guaranteed Lighthouse scores. It never claims pages, devices, logins or metrics it has no evidence for. See [limitations](docs/limitations.md), [security](SECURITY.md), [contributing](CONTRIBUTING.md).
