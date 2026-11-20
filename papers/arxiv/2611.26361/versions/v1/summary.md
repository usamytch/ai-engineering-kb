# How Much Should an Agent Remember? Deployment Lessons from Self-Distilled Memory for LLM Agents

## Executive summary

The paper studies self-distilled procedural memory for LLM agents: lessons are extracted from train/dev trajectories, consolidated into provenance-bearing guidelines, then injected wholesale or selected at inference. Its strongest controlled evidence is model-dependent dose response: DeepSeek-V3.2 improves monotonically to the full set, while gpt-oss-120b does better with a small retrieved subset than with all guidelines. The work is unusually valuable for documenting failures—harmful high-support advice, lost provenance, noisy single runs, scaffold confounding, and silent infrastructure faults. However, configuration selection used test_normal because no held-out validation split remained, most central results are single runs, and the system lacks automatic correctness, contradiction, staleness, or recency handling. The deployment evidence is encouraging but mixed: the clearest replicated CUGA gain comes with GLM-5.3-Flash, while GPT-4.1 deltas remain below the paper’s own noise threshold.

## Problem

**Statement.** Long-horizon LLM agents repeatedly make procedural rather than factual errors. The paper asks whether an agent can improve by distilling its own trajectories into reusable guidance, and how much such memory should be delivered to models of different capability.

**Why it matters.** Recurring mistakes such as incorrect pagination, wrong entity resolution, duplicate side-effecting calls, and answering when no answer was requested can reduce reliability in deployed agents. A memory mechanism must therefore improve completion without overwhelming weaker models, corrupting provenance, or silently introducing harmful rules.

**Scope.** The study covers an offline extraction–consolidation–delivery pipeline, primarily measured with the AppWorld reference ReAct agent and six memory-enabled models. It also reports CUGA evaluations on AppWorld and the retail split of τ-bench, plus one qualitative watsonx Orchestrate transfer trace. It does not establish performance for arbitrary agent architectures, continually updated unattended memory, or production populations at scale.

## Method

The agent is run on benchmark train and dev tasks, retaining successful and failed trajectories. The same model used by the agent extracts one to three imperative lessons per trajectory. Lessons are embedded, clustered by source-task embeddings, and merged only within clusters; uncovered lessons pass through unchanged. Consolidation conserves total support and retains evidence polarity and provenance. At inference, the system either injects all guidelines or combines an always-present high-support core with task-similar retrieved guidelines, deduplicating candidates. No separate teacher model or human labeling is used.

### Key components

- Trajectory capture through instrumented clients, observability-store synchronization, or an MCP submission tool.
- Outcome-grounded lesson extraction from both successes and failures; success polarity comes from the evaluator rather than model self-report.
- Support-conserving consolidation that clusters near-duplicates, merges equivalent advice, and carries uncovered lessons through unchanged.
- Static full-memory injection or dose-controlled retrieval using support, source-task similarity, and deduplication.
- Pluggable storage and MCP delivery through tools including get_guidelines, get_relevant_guidelines, and save_trajectory.
- Operational checks added after failures: conservation regression tests, per-task exception handling, minimum model-call assertions, progress watchdogs, and store-growth checks.

### Assumptions

- Benchmark evaluator outcomes are valid labels for whether extracted evidence came from successful or failed behavior.
- Train/dev trajectories are representative enough to produce guidance transferable to the test tasks.
- Source-task embedding similarity is useful for retrieval, although the reported task-level analysis did not show it predicting improvement.
- Using the same model for acting, extraction, and consolidation represents the intended self-improvement deployment setting.
- Task and scenario completion changes can be interpreted only relative to run-to-run noise and a fixed agent scaffold.

## Main claims

- **The useful memory dose depends on model capability: a capable model can benefit from the full long tail, whereas a weak model may benefit more from a selected subset.**
  - Evidence: [b00044-9504336a83] “A strong model with headroom keeps improving as memory grows.”; [b00044-9504336a83] “Its best result comes from about 29 selected guidelines: 55.4 TGC, the mean of two runs (56.0 and 54.8).”
- **Aggressive compression loses valuable situational guidance; lossless storage should be paired with selection at delivery rather than indiscriminate full injection.**
  - Evidence: [b00054-c7503cc682] “Those twelve gave DeepSeek +2.9 TGC. The full set of 191 gave +9.5 and more than doubled the SGC gain.”; [b00055-35b6b962a7] ““Keep everything” is only right when delivery can select.”
- **Support is a recurrence signal, not a correctness guarantee, so unattended memory requires an additional correctness or recency mechanism.**
  - Evidence: [b00063-8bac99b4d3] “Support counts how often a lesson was derived. That is evidence of generality, not of correctness.”; [b00063-8bac99b4d3] “We would not run an unattended memory loop without one.”
- **Fair memory-system comparisons require a fixed agent scaffold, repeated runs for small deltas, and token reporting alongside accuracy.**
  - Evidence: [b00070-4a45c3a622] “The memory contributions are comparable, and the headline gap is mostly scaffold.”; [b00067-682747ee33] “We treat differences under about five tasks as noise.”; [b00071-2c344c8a1e] “We report per-task tokens alongside accuracy in every table, and we lead with deltas.”

## Results

- **On AppWorld test_normal, DeepSeek-V3.2 rose from 79.8 TGC without memory to 89.3 TGC with all 191 guidelines; SGC rose from 64.3 to 80.4. The hard-split improvement was also substantial, from 60.4 to 72.9 TGC and from 41.7 to 58.3 SGC.**
  - Context: This is the paper’s strongest dose-response result for the reference ReAct scaffold, although individual adjacent dose changes were within noise and the configurations were evaluated directly on test_normal.
  - Evidence: [b00044-9504336a83] “DeepSeek-V3.2 climbs 79.8 → 82.7 → 83.9 → 85.7 → 89.3 TGC as the injected set grows from 0 to 12 to 19 to 47 to all 191 guidelines.”; [b00044-9504336a83] “SGC rises from 64.3 to 80.4.”; [b00044-9504336a83] “The gain holds on the hard split (60.4 → 72.9 TGC, 41.7 → 58.3 SGC).”
- **For gpt-oss-120b, full injection raised TGC from 39.9 to 51.2, but retrieval of about 29 guidelines achieved mean TGC 55.4 across two runs, with 116K tokens per task versus 110K at baseline. This shows a non-monotonic dose response for the weakest tested model.**
  - Context: The selected configuration was chosen among configurations run on test_normal, so its advantage over the fixed all-guidelines rule is exploratory rather than clean held-out model selection.
  - Evidence: [b00044-9504336a83] “gpt-oss-120b starts at 39.9. With all 199 guidelines it scores 51.2.”; [b00044-9504336a83] “Its best result comes from about 29 selected guidelines: 55.4 TGC, the mean of two runs (56.0 and 54.8).”; [b00044-9504336a83] “That is seven tasks above the full set, at essentially baseline token cost (116K vs. 110K per task).”
- **Compression was materially worse for DeepSeek-V3.2: 12 compressed guidelines produced +2.9 TGC, whereas 191 losslessly consolidated guidelines produced +9.5 TGC; 144 of the full guidelines had support one.**
  - Context: This ablation supports retaining rare situational lessons for capable models, but does not isolate which support-one guidelines caused the gain.
  - Evidence: [b00051-3dc0d216af] “†Only the 12-guideline compressed set was run for Opus.”; [b00054-c7503cc682] “Those twelve gave DeepSeek +2.9 TGC. The full set of 191 gave +9.5 and more than doubled the SGC gain.”; [b00054-c7503cc682] “The difference is the 144 guidelines with support one.”
- **A high-support pagination guideline caused a concrete regression because the agent assumed a page limit of 20 while the API default was 5. Manual rewriting recovered the task and raised hard-tier TGC from 66.7 to 73.0.**
  - Context: This is a consequential negative result demonstrating that frequency-based support can amplify incorrect advice. The fix was manual, and the pipeline still lacks an automatic harm or contradiction signal.
  - Evidence: [b00062-1047b7cd4f] “It assumed a limit of 20, while the API’s default page size was 5.”; [b00062-1047b7cd4f] “That was a regression on a task the baseline had passed. We fixed it by hand.”; [b00062-1047b7cd4f] “The task recovered, and hard-tier TGC rose from 66.7 to 73.0.”
- **In the repaired CUGA integration with GLM-5.3-Flash, the full 164-guideline set increased mean TGC from 87.8 to 93.2 and SGC from 84.8 to 88.4 over two runs per arm, while tokens per task increased by 36%. A 29-guideline subset remained within noise of baseline.**
  - Context: This replicated deployment-scaffold result supports the strong-model/full-memory pattern outside the reference ReAct agent, but its evidence remains limited to two runs per arm.
  - Evidence: [b00084-c94dacc9f3] “280 lessons, consolidated losslessly into 164 guidelines.”; [b00084-c94dacc9f3] “The full set raises TGC from 87.8 to 93.2, about nine tasks, and SGC from 84.8 to 88.4.”; [b00090-d4b0175813] “Table 6: CUGA with GLM-5.3-Flash on AppWorld test_normal, mean of two runs per arm.”; [b00084-c94dacc9f3] “The cost is 36% more tokens per task.”; [b00084-c94dacc9f3] “The 29-guideline sup3 subset stays within noise of the baseline.”

## Experimental evaluation

### Datasets

- AppWorld: nine simulated applications, 457 APIs, and 750 Python-execution tasks. The main evaluation uses test_normal with 168 tasks; test_challenge with 417 tasks is used where noted. Memory is mined only from train/dev trajectories.
  - Evidence: [b00039-72890f6e6f] “AppWorld simulates nine applications (email, payments, music, shopping, and others) behind 457 APIs and about a hundred simulated people”; [b00039-72890f6e6f] “We use test_normal (168 tasks) throughout and test_challenge (417 tasks) where noted.”; [b00039-72890f6e6f] “All memory is mined from train/dev only.”
- The CUGA deployment evaluation also uses the retail split of τ-bench, with 74 training tasks and 40 test tasks.
  - Evidence: [b00083-f9b6d5f01c] “the retail split of τ-bench (Yao et al. 2025; Barres et al. 2026), a customer-service suite of 74 training and 40 test tasks”

### Baselines

- No-memory variants of the same reference ReAct scaffold are the primary baselines for within-model AppWorld comparisons.
  - Evidence: [b00074-7c8cf6a031] “DeepSeek-V3.2 ACE-ReAct, no memory 0 72.0 57.1 221K”; [b00074-7c8cf6a031] “ReAct, no memory 0 79.8 64.3 148K”
- ACE is the prior memory-system comparator, but its ACE-ReAct scaffold has a different prompt and worked examples, making final-score comparisons confounded unless expressed as lift over each method’s own baseline.
  - Evidence: [b00070-4a45c3a622] “ACE’s ReAct variant carries a different prompt template, with a playbook slot and a longer set of worked examples.”; [b00070-4a45c3a622] “Measured as lift over its own baseline, ACE gains +8.4/+16.2 and ours +9.5/+16.1.”
- CUGA evaluations compare memory-enabled arms against Base CUGA or no-memory CUGA using the same model.
  - Evidence: [b00085-cfa88cb887] “Method TGC SGC Steps/Task Base CUGA 71.03 54.76 9.63 Ours (lossless) 72.42 58.93 9.31”; [b00089-c20b9fd933] “Arm Guid. TGC SGC Steps Tok/task No memory 0 87.8 84.8 33.8 219K”

### Metrics

- TGC is the fraction of tasks passing every evaluation check; SGC is the stricter fraction of scenarios for which every task variant passes.
  - Evidence: [b00039-72890f6e6f] “TGC is the fraction of tasks that pass all of their evaluation checks.”; [b00039-72890f6e6f] “SGC is the stricter fraction of scenarios in which every task variant passes.”
- Efficiency measures include tokens per task, steps per task, and—on τ-bench—average turns per task.
  - Evidence: [b00073-822aacac17] “The overhead is almost entirely input-side, because the injected set is re-sent on every reasoning step.”; [b00087-f4f6cac55b] “Avg turns / task 31.3 30.8 −0.5”
- τ-bench additionally reports pass^3, requiring all three trials for a task to pass.
  - Evidence: [b00088-541f82c282] “the stricter pass^3 measure (which credits a task only when all three of its trials pass)”

### Ablations

- Memory-dose ablation for DeepSeek-V3.2 compares 0, 12, 19, 47, and 191 injected guidelines; the endpoints differ by 16 tasks.
  - Evidence: [b00044-9504336a83] “DeepSeek-V3.2 climbs 79.8 → 82.7 → 83.9 → 85.7 → 89.3 TGC as the injected set grows from 0 to 12 to 19 to 47 to all 191 guidelines.”; [b00044-9504336a83] “the endpoints are 16 tasks apart.”
- For gpt-oss-120b, the study compares all 199 guidelines, a 24-guideline core, and retrieval of about 29 guidelines.
  - Evidence: [b00044-9504336a83] “With all 199 guidelines it scores 51.2. That is no better than the 53.6 it scores with a 24-guideline core”; [b00044-9504336a83] “Its best result comes from about 29 selected guidelines: 55.4 TGC”
- The consolidation ablation contrasts a compressed 12-guideline set with the full lossless 191-guideline set for DeepSeek-V3.2.
  - Evidence: [b00044-9504336a83] “DeepSeek-V3.2 climbs 79.8 → 82.7 → 83.9 → 85.7 → 89.3 TGC as the injected set grows from 0 to 12 to 19 to 47 to all 191 guidelines.”; [b00054-c7503cc682] “Those twelve gave DeepSeek +2.9 TGC. The full set of 191 gave +9.5 and more than doubled the SGC gain.”

### Negative results

- GLM-5 was saturated: its score was unchanged with 72 guidelines.
  - Evidence: [b00044-9504336a83] “GLM-5 is saturated: it scores 87.5 with or without its 72 guidelines.”
- Gemma-4-31B showed no overall benefit and was harmed by an over-tight core.
  - Evidence: [b00044-9504336a83] “Gemma-4-31B is too weak to apply memory: a wash overall, and hurt by an over-tight core.”
- Task–guideline embedding similarity did not distinguish improved from regressed tasks.
  - Evidence: [b00066-159e9e3ff1] “Improved and regressed tasks had mean retrieval cosine of 0.463 and 0.468.”
- An initial 50-task CUGA evaluation found no statistically significant effect, but the write path was broken and the store never grew beyond its seed.
  - Evidence: [b00082-67c31c3c0f] “An initial 50-task evaluation found no statistically significant effect on pass rate or step count.”; [b00082-67c31c3c0f] “the memory store never grew past its seed.”
- The repaired GPT-4.1 CUGA gains on two benchmarks were below the paper’s own noise floor and do not establish effect size.
  - Evidence: [b00083-f9b6d5f01c] “Each of these deltas is about two tasks per trial. That is below the noise floor of Insight 5.”; [b00083-f9b6d5f01c] “They do not establish its size.”


## Limitations

- Configuration selection is test-contaminated: dev was consumed for memory mining, leaving no held-out split, and multiple configurations were compared directly on test_normal.
  - Evidence: [b00039-72890f6e6f] “Because dev is consumed by mining, no held-out split was left for choosing a configuration.”; [b00039-72890f6e6f] “We compared configurations directly on test_normal”
- Most benchmark results are single runs despite meaningful stochastic variation; the authors estimate that differences below about five tasks are noise.
  - Evidence: [b00039-72890f6e6f] “Results are single runs, the benchmark’s convention, except where noted.”; [b00067-682747ee33] “We treat differences under about five tasks as noise.”
- The pipeline has no automatic mechanism for detecting contradicted, stale, or harmful guidelines, making unattended continual operation unsafe.
  - Evidence: [b00063-8bac99b4d3] “Our pipeline has no notion of a guideline being contradicted, stale, or harmful.”; [b00063-8bac99b4d3] “We would not run an unattended memory loop without one.”
- Cross-method comparison with ACE is confounded by different agent scaffolds, so absolute final-score gaps cannot be attributed solely to memory.
  - Evidence: [b00070-4a45c3a622] “But the two agents’ no-memory baselines were 79.8 and 72.0.”; [b00070-4a45c3a622] “The memory contributions are comparable, and the headline gap is mostly scaffold.”
- The watsonx Orchestrate evidence is a single uncontrolled qualitative example with different source and transfer inputs.
  - Evidence: [b00092-eafcb9fc4c] “Because the inputs differ, the step and latency values are descriptive rather than a controlled estimate of improvement.”; [b00092-eafcb9fc4c] “This is a single qualitative example rather than a benchmark.”
- Full injection can impose substantial input-token cost because the guideline set is resent at every reasoning step.
  - Evidence: [b00073-822aacac17] “The full 191-guideline set costs 78% more tokens per task than baseline.”; [b00073-822aacac17] “The overhead is almost entirely input-side, because the injected set is re-sent on every reasoning step.”

## Reproducibility

**Status:** partial

The described open-source implementation and detailed operational narrative make the pipeline inspectable in principle, but the supplied paper evidence is insufficient for exact numerical reproduction. Reproduction would require reconstructing prompts and configurations and obtaining or regenerating trajectory-level artifacts. The single-run primary results and test-set configuration search further limit confirmatory reproducibility.

**Available artifacts**

- The paper states that the pipeline is available in the open-source altk-evolve library.
- It names concrete configuration controls: consolidation_mode, min_support, core_support, retrieval_top_k, and injection_mode.
- It specifies benchmark splits, principal model/scaffold combinations, guideline counts, completion metrics, token costs, and selected repeated-run ranges.
- The references identify support-conserving consolidation and dosage-aware retrieval changes in named pull requests.

**Missing pieces**

- Exact extraction, consolidation, and inference prompts are not supplied in the document blocks.
- Model endpoint versions, decoding settings beyond the temperature-zero discussion, seeds, and full runtime environment are not comprehensively specified.
- The exact per-model configurations behind every reported point are not fully enumerated.
- Raw trajectories, extracted lessons, consolidated guideline sets, task-level outcomes, and evaluation logs are not stated to be released.
- No held-out configuration-selection split is available for the primary AppWorld study.
- Most central results lack repeated-run distributions, confidence intervals, or formal significance tests.

## AIDB assessment

- Novelty: The extraction-and-consolidation method is explicitly not claimed as the main novelty. The original contribution is the deployment-centered empirical account: model-dependent memory dose, preservation of long-tail guidance, provenance invariants, recurrence-versus-correctness failure, scaffold confounding, cost accounting, and silent operational faults.
- Usefulness: High for teams building agent memory systems. The paper supplies actionable design and evaluation practices and exposes failure modes often omitted from benchmark reports. Its quantitative conclusions are strongest for the large DeepSeek dose trend and the replicated GLM-5.3-Flash CUGA result; smaller deltas should not drive adoption decisions.
- Confidence: medium
- Recommended action: read
- Rationale: The paper deserves close reading as an engineering and evaluation guide, but not unqualified adoption of its performance claims. Test-set configuration selection, mostly single-run measurements, scaffold confounding, and absent correctness/recency control materially weaken causal and deployment-safety conclusions. AIDB should treat the pipeline as a promising reference design requiring independent repeated evaluation and a harm-aware maintenance layer.

## Uncertainties

- **It is unclear whether memory dose is best predicted by baseline capability itself or by correlated factors such as context handling, instruction following, extraction quality, or consolidation quality.** — A deployment policy needs a measurable selector for dose; model identity and baseline score alone may not transfer across tasks or scaffolds.
  - Evidence: [b00037-5577805092] “the model that ran the agent is also the model that extracted its lessons and consolidated them.”; [b00045-a0bde63bec] “the optimal amount is a function of capability.”
- **The marginal value and harm distribution of support-one guidelines is unresolved; aggregate compression comparisons do not identify which rare guidelines help, distract, or regress tasks.** — Safe retrieval and pruning require guideline-level causal evidence, not only aggregate support counts.
  - Evidence: [b00033-8a7472f2ca] “For DeepSeek this turns 290 lessons into 191 guidelines, of which 144 have support one.”; [b00063-8bac99b4d3] “A popular wrong lesson scores high.”
- **The apparent advantage of selected memory for gpt-oss-120b may be overestimated because configurations were selected on the same test split and the best TGC is based on only two runs.** — This is the central evidence for non-monotonicity in a weak model and directly motivates dosage-aware retrieval.
  - Evidence: [b00039-72890f6e6f] “We compared configurations directly on test_normal”; [b00051-3dc0d216af] “‡TGC is the mean of two runs (56.0, 54.8).”
- **The production effectiveness of cross-task transfer remains unquantified beyond benchmark integrations and one descriptive trace.** — Real workflows may differ from simulated benchmarks in task distribution, tool side effects, drift, and feedback availability.
  - Evidence: [b00092-eafcb9fc4c] “This is a single qualitative example rather than a benchmark.”

## Open questions

- Can a held-out validation protocol choose memory dose reliably without consuming the benchmark test split?
- Which observable model properties predict whether full, support-thresholded, or retrieval-based delivery will be optimal?
- How should guideline correctness, contradiction, recency, and task-level harm be represented and updated over time?
- Can rare support-one guidelines be selected using calibrated utility estimates rather than embedding similarity alone?
- Do the reported gains persist across repeated runs, new task distributions, changing APIs, and longer-lived production memory stores?
- How much of the gain comes from extracting from successful trajectories versus failure trajectories?
- Can static-prefix caching preserve full-memory accuracy while materially reducing billed input cost and latency?

## Proposed AIDB experiments

- **Hypothesis:** A validation-selected dose policy will retain the advantage of retrieval for weaker models and full lossless memory for stronger models on a genuinely untouched test set.
  - Baseline: Compare no memory, inject all, fixed support cores, and retrieval under the paper’s current test-selected protocol versus selection on a newly held-out validation partition.
  - Primary metric: Test-set TGC lift over no memory, accompanied by SGC, tokens per task, and the mean with a confidence interval across at least five matched runs.
  - Stop condition: Stop when every model–dose arm has at least five completed matched runs and the confidence interval for the selected policy’s TGC difference versus inject-all is narrow enough to exclude a five-task-equivalent noise band, or when a prespecified compute budget is exhausted.
- **Hypothesis:** Adding outcome-based down-voting and recency/contradiction handling will reduce guideline-induced regressions without erasing the completion gain of lossless memory.
  - Baseline: Support-only consolidation and retrieval exactly as described in the paper, compared with the same store augmented by per-guideline harm, contradiction, and recency signals.
  - Primary metric: Number of baseline-passed tasks regressed by memory, with overall TGC and SGC as co-reported guardrails.
  - Stop condition: Stop after a prespecified stream of repeated and shifted tasks when the augmented system either reduces regressions without a statistically credible TGC loss, or fails to reduce regressions across two consecutive evaluation checkpoints.
- **Hypothesis:** Guideline-level utility learned from counterfactual task replays will outperform source-task cosine similarity for selecting rare, support-one guidance at equal token cost.
  - Baseline: The reported retrieval scheme using a high-support core plus source-task embedding similarity and deduplication.
  - Primary metric: TGC at a matched per-task input-token budget, with calibration between predicted guideline utility and observed task outcome change.
  - Stop condition: Stop after each candidate selector has been evaluated on the same held-out tasks across at least five matched runs and either the utility selector exceeds the baseline outside the measured noise band or its confidence interval rules out a practically meaningful gain.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:10.665467+00:00`
- Document SHA-256: `82a768a9d6f9e6de33fa1ef6d0b897771223b7fb78282139e298b4066b0fb5e1`
- Metadata SHA-256: `45d54c4c310d86eb956902ef241345fc11b6724889c0ea8b52ed80fb26dbffe5`
- Blocks: 130
- Deterministic repair attempts: 0
