# Cue Codebook v1.2

## Status and scope

Version 1.2 is the final coding manual for the completed pilot. It retains the cue taxonomy frozen in v1 before generation; v1.1 added recording fields after Q0 without changing that taxonomy. Version 1.2 documents the attribution rules that were made explicit during manual coding. These clarifications are not presented as pre-specified categories. After the rules were finalised, J001–J064 were re-audited for consistency.

The top-level unit is one Judge justification. Each justification receives one `PRIMARY_CUE` and zero or more cue-event records. Repeated cue codes are allowed when they describe distinct evidence spans. `OVERALL_JUDGMENT` is stored separately and excluded from cue-frequency denominators.

## Cue-event fields

| Field | Allowed values | Meaning |
|---|---|---|
| `CUE_CODE` | One code below | Type of stated evidence |
| `TARGET_RESPONSE` | `A`, `B`, `BOTH`, `COMPARISON` | Response described by the cue |
| `SIGNAL_DIRECTION` | `HUMAN_SIGNAL`, `AI_SIGNAL`, `UNSPECIFIED` | Explicit authorship inference attached to the cue |
| `EVIDENCE_SPAN` | Short verbatim span | Text supporting the event |

## Target-response rule

1. Follow the grammatical subject of the evidence span when it identifies a response.
   - “Response B is more detailed” → `B`.
   - “Response A is too brief” → `A`.
2. Use `BOTH` when one non-comparative statement explicitly applies to both responses.
3. Use `COMPARISON` only when the cue is genuinely relational and cannot be assigned without losing its meaning.
4. Do not use `COMPARISON` merely because the sentence contains “more,” “less,” or contrasts two responses; assign the cue to the response whose property is being described.

## Signal-direction rule

1. Code `HUMAN_SIGNAL` or `AI_SIGNAL` only when the justification explicitly links that cue to an authorship inference.
2. Do not infer direction from the final selected response, confidence score, positive or negative evaluation, or presumed competence.
3. Use `UNSPECIFIED` when the Judge states a difference or quality assessment without attaching it to human or AI authorship.
4. An anaphoric sentence such as “This is characteristic of a human researcher” applies only to the cue or cue unit clearly referenced by “this.”
5. A trailing relation such as “which feels more AI-generated” applies to its nearest grammatically supported cue unit. Extend it to the whole response only when the response itself is the clear antecedent.
6. When coordinated cues share an explicit attribution, assign the direction to each coordinated cue. Do not extend it across a sentence boundary without an explicit link.
7. An explicit contrast with the expected target-group author (e.g., “expected from a postgraduate researcher”) counts as an authorship link and can receive `AI_SIGNAL`; an expectation tied only to the question or domain (e.g., “expected for this question” or “expected in this domain”) remains `UNSPECIFIED`.
8. “Expert analysis” or “expert explanation” alone is not an authorship link and remains `UNSPECIFIED`; “a human expert” or “a human researcher” is an explicit authorship link and can receive `HUMAN_SIGNAL`.

## Primary-cue rule

`PRIMARY_CUE` is the first eligible cue that explicitly supports the concluding authorship judgment. Introductory restatements and the final selection itself do not count. If two cue types are inseparable or their ordering is genuinely ambiguous:

- retain the first eligible cue as `PRIMARY_CUE`;
- set `PRIMARY_CUE_AMBIGUOUS: Yes`; and
- name one `COMPETING_CUE` in the `Competing cue` field.

This is a reproducibility rule, not a claim that the first-mentioned cue was psychologically decisive.

## Cue taxonomy

### `STYLE_FORMAT`

Length and visual or structural form: bullets, numbered lists, headings, paragraphing, sentence length, punctuation patterns, brevity, verbosity, or checklist structure. A list is not automatically an AI stereotype.

### `STYLE_REGISTER`

Tone or discourse register: formal, conversational, casual, polished, academic, direct, impersonal, boilerplate, or reviewer-like phrasing. Use `LANGUAGE_FORM` for grammaticality and idiomaticity.

### `LANGUAGE_FORM`

Grammar, idiomaticity, fluency, awkward phrasing, tense or agreement, spelling, capitalisation, and typographical form. Do not independently infer a writer's language background.

### `AI_STEREOTYPE`

An explicit expectation about typical AI writing, including “sounds AI-generated,” formulaic survey structure, generic AI framing, templated language, or excessive polish explicitly linked to AI authorship. Genericity without an AI attribution is coded by the underlying substantive, format, or register cue with `UNSPECIFIED` direction.

### `TECHNICAL_SUBSTANCE`

Factual or conceptual accuracy, technical terminology, methodological depth, relevant evidence, explanation quality, substantive coverage, errors, vagueness, or precision.

### `CONTEXT_SENSITIVITY`

Attention to assumptions, exceptions, cultural or linguistic variation, trade-offs, alternative explanations, situational constraints, or need for additional context.

### `EPISTEMIC_STYLE`

Expression of certainty and evidential restraint: hedging, calibration, qualification, acknowledgement of insufficient evidence, overconfidence, or causal overclaiming.

### `EXPERIENTIAL_TACIT`

Practical or tacit workflow knowledge: realistic debugging sequences, actionable next steps, concrete failure modes, procedural judgment, hands-on experimentation, or references to observed research practice.

### `SOCIAL_MEMBERSHIP`

Shared roles, practices, terminology, or experiences that explicitly index membership in the target social world. General NLP knowledge is insufficient.

### `CONTENT_DIFFERENCE`

A substantive difference the Judge explicitly identifies between the human anchor and Pretender response. This does not code differences between prompt conditions; those are handled by the separate content-preservation check.

### `OVERALL_JUDGMENT`

The final holistic selection or assessment, such as “more convincing” or “A is human.” Store separately and exclude from evidence-cue counts.

### `UNCLEAR_OTHER`

A stated reason that cannot be assigned to another code. Preserve the evidence span and explain the uncertainty in a memo.

## Event segmentation

- Merge adjacent phrases when they express one cue type about the same target with the same direction.
- Split when cue type, target, or signal direction changes.
- Treat “structured approach/answer/plan” as a response-form cue (`STYLE_FORMAT`); when “structured” modifies a content noun such as “structured experimental controls” or “structured reasoning,” keep it with the substantive cue unless form is independently invoked.
- Treat examples as part of the cue they instantiate unless they introduce a distinct evidential property.
- Exclude confidence statements such as “both are plausible” unless they are themselves used as an authorship cue.
- Preserve contradictory cues rather than resolving them. The same property may be treated as a human signal in one justification and an AI signal in another.

## Reliability record

I completed the main coding as the sole coder. No independent second coder was used, so no inter-rater reliability statistic is reported. The target and attribution rules evolved during coding; J001–J064 were therefore re-audited under this final manual. A future study should use a second independent coder on a pre-specified subset before reporting Cohen's kappa or Krippendorff's alpha.

## Version history

- **v1:** Pre-generation cue taxonomy.
- **v1.1:** Added `TARGET_RESPONSE`, `SIGNAL_DIRECTION`, and `EVIDENCE_SPAN` after the Q0 development run exposed opposite interpretations of the same response features.
- **v1.2:** Finalised grammatical-target, authorship-attribution-scope, segmentation, and genericity rules; recorded the J001–J064 consistency re-audit. No new cue category was added.
