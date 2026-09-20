# Cue Codebook v1

## Unit and general rules

The basic unit is one complete LLM-judge justification. Multiple cue codes are allowed. Each justification receives one `PRIMARY_CUE`; `OVERALL_JUDGMENT` is recorded separately and is not counted as evidence in cue-distribution summaries. Code only cues that are stated or directly supported by the justification. Do not infer author identity, language background, or competence beyond what the judge states.

## PRIMARY_CUE rule

The primary cue is the first cue mentioned in the judge's explanation that explicitly supports its concluding authorship judgment. Introductory restatements and the overall selection itself do not count as cues. If two cues are presented as inseparable or their ordering is genuinely ambiguous, retain the first eligible cue as `PRIMARY_CUE` and add `PRIMARY_CUE_AMBIGUOUS: true` with a short memo naming the competing cue. This mechanical rule is used for consistency and does not imply that the first-mentioned cue was psychologically decisive.

## Codes

### `STYLE_FORMAT`

Length and visual or structural form: bullet points, numbered lists, headings, paragraph structure, sentence length, punctuation patterns, or unusual brevity/verbosity. Excludes register and grammaticality.

### `STYLE_REGISTER`

Tone or discourse register: formal, conversational, casual, polished, academic, direct, or impersonal. Excludes local language-form errors and generic-AI attributions.

### `LANGUAGE_FORM`

Grammaticality, idiomaticity, awkward phrasing, tense/agreement patterns, spelling, capitalisation, or typographical errors. A judge's explicit reference to non-native-like phrasing is coded here, but the coder must not independently infer an author's language background.

### `AI_STEREOTYPE`

An explicit expectation about typical AI writing: generic, formulaic, templated, overly polished, predictable framing, or an explicit statement that a response “sounds like AI.” A list alone is `STYLE_FORMAT` unless the judge connects it to an AI stereotype.

### `TECHNICAL_SUBSTANCE`

Factual or conceptual accuracy, technical error, relevant evidence, methodological depth, explanation quality, or substantive question coverage.

### `CONTEXT_SENSITIVITY`

Attention to assumptions, exceptions, situational variation, trade-offs, alternative explanations, or the need for additional context.

### `EPISTEMIC_STYLE`

The expression of certainty or uncertainty: hedging, calibrated uncertainty, qualification, acknowledgement of insufficient evidence, or overconfidence.

### `EXPERIENTIAL_TACIT`

Cues suggesting practical research experience or tacit workflow knowledge, such as realistic debugging steps, concrete failure modes, or experience-grounded procedural judgment.

### `SOCIAL_MEMBERSHIP`

Shared practices, terminology, roles, or experiences that explicitly index membership in the target social world. General NLP knowledge alone is not sufficient.

### `CONTENT_DIFFERENCE`

A substantive difference that the judge explicitly identifies between the two responses it is comparing: the fixed human anchor and one pretender response. Examples include one response containing an important concept, conclusion, justification, or omission absent from the other. This code does not assess differences between Condition 1 and Condition 2; prompt-condition content neutrality is handled separately by the content-preservation check.

### `OVERALL_JUDGMENT`

The final holistic selection or assessment, such as “more convincing,” “more likely to be human,” or “Answer A is human.” It is stored separately from the evidence cues and excluded from cue-frequency denominators.

### `UNCLEAR_OTHER`

A stated reason that cannot be assigned clearly to another code. Preserve the text and add a memo. Repeated patterns are recorded after main generation as candidate `EMERGENT_*` codes without modifying v1.

## v0 excerpt test

The public Introduction example was used only to test whether v0 separated judgment from evidence. The judge's attention to comma-linked/list-like presentation maps to `STYLE_FORMAT`; recognition that problem-solving depends on the situation maps to `CONTEXT_SENSITIVITY`; and the statement that one response is more convincing maps to `OVERALL_JUDGMENT`. `AI_STEREOTYPE` is added only if the judge explicitly links the format to expected AI behaviour. The test supported retaining separate surface, substantive, and judgment codes in v1.

