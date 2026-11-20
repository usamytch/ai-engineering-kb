# AutoRAGBench: A Benchmark for LLM Agents Automating RAG System Development

## Executive summary

AutoRAGBench evaluates autonomous, open-code RAG development across nine tasks under a standardized six-hour, single-GPU budget. Its strongest configuration, GPT-6.1 Sol with Codex CLI, averages 56.1, versus 46.4 for Reference RAG and 44.4 for a composite Human-SOTA envelope. The benchmark also reveals important costs and instability: every agent system is slower than Reference RAG, some final development checks regress from earlier peaks, and development gains do not reliably predict hidden-test quality. The evidence supports the practical promise of agent-built RAG, but not a clean attribution to model capability, harness, individual components, or human-versus-agent design. Single builds, adapted baselines, unverified qualitative labels, and no component ablations constrain causal conclusions.

## Problem

**Statement.** The paper asks how well LLM agents can build RAG systems autonomously across heterogeneous tasks and improve those systems through iterative experimentation in an unrestricted code space.

**Why it matters.** Effective RAG requires task-specific choices over corpus processing, indexing, retrieval, reranking, evidence selection, prompts, and control flow. Automating this engineering loop could reduce substantial manual effort, but final accuracy alone cannot establish whether an agent improves reliably or whether its gains survive iteration.

**Scope.** The benchmark covers nine English-language RAG tasks in five categories. Nine complete model–harness configurations receive supplied corpora and training examples, internet access under data-use restrictions, one H800 GPU, and six hours. Final systems are assessed on hidden tests with five held-out answering models; trajectories are also analyzed.

## Method

Each agent starts in a clean isolated container without starter code, persistent memory, a prescribed pipeline, or a predefined configuration space. It may inspect data, install libraries, download auxiliary models, implement a retrieval service, and use supplied examples for self-checks. The frozen service must return ordered spans from the supplied corpus. Five held-out models answer from a validated common evidence prefix. Scores are averaged across answering models and then equally across tasks. Development trajectories support descriptive analysis of preparation, implementation, testing, analysis, first-to-last progress, peak-to-last regression, time, tokens, and API cost.

### Key components

- A task suite spanning open-domain QA, document multi-hop QA, domain-specific QA, fact verification, and knowledge-graph QA.
- A controlled build protocol with fresh containers, hidden tests, common instructions, fixed compute and time budgets, and a frozen retrieval interface.
- Integrity checking through automated trajectory and submission review, followed by manual review of suspected violations and reruns.
- Outcome evaluation using task-specific answer metrics, five held-out answering models, rank stability, and retrieval latency.
- Process evaluation using recorded actions and observations, comparable self-check scores, development activities, resource allocation, and API spending.
- Additional comparisons against adapted human-designed methods, predefined automated RAG searches, and agent improvements to existing systems.

### Assumptions

- Averaging five small answering models is treated as a useful proxy for the quality of retrieved evidence.
- The unweighted mean of heterogeneous task metrics is treated as a meaningful overall score.
- The supplied training examples and Qwen3.5-4B self-checks provide adequate feedback for iterative development.
- The integrity audit detects consequential external-data and test-set violations well enough to preserve benchmark validity.
- A model plus its harness is the evaluation unit; cross-harness results do not isolate the underlying LLM.
- The composite Human-SOTA envelope is a comparison reference, not a deployable system or an upper bound on human engineering.

## Main claims

- **The paper presents AutoRAGBench as the first benchmark of autonomous from-scratch RAG development in an open code space.**
  - Evidence: [b00015-9b16d2254d] “We propose AutoRAGBench, the first benchmark to evaluate how well LLM agents automate the development of RAG systems from scratch in an open code space.”
- **The evaluation jointly measures delivered RAG systems and the iterative processes that produce them.**
  - Evidence: [b00017-8a9f06f12f] “We design an evaluation framework that combines RAG system evaluation with development process evaluation”
- **The paper argues that task-specific open-code construction adds value beyond searches over fixed pipeline spaces.**
  - Evidence: [b00013-b87d451bf5] “In our adapted comparisons, it also outperforms automated searches over predefined RAG pipelines [20, 21], including a search driven by the same LLM.”; [b00161-047a62a2be] “All 18 agent-built knowledge-graph systems use graph traversal (Section VI-D), an option absent from both framework search spaces.”
- **The authors release code and data to support subsequent research.**
  - Evidence: [b00019-07e9f6efb7] “We release our code and data on GitHub11 1 https://github.com/ZhanGHanG9991/AutoRAGBench”

## Results

- **GPT-6.1 Sol with Codex CLI is the strongest tested configuration: it averages 56.1, compared with 46.4 for Reference RAG and 44.4 for the composite Human-SOTA baseline. The reported margins are 9.7 and 11.7 points, respectively; all nine agents beat naive BM25, while seven beat Reference RAG.**
  - Context: This is the principal hidden-test comparison, averaged over five held-out answering models and nine equally weighted tasks. Human-SOTA is a per-task envelope of adapted implementations with a different development budget, so it is not a controlled human-versus-agent contest.
  - Evidence: [b00124-efc7f225b3] “GPT-6.1 Sol with Codex CLI achieves the highest average, 56.1, and the best score on seven tasks.”; [b00124-efc7f225b3] “The reference RAG system combines hybrid retrieval with reranking and reaches 46.4.”; [b00124-efc7f225b3] “Its 9.7-point gain over the reference system is comparable to the gain from naive BM25 RAG to the reference system.”; [b00124-efc7f225b3] “The composite Human-SOTA baseline averages 44.4, below all nine agent configurations. GPT-6.1 Sol exceeds this baseline by 11.7 points.”; [b00124-efc7f225b3] “All nine agent configurations outperform naive BM25 RAG, and seven outperform the reference system.”
- **Performance gains are task-dependent. All nine configurations beat Reference RAG on WebQSP by 14.1 points on average, but only three beat it on HotpotQA, whose mean gain is 0.6. Four agent-built systems score below naive BM25 on MH-RAG.**
  - Context: The broad suite exposes both specialization and failures that the aggregate score hides. Gains are strongest on knowledge-graph and domain-specific tasks, whereas some multi-hop settings remain difficult.
  - Evidence: [b00125-282d9eb2ec] “On WebQSP, all nine configurations outperform the reference system, by 14.1 points on average.”; [b00125-282d9eb2ec] “On HotpotQA, the best configuration gains 13.0 points, but only three outperform the reference system. The mean gain is just 0.6 points.”; [b00126-4449032e57] “On MH-RAG, four agent-built systems score below naive BM25 RAG.”
- **Iteration usually finds improvements but does not reliably retain or generalize them. Among 77 comparable builds, 72 improve by at least one point at some stage and the median first-to-last gain is 5.5 points; nevertheless, 20 finish at least one point below their observed peak. GPT-5.6 Luna has the largest median development gain, 10.0, but ranks tenth on hidden tests.**
  - Context: These are within-build self-check measurements using Qwen3.5-4B, not direct causal estimates of learning efficiency. Question selection differs, and the last eligible check may not be the frozen submission.
  - Evidence: [b00143-70a3d55585] “Their median net gain in development score from the first to the last observed version (Δdev) was 5.5 points.”; [b00143-70a3d55585] “72 of the 77 builds (93.5%) improved on their first score by at least one point at some stage”; [b00143-70a3d55585] “fell at least one point below it in 20.”; [b00144-1507ba40f8] “GPT-5.6 Luna had the largest median net gain on its own development questions (10.0 points), yet it ranked tenth on the hidden tests”
- **Higher accuracy carries a latency cost. Every agent-built system is slower than Reference RAG; agent latency ranges from 0.50 to 2.01 seconds per question versus 0.35 for Reference RAG and 0.10 for naive BM25. Several systems are strictly dominated in the score–latency plane.**
  - Context: Latency includes retrieval-time model calls, rewriting, multi-step retrieval, and reranking, but excludes final answer generation. Thus the benchmark exposes a deployment trade-off not represented by the accuracy ranking.
  - Evidence: [b00132-8fabc7749f] “Every agent-built system takes longer on average to retrieve evidence than Reference RAG.”; [b00132-8fabc7749f] “Mean retrieval latency ranges from 0.50 to 2.01 seconds per question.”; [b00132-8fabc7749f] “This is 1.4 to 5.8 times the reference system’s mean of 0.35 seconds. Naive BM25 RAG takes 0.10 seconds per question.”; [b00134-f4acc3bcc4] “For each of the other five configurations, at least one system retrieves evidence faster and scores higher.”
- **When given existing human-designed implementations, GPT-6.1 Sol improves all seven tested starting systems by 7.4 to 26.4 points, averaging 16.6; DeepSeek improves them by 3.9 to 12.1 points, averaging 8.9. However, a separate CWQ repeat regresses from 34.58 to 33.20.**
  - Context: The agents receive code, dependencies, indexes, and interfaces and must preserve each method’s core mechanism. This tests maintenance and adaptation rather than from-scratch construction, but it uses only one reported build per agent-task pair plus one noted repeat.
  - Evidence: [b00153-5d60c42587] “GPT-6.1 Sol gains 7.4 to 26.4 points, with a mean of 16.6.”; [b00153-5d60c42587] “DeepSeek gains 3.9 to 12.1 points, with a mean of 8.9.”; [b00153-5d60c42587] “In a separate repeat on CWQ, the score fell from 34.58 to 33.20.”

## Experimental evaluation

### Datasets

- Nine tasks: NQ; HotpotQA, MuSiQue, and MH-RAG; PubMedQA and QASPER; FEVER; WebQSP and CWQ. They span five task categories and use supplied corpora with retained training and hidden-test examples.
  - Evidence: [b00051-b5126768fc] “the task suite in AutoRAGBench consists of nine benchmarks spanning open-domain question answering (QA), document-based multi-hop QA, domain-specific QA, fact verification, and knowledge-graph QA.”; [b00053-af5fca95e2] “Open-domain QA NQ 21,015,324 10,000 1,000 EM”
- Training sets are capped where applicable, while test sets are generally capped separately; corpus record types differ across benchmarks, limiting direct interpretation of corpus-size comparisons.
  - Evidence: [b00051-b5126768fc] “For each benchmark, we retain up to 10,000 training examples and 1,000 test examples to ensure comparable evaluation scales across tasks.”; [b00051-b5126768fc] “record types varying across benchmarks (e.g., passages, full papers, and news articles).”

### Baselines

- Closed-book answering without retrieved evidence.
  - Evidence: [b00104-ac4cc031b2] “The answering models answer each question without evidence, relying only on their parametric knowledge.”
- Naive BM25 RAG using roughly 200-word passages and the top five retrieval results.
  - Evidence: [b00105-0c52b9fe34] “This baseline splits the corpus into passages of about 200 words, indexes them with BM25 [52], and returns the top five passages for each question.”
- Reference RAG combining sparse and dense retrieval, reciprocal-rank fusion, reranking, and one auxiliary follow-up query on multi-hop tasks.
  - Evidence: [b00106-858a060386] “This baseline combines BM25 and bge-base-en-v1.5 [53] dense retrieval over the same passages using reciprocal rank fusion”
- A composite Human-SOTA envelope constructed from adapted human-designed RAG methods; it is neither one system nor an upper bound and uses a longer development limit.
  - Evidence: [b00107-3b5727d581] “The composite is a per-task envelope over these implementations, not a single deployable system or an upper bound on human-designed RAG.”; [b00107-3b5727d581] “Their 24-hour development limit differs from the agents’ six-hour budget.”
- Agentic AutoRAG and FlashRAG as automated searches over configurable or predefined pipeline spaces.
  - Evidence: [b00108-a9d4d9acca] “We compare agents with Agentic AutoRAG [20] and FlashRAG [21].”; [b00108-a9d4d9acca] “The FlashRAG baseline automatically evaluates predefined single-pass and multi-step retrieval pipelines”

### Metrics

- Task-specific EM, token F1, label accuracy, and Hits@1, normalized as prescribed for relevant tasks.
  - Evidence: [b00059-02faf057cc] “NQ and MH-RAG use exact match (EM)”; [b00059-02faf057cc] “HotpotQA, MuSiQue, and QASPER use answer token F1”; [b00059-02faf057cc] “FEVER and PubMedQA use label accuracy (Acc.). WebQSP and CWQ use Hits@1”
- Scores on a 0–100 scale, averaged over answering models and then equally over nine tasks.
  - Evidence: [b00078-5f9a3d7d7d] “We report scores on a 0–100 scale. The overall score is the unweighted mean of the nine task scores”
- Rank stability across five held-out answering models.
  - Evidence: [b00102-f2147b65a0] “We use five language models as answering models”; [b00081-4c319ff88e] “We assess rank stability by comparing these orderings across answering models.”
- Mean retrieval latency, excluding final answer generation.
  - Evidence: [b00082-d5236c6ae2] “This latency excludes final answer generation by G.”
- Development progress and regression measured by first-to-last score change and peak-to-last drop, plus activity time, tokens, and API spending.
  - Evidence: [b00093-6f7d630878] “We measure the change in score from the first observed version to the last (Δdev) and the drop from the highest observed score to the last (Δdrop).”; [b00096-dfa71f2e7a] “We measure how much time each development activity takes and how much each agent spends on API calls across tasks.”

### Ablations

- A paired HotpotQA validation check isolates title expansion within one improved HyDE system; answer F1 rises from 77.58 to 78.86 on 200 questions. This is a narrow component check, not a systematic benchmark-wide ablation.
  - Evidence: [b00155-3b78e0cea2] “In a paired check on 200 validation questions, title expansion raises Qwen3.5-4B answer F1 from 77.58 to 78.86.”

### Negative results

- Final development checks can regress from earlier peaks.
  - Evidence: [b00143-70a3d55585] “fell at least one point below it in 20.”
- Large self-check gains need not predict hidden-test rank.
  - Evidence: [b00144-1507ba40f8] “GPT-5.6 Luna had the largest median net gain on its own development questions (10.0 points), yet it ranked tenth on the hidden tests”
- Some agent systems underperform naive retrieval on an individual task.
  - Evidence: [b00126-4449032e57] “On MH-RAG, four agent-built systems score below naive BM25 RAG.”
- FlashRAG fails to complete HotpotQA indexing within the build deadline.
  - Evidence: [b00158-6d84d15064] “FlashRAG did not finish indexing HotpotQA within six hours.”
- A repeated CWQ improvement run produces a lower score than its starting system.
  - Evidence: [b00153-5d60c42587] “In a separate repeat on CWQ, the score fell from 34.58 to 33.20.”


## Limitations

- Cross-configuration rankings confound model and harness; only within-harness model comparisons isolate the harness, and no factorial model-by-harness study is reported.
  - Evidence: [b00127-7146f4f0bf] “Cross-harness rankings compare complete agent configurations because both the LLM and harness change.”
- The composite Human-SOTA comparison is not a controlled estimate of agent superiority over human engineering: it is a per-task envelope of adapted systems, uses a different development budget, and may not reproduce original-paper results.
  - Evidence: [b00107-3b5727d581] “The composite is a per-task envelope over these implementations, not a single deployable system or an upper bound on human-designed RAG.”; [b00107-3b5727d581] “Its scores need not reproduce the results reported in the original papers.”
- The reported strategy frequencies are observational and do not establish which components cause gains; the labels also lack completed second-coder verification.
  - Evidence: [b00137-93c62d1f2e] “A second coder has yet to verify the labels.”; [b00140-705e7d4d9c] “Measuring their effects would require component ablations.”
- Development-trajectory comparisons are not standardized across builds: question sets can differ, checks may not match frozen submissions, and selection and eligibility differ.
  - Evidence: [b00095-309abd3385] “question sets can differ across builds, and the last observed check need not evaluate the exact system frozen at the deadline.”; [b00144-1507ba40f8] “Differences in question selection and check eligibility limit comparisons of learning efficiency across builds.”
- Automated-framework comparisons are constrained by an incomplete adapter and search-space/indexing limits, weakening attribution of the observed gap to open-code agency itself.
  - Evidence: [b00160-12cf1bade9] “Our adapter omits some retrieval and generation diagnostics or leaves them at their defaults”; [b00162-22d3c372c6] “Indexing time and token limits further restrict the search.”
- The activity analysis covers only Codex CLI builds, and its labeling rules were partly developed with the labeling model; independent human validation remains unfinished.
  - Evidence: [b00147-29f98ea810] “For the 36 Codex CLI builds, we assign elapsed time (including waits) and output tokens to Prepare, Code, Run, Test, or Analyze”; [b00147-29f98ea810] “The labeling model helped develop the rules, and independent human validation remains open.”
- The supplied blocks report point estimates but no repeated main builds, confidence intervals, or variance estimates; the isolated CWQ repeat demonstrates that run-to-run reversals can occur.
  - Evidence: [b00153-5d60c42587] “In a separate repeat on CWQ, the score fell from 34.58 to 33.20.”

## Reproducibility

**Status:** partial

The experimental protocol is unusually concrete and the authors claim to release code and data, making structural reproduction plausible. Exact numerical reproduction remains uncertain because the evaluated agents and harnesses may be versioned services, main runs appear unreplicated, and several critical prompts, adaptations, audit details, and immutable environment specifications are absent from the supplied material.

**Available artifacts**

- The paper states that code and data are released on GitHub.
- A project website is identified.
- The task suite, build budgets, container resources, retrieval interface, evidence limits, answering models, prompts settings, latency handling, and baseline designs are described.
- Development trajectories and final systems are said to be recorded and audited.

**Missing pieces**

- No commit hash, immutable archive, software lockfile, or artifact license is stated in the supplied blocks.
- Exact model checkpoints, provider-side model snapshots, API versions, and full harness versions are not consistently specified in the supplied blocks.
- Random seeds and repeated-run protocol for the main experiment are not stated.
- The full common task prompt, task-specific answering instructions, integrity-audit prompt, and manual audit rubric are not included in the supplied blocks.
- No confidence intervals, variance estimates, or main-result replication counts are reported.
- The availability of raw trajectories, frozen submissions, audit decisions, and per-question outputs is not established by the supplied blocks.
- Exact adaptations for every Human-SOTA and automated-framework baseline are not fully specified in the supplied blocks.

## AIDB assessment

- Novelty: High at the benchmark-design level: the work shifts evaluation from selecting predefined RAG configurations to autonomous construction in an open code space, while evaluating both frozen systems and their development trajectories. The novelty claim itself is author-stated and is not independently verified here.
- Usefulness: High for comparing complete RAG-building agents under a standardized resource budget and for identifying task-specific strengths, latency trade-offs, iteration regressions, and failure modes. Lower for selecting individual retrieval components or estimating pure model capability because configurations confound model and harness and component ablations are sparse.
- Confidence: medium
- Recommended action: read
- Rationale: The benchmark addresses an important emerging capability with broad tasks, hidden tests, multiple answering models, explicit latency measurement, process traces, and strong baseline coverage. The principal result is consequential, but adoption as a definitive leaderboard should wait for repeated runs, immutable artifacts, independent label validation, component ablations, and more controlled model–harness and human-baseline comparisons.

## Uncertainties

- **How much of each configuration’s score is attributable to the underlying LLM versus its harness?** — AIDB cannot infer a model ranking or select a harness independently from results on complete configurations.
  - Evidence: [b00127-7146f4f0bf] “Cross-harness rankings compare complete agent configurations because both the LLM and harness change.”
- **How stable are the main scores across independent six-hour builds?** — Without repeated main runs, small rank gaps and task-specific conclusions may reflect stochastic development paths.
  - Evidence: [b00153-5d60c42587] “In a separate repeat on CWQ, the score fell from 34.58 to 33.20.”
- **Which learned components or evidence-control decisions actually cause the leading configurations’ gains?** — Observed strategy prevalence cannot guide component adoption without controlled removals or substitutions.
  - Evidence: [b00140-705e7d4d9c] “These counts describe strategy choices in the observed builds. Measuring their effects would require component ablations.”
- **How much does repeated exposure to development questions inflate self-check gains?** — Trajectory scores may overstate genuine iterative learning and obscure generalization failures.
  - Evidence: [b00144-1507ba40f8] “Luna ran 85% of its self_check commands on the full development file, compared with at most 29% for any other configuration.”; [b00144-1507ba40f8] “Agents may reuse training examples.”
- **How reliable are the automated integrity checks and strategy/activity annotations?** — Undetected violations could bias scores, while annotation error could distort process conclusions.
  - Evidence: [b00067-3804a7f4af] “We use DeepSeek to automatically check these trajectories and systems for potential violations.”; [b00137-93c62d1f2e] “A second coder has yet to verify the labels.”

## Open questions

- Do rankings and task-level conclusions persist across multiple independent builds with confidence intervals?
- What is the factorial effect of model, harness, build budget, and available compute?
- Which specific components explain the leading systems’ gains when removed, swapped, or held constant?
- How do systems perform under production constraints that jointly penalize latency, API cost, indexing cost, memory, and answer quality?
- Do the conclusions transfer to multilingual, multimodal, continuously updated, private, or adversarial corpora?
- Can development feedback be standardized with fixed, untouched validation partitions to reduce repeated-question bias?
- How sensitive are results to the five answering models and to the common evidence-packing policy?
- What fraction of integrity-audit flags are true positives and false negatives under independent human review?

## Proposed AIDB experiments

- **Hypothesis:** The leading configuration’s advantage is reproducible rather than a consequence of a favorable single development trajectory.
  - Baseline: Repeat GPT-6.1 Sol with Codex CLI, GPT-6 Sol with Codex CLI, Reference RAG, and the composite’s selected per-task methods under the published protocol, using independent clean builds and identical hidden evaluation.
  - Primary metric: Mean nine-task score with a confidence interval over independent builds; secondary outcomes are per-task win probability, retrieval latency, and failure rate.
  - Stop condition: Stop after enough independent builds to estimate every leading pairwise mean-score difference with a confidence interval narrow enough to determine whether its sign is stable; otherwise report the comparison as inconclusive.
- **Hypothesis:** Task-adaptive learned scorers and per-question evidence control causally explain a substantial share of the two leading configurations’ gains.
  - Baseline: For each frozen leading system, compare the intact system with matched variants that remove learned classifiers/scorers, disable per-question evidence adjustment, and replace both with the Reference RAG mechanism while preserving all other code and budgets.
  - Primary metric: Change in hidden-test task score, accompanied by change in mean retrieval latency.
  - Stop condition: Stop when every targeted component has a paired ablation on every task where it is used and repeated evaluations show whether the score effect is consistently positive or indistinguishable from zero.
- **Hypothesis:** A fixed untouched validation partition reduces apparent development gains but improves selection of the final frozen version and hidden-test generalization.
  - Baseline: Compare the published flexible self_check workflow with a workflow using disjoint tuning and fixed validation sets, identical agents, tasks, compute, prompts, and build time.
  - Primary metric: Hidden-test score of the frozen submission; secondary metrics are development-to-hidden generalization gap and peak-to-final regression frequency.
  - Stop condition: Stop after repeated builds provide a stable estimate of the difference in hidden-test score and regression frequency; reject the hypothesis if fixed validation does not improve either outcome.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:51:00.831840+00:00`
- Document SHA-256: `86322b4c1aaf856e00ba01b5a68eb5f5e734e4a67d4bfa179da7721eb235fbe8`
- Metadata SHA-256: `7da5ebd1cc67444dadac4e1e2f1c39725014df2599d3fc7197c80c6ac0a18aef`
- Blocks: 245
- Deterministic repair attempts: 1
