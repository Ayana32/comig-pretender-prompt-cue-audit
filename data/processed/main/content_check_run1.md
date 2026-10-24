# Content-Preservation Check — Designated Run 1

Use the frozen definitions and allowed values in `content_check.md`. Do not regenerate confounded cases.

## Q1

**Question:** You observe high cross-lingual representational similarity between English and a target language, but an intervention transfers inconsistently at the behavioural level. How would you interpret this result, and what would you test next?

### Naive, run 1

This is a very interesting and somewhat common observation in multilingual language model analysis. High cross-lingual representational similarity (e.g., as measured by CKA, SVCCA, or centered kernel alignment metrics between English and the target language) suggests that the model encodes similar information or features for the two languages at the representational level. However, inconsistent behavioral transfer (e.g., in downstream task performance or zero-shot/few-shot evaluation) indicates that this similarity does not straightforwardly translate to functional equivalence or reliable transfer of knowledge.

### Interpretation

1. **Representational similarity ≠ functional equivalence:**  
   High similarity in intermediate or final layer embeddings might reflect shared low-level syntactic or lexical patterns but may not capture deeper semantic or task-relevant distinctions necessary for behavioral consistency. The model might still be using language-specific heuristics or have language-specific biases that affect task performance.

2. **Task-specific vs. general representations:**  
   The shared representation may encode language-general features (e.g., morphology, syntax) but the task demands (e.g., sentiment, NLI) might rely on language-specific phenomena or cultural context that are not well aligned or captured by the model.

3. **Data distribution and annotation differences:**  
   Inconsistent behavioral transfer could arise if training data for the target language diverges in style, domain, or annotation guidelines from English data, causing the model to fail in generalizing despite similar representations.

4. **Intervention granularity and localization:**  
   The intervention (e.g., fine-tuning, prompt engineering, or model surgery) might affect only parts of the model or certain layers, while the behavioral task depends on other components or cross-layer interactions. Thus, representational similarity at one layer might not reflect the full pipeline of processing relevant for behavior.

### What to test next?

1. **Layer-wise and component-wise analysis:**  
   - Check representational similarity across multiple layers, especially those implicated in task-specific behaviors.  
   - Analyze whether the intervention changes representations in the same way for both languages at different layers.

2. **Probing task-relevant features:**  
   - Use diagnostic classifiers or probing tasks to test whether task-relevant linguistic properties (e.g., semantic roles, negation, discourse relations) are similarly encoded across languages.  
   - This can reveal which linguistic phenomena are causing inconsistent transfer.

3. **Behavioral consistency at finer granularity:**  
   - Evaluate behavioral transfer at the level of specific phenomena or linguistic constructions rather than aggregate task metrics.  
   - For example, analyze errors or performance differences on subsets of data that are linguistically or culturally distinctive.

4. **Intervention localization and ablation studies:**  
   - Test whether interventions targeted at different layers or modules produce more consistent transfer.  
   - Perform ablations to see if certain parts of the model contribute disproportionately to inconsistent behavior.

5. **Cross-lingual alignment methods:**  
   - Experiment with explicit alignment techniques (e.g., canonical correlation analysis, mapping-based methods) to improve functional alignment beyond representational similarity.  
   - Evaluate if forcing alignment at the task-head or output layer improves behavioral consistency.

6. **Data and annotation checks:**  
   - Inspect the training and evaluation data for domain mismatch, annotation inconsistency, or cultural bias.  
   - Consider augmenting or re-annotating data to reduce noise or divergence.

### Summary

High representational similarity is a useful but incomplete signal of cross-lingual transferability. The gap with inconsistent behavioral transfer suggests a mismatch between representational overlap and task-relevant functional equivalence. Careful layer-wise analysis, probing, and targeted interventions should be used to pinpoint the source of inconsistency and improve transfer robustness.

---

If you want, I can also recommend specific papers or tools commonly used for these analyses.

### Style-controlled, run 1

High cross-lingual similarity suggests shared representations, but inconsistent behavioral transfer indicates the model might not fully capture task-specific nuances or language-specific features. I'd next probe task alignment, fine-tune on the target language, and analyze error patterns to pinpoint representational gaps affecting performance.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q2

**Question:** You are evaluating an LLM on a benchmark translated from English into several languages. What would make you question whether performance differences reflect model capability rather than translation or dataset artifacts?

### Naive, run 1

As a postgraduate researcher with practical experience in multilingual LLM evaluation, when I see performance differences across languages on a benchmark that’s been translated from English, I would question whether those differences genuinely reflect the model’s multilingual capability or are instead artifacts of the translation or dataset construction process. Several factors would raise red flags:

1. **Quality and Consistency of the Translation**  
   - **Literal vs. natural translation:** If the translations are too literal or awkward, they may not reflect natural usage in the target language, leading to unnatural input distributions that the model struggles with.  
   - **Translator expertise and guidelines:** Inconsistent quality, or translations done by non-experts or via machine translation without careful post-editing, can introduce noise or errors that hurt performance.  
   - **Cultural and pragmatic mismatches:** Some content may not translate well due to cultural references, idiomatic expressions, or pragmatics that don’t carry over, causing the benchmark to test something other than pure language understanding.

2. **Dataset Artifacts Introduced During Translation**  
   - **Changes in lexical difficulty or ambiguity:** The translated benchmark might differ in lexical difficulty, ambiguity, or syntactic complexity, confounding direct performance comparison.  
   - **Altered label distributions:** For example, if classification labels depend on lexical cues or culturally specific knowledge that changes in translation, the task difficulty or label balance might shift.  
   - **Unintended hints or artifacts:** The translation process might inadvertently introduce artifacts (e.g., token patterns or frequent phrases) that models exploit differently across languages.

3. **Alignment of Task Semantics and Formats**  
   - **Task format consistency:** The prompt or input format might not align perfectly across languages, especially for tasks requiring nuanced instructions or output formats.  
   - **Semantic equivalence of questions and answers:** Some questions may become ambiguous or lose nuance in translation, making the task easier or harder in certain languages.

4. **Model Tokenization and Vocabulary Coverage**  
   - **Differences in subword tokenization efficiency:** The model’s tokenizer might segment input differently in each language, affecting input length and representation quality independently of underlying model capability.  
   - **Out-of-vocabulary or rare tokens:** Translations might introduce more rare or unseen tokens, disproportionately impacting performance.

5. **Baseline and Human Performance Comparisons**  
   - **Human baseline variability:** If human performance on the translated benchmark differs significantly from English, this suggests the translation or task formulation affects difficulty.  
   - **Cross-lingual transfer baselines:** Comparing zero-shot vs. fine-tuned performance can help isolate whether lower performance reflects model limitations or dataset issues.

---

**In sum, I would be cautious about interpreting raw performance differences as purely reflecting model multilingual ability unless the translation and dataset artifacts are carefully controlled for. This typically involves:**

- Validating translation quality with native speakers.  
- Ensuring semantic and pragmatic equivalence of benchmark items.  
- Analyzing lexical and syntactic complexity across languages.  
- Checking for dataset artifacts or label distribution shifts.  
- Using complementary evaluation methods like human baselines and probing.  

Only with such rigor can we credibly attribute performance differences to model capability rather than extrinsic artifacts introduced by translation or dataset design.

### Style-controlled, run 1

I’d be suspicious if performance differences align closely with translation quality issues, like mistranslations or unnatural phrasing, or if the dataset’s cultural references don’t transfer well. Also, inconsistent annotation or tokenization quirks across languages could skew results away from true model ability.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q3

**Question:** A multilingual model performs substantially worse in a low-resource language. How would you investigate whether tokenization is a major cause rather than merely a correlated explanation?

### Naive, run 1

Great question. When a multilingual model underperforms on a low-resource language, tokenization is a common suspect but disentangling it from correlated factors (e.g., data scarcity, domain mismatch) requires a careful experimental approach. Here's how I would investigate whether tokenization is a major causal factor rather than just correlated:

---

### 1. **Analyze the Tokenizer's Coverage and Granularity**

- **Vocabulary overlap:** Check how many tokens from the low-resource language are covered by the tokenizer’s vocabulary. A tokenizer trained primarily on high-resource languages may have poor coverage or produce overly fragmented tokens.
- **Token length statistics:** Compute average token lengths and number of tokens per sentence compared to high-resource languages. Excessive fragmentation (many subword units per word) often signals suboptimal tokenization.
- **Rare token frequency:** Identify how often rare or unknown tokens appear. High frequency suggests poor tokenization.

---

### 2. **Ablation Study with Alternative Tokenizations**

- **Use language-specific tokenizers:** Replace the original tokenizer with a tokenizer optimized or trained specifically for the low-resource language (e.g., a dedicated SentencePiece or BPE model trained on only that language).
- **Use character-level or byte-level tokenization:** These tokenizers avoid vocabulary issues and can serve as a baseline to see if avoiding subword fragmentation helps.
- **Evaluate model performance with these tokenizers:** If performance improves significantly with a better or alternative tokenizer, that strongly implicates tokenization as a cause.

---

### 3. **Control for Other Factors**

- **Keep training data fixed:** Ensure the training corpus size and quality remain constant when changing tokenizers to isolate the effect.
- **Control for model size and architecture:** Use the same model architecture so improvements are not due to model capacity changes.

---

### 4. **Error Analysis and Qualitative Inspection**

- Look for failure modes related to tokenization, such as:
  - Errors on morphologically rich words that are split incorrectly.
  - Misalignment between tokens and linguistic units (e.g., morphemes or phonemes).
- Compare model outputs with different tokenizers on the same inputs.

---

### 5. **Correlation vs. Causation via Probing**

- Train a smaller diagnostic classifier or probe on tokenized inputs to predict linguistic properties (e.g., POS tags, morphological features).
- If tokenization quality correlates with downstream task performance and linguistic probing accuracy, it supports causality.

---

### Summary

If changing the tokenizer to a more appropriate or finer-grained one for the low-resource language leads to a clear and consistent improvement in evaluation metrics, while controlling for other variables, this is strong evidence that tokenization was a major cause of poor performance rather than merely correlated with it.

---

**In practice, I’d start by comparing the original tokenizer’s tokenization statistics and vocabulary coverage for the low-resource language, then run controlled experiments swapping tokenizers, ideally keeping training data and model architecture fixed.** This approach is common in recent multilingual NLP research (e.g., studies on mBERT, XLM-R, and language-specific adaptations) to diagnose tokenization bottlenecks.

### Style-controlled, run 1

I’d compare tokenization quality by inspecting token overlap and segmentation consistency between high- and low-resource languages, then run controlled experiments swapping tokenizers or using character-level inputs. If performance shifts significantly, it indicates tokenization is a key factor, not just correlated.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q4

**Question:** You need to evaluate open-ended responses from a multilingual LLM, but there is no single correct reference answer. How would you choose an evaluation method, and what limitations would you report?

### Naive, run 1

Given the scenario of evaluating open-ended responses from a multilingual LLM without a single correct reference answer, here is how I would approach the evaluation and the limitations I would report, drawing on current best practices and recent research insights in multilingual NLP:

---

### Choosing an Evaluation Method

1. **Use of Reference-Free (or Minimal-Reference) Metrics:**
   Since no single correct reference exists, traditional reference-based metrics like BLEU or ROUGE are ill-suited. Instead, I would prioritize:
   - **Semantic similarity metrics** such as BERTScore, or multilingual embeddings-based similarity (e.g., LASER, LaBSE) that assess semantic overlap without requiring exact matches.
   - **Learned evaluation models** like COMET or BLEURT that can be fine-tuned or adapted for multilingual settings and can judge quality beyond surface form overlap.

2. **Human Evaluation with Well-Defined Criteria:**
   - Design human evaluation protocols that assess aspects like **fluency**, **relevance**, **coherence**, and **informativeness**.
   - Use multilingual annotators or experts proficient in the target languages to ensure cultural and linguistic appropriateness.
   - Employ pairwise comparison or direct assessment to reduce annotator bias.

3. **Task-Specific Probing or Downstream Evaluation:**
   - If the open-ended responses are meant for a specific task (e.g., summarization, question answering), evaluate performance indirectly via downstream task metrics.
   - Alternatively, use **interactive or extrinsic evaluations**, such as user satisfaction or success rate in completing a task.

4. **Diversity and Robustness Metrics:**
   - Evaluate the diversity of outputs to ensure the model does not produce generic or templated answers.
   - Assess robustness across languages and dialects, potentially through stress tests or adversarial examples.

---

### Limitations to Report

1. **Subjectivity and Variability in Human Judgments:**
   - Human evaluation can be subjective and inconsistent, especially across languages and cultural contexts.
   - Inter-annotator agreement may be low, requiring careful training and calibration of annotators.

2. **Limitations of Semantic Similarity Metrics:**
   - Embedding-based metrics may fail to capture subtle nuances, pragmatics, or culturally specific meanings.
   - These metrics might be biased towards high-resource languages or domains seen during pretraining.

3. **Lack of Ground Truth:**
   - Without reference answers, it is difficult to conclusively determine correctness or completeness.
   - Evaluation can only approximate quality, not guarantee it.

4. **Language and Domain Coverage:**
   - Performance and evaluation quality may vary significantly across languages, especially low-resource or morphologically rich languages.
   - Domain mismatch can further degrade evaluation reliability.

5. **Potential for Overfitting to Evaluation Metrics:**
   - Models may be optimized for specific metrics rather than genuine understanding or quality, especially if metrics are not carefully chosen.

---

### Summary

In sum, I would combine reference-free semantic similarity metrics with carefully designed human evaluation protocols, ideally complemented by downstream or task-specific metrics. I would transparently report the subjective nature of evaluation, metric biases, and the challenge posed by multilingual variability. This multifaceted approach reflects current consensus in the community that no single metric suffices for open-ended multilingual LLM evaluation, and that human judgment remains essential despite its limitations.

### Style-controlled, run 1

I’d lean on human evaluation focusing on relevance, coherence, and cultural appropriateness, supplemented by diversity metrics to capture response variability. Automated metrics like BLEU or ROUGE fall short without references. Limitations include subjectivity, annotator bias, and scalability challenges.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q5

**Question:** Your results change noticeably across model families, layers, prompts or random seeds. How would you decide whether you have found a meaningful effect or an unstable experimental artifact?

### Naive, run 1

This is a very common and important concern in multilingual language-model evaluation, especially given the variability introduced by different model architectures, layers, prompts, and random seeds. To decide whether observed differences constitute a meaningful effect or just unstable artifacts, I would proceed along several complementary lines:

1. **Statistical significance and effect size:**  
   First, I would run multiple evaluation runs varying seeds and prompts systematically to quantify variability. Using standard statistical tests (e.g., paired bootstrap tests) and confidence intervals helps assess whether differences are statistically significant beyond noise levels. Effect sizes and confidence intervals give more nuance than p-values alone.

2. **Consistency across independent runs:**  
   If the effect is robust, it should replicate reliably across independent runs (different seeds) and different prompt formulations. If the effect flips signs or disappears under minor perturbations, it’s likely an artifact.

3. **Cross-model-family comparison:**  
   If a phenomenon is observed in one model family but not in others, it could be either a model-specific effect or noise. To argue for meaningfulness, I would look for consistent trends across related model architectures or training regimens.

4. **Layer-wise pattern analysis:**  
   Layerwise effects can be subtle but informative. Genuine effects often show smooth or interpretable patterns across adjacent layers (e.g., monotonic trends or identifiable representational changes). Random noise or artifacts tend to be erratic and lack clear structure.

5. **Control experiments and baselines:**  
   Introducing control conditions, such as randomizing input tokens, using meaningless prompts, or evaluating on unrelated languages/tasks, helps verify that the observed effects are not due to confounds or chance.

6. **Theoretical grounding and prior work:**  
   I would cross-check whether similar effects have been documented in prior literature or align with known linguistic or model-theoretic intuitions. Novel findings require stronger evidence, but if they fit into an existing explanatory framework, that supports their validity.

7. **Signal-to-noise ratio and measurement reliability:**  
   Evaluations on small datasets or unstable metrics can produce spurious effects. Ensuring adequate sample sizes and using robust metrics (e.g., aggregated over many sentences) improves reliability.

8. **Qualitative analysis:**  
   Sometimes, a close qualitative inspection of failure cases or model outputs can reveal whether differences reflect meaningful linguistic or representational changes, or just random fluctuations.

---

**Summary:**  
I would characterize effects as meaningful if they are statistically significant, reproducible across seeds and prompts, consistent across related model families or layers, supported by controls, and theoretically plausible. If effects are fragile, inconsistent, or lack clear patterns, I would treat them as unstable artifacts and interpret cautiously, possibly designing further experiments to resolve ambiguity.

### Style-controlled, run 1

I’d first check if the effect consistently appears across multiple seeds and closely related models, ensuring it’s not just noise. Then, I’d validate with different prompts or tasks to see if the pattern holds, indicating a meaningful signal rather than a random artifact.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q6

**Question:** You inherit a multilingual LLM experiment repository whose reported results you cannot reproduce. What would you inspect first, and how would you determine where the discrepancy comes from?

### Naive, run 1

Given the scenario of inheriting a multilingual LLM experiment repository with irreproducible reported results, here is how I would approach the investigation, grounded in practical experience from multilingual NLP and LLM evaluation:

---

### 1. **Check the Experimental Setup and Environment**

- **Dependencies and Versions:**  
  Confirm that the exact versions of the codebase, frameworks (e.g., PyTorch, TensorFlow), tokenizers (e.g., HuggingFace tokenizers), and dependencies are installed. Differences in library versions can cause small but critical changes in model behavior and tokenization.

- **Hardware and Random Seeds:**  
  Verify the hardware setup (GPUs/TPUs, memory constraints) and ensure that the random seeds for initialization, data shuffling, and any sampling processes are set and fixed as in the original experiments. Even subtle differences here can lead to non-deterministic outcomes.

---

### 2. **Validate the Data Processing Pipeline**

- **Data Versions and Preprocessing:**  
  Check that the dataset versions used for training and evaluation match exactly. Multilingual datasets often have multiple releases or subsets (e.g., FLORES, XTREME). Also, inspect the data preprocessing scripts for tokenization, normalization, and filtering steps, ensuring they are identical.

- **Language Tags and Tokenization:**  
  Especially for multilingual models, language ID tokens or special prefixes are critical. Confirm that these are correctly applied and consistent with the original setup.

---

### 3. **Review Model Checkpoints and Loading**

- **Checkpoint Integrity:**  
  Confirm that the model checkpoints used are the exact ones reported. Sometimes, the repository may point to a different checkpoint or a fine-tuned variant. Check the hash or metadata of the checkpoint files.

- **Model Configuration:**  
  Make sure the model architecture and hyperparameters (e.g., layer sizes, number of attention heads) match those used to generate the results. Misalignment here can cause drastic differences.

---

### 4. **Re-execute Evaluation Code with Verbose Logging**

- **Intermediate Outputs:**  
  Run the evaluation scripts with verbose or debug logging to inspect intermediate outputs such as tokenized inputs, model logits, and final predictions. This can highlight where the results start diverging.

- **Metric Calculation:**  
  Verify that the evaluation metrics (e.g., BLEU, chrF, accuracy) are computed exactly as in the original paper or report, including any post-processing (e.g., detokenization). Differences in metric computation can cause apparent irreproducibility.

---

### 5. **Cross-Check with External Baselines or Prior Runs**

- **Baseline Consistency:**  
  If the repository includes baseline models or previously published results, check if those can be reproduced. This helps determine if the discrepancy is systemic or specific to certain models or languages.

- **Compare Against Published Benchmarks:**  
  Run the model on established multilingual benchmarks (FLORES, XTREME, etc.) and compare with published numbers to isolate if the discrepancy is in the data, model, or evaluation.

---

### 6. **Consult Documentation and Communicate**

- **Check for Updates or Known Issues:**  
  Review any documentation, issue trackers, or community discussions related to the repository. Sometimes, subtle bugs or environment issues are documented post-publication.

- **Contact Original Authors if Possible:**  
  If the discrepancy remains unresolved, reaching out to the original authors for clarifications or unpublished details can be invaluable.

---

### Summary:

**The first and most critical step is to verify the exact experimental environment (code, dependencies, seeds), data versions, and model checkpoints.** From there, systematically inspect the data processing, model loading, and evaluation metric implementations while logging intermediate outputs to pinpoint where results diverge.

This approach is essential in multilingual LLM evaluation because small differences in tokenization, language tags, or data versions can disproportionately affect multilingual performance, leading to irreproducibility.

---

If you want, I can share a checklist or scripts I use for systematically validating multilingual LLM experiments.

### Style-controlled, run 1

I’d start by verifying the exact model checkpoints, tokenizers, and preprocessing scripts to ensure alignment with the original setup. Then, I’d check the evaluation metrics and data splits used, since subtle differences there often cause discrepancies in multilingual benchmarks.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q7

**Question:** A reviewer argues that your experiment shows only a correlation between an internal representation and model behaviour, not a causal relationship. How would you respond or redesign the experiment?

### Naive, run 1

Thanks for the insightful comment. I agree that demonstrating correlation between an internal representation and model behavior is not sufficient to establish causality. To address this, I would consider the following steps:

1. **Intervention-based probing**: Instead of just measuring correlations between representations and outputs, introduce controlled interventions on the internal representation. For example, use techniques like causal mediation analysis or intervention-based probing (e.g., ablation, representation editing, or counterfactual modification) to directly manipulate the representation and observe changes in downstream behavior. This can help establish whether the representation is causally necessary or sufficient for the behavior.

2. **Causal mediation analysis**: Following recent work (e.g., Vig et al. 2020, Geiger et al. 2021), I might frame the problem as a mediation analysis where the internal representation is a mediator between the input and output. By intervening on the mediator and measuring the effect on output, one can assess causal influence.

3. **Ablation or lesion studies**: Remove or perturb specific components or neurons corresponding to the internal representation and check if the model’s behavior deteriorates in a manner consistent with the hypothesized causal role.

4. **Counterfactual generation**: Generate counterfactual internal states where the representation is altered while keeping other factors fixed, then measure how the model’s output changes. This can be done via techniques like vector arithmetic or gradient-based modifications in the representation space.

5. **Redesigning the experiment**: Incorporate a controlled manipulation step. For example, if the internal representation encodes language identity or syntactic features, selectively modify it and observe whether the model’s multilingual predictions shift accordingly.

In sum, to move beyond correlation, the experiment must include *interventions* on the internal representations and measure their *causal effect* on behavior. This is aligned with the current best practices in interpretability and causal analysis within NLP models. I would revise the experimental design to include such interventions and report causal metrics accordingly.

### Style-controlled, run 1

I’d acknowledge the reviewer’s point and clarify that correlation is a first step. To probe causality, I’d propose interventions like targeted ablation or counterfactual generation on the representation, then measure corresponding changes in model behavior to establish a more direct causal link.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |

## Q8

**Question:** One language produces a result in the opposite direction from the others, even though the implementation checks pass. How would you investigate and report that result? 

### Naive, run 1

When encountering a language that produces results in the opposite direction from others in a multilingual LM evaluation—despite passing implementation checks—I'd approach it systematically as follows:

**1. Re-examine Data and Preprocessing**  
- **Data quality and representativeness:** Confirm that the test data for this language is comparable in domain, difficulty, and annotation quality to the other languages. Differences here can skew results.  
- **Tokenization and normalization:** Check if the tokenization or text normalization pipeline for this language differs substantially and might affect model inputs or outputs differently. For instance, segmentation errors, script issues, or casing.  
- **Alignment of evaluation metrics:** Ensure that the evaluation metric is applied consistently across languages, especially for metrics sensitive to language morphology (e.g., BLEU, perplexity, accuracy).

**2. Verify Model and Evaluation Code Behavior for This Language**  
- **Language-specific model behavior:** Look at the model’s outputs and intermediate representations (e.g., logits, embeddings) for this language to detect any anomalies or unexpected patterns.  
- **Edge cases or language-specific bugs:** Even if implementation checks pass, subtle bugs might appear only under certain linguistic conditions. For example, mis-handling of right-to-left scripts, token ID mismatches, or fallback behavior.  
- **Random seeds and variability:** Run multiple evaluation seeds to rule out chance or variance-driven artifacts.

**3. Compare Linguistic and Resource Factors**  
- **Model training data distribution:** Confirm the extent and quality of training data for the language. Sparse or noisy training data can cause models to behave differently.  
- **Morphological complexity and typology:** Some metrics or models may perform differently on agglutinative or polysynthetic languages, or on languages with freer word order. This could invert expected correlations.  
- **Script and orthography:** Scripts with ambiguous segmentation or homographs might confuse the model or metric.

**4. Perform Ablation and Controlled Experiments**  
- **Cross-lingual transfer tests:** Evaluate the model’s zero-shot or few-shot performance on this language versus others to isolate if the issue is model capacity or data.  
- **Metric sanity checks:** Try alternative metrics or human evaluation to verify if the observed direction is a true signal or an artifact of metric sensitivity.  
- **Input perturbation:** Modify inputs slightly to see if the model’s response changes logically.

**5. Document and Report Clearly**  
- **Detailed description:** Clearly describe the anomaly, the languages involved, and the evaluation setup.  
- **Hypotheses and tests:** Outline all hypotheses tested, the experiments run, and their outcomes.  
- **Implications:** Discuss what this means for cross-lingual evaluation reliability and model generalization.  
- **Recommendations:** Suggest next steps, such as collecting more data, refining metrics, or developing language-specific handling.

---

**In summary:** an anomalous result in one language demands careful linguistic, data, and technical scrutiny beyond standard implementation checks. Multilingual evaluation is complex due to language-specific idiosyncrasies in data, models, and metrics. Transparent investigation and reporting not only help debug but also deepen understanding of multilingual model behavior.

### Style-controlled, run 1

I’d first verify data preprocessing and tokenization for that language to rule out subtle issues, then double-check evaluation metric alignment and model outputs. Comparing intermediate results with other languages helps isolate anomalies. When reporting, I’d detail these steps, highlight potential linguistic or data idiosyncrasies, and suggest cautious interpretation.

| Field | Entry |
|---|---|

| `CORE_CLAIM_PRESERVED` |  |

| `TECHNICAL_ERROR_DIFFERENCE` |  |

| `IMPORTANT_CONTENT_OMISSION` |  |

| `ADDITIONAL_CLAIM` |  |

| `OVERALL_COMPARABILITY` |  |

| `evidence_note` |  |
