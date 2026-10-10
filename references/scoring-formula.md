# Scoring formula
priority_score = (impact * confidence) / effort, rounded to one decimal.
- impact 1-5: effect on the primary conversion goal or user experience.
- confidence 1-5: strength of the evidence (5 = reproduced automated evidence; 1 = untested hypothesis).
- effort 1-5: implementation cost (1 = trivial, 5 = project).
The formula orders work; it does not measure value in absolute terms. Hypotheses with confidence 1-2 should get verification tickets before fixes.
