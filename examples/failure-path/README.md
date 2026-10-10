# Failure path
Canonical failure: a finding states a measurement ("LCP 4.2s") with no evidence row. The validator forces the choice: add real evidence or mark the finding HYPOTHESIS. Related failures reproduced in tests: unknown evidence_id, formula drift, missing ticket, missing coverage statement. Recovery: fix the named artifact, re-validate, resume from the last human-reviewed artifact.
