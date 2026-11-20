# NariQ: Sub-3-Bit Quantization for Long-Horizon Agentic Tasks

## Executive summary

NariQ is a trellis-coded post-training quantization recipe that calibrates Qwen3.8-27B on BF16-generated agent traces and emphasizes model-written tokens. In the authors’ harness, its 3.0- and 2.5-bpw files remain statistically level with BF16 on DeepSWE and Terminal Bench while retaining short-task performance; the 2.0-bpw file degrades materially. The controlled same-harness BF16 comparisons are promising, and held-out KL results strengthen the case. However, external quantized baselines use a different harness, only one model is tested, several component studies are confounded, calibration data details are incomplete, and long-context memory remains unresolved. The result merits replication, not yet broad adoption.

## Problem

**Statement.** Determine whether a language model can be quantized to three or fewer bits per weight without losing long-horizon agent capability, when conventional calibration on short web text and evaluation by perplexity may not represent tool-using behavior.

**Why it matters.** Long-horizon agents accumulate large contexts and many tool interactions, making weight memory important for local deployment. The paper argues that the practical target is consumer hardware with limited memory and that strong short-benchmark scores can conceal severe agent-task degradation.

**Scope.** The study covers post-training quantization of Qwen3.8-27B at 3.0, 2.5, and 2.0 bpw. It evaluates coding agents, terminal tasks, mathematics, visual understanding, multilingual reasoning, offline KL, file size, and single-session generation speed.

## Method

NariQ retains trellis coding but changes the training signal and precision allocation. It constructs BF16-generated agent traces, computes KL only at model-written target positions while retaining tool output in the prefix, estimates per-module loss from gradients, predicts loss across candidate widths using measured trellis-code error, solves a discretized multiple-choice knapsack, bands output rows by predicted token probability, and tunes scales and norm weights on a mixture of coding traces and general replies.

### Key components

- Model-written-token KL: both models receive the complete prefix, but only BF16-generated model positions contribute prediction targets.
- Two-sided trellis rounding is retained when it reduces held-out curvature-weighted error sufficiently; nearly all modules use both input- and output-side statistics.
- Per-module sensitivity is inferred from gradients at several width assignments, rescaled by measured code error, combined with inverse-variance weighting, and made conservative with a two-standard-error margin.
- A dynamic-programming allocator chooses one permitted width per module under an exact storage check. Linear layers are constrained to at least two bits after the one-bit loss estimate failed.
- The output layer is partitioned into probability-ranked bands with separate widths; every output band receives at least two bits to protect rare tokens. At the lowest budget, the input embedding is also banded.
- Scale and norm tuning mixes coding-agent traces with general math, science, chat, code, and long-document replies.

### Assumptions

- The second-order expansion around BF16 and the neglect of interactions between module errors are adequate for allocating widths.
- Curvature-weighted errors at different trellis widths are sufficiently uncorrelated to interpret the gradient score as the current module loss.
- A module’s loss at another width scales proportionally with the trellis code’s measured mean squared error.
- Mean BF16 token probability is an adequate proxy for output-row sensitivity.
- KL at model-written positions is a useful development surrogate for downstream agent success.
- Repository-level exclusion of DeepSWE repositories sufficiently limits calibration-to-benchmark contamination.

## Main claims

- **The paper claims that NariQ at 3.0 and 2.5 bpw matches BF16, within experimental noise, across every benchmark it ran, whereas the 2.0-bpw checkpoint trails BF16.**
  - Evidence: [b00011-5c36b91e15] “NariQ at 3.0 and 2.5 bpw is level with BF16 within noise on all benchmarks we ran; at 2.0 bpw, it trails BF16.”
- **The claimed methodological distinction is calibration and bit allocation around tokens written by the BF16 agent, without removing tool outputs or other context from the prefix.**
  - Evidence: [b00015-dbacf4db6c] “First, the end-to-end loss counts only model-written tokens.”; [b00017-9f444467c6] “The mask selects prediction targets; it does not remove context tokens.”
- **The authors present this as the first demonstration that quantization at or below three bits per weight can match the corresponding full-precision model on long-horizon agent tasks.**
  - Evidence: [b00003-a822d9d589] “To our knowledge, these are the first quantizations at or below 3 bits per weight shown to match their full-precision version on long-horizon agentic tasks.”

## Results

- **On DeepSWE, the 3.0- and 2.5-bpw files solved 47 and 46 tasks versus 44 for BF16, with scores of 84.9% and 84.5% versus 83.0%. Paired differences were +1.9 and +1.5 points, with standard errors of 3.2 and 3.6.**
  - Context: This is the strongest same-harness long-horizon comparison. The uncertainty intervals implied by the reported standard errors do not establish superiority; they support the narrower interpretation that no degradation was detected.
  - Evidence: [b00045-76242d556c] “At 3.0 and 2.5 bpw, our files are level with BF16 on DeepSWE (Table 1).”; [b00045-76242d556c] “They solve 47 and 46 tasks against BF16’s 44, and their DeepSWE scores are 84.9% and 84.5% against BF16’s 83.0% (paired by task, +1.9 and +1.5 points, s.e. 3.2 and 3.6).”
- **On Terminal Bench 2.1, the 3.0- and 2.5-bpw files achieved 102% and 96% of BF16. Their paired differences were +1.2 and −2.4 points, with standard errors of 3.5 and 3.2.**
  - Context: The results are consistent with parity but are noisy. They should not be interpreted as evidence that quantization improves performance.
  - Evidence: [b00046-995d80d1e1] “On Terminal Bench 2.1, our 3.0 and 2.5 bpw files score 102% and 96% of our BF16, within noise of it (paired by task, +1.2 and −2.4 points, s.e. 3.5 and 3.2)”
- **The 2.0-bpw file materially underperformed: on DeepSWE it solved 33 tasks and scored 75.7%, 7.3 points below BF16; on Terminal Bench it achieved 84%, 10.2 points below; on AIME its largest reported non-coding drop was 11.7 points.**
  - Context: This consequential negative result identifies a practical boundary: the recipe’s apparent parity at the two larger budgets does not extend to the lowest evaluated budget.
  - Evidence: [b00045-76242d556c] “At 2.0 bpw, our file solves 33 tasks and scores 75.7%, 7.3 points under BF16 (s.e. 3.3).”; [b00046-995d80d1e1] “our 2.0 bpw file scores 84%, 10.2 points under (s.e. 3.5).”; [b00050-03f194e198] “At 2.0 bpw, the largest drop is on AIME, 11.7 points.”
- **On held-out offline comparisons, the strongest published files in the 2.5- and 3.0-bpw budget groups had 1.7–4.9× NariQ’s KL on every set despite using the same or more bits. At 2.0 bpw, a competitor using 0.27 bpw more was slightly better on math, 0.0819 versus 0.0829, while NariQ led by 2.1× on agent KL.**
  - Context: These centrally scored comparisons avoid the agent-harness mismatch and include a reserve set reportedly unused for selection, but KL remains a surrogate rather than an agent-success metric.
  - Evidence: [b00097-87ca830b23] “at 2.5 and 3.0 bpw the best published file in each budget group has 1.7–4.9× our KL on every set, with the same or more bits.”; [b00097-87ca830b23] “At 2.0 bpw, Unsloth’s UD-IQ2_XS, with 0.27 bpw more, is slightly ahead on the math set (0.0819 against 0.0829); we lead on the other sets, by 2.1× on agent KL.”
- **The text-only files occupy 10.1, 8.4, and 6.8 GB at 3.0, 2.5, and 2.0 bpw. On one RTX PRO 6000, generation reached 89, 99, and 112 tokens/s at 4K context and 71, 77, and 85 at 64K.**
  - Context: These measurements demonstrate a concrete storage and throughput profile for the authors’ specialized fork and one GPU, not portable performance across consumer hardware or concurrent sessions.
  - Evidence: [b00052-139db6ae5e] “occupy 10.1, 8.4 and 6.8 GB at 3.0, 2.5 and 2.0 bpw.”; [b00052-139db6ae5e] “At these three budgets, our llama.cpp fork on one RTX PRO 6000 generates 89, 99 and 112 tokens/s at a 4K-token context, and 71, 77 and 85 at 64K, for a single session.”

## Experimental evaluation

### Datasets

- Calibration and development data consist of BF16 agent sessions on open-source software tasks, partitioned by repository; repositories shared with DeepSWE were removed. A reserve trace set was kept out of selection.
  - Evidence: [b00034-8327fcabe3] “Agent sessions of the BF16 model on open-source software tasks, split by repository into calibration, development and reserve sets, with every repository shared with DeepSWE removed.”; [b00035-3d2ba4f926] “on a reserve set never used for selection”
- DeepSWE v1.1 contains 113 tasks from 91 repositories across five languages; each task receives one attempt and failures count as zero.
  - Evidence: [b00036-bb589eaeaf] “A software engineering benchmark of 113 tasks from 91 repositories in five languages.”; [b00036-bb589eaeaf] “Each task gets one attempt; agent failures count as zero, and no task is rerun.”
- Terminal Bench 2.1 uses the 82 tasks reported by Unsloth, with three attempts per task and mean test reward across attempts.
  - Evidence: [b00037-16ba160433] “We run the 82 tasks Unsloth reports on, with 3 attempts each”; [b00037-16ba160433] “We report the mean test reward over all attempts; a trial left without a grade counts as zero.”
- AIME 2025+2026, RealWorldQA, and MGSM assess math, visual understanding, and multilingual performance outside coding.
  - Evidence: [b00038-995f2d4d05] “AIME 2025+2026 [12], RealWorldQA [27] and MGSM [17]. Math, visual understanding and multilingual tasks, to measure what a file keeps outside coding.”

### Baselines

- Same-harness BF16 is the primary controlled baseline for the authors’ files.
  - Evidence: [b00041-987ee14ada] “We run BF16 and our files in our harness.”
- Published agent results cover Unsloth Dynamic V3.1, GSQ-RCO, and EXL3 files, each normalized to BF16 in its own harness.
  - Evidence: [b00041-987ee14ada] “its Dynamic V3.1 GGUFs, GSQ-RCO’s GGUFs [10] and the EXL3 files [24].”; [b00041-987ee14ada] “Table 1 reports each file relative to its own harness’s BF16, but this normalization does not remove harness differences.”
- Offline KL baselines include published files near the target budgets from GSQ-RCO, DASLab, Unsloth, and EXL3, decoded to BF16 and scored by the authors’ code.
  - Evidence: [b00042-0a382b9a78] “We decode every published file of this model near our budgets, from GSQ-RCO, DASLab [3], Unsloth and EXL3, exactly to BF16 and score it with our code.”

### Metrics

- DeepSWE metrics include mean fraction of new tests passed, fully solved task count, and paired differences with standard errors.
  - Evidence: [b00036-bb589eaeaf] “We report the DeepSWE score, the mean fraction of a task’s new tests that pass, the number of tasks solved”; [b00036-bb589eaeaf] “and paired differences with standard errors.”
- Terminal Bench uses mean test reward over all attempts, assigning zero to ungraded trials.
  - Evidence: [b00037-16ba160433] “We report the mean test reward over all attempts; a trial left without a grade counts as zero.”
- Outside coding, the paper reports accuracy percentages, with avg@8 for AIME and repeated samples for RealWorldQA.
  - Evidence: [b00038-995f2d4d05] “We sample 8 replies per AIME problem (avg@8), 3 per RealWorldQA question and 1 per MGSM question”
- Offline fidelity is KL divergence from BF16 at model-written positions; lower is better.
  - Evidence: [b00098-9d4eb1d443] “KL from BF16 at model-written tokens (lower is better).”

### Ablations

- The development sequence reports that trellis coding reduced agent KL by 3.2× relative to GPTQ+GSQ and later changes reduced it another 2.7×, but the model-token stage simultaneously added a statistical margin and therefore does not isolate masking.
  - Evidence: [b00028-dc59f44554] “Trellis coding has 3.2× lower agent KL than GPTQ+GSQ”; [b00028-dc59f44554] “Subsequent changes reduce KL a further 2.7×.”; [b00028-dc59f44554] “The model-token step also adds the two-standard-error margin, so it does not isolate masking alone.”
- Probability-banded output rows reduced mean per-trial KL at the larger reported budget.
  - Evidence: [b00026-85eb30806c] “At 3.0 bpw the bands lower the mean per-trial KL by 12.1%.”
- For the lowest-budget file, adding general data to scale tuning improved AIME relative to coding-only tuning.
  - Evidence: [b00027-7849443bc1] “An earlier 2.0 bpw file tuned on coding traces alone scored 77.3% on AIME against BF16’s 97.7%; adding the general data raised it to 86.0%.”

### Negative results

- The module-loss approximation failed for one-bit allocations; promoting the affected modules produced a much larger KL reduction than predicted, motivating a minimum width for linear layers.
  - Evidence: [b00025-419b54bf4b] “The loss estimate fails at 1 bit:”; [b00025-419b54bf4b] “moving the 12 modules the allocator had put at 1 bit up to 2 bits lowered KL by 7.2% for only 0.021 bpw, far more than predicted.”
- One-bit output bands reduced average KL on most traces but damaged traces involving rare tokens, including multilingual text.
  - Evidence: [b00026-85eb30806c] “bands at 1 bit lowered KL on most traces but raised it on traces that use rare tokens, such as multilingual text”
- The lowest-budget checkpoint trails BF16 on both long-horizon agent tasks and AIME.
  - Evidence: [b00058-953adaaa74] “At 2.0 bpw, our file trails BF16 by 7.3 points on DeepSWE and 11.7 on AIME”


## Limitations

- External agent baselines are not controlled head-to-head: they use a different agent, a different number of attempts, and chart-derived solved counts. Normalization to each harness’s BF16 does not eliminate this confound.
  - Evidence: [b00041-987ee14ada] “Unsloth uses mini-swe-agent [19] and at least three passes per DeepSWE task [26]; we use Claude Code and one attempt.”; [b00041-987ee14ada] “this normalization does not remove harness differences.”; [b00041-987ee14ada] “read from its chart to about ±0.5 tasks.”
- Evidence is restricted to one base model and a limited set of agent harnesses and benchmarks; generalization remains untested.
  - Evidence: [b00058-953adaaa74] “evaluations on more models, more agent harnesses and more agentic benchmarks remain future work.”
- The 2.0-bpw checkpoint does not retain BF16-level quality, and the proposed recovery through broader training is only a hypothesis.
  - Evidence: [b00058-953adaaa74] “we hypothesize that training beyond scales and norms can recover it.”
- The multi-token prediction module is excluded from quantization, so the released quantized scope does not cover the complete original checkpoint.
  - Evidence: [b00059-344b06ed6e] “The multi-token prediction module is not yet quantized”
- The optimized inference path is hardware-specific: it targets one GPU generation, is slower elsewhere, and falls back to CPU on sufficiently old hardware.
  - Evidence: [b00059-344b06ed6e] “our llama.cpp fork is tuned for one GPU generation (SM120); other GPUs run it slower, and GPUs older than Ampere fall back to the CPU.”
- Weights alone do not settle long-context deployment memory because KV-cache and activation quantization are future work.
  - Evidence: [b00059-344b06ed6e] “We also plan to quantize the KV cache and activations, so long contexts fit on 16 GB consumer GPUs”
- The allocator uses a discretized budget and an exact cost check, but it does not guarantee a globally optimal allocation.
  - Evidence: [b00025-419b54bf4b] “An exact-cost check enforces the storage limit, but global optimality is not guaranteed.”

## Reproducibility

**Status:** partial

Artifacts for inference appear available, and the evaluation protocol is described more clearly than the complete construction pipeline. Reproducing reported inference may be feasible, but independently rebuilding identical files and auditing every benchmark result would require substantial missing data and configuration. Reproducibility is therefore partial rather than strong.

**Available artifacts**

- The paper states that Qwen3.8-27B-NariQ-GGUF files are released.
- The paper states that inference is available through the authors’ llama.cpp fork.
- Benchmark versions, common sampling settings, context window, attempt policies, task counts, and the DeepSWE task-repository commit are reported.
- The quantization objective, allocation strategy, output banding, and scale-tuning mixture are described.

**Missing pieces**

- Exact calibration, development, reserve, general-prompt, and math-prompt datasets or trace files are not supplied in the document blocks.
- Trace counts, token counts, repository lists, preprocessing details, and random seeds are not reported.
- The precise candidate width sets, budget discretization, optimization schedule, learning rates, tuning duration, and full per-module allocations are not reported.
- No executable benchmark commands, environment lockfile, full hardware/software configuration, or raw per-task outputs are provided in the supplied material.
- The paper does not report repeated end-to-end quantization runs, independent replication, or uncertainty from calibration and allocation randomness.

## AIDB assessment

- Novelty: Potentially high. The central contribution is not a new trellis code but an agent-aware post-training recipe: model-written-token KL, gradient-derived module losses, probability-banded output precision, and mixed-domain scale tuning. The first-at-this-budget claim is explicitly qualified by the authors and is not independently established by the supplied blocks.
- Usefulness: High for researchers evaluating low-bit local agents. The study directly tests long-horizon tasks and reports paired uncertainty, storage, and throughput. Immediate production usefulness is narrower because only one model and one optimized GPU path are demonstrated, while full long-context memory and cross-harness comparisons remain unresolved.
- Confidence: medium
- Recommended action: read
- Rationale: The same-harness BF16 comparisons and reserve-set KL results justify close attention. Adoption should wait for independent reproduction, matched-harness quantized baselines, broader model coverage, and end-to-end memory measurements on actual consumer GPUs.

## Uncertainties

- **Whether NariQ is better than competing quantizers on agent success under identical serving and agent conditions.** — The headline external comparison mixes harnesses, agents, and attempt counts; relative-to-BF16 normalization cannot identify which quantizer is intrinsically better.
  - Evidence: [b00041-987ee14ada] “this normalization does not remove harness differences.”
- **Whether apparent parity is stable across new task samples and repeated stochastic runs.** — DeepSWE uses one attempt per task, and the paired standard errors are larger than the reported differences at the larger budgets.
  - Evidence: [b00036-bb589eaeaf] “Each task gets one attempt; agent failures count as zero, and no task is rerun.”; [b00045-76242d556c] “paired by task, +1.9 and +1.5 points, s.e. 3.2 and 3.6”
- **Which individual NariQ changes cause downstream agent gains.** — The development ablation is partly bundled, so the contribution of model-token masking cannot be separated from the added uncertainty margin.
  - Evidence: [b00028-dc59f44554] “The model-token step also adds the two-standard-error margin, so it does not isolate masking alone.”
- **Whether the method transfers to other model architectures, sizes, agent harnesses, and task domains.** — A method tuned around one model’s generated traces and module sensitivities may not preserve behavior elsewhere.
  - Evidence: [b00058-953adaaa74] “evaluations on more models, more agent harnesses and more agentic benchmarks remain future work.”
- **Whether the compressed weights enable the intended long-context deployment on common consumer hardware.** — Reported weight sizes omit unresolved KV-cache and activation memory, while optimized speed is tied to a particular GPU generation.
  - Evidence: [b00059-344b06ed6e] “We also plan to quantize the KV cache and activations, so long contexts fit on 16 GB consumer GPUs”; [b00059-344b06ed6e] “our llama.cpp fork is tuned for one GPU generation (SM120)”

## Open questions

- How does NariQ compare with every public quantized baseline when all files use the same server, agent, prompts, attempt count, and task snapshot?
- Does model-written-token masking outperform an all-token objective when every other quantization and allocation choice is held fixed?
- How sensitive are allocations and downstream scores to calibration repositories, trace count, random seeds, and the coding-to-general tuning mixture?
- Does the reserve-set KL improvement predict agent-task improvement across models and budgets, or only within this construction pipeline?
- Can the 2.0-bpw deficit be recovered without increasing effective storage, and does any recovery generalize beyond the tuning domains?
- What is peak end-to-end memory at long context, including vision, KV cache, activations, runtime workspace, and the unquantized multi-token prediction module?

## Proposed AIDB experiments

- **Hypothesis:** Under a fully matched harness, NariQ at 3.0 and 2.5 bpw is non-inferior to BF16 and outperforms same-budget public quantizers on long-horizon agent success.
  - Baseline: BF16 plus all available public files in the same effective-bpw bands, served with identical software, agent, prompts, sampling, task snapshot, attempt count, and hardware.
  - Primary metric: Paired difference in DeepSWE score with a prespecified non-inferiority margin; fully solved task count and Terminal Bench mean reward are secondary metrics.
  - Stop condition: Conclude support only if the confidence interval excludes the non-inferiority margin against BF16 and excludes zero against the strongest matched-budget quantized baseline; otherwise report the hypothesis unresolved or rejected.
- **Hypothesis:** Restricting KL targets to model-written tokens improves agent performance beyond an all-token calibration objective.
  - Baseline: A matched NariQ build using all-token KL, with identical traces, trellis codes, candidate widths, storage budget, optimizer, output banding, and scale-tuning data.
  - Primary metric: Paired DeepSWE score difference, accompanied by reserve agent KL to test whether the surrogate tracks downstream behavior.
  - Stop condition: Stop after the preregistered task set and seeds; accept the mechanism only if the model-token variant improves the confidence-bounded paired agent score without degrading the non-coding benchmark aggregate beyond a prespecified tolerance.
- **Hypothesis:** The 2.0-bpw quality gap can be reduced through training beyond scales and norms without exceeding the original storage budget.
  - Baseline: The released 2.0-bpw checkpoint and a scale-and-norm-only retraining control using the same data and compute.
  - Primary metric: Worst-case BF16-relative deficit across DeepSWE, Terminal Bench, AIME, RealWorldQA, and MGSM, with exact file bpw reported.
  - Stop condition: Stop if the extended-training variant fails to reduce the worst-case deficit on a held-out evaluation while remaining within the original bit budget, or if gains appear only on domains represented in tuning data.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:11.494845+00:00`
- Document SHA-256: `b55b6b2ae5df1b1bcbde5dcc049e34e7a74759a9e001e0f5e26faa9aacdaa3a4`
- Metadata SHA-256: `c1a5bbc337aae2830d6fbd50f862f9c758b2da250fd7b3555efa764fc5885e88`
- Blocks: 99
- Deterministic repair attempts: 0
