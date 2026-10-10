# Architecture
Pure file workflow: Markdown/CSV artifacts in runs/<run_id>/, gates in workflow/gates.yaml, deterministic stdlib validator in scripts/validate.py, JSON Schema contracts in schemas/. No services, no network calls, no state outside the run directory.
