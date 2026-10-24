# Auditing the Pretender Prompt in COMIG

## Do style controls change what LLM judges notice?

### Motivation

In COMIG, organisers write the prompt that asks an LLM Pretender to imitate a target social group. I asked whether that prompt itself creates surface artifacts that let judges identify the LLM through stylistic shortcuts rather than evidence of domain competence. I designed this as a pre-participant methodological audit, not as a substitute for a human COMIG study.

### Design

I compared a paper-inspired naive prompt with a style-controlled prompt across eight open-ended multilingual NLP and LLM-evaluation questions. I generated three responses per question and condition, giving 48 Pretender responses. Before inspecting model output, I froze the questions, human anchors, prompt conditions, codebook, A/B schedule, and core protocol, and recorded the freeze commits.

For the designated first generation, two LLM Judges compared each Pretender response with a fixed human anchor in both presentation orders. This produced 64 judgments: 32 per prompt condition. I coded all 64 justifications with condition and Judge labels masked, while recognising that wording could still reveal condition features. The codebook separates cue type, target response, and explicitly stated authorship direction.

### Findings

- **The composition of primary stated cues changed.** Style/form was the primary cue in 10/32 naive justifications and 2/32 controlled justifications. Across matched question × Judge × order cells, nine changed from style/form to non-style and one changed in the reverse direction. The exact two-sided McNemar test was `p = 0.021`.
- **No prompt-condition selection difference was detected.** The Pretender was selected as human in 24/32 naive judgments and 25/32 controlled judgments, with strongly overlapping Wilson intervals.
- **Selection stability depended strongly on the evaluator.** Judge 1 was order-stable on 4/16 pairs, whereas Judge 2 was stable on 15/16. The order-consistent aggregate was therefore dominated by Judge 2.
- **Style control introduced a content trade-off.** Mean length fell from 447.4 to 41.9 words and mean list-item count from 18.3 to zero. Five of eight designated pairs remained content-comparable, three were confounded, and every controlled response omitted important content.
- **Artifact migration is possible but exploratory.** Comma density increased under control in six of eight questions, consistent with enumeration moving from bullets into sentence-internal punctuation. Eight questions are insufficient for an inferential claim.

### Interpretation

Style control changed the composition of the Judges' stated primary cues, but this may partly reflect the removal of visible features available to mention. The pilot did not detect a corresponding change in aggregate selections. Evaluator choice strongly affected selection stability, and the controlled prompt reduced substantive coverage. Prompt controls should therefore be audited for content loss and displaced artifacts rather than assumed to remove nuisance variation cleanly.

For COMIG, this matters educationally as well as methodologically. If identification relies on prompt-induced surface artifacts, participants may practise detecting an AI writing style rather than articulating what competence means in their social world.

### Limitations

This pilot evaluates two LLM Judges, not human COMIG participants. I was the sole coder, and no independent second coder was used, so no inter-rater reliability statistic is reported. The application rules were refined during coding, after which all J001–J064 records were re-audited. Judge justifications were length-limited, so cue counts reflect stated cues rather than every cue the models may have used. Each presentation order was called once, so flipped pairs combine possible position sensitivity with run-to-run variability.

### Next step

I would next run a formally reviewed human validation study in a clearly defined social world. Participants would formulate questions as proxy researchers, and human Judges would provide selections, confidence, justifications, and reflections. A second coder would independently code a pre-specified subset. I would also test a prompt intervention that reduces obvious format shortcuts without forcing the response to match a 41-word anchor and thereby removing substantive content.

### Summary

> I audited whether the organiser's Pretender prompt could create stylistic shortcuts before COMIG involved human participants. Style control significantly shifted the primary cues stated by two LLM Judges, but I did not detect a change in their aggregate selections. The manipulation also removed substantive content, and selection stability differed sharply between evaluators. My main conclusion is therefore that prompt controls and evaluators both need validation before their outputs can support claims about competence or AI literacy.

### Reference

Segersven, O., & Mannila, L. (2025). Introducing the Competence Imitation Game: A Research and Teaching Tool for Context-Specific AI Literacy. In *AISEER'25: 2nd International Workshop on AI in Society, Education and Educational Research*, CEUR Workshop Proceedings, Vol. 4138. https://ceur-ws.org/Vol-4138/paper3.pdf
