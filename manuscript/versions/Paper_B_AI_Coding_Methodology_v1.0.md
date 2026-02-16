<!--
===============================================================================
MANUSCRIPT STATUS: DRAFT SCAFFOLD — Data collection in progress
===============================================================================

This manuscript is structured as a complete scaffold awaiting empirical results.
Sections marked [PLACEHOLDER] will be populated after data collection.
All methodological decisions are finalized.

TARGET JOURNAL: TBD (candidates: JASIST, Systematic Reviews, Research Synthesis
Methods, Journal of Educational Psychology)

===============================================================================
-->

# LLM-Assisted Coding for Systematic Reviews: A Three-Model Comparative Framework Applied to Educational Meta-Analysis

**Hosung You**

College of Education, Pennsylvania State University

**Version: 1.0 (Scaffold)**

---

**Author Note**

Hosung You https://orcid.org/[ORCID-ID]

Correspondence concerning this article should be addressed to Hosung You, College of Education, Pennsylvania State University, University Park, PA 16802. Email: hosung@psu.edu

Data Availability Statement: The complete dataset, AI prompts, extraction logs, and analysis code are available at [OSF Repository Link].

Conflict of Interest: The author declares no conflicts of interest.

Funding: This research received no external funding.

---

## Abstract

The exponential growth of empirical research necessitates scalable approaches to systematic review data extraction, yet the reliability of large language models (LLMs) for this task remains inadequately characterized. This study presents a comprehensive evaluation of three frontier LLMs — Claude (Anthropic), GPT-4o (OpenAI), and Gemini (Google) — for meta-analysis coding, benchmarked against a human gold standard dataset from an independent meta-analysis of generative AI in higher education (*k* = [PLACEHOLDER] studies, *n* = [PLACEHOLDER] effect sizes). Each LLM independently extracted [PLACEHOLDER] variables per study across study characteristics, effect size data, and outcome classifications. We assessed (a) field-level accuracy using exact match, within-threshold agreement, and error classification; (b) inter-method reliability via Cohen's kappa (categorical) and intraclass correlation coefficients (continuous); (c) multi-model consensus performance against single-model extraction; and (d) cost-time efficiency relative to human coding. Results revealed [PLACEHOLDER: summary of key findings]. A multi-model consensus approach, where the final value is accepted only when at least two of three models agree, [PLACEHOLDER: outperformed/matched] single-model extraction for [PLACEHOLDER: which variable types]. We propose a practical human-AI hybrid workflow that [PLACEHOLDER: key recommendation]. This study contributes a reproducible evaluation framework, a publicly available prompt library, and evidence-based recommendations for integrating LLMs into systematic review pipelines.

*Keywords:* large language models, systematic review automation, meta-analysis coding, data extraction, inter-rater reliability, human-AI collaboration, GPT-4o, Claude, Gemini, research synthesis methodology

---

## Introduction

### The Data Extraction Bottleneck in Systematic Reviews

Systematic reviews and meta-analyses represent the highest level of evidence in evidence-based practice (Higgins et al., 2023). However, the data extraction phase — where reviewers manually extract study characteristics, statistical values, and outcome classifications from primary studies — remains one of the most labor-intensive, error-prone, and rate-limiting steps in the review process (Buscemi et al., 2006; Jones et al., 2005). A single meta-analysis may require hundreds of hours of human coding effort, with dual coding for reliability assessment effectively doubling the workload (Pigott & Polanin, 2020).

The challenge is compounded by the accelerating pace of empirical research. In rapidly evolving fields such as educational technology, the volume of eligible studies can increase substantially between protocol registration and manuscript submission, creating a tension between comprehensiveness and timeliness (Tsafnat et al., 2014). This bottleneck has motivated decades of work on systematic review automation, with efforts ranging from machine-learning-assisted screening (O'Mara-Eves et al., 2015; Marshall & Wallace, 2019) to natural language processing for data extraction (Jonnalagadda et al., 2015).

### Large Language Models as a Potential Solution

The emergence of frontier large language models (LLMs) — including GPT-4o (OpenAI, 2024), Claude (Anthropic, 2024), and Gemini (Google, 2024) — has introduced a qualitatively different approach to automated data extraction. Unlike earlier NLP systems that required task-specific training data and feature engineering, LLMs can process complex academic text through natural language instructions (prompts), potentially extracting structured data without domain-specific fine-tuning (Brown et al., 2020; Wei et al., 2022).

Early evidence suggests promising but inconsistent performance. Guo et al. (2024) found that GPT-4 achieved moderate accuracy for extracting PICO elements from clinical trial abstracts, but performance varied substantially across element types. Khraisha et al. (2024) demonstrated that LLMs could assist with various stages of systematic reviews but noted significant limitations in numerical data extraction. Wang et al. (2024) evaluated ChatGPT for screening and data extraction in medical systematic reviews, reporting high sensitivity but variable specificity across different data types.

However, the existing literature has critical gaps. First, most evaluations have examined a single LLM, making cross-model comparisons impossible. Second, evaluations have focused predominantly on clinical/medical systematic reviews, with limited evidence from social science and education domains where coding schemas are often more complex and subjective. Third, few studies have examined the full range of meta-analysis coding variables — from straightforward bibliographic data to complex statistical extractions and subjective outcome classifications. Fourth, the potential of multi-model consensus approaches remains unexplored.

### The Present Study

This study addresses these gaps through a comprehensive evaluation of three frontier LLMs for meta-analysis data extraction, using a human gold standard dataset from an independently conducted meta-analysis of generative AI effectiveness in higher education (You, 2026). The gold standard dataset provides an ideal benchmark because it includes: (a) a large and diverse set of primary studies (*k* = [PLACEHOLDER]); (b) multi-dimensional coding spanning bibliographic, methodological, statistical, and classificatory variables; (c) rigorous dual-coding with established inter-rater reliability; and (d) consensus-resolved final values verified against source documents.

We address four research questions:

**RQ1.** How accurately can frontier LLMs (Claude, GPT-4o, Gemini) extract meta-analysis coding data compared to the human gold standard?

**RQ2.** For which variable types (bibliographic, methodological, statistical, classificatory) do LLMs show the highest and lowest agreement with human coders?

**RQ3.** Does a multi-model consensus approach (requiring agreement from at least two of three models) improve extraction accuracy compared to any single model?

**RQ4.** What is the optimal human-AI hybrid workflow that maximizes both efficiency (time, cost) and accuracy for systematic review data extraction?

### Contribution

This study makes three contributions to the research synthesis methodology literature. First, we provide the first head-to-head comparison of three frontier LLMs on the same meta-analysis coding task, enabling direct cross-model evaluation. Second, we introduce and evaluate a multi-model consensus approach that leverages model diversity to improve reliability. Third, we propose an evidence-based human-AI hybrid workflow with concrete decision rules for when AI extraction is sufficient versus when human verification is required, along with a publicly available prompt library for replication.

---

## Method

### Study Design Overview

This methodological study employed a comparative accuracy design. Three LLMs independently extracted coding data from the same set of primary studies, and their outputs were evaluated against a pre-established human gold standard. The design is analogous to comparing a new diagnostic test against a reference standard in clinical research (Bossuyt et al., 2015).

### The Human Gold Standard

#### Source Dataset

The gold standard was derived from a three-level meta-analysis examining the effectiveness of generative AI interventions on learning outcomes in higher education (You, 2026; hereafter "the parent meta-analysis"). The parent meta-analysis is reported separately as an independent substantive contribution (Paper A) and does not reference AI-assisted coding.

The dataset includes *k* = [PLACEHOLDER] primary studies with *n* = [PLACEHOLDER] effect sizes extracted from [PLACEHOLDER] participants. Studies were published between November 2022 and February 2026 and were identified through systematic searches of seven databases (PsycINFO, ERIC, Education Source, ProQuest, Semantic Scholar, OpenAlex, Web of Science).

#### Human Coding Protocol

Two trained coders (the first author [faculty] and a postdoctoral researcher with experience in educational research methodology) independently coded all included studies following a detailed coding manual (You, 2026; available at [OSF Repository Link]). The coding protocol specified:

1. **Training phase**: Both coders completed a structured training program using 10 pilot studies. After each pilot batch (5 studies), inter-rater reliability was assessed, discrepancies discussed, and coding rules refined. Training continued until Cohen's kappa exceeded 0.70 for all categorical variables and ICC exceeded 0.75 for continuous variables.

2. **Independent coding**: Each coder independently extracted all variables for every study using the standardized Excel template (GenAI_MetaAnalysis_v10_TEMPLATE.xlsx). Coders were blinded to each other's extractions during this phase.

3. **Reliability assessment**: Inter-rater reliability was computed for all variable categories:
   - Categorical variables: Cohen's kappa (weighted where ordinal)
   - Continuous variables: Two-way random-effects, single-measures ICC(2,1)
   - Effect size values: ICC and mean absolute difference

4. **Consensus resolution**: All discrepancies were resolved through a structured protocol: (a) automatic resolution for within-threshold differences (e.g., rounding differences in statistics); (b) coder discussion for substantive disagreements; (c) third-reviewer adjudication for unresolved cases. Every resolution was documented in the DISCREPANCY_LOG sheet.

#### Gold Standard Reliability

[PLACEHOLDER: Report actual IRR statistics here]

| Variable Category | Metric | Value | Interpretation |
|:-----------------|:------:|:-----:|:--------------|
| Study characteristics (categorical) | Cohen's kappa | [PLACEHOLDER] | [PLACEHOLDER] |
| Study characteristics (continuous) | ICC(2,1) | [PLACEHOLDER] | [PLACEHOLDER] |
| Outcome classification | Cohen's kappa | [PLACEHOLDER] | [PLACEHOLDER] |
| Effect size values | ICC(2,1) | [PLACEHOLDER] | [PLACEHOLDER] |
| Effect size values | Mean |*d*| | [PLACEHOLDER] | [PLACEHOLDER] |

### LLM Extraction Protocol

#### Model Selection

Three frontier LLMs were selected based on: (a) representing distinct model families (different training data, architectures, and alignment approaches); (b) demonstrated capability on academic text processing; and (c) availability of API access for reproducible, programmatic extraction.

| Model | Provider | Version | Context Window | Access |
|:------|:---------|:--------|:--------------|:-------|
| Claude | Anthropic | [PLACEHOLDER: specific version] | [PLACEHOLDER] tokens | API |
| GPT-4o | OpenAI | [PLACEHOLDER: specific version] | 128K tokens | API |
| Gemini | Google | [PLACEHOLDER: specific version] | [PLACEHOLDER] tokens | API |

Model versions were frozen at the start of extraction and documented for reproducibility. All extractions used temperature = 0 (deterministic output) to ensure replicability.

#### Prompt Design

Prompts were developed through an iterative process:

1. **Initial design**: Structured prompts were created for each variable category, incorporating: (a) the variable definition from the coding manual; (b) permissible values and coding rules; (c) one worked example; and (d) output format specification (JSON).

2. **Pilot testing**: Prompts were tested on 5 studies not included in the final dataset. Outputs were compared against human coding, and prompts were refined to address systematic errors.

3. **Standardization**: Final prompts were identical across all three models to ensure comparability. The complete prompt library is available at [OSF Repository Link].

Prompts were organized into four extraction modules corresponding to variable categories:

| Module | Variables | Input | Output Format |
|:-------|:---------|:------|:-------------|
| A: Study Characteristics | [PLACEHOLDER: count] variables (authors, year, design, sample, discipline, tool, etc.) | Full-text PDF | JSON with field-level values |
| B: Outcome Classification | Outcome dimension, Bloom's level, measure type | Results/measures sections | JSON with classification + justification |
| C: Statistical Extraction | Means, SDs, sample sizes, test statistics, p-values | Results/tables | JSON with values + source location |
| D: Effect Size Verification | Hedges' g calculation inputs, computed values | Module C output + formulas | JSON with computed ES + verification |

#### Extraction Procedure

For each included study:

1. The full-text PDF was converted to text and provided to each LLM via API.
2. Modules A through D were executed sequentially (output from earlier modules provided as context for later modules where relevant).
3. Each model processed each study independently (no cross-model information sharing).
4. Raw model outputs (complete JSON responses) were logged in the AI_CODING sheet of the Excel workbook.
5. Extraction was conducted in [PLACEHOLDER: month/year], with all three models run within a [PLACEHOLDER]-day window to minimize version drift.

#### Cost and Time Recording

For each extraction, we recorded: (a) input token count; (b) output token count; (c) API cost (USD); (d) wall-clock processing time (seconds). These were compared against estimated human coding time based on coder logs from the gold standard coding phase.

### Analysis Plan

#### RQ1: Overall Accuracy

For each LLM, we computed:

- **Exact match rate**: Proportion of extracted values identical to the gold standard (after normalization for formatting differences).
- **Within-threshold match rate**: For continuous variables, proportion within a pre-specified tolerance (e.g., |difference| < 0.01 for effect sizes, |difference| < 0.5 for sample sizes).
- **Error rate**: Proportion of extracted values differing from the gold standard beyond tolerance thresholds.
- **Missing rate**: Proportion of variables the model failed to extract or returned null.

Overall accuracy was computed as a weighted average across variable categories, with weights proportional to the number of variables in each category.

#### RQ2: Variable-Type Analysis

Accuracy metrics were computed separately for each variable category (bibliographic, methodological, statistical, classificatory) and for individual variables within categories. We used:

- **Cohen's kappa** (categorical variables): Comparing LLM classifications against the gold standard.
- **ICC(2,1)** (continuous variables): Treating each LLM as a "rater" alongside the gold standard.
- **Error taxonomy**: Systematic classification of errors into types:
  - *Omission errors*: Variable not extracted (null/missing)
  - *Commission errors*: Incorrect value extracted
  - *Partial errors*: Partially correct (e.g., correct direction but wrong magnitude)
  - *Format errors*: Correct value, wrong format (e.g., "45" vs. "n = 45")
  - *Hallucination errors*: Plausible but fabricated values not present in source

#### RQ3: Multi-Model Consensus

Three consensus strategies were evaluated:

1. **Majority vote** (categorical): Accept the value agreed upon by at least 2 of 3 models. If all three disagree, flag for human review.
2. **Median value** (continuous): Take the median of three model estimates. If any estimate deviates by more than [PLACEHOLDER]% from the median, flag for human review.
3. **Unanimous agreement**: Accept only when all three models agree; flag all disagreements for human review.

For each strategy, we computed accuracy against the gold standard and the proportion of items flagged for human review (the "human review burden").

#### RQ4: Workflow Optimization

We modeled the total cost (time and monetary) of five workflows:

| Workflow | Description |
|:---------|:-----------|
| W1: Full human | Two human coders + consensus (current best practice) |
| W2: Single AI + full human verification | One LLM extracts, human verifies all fields |
| W3: Single AI + selective human verification | One LLM extracts, human verifies only flagged/complex fields |
| W4: Multi-AI consensus + selective human verification | Three LLMs extract, consensus for agreement, human for disagreement |
| W5: AI-first with human audit | AI consensus accepted for high-reliability fields; human codes only low-reliability fields from scratch |

For each workflow, we estimated: (a) accuracy (vs. gold standard); (b) total time (hours); (c) total cost (USD, including API fees and estimated human labor); (d) error rate by type.

The optimal workflow was identified as the one maximizing accuracy while minimizing cost, subject to a minimum accuracy threshold (operationalized as kappa > 0.80 for categorical and ICC > 0.90 for continuous variables).

---

## Results

*[This section will be populated after data collection and analysis are complete.]*

### Human Gold Standard Reliability

[PLACEHOLDER: IRR statistics for the human coding]

### RQ1: Overall LLM Accuracy

[PLACEHOLDER: Overall accuracy table by model]

**Table 1. Overall Extraction Accuracy by Model**

| Model | Exact Match | Within-Threshold | Error Rate | Missing Rate | Weighted Accuracy |
|:------|:----------:|:----------------:|:----------:|:------------:|:-----------------:|
| Claude | [PH] | [PH] | [PH] | [PH] | [PH] |
| GPT-4o | [PH] | [PH] | [PH] | [PH] | [PH] |
| Gemini | [PH] | [PH] | [PH] | [PH] | [PH] |

### RQ2: Variable-Type Analysis

[PLACEHOLDER: Variable-category breakdown]

**Table 2. Agreement with Gold Standard by Variable Category and Model**

| Variable Category | Metric | Claude | GPT-4o | Gemini |
|:-----------------|:------:|:------:|:------:|:------:|
| Bibliographic (author, year, title) | Exact match | [PH] | [PH] | [PH] |
| Methodological (design, sample, tool) | Kappa | [PH] | [PH] | [PH] |
| Statistical (M, SD, n, test stats) | ICC | [PH] | [PH] | [PH] |
| Classificatory (outcome dim., Bloom) | Kappa | [PH] | [PH] | [PH] |
| Effect sizes (Hedges' g) | ICC | [PH] | [PH] | [PH] |

[PLACEHOLDER: Error taxonomy analysis]

**Table 3. Error Type Distribution by Model**

| Error Type | Claude | GPT-4o | Gemini |
|:-----------|:------:|:------:|:------:|
| Omission | [PH] | [PH] | [PH] |
| Commission | [PH] | [PH] | [PH] |
| Partial | [PH] | [PH] | [PH] |
| Format | [PH] | [PH] | [PH] |
| Hallucination | [PH] | [PH] | [PH] |

### RQ3: Multi-Model Consensus

[PLACEHOLDER: Consensus performance]

**Table 4. Multi-Model Consensus Performance**

| Strategy | Accuracy | Human Review Burden | Effective Accuracy (after human review) |
|:---------|:--------:|:-------------------:|:---------------------------------------:|
| Majority vote | [PH] | [PH] | [PH] |
| Median value | [PH] | [PH] | [PH] |
| Unanimous agreement | [PH] | [PH] | [PH] |
| Best single model | [PH] | — | [PH] |

### RQ4: Workflow Comparison

[PLACEHOLDER: Workflow analysis]

**Table 5. Workflow Cost-Accuracy Comparison**

| Workflow | Accuracy | Time (hrs) | Cost (USD) | Error Rate |
|:---------|:--------:|:----------:|:----------:|:----------:|
| W1: Full human | Reference | [PH] | [PH] | [PH] |
| W2: Single AI + full verify | [PH] | [PH] | [PH] | [PH] |
| W3: Single AI + selective verify | [PH] | [PH] | [PH] | [PH] |
| W4: Multi-AI + selective verify | [PH] | [PH] | [PH] | [PH] |
| W5: AI-first + human audit | [PH] | [PH] | [PH] | [PH] |

---

## Discussion

### Summary of Findings

[PLACEHOLDER: Summarize key findings from RQ1-RQ4]

### Comparison with Prior Work

The findings extend the growing literature on LLM-assisted systematic review automation. Prior evaluations of GPT-4 for data extraction in clinical systematic reviews (Guo et al., 2024; Wang et al., 2024) reported [PLACEHOLDER: compare with our findings]. Our study advances this work by: (a) comparing three models head-to-head rather than evaluating a single model; (b) examining educational rather than clinical research, where coding schemas involve more subjective judgments; (c) evaluating the full range of meta-analysis variables rather than only PICO elements; and (d) introducing multi-model consensus as a reliability-enhancing strategy.

[PLACEHOLDER: Discuss model-specific strengths and weaknesses]

### Implications for Systematic Review Practice

#### When AI Coding Is Sufficient

[PLACEHOLDER: Based on RQ2, identify variable types where AI extraction meets reliability thresholds without human verification]

#### When Human Verification Remains Essential

[PLACEHOLDER: Based on RQ2, identify variable types where human verification is necessary]

#### The Case for Multi-Model Consensus

[PLACEHOLDER: Based on RQ3, discuss whether consensus approaches justify additional API costs]

#### A Recommended Workflow

Based on our findings, we recommend [PLACEHOLDER: describe the optimal workflow from RQ4]. This approach [PLACEHOLDER: describe accuracy and efficiency gains].

The recommended workflow proceeds in three phases:

1. **AI extraction phase**: [PLACEHOLDER: which models, which prompts]
2. **Automated quality control**: [PLACEHOLDER: consensus rules, flagging criteria]
3. **Targeted human review**: [PLACEHOLDER: which fields, estimated burden]

### Limitations

Several limitations should be noted. First, our evaluation is based on a single meta-analysis dataset from the educational technology domain. The coding schema, variable types, and study characteristics may not generalize to clinical, biomedical, or other systematic review contexts where different challenges (e.g., RCT-specific data, drug dosing information, adverse event coding) predominate. Replication across diverse review domains is needed.

Second, LLM capabilities evolve rapidly. The specific model versions evaluated here ([PLACEHOLDER: versions]) may be superseded by more capable models within months. However, our evaluation framework and prompt library can be readily applied to future models, and the general patterns observed (e.g., relative difficulty of variable types) are likely to persist across model generations.

Third, we used a fixed prompt design across all three models. Model-specific prompt optimization could improve individual model performance but would complicate cross-model comparison. Our standardized approach prioritizes comparability and practical replicability.

Fourth, the gold standard itself is not error-free. While dual-coded with documented reliability and consensus resolution, some residual errors likely remain in the human reference data. These would appear as "AI errors" in our analysis when the AI extraction is actually correct. The impact of this limitation is bounded by the observed human inter-rater reliability statistics.

Fifth, our cost analysis relies on API pricing at the time of data collection ([PLACEHOLDER: date]), which is subject to change. However, the relative cost comparisons between workflows are likely more stable than absolute costs, as all models tend to decrease in price over time.

### Future Directions

[PLACEHOLDER: Based on findings, suggest 3-4 directions]

1. **Domain-specific evaluation**: Replicate this framework in clinical, environmental, and social science systematic reviews to assess generalizability.
2. **Fine-tuned models**: Evaluate whether domain-specific fine-tuning improves extraction accuracy for the variable types where general-purpose LLMs underperform.
3. **Dynamic prompt optimization**: Develop adaptive prompting strategies that adjust extraction approach based on study characteristics (e.g., complexity, reporting quality).
4. **Longitudinal tracking**: Establish a benchmark dataset and leaderboard for tracking LLM performance on systematic review extraction tasks across model generations.

---

## Conclusion

[PLACEHOLDER: Write after results are available]

This study demonstrates that [PLACEHOLDER: key finding]. By comparing three frontier LLMs against a rigorously established human gold standard, we provide the first comprehensive evidence base for integrating AI-assisted coding into systematic review workflows. Our findings suggest that [PLACEHOLDER: practical recommendation], offering a path toward more efficient and scalable evidence synthesis without compromising the methodological rigor that gives systematic reviews their epistemic authority.

---

## References

Bossuyt, P. M., Reitsma, J. B., Bruns, D. E., Gatsonis, C. A., Glasziou, P. P., Irwig, L., ... & Cohen, J. F. (2015). STARD 2015: An updated list of essential items for reporting diagnostic accuracy studies. *Radiology*, *277*(3), 826-832.

Brown, T. B., Mann, B., Ryder, N., Subbiah, M., Kaplan, J., Dhariwal, P., ... & Amodei, D. (2020). Language models are few-shot learners. *Advances in Neural Information Processing Systems*, *33*, 1877-1901.

Buscemi, N., Hartling, L., Vandermeer, B., Tjosvold, L., & Klassen, T. P. (2006). Single data extraction generated more errors than double data extraction in systematic reviews. *Journal of Clinical Epidemiology*, *59*(7), 697-703.

Guo, E., Gupta, M., Deng, J., Park, Y. J., Paget, M., & Nauber, C. (2024). Automated paper screening for clinical reviews using large language models. *Journal of Medical Internet Research*, *26*, e48996.

Higgins, J. P. T., Thomas, J., Chandler, J., Cumpston, M., Li, T., Page, M. J., & Welch, V. A. (Eds.). (2023). *Cochrane handbook for systematic reviews of interventions* (Version 6.4). Cochrane.

Jones, A. P., Remmington, T., Williamson, P. R., Ashby, D., & Smyth, R. L. (2005). High prevalence but low impact of data extraction and reporting errors were found in Cochrane systematic reviews. *Journal of Clinical Epidemiology*, *58*(7), 741-742.

Jonnalagadda, S. R., Goyal, P., & Huffman, M. D. (2015). Automating data extraction in systematic reviews: A systematic review. *Systematic Reviews*, *4*, 78.

Khraisha, Q., Put, S., Kappenberg, J., Warber, A., & Ostfeld, K. (2024). Can large language models replace humans in systematic reviews? A comprehensive review. *Research Synthesis Methods*, *15*(6), 842-862.

Marshall, I. J., & Wallace, B. C. (2019). Toward systematic review automation: A practical guide to using machine learning tools in research synthesis. *Systematic Reviews*, *8*, 163.

O'Mara-Eves, A., Thomas, J., McNaught, J., Miwa, M., & Ananiadou, S. (2015). Using text mining for study identification in systematic reviews: A systematic review of current approaches. *Systematic Reviews*, *4*, 5.

Pigott, T. D., & Polanin, J. R. (2020). Methodological guidance paper: High-quality meta-analysis in a systematic review. *Review of Educational Research*, *90*(1), 24-46.

Tsafnat, G., Glasziou, P., Choong, M. K., Dunn, A., Galgani, F., & Coiera, E. (2014). Systematic review automation technologies. *Systematic Reviews*, *3*, 74.

Wang, S., Scells, H., Koopman, B., & Zuccon, G. (2024). Can ChatGPT write a good boolean query for systematic review literature search? *arXiv preprint arXiv:2302.03495*.

Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., ... & Zhou, D. (2022). Chain-of-thought prompting elicits reasoning in large language models. *Advances in Neural Information Processing Systems*, *35*, 24824-24837.

You, H. (2026). Generative AI in higher education: A three-level meta-analysis revealing cognitive dependency in metacognitive outcomes. [Manuscript in preparation]. College of Education, Pennsylvania State University.

---

## Appendices

### Appendix A: Complete Prompt Library

*[To be populated with the standardized extraction prompts for each module (A-D) after pilot testing.]*

### Appendix B: Variable-Level Accuracy Tables

*[To be populated with per-variable kappa/ICC values for each model.]*

### Appendix C: Error Examples

*[To be populated with representative examples of each error type from each model, with source text.]*

### Appendix D: Relationship to the Parent Meta-Analysis

This methodological study (Paper B) and the parent meta-analysis (Paper A; You, 2026) share the same human gold standard dataset but serve distinct purposes:

- **Paper A** reports a substantive three-level meta-analysis of generative AI effectiveness in higher education. It uses only human-coded data and makes no reference to AI-assisted coding. Paper A can be read and evaluated independently as a standalone contribution to the educational technology literature.

- **Paper B** (this paper) evaluates the reliability of LLM-assisted coding by comparing AI extractions against the human gold standard established during Paper A's data collection. Paper B references Paper A's dataset as a benchmark but contributes independently to the research synthesis methodology literature.

The gold standard was established through Paper A's dual-coding protocol *before* any AI extraction was conducted, ensuring that human coding was not influenced by AI outputs. The chronological workflow was:

1. Human coders independently coded all studies (Paper A protocol)
2. Inter-rater reliability computed and discrepancies resolved → gold standard finalized
3. LLMs independently extracted the same data (Paper B protocol)
4. AI outputs compared against the finalized gold standard

This temporal separation ensures the independence and integrity of both the gold standard and the AI evaluation.

---

*Manuscript scaffold created: 2026-02-16*
*Status: Awaiting data collection for empirical sections*
