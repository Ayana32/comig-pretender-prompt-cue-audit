# Canonical Q0 Dry-Run Analysis

Canonical API run: `20260921T184834Z`  
Purpose: development and instrument validation only; excluded from Q1-Q8 results.

## Gate outcome

- Pretender conditions completed: 2/2.
- Judge outputs schema-valid: 6/6.
- Full Q0 gate: passed.
- Final models: GPT-4.1 Mini Pretender; Nex Judge 1; Gemini 2.5 Flash-Lite Judge 2.

## Surface-feature observation

The fixed human anchor contained 40 words, the naive Pretender response 347, and the style-controlled response 41. The naive response contained eight detected list items and ten paragraphs; both the anchor and controlled response contained no list items and one paragraph. The style clause therefore removed a strong formatting shortcut and achieved the intended approximate length target.

However, the content-preservation check marked Q0 `Confounded`: the controlled response retained the central recommendation but omitted much of the naive response's substantive coverage. Surface differences are descriptive and cannot be attributed solely to style control.

## Judge-disagreement observation

Nex selected the true human anchor A on all three calls, using terseness, roughness, awkward phrasing, and limitation-focused language as human signals while treating polished structure as an AI signal. Gemini selected Pretender response B on all three calls, treating detail, structure, concrete methods, and field-appropriate depth as human-expertise signals.

The same structured and detailed presentation therefore moved perceived humanness in opposite directions across judges. Aggregate cue counts alone would conceal this disagreement, motivating codebook v1.1's cue-level target and signal-direction fields. Because this observation comes from one development item, a fixed diagnostic setup, and three repeated calls per judge, it is recorded only as a hypothesis: the main analysis will test whether directionally opposed readings recur across Q1-Q8.

Nex explicitly cited the anchor phrase “I have to claim” as evidence in its authorship judgment. This is the first observed case in which the anchor's language form contributed to the decision and confirms the relevance of the pre-specified `LANGUAGE_FORM` code. It does not establish that such language reliably identifies human authorship or competence.

## Instrument decisions

- Surface-feature extractor: retained for main generation.
- Content-preservation form: v1 retained unchanged.
- Cue taxonomy: retained.
- Cue-record schema: revised from v1 to v1.1 before main generation to add `TARGET_RESPONSE`, `SIGNAL_DIRECTION`, and `EVIDENCE_SPAN`.
- Q0 outputs and observations: excluded from main summary statistics.
