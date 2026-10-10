#!/usr/bin/env python3
"""Deterministic contract validator for a website-audit run directory.

Read-only. Checks file contracts, evidence linkage, score ranges, priority
formula and ticket coverage. Cannot verify the site was actually tested.
Exit 0 on pass, 1 on failures.
"""
import csv, json, os, re, sys

EVID_HEADERS = ["evidence_id", "url", "type", "source_file", "captured_at"]
FIND_HEADERS = ["finding_id", "dimension", "url", "observation", "evidence_id",
                "impact", "confidence", "effort", "reproduction", "proposed_fix"]
BACKLOG_HEADERS = ["rank", "finding_id", "priority_score"]
DIMENSIONS = ["technical-audit.md", "seo-audit.md", "ux-audit.md",
              "conversion-audit.md", "content-audit.md", "analytics-audit.md"]
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
STATE_FIELDS = ["run_id", "skill_version", "phase", "status", "completed_phases", "timestamps"]
STATUSES = {"not_started", "in_progress", "blocked", "needs_review", "approved", "rejected", "completed"}

def read_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def validate(run):
    errors = []
    def need(p):
        if not os.path.isfile(os.path.join(run, p)):
            errors.append(f"missing file: {p}")
            return False
        return True

    for p in ["state.json", "scope.md", "evidence-register.csv", "findings.csv",
              "prioritized-backlog.csv", "coverage-limitations.md"] + DIMENSIONS:
        need(p)
    if errors:
        return {"valid": False, "errors": errors}

    state = json.load(open(os.path.join(run, "state.json"), encoding="utf-8"))
    for f in STATE_FIELDS:
        if f not in state:
            errors.append(f"state.json missing field: {f}")
    if state.get("status") not in STATUSES:
        errors.append(f"state.json bad status: {state.get('status')}")

    ev = read_csv(os.path.join(run, "evidence-register.csv"))
    ev_ids = set()
    if ev:
        for h in EVID_HEADERS:
            if h not in ev[0]:
                errors.append(f"evidence-register.csv missing header: {h}")
        for r in ev:
            ev_ids.add(r["evidence_id"])
            if r.get("type") not in {"automated", "manual"}:
                errors.append(f"evidence {r.get('evidence_id')}: bad type")
            if not DATE_RE.match(r.get("captured_at", "")):
                errors.append(f"evidence {r.get('evidence_id')}: bad captured_at")
            sf = r.get("source_file", "")
            if sf and not os.path.isfile(os.path.join(run, sf)):
                errors.append(f"evidence {r.get('evidence_id')}: source_file not found: {sf}")

    cov = open(os.path.join(run, "coverage-limitations.md"), encoding="utf-8").read()
    if "not covered" not in cov.lower() and "no known gaps" not in cov.lower():
        errors.append("coverage-limitations.md must state what is not covered (or 'no known gaps')")

    findings = read_csv(os.path.join(run, "findings.csv"))
    fids = []
    if findings:
        for h in FIND_HEADERS:
            if h not in findings[0]:
                errors.append(f"findings.csv missing header: {h}")
        for r in findings:
            fids.append(r["finding_id"])
            e = r.get("evidence_id", "")
            if e != "HYPOTHESIS" and e not in ev_ids:
                errors.append(f"finding {r.get('finding_id')}: unknown evidence_id {e!r}")
            for f_ in ["impact", "confidence", "effort"]:
                try:
                    v = int(r[f_])
                    if not 1 <= v <= 5:
                        raise ValueError
                except (ValueError, KeyError):
                    errors.append(f"finding {r.get('finding_id')}: {f_} must be integer 1-5")
            if not r.get("reproduction", "").strip():
                errors.append(f"finding {r.get('finding_id')}: empty reproduction")
            if not r.get("proposed_fix", "").strip():
                errors.append(f"finding {r.get('finding_id')}: empty proposed_fix")

    backlog = read_csv(os.path.join(run, "prioritized-backlog.csv"))
    if backlog:
        for h in BACKLOG_HEADERS:
            if h not in backlog[0]:
                errors.append(f"prioritized-backlog.csv missing header: {h}")
        fmap = {r["finding_id"]: r for r in findings}
        scores = []
        for i, r in enumerate(backlog, 1):
            fid = r.get("finding_id")
            if fid not in fmap:
                errors.append(f"backlog row {i}: unknown finding {fid}")
                continue
            f = fmap[fid]
            try:
                expect = round(int(f["impact"]) * int(f["confidence"]) / int(f["effort"]), 1)
                got = float(r["priority_score"])
                if abs(expect - got) > 0.05:
                    errors.append(f"backlog {fid}: priority_score {got} != formula {expect}")
                scores.append(got)
                if int(r["rank"]) != i:
                    errors.append(f"backlog {fid}: rank {r['rank']} != row order {i}")
            except (ValueError, KeyError):
                errors.append(f"backlog {fid}: bad numbers")
        if scores != sorted(scores, reverse=True):
            errors.append("prioritized-backlog.csv not sorted by priority_score desc")
        covered = {r.get("finding_id") for r in backlog}
        if covered != set(fids):
            errors.append("backlog does not cover exactly the findings set")

    brief_dir = os.path.join(run, "implementation-briefs")
    briefs = {os.path.splitext(f)[0] for f in os.listdir(brief_dir)} if os.path.isdir(brief_dir) else set()
    for fid in fids:
        if fid not in briefs:
            errors.append(f"missing implementation brief for {fid}")
        else:
            body = open(os.path.join(brief_dir, fid + ".md"), encoding="utf-8").read()
            if "## Acceptance criteria" not in body:
                errors.append(f"implementation-briefs/{fid}.md missing ## Acceptance criteria")
    return {"valid": not errors, "errors": errors}

if __name__ == "__main__":
    result = validate(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(json.dumps(result, indent=2))
    sys.exit(0 if result["valid"] else 1)
