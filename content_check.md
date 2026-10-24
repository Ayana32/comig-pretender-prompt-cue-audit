# Content-Preservation Check v1

## Purpose and unit

This manual check assesses whether the style-controlled prompt changes substantive content relative to the paper-inspired naive prompt. The unit is one question's designated-run pair:

- Condition 1: paper-inspired naive pretender response
- Condition 2: style-controlled pretender response

The human anchor is not part of this comparison and neither pretender response is treated as a gold-standard answer. The check is applied to Q1–Q8 only. Q0 is used for development and excluded from the main content-preservation results.

## Five-field record

| Field | Allowed values | Operational question |
|---|---|---|
| `CORE_CLAIM_PRESERVED` | `Yes`, `Partial`, `No` | Does the controlled response retain the naive response's main conclusion and central reasoning? |
| `TECHNICAL_ERROR_DIFFERENCE` | `None`, `Naive worse`, `Controlled worse` | Does one response contain a material technical error not present, or less severe, in the other? |
| `IMPORTANT_CONTENT_OMISSION` | `None`, `Naive omits`, `Controlled omits`, `Both/different` | Does either response omit an important qualification, step, or consideration present in the other? |
| `ADDITIONAL_CLAIM` | `None`, `Naive adds`, `Controlled adds`, `Both/different` | Does either response introduce a substantive claim absent from the other rather than merely rephrase it? |
| `OVERALL_COMPARABILITY` | `Comparable`, `Confounded` | Can their surface features be compared as two substantively similar attempts, or is content change large enough to confound interpretation? |

Each record also includes short evidence notes. Notes should identify the relevant claim, error, omission, or addition without rewriting either response.

## Decision rules

### `CORE_CLAIM_PRESERVED`

- `Yes`: the same main conclusion and central rationale are present, allowing compression or paraphrase.
- `Partial`: the conclusion remains but a central rationale, condition, or qualification changes or disappears.
- `No`: the conclusion reverses, the response answers a materially different question, or the central rationale is replaced.

### `TECHNICAL_ERROR_DIFFERENCE`

Use `None` when there is no identifiable difference in material technical correctness, including cases where both responses share the same possible error. Use a directional value only for a specific, memoed error. Differences in depth, phrasing, or caution alone are not technical errors.

### Omission and addition

These fields are relational rather than absolute-quality judgments. `Naive omits` means important content appears only in the controlled response; `Controlled omits` means it appears only in the naive response. `Both/different` means each omits or adds distinct substantive material, preventing a single direction. Minor examples, discourse markers, and stylistic elaboration do not count unless they change the answer's substance.

### `OVERALL_COMPARABILITY`

- `Comparable`: differences are primarily stylistic, or substantive differences are small enough that the planned surface-feature comparison remains interpretable.
- `Confounded`: changed conclusions, material accuracy differences, major omissions/additions, or substantially different solution strategies make a style-only interpretation unsafe.

`Confounded` cases are retained and flagged; they are never deleted or regenerated to obtain a cleaner comparison. Surface features may still be reported descriptively, but the case is excluded from any claim that differences arose from style control alone.

## Recording template

| Field | Entry |
|---|---|
| `question_id` | `Q1`–`Q8` |
| `run_id` | `run_1` |
| `CORE_CLAIM_PRESERVED` | `Yes` / `Partial` / `No` |
| `TECHNICAL_ERROR_DIFFERENCE` | `None` / `Naive worse` / `Controlled worse` |
| `IMPORTANT_CONTENT_OMISSION` | `None` / `Naive omits` / `Controlled omits` / `Both/different` |
| `ADDITIONAL_CLAIM` | `None` / `Naive adds` / `Controlled adds` / `Both/different` |
| `OVERALL_COMPARABILITY` | `Comparable` / `Confounded` |
| `evidence_note` | Brief text |

## Version rule

Version v1 is frozen before Q0. Q0 may expose an unclear definition or missing recording instruction; any change is documented as v1.1 with its reason before main generation. Any Q0 record already coded with v1 is recoded using v1.1; model responses are not regenerated for a coding-form revision. Once main generation begins, the form and definitions are not revised. Unexpected patterns are retained in notes rather than retrofitted into v1.
