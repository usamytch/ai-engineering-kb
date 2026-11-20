# Is Complex Agentic Memory Always Needed? Naive RAG Is Stronger Than We Thought

## Executive summary

The paper makes a strong case that a properly specified raw-history RAG baseline is mandatory when evaluating agentic memory. Raw-RAG combines dense retrieval, cross-encoder reranking, and source-preserving evidence; it leads the compared memory systems in six of seven main benchmark–model settings and is substantially cheaper to ingest. Controlled ablations support reranking and moderate retrieval depth, while three added memory-management variants hurt accuracy. Evidence diagnostics suggest coverage and preservation of dependency paths matter more than conditional reader utilization. The conclusion should remain scoped to offline public benchmarks: supplementary personalization results favor structured systems, comparisons mix newly measured and published scores, and oracle diagnostics do not isolate ingestion loss from evidence presentation.

## Problem

**Statement.** The paper asks whether extraction, mutation, summarization, graphs, and retrieval control improve long-term conversation understanding beyond a strong, fixed retrieval pipeline over unmodified history.

**Why it matters.** Weak RAG controls can falsely attribute gains to agentic memory. A credible reference must preserve source information, retrieve broadly enough for dispersed evidence, rerank candidates, and expose its accuracy, latency, and context-budget trade-offs.

**Scope.** The main evidence covers offline question answering and related memory tasks on four public benchmarks, with supplementary personalization and ingestion-scaling studies. It does not establish behavior in interactive, multimodal, privacy-constrained, deletion-enforcing, or tool-operating systems.

## Method

Raw-RAG serializes timestamped conversation history and image captions, indexes overlapping token windows without LLM transformation, retrieves candidates by dense cosine similarity, reranks them with a cross-encoder, and supplies selected source text to a reader LLM. The study compares this pipeline with agentic systems and Full-context, then analyzes mutation, retrieval design, context budgets, latency, evidence coverage, path retention, and privileged complete-store access.

### Key components

- Source-preserving indexing with 256-token windows and 32-token overlap.
- Dense retrieval of 128 candidates followed by cross-encoder selection of 15 items.
- Benchmark-specific evidence assembly, including chronological presentation for MEME and complete-turn expansion where enabled.
- Matched benchmark conditions where possible, with repeated LLM judgments for LoCoMo and LongMemEval.
- Paired bootstrap intervals, source or episode stratification, and Holm correction for selected diagnostic and ablation families.
- Diagnostics separating evidence coverage from conditional utilization and answer-value coverage from complete supporting-path coverage.

### Assumptions

- Raw histories and transformed stores are compared as end-to-end systems; representation, retrieval, evidence formatting, and reader interaction may all contribute to observed differences.
- Published baseline scores are treated as valid comparison points when direct reruns are unavailable.
- LLM-based correctness and sufficiency judgments are adequate proxies under the documented prompts and repetition procedures.
- The evaluated retrieval budgets and benchmark task distributions are representative of the paper's target setting, not of all operational memory workloads.

## Main claims

- **A well-configured naive RAG pipeline is a stronger reference baseline than prior evaluations imply and leads most of the paper's main comparisons.**
  - Evidence: [b00042-c327b8915b] “Raw-RAG achieves the highest score among the compared memory systems in six of seven benchmark–model settings, excluding Full-context.”
- **The proposed explanation is primarily evidence access: Raw-RAG retrieves sufficient evidence more often, even though it does not have the best conditional utilization.**
  - Evidence: [b00064-e64c21e6d7] “Thus, systems differ more in supplying sufficient evidence than in answering correctly once it is supplied.”; [b00064-e64c21e6d7] “Raw-RAG leads in coverage, helping offset its less-than-best conditional utilization and explaining its strong performance.”
- **Preserving answer values alone is insufficient; chronological and dependency relations are material to reasoning.**
  - Evidence: [b00066-9b7532c3de] “Useful retrieval therefore includes the order and dependencies that make one value current.”; [b00068-c3f7f3dc74] “Systems that retrieve answer values can still differ substantially in preserving their supporting relations.”
- **Explicit mutation is not shown to help in the tested Mem0 configuration.**
  - Evidence: [b00009-01c64d8817] “Replacing UPDATE with append-only ADD and DELETE with NONE raises LoCoMo accuracy from 67.36% to 69.42%, without reducing any category score (Table 2).”; [b00009-01c64d8817] “Explicit mutation provides no accuracy gain in this configuration.”

## Results

- **Across the main comparisons, Raw-RAG ranks first among memory systems in six of seven benchmark–model settings. Its reported leads are 0.65–0.95 points on LoCoMo, 0.13 points on LongMemEval, 2.24 points on GPT-4o-mini MEME, and 4.48–5.53 points on MemoryAgentBench. The exception is DeepSeek-V4-Flash MEME, where MemMachine leads Raw-RAG by 1.52 points and Full-context leads it by 19.98 points.**
  - Context: This is the headline end-to-end result. The explicit exception is consequential: raw retrieval is not uniformly best, and access to the full history can be much stronger on a dynamic-state benchmark.
  - Evidence: [b00042-c327b8915b] “It leads LoCoMo by 0.65–0.95 points, LongMemEval by 0.13 points, GPT-4o-mini MEME by 2.24 points, and MemoryAgentBench by 4.48–5.53 points.”; [b00042-c327b8915b] “MemMachine leads DeepSeek-V4-Flash MEME among the memory systems by 1.52 points, while Full-context leads Raw-RAG by 19.98 points in that setting.”
- **Retrieval design matters: removing reranking reduces MemoryAgentBench Total by 3.92 points, while final retrieval depths of 1 and 120 reduce it by 11.73 and 14.57 points. Depths from 5 through 60 remain close to the default, so the evidence favors moderate depth rather than the exact choice of 15.**
  - Context: This is the strongest controlled support for why Raw-RAG outperforms historically weak RAG baselines. The extremes fail, while several moderate settings are statistically compatible with the default.
  - Evidence: [b00051-1e185229a8] “Top-120 loses 14.57 points, driven by long-range understanding and conflict resolution.”; [b00199-68166632d0] “15 48.32 – –”; [b00051-1e185229a8] “Removing reranking lowers Total by 3.92 points (pHolm=0.0012), while returning only one item lowers it by 11.73 points.”; [b00199-68166632d0] “1 36.59 -11.73 [-14.05,-9.43]”; [b00199-68166632d0] “120 33.74 -14.57 [-16.83,-12.34]”; [b00051-1e185229a8] “Final-k values of 5, 10, 30, and 60 stay within 1.3 points of the baseline.”
- **All three tested memory-management additions hurt MemoryAgentBench Total relative to Raw-RAG: atomic facts by 19.62 points, raw-summary augmentation by 5.81 points, and graph expansion by 5.78 points. Atomic facts also reduce test-time learning from 47.68% to 15.37%.**
  - Context: This is a controlled negative result for these particular representations and reader stack, not a general proof that memory management cannot help. Evidence length, demonstration structure, and reader-format compatibility remain coupled.
  - Evidence: [b00053-00c7200192] “Atomic-fact extraction reduces test-time learning from 47.68% to 15.37% and Total by 19.62 points”; [b00053-00c7200192] “Summary augmentation largely preserves Accurate Retrieval performance but loses 5.81 points overall”; [b00053-00c7200192] “Graph expansion ties Raw-RAG on long-range understanding yet remains 5.78 points lower overall.”
- **Evidence diagnostics favor coverage and path preservation. Raw-RAG coverage is 45.29% on MemoryAgentBench and 76.35% on MEME; its conditional path coverage is 62.34%, ahead of MemMachine at 56.70%. Under privileged complete-store access on MEME, Raw-RAG reaches 57.54% and MemMachine 57.46%, versus 61.60% for raw evidence.**
  - Context: These diagnostics support the proposed mechanism, but coverage uses an LLM judge on MemoryAgentBench, and the complete-store comparison changes selection, packing, and reader policy. It therefore cannot isolate ingestion-time information loss.
  - Evidence: [b00064-e64c21e6d7] “Raw-RAG achieves the highest coverage on both benchmarks: 45.29% and 76.35%.”; [b00068-c3f7f3dc74] “Raw-RAG achieves the highest conditional path coverage (62.34%), followed by MemMachine (56.70%)”; [b00075-d2ea866341] “Raw-RAG and MemMachine, which retain raw conversational content in their evaluated stores, reach 57.54% and 57.46%, respectively, compared with 61.60% for raw evidence.”
- **On the same MEME latency slice, Raw-RAG completes ingestion-to-ready plus search in 305.91 seconds, compared with 1561.97 seconds for the next-fastest listed system and 9301.48 seconds for EverMemOS. These measurements exclude answer generation and evaluation.**
  - Context: The efficiency advantage is large for the measured deployment, but system readiness definitions, internal parallelism, APIs, endpoint load, and local resources affect wall-clock comparisons.
  - Evidence: [b00048-185c4c0685] “EMem [59] 1082.37 479.59 1561.97 Raw-RAG 50.32 255.59 305.91”; [b00048-185c4c0685] “EverMemOS [10] 8217.69 1083.79 9301.48”; [b00047-42ee788d02] “Total: Add-to-ready plus Search, without answer generation or evaluation.”

## Experimental evaluation

### Datasets

- LoCoMo: 10 conversations and 1,540 non-adversarial questions spanning single-hop, multi-hop, temporal, and open-domain reasoning.
  - Evidence: [b00037-85ca71dd75] “LoCoMo (10 conversations; 1,540 non-adversarial questions on single-hop, multi-hop, temporal, and open-domain reasoning)”
- LongMemEval: 500 examples covering recall, temporal reasoning, preferences, and updates.
  - Evidence: [b00037-85ca71dd75] “LongMemEval (500 examples on recall, temporal reasoning, preferences, and updates)”
- MEME: 100 episodes and 1,188 phase-specific questions targeting dynamic updates and dependency understanding.
  - Evidence: [b00037-85ca71dd75] “MEME (100 episodes; 1,188 phase-specific questions on dynamic memory updates and complex memory dependency understanding)”
- MemoryAgentBench: 2,071 questions from 14 sources across retrieval, test-time learning, long-range understanding, and conflict resolution.
  - Evidence: [b00037-85ca71dd75] “MemoryAgentBench (2,071 questions from 14 sources on accurate retrieval, test-time learning, long-range understanding, and conflict resolution)”
- Supplementary PersonaMem-v2 evaluation: nine scenarios and 5,000 multiple-choice questions; Raw-RAG ranks third rather than first.
  - Evidence: [b00187-db2a53b394] “covering nine conversational scenarios.”; [b00193-ce9f099b38] “Raw-RAG achieves 49.62% accuracy (2,481/5,000), ranking third among seven systems behind MemOS and EverMemOS”

### Baselines

- Agentic systems include EverMemOS, MemOS, EMem, SimpleMem, MemU, MemMachine, Mem0, Memora, Nemori, MemoryOS, A-MEM, and RecMem, plus Full-context.
  - Evidence: [b00038-355998528b] “Baselines include EverMemOS [10], MemOS [21], EMem [59], SimpleMem [23], MemU [31], MemMachine [49], Mem0 [4], Memora [53], Nemori [30], MemoryOS [16], A-MEM [54], and RecMem [5], alongside Full-context.”
- Full-context is a no-retrieval reference that directly supplies visible chronological history under a bounded-history policy.
  - Evidence: [b00580-07578ba1da] “Full-context omits both memory transformation and retrieval: the reader receives the visible chronological history directly”

### Metrics

- LoCoMo and LongMemEval primarily use question-weighted LLM-judge accuracy under the stated repeated-judgment procedures.
  - Evidence: [b00150-39afba0f4a] “judge accuracy is the mean of the binary correctness judgments across questions and judge repetitions.”; [b00171-131b826f8a] “Overall accuracy is question-weighted.”
- MEME Overall is the macro-average of six task scores; selected after-state tasks also require the corresponding before-phase answer to pass.
  - Evidence: [b00487-e84f23f846] “Overall is the six-task macro-average.”; [b00487-e84f23f846] “an after-phase pass receives credit only if the corresponding before-phase answer was also correct”
- MemoryAgentBench Overall averages four capability scores rather than pooling all questions.
  - Evidence: [b00590-af221f933a] “Overall=AR+TTL+LRU+CR4.”; [b00591-7741ee33d1] “A flat average over all questions or over the six TTL sources would assign different weights.”
- Diagnostics measure evidence coverage, conditional reader utilization, result coverage, and executable-path retention.
  - Evidence: [b00063-c5b9d04dc5] “We measure coverage, the fraction of questions with sufficient retrieved evidence, and utilization, answer accuracy conditional on sufficient evidence.”; [b00067-98b6c2afc8] “This conditional rate measures how often successful value retrieval also preserves the relations and paths needed to use those values.”

### Ablations

- Reranker removal, chunk sizes, final retrieval depth, and display-turn deduplication on MemoryAgentBench.
  - Evidence: [b00046-ca2e29db72] “− reranker 59.13 44.29 29.66 44.50 44.40 -3.92 [-5.80,-2.06]”; [b00046-ca2e29db72] “128/16 70.50 46.89 28.93 46.00 48.08 -0.24 [-1.54,+1.05]”
- Atomic-fact replacement, raw-summary augmentation, and graph-expanded raw retrieval.
  - Evidence: [b00053-00c7200192] “We evaluate three memory-management operations: atomic-fact extraction, summary augmentation, and graph-based retrieval expansion.”
- Cross-system and Raw-RAG-only evidence-budget controls impose a 5,000-token reader-evidence ceiling.
  - Evidence: [b00211-33d04f5d61] “This intervention freezes each system’s retrieved evidence and imposes a 5,000-token ceiling on formatted reader evidence”; [b00224-9300cfdfca] “MEME 1,188 1,188 4,173.1 4,273 39.30 38.21 −1.09”
- Mem0 mutation policy is compared with an ADD/NONE-only intervention.
  - Evidence: [b00011-d5d0ee9747] “Overall 67.36 69.42 +2.06”

### Negative results

- DeepSeek-V4-Flash MEME is the main setting where Raw-RAG does not lead the compared memory systems.
  - Evidence: [b00042-c327b8915b] “MemMachine leads DeepSeek-V4-Flash MEME among the memory systems by 1.52 points”
- Raw-RAG underperforms structured systems on supplementary PersonaMem-v2 and leads no individual scenario.
  - Evidence: [b00193-ce9f099b38] “ranking third among seven systems behind MemOS and EverMemOS, without leading any individual scenario.”
- Added atomic facts, summaries, and graph expansion all reduce overall accuracy in the tested configuration.
  - Evidence: [b00053-00c7200192] “Thus, these three memory-management additions reduce overall accuracy in this setting.”
- The smaller evidence budget decreases Raw-RAG on MEME, while its apparent LoCoMo gain is largely attributable to unchanged contexts and rerun variability.
  - Evidence: [b00226-92099f52d5] “Table 23 shows higher rerun scores on LoCoMo and LongMemEval and a 1.09-point decrease on MEME.”; [b00227-c56c79330a] “Most of its observed gain therefore comes from questions whose evidence did not change.”


## Limitations

- External validity is narrow: the evidence concerns offline public-benchmark conversations, not interactive, multimodal, or wider operational use.
  - Evidence: [b00078-2040c734e3] “Our evidence is limited to offline conversation on public benchmarks; it does not establish performance for interactive, multimodal, or broader operational settings.”
- Raw-history retention raises storage and privacy issues, and benchmark deletion questions do not test physical erasure.
  - Evidence: [b00078-2040c734e3] “raw-history approaches also raise storage and privacy concerns.”; [b00485-52b48ad120] “physical erasure from storage is outside its scoring criteria.”
- Some headline comparisons combine scores measured in this study with published scores obtained under other environments; complete equivalence is therefore limited to explicitly aligned settings.
  - Evidence: [b00146-6c2cbba855] “Published baseline scores are retained, and Raw-RAG results are measured in this study.”; [b00597-7b25fdffb4] “Published comparison scores were obtained in the environments described by their respective studies.”
- The complete-store diagnostic does not isolate ingestion-time information loss because evidence export, selection, ordering, packing, task policy, and reading also differ.
  - Evidence: [b00440-9b458b20ee] “The comparison therefore does not isolate information loss during ingestion.”; [b00440-9b458b20ee] “Native-to-complete gains likewise combine broader access to stored evidence with changes to task information and readout policy.”
- Coverage and utilization are not controlled reader comparisons because each system's sufficient-evidence subset differs.
  - Evidence: [b00063-c5b9d04dc5] “the system-specific question sets preclude a controlled comparison of readers.”
- LLM services and zero-temperature judgments can vary; statistical intervals condition on observed outputs and store builds rather than capturing model-service variability.
  - Evidence: [b00621-bb2fb33a30] “Hosted model and service behavior can change, and outputs can vary across temperature-zero requests and repeated judgments.”; [b00443-bb1c14adf3] “conditional on the observed reader and semantic-judge outputs, store builds, and sufficiency labels”
- Historical LoCoMo judge responses and failure statuses are unavailable, so zero scores cannot be separated into wrong judgments, formatting failures, or request failures.
  - Evidence: [b00635-37619124b2] “Raw judge responses and per-judgment parse and request status are unavailable.”; [b00635-37619124b2] “leaving the exact format-failure count unknown.”

## Reproducibility

**Status:** partial

Methodological reporting is unusually detailed and should support an informed reimplementation, but exact reproduction is not established. The supplied document does not state that the paper's full code, saved contexts, built stores, answers, judgments, or environment lockfiles are released; several historical records and versions are explicitly missing.

**Available artifacts**

- Detailed Raw-RAG indexing, retrieval, evidence-assembly, and query-construction specifications.
- Benchmark task definitions, scoring and aggregation rules, baseline configurations, prompts, software versions, hardware, latency boundaries, and statistical procedures.
- Public benchmark citations; the MEME reference explicitly identifies code and data.

**Missing pieces**

- No paper-specific code or complete experiment artifact release is stated in the supplied blocks.
- Some historical dependency versions are unavailable.
- Historical raw LoCoMo judge responses and diagnostic statuses are unavailable.
- Original random seeds for one complete-store bootstrap analysis are unavailable.
- API-backed models and services may change, limiting exact replay.

## AIDB assessment

- Novelty: The main novelty is not a new retrieval primitive but a rigorous reframing: source-preserving dense retrieval plus reranking is elevated from a weak control to a diagnostic baseline, then analyzed through mutation interventions, retrieval ablations, evidence sufficiency, path retention, complete-store controls, and cost measurements.
- Usefulness: High for benchmark design and memory-system evaluation. It supplies a concrete minimum baseline, identifies under-tuned retrieval as a confound, and shows where transformation may destroy demonstrations or relational evidence. It is less decisive for production systems requiring privacy, deletion, authoritative state, tool triggers, bounded storage, or personalization.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled retrieval and representation ablations are persuasive, and the negative results are practically important. Adoption as a mandatory baseline is justified for similar offline benchmarks. Broader adoption as a memory architecture would be premature because the strongest claims depend on benchmark scope, mixed-source comparisons, capable readers, and diagnostics that do not isolate all causal mechanisms.

## Uncertainties

- **How much of Raw-RAG's advantage comes from source preservation versus reranking, evidence volume, reader prompt compatibility, or benchmark-specific assembly?** — The paper isolates several components but not a complete factorial decomposition across all benchmarks; system builders need to know which elements transfer.
  - Evidence: [b00619-fb4540c713] “Both token volume and demonstration format vary in this ablation; the separate six-system 5k control in Appendix A.4 leaves these factors coupled.”
- **Whether explicit state construction helps weaker readers or amortizes repeated reasoning remains unresolved.** — Agentic memory may trade ingestion cost for cheaper or more reliable repeated queries, a benefit not captured by single-answer accuracy and ingestion-focused timing.
  - Evidence: [b00617-9549f3ba8e] “Whether state construction during ingestion helps weaker readers or reduces repeated inference remains an open question.”
- **The supplementary personalization result may indicate a real advantage for profile-enabled memory, but the comparison does not isolate profiles and lacks significance testing.** — It limits the claim that raw retrieval is generally sufficient for personalized assistants.
  - Evidence: [b00193-ce9f099b38] “The comparison measures overall system performance with each system’s native profile configuration; statistical significance remains untested.”
- **Long-history behavior under fixed retrieval and reader budgets is not established.** — Raw storage and sparse retrieval may degrade as relevant evidence becomes more dispersed or semantically distant.
  - Evidence: [b00621-bb2fb33a30] “Raw storage grows with history length, and a fixed candidate and reader budget can miss dispersed or low-similarity evidence.”

## Open questions

- At what history length, evidence dispersion, or update rate do structured memories overtake source-preserving retrieval under equal reader-token and compute budgets?
- Can a hybrid store preserve raw provenance and demonstration structure while adding compact, authoritative state for privacy, deletion, and tool use?
- Does ingestion-time state construction improve weaker readers or reduce total lifecycle cost when the same memory is queried repeatedly?
- Which failure modes explain Raw-RAG's weakness on DeepSeek-V4-Flash MEME and PersonaMem-v2, and are they retrieval, reader, or representation failures?
- How stable are LLM-judge, sufficiency, and path-retention conclusions across independent judges and fully deterministic task checks?

## Proposed AIDB experiments

- **Hypothesis:** Raw source preservation, rather than added context length alone, drives the advantage over atomic facts and summaries on test-time learning and dependency tasks.
  - Baseline: Raw-RAG and the paper's atomic-fact, raw-summary, and graph-expanded variants, matched factorially for reader-visible tokens, item count, ordering, and reader prompt.
  - Primary metric: Paired change in MemoryAgentBench test-time-learning Total and MEME executable-path coverage, with episode/source-stratified confidence intervals.
  - Stop condition: Stop when every condition has identical token and item budgets and the confidence interval for each raw-versus-transformed contrast either excludes zero or lies wholly within a predeclared equivalence margin.
- **Hypothesis:** Structured state helps weaker readers and repeated queries enough to offset ingestion cost in total lifecycle compute.
  - Baseline: Raw-RAG versus an append-only raw-plus-state hybrid and a mutation-based system, evaluated with at least one weaker and one stronger reader over the same stores.
  - Primary metric: Accuracy per total lifecycle cost, including ingestion, retrieval, answer generation, and cumulative tokens over increasing queries per stored history.
  - Stop condition: Stop after the crossover point is identified with a confidence interval, or after the maximum preregistered query count if no structured system reaches higher accuracy per cost.
- **Hypothesis:** Profile-enabled memory explains the supplementary PersonaMem-v2 advantage rather than unrelated implementation differences.
  - Baseline: Raw-RAG without a profile, Raw-RAG with a profile retrieved under the same pipeline, and the leading profile-enabled systems under identical reader, option order, evidence budget, and scoring.
  - Primary metric: Question-weighted multiple-choice accuracy with paired confidence intervals, plus scenario-level error attribution for preference retrieval and update handling.
  - Stop condition: Stop when the profile effect is statistically resolved after multiplicity correction or its interval fits within a predeclared equivalence margin.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:03.118585+00:00`
- Document SHA-256: `709ac43d5d206158323a4902165c6dffe79532bc1b389b62e49109c02f046f95`
- Metadata SHA-256: `f0480be652fb832cd34797be219d5aef8794dc415501d48559cd68bf3404f931`
- Blocks: 674
- Deterministic repair attempts: 0
