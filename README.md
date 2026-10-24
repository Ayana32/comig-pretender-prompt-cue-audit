# COMIG Pretender Prompt and Cue Audit

An independent pilot that builds on the Competence Imitation Game (COMIG) introduced by Segersven and Mannila (2025). It is not part of, or endorsed by, the original COMIG project.

## In brief

- **Question:** Can the organiser's Pretender prompt create stylistic shortcuts that distract from domain competence?
- **Design:** 8 questions × 2 prompt conditions × 3 generations; two LLM evaluators assessed the pre-designated first runs in both A/B orders.
- **Result 1:** Style/form was the primary stated cue in **10/32** naive justifications and **2/32** controlled justifications.
- **Result 2:** Pretender-as-human selections barely changed (**24/32** vs **25/32**), while order consistency differed sharply between evaluators.
- **Limit:** This was a pre-participant audit with one human coder, researcher-written anchors, and no human COMIG Judges.

> **Takeaway:** Style control changed what evaluators said they noticed more than what they selected, but it also removed substantive content. Prompt controls and evaluators should therefore be audited before COMIG outcomes are interpreted as evidence about competence.

## Why this matters

In COMIG, organisers prompt an LLM Pretender to imitate members of a social world. If the prompt produces obvious artifacts—such as excessive length, lists, or formulaic prose—a Judge may identify writing style without reflecting on domain competence. This pilot tests that validity risk before recruiting participants.

## Relation to COMIG

| COMIG component | This pilot |
| --- | --- |
| Human Judges from a social world | Two LLM evaluators used only as diagnostic tools |
| Participant-generated questions | Researcher-finalised technical questions |
| Human Non-Pretender responses | Fixed researcher-written anchors |
| Pretender imitation | GPT-4.1 Mini under two organiser-prompt conditions |
| Identification, confidence, justification, reflection | Selection, confidence, and justification audited; no participant reflection |

This pilot does **not** estimate human identification accuracy or replace participant Judges.

## Design

| Component | Setting |
| --- | --- |
| Questions | 8 open-ended multilingual NLP/LLM-evaluation questions |
| Human anchors | Written by the researcher without AI rewriting; mean **40.75 words** |
| Pretender | GPT-4.1 Mini |
| Naive condition | Shared imitation prompt only |
| Style-controlled condition | Approximately **41 words**, conversational prose, no lists or headings |
| Generations | 3 per question and condition (**48 total**) |
| Evaluator audit | Pre-designated `run_1` only; both A/B orders |
| Evaluator 1 | Nex N2.5 Mini |
| Evaluator 2 | Gemini 2.5 Flash Lite |
| Evaluator outputs | **64** schema-valid justifications |
| Manual coding | **285** cue events, coded by one human coder |

For each stated cue, coding recorded:

- **cue type:** what feature the evaluator mentioned;
- **target response:** which answer the feature described;
- **authorship direction:** whether it was explicitly treated as a human signal, AI signal, or neither; and
- **evidence span:** the exact supporting words in the justification.

Condition and evaluator labels were masked during coding, although wording could reveal response features, so this was **label-masked rather than fully blind**. The individual cue taxonomy was fixed before generation; Q0 then motivated the addition of target, direction, and evidence-span fields before the main run.

## Main results

### 1. The primary stated cue changed

| Condition | Style/form primary cue | Other primary cue |
| --- | ---: | ---: |
| Naive | 10/32 | 22/32 |
| Style-controlled | 2/32 | 30/32 |

Across matched question × evaluator × order cells, 9 changed from style/form to non-style and 1 changed in the reverse direction. The exploratory exact McNemar test gave **p = 0.021**. This supports a change in the composition of *stated cues*, not direct access to an evaluator's internal reasoning.

The same format cue did not have a fixed meaning. Among naive `STYLE_FORMAT` events with an explicit authorship direction, **14 were AI signals and 12 were human signals**.

### 2. Selections barely changed, but evaluators behaved differently

| Evaluator | Pretender selected as human | Original–swapped flips |
| --- | ---: | ---: |
| Evaluator 1 — Nex | 18/32 | 12/16 |
| Evaluator 2 — Gemini | 31/32 | 1/16 |
| **Both evaluators** | **49/64** | **13/32** |

By prompt condition, the Pretender was selected as human in **24/32** naive and **25/32** controlled evaluations. No condition difference was detected in this small sample. A flip is consistent with order sensitivity, but cannot be separated from run-to-run variation because each order was evaluated once.

### 3. Style control had a content cost

| Measure | Naive | Style-controlled |
| --- | ---: | ---: |
| Mean words | 447.4 | 41.9 |
| Mean list items | 18.3 | 0 |
| Important omissions | — | 8/8 |

Core claims were fully preserved in **5/8** pairs and partly preserved in **3/8**. Five pairs remained comparable and three were marked confounded; therefore, the pre-specified threshold of more than 4/8 confounded pairs was not reached.

Comma density nevertheless increased under control in 6/8 questions. This is exploratory evidence that an artifact may be displaced rather than removed—for example, from bullets into sentence-internal enumeration.

## One illustrative item: Q6

**Question:** *You inherit a multilingual LLM experiment repository whose reported results you cannot reproduce. What would you inspect first, and how would you determine where the discrepancy comes from?*

**Researcher-written human anchor — 47 words**

> First, I would identify which parts of the experiment are reproducible and which are not, and document why the non-reproducible parts cannot be reproduced. Then, I would trace the pipeline step by step and record intermediate outputs at each stage to localise where the discrepancy comes from.

**Naive Pretender — 563 words, excerpt**

> Given the scenario of inheriting a multilingual LLM experiment repository with irreproducible reported results, here is how I would approach the investigation... Check the experimental setup and environment... Validate the data processing pipeline...

[View the complete naive response](data/raw/main_generation/20260922T173531Z/calls/Q6__naive__run_1.json).

**Style-controlled Pretender — 39 words**

> I'd start by verifying the exact model checkpoints, tokenizers, and preprocessing scripts to ensure alignment with the original setup. Then, I'd check the evaluation metrics and data splits used, since subtle differences there often cause discrepancies in multilingual benchmarks.

The controlled answer removed the obvious length and list cues, but also omitted the anchor's key proposal to compare intermediate outputs and locate the first point of divergence. This pair was therefore marked **Confounded**.

## Examples from evaluator justifications

| Coded cue | Evaluator's words | Interpretation |
| --- | --- | --- |
| Format → AI | “Response A is more verbose” | A surface feature was used as an AI signal. |
| Format → human | “it is structured” | The same broad cue family could also support human authorship. |
| Workflow → human | “sounds more like a researcher's practical workflow: it names concrete checks” | Practical detail was treated as evidence of human expertise. |
| Language form → human | “Its slightly awkward phrasing also feels more human” | Non-native-like language form became an authorship cue. |

## Pre-specified and exploratory analyses

| Fixed before the main analysis | Exploratory after inspecting results |
| --- | --- |
| Two prompt conditions and three generation runs | Broad style/form vs substantive/practical families |
| `run_1` designated for evaluator audit and content checks | Exact McNemar test on primary-cue-family shifts |
| A/B presentation schedule and swapped evaluation | Comma-density artifact-migration interpretation |
| Individual cue taxonomy | Cross-condition interpretation of stated cue composition |
| Direction-stratified cue counting |  |
| Content-confound threshold: more than 4/8 pairs |  |

For summaries, **style/form** includes `STYLE_FORMAT`, `STYLE_REGISTER`, `LANGUAGE_FORM`, and `AI_STEREOTYPE`. **Substantive/practical** includes `TECHNICAL_SUBSTANCE`, `CONTEXT_SENSITIVITY`, `EPISTEMIC_STYLE`, `EXPERIENTIAL_TACIT`, and `SOCIAL_MEMBERSHIP`.

## Limitations

1. No human participants were recruited; LLM evaluators may not use the cues human Judges use.
2. The technical questions tested articulated knowledge, not embodied or personal experience.
3. One non-native-English researcher wrote all anchors, which may itself create language-form cues.
4. One coder completed all 64 justifications; there is no independent inter-rater reliability estimate.
5. The sample is small and reuses eight questions across cells; inferential results are exploratory.
6. Style control changed both surface form and content, while order effects and stochastic variation were not separated.

## Next study

A participant study would recruit Judges and Non-Pretenders from one clearly defined social world, allow participants to formulate questions as proxy researchers, and collect confidence, justification, and reflection. It would undergo formal ethical review, use an independent second coder, include experiential questions, and test style controls that do not force content loss.

## Reproduce and inspect

No-API reproduction:

```bash
python3 scripts/reproduce_statistics.py
```

Full execution instructions are in [`RUNNING.md`](RUNNING.md).

Key files:

- [`research_brief.md`](research_brief.md) — one-page research summary
- [`ANALYSIS.md`](ANALYSIS.md) — full interpretation and claim boundaries
- [`codebook_v1_2.md`](codebook_v1_2.md) — final coding manual
- [`results/COMIG_blind_justification_coding.xlsx`](results/COMIG_blind_justification_coding.xlsx) — coded data (label-masked, not fully blind)
- [`DATA_AND_REPRODUCIBILITY.md`](DATA_AND_REPRODUCIBILITY.md) — data and provenance map

## Freeze record

- Pre-generation freeze: `d4cb1f395d562d463c020b2593f17957ce7fab8a`
- Pre-Q0 tool freeze: `6747f20d0f2710550f3f0ba0c19f1307a9d25b7b`

These commits are retained in the development repository history and full-history bundle.

## Reference

Segersven, O., & Mannila, L. (2025). Introducing the Competence Imitation Game: A Research and Teaching Tool for Context-Specific AI Literacy. In *AISEER'25: 2nd International Workshop on AI in Society, Education and Educational Research*, CEUR Workshop Proceedings, Vol. 4138. https://ceur-ws.org/Vol-4138/paper3.pdf
