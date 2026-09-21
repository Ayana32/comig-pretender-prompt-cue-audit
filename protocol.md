# Protocol v1.5 — stable paid model endpoints

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
pretender_model_candidate: openai/gpt-4.1-mini
catalog_canonical_slug_observed: openai/gpt-4.1-mini-2025-04-14
access_tier: paid
retired_candidates:
  - qwen/qwen3.8-27b:free
  - z-ai/glm-5.2:free
  - mistralai/mistral-small-2603
model_status: candidate_until_Q0_gate_passes
temperature: 0.7
top_p: 0.95
max_output_tokens: 1024
reasoning: not_applicable_or_not_requested
runs_per_condition: 3
designated_run: run_1
seed_policy: use_only_if_supported; otherwise record_unsupported
finish_reason_recorded: true
```

The same model and supported parameters are used across both conditions. Every response records the exact model ID or alias, provider, access tier, access date, supported parameters, output-token count where available, and finish reason. Responses terminated by an output-token limit are retained as documented cases but excluded from length and mean-sentence-length comparisons.

Reasoning is explicitly disabled for Judge calls that support the parameter because the Q0 dry run showed that provider-default reasoning differed across model families and could consume most of the shared `max_tokens` budget. The initial Qwen controlled response used 799 reasoning tokens before producing a 41-word visible answer, while one naive HTTP-200 response had no string content. GPT-4.1 Mini does not advertise a reasoning parameter, so that field is omitted rather than sending an unsupported control. This decision was first recorded as protocol v1.1; free-model replacements were recorded in v1.2, the first paid candidate in v1.3, the stable OpenAI candidate in v1.4, and the stable paid Judge 2 candidate in v1.5.

Because free access tiers may change model aliases, backend providers, limits, or availability over time, exact reproducibility is not guaranteed. The exact identifier exposed by the provider and execution date will be recorded.

## Analysis scope

- Surface features: all 48 main pretender responses plus all 9 human anchors.
- Content-preservation check: Q1–Q8, designated run only.
- Judge audit: Q1–Q8, both conditions, designated run only.
- Manual cue coding: all designated-run judge justifications.
- Optional automated coding: exploratory concordance only; the manual coder is not treated as ground truth.

## Judge models

```yaml
judge_model_1_candidate: nex-agi/nex-n2.5-mini:free
judge_model_1_catalog_canonical_slug_observed: nex-agi/nex-n2.5-mini-20260908
judge_model_2_candidate: google/gemini-2.5-flash-lite
judge_model_2_catalog_canonical_slug_observed: google/gemini-2.5-flash-lite
judge_response_format: json_object
reasoning: disabled
model_status: candidates_until_Q0_gate_passes
distinct_families_from_pretender_and_each_other: required
```

Using distinct families reduces direct self-enhancement confounding but does not guarantee evaluator independence.

The original candidate IDs were retrieved from the OpenRouter models API on 2026-09-20 UTC; replacement availability and supported parameters were checked again on 2026-09-21 UTC. Canonical slugs are provenance records rather than guarantees of a fixed backend. GPT-4.1 Mini is the paid Pretender, Nex is Judge 1, and paid Gemini 2.5 Flash-Lite is the Judge 2 candidate. The Judge models advertise structured or JSON response support. Gemini is not frozen as Judge 2 until it passes three Q0 schema-valid calls.

Qwen was retired after a separately timed retry on 2026-09-21 again failed both required conditions: the naive request returned HTTP 200 without string content, while the style-controlled request exhausted retries with upstream HTTP 429. Gemma was retired after two separately timed diagnostics produced 0/6 successful calls, all due to upstream HTTP 429. A subsequent authenticated replacement gate found Nex schema-valid on 3/3 calls, but both GLM Pretender conditions exhausted retries because its free upstream provider was overloaded. Nex is therefore retained as Judge 1, while GLM is retired. Paid Mistral then completed the naive condition but exhausted upstream 429 retries for the style-controlled condition. GPT-4.1 Mini passed both Pretender conditions and is frozen. In the complete Q0 run, Nemotron produced only 1/3 schema-valid outputs; the other two raw responses were explicit NVIDIA `503 provider_overloaded` errors. Nemotron is therefore retired and paid Gemini 2.5 Flash-Lite becomes the final Judge 2 candidate.

For the Q0 access and parsing gate only, the human anchor is placed in A and the naive Pretender output in B. Each Judge candidate evaluates this same pair independently three times. If the live naive output is unavailable, Judges instead receive a frozen diagnostic Pretender fixture so their access and JSON compliance can still be tested. Fixture-based outputs are marked as diagnostics and excluded from cue coding, condition comparison, and all identification claims. A failure in any model is recorded without preventing the remaining model endpoints from being attempted.

Judge calls use `judge_prompt.md` v1, including its forced A/B choice, confidence scale, justification-length guidance, JSON schema, and invalid-output policy. Q0 tests parse stability before the judge models are frozen.

The judge prompt and pretender shared base describe the same target social world: postgraduate researchers in speech and natural language processing with relevant multilingual language-model evaluation experience. This alignment is intentional, but it may also shape which membership cues judges attend to and is therefore part of the documented setup.

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
