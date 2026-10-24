# Preliminary Results

## Scope

This pre-participant pilot compares a paper-inspired naive Pretender prompt with a style-controlled prompt. It does not measure human identification accuracy, establish how human COMIG Judges reason, or treat the fixed anchors as expert ground truth.

## Generation quality assurance

- 8 questions × 2 conditions × 3 runs = 48 Pretender responses.
- All 48 expected responses were present and unique.
- All generations ended with `finish_reason=stop`; no response was truncated.
- Q0 remained separate from the eight-item main analysis.

## Surface-feature observations

Across the 24 responses in each condition:

| Feature | Naive | Style-controlled | Human anchors |
|---|---:|---:|---:|
| Mean word count | 447.417 | 41.917 | 40.750 |
| Mean list-item count | 18.292 | 0.000 | 0.000 |
| Mean heading count | 2.833 | 0.000 | 0.000 |
| Mean paragraph count | 13.917 | 1.000 | 1.000 |
| Mean comma density per 100 words | 5.694 | 6.976 | 9.709 |
| Mean sentence length | 15.665 | 20.222 | 15.739 |
| Mean first-person density per 100 words | 0.588 | 0.099 | 5.990 |
| Mean hedge count | 5.792 | 0.750 | 0.375 |

The style-controlled condition followed its explicit constraints closely: individual responses ranged from 35 to 48 words; all 24 contained zero list items, zero headings and one paragraph. In contrast, naive structure varied across runs, including list-item ranges of 12–39 for Q6, 11–27 for Q4 and 16–30 for Q8. The three-run design therefore captured instability that a one-generation design would miss.

Comma density increased under style control in six of eight questions, while mean sentence length also increased overall. This supports an **artifact-migration hypothesis** for the subsequent Judge audit: banning bullets and headings may relocate enumerative structure into comma-linked prose rather than eliminate it. This remains a hypothesis until Judge justifications show whether the cue is actually used.

Style control did not make the outputs uniformly more anchor-like. It aligned length, list use and paragraph structure, but first-person density moved further away from the anchors. Prompt effects should therefore be described feature by feature rather than as a single increase in “human similarity.”

Hedge density is not emphasized because one token produces a large per-100-word change in approximately 41-word outputs. Raw hedge counts are reported instead.

## Content-preservation check

The designated run-1 pairs were assessed manually by a single coder using the pre-specified five-field form.

- Comparable: 5/8 (Q2, Q3, Q5, Q7, Q8)
- Confounded: 3/8 (Q1, Q4, Q6)
- Core claim preserved: Yes in 5/8; Partial in 3/8; No in 0/8
- Technical error difference: None in 8/8
- Important content omission: Controlled omits in 8/8

The pre-specified majority-confounded rule was not triggered. The pilot therefore does **not** support the global conclusion that prompt-based style control was non-content-neutral across this setup. Instead, it found item-specific content confounding in Q1, Q4 and Q6, where compression removed or shifted parts of the requested reasoning process.

For the five comparable questions only, the same broad surface pattern remained descriptively visible: mean word count was 421.533 versus 42.133, mean list-item count was 16.667 versus 0, and mean comma density was 5.398 versus 6.442 for naive and style-controlled responses respectively. These are descriptive observations, not causal estimates.

## Implication for the Judge audit

The naive responses are much longer than both the anchors and controlled responses. A Judge may therefore identify authorship using length and list structure without reflecting on domain competence. The Judge audit should test whether:

1. `STYLE_FORMAT` dominates justifications in the naive condition;
2. comma-linked enumeration appears as a cue in the controlled condition;
3. length matching shifts attention toward substantive competence cues;
4. Judges disagree on whether polished detail signals human expertise or AI generation; and
5. limited first-person researcher voice affects judgments despite successful length matching.

## Claim boundary

The current results establish prompt sensitivity in generated surface form and identify three content-confounded items. They do not show that human COMIG participants use these cues, that either prompt is superior, or that identification performance reflects domain competence. Those questions require the planned Judge audit and later human validation.

## Limitation

The content-preservation check used one coder and one designated generation per condition. The sample is intentionally small and question-specific. Model aliases and routing may also change over time. Results should be treated as a transparent design pilot rather than a population estimate.
