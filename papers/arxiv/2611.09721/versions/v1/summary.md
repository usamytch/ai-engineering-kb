# MemoryDojo: Benchmarking Poisoning Through LLM Agent Memory

## Executive summary

MemoryDojo studies how one poisoned tool observation survives, propagates through, is retrieved from, and changes behavior through agent memory across sessions. Its strongest contribution is lifecycle-aware comparison of five complete memory integrations, rather than treating retrieval as equivalent to compromise. Optimized attacks increased later-task behavioral reach for every tested system, while architecture, model, domain, insertion timing, and prior benign history materially changed outcomes. The benchmark is broad and diagnostically useful, but causal attribution to memory architecture is limited by bundled retrieval policies, budgets, and model-dependent memory processing. Reproducibility is currently partial because code and data are promised, not supplied in the document.

## Problem

**Statement.** The paper asks how different agent-memory architectures shape the persistence, retrieval, propagation, and later behavioral impact of a malicious instruction encountered once during ordinary tool use.

**Why it matters.** Persistent memory can convert a transient indirect prompt injection into behavior that recurs after the original observation has left the context window, potentially amplifying both duration and scope of harm.

**Scope.** The study covers sandboxed, synthetic, multi-session trajectories in Workspace, Travel, Banking, and Slack; five open-source memory integrations; one primary task model plus three transfer models; single poison insertion; and no evaluated defenses.

## Method

MemoryDojo concatenates compatible AgentDojo tasks into stateful trajectories, optionally prefixes them with LongMemEval-S histories, and repeatedly executes a retrieve–interact–write cycle. One attacker payload is appended to a tool observation. Native memory processing and retrieval remain enabled. The benchmark inspects post-write memory and later retrieved items, classifies poison preservation, attributes retrieval to original or descendant entries, and separately scores later execution of the attack objective. A memory-aware optimizer revises payloads in a separate synthetic environment using behavioral outcomes, coarse lifecycle evidence, and failure examples, then transfers the selected payload to benchmark runs.

### Key components

- Three trajectory collections: same-domain, cross-domain, and history-prefixed cross-domain.
- Adapters for A-MEM, Graphiti, Letta, Mem0, and Memora, preserving their native representations and retrieval mechanisms.
- Lifecycle tracing for insertion, retrieval, persistence, propagation, and joint persistence-plus-propagation.
- Behavioral measures separating trajectory-level reach, pooled later-task reach, and reach conditional on retrieval.
- Payload optimization conditioned on the memory-system description, attack objective, domain ontology, auxiliary-run feedback, and a task-utility eligibility constraint.
- Transfer and sensitivity evaluation across task models, application domains, poison timing, and accumulated benign history.

### Assumptions

- The attacker controls exactly one external-tool result but not system prompts, user requests, later tool results, benchmark tasks, utility checks, or memory implementations.
- The benchmark treats each complete memory integration—including native context selection and retrieval budget—as the comparison unit.
- LLM judgments reliably identify exact, transformed, and fragmented poison-bearing content and attack-objective completion.
- Synthetic task suites and replayed conversation histories adequately expose security-relevant behavior of deployed memory agents.
- Optimized auxiliary-environment payloads are sufficiently separated from benchmark tasks to test transfer rather than direct task leakage.

## Main claims

- **MemoryDojo contributes a comparative, longitudinal benchmark that follows poisoning through native writes and later tasks across differing memory systems.**
  - Evidence: [b00020-359583615e] “MemoryDojo performs a comparative evaluation of continued agent operation over multi-session trajectories.”; [b00020-359583615e] “it tracks subsequent task execution and native memory updates across different memory systems”
- **The evaluation distinguishes poison presence and retrieval from actual attacker-desired behavior, avoiding the assumption that retrieval itself constitutes compromise.**
  - Evidence: [b00051-f09f6a2594] “BR and BRT measure its longitudinal effect on later sessions, where the poison can only act through memory.”; [b00067-be5f6c6d7f] “However, retrieval alone does not imply behavioral reach”
- **The optimization procedure is memory-aware and selects for later behavioral reach while constraining legitimate-task utility.**
  - Evidence: [b00054-171f8fcd66] “selection maximizes auxiliary BRT subject to a utility threshold.”; [b00190-4b6a20f4cb] “retaining the seed unless the revision improves BRT.”
- **The authors conclude that susceptibility and downstream effects depend materially on the combined memory integration and model.**
  - Evidence: [b00091-ec4444307f] “with substantial variation across systems in retrieval, propagation, and behavioral effects.”; [b00215-f605c3d311] “the effect of a fixed payload depends on both the model and memory integration”

## Results

- **For GPT-5.6-Luna same-domain runs, optimization raised BRT for every memory system: A-MEM from 21.02 to 44.01, Graphiti from 7.76 to 9.31, Letta from 15.30 to 46.26, Mem0 from 7.90 to 21.02, and Memora from 20.38 to 29.76.**
  - Context: This is the strongest controlled comparison between unoptimized and memory-aware optimized payloads. Gains are not explained uniformly by retrieval: Letta’s BRT|R rose sharply, while A-MEM’s insertion and retrieval stayed broadly similar. Task utility sometimes fell, so reach improvements should be interpreted jointly with utility.
  - Evidence: [b00063-d1d007e6b8] “Table 1: Same-domain results for unoptimized and optimized poison for GPT-5.6-Luna.”; [b00064-321cf9357f] “Unoptimized A-MEM 98.92 25.27 89.84 60.28 8.01 31.71 72.25 21.02 23.39 45.70”; [b00064-321cf9357f] “Graphiti 98.39 23.12 33.43 81.86 5.49 12.66 80.49 7.76 23.21 24.73”; [b00064-321cf9357f] “Letta 98.92 24.19 64.88 77.28 1.74 20.98 69.46 15.30 23.59 16.67”; [b00064-321cf9357f] “Mem0 60.75 20.97 56.70 78.11 0.87 21.02 76.66 7.90 13.93 14.52”; [b00064-321cf9357f] “Memora 97.85 23.12 86.18 62.36 6.55 31.10 65.72 20.38 23.65 38.71”; [b00064-321cf9357f] “Optimized A-MEM 97.85 19.35 93.37 37.16 13.29 49.55 60.74 44.01 47.13 70.97”; [b00064-321cf9357f] “Graphiti 100.00 4.30 30.61 62.67 17.51 19.82 81.42 9.31 30.41 30.11”; [b00064-321cf9357f] “Letta 95.70 25.81 72.21 46.48 0.59 52.93 53.67 46.26 64.06 50.54”; [b00064-321cf9357f] “Mem0 77.42 9.68 71.65 53.94 4.33 41.73 71.77 21.02 29.33 39.78”; [b00064-321cf9357f] “Memora 98.92 24.73 92.81 47.72 12.46 39.82 74.15 29.76 32.07 66.67”
- **Retrieval was not sufficient for behavioral compromise: with GLM, Letta had 100% RSR but 15.09% BRT; with GPT-5.4-mini, Graphiti had 38.08% RSR but only 0.28% BRT.**
  - Context: This cross-model negative result validates the paper’s decision to measure behavior separately from storage and retrieval. It also shows that a fixed optimized payload’s effectiveness is jointly determined by model and memory integration.
  - Evidence: [b00215-f605c3d311] “Letta with GLM has 100% RSR and 15.09% BRT”; [b00215-f605c3d311] “With mini, Graphiti retrieves poison on 38.08% of planned later tasks but reaches only 0.28%.”; [b00214-eb599e5608] “GPT-5.4-mini uses default none reasoning”
- **Cross-domain execution occurred in four systems, but Graphiti showed 0.00 cross-domain BR and BRT; for the other systems, cross-domain BRT ranged from 2.72 to 6.37 and was below within-domain BRT ranging from 17.57 to 38.06.**
  - Context: This indicates limited but nonzero generalization of a target-domain payload into unrelated tasks. Domain relevance appears to affect both retrieval and compliance, and the bundled integrations differ substantially.
  - Evidence: [b00079-e2eca7923c] “We observe cross-domain reach in four systems”; [b00226-7c5b40d9b9] “Graphiti 96.77 30.05 25.00 10.94 36.41 7.55 0.00 0.00 0.00”; [b00226-7c5b40d9b9] “Letta 96.77 57.78 37.10 38.06 65.87 54.96 26.61 6.37 11.59”; [b00226-7c5b40d9b9] “Mem0 49.19 45.15 31.45 17.57 38.91 35.64 13.71 2.72 7.64”
- **Under history pressure, Letta produced 0.00 BRT and BR, whereas Memora retained 5.32 BRT and 45.16 BR; all systems had lower RSR and BRT than without a history prefix.**
  - Context: Accumulated benign memory weakened attacks, especially by increasing retrieval competition, but did not eliminate later-task reach in four integrations. Because the history-prefixed collection reuses cross-domain sequences, this is a meaningful pressure test, though not a randomized isolation of history content effects.
  - Evidence: [b00082-79a43d15e9] “Letta 95.97 10.48 7.94 70.47 65.22 0.00 0.00 0.00”; [b00082-79a43d15e9] “Memora 96.77 20.16 44.18 77.65 75.00 5.32 12.03 45.16”; [b00086-15547051e1] “Table 2 shows lower RSR and BRT for every system than in the cross-domain experiment without a history prefix.”

## Experimental evaluation

### Datasets

- MemoryDojo contains same-domain, cross-domain, and history-prefixed cross-domain collections built from AgentDojo task templates and cleaned LongMemEval-S histories.
  - Evidence: [b00029-f271595861] “We construct multi-session trajectories using task templates from AgentDojo”; [b00149-e7576bcbec] “We use the cleaned LongMemEval-S dataset”
- The benchmark composition totals 155 trajectories and 2,162 task sessions; recorded history sessions are additional to those task-session counts.
  - Evidence: [b00141-0e963eac56] “Total 97 155 2,162 3–60”; [b00140-6007b0bb60] “The final collection additionally contains 1,493 recorded history sessions”

### Baselines

- Unoptimized seed payloads are the primary attack baseline for evaluating memory-aware optimization.
  - Evidence: [b00062-107d0334b7] “Table 1 compares the unoptimized and optimized payloads”
- Five complete memory integrations are compared: A-MEM, Graphiti, Letta, Mem0, and Memora.
  - Evidence: [b00059-55d02f4a96] “A-MEM, Graphiti, Letta, Mem0, and Memora.”
- Model transfer uses GPT-5.4-mini, DeepSeek-V4-Flash-0731, and GLM-5.3-Flash with payloads optimized against GPT-5.6-Luna.
  - Evidence: [b00059-55d02f4a96] “we additionally evaluate GPT-5.4-mini, DeepSeek-V4-Flash-0731 (DeepSeek-AI, 2026), and GLM-5.3-Flash”; [b00059-55d02f4a96] “using the Luna-optimized payloads.”

### Metrics

- Insertion success rate classifies whether any exact, transformed, or fragmented representation of the payload is written after insertion.
  - Evidence: [b00037-fd54bcfbfb] “An exact match preserves the complete payload word for word”; [b00037-fd54bcfbfb] “𝒞+={exact,transformed,fragmented}”
- Retrieval success rate pools post-insertion sessions in which at least one returned memory item contains attributable poison.
  - Evidence: [b00039-4470140f63] “retrieval succeeds when at least one item qualifies.”
- PE, PR, and PP attribute poison-bearing retrieval to original entries, descendant entries, or both.
  - Evidence: [b00046-35d8f0fa0e] “persistence only (PE), propagation only (PR), or both (PP).”
- BR measures whether any later task is reached; BRT measures the pooled fraction of later tasks satisfying the objective; BRT|R conditions later-task reach on retrieval.
  - Evidence: [b00049-f1d7da62bc] “A run is reached if the attack objective is achieved in at least one session after insertion.”; [b00049-f1d7da62bc] “Task-level behavioral reach (BRT) measures the fraction of post-insertion tasks on which the objective is observed”; [b00060-a690320088] “later-task reach given retrieval (BRT|R)”
- Task utility uses native task checks; memory utility uses the held-out LongMemEval question after a history-prefixed trajectory.
  - Evidence: [b00052-58f50d329e] “task utility as the fraction of all task sessions that pass the benchmark’s task success checks.”; [b00052-58f50d329e] “memory utility through accuracy on the held-out LongMemEval question”

### Ablations

- Unoptimized versus memory-aware optimized payloads isolates the effect of the optimization procedure within each integration.
  - Evidence: [b00063-d1d007e6b8] “Same-domain results for unoptimized and optimized poison for GPT-5.6-Luna.”
- Three additional task models test transfer of payloads selected against the primary model.
  - Evidence: [b00072-4de51d6584] “optimization was performed using GPT-5.6-Luna, but we observe strong effects in these different models as well.”
- Midpoint insertion tests sensitivity to poison timing after earlier sessions have populated memory.
  - Evidence: [b00220-c78f6834d3] “poison inserted at the trajectory midpoint, after earlier sessions have contributed entries to memory.”
- Cross-domain trajectories and history prefixes test domain shift, trajectory length, and benign-memory pressure.
  - Evidence: [b00057-457b522075] “then consider trajectories that cross application domains and finish by adding extra memory pressure.”

### Negative results

- Retrieval frequently failed to induce the attacker objective, demonstrating that exposure is not equivalent to behavioral reach.
  - Evidence: [b00067-be5f6c6d7f] “retrieval alone does not imply behavioral reach”
- History pressure eliminated later-task reach for Letta in the reported setting.
  - Evidence: [b00086-15547051e1] “Letta, which previously had the highest in BRT, has no later-task reach.”
- Graphiti exhibited no observed cross-domain reach.
  - Evidence: [b00226-7c5b40d9b9] “Graphiti 96.77 30.05 25.00 10.94 36.41 7.55 0.00 0.00 0.00”
- Later insertion generally weakened retrieval and behavioral impact, although it did not remove the attack.
  - Evidence: [b00073-da8d9cea8e] “Delaying poison insertion until the trajectory midpoint generally reduces subsequent retrieval and behavioral impact, but does not eliminate the attack.”


## Limitations

- The study compares complete integrations rather than controlling representation, retrieval budget, context policy, and memory-side generation independently. Observed differences therefore cannot be attributed solely to architecture.
  - Evidence: [b00059-55d02f4a96] “these configurations compare complete memory integrations, including their different context-selection policies and budgets.”
- The threat model permits only one poisoned observation and excludes repeated or adaptive attacker intervention, limiting conclusions about cumulative campaigns.
  - Evidence: [b00024-61e0b99a09] “which is appended once at a single insertion point”; [b00092-4eb34ad867] “investigate multiple instances of poisoning in a trajectory”
- Evaluation is restricted to sandboxed synthetic tasks and locally hosted memory, so deployment validity and interaction with real organizational data remain untested.
  - Evidence: [b00094-8937a44077] “We limit the benchmark to sandboxed task suites, synthetic trajectories, and locally hosted memory state.”
- The paper does not evaluate defenses, despite positioning the benchmark as security infrastructure.
  - Evidence: [b00092-4eb34ad867] “systematically evaluate memory defenses against poisoning.”
- Semantic lifecycle labels and some validation steps depend on an LLM judge, but the supplied blocks do not report human agreement, judge calibration, confidence intervals, or repeated-run variance.
  - Evidence: [b00037-fd54bcfbfb] “using an LLM Judge to classify four categories.”; [b00182-0edb5de7af] “Both deterministic checks and LLM judges are used here.”
- Task agents and generative memory components are changed together in cross-model evaluation, preventing isolation of task-model sensitivity from memory-side generation sensitivity.
  - Evidence: [b00214-eb599e5608] “Task agents and generative memory components change together”

## Reproducibility

**Status:** partial

The methodological description is unusually detailed and includes formulas, configuration tables, and trajectory construction rules, but independent reproduction cannot yet be considered strong because the artifacts are promised for future release rather than available here.

**Available artifacts**

- The document specifies trajectory construction, attack insertion, lifecycle metrics, optimization stages, memory configurations, retrieval budgets, and model settings.
- The authors state an intention to release benchmark data, trajectory-construction code, memory-system integrations, and evaluation scripts.
- Run records are described as saving model, provider, and retrieval settings.

**Missing pieces**

- No released repository, benchmark package, data archive, commit identifier, or executable artifact is supplied in the provided material.
- No exact dependency versions, memory-system revisions, API snapshots, random seeds, repetition counts, uncertainty estimates, or complete optimizer budget are stated in the supplied blocks.
- The preset utility tolerance, fixed optimization-round count, full payloads, and complete prompts for judges and optimizer are not present in the supplied blocks.
- No human validation or inter-rater reliability for semantic judgments is reported.

## AIDB assessment

- Novelty: High at the benchmark-design level: the paper combines multi-session execution, native memory updates, lifecycle attribution, later-task behavioral metrics, and memory-aware payload optimization across multiple integrations. Its novelty is comparative instrumentation and longitudinal measurement, not the first demonstration of memory poisoning.
- Usefulness: High for red-teaming and regression testing agent-memory systems. The separation of insertion, retrieval, propagation, conditional compliance, and utility can locate failure stages that a single attack-success score would hide. Usefulness for architectural conclusions is moderated by bundled system configurations and model-dependent components.
- Confidence: medium
- Recommended action: adopt
- Rationale: Adopt the benchmark concepts and metric decomposition for internal security evaluation, but treat the reported system ranking as configuration-specific. Require artifact release, judge validation, repeated-run uncertainty, and controlled component ablations before using the results to select or certify a production memory architecture.

## Uncertainties

- **It is unclear how stable the reported percentages are across reruns, seeds, provider changes, and nondeterministic memory-side generation.** — Without dispersion or repeated-run statistics, modest differences between integrations or payload conditions may not represent reliable ordering.
  - Evidence: [b00199-768eb99f70] “0.1 for memory-side generation”
- **The accuracy and bias of the semantic judge for transformed or fragmented poison are unresolved.** — ISR, RSR, and attribution depend on recognizing rewritten meaning; systematic false positives or negatives could change lifecycle conclusions.
  - Evidence: [b00037-fd54bcfbfb] “a transformed match preserves its salient instruction or meaning after rewriting”; [b00037-fd54bcfbfb] “a fragmented match retains only part of that meaning.”
- **The relative contribution of representation, write transformation, retrieval budget, context ordering, and task-agent behavior remains unidentified.** — The paper supports conclusions about complete integrations, but not clean causal claims about any single architectural mechanism.
  - Evidence: [b00059-55d02f4a96] “including their different context-selection policies and budgets.”
- **Transfer beyond the selected synthetic domains, task templates, objectives, and single-payload threat model is unknown.** — Production attackers may use repeated, adaptive, less explicit, or organization-specific payloads whose persistence and detectability differ.
  - Evidence: [b00171-8163b040c4] “The domains cover workspace, travel, banking, and communication tasks.”; [b00024-61e0b99a09] “After insertion, ordinary tasks continue without further attacker intervention.”

## Open questions

- Will the released package pin exact versions and commits for every memory integration and model-facing dependency?
- How sensitive are lifecycle labels and rankings to judge model, judge prompt, and human adjudication?
- Which individual integration components cause the largest changes: write abstraction, representation, retrieval budget, expansion, reranking, or context placement?
- Do repeated low-salience poisons outperform one explicit poison under equal attacker and utility budgets?
- How do input filtering, provenance tracking, taint propagation, retrieval-time filtering, and memory deletion affect BR, BRT, and benign utility?
- Are optimized payload gains preserved under unseen objectives, languages, organizations, and real user histories?

## Proposed AIDB experiments

- **Hypothesis:** Memory representation alone explains less variation in later-task reach than retrieval policy and context budget.
  - Baseline: Reproduce each complete native integration, then run matched-budget variants with retrieval count, context-token budget, and expansion disabled or standardized while holding task and memory-side models fixed.
  - Primary metric: Change in BRT and BRT|R relative to each native integration, with bootstrap confidence intervals across trajectories.
  - Stop condition: Stop when every integration has completed the native condition and all matched-budget conditions with enough repeated runs for the confidence interval on each BRT difference to exclude effects larger than the preregistered practical threshold.
- **Hypothesis:** LLM-judge choice materially changes transformed and fragmented poison labels but has limited effect on exact-match cases.
  - Baseline: Use the paper’s GPT-5.6-Luna judge as the reference condition and compare multiple independent judges plus blinded human annotation on a stratified sample of writes and retrievals.
  - Primary metric: Class-wise precision, recall, and agreement for exact, transformed, fragmented, and not-observed labels; additionally report induced changes in ISR and RSR.
  - Stop condition: Stop after the preregistered sample size is reached and each class has enough human-labeled examples to bound its recall confidence interval within the target width.
- **Hypothesis:** A provenance-aware retrieval defense reduces later-task reach more than benign task or memory utility.
  - Baseline: Unmodified native integration and a simple retrieval-time content filter, compared against provenance tagging with taint propagation through rewritten and linked memories.
  - Primary metric: BRT reduction at matched TU and MU, with BR and false-positive removal of benign memories as secondary metrics.
  - Stop condition: Stop when all systems and trajectory collections are evaluated; reject the defense if its BRT reduction misses the preregistered target or if either utility measure falls beyond the allowed margin.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:06.038766+00:00`
- Document SHA-256: `fe2ad21164bfc5a34ac119aac8b1aad96616ca91a0238eb73fac3bd6cfc7534a`
- Metadata SHA-256: `bbafeff3bd335488b6567586dccf69aaf9749970fdafbcaf23f19464e8956365`
- Blocks: 231
- Deterministic repair attempts: 0
