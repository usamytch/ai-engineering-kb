# CompAct-Bench: A Benchmark for Working-Context Compaction in Long-Horizon Agent Tasks

## Executive summary

CompAct-Bench evaluates context compaction by its effect on subsequent agent completion rather than summary similarity. It controls compacted length, executor, restored environment, and remaining action budget across Search, Coding, and Workspace tasks. Under aggressive compaction, even the strongest model retains limited downstream reliability. Stage effects reverse by domain: later Search worsens while Coding improves, consistent with repository state preserving materialized progress. Key threats are selection of reliably solved tasks, one boundary per trajectory, executor dependence, an internal Workspace suite, imperfect length calibration, and incompletely documented human validation.

## Problem

**Statement.** The paper asks whether a shorter model-generated representation of accumulated interaction history preserves enough working state for an agent to finish a long-running task.

**Why it matters.** Finite context windows make context management necessary, but a concise retrospective summary can still omit or distort facts, progress, epistemic status, constraints, and unresolved obligations needed for future actions.

**Scope.** The study covers information seeking, software engineering, and workspace automation. It evaluates robustness of previously successful executions after an intermediate handoff, not general task-solving ability or a complete production memory policy.

## Method

The authors screen tasks with three executor runs, retain only consistently solved tasks with nontrivial histories, and select one successful reference trajectory. Each trajectory is assigned to an early, middle, or late compaction boundary. The pre-boundary interaction body is compacted once while the system/task head remains verbatim. Iterative Ratio Calibration controls character length. Three fresh continuations resume from the boundary environment with fixed executors, tools, evaluators, and a matched remaining-action budget; strict success is averaged across continuations.

### Key components

- A process-level benchmark built from successful agent trajectories without reference summaries.
- Separation of the evaluated compactor from fixed downstream executors and task evaluators.
- Character-level Iterative Ratio Calibration for approximately matched compacted-output lengths.
- Reconstructed boundary environments and continuation budgets matched to the reference remainder.
- Bootstrap uncertainty, execution-stage comparisons, without-history controls, state-persistence analyses, and trajectory-grounded error annotation.

### Assumptions

- Consistent success in screening makes the reference execution stable enough to attribute later degradation mainly to compaction.
- Deterministic action replay reconstructs a sufficiently comparable environment although outputs need not be byte-identical.
- Character-length matching provides a useful cross-provider control despite not matching tokenizer usage or full assembled-context length.
- Holding one compacted context fixed across fresh continuations separates rollout variability from compaction-generation variability.
- Findings obtained with the selected prompts, executors, tools, and evaluators meaningfully represent compaction capability.

## Main claims

- **The benchmark measures compaction functionally through downstream completion rather than resemblance to a reference summary.**
  - Evidence: [b00007-0ee0b619c8] “The final task outcome provides a direct functional measure of the effect of compaction on subsequent execution”; [b00044-39f4080cc3] “without requiring manually constructed reference summaries or compaction labels”
- **The protocol fixes major continuation variables across compactors and treats the compacted working context as the primary variable.**
  - Evidence: [b00039-d65d5995d9] “The task, boundary environment state, executor, and budget are therefore fixed across compactors, leaving Mb as the primary variable.”; [b00154-aa5b66ad54] “The same compacted context is then held fixed across three independent continuations.”
- **Dependence on textual compaction varies with whether prior progress remains available in the environment.**
  - Evidence: [b00258-0e4c08e9bb] “everything the executor has learned before the boundary exists only in Hb.”; [b00267-00da64809c] “Compacted context therefore contributes most where task state lives in the context rather than in the environment.”
- **Compaction can alter epistemic or procedural meaning rather than merely omit factual content.**
  - Evidence: [b00303-5a678ce392] “compaction can alter the epistemic or procedural meaning of retained information rather than merely omit facts.”; [b00281-d43d1f1626] “69.1% are preserved, 25.3% omitted, 5.6% distorted, and 0.1% uncertain.”

## Results

- **At the 10% retention setting, Claude Opus 5 obtains 68.5% overall post-compaction accuracy; performance across compactors ranges from 46.0% to 68.5%, averaging 56.7%.**
  - Context: This is strict downstream accuracy on tasks selected for reliable success before compaction. It measures robustness to history replacement rather than unconstrained task-solving ability.
  - Evidence: [b00054-85bc61660f] “under the default 10% retention setting”; [b00055-62522999e8] “Claude Opus 5 achieves the highest observed overall score of 68.5%”; [b00055-62522999e8] “overall post-compaction performance ranges from 46.0% to 68.5%, with an average of 56.7%.”
- **Stage effects reverse by domain: Search falls from 52.9% at the 25% boundary to 42.6% at 50% and 34.6% at 75%, whereas Coding rises from 64.0% to 72.7% and 86.1%. Nine of twelve compactors decline monotonically on Search, while ten rise monotonically on Coding.**
  - Context: Each trajectory belongs to one stratified boundary group, so this is a between-task stage comparison rather than repeated evaluation of every task at every boundary. The reversal weakens a universal input-length explanation.
  - Evidence: [b00060-d163a25fbe] “Search performance decreases from 52.9% at the 25% boundary to 42.6% at 50% and 34.6% at 75%.”; [b00060-d163a25fbe] “Coding shows the opposite pattern, increasing from 64.0% to 72.7% and 86.1%, respectively.”; [b00060-d163a25fbe] “nine of the twelve compactors show a monotonic decrease on Search, whereas ten show a monotonic increase on Coding”
- **For Coding, continuation without history from the reconstructed boundary state reaches 66.7%, 58.1%, and 71.9% across boundaries, versus 48.5%, 35.5%, and 15.6% from the initial state. Adding compacted context produces 64.0%, 72.7%, and 86.1%, with gains of −2.7, +14.6, and +14.2 points.**
  - Context: The controlled comparison supports the state-persistence account: repository progress can survive independently of text, while compacted context adds value at later boundaries. Its observed early-boundary increment is negative.
  - Evidence: [b00269-f07566b5d7] “Coding Without Hb, initial state 48.5 35.5 15.6 Without Hb, boundary state 66.7 58.1 71.9”; [b00269-f07566b5d7] “With Mb 64.0 72.7 86.1 Gain −2.7 +14.6 +14.2”
- **Among failed continuations, an annotated compaction error occurs in 92.5% of early failures and 85.8% of budget exhaustions. Critical omission is associated with +18.2 points of repeated work, progress/state loss with +13.8, and constraint/goal distortion with +10.5 points of unverified commitment.**
  - Context: These are associations restricted to failed cases, not causal estimates. Initial annotations are model-generated, with manual review reported only for a subset.
  - Evidence: [b00291-90e09864e0] “92.5% of early failures and 85.8% of budget exhaustions”; [b00291-90e09864e0] “critical omission (+18.2), lost resolution (+14.2), and progress/state loss (+13.8)”; [b00291-90e09864e0] “Constraint/goal distortion and factual distortion are associated with more unverified commitments (+10.5 and +7.3).”

## Experimental evaluation

### Datasets

- BrowseComp information-seeking tasks.
  - Evidence: [b00009-df01ceca08] “79 BrowseComp information-seeking tasks”
- SWE-bench software-engineering tasks, implemented with SWE-bench Verified.
  - Evidence: [b00009-df01ceca08] “96 SWE-bench software-engineering tasks”; [b00152-73307c9ba1] “For Coding, we use SWE-bench Verified in an isolated sandbox”
- CompanyBench workspace tasks, used as an internal validation domain rather than a core public component.
  - Evidence: [b00009-df01ceca08] “25 CompanyBench workspace tasks”; [b00016-ebc52bc6ea] “CompanyBench serves as an additional validation domain rather than a core public component of the benchmark.”

### Baselines

- Twelve language models compared as compactors under shared trajectory content, instructions, target, and calibration.
  - Evidence: [b00136-c922aad129] “Every compactor receives the same trajectory content, the same default instruction, the same target retention ratio, and the same Iterative Ratio Calibration (IRC) procedure.”
- Continuation without either original or compacted history from the reconstructed boundary environment.
  - Evidence: [b00251-b1d06bcb29] “the executor receives the original system/task head and the environment state at the boundary, but neither Hb nor Mb.”
- Continuation from the initial unmodified Coding repository without history.
  - Evidence: [b00260-33516eaddf] “The initial-state condition of Appendix F.1 skips replay and starts from the unmodified repository.”

### Metrics

- Strict task success within the matched action budget, successful terminal state, and acceptance by the source evaluator.
  - Evidence: [b00159-bf68532886] “completes within the matched T−b action budget, reaches a terminal state marked successful, and is accepted by the source benchmark evaluator.”
- Avg@3 over fresh continuations sharing one fixed compacted context.
  - Evidence: [b00162-ebfc726245] “this one-compaction, three-continuation, Avg@3 protocol”
- Task-level percentile-bootstrap confidence intervals.
  - Evidence: [b00218-d5d11eb5c9] “We use a stratified task-level percentile bootstrap with 10,000 resamples.”; [b00219-473de0db9e] “task-level bootstrap 95% confidence intervals”
- Realized character-level retention ratio and tolerance adherence.
  - Evidence: [b00189-f9275386ba] “In Tol. is the share inside [0.097,0.103]”

### Ablations

- Without-history continuation from initial versus reconstructed Coding state, then addition of compacted context under the same boundary state.
  - Evidence: [b00267-00da64809c] “This comparison holds the boundary state fixed and varies only whether the executor receives Mb.”
- Observational Coding split according to whether a repository edit was materialized before the boundary.
  - Evidence: [b00263-3b97fa4f04] “Tasks with an edit have a mean strict Avg@3 accuracy of 86.9%, versus 53.0% without an edit”
- Calibration at other target ratios without downstream execution.
  - Evidence: [b00192-7fa95ac3c4] “It measures only the realized compaction length; no downstream continuation is run.”

### Negative results

- Even the strongest compactors still fail many compaction instances.
  - Evidence: [b00055-62522999e8] “Even among the strongest models, a substantial fraction of compaction instances still fail”
- Length calibration becomes unreliable at high retention targets.
  - Evidence: [b00193-2aa9fde35b] “Adherence declines once the target exceeds 20%”; [b00193-2aa9fde35b] “at 80% only 18–44% are”
- Adding compacted context at the early Coding boundary has a negative observed increment.
  - Evidence: [b00269-f07566b5d7] “Gain −2.7 +14.6 +14.2”
- Most failed continuations exhaust their action budgets.
  - Evidence: [b00243-a9c8089f7d] “91.6% of failed Search continuations, 92.0% of failed Coding continuations, and 97.7% of failed Workspace continuations exhausted their budgets”


## Limitations

- Selection conditions on tasks the chosen executor solves consistently, strengthening attribution but narrowing validity to robustly solvable tasks.
  - Evidence: [b00204-dfcfad4c75] “We retain only tasks solved in all three runs (pass3)”; [b00205-e88746bebb] “This construction conditions the benchmark on tasks the executor can solve without compaction.”
- Each trajectory is tested at one boundary, so stage effects compare task groups rather than repeated conditions on identical tasks.
  - Evidence: [b00207-97ac54eefd] “each trajectory is assigned to exactly one boundary rather than evaluated at all three.”
- The retention target controls character length, not tokenizer usage or the full assembled context; the retained head is excluded.
  - Evidence: [b00168-4ed82f072a] “r is therefore a text-length constraint, not an exact fraction of an executor’s token window or of the full assembled context.”; [b00144-a78f4fc4e7] “The retained head is not part of the retention budget”
- Length adherence is weakest for the longest Workspace inputs, leaving residual mismatch.
  - Evidence: [b00188-0f22d76b0c] “Adherence is highest for Coding (93.6%), followed by Search (86.9%) and Workspace (59.7%)”
- The Workspace suite is internal and therefore cannot be independently inspected from the supplied material.
  - Evidence: [b00016-ebc52bc6ea] “an internal workspace-oriented task suite”
- Failure annotations originate from a model, while the size and agreement statistics of human validation are not reported.
  - Evidence: [b00275-c011d5ad91] “Initial annotations are produced by GPT-5.6-Sol with high reasoning effort”; [b00289-5d421e02d9] “We manually reviewed a subset of the annotations”
- The strict matched budget prevents extra recovery but intertwines information preservation with recovery efficiency.
  - Evidence: [b00039-d65d5995d9] “This matched budget prevents the executor from compensating for information loss through extra interaction.”

## Reproducibility

**Status:** partial

The detailed protocol should support a close methodological reimplementation for public tasks. Exact end-to-end reproduction remains blocked by missing runnable artifacts, full instance and trajectory data, and the internal Workspace suite.

**Available artifacts**

- Model identifiers, reasoning configurations, and generation parameters are documented.
- The shared compaction prompt, continuation instructions, IRC procedure, hyperparameters, and acceptance interval are supplied.
- Executors, evaluators, task counts, boundary assignments, bootstrap method, and detailed results are described.

**Missing pieces**

- No code repository or downloadable benchmark artifact is identified in the supplied blocks.
- CompanyBench is internal.
- The complete retained task list and full trajectory collection are not supplied.
- Provider endpoint versions, seeds, costs, and full runtime dependencies are incomplete.
- The size, sampling method, and quantitative agreement of the human annotation review are absent.

## AIDB assessment

- Novelty: High: the work evaluates compaction prospectively through controlled downstream execution rather than retrospective summary similarity.
- Usefulness: High for agent-memory evaluation. It distinguishes actionable state preservation from factual coverage and identifies epistemic status, completed work, pending obligations, and located resources as evaluation targets.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled design and extensive appendices make this a strong evaluation template. Adoption should await public artifacts, replication across executors and prompts, within-task boundary comparisons, and more completely documented human validation.

## Uncertainties

- **Whether rankings generalize across executors, continuation prompts, tool harnesses, and reasoning configurations.** — Observed performance may partly reflect compatibility between each compacted representation and the selected downstream executor.
  - Evidence: [b00149-b0d52e5fae] “Within each benchmark, the executor, harness, tools, evaluator, and execution environment are fixed across all compactors.”
- **Whether opposite Search and Coding stage trends persist when every task is evaluated at every boundary.** — Stratification reduces imbalance but cannot eliminate all differences between assigned task groups.
  - Evidence: [b00207-97ac54eefd] “each trajectory is assigned to exactly one boundary rather than evaluated at all three.”
- **Whether error–behavior associations are causal.** — The analysis covers failed cases and naturally occurring errors, so task difficulty may affect both annotations and behavior.
  - Evidence: [b00287-fbac3eeb72] “The error–outcome statistics in Figure 5 and Appendix G.3 are computed over failed continuations only.”
- **How much results depend on the summarization-style prompt and iterative editing procedure.** — Structured, extractive, or handoff-trained representations may preserve state semantics differently.
  - Evidence: [b00146-83df807be6] “Please summarize the above history concisely.”; [b00179-bc0f41e70a] “the compactor is asked to edit the incumbent rather than rewrite it from scratch.”

## Open questions

- Will model rankings and failure modes replicate with different executor families?
- Does iterative calibration alter content quality relative to one-shot length-matched compaction?
- Can explicit fields for confirmed facts, rejected hypotheses, completed work, pending obligations, constraints, and located resources reduce distortion?
- Do within-task evaluations at every boundary reproduce the reported stage effects?
- What accuracy–cost frontier appears when recovery budgets exceed the reference remainder?
- Can full human annotation validate the reported error prevalence and behavioral associations?

## Proposed AIDB experiments

- **Hypothesis:** A structured handoff separating confirmed facts, hypotheses, rejected alternatives, completed work, pending work, constraints, and located resources improves downstream completion at the same length budget.
  - Baseline: The shared free-form compaction prompt with the same compactor, calibration target, executor, environment state, and action budget.
  - Primary metric: Paired difference in strict Avg@3 accuracy; secondary blinded-human rates of premature commitment, lost resolution, and progress/state loss.
  - Stop condition: Complete both conditions for every retained public task; reject the hypothesis if the paired confidence interval does not exclude no improvement or length matching fails.
- **Hypothesis:** The Search decline and Coding improvement across stages persist under within-task boundary evaluation.
  - Baseline: The reported one-boundary-per-trajectory stratified design.
  - Primary metric: Paired within-task change in strict Avg@3 accuracy across early, middle, and late boundaries, reported separately by domain.
  - Stop condition: Complete every eligible public task at every boundary; reject the hypothesis if trend direction reverses or the paired interval includes no stage change.
- **Hypothesis:** A machine-readable progress ledger persisted in the environment reduces dependence on free-form compacted context, especially for Search and pre-edit Coding states.
  - Baseline: The original boundary environment and compacted context without a progress ledger.
  - Primary metric: Strict Avg@3 accuracy, with repeated-work actions and budget-exhaustion rate as secondary metrics.
  - Stop condition: Complete the preregistered paired public-task sample; reject the hypothesis if accuracy does not improve and neither secondary metric decreases.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:21:22.497337+00:00`
- Document SHA-256: `9ea7a05976d1ef636a5df06e636af48951e338cf8bb2801d28f90b060ecb5ad1`
- Metadata SHA-256: `8259ffc2f3b6364fdeaa77ed2a9b9ab0a41dd24f28cac4a68ddc9a8123a2614f`
- Blocks: 342
- Deterministic repair attempts: 1
