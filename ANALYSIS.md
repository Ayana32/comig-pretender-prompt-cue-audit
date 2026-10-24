# Analysis report

## Design

This descriptive pilot compared a paper-inspired naive Pretender prompt with a style-controlled prompt across eight multilingual NLP and LLM-evaluation questions. The Pretender produced three responses per question and condition. Surface features use all 48 responses. Content checks and the Judge audit use the pre-designated first run only.

Two LLM Judges evaluated each human-anchor–Pretender pair in original and swapped presentation orders. This produced 64 justifications. One coder applied the final v1.2 manual to 285 cue events. The study did not recruit human participants and does not estimate human identification accuracy.

## Confirmatory descriptive result

Style/form was the primary stated cue in 10/32 naive-condition justifications and 2/32 style-controlled justifications. Across matched question × Judge × order cells, nine moved from style/form under the naive prompt to a non-style primary cue under control, while one moved in the reverse direction. The exact two-sided McNemar test is `p = 0.021`.

This supports a change in the composition of stated cues. It does not show that the Judges' latent reasoning changed independently of the stimuli because the controlled condition removed much of the visible formatting variation.

## Selection result

The Pretender was selected as human in 24/32 naive calls and 25/32 controlled calls. The Wilson 95% intervals overlap substantially. The pilot therefore did not detect a prompt-condition difference in aggregate selections.

Judge stability differed sharply. Judge 1 flipped response identity in 12/16 original–swapped pairs; Judge 2 flipped in 1/16. Since each order was called once, these flips do not separate position sensitivity from ordinary run-to-run variation.

## Prompt trade-offs

The style-controlled responses averaged 41.9 words compared with 447.4 under the naive prompt and 40.75 for the human anchors. Lists fell from 18.3 items per naive response to zero under control. However, controlled responses omitted important content in all eight designated comparisons. Five remained comparable and three were marked confounded.

Comma density increased under control in six of eight questions. This is compatible with artifact migration from bullet lists into sentence-internal enumeration, but it remains exploratory.

## Cue-event interpretation

Style/form events fell from 2.31 to 0.91 per justification. Substantive/practical events were similar at 2.91 and 2.78. Justifications containing only `UNSPECIFIED` authorship directions rose from 1/32 to 8/32. This suggests that controlled-condition Judges more often discussed response quality without explicitly explaining why that quality indicated human or AI authorship.

## Claim boundary

- Results describe two LLM Judges, not human COMIG participants.
- Human anchors were written by one multilingual researcher and are not gold-standard expert answers.
- Prompt control changed content as well as style.
- Aggregate selection comparisons are underpowered.
- Stable-pair summaries are dominated by Judge 2.
- One coder completed the coding; no inter-rater reliability estimate is available.
- Model endpoints and routing may change, so exact API reproduction is not guaranteed.

## Main conclusion

In this sample, style control changed what LLM Judges said they noticed more clearly than what they selected. It also introduced content loss and did not remove every possible stylistic artifact. COMIG prompt controls should therefore be audited for both shortcut reduction and construct distortion before participant deployment.
