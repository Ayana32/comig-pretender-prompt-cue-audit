# Frozen Human Anchors v1

The nine anchors were authored directly by the researcher without AI rewriting. Three pre-freeze author corrections were applied: `necessary` to `sufficient` in Q1, `multilingual bias` to `absolute scoring instability` in Q4, and deletion of the accidentally duplicated phrase `answer and` in Q7. No further stylistic, grammatical, or substantive editing was applied.

## Q0 — Dry run only

> I would report their dataset sizes for each language to show the limitation of this evaluation. Also, the way to calculate their estimates should be reported. Furthermore, I have to claim that this result is not confirmed for these reasons.

Word count: 40  
Status: Frozen; excluded from main analysis.

## Q1

> We could claim that representational similarity isn't sufficient for the behavioural effect. First, we should review how we observe these representational similarities. If we use just one method or the wrong way, it means we need more experiments. Second, we could examine the causal mechanism to identify it.

Word count: 48  
Status: Frozen after author terminology correction.

## Q2

> There are many cues, but I would like to pick three. First, when we did back-translation and the results differed significantly, that was the cue. Second, if there are some lexical cues in the translated ones, that was the cue. Last but not least, Large ranking shifts can be the cue for high translation sensitivity.

Word count: 55  
Status: Frozen.

## Q3

> First, I would measure the token fertility or sequence length. Because, in general, low-resource languages have more tokens. Then, test whether reducing fertility through a language-specific tokeniser can improve performance under the controlled setting.

Word count: 34  
Status: Frozen.

## Q4

> I would combine human evaluation and LLM-as-a-judge. One of the main limitations is the lack of gold standards. To reduce absolute scoring instability, I would choose pairwise comparison, but with a position-bias test too.

Word count: 34  
Status: Frozen after author terminology correction.

## Q5

> I would examine the effect size and confidence interval together. Furthermore, replicating the experiments across models, layers, prompts, or random seeds is essential to claim robust results.

Word count: 27  
Status: Frozen.

## Q6

> First, I would identify which parts of the experiment are reproducible and which are not, and document why the non-reproducible parts cannot be reproduced. Then, I would trace the pipeline step by step and record intermediate outputs at each stage to localise where the discrepancy comes from.

Word count: 47  
Status: Frozen.

## Q7

> I would answer by limiting my claims to the correlational evidence supported by the current results. Then, I would redesign activation patching, ablation, or counterfactual interventions to test whether manipulating the representation causally changes model behaviour.

Word count: 36  
Status: Frozen after author deletion of an accidental duplicated phrase.

## Q8

> I would systematically investigate potential sources of the anomalous result, such as data quality, translation, tokenisation, baseline choice, and model behaviour. I would formulate hypotheses for each factor and test them one by one, eliminating possible explanations until I identify the source of the discrepancy.

Word count: 45  
Status: Frozen.

## Main-set length calculation

Q1–Q8 total: 326 words  
Q1–Q8 mean: 40.75 words  
Style target: approximately 41 words  
Counting convention: whitespace-separated words; hyphenated expressions and contractions count as one word.

