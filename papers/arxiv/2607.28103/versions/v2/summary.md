# MIND: Lightweight and Effective Memory Injection Defense for LLM Agents via Intent-Aware Information Bottleneck

## Executive summary

MIND filters poisoned agent memories by comparing each turn’s hidden-state transition with the initial user intent, compressing that signal through a variational information bottleneck, and classifying it with multiple hyperplanes. Across StrategyQA/AgentPoison and MMLU/MINJA, the paper reports large average reductions in retrieval, agent-stage, and injection success rates with limited latency. Component ablations support both the bottleneck and multi-hyperplane design, but evidence is confined to two benchmarks and two attack families, depends on labeled poisoned trajectories and internal representations or a proxy encoder, and omits several details needed for exact reproduction. The method is promising for controlled memory-agent deployments, but broader adaptive-attack and black-box validation is needed before adoption.

## Problem

**Statement.** Memory-augmented agents can retrieve attacker-planted records that redirect behavior away from the initial user request. Existing defenses are framed as either repeatedly auditing memories with an LLM, which accumulates latency over long trajectories, or using lightweight detectors over redundant multi-turn information that may obscure attack signals.

**Why it matters.** A retrieved malicious record can influence several later turns while appearing plausible in isolation, potentially causing incorrect or harmful actions. The paper’s motivating example is fraudulent refund authorization, illustrating that the issue can have direct operational consequences.

**Scope.** The paper studies filtering retrieved memories, and on MMLU also guarding memory writes, under direct AgentPoison and query-only MINJA attacks. The defender knows only that the memory bank may be poisoned and lacks knowledge of the attack strategy, triggers, poisoned records, and target behavior.

## Method

MIND converts memory defense into supervised intent-aware representation denoising. A frozen language model extracts the initial-query representation and the last-token hidden state after each retrieved memory. Their concatenation is compressed by a variational information-bottleneck encoder. An intent-alignment loss pulls benign samples toward the initial-intent anchor and pushes poisoned samples away, while a multi-hyperplane classifier defines a piecewise benign region. At inference, each retrieved memory is independently encoded and retained only when classified as benign.

### Key components

- A frozen feature extractor forms a transition representation from the initial query and the turn state after injecting each retrieved memory; Llama-3.1-8B-Instruct is used as a proxy for closed-source agents.
- A Gaussian variational encoder penalizes divergence from an isotropic prior to compress task-irrelevant and repetitive trajectory information.
- A supervised alignment objective attracts benign representations to the initial-intent anchor and separates poisoned representations by a margin.
- Multiple hyperplanes classify a representation as benign only when it lies below every boundary, allowing a piecewise region for heterogeneous attack patterns.
- The combined objective adds benign-region, poison-exclusion, KL-compression, and intent-alignment losses; inference scores each retrieved memory without gradient computation.

### Assumptions

- Training requires labeled examples identifying whether each retrieved memory is benign or poisoned.
- The initial user query is treated as a stable intent anchor against which later behavior can be judged.
- Useful attack evidence is assumed to appear in last-token hidden-state transitions and to transfer across different training and test triggers.
- For closed-source agents, representations from a separate open model are assumed to be a useful proxy.
- The evaluated defender can intervene in retrieval filtering and, for the MMLU setup, memory writing.

## Main claims

- **The paper claims that benign and poisoned trajectories exhibit distinguishable relationships between initial intent and later behavior, motivating lightweight classification after redundancy reduction.**
  - Evidence: [b00042-aef99df00b] “The hidden states associated with benign and poisoned memories show a distinguishable trend in the representation space.”; [b00044-94acded2ed] “The attention to h0 decreases over turns, and this drop is more severe under poisoned memories ℳa​d​v.”
- **MIND is presented as an intent-aware denoising defense that preserves cross-turn attack signals while removing task-irrelevant information.**
  - Evidence: [b00051-7c291bd8c7] “we formulate filtering as a denoising problem”; [b00051-7c291bd8c7] “we first compress it into a latent space zi that discards task-irrelevant redundancy while preserving the intent-relevant information.”
- **The classifier uses multiple hyperplanes because the authors argue that poisoned behavior is too diverse for a single linear boundary.**
  - Evidence: [b00069-e3d30e6fc1] “poisoned turns span diverse attack patterns that a single linear boundary cannot capture”; [b00069-e3d30e6fc1] “a turn is predicted benign only if it lies below all K hyperplanes”
- **The paper claims that the defense improves robustness while retaining benign task accuracy and inference efficiency.**
  - Evidence: [b00110-7cb9f899c2] “Experiments on StrategyQA and MMLU demonstrate consistent reductions in ASR relative to the baseline without defense”; [b00110-7cb9f899c2] “while maintaining benign task accuracy and inference time.”

## Results

- **On StrategyQA, MIND reduced average ASR-r from 46.72% to 19.57% and average ASR-a from 72.83% to 33.87%, reported as relative reductions of 58.1% and 53.5%.**
  - Context: This is the paper’s strongest aggregate security result across the evaluated backbones, comparing MIND with no defense under AgentPoison. It addresses both poisoned-memory retrieval and the conditional influence of retrieved poison, but is not an adaptive attack evaluation.
  - Evidence: [b00091-520f6de124] “MIND reduces ASR-r and ASR-a from 46.72% to 19.57% and from 72.83% to 33.87% on average”; [b00091-520f6de124] “corresponding to reductions of 58.1% and 53.5%, respectively.”
- **On MMLU, MIND decreased average ISR from 49.74% to 4.33%, a reported 91.3% relative reduction.**
  - Context: This evaluates query-only MINJA injection and includes write-time filtering, so it tests a different threat path from StrategyQA. Because the intervention differs between tasks, the result does not isolate whether retrieval filtering, write filtering, or both produced the improvement.
  - Evidence: [b00091-520f6de124] “MIND decreases ISR from 49.74% to 4.33%, achieving a 91.3% relative reduction.”; [b00202-e3e1bc6b25] “On the MMLU task, MIND further applies memory filtering during the memory writing process”
- **On StrategyQA, mean episode time was 23.13 seconds; MIND was reported as 20.6% faster than LLM Auditor and 70.4% faster than A-MemGuard.**
  - Context: The comparison supports the lightweight-runtime claim relative to repeated LLM auditing. Absolute latency nevertheless varies substantially by backbone, and the supplied blocks do not describe hardware normalization or API-network controls beyond naming the local GPUs.
  - Evidence: [b00093-f2913fb164] “MIND records an average episode time of 23.13 seconds across the four backbones”; [b00093-f2913fb164] “MIND is 20.6% faster than LLM Auditor and 70.4% faster than A-MemGuard.”
- **In the GPT-4o-mini StrategyQA ablation, full MIND obtained ASR-t 25.14%, ASR-r 26.22%, and ASR-a 48.65%; removing both components yielded 28.44%, 30.41%, and 53.65%.**
  - Context: The controlled component study supports complementarity of the information bottleneck and multi-hyperplane classifier on one backbone and benchmark. Removing either component also worsened the reported attack metrics, although the size of each effect is modest relative to the headline no-defense comparison.
  - Evidence: [b00094-edda16a95c] “w/o Both 28.44 30.41 53.65 19.36”; [b00094-edda16a95c] “MIND 25.14 26.22 48.65 19.67”; [b00095-b250913c14] “Component ablation on StrategyQA (GPT-4o-mini backbone), averaged over three independent runs.”

## Experimental evaluation

### Datasets

- StrategyQA trajectories are used for training and evaluation under AgentPoison; training also includes EHR trajectories generated by DeepSeek-V4.
  - Evidence: [b00082-f3338ae8e1] “we train models on EHR (Chen et al., 2024) and StrategyQA agent trajectories generated by DeepSeek-V4 under AgentPoison attacks.”; [b00082-f3338ae8e1] “StrategyQA (Geva et al., 2021) under AgentPoison attacks”
- MMLU is evaluated under the query-only MINJA attack; detailed accuracy covers task–victim configurations and averages two agent backbones.
  - Evidence: [b00082-f3338ae8e1] “MMLU (Hendrycks et al., 2021) under MINJA attacks.”; [b00207-be40e7f355] “Results are macro averages over GPT-4o-mini and Llama-3.1-8B-Instruct with three independent runs.”

### Baselines

- No Defense, used as the primary reference for attack reduction and latency preservation.
  - Evidence: [b00079-17decaf946] “DeepSeek-V4 No Defense 60.16 52.27 71.44 42.23 29.05 91.79 3.94”
- LLM Auditor and A-MemGuard, both involving additional LLM reasoning at retrieval time.
  - Evidence: [b00169-2b44f6fffb] “This consensus-based check requires additional LLM inference at retrieval time.”; [b00171-3ecda2b7c0] “introducing an additional LLM call per retrieval step.”
- Distil, PPL, Sequential Monitor, and AV Filter represent lightweight classifier, perplexity, stream-monitoring, and attention-variance approaches.
  - Evidence: [b00084-7658a7bec0] “a fine-tuned DistilBERT (Sanh et al., 2019) classifier (Distil), perplexity filtering (PPL)”; [b00084-7658a7bec0] “Sequential Monitor (Chen et al., 2025), and AV Filter (Choudhary et al., 2025).”

### Metrics

- ASR-t measures the proportion of test instances with an incorrect final answer, including target and other ground-truth-inconsistent answers.
  - Evidence: [b00189-08c81e1a68] “defined as the proportion of test instances with incorrect final answers”
- ASR-r measures how often poisoned memories are successfully retrieved.
  - Evidence: [b00191-84f22eac7b] “the proportion of retrieval operations where poisoned memories are successfully retrieved.”
- ASR-a measures agent compromise conditional on successful poisoned-memory retrieval.
  - Evidence: [b00193-2bcd8d804a] “conditioned on successful poison-memory retrieval”
- ISR measures successful injected records relative to attack queries for a victim-target pair.
  - Evidence: [b00195-1b62048686] “the ratio of successfully injected records to the total number of attack queries”
- Time is end-to-end latency for a complete multi-turn episode, including memory filtering.
  - Evidence: [b00197-74873ae272] “End-to-end latency per episode (i.e., a complete trajectory containing multiple turns).”
- MMLU task accuracy is additionally reported by task configuration as a macro average.
  - Evidence: [b00207-be40e7f355] “Detailed MMLU accuracy under the MINJA attack, grouped by task configuration.”

### Ablations

- Removal of the information-bottleneck encoder, replacement of the multi-hyperplane classifier with a single MLP, and removal of both components.
  - Evidence: [b00100-9d0041ba1d] “remove the IB encoder, replace the multi-hyperplane classifier with a single MLP, or remove both components.”
- Feature-encoder comparison among Qwen3-8B-it, Llama-3.1-8B-it, and gemma-4-E4B-it.
  - Evidence: [b00096-83a50d7f21] “Qwen3-8B-it 27.16 33.19 51.00 23.14 Llama-3.1-8B-it 25.14 26.22 48.65 19.67 gemma-4-E4B-it 30.62 32.45 49.81 19.87”
- Sensitivity analysis varies the bottleneck and alignment coefficients around the selected setting.
  - Evidence: [b00106-05b007600e] “We vary βIB within {10−4,10−3,10−2} while fixing λalign=0.2”; [b00106-05b007600e] “λalign within {0.1,0.2,0.4} while fixing βIB=10−3.”

### Negative results

- MIND is not uniformly beneficial: on Qwen3-8B-Instruct MMLU, ASR-t increases from 17.65% without defense to 21.07% with MIND, although ISR decreases from 3.09% to 0.23%. These metrics measure different attack stages and must not be conflated.
  - Evidence: [b00079-17decaf946] “No Defense 49.15 47.34 75.12 16.08 17.65 3.09 71.42”; [b00079-17decaf946] “MIND (Ours) 29.17 9.76 10.16 17.88 21.07 0.23 72.94”
- On GPT-4o-mini MMLU, MIND’s ISR is worse than those of LLM Auditor and Sequential Monitor.
  - Evidence: [b00079-17decaf946] “LLM Auditor 42.21 47.77 59.80 27.13 24.63 0.56 9.90”; [b00079-17decaf946] “Sequential Monitor 25.34 40.57 72.55 21.03 22.28 0.74 11.16”; [b00079-17decaf946] “MIND (Ours) 25.14 26.22 48.65 19.67 22.02 10.38 9.34”
- The AV Filter cannot be evaluated on the closed-source backbones, preventing a complete baseline comparison.
  - Evidence: [b00084-7658a7bec0] “Since AV Filter requires model attention distributions, it cannot be evaluated on closed-source backbones.”


## Limitations

- The experiments cover only models described by the authors as being below the stated scale limit; substantially larger models remain unevaluated.
  - Evidence: [b00113-7a9796ab72] “our experiments are limited to models under 8B parameters. Larger-scale models (e.g., 70B) remain as future work.”
- The defense fundamentally requires intermediate representations, restricting direct use with fully black-box agents; the proxy-encoder workaround is evaluated but does not eliminate this architectural dependency.
  - Evidence: [b00115-b0757a22bc] “MIND requires access to intermediate model representations, which limits its direct application to fully black-box models.”; [b00047-e7523a317d] “For closed-source agents such as DeepSeek and GPT, we use Llama-3.1-8B-Instruct as a proxy representation extractor f.”
- External validity is narrow: evaluation uses two benchmarks, two named attack methods, and a fixed retriever configuration. The supplied evidence does not test adaptive attackers aware of MIND, clean-distribution drift, multilingual tasks, or broader agent tools and environments.
  - Evidence: [b00082-f3338ae8e1] “we consider two attack scenarios: StrategyQA (Geva et al., 2021) under AgentPoison attacks and MMLU (Hendrycks et al., 2021) under MINJA attacks.”; [b00082-f3338ae8e1] “For retrieval, we adopt the BGE-large-en (Xiao et al., 2024), retrieving 5 memories at each turn.”
- The method is supervised and relies on explicit benign-versus-poison labels, but the paper does not establish how such labels would be obtained or maintained in a production memory system facing novel attacks.
  - Evidence: [b00047-e7523a317d] “The label li indicates whether the injected memory is benign:”; [b00048-b8e5a27a9d] “li={1,mj(t)∉ℳa​d​v(benign),0,mj(t)∈ℳa​d​v(poisoned). (3)”
- The main security table reports averages but no confidence intervals, standard deviations, or statistical tests, limiting assessment of variability and significance.
  - Evidence: [b00080-c1ae7a0791] “Memory defense results averaged over three seeds under two attack settings.”

## Reproducibility

**Status:** partial

Reproduction is plausible but not turnkey from the supplied paper blocks. The implementation paragraph is unusually concrete and a code link is stated, yet several model, data, attack, and environment details needed to match the tables exactly are absent. Closed-source API backbones also introduce version and latency variability.

**Available artifacts**

- The abstract states that code is available at https://github.com/novdream/MIND.
- Implementation details specify the frozen encoder, selected layers, representation dimensions, split ratio and seed, architecture, dropout, optimizer, epochs, learning rate, batch size, loss weights, thresholds, precision, retrieval count, run count, and GPU hardware.
- The paper provides metric definitions, a training objective, an inference description, complexity analysis, baseline descriptions, and named attack configurations.

**Missing pieces**

- Exact dataset sizes, query splits, and counts of benign and poisoned training instances.
- The concrete number of hyperplanes and the classification/alignment margin values used in reported experiments.
- Full preprocessing, prompt templates, trajectory-generation procedure, memory-bank construction, and attack parameters beyond high-level descriptions.
- Package versions, API model snapshots, decoding settings, API latency controls, and random seeds beyond the data-split seed.
- Per-run results, uncertainty estimates, and statistical significance tests.
- A documented procedure for obtaining poison labels in a realistic deployment.

## AIDB assessment

- Novelty: The main contribution is a coherent combination of intent anchoring, variational information compression, and a multi-hyperplane decision region for per-memory filtering across multi-turn trajectories. Each ingredient is established, but their application to cross-turn memory-injection defense and the explicit initial-intent relation is a meaningful systems-level synthesis.
- Usefulness: Potentially useful for memory-agent systems where hidden states or a trusted proxy encoder are available and labeled attack trajectories can be collected. The reported runtime advantage over repeated LLM auditing is operationally attractive. Deployment value is less clear for fully black-box services, rapidly changing intents, unlabeled environments, or adaptive adversaries.
- Confidence: medium
- Recommended action: watch
- Rationale: The controlled results and ablations justify further evaluation, but the evidence base is too narrow for immediate adoption. AIDB should prioritize independent reproduction, adaptive-attack testing, and measurement of false-positive utility loss on clean, long-horizon workloads before recommending production use.

## Uncertainties

- **The supplied main table exposes attack rates and time but not an explicit task-accuracy column, although the narrative says accuracy is preserved.** — Security filters can obtain low attack rates by discarding useful memories. Without directly paired clean and attacked task accuracy across all backbones, the claimed security–utility trade-off is incompletely auditable.
  - Evidence: [b00086-e71008ef54] “we report end to-end task performance ASR (ASR-t), retrieval-stage ASR (ASR-r), agent-reasoning ASR (ASR-a), and end-to-end episode time.”; [b00110-7cb9f899c2] “while maintaining benign task accuracy and inference time.”
- **MMLU adds write-time filtering, while StrategyQA is described primarily as retrieval filtering.** — The strong MMLU injection result cannot be attributed cleanly to the same intervention evaluated on StrategyQA, complicating comparison and causal interpretation.
  - Evidence: [b00202-e3e1bc6b25] “On the MMLU task, MIND further applies memory filtering during the memory writing process”
- **The paper states that training and testing triggers differ, but does not quantify trigger diversity or evaluate attacker adaptation to the learned boundary.** — Generalization to held-out triggers is weaker evidence than robustness to attacks optimized against the deployed detector.
  - Evidence: [b00082-f3338ae8e1] “The triggers used during training and testing are different.”; [b00183-2cdf42a8e7] “We evaluate three optimized triggers, one per random seed.”
- **It is unclear how well the initial-query anchor handles legitimate intent evolution, corrections, or compound goals over long conversations.** — A fixed initial intent could cause false positives when later user behavior changes legitimately, reducing utility or blocking valid memories.
  - Evidence: [b00065-6bbf90f110] “we optimize it through a supervised alignment surrogate that anchors each latent to the initial intent.”
- **The claim that representation extraction cost is shared with ordinary inference appears difficult to reconcile with using a separate proxy model for closed-source agents.** — If the proxy requires an additional forward pass, deployment latency and compute may be higher than the complexity narrative suggests.
  - Evidence: [b00047-e7523a317d] “we use Llama-3.1-8B-Instruct as a proxy representation extractor f.”; [b00217-9da0e89233] “this cost is shared with standard LLM inference”

## Open questions

- How are benign and poisoned memory labels acquired and refreshed after deployment without privileged knowledge of the attack corpus?
- What are the clean-memory false-positive rate, poisoned-memory false-negative rate, precision, recall, and calibration at the selected thresholds?
- Does MIND remain effective against an adaptive attacker that optimizes memories to stay close to the initial-intent anchor or inside every learned hyperplane?
- How does performance change with longer trajectories, larger retrieval sets, multilingual inputs, legitimate intent shifts, and distribution drift?
- What portion of end-to-end latency comes from the proxy encoder rather than the lightweight classifier, especially for API-hosted agents?
- Can the MMLU gain be decomposed into retrieval-time and write-time filtering effects?
- What are the exact values of the hyperplane count and margin parameters used for the reported results?

## Proposed AIDB experiments

- **Hypothesis:** MIND remains robust when the attacker knows the detector and optimizes poisoned memories to minimize intent-space deviation while preserving attack success.
  - Baseline: No Defense, the published non-adaptive AgentPoison and MINJA settings, and the strongest published defense baseline available for each backbone.
  - Primary metric: Adaptive ASR-t, accompanied by ASR-r, ASR-a, ISR, and clean-memory false-positive rate.
  - Stop condition: Reject the robustness hypothesis if adaptive ASR-t is not lower than the strongest defense baseline or if clean-memory false positives erase the reported task-accuracy advantage.
- **Hypothesis:** Intent anchoring remains useful when users legitimately revise, narrow, or replace their goals during long multi-turn interactions.
  - Baseline: Full MIND with a fixed initial-query anchor versus no defense and a variant that updates the anchor only after explicit user corrections.
  - Primary metric: Clean task completion accuracy under scripted intent shifts, jointly reported with poisoned-memory recall.
  - Stop condition: Stop favoring the fixed-anchor design if its clean task completion accuracy is worse than the updating-anchor variant without a compensating improvement in poisoned-memory recall.
- **Hypothesis:** The lightweight advantage persists after accounting separately for proxy representation extraction, classifier scoring, retrieval, agent inference, and network latency.
  - Baseline: No Defense, LLM Auditor, A-MemGuard, and MIND with both local and API-hosted agent backbones under identical episode workloads.
  - Primary metric: Median and tail end-to-end latency per episode, with component-level compute time and accelerator utilization.
  - Stop condition: Reject the efficiency claim if MIND’s end-to-end latency is not lower than LLM Auditor under controlled conditions or if the proxy encoder becomes the dominant incremental cost.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-10-16T14:31:52.196966+00:00`
- Document SHA-256: `fa4a2d01b1fb0126f54834d9cea62204938a90453d1229e1916653bff71c03d8`
- Metadata SHA-256: `615620517b304b1e099b49327cceb9e66f87c48ab608ec86d655686ac2ec68f3`
- Blocks: 226
- Deterministic repair attempts: 0
