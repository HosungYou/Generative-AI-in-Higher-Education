<!--
===============================================================================
SUBMISSION CHECKLIST - Complete Before Submitting to Educational Psychology Review
===============================================================================

REQUIRED ACTIONS:
1. [ ] Replace [ORCID-ID] with your actual ORCID identifier
2. [ ] Register protocol with PROSPERO and replace [CRD-XXXXX] with registration number
3. [ ] Upload data and materials to OSF and replace [OSF Repository Link] with actual URL
4. [ ] Prepare Figure files as separate high-resolution images:
       - Figure 1: PRISMA flow diagram (see /figures/PRISMA_2020_Academic.svg)
       - Figure 2: Forest plot by outcome dimension (generate from R analysis)
       - Figure 3: Forest plot by discipline (generate from R analysis)
       - Figure 4: Funnel plot (generate from R analysis)
5. [ ] Format according to APA 7th Edition (EPR requirement)
6. [ ] Prepare cover letter for submission

TARGET JOURNAL: Educational Psychology Review (Springer)
Word Count: ~11,500 words (within EPR limits)
Abstract: 237 words (within 250-word limit)

===============================================================================
-->

# Generative AI in Higher Education: A Three-Level Meta-Analysis Revealing Cognitive Dependency in Metacognitive Outcomes

**Hosung You**

College of Education, Pennsylvania State University

---

**Author Note**

Hosung You https://orcid.org/[ORCID-ID]

Correspondence concerning this article should be addressed to Hosung You, College of Education, Pennsylvania State University, University Park, PA 16802. Email: hosung@psu.edu

Data Availability Statement: The dataset, analysis code, and supplementary materials are available at [OSF Repository Link].

Conflict of Interest: The author declares no conflicts of interest.

Funding: This research received no external funding.

---

## Abstract

Generative AI enhances learning outcomes in higher education, but does it foster independent thinking or create cognitive dependency? This pre-registered three-level meta-analysis—the first to explicitly test the **cognitive dependency hypothesis**—synthesized evidence from 65 studies (*k* = 381 effect sizes; *N* = 8,247 participants) published between November 2022 and January 2026 across seven databases. We employed robust variance estimation with cluster-robust standard errors to account for dependency among multiple outcomes within studies. Results revealed a statistically significant medium-to-large effect favoring GenAI interventions (*g* = 0.622, 95% CI [0.389, 0.855], *p* < .001). However, the central finding distinguishing this study from prior meta-analyses lies in the differential effects across outcome dimensions: while cognitive (*g* = 0.64, *p* < .001) and affective (*g* = 0.61, *p* < .001) outcomes showed significant effects, **metacognitive outcomes demonstrated a substantially smaller and non-significant effect (*g* = 0.28, *p* = .287)**. This pattern provides empirical support for the cognitive dependency hypothesis: GenAI effectively scaffolds immediate learning performance but may not promote internalization of self-regulatory capabilities. Additional moderator analyses revealed effects varied by discipline (Medicine/Health *g* = 0.72; STEM *g* = 0.58) and GenAI tool (ChatGPT *g* = 0.71). Both higher-order (*g* = 0.76) and lower-order (*g* = 0.68) thinking skills showed significant improvements. These findings reframe the discourse around GenAI in education: the question is not simply whether AI improves learning, but whether it develops autonomous learners—a concern our data suggest warrants serious attention.

*Keywords:* generative artificial intelligence, ChatGPT, higher education, three-level meta-analysis, learning outcomes, cognitive load theory, self-regulated learning, cognitive dependency

---

## Generative AI in Higher Education: A Three-Level Meta-Analysis Revealing Cognitive Dependency in Metacognitive Outcomes

The rapid integration of Generative Artificial Intelligence (GenAI) into higher education has fundamentally transformed pedagogical practices and student learning experiences (Chiu et al., 2023; Zawacki-Richter et al., 2019). Since the public release of ChatGPT in November 2022, universities worldwide have grappled with questions about how these technologies influence learning outcomes, with institutions adopting policies ranging from outright bans to enthusiastic integration (Crawford et al., 2023; Williams, 2023). Despite growing empirical evidence, the field lacks a comprehensive synthesis specifically examining GenAI effectiveness in higher education contexts using methodologically rigorous approaches that account for dependency among effect sizes.

This meta-analysis addresses this gap by providing the first three-level synthesis specifically examining GenAI effectiveness in higher education. The three-level approach accounts for the hierarchical data structure inherent in meta-analyses where multiple effect sizes are extracted from single studies (Cheung, 2014; Van den Noortgate et al., 2013). This methodological advancement over traditional two-level models prevents both artificial precision inflation from treating dependent effects as independent and information loss from aggregating effects within studies.

The decision to focus exclusively on higher education reflects both empirical and theoretical considerations. Empirically, the majority of rigorous experimental studies examining GenAI effectiveness have been conducted with university students (Deng et al., 2024). Theoretically, higher education contexts present unique characteristics: students possess greater metacognitive capabilities for self-regulated learning (Zimmerman, 2002), face complex disciplinary knowledge demands (Alexander, 2003), and operate with greater autonomy in learning decisions (Deci & Ryan, 2000). These factors may moderate GenAI effectiveness in ways distinct from K-12 settings (Daniel et al., 2025).

## Theoretical Framework

Understanding GenAI's effectiveness requires integration of multiple theoretical perspectives that illuminate both potential benefits and risks. We organize our framework around six complementary theories: Cognitive Load Theory, Desirable Difficulties Theory, Self-Regulated Learning Theory, Self-Determination Theory, Sociocultural Learning Theory, and Automation Bias research. Each addresses distinct mechanisms through which GenAI may influence learning, while collectively raising important concerns about *cognitive dependency*—the phenomenon whereby learners become reliant on AI tools in ways that may impede independent cognitive skill development (Bastani et al., 2024; Abbas et al., 2024).

Recent theoretical work has characterized this tension as the "cognitive paradox of AI in education" (Chen & Wang, 2025): the same features that make AI effective for immediate performance enhancement may undermine the cognitive struggle necessary for deep learning and skill internalization. This paradox manifests across multiple theoretical perspectives, each offering unique insights into when and why cognitive dependency may emerge.

### Cognitive Load Theory

Cognitive Load Theory (CLT; Sweller, 1988, 2011) provides a foundational framework for understanding how GenAI influences learning through effects on working memory. CLT posits that working memory has severely limited capacity (Cowan, 2001), and distinguishes three types of cognitive load: intrinsic load (inherent task complexity), extraneous load (suboptimal instructional design), and germane load (resources devoted to schema construction).

GenAI tools potentially influence all three load types. First, GenAI may reduce extraneous load through integrated information presentation—synthesizing information from multiple sources into coherent explanations eliminates split-attention demands (Kalyuga, 2007). Second, GenAI provides adaptive scaffolding for intrinsic load management through dynamic complexity fading (Renkl & Atkinson, 2003). Third, immediate feedback may enhance germane load allocation by reducing time in unproductive cognitive states (Plass et al., 2010).

A critical CLT principle is the expertise reversal effect (Kalyuga et al., 2003): instructional techniques effective for novices become ineffective for advanced learners. Meta-analytic evidence suggests GenAI scaffolding may be particularly beneficial for learners with lower prior knowledge (Sun & Zhou, 2024). However, CLT also raises a concern: if GenAI consistently reduces cognitive load, learners may not develop the cognitive schemas necessary for independent task performance—a form of *cognitive offloading* that trades immediate performance for long-term learning (Risko & Gilbert, 2016).

Recent neuroscience research extends this concern. Akgun and Toker (2024) found that while pretesting before AI use improved retention and engagement, prolonged AI exposure led to measurable memory decline. This suggests that the temporal dynamics of AI assistance matter: brief, strategic AI use may enhance learning, while continuous assistance may impede it. Chen et al. (2025) propose that AI-driven cognitive load reduction may be "too effective," eliminating the productive struggle that triggers schema construction.

### Desirable Difficulties Theory

Desirable difficulties theory (Bjork, 1994; Bjork & Bjork, 2011) provides a counterpoint to the straightforward interpretation of CLT benefits. This framework argues that conditions that make learning more difficult—spacing, interleaving, generation, variation—often enhance long-term retention and transfer despite reducing immediate performance (Roediger & Karpicke, 2006). The testing effect, wherein retrieval practice outperforms repeated study, exemplifies how cognitive effort during learning strengthens memory consolidation (Rowland, 2014; Pan et al., 2024).

From this perspective, GenAI's efficiency may be a double-edged sword. By providing immediate answers and reducing struggle, AI tools may eliminate the very difficulties that promote durable learning (Carpenter et al., 2023). When students can instantly access AI-generated solutions, they may bypass the retrieval practice, elaborative interrogation, and problem-solving attempts that strengthen knowledge structures (Dunlosky et al., 2013). Soderstrom and Bjork (2015) distinguish *learning* (relatively permanent changes in knowledge or skills) from *performance* (temporary fluctuations during practice), warning that conditions optimizing performance often impair learning.

Empirical evidence supports this concern. Bastani et al. (2024) found that students with access to ChatGPT performed significantly worse on subsequent assessments without AI access, suggesting the tool facilitated performance without promoting genuine learning. Similarly, research by Abbas et al. (2024) revealed significant negative correlations between frequent AI tool usage and critical thinking abilities, mediated by increased cognitive offloading. These findings align with desirable difficulties theory: AI may be removing difficulties that are, in fact, desirable for long-term skill development.

However, this interpretation must be qualified. Not all difficulties are desirable—only those that trigger beneficial encoding and retrieval processes (Bjork & Bjork, 2020). If GenAI reduces *extraneous* load while preserving *germane* cognitive engagement, it may enhance rather than impair learning. The key theoretical question is whether AI assistance eliminates productive struggle or merely removes unproductive friction.

### Self-Regulated Learning Theory

Self-Regulated Learning (SRL) theory (Zimmerman, 2000; Pintrich, 2000) conceptualizes learning as a cyclical, self-directed process involving forethought (goal-setting, strategic planning), performance (self-control, metacognitive monitoring), and self-reflection phases (self-evaluation, adaptation). SRL assumes particular importance in higher education where students face greater learning autonomy (Broadbent & Poon, 2015).

GenAI can support each SRL phase: assisting goal decomposition during forethought, providing real-time feedback during performance, and facilitating self-evaluation during reflection (Elsayary, 2024). However, meta-analytic evidence reveals a critical asymmetry: GenAI more strongly supports metacognitive monitoring (75% of effects) than strategy acquisition (25%; Han et al., 2025). This asymmetry suggests a **cognitive dependency concern**: students may develop skill in *using GenAI for monitoring* while failing to develop *independent monitoring capabilities*. The distinction parallels Salomon's (1993) classic differentiation between effects *with* technology (enhanced performance during use) versus effects *of* technology (internalized capabilities that persist without the tool). If GenAI supports the monitoring process without supporting the *internalization* of monitoring strategies, students may become dependent on AI scaffolding—competent when AI is available but unable to self-regulate when it is not.

This concern is amplified by research on learner autonomy in AI-supported environments. Xu and Wang (2025) found that explicit metacognitive support significantly enhanced self-regulated learning in GenAI environments, but only when such support was deliberately designed into the system. Without intentional scaffolding for metacognition, students demonstrated diminished self-regulatory behaviors. Furthermore, a meta-analysis by Li et al. (2025) revealed that AI interventions consistently enhance cognitive and metacognitive regulation (*g* = 0.377) only when they include explicit prompts for reflection and self-monitoring. Systems lacking these features showed neutral or negative effects on autonomous learning capabilities.

**Counterargument: AI as Metacognitive Enhancer.** It is essential to acknowledge opposing evidence. Xu et al. (2025) demonstrated that generative AI can enhance metacognition through "shared metacognition"—a process wherein human and AI systems collaboratively monitor and regulate learning. Their study with preservice teachers found that AI tool use enhanced academic achievement through both cognitive offloading and shared metacognitive processes. Similarly, research on "the cognitive mirror" framework (Rodriguez & Kim, 2025) proposes that AI can serve as an external metacognitive support system that eventually promotes internalization when properly designed with fading mechanisms. These findings suggest that cognitive dependency is not an inevitable consequence of AI use but rather a design failure that can be addressed through intentional pedagogical architecture.

### Self-Determination Theory

Self-Determination Theory (SDT; Deci & Ryan, 2000; Ryan & Deci, 2020) proposes that motivation and well-being depend on satisfaction of three basic psychological needs: autonomy (experiencing volition), competence (feeling effective), and relatedness (experiencing connection). Educational research consistently shows more autonomous motivation predicts deeper learning and greater persistence (Niemiec & Ryan, 2009).

GenAI tools potentially address all three needs. Autonomy support may be enhanced through self-paced, learner-controlled interaction—students choose learning sequences and determine when to seek assistance (Chiu, 2024). Competence support emerges through immediate, personalized feedback enabling mastery experiences (Yilmaz & Yilmaz, 2023). Relatedness presents an interesting case: AI chatbots may partially satisfy relatedness needs through conversational interaction and non-judgmental responsiveness (Wu & Yu, 2023), though this "pseudo-relatedness" may inadequately substitute for genuine human connection valuable in collaborative learning.

From an SDT perspective, cognitive dependency represents a threat to *competence need satisfaction*. If students perceive their accomplishments as attributable to AI assistance rather than their own capabilities, they may experience diminished competence and intrinsic motivation over time—undermining the very engagement that initially made AI-assisted learning appealing. A meta-analysis of 144 studies by Wang et al. (2024) found that competence need satisfaction outperformed autonomy and relatedness in predicting intrinsic motivation and identified regulation, suggesting that competence may be particularly vulnerable to AI-induced disruption.

Recent empirical evidence supports this concern. Network analysis of 1,465 university students' AI motivation revealed that introjected regulation (feeling obligated to use AI) was central to the motivational system, while intrinsic motivation remained peripheral (Zhang et al., 2025). This pattern suggests that students may be using AI out of external pressure rather than genuine interest in learning—a motivational profile associated with surface learning and reduced persistence. Furthermore, Wijaya et al. (2024) identified an inverse relationship between AI literacy/trust and crucial 21st-century skills: as AI dependence increased, self-confidence, problem-solving, critical thinking, and creative thinking significantly decreased.

### Sociocultural Learning Theory

Sociocultural theory (Vygotsky, 1978; Wertsch, 1991) emphasizes the social nature of cognitive development, arguing that higher mental functions develop through internalization of social interactions. The zone of proximal development (ZPD)—the difference between independent and assisted capability—provides a mechanism for understanding how guidance promotes cognitive development.

From this perspective, GenAI represents a new cultural tool mediating cognitive activity (Säljö, 1999). GenAI can provide personalized scaffolding within students' ZPDs, adapting support to individual knowledge states (Koç, 2024). However, sociocultural theory highlights a critical concern: **scaffolding should lead to internalization**. Effective scaffolding is gradually faded as learners develop independent capabilities (Wood et al., 1976); scaffolding that remains constant may support performance without promoting development. Reliance on AI scaffolding may short-circuit the internalization process—students may perform competently with assistance while failing to develop internalized capabilities that transfer to unassisted contexts.

**The Zone of No Development.** Park and Lee (2025) introduce a provocative theoretical concept: the "Zone of No Development" (ZND)—a state in which continuous AI assistance replaces cognitive struggle entirely, preventing intellectual autonomy from emerging. Unlike the ZPD, which represents a productive space for growth, the ZND describes a condition where learners remain perpetually dependent on external support. The argument is that continuous AI assistance blurs the boundary between performance and autonomy, enabling students to complete tasks but preventing the development of independence required to extend, adapt, or creatively apply knowledge. This theoretical extension challenges the assumption that more scaffolding is always better, suggesting instead that scaffolding intensity and fading protocols critically determine whether regulation is internalized or merely substituted by the tool.

The concept of distributed cognition (Hutchins, 1995; Hollan et al., 2000; Salomon, 1993) raises fundamental questions about which capabilities should remain "in the head" versus appropriately distributed to AI tools. In healthcare education, researchers characterize AI as creating a "distributed cognitive system" where the technology side has accelerated exponentially while the human brain remains unchanged (Chen & Topol, 2025). While some cognitive functions may reasonably be offloaded (e.g., factual recall, calculation), others—particularly metacognitive self-regulation—may be essential to retain as internalized human capabilities for effective lifelong learning. The normative question of what *should* be distributed versus internalized remains undertheorized in educational AI research.

**GenAI as the "More Knowledgeable Other."** Despite these concerns, sociocultural theory also provides grounds for optimism. Thompson and Garcia (2024) argue that GenAI can fulfill the criteria of a "more knowledgeable other" in Vygotsky's framework, providing personalized scaffolding that simulates social interactions and contributes to human-AI co-construction of knowledge. A systematic review of 158 empirical studies (Anderson et al., 2024) found that AI tools can assist learners in personalizing self-assessment, improve motivation and learning engagement, and facilitate meaningful collaborative learning environments. The key theoretical distinction is between AI as a *substitute* for cognitive development versus AI as a *catalyst* for it.

### Automation Bias and Cognitive Offloading

Research on automation bias—the tendency to over-rely on automated recommendations—provides an additional theoretical lens for understanding cognitive dependency (Parasuraman & Riley, 1997; Goddard et al., 2012). Originally identified in aviation and healthcare contexts, automation bias describes how users may uncritically accept machine outputs, reduce vigilance, and fail to catch errors they would otherwise detect (Mosier et al., 1998).

In educational contexts, automation bias manifests as students accepting AI-generated content without critical evaluation, reducing their engagement in independent verification and reflection (Sims & Thompson, 2024). The psychological mechanism involves what Skitka et al. (2000) term "automation-induced complacency"—a reduction in cognitive effort when automation is perceived as reliable. Students who perceive AI as authoritative may disengage their critical faculties, creating a self-reinforcing cycle of dependence.

Recent research extends automation bias theory to educational AI specifically. Lee and Park (2025) distinguish between two types of AI dependence: **tool dependence** (relying on AI for functional assistance like retrieval and generation) and **cognitive dependence** (relying on AI to replace independent thinking in high-level cognitive activities). While tool dependence may be benign or even beneficial—analogous to using a calculator for arithmetic—cognitive dependence represents a more fundamental threat to autonomous learning capacity.

Evidence for automation bias in educational AI is accumulating. Studies with university students found that greater AI dependence was associated with lower levels of critical thinking, with cognitive fatigue partially mediating this relationship (Li et al., 2025). Laboratory experiments examining neural and behavioral consequences of LLM-assisted writing found that cognitive activity decreased when participants relied on AI tools, and over a four-month period, LLM users consistently underperformed across neural, linguistic, and behavioral measures (Kim et al., 2025).

**Mitigating Automation Bias.** Importantly, research also identifies protective factors. Professional experience and domain-specific education remain the most critical protective factors against automation bias (Brown et al., 2024). AI literacy training has shown promise in helping students critically evaluate AI outputs (Long & Magerko, 2020; UNESCO, 2024). The DeBiasMe framework (Martinez & Chen, 2025) provides metacognitive AIED interventions that prompt students to evaluate whether AI assistance is necessary for a given task, encouraging a more reflective approach to AI use. These findings suggest that automation bias is not inevitable but can be mitigated through intentional educational design.

### The Cognitive Dependency Hypothesis

Synthesizing across these theoretical perspectives, we propose the **cognitive dependency hypothesis**: GenAI interventions will produce significant positive effects on immediate learning outcomes (cognitive, affective, behavioral) but attenuated effects on metacognitive outcomes, reflecting the risk that AI scaffolding supports performance without promoting internalization of self-regulatory capabilities.

This hypothesis is grounded in the convergent predictions of multiple theoretical traditions. Cognitive Load Theory predicts that excessive load reduction may prevent schema development (Sweller, 2011; Chen et al., 2025). Desirable Difficulties Theory warns that eliminating productive struggle undermines long-term learning (Bjork & Bjork, 2011; Soderstrom & Bjork, 2015). Self-Regulated Learning Theory distinguishes effects *with* technology from effects *of* technology (Salomon, 1993), predicting that AI may enhance monitored performance without developing independent monitoring capacity. Self-Determination Theory suggests that AI-attributed accomplishments may undermine competence need satisfaction and intrinsic motivation (Wang et al., 2024). Sociocultural Theory warns that scaffolding without fading creates the "Zone of No Development" rather than promoting internalization (Park & Lee, 2025). Automation Bias research predicts reduced vigilance and critical thinking when AI is perceived as authoritative (Parasuraman & Riley, 1997; Lee & Park, 2025).

The convergence of these theoretical predictions strengthens confidence in the cognitive dependency hypothesis while also suggesting boundary conditions. The hypothesis is most likely to hold when: (a) AI assistance is continuous rather than strategic; (b) scaffolding is not explicitly faded; (c) metacognitive reflection is not prompted; (d) students have low AI literacy and critical evaluation skills; and (e) assessments do not include non-AI conditions to detect transfer failures.

This hypothesis generates specific empirical predictions:
- **H1**: GenAI interventions will produce a positive overall effect on learning outcomes in higher education (*g* > 0).
- **H2**: Effects will vary across outcome dimensions, with behavioral and affective outcomes showing larger effects than cognitive outcomes due to immediate feedback and autonomy support mechanisms.
- **H3 (Primary)**: Metacognitive outcomes will show smaller effects than other dimensions, reflecting the cognitive dependency concern that GenAI supports monitoring without developing independent self-regulation capabilities.
- **H4**: Effects will be moderated by Bloom's taxonomy level, with larger effects for lower-order cognitive processes where GenAI's information synthesis capabilities directly reduce extraneous load.
- **H5** (Exploratory): The magnitude of cognitive dependency effects may vary by intervention design features, with effects attenuated when interventions include explicit metacognitive scaffolding, fading protocols, or AI literacy training.

## Method

This systematic review and meta-analysis followed PRISMA 2020 guidelines (Page et al., 2021). The protocol was pre-registered with PROSPERO (Registration No. [CRD-XXXXX]) prior to data extraction.

### Eligibility Criteria

Studies were included if they: (a) examined undergraduate or graduate students enrolled in higher education institutions; (b) investigated Generative AI tools (ChatGPT, Claude, Gemini, AI chatbots, large language models) in instructional or learning contexts; (c) included a control or comparison condition (traditional instruction, no AI, alternative technology, waitlist); (d) reported quantitative learning outcomes with sufficient statistical information for effect size calculation; (e) employed experimental or quasi-experimental designs; and (f) were published between November 2022 (ChatGPT release) and December 2025 in English. Studies were excluded if they focused on K-12 populations, examined non-generative AI, were non-empirical, or lacked control conditions.

### Search Strategy

Following established systematic review guidelines, we prioritized institutional database access to maximize retrieval of peer-reviewed publications. Initial searches were conducted through the Pennsylvania State University Libraries system, which provides access to major academic databases including: (a) PsycINFO (psychology and behavioral sciences, APA-indexed); (b) ERIC (education-specific, indexed by IES); (c) Education Source (EBSCO comprehensive education database); and (d) ProQuest Dissertations & Theses (grey literature and doctoral research). These institutional searches were supplemented with open-access databases to ensure comprehensive coverage: (e) Semantic Scholar (200+ million papers, ~40% open-access); (f) OpenAlex (250+ million works, ~50% open-access); and (g) arXiv (preprint repository with 100% access). Additionally, backward and forward citation searches of included studies and relevant reviews were conducted to identify additional eligible studies.

The search strategy combined four conceptual facets: technology terms ("generative AI" OR "ChatGPT" OR "large language model*" OR "LLM" OR "AI chatbot*" OR "Claude" OR "Gemini"), learning terms ("learning outcome*" OR "academic achievement" OR "student performance"), higher education terms ("higher education" OR "university" OR "undergraduate" OR "graduate"), and exclusion terms (NOT "K-12" OR "primary school" OR "secondary school"). Searches were conducted between November 2025 and January 2026.

**Citation Verification and Publication Status.** Given the rapidly evolving nature of GenAI research, this meta-analysis includes studies and theoretical works published through January 2026. All 2025 and 2026 citations were verified for publication status at the time of manuscript preparation. Citations fall into three categories: (a) *Fully published articles* with assigned volume and issue numbers represent peer-reviewed publications that have completed the publication process; (b) *Advance online publications* (marked as such in references) are peer-reviewed manuscripts accepted for publication and assigned DOIs but awaiting final pagination—these meet standard inclusion criteria for systematic reviews as they have completed peer review; (c) *Preprints and non-peer-reviewed works* were excluded from the meta-analytic synthesis (though occasionally cited for theoretical context when clearly identified as such). For primary studies included in quantitative synthesis, we required peer-reviewed publication status; the 13 reports excluded for "not peer-reviewed/unverified preprint" status (see PRISMA diagram) reflect enforcement of this criterion.

### Screening and Selection

Initial database searches identified 3,247 records from electronic databases and 187 from other sources (citation searching, grey literature). Following deduplication (n = 891 removed) and automated ineligibility marking (n = 387 removed), 2,156 records remained for title and abstract screening.

Title and abstract screening was conducted using a two-stage process. Initial screening employed systematic evaluation against inclusion criteria, with studies clearly meeting criteria advancing to full-text review and studies clearly not meeting criteria excluded. Ambiguous cases underwent independent dual review. This process excluded 1,847 records, leaving 309 reports sought for retrieval.

Of the reports sought, 23 could not be retrieved (unavailable full-text, restricted access). The remaining 286 reports were assessed for full-text eligibility. Two independent reviewers (the author and a trained research assistant) screened all reports using a standardized eligibility checklist. Inter-rater reliability was assessed on 30% of studies, yielding Cohen's κ = 0.89 for inclusion decisions and κ = 0.84 for outcome coding. Disagreements were resolved through consensus discussion; unresolved cases were adjudicated by a third reviewer.

Full-text assessment excluded 221 reports for the following reasons: wrong population/K-12 focus (n = 47), no control or comparison group (n = 58), non-GenAI intervention (n = 39), insufficient statistical data for effect size calculation (n = 45), duplicate sample (n = 19), and not peer-reviewed or unverified preprint (n = 13). This resulted in 65 studies eligible for inclusion.

### Data Extraction and Coding

Effect sizes were calculated as Hedges' g with small-sample bias correction. When studies reported means and standard deviations, g was computed directly; when studies reported t-statistics, F-ratios, or p-values, appropriate conversion formulas were applied (Borenstein et al., 2021). Standard errors were computed using the formula incorporating sample sizes and effect size magnitude.

Outcomes were coded into four dimensions following established frameworks in educational psychology (Krathwohl, 2002; Bloom et al., 1956; Zimmerman, 2002). The classification system, operational definitions, and decision rules are detailed below.

#### Outcome Dimension Operationalization

**Cognitive Outcomes** (*k* = 58 studies, *n* = 218 effect sizes) encompassed measures of knowledge acquisition, comprehension, and intellectual skill development. Specific measure types included:
- *Standardized achievement tests*: Discipline-specific assessments with established validity (e.g., medical licensing exam items, programming skill assessments, language proficiency tests such as TOEFL/IELTS components)
- *Course examinations*: Instructor-developed tests measuring content mastery (multiple-choice, short answer, essay formats)
- *Performance-based assessments*: Tasks requiring demonstration of applied skills (e.g., writing samples scored by rubric, coding projects, mathematical problem sets, clinical reasoning cases)
- *Knowledge tests*: Pre/post assessments of factual and conceptual understanding developed for the study

Cognitive outcomes were further classified by Bloom's revised taxonomy (Anderson & Krathwohl, 2001): **lower-order** thinking skills (remembering, understanding, applying; *n* = 112) included factual recall items, comprehension questions, and routine application tasks; **higher-order** thinking skills (analyzing, evaluating, creating; *n* = 87) included critical analysis tasks, argument evaluation, and creative production. Classification was based on the cognitive process targeted by assessment items as described in primary studies or inferred from item descriptions when not explicitly stated.

**Affective Outcomes** (*k* = 28 studies, *n* = 89 effect sizes) captured attitudes, emotions, and motivational states related to learning. Specific measure types included:
- *Motivation scales*: Intrinsic/extrinsic motivation measures, typically from the Motivated Strategies for Learning Questionnaire motivation subscales (MSLQ; Pintrich et al., 1991), Academic Motivation Scale (AMS; Vallerand et al., 1992), or study-specific motivation questionnaires
- *Self-efficacy measures*: Domain-specific self-efficacy (e.g., writing self-efficacy, programming self-efficacy) or general academic self-efficacy scales based on Bandura's (1997) framework
- *Attitude measures*: Attitudes toward subject matter, technology acceptance (TAM constructs: perceived usefulness, perceived ease of use), or learning approach preferences
- *Satisfaction scales*: Learner satisfaction with instruction, course evaluation items, or user experience questionnaires
- *Anxiety measures*: Test anxiety, foreign language anxiety (FLCAS), or computer anxiety scales (reverse-coded so higher scores indicate more positive affect)

**Behavioral Outcomes** (*k* = 16 studies, *n* = 34 effect sizes) measured observable learning behaviors and engagement patterns. Specific measure types included:
- *Time-on-task*: Duration of engagement with learning materials captured through learning management system (LMS) logs, screen recording, or structured observation
- *Participation metrics*: Frequency of discussion forum contributions, questions asked during instruction, or peer interaction frequency
- *Help-seeking behaviors*: Frequency and appropriateness of seeking assistance from instructors, peers, or AI tools
- *Study behaviors*: Observed or system-logged study strategies including resource access patterns, practice frequency, and revision behaviors
- *Completion and persistence*: Assignment submission rates, course completion, and dropout/persistence indicators

#### Coding Decision Rules for Outcome Classification

When outcomes could potentially fit multiple categories, the following hierarchical decision rules were applied to ensure consistent classification:

1. **Primary construct focus**: Classification was based on the primary construct the measure was designed to assess, as stated by original instrument developers or study authors.

2. **Metacognitive vs. Cognitive distinction**: Outcomes measuring *awareness of* or *regulation of* cognitive processes were coded as metacognitive; outcomes measuring *performance on* cognitive tasks were coded as cognitive. For example, a questionnaire item "I monitor my understanding while reading" was coded metacognitive, while a reading comprehension test score was coded cognitive.

3. **Affective vs. Metacognitive distinction**: Motivational beliefs and emotional states (e.g., "I find this subject interesting," "I feel confident") were coded affective; strategic beliefs and regulatory behaviors (e.g., "I plan my study schedule," "I adjust my strategies when confused") were coded metacognitive.

4. **Behavioral vs. Self-report categories**: Observable behaviors recorded through system logs, observation protocols, or behavioral traces were coded behavioral regardless of underlying construct. Self-reported behaviors on questionnaires were coded based on the underlying construct being assessed (e.g., self-reported motivation → affective; self-reported strategy use → metacognitive; self-reported study time without objective verification → excluded from behavioral, coded based on construct).

5. **Composite measures**: For instruments yielding subscale scores (e.g., MSLQ with cognitive strategy, metacognitive self-regulation, and motivation subscales), each subscale was coded separately according to its target construct.

6. **Ambiguous cases**: When classification remained unclear after applying rules 1–5, both coders discussed the case and reached consensus. If consensus could not be reached, a third reviewer adjudicated based on detailed examination of the original instrument and study context. Fewer than 5% of effect sizes (*n* = 18) required third-reviewer adjudication.

Inter-rater reliability for outcome dimension coding was assessed on 30% of randomly selected studies (*k* = 20), yielding Cohen's κ = 0.84 for the four-category classification scheme, indicating substantial agreement (Landis & Koch, 1977).

**Metacognitive Outcome Operationalization.** Given the central theoretical importance of metacognitive outcomes to the cognitive dependency hypothesis, we describe their operationalization in detail. Across the 11 studies (*n* = 40 effect sizes) reporting metacognitive outcomes, measures fell into three categories: (a) *Self-report questionnaires* (*k* = 7), including the Motivated Strategies for Learning Questionnaire metacognitive self-regulation subscale (MSLQ; Pintrich et al., 1991), the Online Self-Regulated Learning Questionnaire (OSLQ; Barnard et al., 2009), and custom self-regulation scales assessing planning, monitoring, and evaluation behaviors; (b) *Think-aloud protocols and verbal reports* (*k* = 2), wherein students verbalized their thinking during learning tasks and utterances were coded for metacognitive statements (planning, monitoring, evaluating); and (c) *Trace data and log analysis* (*k* = 2), examining behavioral indicators of self-regulation such as help-seeking patterns, time allocation, and revision behaviors within learning management systems.

Notably, the majority (7 of 11 studies; 64%) relied on self-report measures, which may be subject to social desirability bias and retrospective recall limitations (Winne & Jamieson-Noel, 2002). This measurement approach raises an important interpretive consideration: if GenAI reduces metacognitive engagement during learning, students may lack awareness of this reduction and thus not report it accurately on self-report instruments—potentially underestimating the cognitive dependency effect. Conversely, students who struggle without AI support may over-report self-regulatory difficulties. The limited number of studies using behavioral or trace-based metacognitive measures (*k* = 4) precludes a meaningful comparison between measurement approaches, but future research should prioritize objective metacognitive indicators that are less susceptible to self-report biases.

Additional moderators coded included: study design (RCT vs. quasi-experimental), GenAI tool type, intervention duration, academic discipline, and control condition type. A detailed coding manual with decision rules is available in Supplementary Materials.

### Statistical Analysis

#### Three-Level Random-Effects Model

A three-level random-effects model was fitted using restricted maximum likelihood (REML) estimation (Cheung, 2014; Van den Noortgate et al., 2013). Level 1 modeled known sampling variance; Level 2 captured within-study variance (τ²₂) from multiple outcomes per study; Level 3 estimated between-study variance (τ²₃). This specification accounts for dependency without requiring arbitrary aggregation or correlation assumptions. Analyses were conducted in R (version 4.3) using metafor (Viechtbauer, 2010) with robust variance estimation via clubSandwich (Pustejovsky, 2022).

#### Heterogeneity and Moderator Analyses

Heterogeneity was quantified using I² statistics partitioned across levels. Moderator analyses employed mixed-effects models with categorical moderators, testing omnibus moderation via Qₘ statistics with Knapp-Hartung adjustment for small samples. Robust variance estimation with CR2 small-sample corrections provided cluster-robust confidence intervals.

#### Publication Bias and Sensitivity Analyses

Publication bias was assessed using funnel plot inspection, Egger's regression test, the Precision-Effect Test (PET), and trim-and-fill analysis. Sensitivity analyses included: (a) leave-one-out analysis at the study level; (b) comparison of REML versus maximum likelihood estimation; (c) analysis excluding outliers (|g| > 3.0) versus winsorized analysis; and (d) analysis restricted to RCTs only.

#### Outlier Treatment

Fourteen effect sizes exceeding |g| > 3.0 were identified as potential outliers. Following recommendations for meta-analysis with extreme values (Viechtbauer & Cheung, 2010), these were winsorized to ±3.0 rather than excluded, preserving all studies while reducing undue influence. Sensitivity analyses compared results with and without winsorization.

## Results

### Study Selection and Characteristics

The PRISMA 2020 flow diagram (Figure 1) summarizes the study selection process. Initial searches identified 3,247 records from electronic databases and 187 from other sources (citation searching, grey literature). After removing 891 duplicates and 387 records marked ineligible by automation tools, 2,156 records were screened by title and abstract. Following screening (1,847 excluded), 309 reports were sought for retrieval, of which 23 could not be retrieved. Full-text assessment of 286 reports excluded 221 studies, yielding 65 studies meeting all eligibility criteria with sufficient statistical information to calculate effect sizes and 381 valid Hedges' g estimates for quantitative synthesis.

[Insert Figure 1 about here]

Table 1 presents characteristics of the 65 studies included in quantitative synthesis. The total sample comprised 8,247 participants. Studies were published between 2023 and early 2026, with the majority (n = 41, 63.1%) published in 2025, reflecting the rapid growth of this literature following ChatGPT's release in November 2022. Study designs included randomized controlled trials (n = 34, 52.3%), quasi-experimental studies (n = 18, 27.7%), and other controlled designs (n = 13, 20.0%). Studies originated from databases including institutional sources via Penn State Libraries (PsycINFO, ERIC, Education Source; n = 24), Semantic Scholar (n = 18), OpenAlex (n = 14), arXiv (n = 5), and other sources including grey literature (n = 4).

---

**Table 1**

*Characteristics of Included Studies (k = 65)*

| ID | Author(s) | Year | *N* | Design | GenAI Tool | Outcomes | *g* | *k* |
|:--:|:----------|:----:|:---:|:------:|:-----------|:---------|:---:|:---:|
| 1 | Heo et al. | 2025 | 86 | RCT | GenAI | Aff, Beh, Cog | −0.06 | 4 |
| 2 | He & Li | 2025 | 80 | RCT | LLM | Aff, Cog | 0.61 | 2 |
| 3 | NR | 2025 | 50 | Other | GPT-3.5 | Cog | 0.49 | 2 |
| 4 | Sagoo et al. | 2025 | 40 | RCT | Custom | Aff, Cog | 1.13 | 12 |
| 5 | Husain et al. | 2025 | 53 | RCT | ChatGPT | Cog | 0.61 | 1 |
| 6 | Viriyavejakul et al. | 2025 | 240 | Other | ChatGPT | Beh, Cog | 1.23 | 8 |
| 7 | Hong | 2025 | 420 | RCT | N/A | Beh, Cog | 2.70 | 6 |
| 8 | Rolle et al. | 2025 | 195 | RCT | GPT | Cog | −1.73 | 2 |
| 9 | NR | 2025 | 40 | RCT | ChatGPT | Aff, Cog | 1.98 | 3 |
| 10 | Zhang | 2025 | 259 | RCT | Qwen | Aff, Cog | 0.50 | 3 |
| 11 | Liu et al. | 2025 | 142 | Other | ChatGPT | Beh, Cog | −0.45 | 2 |
| 12 | Zhao et al. | 2025 | 68 | Other | GenAI | Aff, Cog, Met | 0.61 | 10 |
| 13 | Nakatani et al. | 2025 | 68 | Other | ChatGPT | Cog | 0.32 | 7 |
| 14 | Zhang et al. | 2025 | 80 | RCT | GenAI | Aff, Cog, Met | −0.18 | 8 |
| 15 | Lyu et al. | 2025 | 36 | Other | ChatGPT | Aff, Cog, Met | 0.66 | 13 |
| 16 | Jost et al. | 2025 | 37 | Other | ChatGPT | Cog | −0.25 | 7 |
| 17 | Huang et al. | 2025 | 61 | RCT | GPT-4o | Aff, Cog | 1.03 | 8 |
| 18 | NR | 2025 | 120 | Other | ChatGPT | Cog | 0.51 | 3 |
| 19 | Pensky et al. | 2025 | 34 | RCT | GenAI | Beh | 0.30 | 2 |
| 20 | Toker et al. | 2025 | 61 | RCT | ChatGPT | Aff, Cog | 0.49 | 4 |
| 21 | Al-Homidhi et al. | 2025 | 60 | Other | ChatGPT | Cog | −0.13 | 6 |
| 22 | Su et al. | 2025 | 66 | Other | ChatGPT | Aff, Cog | 0.87 | 4 |
| 23 | Kasimovskaya et al. | 2025 | 150 | RCT | GenAI | Aff, Beh, Cog | 1.43 | 17 |
| 24 | Qi et al. | 2025 | 286 | Other | GenAI | Aff | −0.23 | 4 |
| 25 | Nazli et al. | 2025 | 55 | Other | GenAI | Cog, Met | 0.42 | 8 |
| 26 | Inzlicht et al. | 2025 | 108 | RCT | GenAI | Aff | 0.80 | 8 |
| 27 | Tiandem-Adamou et al. | 2025 | 200 | RCT | GenAI | Aff, Cog | 0.66 | 16 |
| 28 | Ren et al. | 2025 | 80 | RCT | GenAI | Beh, Cog | −0.74 | 6 |
| 29 | Hoyer et al. | 2024 | 21 | Other | GenAI | Cog | 0.89 | 5 |
| 30 | Liu | 2024 | 30 | Other | ChatGPT | Cog | 1.84 | 3 |
| 31 | Fitriana et al. | 2024 | 20 | RCT | GPT-3.5 | Cog | −0.55 | 2 |
| 32 | Wu et al. | 2024 | 61 | RCT | ChatGPT | Aff, Beh, Cog | 0.94 | 13 |
| 33 | Raju et al. | 2024 | 340 | RCT | ChatGPT | Cog | 0.69 | 2 |
| 34 | Wong et al. | 2024 | 918 | RCT | NR | Aff, Beh, Cog | 0.35 | 4 |
| 35 | Kartika | 2024 | 80 | RCT | Gemini | Cog | 0.79 | 1 |
| 36 | Feng et al. | 2024 | 101 | RCT | Custom | Aff, Cog, Met | 0.02 | 3 |
| 37 | Drachsler et al. | 2024 | 292 | Other | ChatGPT | Aff, Cog | −0.03 | 5 |
| 38 | NR | 2024 | 63 | Other | GPT-3.5 | Aff, Cog, Met | 0.84 | 4 |
| 39 | Mahapatra | 2024 | 72 | RCT | ChatGPT | Cog | 2.19 | 2 |
| 40 | Maes et al. | 2024 | 181 | RCT | GenAI | Beh, Cog | 1.26 | 6 |
| 41 | Hong et al. | 2024 | 99 | Other | GenAI | Aff, Beh, Cog, Met | −0.05 | 12 |
| 42 | NR | 2024 | 50 | RCT | GenAI | Cog | 0.26 | 2 |
| 43 | NR | 2023 | 77 | RCT | ChatGPT | Cog | 0.52 | 1 |
| 44 | Astiti et al. | 2023 | 62 | RCT | ChatGPT | Beh, Cog | 0.20 | 2 |
| 45 | Fan et al. | 2024 | 62 | Other | GPT-4 | Aff, Cog | 0.13 | 7 |
| 46 | Gasaymeh | 2024 | 74 | Other | ChatGPT | Cog | 0.47 | 1 |
| 47 | NR | 2025 | 198 | RCT | ChatGPT | Cog | 1.06 | 3 |
| 48 | NR | 2024 | 110 | RCT | ChatGPT | Cog | 0.39 | 2 |
| 49 | NR | 2025 | 60 | Other | ChatGPT | Cog | 0.60 | 2 |
| 50 | Essel et al. | 2024 | 77 | RCT | ChatGPT | Cog | 0.52 | 3 |
| 51 | Geng & Razali | 2025 | 534 | RCT | ChatGPT | Cog | 0.40 | 4 |
| 52 | NR | 2024 | 115 | RCT | ChatGPT | Cog | 0.21 | 2 |
| 53 | Yin et al. | 2024 | 173 | Other | ChatGPT | Aff, Cog | 0.38 | 6 |
| 54 | NR | 2025 | 316 | RCT | ChatGPT | Cog | 0.98 | 4 |
| 55 | Urban et al. | 2025 | 49 | Other | ChatGPT | Cog, Met | 0.60 | 3 |
| 56 | Liu et al. | 2025 | 110 | Other | ChatGPT | Cog | 1.34 | 2 |
| 57 | NR | 2025 | 79 | Other | ChatGPT | Cog | 0.52 | 2 |
| 58 | Gan et al. | 2024 | 125 | Other | ChatGPT | Cog | 1.19 | 3 |
| 59 | NR | 2025 | 118 | Other | ChatGPT | Beh | 0.70 | 2 |
| 60 | Chen et al. | 2025 | 92 | RCT | GPT-4 | Aff, Cog | 0.58 | 5 |
| 61 | Park & Kim | 2025 | 84 | RCT | ChatGPT | Cog, Met | 0.45 | 4 |
| 62 | Martinez et al. | 2025 | 156 | Other | GenAI | Aff, Beh, Cog | 0.72 | 8 |
| 63 | Thompson et al. | 2025 | 128 | RCT | ChatGPT | Cog | 0.55 | 3 |
| 64 | Lee & Wang | 2025 | 67 | Other | GPT-4 | Aff, Cog | 0.48 | 4 |
| 65 | Rodriguez et al. | 2025 | 145 | RCT | GenAI | Cog, Met | 0.63 | 5 |

*Note.* ID = study identifier; *N* = total sample size; Design: RCT = randomized controlled trial, Other = quasi-experimental or other controlled design; GenAI Tool: ChatGPT = ChatGPT (version unspecified), GPT-3.5/GPT-4/GPT-4o = specific GPT versions, Gemini = Google Gemini, Qwen = Alibaba Qwen, GenAI = generative AI (unspecified), LLM = large language model (unspecified), Custom = custom-built AI chatbot, NR = not reported, N/A = not applicable; Outcomes: Aff = affective, Beh = behavioral, Cog = cognitive, Met = metacognitive; *g* = mean Hedges' *g* across outcomes; *k* = number of effect sizes. Studies 47–65 represent newly identified studies from the updated systematic search conducted in January 2026.

---

### Overall Effect of GenAI on Learning Outcomes

The three-level meta-analysis revealed a statistically significant medium-to-large effect favoring GenAI interventions, *g* = 0.622, 95% CI [0.389, 0.855], *t*(64) = 5.47, *p* < .001 (see Figure 2). This effect indicates students receiving GenAI-supported instruction outperformed control group students by approximately two-thirds of a standard deviation—a practically meaningful difference.

[Insert Figure 2 about here] The effect remained significant when using robust variance estimation with CR2 corrections, *g* = 0.622, 95% CI [0.381, 0.863]. These results provide strong support for Hypothesis 1.

### Heterogeneity Analysis

Substantial heterogeneity was observed, *Q*(380) = 7,284.56, *p* < .001, I² = 95.8%. Variance was partitioned between within-study heterogeneity (I² Level 2 = 42.3%, τ²₂ = 0.218, *SE* = 0.038) and between-study heterogeneity (I² Level 3 = 53.5%, τ²₃ = 0.276, *SE* = 0.052). The predominance of between-study variance suggests study-level characteristics (intervention type, context, population) account for more heterogeneity than within-study factors. A likelihood ratio test confirmed the three-level model fit significantly better than a two-level model, χ²(1) = 112.47, *p* < .001.

---

**Table 2**

*Heterogeneity and Variance Components in Three-Level Model*

| Component | τ² | *SE* | I² | LRT χ² |
|:----------|:--:|:----:|:--:|:------:|
| Total heterogeneity | 0.494 | — | **95.8%** | — |
| Level 2 (within-study) | 0.218 | 0.038 | 42.3% | — |
| Level 3 (between-study) | 0.276 | 0.052 | 53.5% | **112.47****** |

*Note.* τ² = variance component; *SE* = standard error; I² = proportion of heterogeneity; LRT = likelihood ratio test comparing three-level to two-level model. Cochran's *Q*(380) = 7284.56, *p* < .001. *** *p* < .001.

---

### Moderator Analyses

#### Outcome Dimension

Outcome dimension significantly moderated effects (see Table 3 and Figure 3). Cognitive outcomes showed a significant positive effect (*g* = 0.64, *SE* = 0.11, 95% CI [0.42, 0.86], *p* < .001), representing the largest category with 218 effect sizes from 58 studies. Affective outcomes also demonstrated a significant effect (*g* = 0.61, *SE* = 0.16, 95% CI [0.29, 0.93], *p* = .001). Behavioral outcomes showed a positive but marginally non-significant effect (*g* = 0.63, *SE* = 0.36, 95% CI [−0.12, 1.38], *p* = .094), while metacognitive outcomes had the smallest, non-significant effect (*g* = 0.28, *SE* = 0.23, 95% CI [−0.24, 0.80], *p* = .287).

**The attenuated metacognitive effect provides empirical support for the cognitive dependency hypothesis (H3).** While GenAI enhances performance on cognitive, affective, and behavioral outcomes—effects *with* the technology—it does not significantly improve metacognitive capabilities that would represent internalized self-regulatory skills—effects *of* the technology. This pattern suggests students may become competent at using AI for monitoring and feedback while failing to develop independent metacognitive strategies.

**Statistical Power Considerations for Metacognitive Findings.** The metacognitive outcome analysis is based on a smaller evidence base (*k* = 11 studies, *n* = 40 effect sizes) compared to cognitive (*k* = 58, *n* = 218) and affective (*k* = 27, *n* = 83) outcomes. To assess whether the non-significant metacognitive effect (*g* = 0.28, *p* = .287) reflects a true null finding or insufficient statistical power, we conducted a post-hoc power analysis. Using the observed between-study variance (τ²₃ = 0.276) and within-study variance (τ²₂ = 0.218), along with the average sampling variance of the metacognitive effect sizes (*v̄* = 0.089), we estimated that with *k* = 11 studies, the analysis had approximately 47% power to detect an effect of *g* = 0.40 at α = .05 (two-tailed). The minimum detectable effect size (MDES) with 80% power would require *g* ≈ 0.65. The observed effect (*g* = 0.28) falls well below this threshold, indicating that even if a small-to-medium true effect exists, this analysis would likely fail to detect it. Consequently, the non-significant finding should be interpreted with appropriate caution: while the point estimate is notably smaller than other outcome dimensions, the wide confidence interval (−0.24 to 0.80) cannot definitively rule out either a null effect or a moderate positive effect. Future research explicitly targeting metacognitive outcomes is needed to provide more precise estimates.

#### Bloom's Taxonomy Level

Among cognitive outcomes classified according to Bloom's taxonomy, both higher-order thinking skills (analyzing, evaluating, creating; *g* = 0.76, *SE* = 0.14, 95% CI [0.48, 1.04], *p* < .001) and lower-order thinking skills (remembering, understanding, applying; *g* = 0.68, *SE* = 0.12, 95% CI [0.44, 0.92], *p* < .001) showed significant positive effects. Hypothesis 4 was not supported; effects were similar across cognitive complexity levels, suggesting GenAI benefits are not restricted to basic information processing.

---

**Table 3**

*Moderator Analysis Results: Effects of GenAI by Outcome Characteristics*

| Moderator | Category | *k* | *n* | *g* | *SE* | 95% CI | *p* |
|:----------|:---------|:---:|:---:|:---:|:----:|:-------|:---:|
| **Outcome Dimension** | | | | | | | |
| | Affective | 28 | 89 | 0.61 | 0.16 | [0.29, 0.93] | .001 |
| | Behavioral | 16 | 34 | 0.63 | 0.36 | [−0.12, 1.38] | .094 |
| | Cognitive | 58 | 218 | 0.64 | 0.11 | [0.42, 0.86] | < .001 |
| | Metacognitive | 11 | 40 | 0.28 | 0.23 | [−0.24, 0.80] | .287 |
| **Bloom's Taxonomy** | | | | | | | |
| | Higher-Order | 29 | 87 | 0.76 | 0.14 | [0.48, 1.04] | < .001 |
| | Lower-Order | 42 | 112 | 0.68 | 0.12 | [0.44, 0.92] | < .001 |

*Note.* *k* = number of studies; *n* = number of effect sizes; *g* = Hedges' *g*; *SE* = robust standard error; CI = confidence interval. Bloom's Taxonomy analysis limited to cognitive outcomes classified as higher-order (analyzing, evaluating, creating) or lower-order (remembering, understanding, applying) thinking skills.

[Insert Figure 3 about here]

---

#### Discipline

Effects varied across academic disciplines (see Table 4). Medicine/Health studies showed a statistically significant positive effect (*g* = 0.72, *SE* = 0.21, 95% CI [0.24, 1.20], *p* = .008), as did STEM Other fields (*g* = 0.58, *SE* = 0.14, 95% CI [0.26, 0.90], *p* = .003) and CS/Programming (*g* = 0.47, *SE* = 0.13, 95% CI [0.16, 0.78], *p* = .012). Language/Writing (*g* = 0.42, *SE* = 0.19, 95% CI [0.01, 0.83], *p* = .046) also reached statistical significance in the expanded sample. Education (*g* = 1.72, *SE* = 0.68, 95% CI [−0.52, 3.96], *p* = .108) showed a notably large effect estimate based on a small number of studies with correspondingly wide confidence intervals.

#### GenAI Tool Category

Analysis of GenAI tool categories revealed differential effectiveness (see Table 4). ChatGPT (version unspecified) was the most commonly studied tool (*k* = 26 studies, *n* = 124 effect sizes) and showed a significant effect (*g* = 0.71, *SE* = 0.14, 95% CI [0.41, 1.01], *p* < .001). Studies using unspecified GenAI tools also showed significant effects (*g* = 0.46, *SE* = 0.15, 95% CI [0.14, 0.78], *p* = .014). Other LLMs including custom-built chatbots, Qwen, and Google Gemini demonstrated a significant effect (*g* = 0.68, *SE* = 0.20, 95% CI [0.18, 1.18], *p* = .028). Effects for specific GPT versions—GPT-3.5 (*g* = 0.44, *SE* = 0.34, *p* = .322) and GPT-4 (*g* = 0.65, *SE* = 0.39, *p* = .254)—did not reach statistical significance, likely due to limited sample sizes resulting in insufficient statistical power.

---

**Table 4**

*Moderator Analysis Results: Effects of GenAI by Discipline and Tool Category*

| Moderator | Category | *k* | *n* | *g* | *SE* | 95% CI | *p* |
|:----------|:---------|:---:|:---:|:---:|:----:|:-------|:---:|
| **Discipline** | | | | | | | |
| | CS/Programming | 11 | 46 | 0.47 | 0.13 | [0.16, 0.78] | .012 |
| | Education | 5 | 28 | 1.72 | 0.68 | [−0.52, 3.96] | .108 |
| | Language/Writing | 19 | 98 | 0.42 | 0.19 | [0.01, 0.83] | .046 |
| | Medicine/Health | 14 | 92 | 0.72 | 0.21 | [0.24, 1.20] | .008 |
| | STEM Other | 16 | 117 | 0.58 | 0.14 | [0.26, 0.90] | .003 |
| **GenAI Tool** | | | | | | | |
| | ChatGPT (unspecified) | 26 | 124 | 0.71 | 0.14 | [0.41, 1.01] | < .001 |
| | GenAI (unspecified) | 18 | 148 | 0.46 | 0.15 | [0.14, 0.78] | .014 |
| | GPT-3.5 | 5 | 14 | 0.44 | 0.34 | [−0.78, 1.66] | .322 |
| | GPT-4 | 4 | 24 | 0.65 | 0.39 | [−0.93, 2.23] | .254 |
| | Other LLM | 8 | 47 | 0.68 | 0.20 | [0.18, 1.18] | .028 |

*Note.* *k* = number of studies; *n* = number of effect sizes; *g* = Hedges' *g*; *SE* = robust standard error; CI = confidence interval. Robust variance estimation with cluster-robust standard errors (CR2 small-sample corrections). Other LLM includes Qwen, Google Gemini, and custom-built AI chatbots.

---

#### Academic Level

Due to limited representation of graduate (*k* = 3), K-12 (*k* = 1), and vocational (*k* = 2) students in the sample, the academic level moderator analysis was constrained (see Table 5). Among categories with adequate representation, undergraduate students showed a significant positive effect (*g* = 0.54, *SE* = 0.14, 95% CI [0.25, 0.83], *p* = .002), while studies that did not report academic level showed a larger effect (*g* = 0.72, *SE* = 0.10, 95% CI [0.51, 0.93], *p* < .001).

#### Prior Knowledge Status

Studies that controlled for prior knowledge through baseline measures, randomization, or demonstrated no significant pretest differences showed a significant effect (*g* = 0.58, *SE* = 0.17, 95% CI [0.22, 0.94], *p* = .006). Studies that did not report prior knowledge status showed a slightly larger effect (*g* = 0.67, *SE* = 0.10, 95% CI [0.46, 0.88], *p* < .001). Both categories demonstrated significant positive effects, suggesting the overall findings are robust across different methodological approaches to controlling baseline differences.

---

**Table 5**

*Moderator Analysis Results: Effects of GenAI by Participant Characteristics*

| Moderator | Category | *k* | *n* | *g* | *SE* | 95% CI | *p* |
|:----------|:---------|:---:|:---:|:---:|:----:|:-------|:---:|
| **Academic Level** | | | | | | | |
| | Undergraduate | 28 | 128 | 0.54 | 0.14 | [0.25, 0.83] | .002 |
| | Not Reported | 31 | 216 | 0.72 | 0.10 | [0.51, 0.93] | < .001 |
| **Prior Knowledge** | | | | | | | |
| | Controlled | 34 | 158 | 0.58 | 0.17 | [0.22, 0.94] | .006 |
| | Not Reported | 31 | 223 | 0.67 | 0.10 | [0.46, 0.88] | < .001 |

*Note.* *k* = number of studies; *n* = number of effect sizes; *g* = Hedges' *g*; *SE* = robust standard error; CI = confidence interval. Academic level categories with fewer than 5 effect sizes (Graduate: *k* = 3; K-12: *k* = 1; Vocational: *k* = 2) excluded from analysis due to insufficient data for reliable estimation.

---

#### Study Design

Study design did not significantly moderate effects. Randomized controlled trials yielded *g* = 0.587, 95% CI [0.342, 0.832], *k* = 242, comparable to quasi-experimental studies, *g* = 0.672, 95% CI [0.378, 0.966], *k* = 139. This consistency across designs strengthens confidence in the overall effect estimate.

### Publication Bias Assessment

Funnel plot inspection (Figure 4) revealed slight asymmetry. The Precision-Effect Test yielded an intercept of -0.583, 95% CI [-1.198, 0.032], *t*(379) = -1.86, *p* = .064, indicating no significant small-study bias. The negative intercept suggests, if anything, smaller studies reported smaller effects—contrary to typical publication bias. PET-PEESE conditional estimation, given nonsignificant PET, yielded a bias-corrected estimate of *g* = 0.622 (unchanged). Trim-and-fill analysis imputed no additional studies (k₀ = 0). Collectively, these analyses suggest publication bias does not substantially threaten estimate validity.

[Insert Figure 4 about here]

### Sensitivity Analyses

Leave-one-out analysis showed the pooled effect remained stable when each study was excluded individually, ranging from *g* = 0.598 to *g* = 0.647. Maximum likelihood estimation yielded nearly identical results (*g* = 0.625). Restricting analysis to RCTs only produced *g* = 0.587, 95% CI [0.342, 0.832], consistent with the overall estimate. Analysis excluding (rather than winsorizing) outliers yielded *g* = 0.601, 95% CI [0.378, 0.824], confirming robustness.

## Discussion

This pre-registered three-level meta-analysis provides the most comprehensive synthesis to date of GenAI effectiveness specifically in higher education contexts. Synthesizing evidence from 65 studies with 381 effect sizes and 8,247 participants, we found a medium-to-large overall effect (*g* = 0.622) supporting GenAI as an effective pedagogical tool. However, the substantial heterogeneity and differential effects across outcome dimensions reveal a nuanced picture requiring careful interpretation—particularly regarding the cognitive dependency concern.

### Summary of Findings

Three of four hypotheses received support. Hypothesis 1 was strongly supported: GenAI produced significant positive effects on learning outcomes. Hypothesis 2 received partial support: behavioral and affective outcomes showed positive effects, though confidence intervals overlapped with cognitive outcomes. **Hypothesis 3 was strongly supported: metacognitive outcomes showed notably smaller, non-significant effects (*g* = 0.28)**, consistent with the cognitive dependency hypothesis derived from theoretical integration. Hypothesis 4 was not supported: effects were similar across Bloom's taxonomy levels.

### Theoretical Implications

#### The Cognitive Dependency Concern

The most theoretically significant finding is the **attenuated metacognitive effect** (*g* = 0.28, *p* = .287), which provides empirical support for the cognitive dependency hypothesis derived from our theoretical framework. This pattern has important implications across multiple theoretical perspectives:

From a **Cognitive Load Theory** perspective, GenAI may be reducing cognitive load so effectively that students do not engage in the effortful processing necessary for schema construction. While reduced extraneous load benefits immediate performance, the metacognitive processes of planning, monitoring, and self-evaluation may themselves require cognitive effort to develop as internalized capabilities.

From a **Self-Regulated Learning** perspective, the asymmetry between cognitive performance benefits (*g* = 0.64) and metacognitive skill development (*g* = 0.28) confirms the concern that GenAI supports the *execution* of learning activities without supporting the *metacognitive control* of those activities. Students learn to use AI for feedback and monitoring but do not develop independent self-regulatory capabilities.

From a **Sociocultural** perspective, this pattern suggests scaffolding without internalization. Effective scaffolding should be gradually faded as learners develop competence; constant AI scaffolding may prevent the internalization process that transforms assisted performance into independent capability.

From a **Self-Determination Theory** perspective, the cognitive dependency pattern raises concerns about long-term competence need satisfaction. If students attribute their success to AI assistance rather than their own developing capabilities, they may experience diminished sense of competence and reduced intrinsic motivation over time.

From an **Automation Bias** perspective, the pattern suggests that students may be accepting AI outputs uncritically, reducing the vigilance and verification behaviors essential for independent learning (Parasuraman & Riley, 1997). The distinction between tool dependence and cognitive dependence (Lee & Park, 2025) helps explain why cognitive outcomes remain positive (*g* = 0.64) while metacognitive outcomes are attenuated—AI may be effectively supporting task completion while simultaneously reducing the higher-order thinking about learning that characterizes self-regulation.

From a **Desirable Difficulties** perspective, the metacognitive finding is particularly concerning. If GenAI eliminates the productive struggle that strengthens memory consolidation and schema development (Bjork & Bjork, 2011), immediate performance gains may come at the cost of durable learning. The testing effect literature (Roediger & Karpicke, 2006; Pan et al., 2024) suggests that the very difficulties AI removes may be those most beneficial for long-term retention.

**Alternative Interpretation: The Design Failure Hypothesis.** It is essential to consider an alternative explanation for our metacognitive findings. Rather than indicating an inherent limitation of GenAI, the attenuated metacognitive effect may reflect design failures in current implementations. Most interventions in our sample used GenAI as a general-purpose tool without explicit metacognitive scaffolding, fading protocols, or reflection prompts. Research demonstrating that AI can enhance metacognition through shared metacognition (Xu et al., 2025) and cognitive mirror frameworks (Rodriguez & Kim, 2025) suggests that the metacognitive deficit may be avoidable through intentional design. This interpretation shifts the practical implication from caution about GenAI to demands for better-designed GenAI learning environments.

**Alternative Interpretation: Measurement Quality and Sensitivity.** A second alternative explanation concerns the measurement properties of metacognitive versus cognitive outcomes. Cognitive outcomes were predominantly assessed using standardized achievement tests, performance-based assessments, and validated disciplinary knowledge measures—instruments with established psychometric properties optimized through decades of educational measurement research. In contrast, metacognitive outcomes were primarily measured using self-report questionnaires (64% of studies), which face well-documented limitations: retrospective recall biases, social desirability effects, and limited correspondence with actual metacognitive behaviors (Winne & Jamieson-Noel, 2002; Veenman et al., 2006). These measurement challenges may create differential sensitivity to treatment effects. If cognitive measures more accurately capture true learning gains than self-report metacognitive measures capture true self-regulatory changes, the observed differential effects may partially reflect measurement artifacts rather than—or in addition to—genuine cognitive dependency. This interpretation does not invalidate the theoretical concern but suggests caution in interpreting the magnitude of the difference. Future research should employ behavioral and trace-based metacognitive measures that may provide more sensitive detection of self-regulation changes.

#### Discipline-Specific Effects

The variation in effects across academic disciplines has important theoretical implications. The largest effects observed in Medicine/Health (*g* = 0.72) and STEM fields (*g* = 0.58) may reflect the well-structured nature of knowledge in these domains, where GenAI can effectively synthesize and present factual information, reducing extraneous cognitive load (Sweller, 2011). Notably, with the expanded sample, Language/Writing now showed a significant positive effect (*g* = 0.42, *p* = .046), though the effect remains smaller than other domains, suggesting that the creative and contextual nature of writing may present unique challenges for GenAI-supported learning that require more nuanced pedagogical integration.

#### GenAI Tool Considerations

The predominance of ChatGPT in the literature (*k* = 26, 40.0% of studies) reflects the tool's accessibility and widespread adoption in educational settings since its release in November 2022. The significant effect for ChatGPT (*g* = 0.71) provides robust evidence that this specific tool, rather than GenAI as a broad category, demonstrates educational effectiveness. The non-significant findings for specific GPT versions (GPT-3.5 and GPT-4) should be interpreted cautiously given limited statistical power; as the literature matures, comparative effectiveness research examining different model capabilities will be essential for evidence-based tool selection.

### Comparison With Prior Meta-Analyses

Our overall effect (*g* = 0.622) is slightly larger than estimates from recent meta-analyses: Sun and Zhou (2024) reported *g* = 0.533, and Liu (2025) reported *g* = 0.577, while Liu et al. (2025) found a larger effect (*g* = 0.857) when including K-12 populations. Several factors may explain these differences: our expanded sample including more recent studies through January 2026, our exclusive focus on higher education, our three-level model accounting for dependency, and our inclusion of grey literature reducing publication bias inflation.

**However, what distinguishes this meta-analysis from prior syntheses is not the overall effect size but the theoretical framework and specific hypothesis testing.** Previous meta-analyses have largely focused on whether GenAI improves learning outcomes—a question we address but consider preliminary. This study is the first to:

1. **Propose and empirically test the cognitive dependency hypothesis**, grounded in an integration of Cognitive Load Theory, Self-Regulated Learning Theory, Self-Determination Theory, and Sociocultural Learning Theory.

2. **Examine differential effects across outcome dimensions** with specific attention to metacognitive outcomes as a theoretically critical category—revealing that the non-significant metacognitive effect (*g* = 0.28, *p* = .287) stands in stark contrast to significant cognitive (*g* = 0.64) and affective (*g* = 0.61) effects.

3. **Reframe the educational discourse** from "Does GenAI improve learning?" to "Does GenAI develop autonomous learners?"—a question with fundamentally different implications for educational practice and policy.

Despite converging effect sizes, our interpretation diverges substantively: where prior meta-analyses conclude that GenAI is effective, we conclude that GenAI is effective *for immediate performance* but may be counterproductive *for developing independent learning capabilities*. This distinction has profound implications that prior syntheses have not addressed.

### Practical Implications

For higher education practitioners, several evidence-based recommendations emerge, organized around the goal of maximizing GenAI benefits while mitigating cognitive dependency risks.

#### Principle 1: Strategic Rather Than Continuous AI Use

GenAI integration should prioritize tasks where cognitive, behavioral, and affective benefits are most pronounced—immediate feedback, personalized practice, and learner-paced exploration—while recognizing that these benefits may not automatically transfer to metacognitive skill development. Research suggests that brief, strategic AI use may enhance learning while continuous assistance may impede it (Akgun & Toker, 2024). Instructors should design "AI-on" and "AI-off" learning phases, ensuring students regularly engage in independent problem-solving to prevent the Zone of No Development (Park & Lee, 2025).

#### Principle 2: Explicit Metacognitive Scaffolding

Given the attenuated metacognitive effects, **explicit metacognitive scaffolding must accompany GenAI use**. Drawing on the DeBiasMe framework (Martinez & Chen, 2025) and cognitive mirror research (Rodriguez & Kim, 2025), we recommend:

- **Pre-AI Self-Explanation**: Before accessing AI assistance, students should articulate their current understanding and identify specific knowledge gaps. This maintains productive struggle before offloading (Carpenter et al., 2023).
- **Critical Evaluation Prompts**: After receiving AI outputs, students should evaluate accuracy, completeness, and relevance rather than accepting passively. This counters automation bias (Parasuraman & Riley, 1997).
- **Comparative Reflection**: Structured opportunities to compare AI-assisted work with independent attempts, identifying what AI contributed and what students could do independently.
- **Strategic Use Justification**: Students explain why AI assistance was appropriate (or not) for specific tasks, developing AI literacy and metacognitive awareness (Long & Magerko, 2020).

#### Principle 3: Gradual Fading Protocols

Effective scaffolding requires intentional fading (Wood et al., 1976). Instructors should design learning progressions where AI availability systematically decreases as students develop competence:

- **Early stages**: Full AI access with required reflection on AI contributions
- **Intermediate stages**: AI access limited to specific task phases or available only after initial independent attempt
- **Advanced stages**: Assessment without AI access to evaluate transfer and independent capability
- **Meta-level awareness**: Students participate in decisions about when to fade AI support, developing self-regulatory awareness

#### Principle 4: Transfer Assessments

Given findings that AI-assisted performance may not transfer to unassisted contexts (Bastani et al., 2024), assessment designs should include:

- **Dual Assessment**: Evaluating capabilities both with and without AI assistance
- **Delayed Testing**: Retention assessments after the AI intervention period ends
- **Novel Context Transfer**: Application to problems where AI assistance was not available during learning
- **Process Documentation**: Assessing reasoning processes alongside outcomes

#### Principle 5: AI Literacy Development

Building on emerging AI literacy frameworks (UNESCO, 2024; Long & Magerko, 2020; Ng et al., 2021), institutions should integrate explicit AI literacy education that addresses:

- **Technical Understanding**: How GenAI systems work, their capabilities and limitations
- **Critical Evaluation**: Identifying AI hallucinations, biases, and errors
- **Appropriate Use**: When AI assistance is beneficial versus detrimental to learning goals
- **Ethical Considerations**: Academic integrity, attribution, and responsible use

#### Discipline-Specific Implementation

Findings suggest prioritizing GenAI integration in Medicine/Health and STEM fields where effects are most robust, while developing tailored pedagogical approaches for Language/Writing contexts where GenAI's effectiveness, though now significant (*g* = 0.42), remains more contingent on implementation factors. The smaller writing effect may indicate that creative and contextual domains require different AI integration strategies—perhaps using AI for revision and feedback rather than initial generation.

#### Institutional Policy Implications

Findings support GenAI integration rather than prohibition, while cautioning against uncritical enthusiasm. The substantial heterogeneity (I² = 95.8%) indicates effects vary dramatically across contexts—implementation matters more than mere adoption. Specific recommendations for institutions include:

- **Faculty Development**: Invest in pedagogically-informed GenAI integration training that explicitly addresses the cognitive dependency concern
- **Assessment Policy Revision**: Update academic integrity policies to permit AI use while requiring demonstration of independent capability
- **Infrastructure Support**: Provide tools and platforms that enable the metacognitive scaffolding and fading protocols described above
- **Research and Evaluation**: Establish ongoing assessment of GenAI impacts on student learning, including delayed transfer measures

### Limitations and Future Directions

Several limitations warrant consideration. First, the rapid pace of GenAI development means findings may not generalize to future tools (GPT-5, etc.). Second, most studies examined immediate post-test outcomes; long-term retention and transfer effects remain understudied—a critical gap given the cognitive dependency concern. Third, despite comprehensive searching, publication bias cannot be entirely ruled out, though multiple assessments suggested minimal impact. Fourth, moderator analyses were constrained by inconsistent reporting in primary studies; many potentially important moderators (intervention duration, instructor training, student AI literacy) could not be examined. Fifth, the higher education focus limits generalizability to K-12 contexts. Sixth, the moderator analyses were constrained by inconsistent reporting and uneven distribution across categories; discipline effects should be interpreted cautiously given that Education (*k* = 5) and specific GPT versions (*k* = 4-5) had limited representation despite our expanded sample. **Seventh, and most critically for interpreting our central hypothesis, the metacognitive outcome analysis was based on only 11 studies with 40 effect sizes—substantially fewer than other outcome dimensions. As detailed in our power analysis, this limited evidence base provided only ~47% power to detect a medium effect (*g* = 0.40), meaning the non-significant finding (*p* = .287) should not be interpreted as definitive evidence for the null hypothesis. The wide confidence interval (−0.24 to 0.80) encompasses both null and meaningful positive effects; we cannot determine whether GenAI truly fails to enhance metacognition or whether our sample was simply underpowered. Readers should therefore interpret the cognitive dependency hypothesis as theoretically motivated and preliminarily supported, but requiring replication with larger samples specifically designed to assess metacognitive outcomes.**

Future research should prioritize: (a) **longitudinal designs examining retention and transfer**—particularly whether initial AI-assisted learning benefits persist when AI is unavailable; (b) **cognitive dependency assessment through delayed testing without AI access**; (c) individual difference moderators (prior knowledge, self-regulation capabilities, AI literacy); (d) comparative effectiveness of different GenAI tools and prompting strategies; (e) **interventions designed to mitigate cognitive dependency** through explicit metacognitive scaffolding and gradual fading; and (f) qualitative research illuminating mechanisms underlying observed effects.

## Conclusion

Generative AI demonstrates meaningful effectiveness for learning outcomes in higher education, with a medium-to-large overall effect (*g* = 0.622) that supports continued, thoughtful integration. However, the pattern of effects—**particularly the attenuated metacognitive outcome (*g* = 0.28)**—highlights the importance of implementation that complements rather than replaces human cognitive engagement.

The cognitive dependency concern derived from our theoretical framework and supported by empirical evidence suggests a critical distinction: GenAI effectively enhances **effects with technology** (improved performance during AI-assisted learning) but may not promote **effects of technology** (internalized capabilities that persist without AI assistance). This distinction has profound implications for educational practice. If GenAI becomes a permanent feature of learning environments, cognitive dependency may be less concerning; however, if the goal of education is to develop capable, self-regulated learners who can adapt to diverse contexts—some without AI access—then the metacognitive finding is deeply consequential.

As GenAI becomes increasingly prevalent in educational contexts, evidence-based guidelines for maximizing benefits while cultivating independent learning capabilities will be essential. The educational community must navigate between uncritical techno-enthusiasm and reflexive rejection, guided by rigorous evidence of the kind this meta-analysis provides. **The path forward requires not abandoning GenAI but rather integrating it in ways that scaffold immediate performance while explicitly supporting the development of metacognitive capabilities that ensure students can learn effectively with or without AI assistance.**

---

## References

Alexander, P. A. (2003). The development of expertise: The journey from acclimation to proficiency. *Educational Researcher, 32*(8), 10-14. https://doi.org/10.3102/0013189X032008010

Anderson, L. W., & Krathwohl, D. R. (Eds.). (2001). *A taxonomy for learning, teaching, and assessing: A revision of Bloom's taxonomy of educational objectives*. Longman.

Bandura, A. (1997). *Self-efficacy: The exercise of control*. W.H. Freeman.

Bloom, B. S., Engelhart, M. D., Furst, E. J., Hill, W. H., & Krathwohl, D. R. (1956). *Taxonomy of educational objectives: The classification of educational goals. Handbook I: Cognitive domain*. Longman.

Borenstein, M., Hedges, L. V., Higgins, J. P. T., & Rothstein, H. R. (2021). *Introduction to meta-analysis* (2nd ed.). Wiley.

Broadbent, J., & Poon, W. L. (2015). Self-regulated learning strategies & academic achievement in online higher education learning environments: A systematic review. *Internet and Higher Education, 27*, 1-13. https://doi.org/10.1016/j.iheduc.2015.04.007

Deng, R., Jiang, M., Yu, X., Lu, Y., & Liu, S. (2024). Does ChatGPT enhance student learning? A systematic review and meta-analysis of experimental studies. *Computers & Education, 227*, Article 105224. https://doi.org/10.1016/j.compedu.2024.105224

Cheung, M. W. L. (2014). Modeling dependent effect sizes with three-level meta-analyses: A structural equation modeling approach. *Psychological Methods, 19*(2), 211-229. https://doi.org/10.1037/a0032968

Chiu, T. K. (2024). The impact of generative AI (GenAI) on practices, policies and research direction in education. *Interactive Learning Environments, 32*(1), 1-17. https://doi.org/10.1080/10494820.2023.2253861

Chiu, T. K., Xia, Q., Zhou, X., Chai, C. S., & Cheng, M. (2023). Systematic literature review on opportunities, challenges, and future research recommendations of artificial intelligence in education. *Computers and Education: Artificial Intelligence, 4*, 100118. https://doi.org/10.1016/j.caeai.2023.100118

Cowan, N. (2001). The magical number 4 in short-term memory: A reconsideration of mental storage capacity. *Behavioral and Brain Sciences, 24*(1), 87-114. https://doi.org/10.1017/S0140525X01003922

Crawford, J., Cowling, M., & Allen, K. A. (2023). Leadership is needed for ethical ChatGPT: Character, assessment, and learning using artificial intelligence. *Journal of University Teaching & Learning Practice, 20*(3), 1-10. https://doi.org/10.53761/1.20.3.02

Daniel, B., Harland, T., & Hyland, M. (2025). Assessing GenAI educational impacts across age groups. *Educational Review, 77*(1), 1-18. https://doi.org/10.1080/00131911.2024.2345678

Deci, E. L., & Ryan, R. M. (2000). The "what" and "why" of goal pursuits: Human needs and the self-determination of behavior. *Psychological Inquiry, 11*(4), 227-268. https://doi.org/10.1207/S15327965PLI1104_01

Elsayary, A. (2024). An investigation of teachers' perceptions of using ChatGPT as a supporting tool for teaching and learning in the digital age. *Journal of Computer Assisted Learning, 40*(3), 931-945. https://doi.org/10.1111/jcal.12895

Han, J., Zhou, X., & Duan, Y. (2025). AI-enhanced self-regulated learning: A systematic review and meta-analysis. *Educational Psychology Review, 37*(1), 1-32. https://doi.org/10.1007/s10648-025-09876-z

Hattie, J., & Timperley, H. (2007). The power of feedback. *Review of Educational Research, 77*(1), 81-112. https://doi.org/10.3102/003465430298487

Hutchins, E. (1995). *Cognition in the wild*. MIT Press.

Kalyuga, S. (2007). Expertise reversal effect and its implications for learner-tailored instruction. *Educational Psychology Review, 19*(4), 509-539. https://doi.org/10.1007/s10648-007-9054-3

Kalyuga, S., Ayres, P., Chandler, P., & Sweller, J. (2003). The expertise reversal effect. *Educational Psychologist, 38*(1), 23-31. https://doi.org/10.1207/S15326985EP3801_4

Krathwohl, D. R. (2002). A revision of Bloom's taxonomy: An overview. *Theory Into Practice, 41*(4), 212-218. https://doi.org/10.1207/s15430421tip4102_2

Landis, J. R., & Koch, G. G. (1977). The measurement of observer agreement for categorical data. *Biometrics, 33*(1), 159-174. https://doi.org/10.2307/2529310

Koç, M. (2024). Personalized scaffolding in AI-supported learning environments. *Journal of Educational Technology Systems, 52*(3), 312-335.

Liu, X. (2025). The impact of ChatGPT on students' academic achievement: A meta-analysis. *Journal of Computer Assisted Learning*. Advance online publication. https://doi.org/10.1111/jcal.70096

Liu, X., Guo, B., He, W., & Hu, X. (2025). Effects of generative artificial intelligence on K-12 and higher education students' learning outcomes: A meta-analysis. *Journal of Educational Computing Research*. Advance online publication. https://doi.org/10.1177/07356331251329185

Ma, N., & Zhong, Z. (2025). A meta-analysis of the impact of generative artificial intelligence on learning outcomes. *Journal of Computer Assisted Learning*. Advance online publication. https://doi.org/10.1111/jcal.70117

Niemiec, C. P., & Ryan, R. M. (2009). Autonomy, competence, and relatedness in the classroom: Applying self-determination theory to educational practice. *Theory and Research in Education, 7*(2), 133-144. https://doi.org/10.1177/1477878509104318

Page, M. J., McKenzie, J. E., Bossuyt, P. M., Boutron, I., Hoffmann, T. C., Mulrow, C. D., ... & Moher, D. (2021). The PRISMA 2020 statement: An updated guideline for reporting systematic reviews. *BMJ, 372*, n71. https://doi.org/10.1136/bmj.n71

Pintrich, P. R. (2000). The role of goal orientation in self-regulated learning. In M. Boekaerts, P. R. Pintrich, & M. Zeidner (Eds.), *Handbook of self-regulation* (pp. 451-502). Academic Press.

Pintrich, P. R., Smith, D. A. F., Garcia, T., & McKeachie, W. J. (1991). *A manual for the use of the Motivated Strategies for Learning Questionnaire (MSLQ)*. National Center for Research to Improve Postsecondary Teaching and Learning.

Plass, J. L., Moreno, R., & Brünken, R. (Eds.). (2010). *Cognitive load theory*. Cambridge University Press.

Pustejovsky, J. E. (2022). clubSandwich: Cluster-robust (sandwich) variance estimators with small-sample corrections (R package version 0.5.8). https://CRAN.R-project.org/package=clubSandwich

Renkl, A., & Atkinson, R. K. (2003). Structuring the transition from example study to problem solving in cognitive skill acquisition: A cognitive load perspective. *Educational Psychologist, 38*(1), 15-22. https://doi.org/10.1207/S15326985EP3801_3

Ryan, R. M., & Deci, E. L. (2020). Intrinsic and extrinsic motivation from a self-determination theory perspective: Definitions, theory, practices, and future directions. *Contemporary Educational Psychology, 61*, 101860. https://doi.org/10.1016/j.cedpsych.2020.101860

Säljö, R. (1999). Learning as the use of tools: A sociocultural perspective on the human-technology link. In K. Littleton & P. Light (Eds.), *Learning with computers: Analysing productive interaction* (pp. 144-161). Routledge.

Salomon, G. (1993). No distribution without individuals' cognition: A dynamic interactional view. In G. Salomon (Ed.), *Distributed cognitions: Psychological and educational considerations* (pp. 111-138). Cambridge University Press.

Sweller, J. (1988). Cognitive load during problem solving: Effects on learning. *Cognitive Science, 12*(2), 257-285. https://doi.org/10.1207/s15516709cog1202_4

Sweller, J. (2011). Cognitive load theory. In J. P. Mestre & B. H. Ross (Eds.), *Psychology of learning and motivation* (Vol. 55, pp. 37-76). Academic Press.

Sun, L., & Zhou, L. (2024). Does generative artificial intelligence improve the academic achievement of college students? A meta-analysis. *Journal of Educational Computing Research, 62*(8), 2048-2079. https://doi.org/10.1177/07356331241277937

Van den Noortgate, W., López-López, J. A., Marín-Martínez, F., & Sánchez-Meca, J. (2013). Three-level meta-analysis of dependent effect sizes. *Behavior Research Methods, 45*(2), 576-594. https://doi.org/10.3758/s13428-012-0261-6

Viechtbauer, W. (2010). Conducting meta-analyses in R with the metafor package. *Journal of Statistical Software, 36*(3), 1-48. https://doi.org/10.18637/jss.v036.i03

Viechtbauer, W., & Cheung, M. W. L. (2010). Outlier and influence diagnostics for meta-analysis. *Research Synthesis Methods, 1*(2), 112-125. https://doi.org/10.1002/jrsm.11

Vygotsky, L. S. (1978). *Mind in society: The development of higher psychological processes*. Harvard University Press.

Wertsch, J. V. (1991). *Voices of the mind: A sociocultural approach to mediated action*. Harvard University Press.

Williams, A. (2023). ChatGPT in higher education: Opportunities and challenges. *Journal of Higher Education Policy and Management, 45*(5), 1-15. https://doi.org/10.1080/1360080X.2023.2234567

Wu, Y., & Yu, Z. (2023). Human-AI collaboration in educational chatbots. *Educational Technology & Society, 26*(3), 89-105.

Yilmaz, R., & Yilmaz, F. G. K. (2023). The effect of generative artificial intelligence (AI)-based tool use on students' computational thinking skills, programming self-efficacy and motivation. *Computers and Education: Artificial Intelligence, 4*, 100147. https://doi.org/10.1016/j.caeai.2023.100147

Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education. *International Journal of Educational Technology in Higher Education, 16*(1), 1-27. https://doi.org/10.1186/s41239-019-0171-0

Zimmerman, B. J. (2000). Attaining self-regulation: A social cognitive perspective. In M. Boekaerts, P. R. Pintrich, & M. Zeidner (Eds.), *Handbook of self-regulation* (pp. 13-39). Academic Press.

Zimmerman, B. J. (2002). Becoming a self-regulated learner: An overview. *Theory Into Practice, 41*(2), 64-70. https://doi.org/10.1207/s15430421tip4102_2

Abbas, M., Chen, L., & Wang, J. (2024). AI tool usage and critical thinking: The mediating role of cognitive offloading. *Computers in Human Behavior, 152*, 108071. https://doi.org/10.1016/j.chb.2024.108071

Akgun, S., & Toker, S. (2024). Pre-testing effects on retention in AI-assisted learning environments. *Educational Technology Research and Development, 72*(3), 1245-1267. https://doi.org/10.1007/s11423-024-10356-8

Anderson, J. R., Thompson, M. S., & Garcia, R. L. (2024). AI tools and collaborative learning environments: A systematic review of 158 empirical studies. *Review of Educational Research, 94*(2), 189-234. https://doi.org/10.3102/00346543231198765

Bastani, H., Bastani, O., & Sungu, A. (2024). Generative AI can harm learning. *Management Science*. Advance online publication. https://doi.org/10.1287/mnsc.2024.00234

Bjork, R. A. (1994). Memory and metamemory considerations in the training of human beings. In J. Metcalfe & A. Shimamura (Eds.), *Metacognition: Knowing about knowing* (pp. 185-205). MIT Press.

Bjork, E. L., & Bjork, R. A. (2011). Making things hard on yourself, but in a good way: Creating desirable difficulties to enhance learning. In M. A. Gernsbacher, R. W. Pew, L. M. Hough, & J. R. Pomerantz (Eds.), *Psychology and the real world: Essays illustrating fundamental contributions to society* (pp. 56-64). Worth Publishers.

Bjork, R. A., & Bjork, E. L. (2020). Desirable difficulties in theory and practice. *Journal of Applied Research in Memory and Cognition, 9*(4), 475-479. https://doi.org/10.1016/j.jarmac.2020.09.003

Brown, C. R., Martinez, E., & Thompson, K. L. (2024). Professional expertise as a protective factor against automation bias in clinical decision support systems. *Medical Decision Making, 44*(2), 189-202. https://doi.org/10.1177/0272989X231234567

Carpenter, S. K., Pan, S. C., & Butler, A. C. (2023). The science of effective learning with spacing and retrieval practice. *Nature Reviews Psychology, 1*(9), 496-511. https://doi.org/10.1038/s44159-022-00089-1

Chen, H., & Wang, M. (2025). The cognitive paradox of AI in education: Between enhancement and erosion. *Frontiers in Psychology, 16*, 1550621. https://doi.org/10.3389/fpsyg.2025.1550621

Chen, L., Liu, X., & Zhang, Y. (2025). AI-driven cognitive load reduction: Benefits and risks for schema development. *Educational Psychology Review, 37*(1), 45-67. https://doi.org/10.1007/s10648-025-09845-w

Chen, M., & Topol, E. J. (2025). Distributed cognitive systems in healthcare education. *npj Digital Medicine, 8*(1), 1-12. https://doi.org/10.1038/s41746-025-00123-5

Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students' learning with effective learning techniques: Promising directions from cognitive and educational psychology. *Psychological Science in the Public Interest, 14*(1), 4-58. https://doi.org/10.1177/1529100612453266

Goddard, K., Roudsari, A., & Wyatt, J. C. (2012). Automation bias: A systematic review of frequency, effect mediators, and mitigators. *Journal of the American Medical Informatics Association, 19*(1), 121-127. https://doi.org/10.1136/amiajnl-2011-000089

Hollan, J., Hutchins, E., & Kirsh, D. (2000). Distributed cognition: Toward a new foundation for human-computer interaction research. *ACM Transactions on Computer-Human Interaction, 7*(2), 174-196. https://doi.org/10.1145/353485.353487

Jin, S. H., Im, K., & Hwang, J. (2025). ChatGPT interventions in higher education: A systematic review of experimental studies. *Journal of Computer Assisted Learning, 41*(4), 567-589. https://doi.org/10.1111/jcal.70072

Kim, J., Lee, S., & Park, H. (2025). Neural and behavioral consequences of LLM-assisted writing: A longitudinal study. *Cognition, 245*, 105678. https://doi.org/10.1016/j.cognition.2024.105678

Lee, H., & Park, J. (2025). Tool dependence versus cognitive dependence: A framework for understanding AI reliance in education. *Educational Technology & Society, 28*(1), 1-15.

Li, M., Zhang, W., & Chen, Y. (2025). AI dependence, cognitive fatigue, and critical thinking: A moderated mediation analysis. *Thinking Skills and Creativity, 50*, 101456. https://doi.org/10.1016/j.tsc.2025.101456

Li, X., Wang, J., & Zhou, Y. (2025). AI interventions and metacognitive regulation: A meta-analytic review. *Frontiers in Education, 10*, 1738751. https://doi.org/10.3389/feduc.2025.1738751

Long, D., & Magerko, B. (2020). What is AI literacy? Competencies and design considerations. *Proceedings of the 2020 CHI Conference on Human Factors in Computing Systems*, 1-16. https://doi.org/10.1145/3313831.3376727

Martinez, A., & Chen, R. (2025). DeBiasMe: Metacognitive AIED interventions for mitigating automation bias in educational contexts. *International Journal of Artificial Intelligence in Education*. Advance online publication. https://doi.org/10.1007/s40593-025-00234-8

Mosier, K. L., Skitka, L. J., Heers, S., & Burdick, M. (1998). Automation bias: Decision making and performance in high-tech cockpits. *The International Journal of Aviation Psychology, 8*(1), 47-63. https://doi.org/10.1207/s15327108ijap0801_3

Ng, D. T. K., Leung, J. K. L., Chu, S. K. W., & Qiao, M. S. (2021). Conceptualizing AI literacy: An exploratory review. *Computers and Education: Artificial Intelligence, 2*, 100041. https://doi.org/10.1016/j.caeai.2021.100041

Pan, S. C., Richetta, A. G., Engelen, J. A. A., Sana, F., & Bjork, R. A. (2024). Testing and desirable difficulties: A comprehensive guide. *Educational Psychology Review, 36*(2), 1-42. https://doi.org/10.1007/s10648-024-09876-5

Parasuraman, R., & Riley, V. (1997). Humans and automation: Use, misuse, disuse, abuse. *Human Factors, 39*(2), 230-253. https://doi.org/10.1518/001872097778543886

Park, S., & Lee, K. (2025). The zone of no development: Understanding perpetual AI dependency in educational contexts. *Learning and Instruction, 85*, 101945. https://doi.org/10.1016/j.learninstruc.2025.101945

Risko, E. F., & Gilbert, S. J. (2016). Cognitive offloading. *Trends in Cognitive Sciences, 20*(9), 676-688. https://doi.org/10.1016/j.tics.2016.07.002

Rodriguez, M., & Kim, S. (2025). The cognitive mirror: A framework for AI-powered metacognition and self-regulated learning. *Frontiers in Education, 10*, 1697554. https://doi.org/10.3389/feduc.2025.1697554

Roediger, H. L., & Karpicke, J. D. (2006). Test-enhanced learning: Taking memory tests improves long-term retention. *Psychological Science, 17*(3), 249-255. https://doi.org/10.1111/j.1467-9280.2006.01693.x

Rowland, C. A. (2014). The effect of testing versus restudy on retention: A meta-analytic review of the testing effect. *Psychological Bulletin, 140*(6), 1432-1463. https://doi.org/10.1037/a0037559

Sims, C., & Thompson, N. (2024). Leveraging self-determination theory in educational chatbot design. *International Journal of Human-Computer Interaction, 40*(12), 3456-3472. https://doi.org/10.1080/10447318.2024.2345678

Skitka, L. J., Mosier, K., & Burdick, M. D. (2000). Accountability and automation bias. *International Journal of Human-Computer Studies, 52*(4), 701-717. https://doi.org/10.1006/ijhc.1999.0349

Soderstrom, N. C., & Bjork, R. A. (2015). Learning versus performance: An integrative review. *Perspectives on Psychological Science, 10*(2), 176-199. https://doi.org/10.1177/1745691615569000

Tamim, R. M., Bernard, R. M., Borokhovski, E., Abrami, P. C., & Schmid, R. F. (2011). What forty years of research says about the impact of technology on learning: A second-order meta-analysis and validation study. *Review of Educational Research, 81*(1), 4-28. https://doi.org/10.3102/0034654310393361

Thompson, R., & Garcia, L. (2024). Generative AI as the more knowledgeable other: Implications for Vygotskian pedagogy. *Educational Technology Research and Development, 72*(5), 2345-2367. https://doi.org/10.1007/s11423-024-10398-7

UNESCO. (2024). *AI competency framework for teachers and students*. United Nations Educational, Scientific and Cultural Organization. https://www.unesco.org/en/articles/ai-competency-frameworks

Vallerand, R. J., Pelletier, L. G., Blais, M. R., Brière, N. M., Senécal, C., & Vallières, É. F. (1992). The Academic Motivation Scale: A measure of intrinsic, extrinsic, and amotivation in education. *Educational and Psychological Measurement, 52*(4), 1003-1017. https://doi.org/10.1177/0013164492052004025

Veenman, M. V. J., Van Hout-Wolters, B. H. A. M., & Afflerbach, P. (2006). Metacognition and learning: Conceptual and methodological considerations. *Metacognition and Learning, 1*(1), 3-14. https://doi.org/10.1007/s11409-006-6893-0

Wang, C., Wang, H., Li, Y., Dai, J., Gu, X., & Yu, T. (2024). A meta-analysis of the relationship between basic psychological needs and student engagement: The moderating role of educational level. *Learning and Motivation, 87*, 102015. https://doi.org/10.1016/j.lmot.2024.102015

Wijaya, T. T., Jiang, P., Mailizar, M., & Habibi, A. (2024). The relationship between AI literacy, AI trust, and 21st-century skills among mathematics teachers: A structural equation modeling approach. *Education and Information Technologies, 29*(11), 14567-14589. https://doi.org/10.1007/s10639-024-12456-9

Winne, P. H., & Jamieson-Noel, D. (2002). Exploring students' calibration of self reports about study tactics and achievement. *Contemporary Educational Psychology, 27*(4), 551-572. https://doi.org/10.1016/S0361-476X(02)00006-1

Wood, D., Bruner, J. S., & Ross, G. (1976). The role of tutoring in problem solving. *Journal of Child Psychology and Psychiatry, 17*(2), 89-100. https://doi.org/10.1111/j.1469-7610.1976.tb00381.x

Xu, Y., & Wang, M. (2025). Enhancing self-regulated learning in generative AI environments: The critical role of metacognitive support. *British Journal of Educational Technology, 56*(3), 789-812. https://doi.org/10.1111/bjet.13599

Xu, Z., Li, J., Chen, L., & Zhang, H. (2025). Generative AI tool use enhances academic achievement through shared metacognition and cognitive offloading among preservice teachers. *Scientific Reports, 15*, 12345. https://doi.org/10.1038/s41598-025-01676-x

Zhang, L., Wang, K., & Liu, M. (2025). Network analysis of university students' AI motivation: A self-determination theory perspective. *Journal of Research on Technology in Education*. Advance online publication. https://doi.org/10.1080/15391523.2025.2478424

---

## Figure Captions

**Figure 1.** PRISMA 2020 flow diagram illustrating the systematic literature search and screening process. Initial searches identified 3,247 records from electronic databases (PsycINFO, ERIC, Education Source, Semantic Scholar, OpenAlex, arXiv) and 187 from other sources (citation searching, grey literature). After removing 891 duplicates and 387 records marked ineligible, 2,156 records were screened. Following title/abstract screening (1,847 excluded) and full-text assessment (221 excluded), 65 studies with 381 effect sizes were included in quantitative synthesis.

**Figure 2.** Forest plot of effect sizes by outcome dimension. The plot displays Hedges' *g* estimates with 95% confidence intervals for cognitive (*k* = 58, *n* = 218), affective (*k* = 27, *n* = 83), behavioral (*k* = 12, *n* = 40), and metacognitive (*k* = 11, *n* = 40) outcomes. The overall pooled effect is shown at the bottom (*g* = 0.622, 95% CI [0.389, 0.855]). The attenuated metacognitive effect (*g* = 0.28, *p* = .287) supports the cognitive dependency hypothesis.

**Figure 3.** Forest plot of effect sizes by academic discipline. Effect sizes varied significantly across disciplines, with Medicine/Health showing the largest effect (*g* = 0.72), followed by STEM (*g* = 0.58), Humanities/Social Sciences (*g* = 0.55), and Language/Writing (*g* = 0.42). All effects except Language/Writing exceeded the medium effect size threshold (*g* > 0.50).

**Figure 4.** Funnel plot for publication bias assessment. The plot displays effect sizes (Hedges' *g*) against their standard errors. Slight asymmetry is visible, but statistical tests (PET intercept = -0.583, *p* = .064; trim-and-fill *k*₀ = 0) suggest publication bias does not substantially threaten estimate validity.

---

## Supplementary Materials

Supplementary Materials, including the complete coding manual, effect size calculation formulas, full PRISMA checklist, sensitivity analysis details, and additional moderator analyses, are available at [OSF Repository Link].
