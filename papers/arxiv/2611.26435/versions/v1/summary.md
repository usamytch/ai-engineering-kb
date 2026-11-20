# Aggron: Aggressive Compression of Agentic KV Caches during Head-of-Line Stalls in the Request Queue

## Executive summary

Aggron is a serving design for memory-bound, multi-tenant LLM agents. It selectively summarizes prose tails, freezes summaries, and schedules compression in otherwise unusable capacity during admission stalls. Against asynchronous APEC and Slipstream on simulated Qwen serving, the paper reports materially lower tail latency and higher throughput, while compressed accuracy remains within a broad rerun-noise estimate. The design is well motivated and ablated, but headline serving gains are simulation-based; accuracy uses limited benchmark subsets; some trajectory changes are significant; and frontier-model results expose regressions when memory is not the bottleneck or summaries miss their hiding window. The work is promising for loaded, KV-constrained deployments, but needs live multi-tenant and stronger statistical replication before adoption.

## Problem

**Statement.** Long-running agents accumulate large KV caches across tool-using turns. Under concurrent load, memory capacity restricts admission and creates head-of-line stalls; conventional synchronous summaries add critical-path work, while asynchronous summaries compete with agent calls for compute and memory.

**Why it matters.** Agentic sessions can involve many model calls and very large contexts, so a few resident programs can saturate accelerator memory, freeze batch growth, and leave compute underused while queued programs incur high latency.

**Scope.** The paper addresses online, shared-server serving of long-horizon agents through context summarization. It studies selective prose compression, queue-aware timing, summary scheduling, accuracy and trajectory effects, and trace-driven performance on several models and task families.

## Method

Aggron classifies each observation as compressible prose or protected non-prose. It tracks only the compressible tail, triggers more aggressively for requests deeper in the admission queue, freezes each generated summary instead of recursively rewriting it, and retains a critical-path backstop plus a rare full-context reset. A controller admits summary work through a separate queue only when three gates predict that it will finish before the agent reaches the head, produce worthwhile shrinkage, and release a KV block. Agent requests retain their queue positions while summaries execute.

### Key components

- Observation-level classification using tool identity and arguments; filesystem, database, and execution outputs are protected, while reasoning and web material remain compressible.
- A contiguous protected prefix prevents separation of a tool call from its structured result; only prose following the latest protected observation is eligible.
- Queue-depth-, age-, and context-size-dependent triggering prioritizes large requests with sufficient waiting time.
- Frozen append-only summaries avoid repeated semantic distillation and preserve prefix-cache validity; a reset ceiling handles eventual context-window exhaustion.
- A separate summarization queue consumes capacity only when the agentic head cannot fit.
- Hideability, compression-worth, and KV-block-release gates limit speculative summary work.

### Assumptions

- Tool families provide a reliable proxy for whether an observation can be summarized safely.
- Recent admission rates and recent summary completion times predict whether a new summary can be hidden.
- FCFS head-of-line stalls leave useful compute and memory capacity for small summary calls.
- Recorded trajectories remain representative when replayed under concurrent synthetic arrivals because compression-induced accuracy and trajectory changes are limited.
- The workload is sufficiently KV-constrained and queued; the mechanism has less opportunity when memory does not saturate or admission waits are short.

## Main claims

- **Aggron’s central systems contribution is to compress waiting agent requests opportunistically at the server in online, multi-tenant serving.**
  - Evidence: [b00017-ab44705a0b] “Aggron, the first system to compress agentic requests opportunistically at the server in online, multi-tenant serving.”
- **The design protects structured tool outputs and summarizes only the prose tail following the latest protected observation.**
  - Evidence: [b00062-cc69b00677] “Aggron classifies as non-prose the output of three families of tools”; [b00063-6acf94d288] “Compressible prose is therefore exactly the prose that follows the most recent non-prose observation.”
- **The separate summary queue is intended to use KV and batch capacity unavailable to the blocked agentic head.**
  - Evidence: [b00081-14e63f4b5f] “Aggron therefore maintains a separate summarization queue.”; [b00081-14e63f4b5f] “admitting summarization work into the KV and batch slots the blocked head cannot use, instead of leaving them idle.”
- **Freezing summaries is meant to avoid repeated information loss and preserve cached prefixes.**
  - Evidence: [b00072-c171bc2fa4] “It does not feed the standing summary back into the next compressor’s input.”; [b00072-c171bc2fa4] “Freezing has a second, systems-side benefit by keeping the KV prefix valid for the whole episode.”

## Results

- **At high load, Aggron sustained 1.44× vanilla throughput, 1.40× APEC throughput, and 1.34× Slipstream throughput; it reduced P99 latency by 33%, 31%, and 27%, respectively.**
  - Context: This is the headline Qwen serving comparison under Poisson arrivals at λ=1. The paper attributes the gain to smaller KV footprints and higher batch occupancy, but these values come from the calibrated simulator rather than a live loaded deployment.
  - Evidence: [b00103-715b205b3c] “At high loads (λ=1), Aggron sustains 1.44× the throughput of vanilla, 1.40× APEC, and 1.34× Slipstream, and cuts P99 latency by 33%, 31% and 27% respectively.”
- **Across the reported accuracy table, every compressed-versus-vanilla difference fell within the paper’s run-to-run noise band; the largest stated accuracy loss was 2.7 percentage points.**
  - Context: The comparison spans three models and four benchmarks, with grow-1k and grow-4k used as the endpoints of Aggron’s dynamic threshold. This supports non-inferiority only relative to the paper’s noise construction, whose bands can be wide.
  - Evidence: [b00110-f9b816d18c] “every difference lies within the run-to-run noise band, so both compressed arms are as accurate as vanilla.”; [b00108-821ae48655] “Gemma-4-26B-A4B SWE 62.7 62.7 65.3 −2.7 −2.7 7.4 0.00 0.00”
- **Trajectory behavior stayed within rerun variation in 22 of 24 arm–benchmark pairs, but Qwen and GLM SWE grow-1k were significant exceptions with excess normalized edit distances of +0.11 and +0.07; those runs made 1.3-1.7× as many tool calls.**
  - Context: Accuracy parity therefore does not imply identical execution cost or behavior. The authors interpret the extra calls as state re-check insertions with unchanged tool order.
  - Evidence: [b00112-d5e5fe4be1] “Summarization also leaves trajectories within run-to-run variation in 22 of 24 arm-benchmark pairs.”; [b00112-d5e5fe4be1] “The two exceptions are SWE grow-1k on Qwen (Δ​d=+0.11) and GLM (+0.07).”; [b00112-d5e5fe4be1] “These agents make 1.3-1.7× as many tool calls as vanilla because they re-check their state after each summary.”
- **The separate summary queue improved Qwen throughput by 1.9-8.0% and lowered P99 by 3.8-8.1% relative to a shared queue; 93-100% of Aggron summaries arrived in time.**
  - Context: This ablation holds the tail-only summaries fixed and changes their queue placement, directly supporting the scheduling contribution. Effects were smaller on the other evaluated models.
  - Evidence: [b00114-83437da4dc] “the separate queue raises throughput by 1.9-8.0% and lowers P99 by 3.8-8.1% on Qwen”; [b00114-83437da4dc] “Aggron admits its summaries almost immediately, so they land in 7-33 s and 93-100% arrive in time.”
- **On frontier-model simulations, ordinary Aggron lost 1.7% on DSV4 when uncompressed serving used only 68% of HBM and summary prefill consumed 8% of serving-GPU time; with cached-tail reuse, DSV4 instead reached +5.3% throughput.**
  - Context: This consequential negative result bounds applicability: compression can hurt when KV memory is not the limiting resource. The improved case depends on a tail-reuse optimization rather than the default mechanism.
  - Evidence: [b00127-3f5176ddb4] “DSV4 (3.4 KiB) fills only 68% of HBM uncompressed, so freed memory buys nothing while summary prefill takes 8% of serving-GPU time (1.6-3.2% elsewhere), and it loses 1.7%.”; [b00127-3f5176ddb4] “throughput rises on all four models by 5-16%, with DSV4 at +5.3%, and P99 falls by 5-14%.”

## Experimental evaluation

### Datasets

- SWE-bench Verified: repository-level bug fixing, using 100 stratified instances and official patch-resolution scoring.
  - Evidence: [b00088-8c307fd04c] “SWE-bench Verified (Jimenez et al., 2024) (100 stratified instances) covers repository-level bug fixing.”
- Terminal-Bench: open-ended terminal work, using 49 tasks and task-specific tests.
  - Evidence: [b00088-8c307fd04c] “Terminal-Bench (Merrill et al., 2026) (49 tasks) covers open-ended terminal work driven by the benchmark’s own terminus agent”
- DeepResearch Bench: 50 English web-research queries against a self-hosted SearXNG instance, graded with the RACE rubric judge.
  - Evidence: [b00088-8c307fd04c] “DeepResearch Bench (Du et al., 2026) (50 English queries) covers long-horizon web research against a self-hosted SearXNG instance”
- MCPMark: 66 filesystem and PostgreSQL tool-use tasks scored by per-task verifiers.
  - Evidence: [b00088-8c307fd04c] “MCPMark (Wu et al., 2026) (66 tasks) covers tool use over the Model Context Protocol across filesystem and PostgreSQL services”
- Serving simulations replay 1,000 programs drawn from all four benchmarks with fixed-seed Poisson arrivals.
  - Evidence: [b00099-97e60c94f1] “Each serving run replays 1,000 programs drawn from all four benchmarks, arriving as a Poisson process at rate λ programs per second with a fixed seed”
- Scaling experiments use long-horizon traces from LH-TB, Terminal-Bench 2.1, and Terminal-Bench Science.
  - Evidence: [b00099-97e60c94f1] “Every model replays the same mix of long-horizon traces, from T1 on LH-TB”; [b00099-97e60c94f1] “DSV4 on Terminal-Bench 2.1 (Merrill et al., 2026), and GLM-5.3 and K3 on Terminal-Bench Science”

### Baselines

- Vanilla execution without compaction in the full context window.
  - Evidence: [b00085-75bdbaaaf4] “Vanilla runs without compaction in the full context window.”
- Slipstream and APEC asynchronous whole-context compaction, configured to compact at 60K.
  - Evidence: [b00085-75bdbaaaf4] “Slipstream and APEC compact the whole context at 60K, past the point where accuracy saturates (Table 1).”
- grow-1k and grow-4k fixed-threshold prose-tail compression arms, used to bound Aggron’s dynamic threshold behavior.
  - Evidence: [b00085-75bdbaaaf4] “The grow-4k and grow-1k arms fix that point at its two ends.”
- Synchronous and asynchronous summarization at a 4K prose cap.
  - Evidence: [b00043-2aaddad6cb] “Synchronous and asynchronous summarization at the 4K prose cap on our benchmark traces”
- Fixed 120K and 24K in-band summarization-and-restart caps for frontier-model scaling.
  - Evidence: [b00099-97e60c94f1] “the baselines cap each program’s context at 120K tokens”; [b00099-97e60c94f1] “and at 24K, within the budgets of Belcak et al. (Belcak et al., 2026), summarizing in-band and restarting at the cap.”

### Metrics

- Serving: throughput, mean latency, P50 latency, P99 latency, batch occupancy, queue-time share, HBM use, and summary latency.
  - Evidence: [b00089-3f90cd821e] “Error (%) is (sim − live)/live against the mean of two live runs at the same λ.”; [b00119-916470dc3c] “Throughput and P99 of the separate vs. shared summary queue.”; [b00043-2aaddad6cb] “Throughput and mean program latency over vanilla.”
- Task accuracy through each benchmark’s official, task-specific, verifier, or judge-based scoring.
  - Evidence: [b00088-8c307fd04c] “scored by the official harness on whether its patch resolves the issue.”; [b00088-8c307fd04c] “with reports graded by the RACE rubric judge.”
- Trajectory divergence through normalized Levenshtein distance and Jaccard overlap of tool sets.
  - Evidence: [b00087-fc1c45320f] “using Levenshtein distance d normalized by the longer sequence, from 0 (identical) to 1 (nothing shared).”; [b00087-fc1c45320f] “We complement it with Jaccard overlap of the sets of tools used, which ignores order.”
- Simulator fidelity through mean absolute error and simulated-versus-live error.
  - Evidence: [b00100-b67df63a0d] “the simulator predicts decode step time within 7.9% and prefill latency within 9.4% mean absolute error.”

### Ablations

- Separate versus shared summary queue while holding tail-only summaries constant.
  - Evidence: [b00114-83437da4dc] “Both fire the same tail-only summaries, so only the summary waits differ.”
- Moving otherwise synchronous 4K-cap summaries into the separate queue without early summaries, to expose the cost of summaries that cannot be hidden.
  - Evidence: [b00120-6e9c4cf89e] “Figure 9(c) masks the controller and moves the 4K cap’s own summarizations, with no early summaries, from the main queue into the separate one.”
- Sweeps of the compression-worth gate and KV-block-release gate around their default settings.
  - Evidence: [b00121-9e1346ee08] “Figure 9(d) sweeps both, normalized to the default setting (α=2.5, 1056-token blocks).”
- Cached-tail reuse and a separate 35B summarizer in frontier-model scaling experiments.
  - Evidence: [b00128-a2da2cdb36] “Moving every summary to a 35B side model frees the serving GPU but cannot reuse its KV.”; [b00127-3f5176ddb4] “If each summary reuses the cached KV of the prose it compresses and recomputes 15% of it”

### Negative results

- Asynchronous summarization matched synchronous throughput and gained little latency in the studied shared-GPU workload.
  - Evidence: [b00046-ffe2410eb3] “Asynchronous summarization matches it in throughput and gains little in latency.”
- Unhideable separate-queue summaries degraded performance, especially at light load.
  - Evidence: [b00120-6e9c4cf89e] “the separate queue loses 0.2-3.8% throughput and adds 1.3-47% to P99 relative to keeping the cap synchronous.”; [b00120-6e9c4cf89e] “The loss peaks at light load (λ=0.05), where the queue is too short to hide a summary.”
- The ordinary frontier-model configuration regressed on DSV4 because memory was not saturated and summary prefill consumed serving time.
  - Evidence: [b00127-3f5176ddb4] “freed memory buys nothing while summary prefill takes 8% of serving-GPU time (1.6-3.2% elsewhere), and it loses 1.7%.”
- A side summarizer regressed sharply on DSV4 under the smaller cap because requests waited on their summaries.
  - Evidence: [b00128-a2da2cdb36] “a third of DSV4’s, where it loses 26% as requests wait on their own summary for 81% of the run.”
- Two compressed SWE configurations significantly changed trajectories and increased tool-call counts.
  - Evidence: [b00112-d5e5fe4be1] “The two exceptions are SWE grow-1k on Qwen (Δ​d=+0.11) and GLM (+0.07).”; [b00112-d5e5fe4be1] “These agents make 1.3-1.7× as many tool calls as vanilla because they re-check their state after each summary.”


## Limitations

- The headline concurrent-serving evaluation is trace-driven simulation rather than a live multi-tenant experiment; live validation is reported for vanilla, while Aggron extends the validated simulator and controller.
  - Evidence: [b00091-90ed5fc570] “We therefore evaluate the system in a trace-driven discrete-event simulator that replays recorded agentic trajectories under a synthetic arrival process.”; [b00100-b67df63a0d] “We validate the simulator end-to-end on vanilla”; [b00100-b67df63a0d] “Aggron extends this validated engine with its controller”
- Simulator error is nontrivial in a lightly loaded regime: reported median and mean errors reach double digits, partly attributed to host-speed variation.
  - Evidence: [b00100-b67df63a0d] “the median and mean miss by up to 16%, as host speed varied by 21% between the two live runs.”
- Accuracy conclusions rely on broad rerun-noise bands, especially for Terminal-Bench, where few tasks were scored and outcomes were unstable.
  - Evidence: [b00111-5fed5adfec] “The noise band varies widely across benchmarks, and is widest on Terminal-Bench (±12-20 pp, against ±7-9 pp on SWE-bench).”; [b00111-5fed5adfec] “It has the fewest tasks (30-40 scored)”
- The selective-compression taxonomy is hand-defined around particular tool families; evidence does not establish safety for unseen tools, mixed-format observations, or adversarially structured prose.
  - Evidence: [b00062-cc69b00677] “Aggron classifies as non-prose the output of three families of tools”
- The contiguous protected prefix leaves some compressible prose untouched, reducing achievable memory savings for workloads with frequent structured observations.
  - Evidence: [b00063-6acf94d288] “The price is that prose written before a file read or a test run is never summarized.”
- The method eventually summarizes protected non-prose at the reset ceiling, weakening the claimed verbatim-preservation property for sufficiently long programs.
  - Evidence: [b00073-b6db12f902] “the reset is the one point at which Aggron does compress non-prose”
- Benefits depend on memory pressure and enough queueing time to hide summaries; the paper demonstrates regressions when either condition fails.
  - Evidence: [b00120-6e9c4cf89e] “The loss peaks at light load (λ=0.05), where the queue is too short to hide a summary.”; [b00127-3f5176ddb4] “DSV4 (3.4 KiB) fills only 68% of HBM uncompressed, so freed memory buys nothing”

## Reproducibility

**Status:** partial

Reproduction is plausible in outline but not turnkey. The paper gives unusually concrete scheduler logic and parameters, yet the supplied material lacks the implementation and full experimental artifacts needed to recreate the headline results exactly. Simulator validation helps, but it validates vanilla more directly than Aggron under loaded execution.

**Available artifacts**

- Detailed architecture, trigger equations, gate definitions, thresholds, hardware configuration, model versions, benchmark task counts, arrival process, and simulator calibration are described.
- The implementation is stated to use unmodified vLLM 0.24 with Aggron as a scheduler subclass, and the same controller code in live and simulated execution.
- A fixed arrival seed and identical arrivals across arms are stated; several underlying trace sources are named.

**Missing pieces**

- No Aggron source-code or simulator repository is supplied in the provided metadata or document blocks.
- No exact fixed seed, complete configuration files, prompts, classifier rule implementation, summary prompt, or task-instance lists are supplied.
- No raw run outputs, per-task outcomes, confidence intervals for serving metrics, or complete live Aggron-versus-baseline measurements are supplied.
- One referenced trajectory dataset is stated to be no longer publicly accessible.

## AIDB assessment

- Novelty: High systems novelty in treating admission delay as a scheduling resource: selective prose compression is combined with queue-position-dependent triggering, frozen summaries, hideability prediction, and a separate queue that runs only when the blocked agent head cannot use available capacity. The individual ingredients are familiar, but their coupling to server admission state appears distinctive within the paper’s comparison set.
- Usefulness: Potentially high for multi-tenant, long-horizon agent serving that is demonstrably KV-bound. The strongest practical value is reduced tail latency without purchasing a dedicated summarizer. Applicability is conditional: compute-bound models, light load, inaccurate hideability prediction, unfamiliar tools, and very long sessions that trigger full resets may erase or reverse the gain.
- Confidence: medium
- Recommended action: watch
- Rationale: The controlled simulator comparisons, queue ablation, explicit negative results, multi-model accuracy study, and trajectory analysis make the work worth close attention. Adoption is premature because headline performance is simulated, live validation is incomplete for Aggron, accuracy uncertainty is broad, and the default method regresses outside its KV-bound operating regime. A live shadow deployment with calibrated safeguards would be the appropriate next step.

## Uncertainties

- **Whether the reported tail-latency and throughput gains survive live concurrent serving with real arrival correlations, tool-time variability, host contention, and scheduler overhead.** — The main deployment claim rests on simulation, and light-load live-versus-simulated latency errors are materially larger than the strongest ablation effects.
  - Evidence: [b00091-90ed5fc570] “We therefore evaluate the system in a trace-driven discrete-event simulator”; [b00100-b67df63a0d] “the median and mean miss by up to 16%”
- **Whether accuracy equivalence would hold under more repetitions and tighter statistical intervals.** — Broad noise bands can conceal practically meaningful degradation, especially on the smallest and most unstable benchmark.
  - Evidence: [b00111-5fed5adfec] “Terminal-Bench (±12-20 pp, against ±7-9 pp on SWE-bench).”; [b00086-7c532c6bdf] “We therefore run vanilla twice, report the mean”
- **Whether tool-name heuristics generalize to novel or composite tools whose outputs mix code, identifiers, prose, and structured data.** — Misclassification could either destroy necessary semantics or protect too much context to yield useful memory savings.
  - Evidence: [b00062-cc69b00677] “Aggron classifies at the granularity of an observation”; [b00062-cc69b00677] “inspects the tool name and arguments.”
- **How often full reset compression occurs in truly unbounded production sessions and how much it damages structured information.** — At reset, the system violates its normal rule of retaining non-prose verbatim, but no reset-specific accuracy evaluation is supplied.
  - Evidence: [b00073-b6db12f902] “When the assembled context exceeds R, Aggron summarizes everything, including the frozen segments”; [b00073-b6db12f902] “the reset is the one point at which Aggron does compress non-prose”

## Open questions

- What are the live, loaded Aggron results against Slipstream, APEC, and synchronous prose compression on identical hardware and arrivals?
- How sensitive are throughput and tail latency to prediction-window length, percentile choice, cold-start modeling, and abrupt workload shifts?
- Can a learned or schema-aware classifier improve compression coverage without increasing semantic failures on mixed-format tool outputs?
- What are accuracy, trajectory, and serving-cost effects after repeated full resets in sessions that exceed the model window many times?
- How do fairness and starvation behave when deep, large requests receive more aggressive compression while FCFS order is retained?
- Does summary generation introduce privacy or cross-tenant isolation concerns when performed inside a shared serving engine?
- Can dynamic routing between the serving engine and a side summarizer avoid the documented side-model regressions without doubling cost?

## Proposed AIDB experiments

- **Hypothesis:** On a live shared server under KV-saturating load, Aggron reduces P99 program latency without reducing task success beyond a prespecified non-inferiority margin.
  - Baseline: Uncompressed serving, synchronous prose-tail compression, Slipstream, and APEC, all using identical models, hardware, task traces, and arrivals.
  - Primary metric: Paired P99 program latency, with throughput and task success as co-reported safeguards.
  - Stop condition: Stop after enough independent arrival seeds produce a stable confidence interval; reject deployment if the latency interval includes no benefit or the task-success interval crosses the chosen non-inferiority margin.
- **Hypothesis:** A schema-aware observation classifier safely compresses more context than the paper’s tool-family heuristic on unseen and mixed-format tools.
  - Baseline: The published tool-name-and-argument classifier.
  - Primary metric: KV tokens removed at matched task success, with semantic retention failures audited per observation type.
  - Stop condition: Stop if any protected identifier, assertion, traceback, query result, or executable fragment is lost in the candidate arm, or if memory reduction fails to improve at matched accuracy.
- **Hypothesis:** Adaptive disabling based on measured HBM pressure and predicted hiding probability prevents regressions in compute-bound and light-load regimes.
  - Baseline: Default Aggron with its published gates, plus vanilla serving.
  - Primary metric: Worst-case throughput change relative to vanilla across a load-by-model matrix.
  - Stop condition: Stop when the adaptive policy either eliminates all statistically resolved throughput regressions or fails its preset maximum-regression bound on any tested regime.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:46:18.965831+00:00`
- Document SHA-256: `8ed9d72aebbb2b8d45fb07a6f21e30914304b9e702d6946b6865c628c9cab84b`
- Metadata SHA-256: `3f3ff1ce2768a1d77f25b7467e4b51284539c98e51cd096598f02f71bb5dbf92`
- Blocks: 223
- Deterministic repair attempts: 1
