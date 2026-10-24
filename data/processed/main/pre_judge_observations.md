# Pre-Judge Observations

These observations were recorded after surface-feature extraction and before the main Judge audit. They are descriptive hypotheses, not findings about which cues the Judges will use.

## Length and format control

- Mean word count: naive 447.417; style-controlled 41.917; main human anchors 40.750.
- Individual style-controlled responses ranged from 35 to 48 words; question-level means ranged from 40.333 to 44.000.
- Individual naive responses ranged from 309 to 593 words.
- All 48 generations ended with `finish_reason=stop`; no response was truncated.
- Style-controlled outputs had zero list items, zero headings, and one paragraph in all 24 cases.
- Naive list structure varied substantially across runs, including Q6 (12–39 list items), Q4 (11–27), and Q8 (16–30). Three runs therefore reveal instability that a single generation would conceal.

## Artifact migration hypothesis

Comma density was higher under style control for six of eight questions, and mean sentence length was generally higher. A plausible hypothesis is that banning bullets and headings did not remove enumerative structure but relocated it into comma-linked prose. This matters because the COMIG Introduction includes a Judge assessment that treats comma-linked list-like style as an AI cue. Whether the main Judges actually invoke this cue remains to be tested in the Judge audit.

## Anchor alignment is multidimensional

First-person density per 100 words was 5.990 in the main human anchors, 0.588 in naive responses, and 0.099 in style-controlled responses. Style control moved outputs toward anchors in length and visible formatting but away from them on first-person researcher voice. Prompt matching should therefore not be described as globally increasing human similarity.

## Reporting caution

Hedge density is unstable for approximately 41-word outputs because a difference of one token produces a large per-100-word change. Hedge raw counts should be primary; density can be shown only as a secondary descriptive statistic.

