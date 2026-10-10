import json, os, shutil, sys, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import validate

SAMPLE = os.path.join(os.path.dirname(__file__), "..", "examples", "synthetic-sample")

class T(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.r = os.path.join(self.d, "run")
        shutil.copytree(SAMPLE, self.r)
    def tearDown(self):
        shutil.rmtree(self.d)
    def v(self):
        return validate.validate(self.r)
    def edit_text(self, path, old, new, count=1):
        p = os.path.join(self.r, path)
        with open(p) as f: t = f.read()
        assert old in t, f"{old} not in {path}"
        with open(p, "w") as f: f.write(t.replace(old, new, count))

    def test_sample_valid(self):
        self.assertEqual(self.v(), {"valid": True, "errors": []})
    def test_missing_dimension(self):
        os.remove(os.path.join(self.r, "seo-audit.md"))
        self.assertFalse(self.v()["valid"])
    def test_unknown_evidence_id(self):
        self.edit_text("findings.csv", ",E5,", ",E99,")
        self.assertFalse(self.v()["valid"])
    def test_hypothesis_allowed(self):
        self.edit_text("findings.csv", ",E5,", ",HYPOTHESIS,")
        self.assertTrue(self.v()["valid"])
    def test_impact_out_of_range(self):
        self.edit_text("findings.csv", ",3,5,1,", ",9,5,1,")
        self.assertFalse(self.v()["valid"])
    def test_empty_reproduction(self):
        p = os.path.join(self.r, "findings.csv")
        lines = open(p).read().splitlines()
        parts = lines[1].split(",")
        parts[8] = ""
        lines[1] = ",".join(parts)
        open(p, "w").write("\n".join(lines) + "\n")
        self.assertFalse(self.v()["valid"])
    def test_priority_formula_wrong(self):
        self.edit_text("prioritized-backlog.csv", ",20.0,", ",19.0,")
        self.assertFalse(self.v()["valid"])
    def test_backlog_unsorted(self):
        p = os.path.join(self.r, "prioritized-backlog.csv")
        lines = open(p).read().splitlines()
        lines[1], lines[6] = lines[6], lines[1]
        open(p, "w").write("\n".join(lines) + "\n")
        self.assertFalse(self.v()["valid"])
    def test_missing_brief(self):
        os.remove(os.path.join(self.r, "implementation-briefs", "F-01.md"))
        self.assertFalse(self.v()["valid"])
    def test_brief_without_acceptance(self):
        self.edit_text("implementation-briefs/F-01.md", "## Acceptance criteria", "## Done when")
        self.assertFalse(self.v()["valid"])
    def test_missing_coverage_statement(self):
        self.edit_text("coverage-limitations.md", "Not covered", "Excluded topics")
        self.edit_text("coverage-limitations.md", "No known gaps", "Everything reviewed")
        self.assertFalse(self.v()["valid"])
    def test_bad_state_status(self):
        p = os.path.join(self.r, "state.json")
        obj = json.load(open(p)); obj["status"] = "done"
        json.dump(obj, open(p, "w"))
        self.assertFalse(self.v()["valid"])

if __name__ == "__main__":
    unittest.main()
