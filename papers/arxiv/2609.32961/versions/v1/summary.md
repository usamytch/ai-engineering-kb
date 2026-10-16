# Beyond Token Savings: A Systematic Study of Context Compression in LLM Agents

## Executive summary

The paper presents a controlled characterization of context compression as a runtime policy with three separable choices: primitive, trigger, and depth. Across two coding benchmarks and three open-weight models, its central finding is that token reduction is not a reliable proxy for task success, latency, or estimated billed input cost. Policies with similar aggregate success can replace one set of solved tasks with another, and policy rankings can reverse across models and workloads. The experimental scale, repeated runs, task-level analysis, and controlled parameter sweeps make this strong evidence against choosing compression solely by token savings. Adoption should nevertheless be conditional: estimated cost depends on an assumed cache-pricing reconstruction rather than measured bills, resource comparisons exclude time-capped runs, and the supplied material provides no public code, raw trajectories, or result files.

## Problem

**Statement.** Agent harnesses commonly bundle what to compress, when to compress, and how much to remove into fixed policies, obscuring which choice changes success and execution cost.

**Why it matters.** Compression changes the information available to later agent decisions and can add summarization, cache-reuse, call-count, and latency overhead. Therefore, smaller contexts may neither preserve task outcomes nor reduce end-to-end cost.

**Scope.** The study concerns agentic coding workflows evaluated with a modified mini-swe-agent harness on selected SWE-bench Verified and Terminal-Bench 1.0 tasks, using Qwen3.5-35B-A3B, Devstral-Small-2-24B, and GLM-4.7-Flash.

## Method

The authors factor each compression policy into a primitive, trigger, and depth, then compare full-context execution with rule-based deletion, LLM rewriting, and stacked policies. The main comparison fixes each model’s primary threshold and canonical depth, while smaller controlled cohorts sweep thresholds and depths. Every task–policy–model configuration is repeated, and outcomes are analyzed both in aggregate and per task. Resource ratios are paired to full context on eligible shared tasks; uncertainty is estimated by task bootstrap.

### Key components

- Primitive axis: truncation, tool-result clearing, free-form or structured summarization, partial summarization retaining a recent verbatim tail, and stacked combinations.
- Trigger axis: token-threshold compression or step-triggered clearing; thresholds are calibrated from uncompressed peak-context distributions separately by model and workload.
- Depth axis: the fraction removed from the compressible window, swept for depth-tunable primitives while depth-invariant operations are evaluated once per threshold.
- Protected context: the system prompt and initial task instruction remain verbatim; compression operates on assistant messages and tool results.
- Evaluation design: full task cohorts for broad comparison, stratified subsets for controlled sweeps, and repeated attempts to expose run-to-run variability.
- Analysis: native benchmark success, cumulative token use including compression calls, estimated billed input cost, wall-clock latency, task gains and losses, and bootstrap intervals.

### Assumptions

- The modified mini-swe-agent loop is sufficiently minimal that other memory mechanisms do not confound the compression intervention.
- Model- and workload-specific thresholds derived from uncompressed trajectories provide meaningful comparable operating points, although they are not identical token thresholds.
- The estimated cache model—cached input charged at one-tenth of fresh input—reasonably represents billed-cost tradeoffs despite not measuring an actual provider bill or cache-hit rate.
- Three attempts per configuration adequately characterize stochastic variability for aggregate and task-level comparisons.
- Selected benchmark tasks and locally served open-weight models are informative about agent compression, while not establishing transfer to other agents, models, or workloads.

## Main claims

- **Context compression should be treated as a multidimensional runtime policy rather than a single token-saving control.**
  - Evidence: [b00017-bba6994844] “We decompose a compression policy along three axes: primitive, trigger, and depth.”; [b00015-30a34efcd0] “context compression is not a single efficiency knob”
- **The evaluation is designed to isolate compression choices while holding the surrounding agent setup and tasks fixed within comparisons.**
  - Evidence: [b00014-dec78169ba] “We examine three policy dimensions, compression mechanism, trigger point, and aggressiveness, while holding the agent loop and task set fixed.”; [b00039-96b39601dd] “Our methodology is designed to separate the effects of these policy choices while controlling the agent harness, task, and model within each comparison.”
- **Token use alone cannot determine whether a policy is effective or efficient because compression also changes cache eligibility, execution length, and per-step overhead.**
  - Evidence: [b00062-b17bb8e246] “Token savings alone therefore do not identify an effective or efficient policy.”; [b00067-2afce8765b] “compression also changes which tokens receive the cached rate, how many calls the agent makes, and how much time each step takes.”
- **Compression policy selection must be conditioned on the executing model and workload rather than transferred mechanically.**
  - Evidence: [b00084-7a0f343dff] “no single compression policy performs best across models”; [b00091-77bc6a3d99] “Consistency across models does not guarantee transfer across workloads.”

## Results

- **On Qwen SWE-bench, every tested compression policy reduced token usage; policies used roughly 0.4–0.7× full-context tokens while success ranged from 11.0 percentage points below to 0.7 points above full context. TRC retained near-baseline success with token, latency, and billed-cost ratios of 0.57×, 0.79×, and 0.71×, whereas SU used 0.59× tokens but lost 11.0 points.**
  - Context: This is the strongest direct demonstration that comparable token reduction does not imply comparable task success or execution cost.
  - Evidence: [b00059-7dcfc9f161] “policies use roughly 0.4–0.7× the tokens, while success ranges from 11.0 percentage points (pp) below full context to 0.7 points above it.”; [b00059-7dcfc9f161] “TRC mostly matches full-context success while reducing token usage, latency, and billed cost to 0.57×, 0.79×, and 0.71×, respectively.”; [b00059-7dcfc9f161] “SU uses a similar 0.59× the tokens but reduces success by 11.0 pp.”
- **On Qwen Terminal-Bench, most policies used roughly 0.25–0.4× full-context tokens, but 11 of 12 lost 5–13 success points; all were slower, with most at roughly 1.05×–1.8× latency, although billed cost decreased for 9 of 12. Policies using roughly one-third of the tokens could take 1.2–1.8× as long.**
  - Context: This controlled workload comparison directly contradicts the assumption that shorter context necessarily yields faster execution.
  - Evidence: [b00061-da1cd64302] “most policies reduce token usage more aggressively, to roughly 0.25–0.4× full context, but 11 of the 12 reduce success by 5–13 percentage points.”; [b00061-da1cd64302] “All policies also take longer than full context, with latency ranging from roughly 1.05× to 1.8× for most policies.”; [b00061-da1cd64302] “Billed cost nevertheless decreases for 9 of the 12 policies”; [b00064-fc9feecb88] “policies using roughly one-third of the tokens can take 1.2–1.8× as long”
- **Trigger timing and depth interact with the primitive. In a Qwen SWE-bench sweep, raising the threshold from 10K to 20K at D=0.5 reduced compression frequency from 4.85 to 1.15 events per attempt. For SU, success rose from 50.7% to 62.7%, cost fell from 1.10× to 0.92×, and latency fell from 653 to 599 seconds. At a 15K threshold, increasing depth from 0.3 to 0.7 reduced TR success from 61.3% to 50.7% but increased SU success from 50.7% to 60.0%.**
  - Context: The parameter sweeps show that later compression can reduce repeated intervention and that aggressiveness cannot be optimized independently of the primitive.
  - Evidence: [b00070-a002be5f67] “Increasing the threshold from 10K to 20K at D=0.5 reduces average compression frequency from 4.85 to 1.15 events per attempt”; [b00070-a002be5f67] “For SU, resolve rate rises from 50.7% to 62.7%, while input cost drops from 1.10× to 0.92× full context and latency falls from 653 to 599 seconds.”; [b00071-7113b7934b] “At a 15K threshold, increasing TR’s depth from 0.3 to 0.7”; [b00071-7113b7934b] “resolve rate drops from 61.3% to 50.7%”; [b00071-7113b7934b] “SU shows the opposite trend: resolve rate rises from 50.7% to 60.0%”
- **Aggregate success concealed substantial task turnover. Relative to Qwen full context, compression policies newly solved 2–7 of 47 missed tasks but lost 6–14 of 53 previously solved tasks. TRC+SU solved 52 tasks versus 53 for full context while gaining 7 and losing 8.**
  - Context: This matters operationally because an apparently equivalent aggregate policy may regress previously reliable task classes.
  - Evidence: [b00078-edc48270dd] “2–7 of the 47 tasks that full context misses become newly solved, while 6–14 of the 53 tasks solved by full context become unsolved.”; [b00078-edc48270dd] “TRC+SU solves 52 tasks compared with 53 for full context, but newly solves 7 tasks while losing 8 previously solved tasks.”
- **Policy effects were model-dependent. OTRC reached 51.3% and 41.3% success for Qwen and GLM with latency of 0.88× and 0.94×, but on Devstral it reached 38.7% and latency rose to 1.42×. A smaller summarizer also failed to guarantee efficiency: SU success fell from 53.3% under self-summarization to 37.3% and 28.0%, and neither alternative reduced mean latency.**
  - Context: These comparisons weaken any claim that one compression recipe or a cheaper summarizer can be selected independently of the agent model.
  - Evidence: [b00083-f9cac2a026] “OTRC performs well with Qwen and GLM, reaching 51.3% and 41.3% resolve rate while reducing latency to 0.88× and 0.94× full context, respectively.”; [b00083-f9cac2a026] “With Devstral, however, the same policy drops resolve rate to 38.7% and increases latency to 1.42× full context.”; [b00251-cc9bbb430f] “resolve rate falls from 53.3% with self-summarization to 37.3% with Qwen3.5-9B and 28.0% with Gemma-4-12B.”; [b00251-cc9bbb430f] “Neither alternative reduces mean end-to-end latency on the shared eligible tasks.”

## Experimental evaluation

### Datasets

- SWE-bench Verified: 100 selected issues from Django, SymPy, and scikit-learn for the main comparison; a 25-task subset for threshold and depth sweeps.
  - Evidence: [b00191-2c49f64736] “Our 100 issues come from Django (34), SymPy (34), and scikit-learn (32)”; [b00191-2c49f64736] “The threshold and depth sweeps use subsets of 25 SWE-bench”
- Terminal-Bench 1.0 using terminal-bench-core 0.1.1: 40 tasks for the main comparison and a 15-task subset for sweeps.
  - Evidence: [b00191-2c49f64736] “For Terminal-Bench 1.0 we use the terminal-bench-core 0.1.1 dataset. Its 40 tasks cover build and environment setup”; [b00191-2c49f64736] “15 Terminal-Bench tasks”

### Baselines

- Full Context (FC), the uncompressed agent, is the principal reference for success and paired resource ratios.
  - Evidence: [b00050-4966d031b9] “We also include the full-context reference”; [b00211-b211f77115] “compare policy effects relative to each model’s full-context baseline”
- Standalone step-triggered tool-result clearing (OTRC) is included as a reference policy without an operative token threshold.
  - Evidence: [b00201-35586c9cd7] “FC and standalone OTRC are evaluated once per task repetition without an operative token threshold.”

### Metrics

- Resolve rate and task-level gains/losses, with native benchmark evaluation and a task considered solved when at least two repeated runs succeed.
  - Evidence: [b00213-ed70c681fa] “Resolve rate averages each task’s success fraction across three runs.”; [b00213-ed70c681fa] “we consider a task solved when at least two of its three runs succeed.”
- Total token consumption includes prompt and output tokens from both agent and summarization calls.
  - Evidence: [b00219-fcbaca5bb1] “Token consumption is the total number of prompt and output tokens recorded over a run, including the summarization calls”
- End-to-end latency is wall-clock time from trajectory start to termination.
  - Evidence: [b00211-b211f77115] “latency measures wall-clock time from trajectory start to termination.”
- Billed input cost is reconstructed from fresh, cached, and summarizer input tokens under an assumed cache discount; it excludes output tokens.
  - Evidence: [b00225-daac8c2693] “Cached input is charged at one-tenth the fresh-input rate; summarizer input is treated as fresh.”; [b00225-daac8c2693] “Output tokens contribute to token consumption but are excluded from this input-cost metric.”
- Uncertainty is reported with task-bootstrap confidence intervals preserving all runs for each sampled task.
  - Evidence: [b00217-6d79dc58a9] “We report 95% confidence intervals by repeatedly sampling tasks with replacement.”

### Ablations

- Trigger-threshold and compression-depth sweeps vary when compression occurs and how aggressively depth-tunable primitives remove context.
  - Evidence: [b00051-8abeba594e] “we evaluate D∈{0.3,0.5,0.7} at each of the tight, primary, and loose thresholds.”
- Cross-model comparison evaluates the same policy family on Qwen, Devstral, and GLM; GLM receives only the primary threshold and fixed canonical depth.
  - Evidence: [b00198-3935a718cd] “GLM is evaluated only at the primary threshold and fixed depth D=0.5”
- Summarizer sensitivity holds the Qwen agent fixed and compares self-summarization with Qwen3.5-9B and Gemma-4-12B for SU and TRC+SU.
  - Evidence: [b00249-be6dceeb49] “Figure 19 compares self-summarization with Qwen3.5-9B and Gemma-4-12B for SU and TRC+SU”

### Negative results

- Most Qwen Terminal-Bench compression policies reduced success despite large token reductions, and all were slower than full context.
  - Evidence: [b00061-da1cd64302] “11 of the 12 reduce success by 5–13 percentage points. All policies also take longer than full context”
- A smaller summarizer did not automatically improve efficiency and could sharply reduce success under SU.
  - Evidence: [b00251-cc9bbb430f] “smaller summarizers do not automatically improve efficiency”; [b00251-cc9bbb430f] “resolve rate falls from 53.3% with self-summarization to 37.3% with Qwen3.5-9B and 28.0% with Gemma-4-12B.”
- A design choice beneficial across models on one workload did not necessarily transfer to another workload.
  - Evidence: [b00091-77bc6a3d99] “Adding partial structured rewriting to per-step clearing (OTRC+SS-p vs. OTRC) reduces Terminal-Bench resolve rate by 12.5, 7.5, and 12.5 percentage points”


## Limitations

- External validity is limited to two coding-oriented benchmarks, selected task cohorts, one agent harness, and three locally served open-weight models; the paper does not establish transfer to closed models, non-coding agents, or production traffic.
  - Evidence: [b00039-96b39601dd] “We evaluate policies across two agentic coding benchmarks and three open-weight models”; [b00041-9343275666] “We use mini-swe-agent”
- The principal billed-cost metric is modeled rather than observed. It assumes a cache discount and reconstructs cache reuse, while Qwen serving had prefix caching disabled.
  - Evidence: [b00226-a49f54839f] “This is an estimate under the assumed cache discount, not a measured provider bill or cache-hit rate; Qwen was served with prefix caching disabled.”
- Main resource comparisons exclude time-capped runs, although time limits form a substantial fraction of unresolved Terminal-Bench attempts; this can condition latency and cost estimates on a non-representative subset.
  - Evidence: [b00215-fac0b62f9c] “Main comparisons of token consumption, cost, and latency exclude runs that reach the time limit”; [b00255-d79abfdde1] “On Terminal-Bench, time limits account for a substantial share of unresolved attempts across models.”
- Controlled threshold and depth sweeps use smaller subsets, and some execution-length comparisons rest on very few shared solved tasks.
  - Evidence: [b00191-2c49f64736] “The threshold and depth sweeps use subsets of 25 SWE-bench and 15 Terminal-Bench tasks”; [b00258-72593e54ac] “Terminal-Bench estimates use only 2–15 tasks and should be interpreted alongside their uncertainty intervals.”
- Threshold calibration and runtime triggering use different token counts, so actual threshold-crossing rates can depart from the intended percentile calibration.
  - Evidence: [b00207-c9f04bac24] “Calibration uses server-reported counts, while runtime checks use the token estimate described in Appendix A.2; exact crossing rates can therefore differ.”
- The cross-model study observes ranking reversals but does not identify whether they arise from information retention, recovery ability, execution behavior, or separate threshold calibration.
  - Evidence: [b00086-13180c4284] “they do not distinguish differences in information retention, recovery from removed context, or execution behavior; thresholds are also calibrated separately for each model.”

## Reproducibility

**Status:** partial

The methodological specification is unusually detailed and includes prompts, policy behavior, task cohorts, software versions, hardware, and analysis rules. That supports conceptual reproduction, but independent numerical reproduction remains only partial because the supplied material does not identify executable code or raw experimental artifacts.

**Available artifacts**

- Compression implementation descriptions and exact summarization prompt templates are included in the appendix.
- Task cohorts, experimental configurations, threshold calibration, metric definitions, inclusion rules, statistical procedures, software versions, inference settings, and resource-limit handling are documented.

**Missing pieces**

- No public source-code repository or downloadable implementation artifact is identified in the supplied blocks.
- No raw trajectories, per-run result files, bootstrap samples, or plotting data are identified in the supplied blocks.
- No model-weight identifiers, exact revisions, container images, random seeds, or complete command lines are identified in the supplied blocks.
- The estimated billed-cost reconstruction is not validated against measured provider bills or cache-hit telemetry.

## AIDB assessment

- Novelty: The strongest contribution is not a new compression algorithm but a controlled three-axis characterization that separates primitive, trigger, and depth while connecting them to task success, task coverage, latency, token use, and estimated cost. The task-turnover and cross-model reversal analyses add decision-relevant evidence beyond aggregate leaderboards.
- Usefulness: Highly useful for teams designing agent runtimes or evaluating compaction. It shows why token count should not be the sole optimization target and supplies a practical evaluation template: pair against full context, track task gains and losses, include compression calls, measure wall time, model cache effects, and tune by model and workload.
- Confidence: high
- Recommended action: read
- Rationale: The paper supports its central conclusions with a large controlled matrix, repeated runs, parameter sweeps, task-level outcomes, and explicit uncertainty procedures. It should inform evaluation and policy-selection practices, but direct adoption of any winning policy is premature because rankings vary across models and workloads, cost is estimated, and executable artifacts are not identified.

## Uncertainties

- **It is unclear whether the reported policy rankings would persist under real prefix caching and provider billing.** — The cost argument depends on cache invalidation, yet cache reuse is reconstructed rather than observed and Qwen was served without prefix caching.
  - Evidence: [b00226-a49f54839f] “not a measured provider bill or cache-hit rate; Qwen was served with prefix caching disabled.”
- **The causes of cross-model ranking reversals remain unresolved.** — Without causal attribution, practitioners cannot predict transfer to a new model without rerunning the policy matrix.
  - Evidence: [b00086-13180c4284] “Explaining the ranking reversals requires further controlled analysis.”
- **The extent to which excluded time-capped runs change resource rankings is not fully resolved by the supplied aggregate text.** — Policies that time out frequently may appear cheaper or faster when those attempts are removed from primary resource comparisons.
  - Evidence: [b00215-fac0b62f9c] “Main comparisons of token consumption, cost, and latency exclude runs that reach the time limit”; [b00255-d79abfdde1] “These patterns provide context for resource comparisons that exclude time-capped runs.”
- **Task-level gains and losses are documented, but the supplied text does not identify which task properties predict benefit or harm from compression.** — Aggregate turnover cannot yet guide selective policy routing or protect task categories that full context already solves.
  - Evidence: [b00078-edc48270dd] “approximately matching full-context success does not mean preserving its task coverage”

## Open questions

- Which retained information—recent actions, tool observations, errors, files, commands, or decisions—causally explains task gains and losses?
- Can a policy choose primitive, trigger, and depth online from trajectory characteristics without sacrificing previously solved tasks?
- Do rankings persist with measured prefix-cache behavior, real provider billing, and concurrent production workloads?
- How stable are conclusions across non-coding tasks, other agent harnesses, closed-weight models, and longer trajectories?
- Would resource rankings change if every terminated attempt were incorporated through censored-time or fixed-budget analysis rather than excluding time-capped runs?

## Proposed AIDB experiments

- **Hypothesis:** A prefix-stable compression policy will preserve more cache reuse and reduce measured input cost without lowering task success relative to rewriting-based summarization.
  - Baseline: The paper’s best rewriting-based policy for each model and workload, plus Full Context and TRC, evaluated on the same task cohorts and repeated-run protocol.
  - Primary metric: Measured provider input cost per attempted task, accompanied by native task success and observed cache-hit tokens.
  - Stop condition: Reject the hypothesis if the prefix-stable policy fails to reduce measured input cost or if its task-success confidence interval indicates a practically meaningful regression against the selected baseline.
- **Hypothesis:** Routing compression from observable trajectory features will outperform any single fixed policy on the joint objective of success, latency, and cost.
  - Baseline: The best fixed policy selected on a training cohort, Full Context, and a token-threshold-only router.
  - Primary metric: Held-out success subject to prespecified measured-cost and end-to-end-latency budgets.
  - Stop condition: Stop if the learned router does not improve held-out success under both budgets, or if gains disappear across repeated splits or models.
- **Hypothesis:** Protecting execution anchors such as exact commands, errors, modified files, and recent tool responses will reduce task losses relative to free-form summarization.
  - Baseline: SU and SS at matched trigger thresholds, target sizes, summarizer model, and compression frequency.
  - Primary metric: Number of full-context-solved tasks retained by the compressed policy, with overall resolve rate as a guardrail.
  - Stop condition: Reject the hypothesis if protected-anchor compression does not reduce losses on held-out tasks or if any reduction is offset by a lower overall resolve rate.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:12:18.176638+00:00`
- Document SHA-256: `5fcba59be81077af3c26b3e3f3d5ac60a44200b4dd935956e90b4e3163f52b47`
- Metadata SHA-256: `e106cffa371f0667d2d801a6b1dd9fb9d4b28129bfdb6c8793196ae165f63755`
- Blocks: 259
- Deterministic repair attempts: 0
