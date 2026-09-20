# Protocol v1 — Pre-dry-run freeze

## Scope

This is a pre-participant methodological stress test, not a COMIG participant study. It tests whether pretender-prompt conditions introduce observable surface artifacts, whether LLM judges invoke such artifacts in their justifications, and whether a pre-specified cue codebook can capture the resulting patterns.

It does not measure human identification accuracy, claim that human judges use the same cues as LLM judges, establish representativeness of the Sheffield NLP community, or treat the fixed human anchors as gold-standard expert answers.

## Items and anchors

- Q0: dry-run development item; excluded from main analysis.
- Q1–Q8: main items.
- Human anchors: frozen before model generation.
- Main-anchor mean: 40.75 whitespace-separated words.
- Style target: approximately 41 words.

## Generation

```yaml
pretender_model: TBD_after_Q0_access_test
temperature: 0.7
top_p: 0.95
max_output_tokens: 1024
runs_per_condition: 3
designated_run: run_1
seed_policy: use_only_if_supported; otherwise record_unsupported
finish_reason_recorded: true
```

The same model and supported parameters are used across both conditions. Every response records the exact model ID or alias, provider, access tier, access date, supported parameters, output-token count where available, and finish reason. Responses terminated by an output-token limit are retained as documented cases but excluded from length and mean-sentence-length comparisons.

Because free access tiers may change model aliases, backend providers, limits, or availability over time, exact reproducibility is not guaranteed. The exact identifier exposed by the provider and execution date will be recorded.

## Analysis scope

- Surface features: all 48 main pretender responses plus all 9 human anchors.
- Content-preservation check: Q1–Q8, designated run only.
- Judge audit: Q1–Q8, both conditions, designated run only.
- Manual cue coding: all designated-run judge justifications.
- Optional automated coding: exploratory concordance only; the manual coder is not treated as ground truth.

## Judge models

```yaml
judge_model_1: TBD_after_Q0_access_test
judge_model_2: TBD_after_Q0_access_test
distinct_families_from_pretender_and_each_other: required
```

Using distinct families reduces direct self-enhancement confounding but does not guarantee evaluator independence.

Judge calls use `judge_prompt.md` v1, including its forced A/B choice, confidence scale, justification-length guidance, JSON schema, and invalid-output policy. Q0 tests parse stability before the judge models are frozen.

## Pre-specified A/B presentation schedule

The original presentation is balanced across Q1–Q8, with four anchors in position A and four in position B. This schedule is fixed before judge calls. For each condition and judge, the original evaluation uses the scheduled placement; the swapped evaluation reverses A and B while preserving response content.

| Question | Original human-anchor position | Original pretender position | Swapped human-anchor position | Swapped pretender position |
|---|---|---|---|---|
| Q1 | B | A | A | B |
| Q2 | A | B | B | A |
| Q3 | B | A | A | B |
| Q4 | B | A | A | B |
| Q5 | A | B | B | A |
| Q6 | A | B | B | A |
| Q7 | B | A | A | B |
| Q8 | A | B | B | A |

The schedule is reused for both prompt conditions and both judge models so condition and judge comparisons do not introduce different item-level position assignments.

## Coding rules

- Codebook version: v1, frozen before inspecting model output.
- Multiple cue codes are allowed.
- One `PRIMARY_CUE` is assigned using the first-eligible-supporting-cue rule in the codebook.
- Ambiguous primary assignments are flagged and memoed.
- `OVERALL_JUDGMENT` is stored separately from evidence cues.
- `CONTENT_DIFFERENCE` refers only to substantive differences the judge identifies within an anchor–pretender comparison.
- Condition-to-condition content preservation is assessed separately.
- Condition-to-condition preservation is recorded with `content_check.md` v1 for Q1–Q8 designated-run pairs; confounded cases are retained and flagged.
- After main generation, new patterns are recorded as `EMERGENT_*`; v1 is not rewritten.

## Language-form limitation

The fixed human anchors were written in English by a multilingual researcher for whom English is not a first language. LLM judges may use grammaticality or idiomaticity as authorship cues. The audit records these under `LANGUAGE_FORM` but does not assume that they reliably indicate linguistic background or domain competence. Some cue patterns may also reflect item-specific variation in the author's familiarity, especially for questions close to the author's dissertation topic.

## Ethics-by-design boundary

No external human participants are recruited, no sensitive personal information is collected, and no human identification accuracy is measured. A future validation study would recruit judges and non-pretenders from a defined social world, allow judges to formulate their own questions, obtain informed consent, specify data retention, and undergo formal ethical review before collection or dissemination.
