# Don’t Drop the Baton: Long-Horizon Robot Manipulation via Agentic Subtask Exploration and Transition-Aware Memory

## Executive summary

The paper presents Baton, an LLM coding agent that decomposes long-horizon manipulation into short subtasks, explores them separately, and stores explicit invocation, handoff, and lookahead transitions in language memory while keeping the VLA frozen. On RoboMemArena, the reported average is 57.7% task success and 78.8% cumulative success, ahead of the strongest reported non-oracle comparator. The central idea is compelling and the main comparison is favorable, but the supplied paper contains no component ablation, uncertainty estimates, repeated-run variance, implementation artifact, prompt specification, or measured exploration-cost table; consequently, the evidence does not isolate which mechanism causes the gain or establish statistical robustness.

## Problem

**Statement.** Long-horizon manipulation fails even when individual contact-rich skills work: errors accumulate, each predecessor changes the successor’s starting state, and a locally successful execution may be unusable by the next subtask.

**Why it matters.** The failure occurs at composition rather than merely at individual skills: the paper reports that a policy can complete many intermediate stages yet finish few full tasks, making boundary reliability essential for generalist manipulation.

**Scope.** The work targets multi-stage, thousand-step manipulation executed by an LLM coding agent over analytic free-space primitives and a frozen callable contact-rich policy. It focuses on test-time exploration, subtask composition, and transition memory rather than parameter training.

## Method

Baton first drafts an ordered decomposition of the task into subtasks and boundaries. It explores missing subtasks independently, stores successful coarse symbolic trajectories and failed attempts, and composes verified units hierarchically. Its memory represents three crossings explicitly: an invocation condition checked from the wrist camera before calling the frozen VLA; a handoff condition that repairs predecessor residue before the successor starts; and a lookahead constraint that selects a current strategy according to the remaining plan. One LLM plays the explorer, verifier, and scheduler roles, and no model parameters are updated.

### Key components

- Hierarchical subtask exploration: solve short subtasks independently and compose verified units outward, localizing failures to a subtask or newly introduced boundary.
- Failure and skill memory: record unsuccessful attempts and store successful coarse trajectories using symbolic perception queries rather than fixed coordinates.
- Invocation transition: a verifier checks a language-stated readiness condition on the live wrist-camera image and permits VLA_ACT only when the condition holds.
- Handoff transition: an edge stores the successor’s entry condition and uses analytic primitives to restore the scene when the predecessor leaves incompatible residue.
- Lookahead transition: a scheduler reads the remaining plan and retrieves a rival execution strategy whose outcome satisfies downstream constraints.
- Node-and-edge memory: nodes contain rival trajectories and invocation conditions; edges contain handoff entry conditions and lookahead execution constraints, jointly forming a language-level handoff contract.

### Assumptions

- A long-horizon instruction can be decomposed into an ordered chain of short-horizon contact-rich subtasks with checkable interfaces.
- The frozen contact-rich backend exposes the same callable interface as VLA_ACT, including a task-conditioned prompt and stop predicate.
- The LLM agent can reliably draft symbolic conditions, judge wrist-camera readiness, diagnose failures, and select strategies from language memory.
- Analytic primitives can reorient, reopen, and restage the robot or scene sufficiently to satisfy boundary conditions.
- A single reference scene configuration provides exploration experience that transfers to held-out configurations.
- Transition entries keyed by transition type can transfer across tasks and semantically related object/container settings.

## Main claims

- **The authors claim Baton is the first coding agent to execute long-horizon robot manipulation end to end over a frozen VLA while learning through test-time exploration without parameter updates.**
  - Evidence: [b00014-fd242d6c68] “We present Baton, the first coding agent to carry long-horizon robot manipulation end to end over a frozen VLA, learning by test-time exploration with no parameter updates.”
- **The method changes exploration from whole-task search to per-subtask search, making the stated scaling additive and making failures attributable to named stages or boundaries.**
  - Evidence: [b00046-d98a6014fb] “Exploration is priced per piece: if a single subtask reaches its first success after T episodes on average, the chain costs on the order of K​T short episodes, plus the composite runs of the rollout below, rather than TK long ones.”; [b00046-d98a6014fb] “And blame is localized: a failure now happens inside a named subtask or at a named boundary, where it can be diagnosed and repaired, instead of voiding a thousand-step episode.”
- **Baton explicitly represents invocation, handoff, and lookahead transitions in memory.**
  - Evidence: [b00051-73260ab322] “The memory keeps one kind of entry for each of the three; we take them in turn, then the store that unifies them.”
- **The invocation transition gates VLA execution on a live wrist-camera readiness judgment and restages rather than forcing an unready attempt.**
  - Evidence: [b00055-dbfc1b6e77] “VLA_ACT may fire only when a stated readiness condition holds on the wrist camera, judged from the live wrist image by an agent role we call the verifier.”; [b00055-dbfc1b6e77] “On failure the agent re-stages with analytic primitives and checks again; an attempt that cannot be made ready is recorded in failure memory, never forced through the gate.”
- **The handoff transition stores a pair-specific entry condition and restores the successor’s starting state with analytic primitives.**
  - Evidence: [b00057-11805e0d8b] “The boundary therefore records an entry condition: what the wrist view must show for uk+1 to start cleanly, here the gripper restored to vertical, open, and above the can.”; [b00057-11805e0d8b] “The same verifier enforces it at the boundary, restoring the state with analytic primitives (re-orient, re-open, re-stage) before the next skill starts.”
- **The lookahead transition makes downstream requirements determine which rival strategy executes the current subtask.**
  - Evidence: [b00060-af4c43c240] “Before uk executes, it reads the remaining plan 𝒫>k=⟨uk+1,…,uK⟩, collects the constraints its boundaries induce, and retrieves the rival that satisfies them, so the same query “pick up the can” returns the side grasp when a microwave placement follows and the deep top grasp when transport and pouring do.”
- **The memory retains multiple strategies for a subtask and adds a new rival only when an existing strategy violates a constraint and constrained re-exploration succeeds.**
  - Evidence: [b00062-65bd54888c] “Rivals are not enumerated in advance: a first success enters alone, and a new rival is added exactly when a constraint rules the incumbent out and re-exploration under it succeeds; the incumbent is kept and annotated, so the set grows with the boundaries the subtask has served.”

## Results

- **Baton reports an average task success rate of 57.7% and cumulative success rate of 78.8%; the paper states these exceed FrameSamp+Modul by 11.6 and 14.9 points, respectively.**
  - Context: Average RoboMemArena evaluation over the two held-out configurations; FrameSamp+Modul is identified as the strongest reported system.
  - Evidence: [b00072-2bc9bf1d51] “Baton attains the best average performance in table 1: 57.7% TSR and 78.8% CSR, exceeding the strongest reported system, FrameSamp+Modul [6], by 11.6 and 14.9 points respectively”
- **Baton’s reported averages also exceed the ground-truth-memory oracle’s 46.1 TSR and 64.8 CSR.**
  - Context: The oracle bounds retrospection alone but is not presented as an overall execution upper bound.
  - Evidence: [b00072-2bc9bf1d51] “surpassing the ground-truth oracle (46.1 and 64.8) on both averages.”
- **Against whole-task Harness VLA under the authors’ exploration setup, Baton reports 57.7% TSR versus 26.9% TSR.**
  - Context: The paper describes this as comparing two ways of spending the same exploration budget on the same reference seed.
  - Evidence: [b00074-31393aed59] “Whole-task Harness VLA reaches a first success only where the chain is short enough to bootstrap end to end: it performs strongly on sequence (82.0 TSR) but never solves an occlusion task during exploration, and its average (26.9 TSR) barely exceeds reactive π0.5. Baton explores the same seed subtask by subtask and reaches 57.7% TSR”
- **The largest stated category margins over the strongest reported system are on occlusion, 50.0 versus 39.1, and counting, 68.8 versus 31.4.**
  - Context: Per-category RoboMemArena TSR comparison.
  - Evidence: [b00074-31393aed59] “with the largest margins over the strongest reported system on occlusion (50.0 vs. 39.1) and counting (68.8 vs. 31.4).”
- **The paper reports that Baton converts 73% of completed stages into completed tasks, the highest ratio in the table.**
  - Context: The authors interpret this descriptive ratio as evidence that remaining failures are less concentrated at boundaries.
  - Evidence: [b00074-31393aed59] “It also converts 73% of its completed stages into completed tasks, the highest ratio in the table, indicating that the remaining failures concentrate less at the boundaries.”
- **Transferring is the only category where a reported system remains ahead of Baton; the authors attribute much of the deficit to task 19 scoring zero on held-out seeds regardless of execution.**
  - Context: This is an author-reported benchmark defect, not a corrected evaluation.
  - Evidence: [b00074-31393aed59] “Transferring is the single category in which a reported system remains ahead; the deficit is largely an evaluation artifact, as the BDDL scene definition of one of the four transferring tasks (task 19) is faulty on the held-out seeds, so every rollout of that task scores zero regardless of execution.”
- **A shown successful evaluation task runs over 1800 steps and is described as roughly 13 times a typical LIBERO task’s length.**
  - Context: Illustrative held-out rollout rather than an aggregate result.
  - Evidence: [b00058-7b08dd66c5] “This task runs over 1800 steps, roughly 13 times the length of a typical LIBERO task.”

## Experimental evaluation

### Datasets

- RoboMemArena: 26 partially observable household tasks averaging over 1,000 steps, with 3–9 verification stages and four categories—transferring, occlusion, counting, and sequence.
  - Evidence: [b00070-5b8a9d1084] “Its 26 household tasks average over 1,000 steps and 3–9 verification stages in partially observable kitchen scenes, with 68.9% of subtasks memory-dependent; stage-level predicates make TSR and CSR measurable.”; [b00070-5b8a9d1084] “Tasks fall into four categories: transferring (4 tasks), a source-to-target mapping among visually similar containers; occlusion (11), the locations and states of objects out of view; counting (7), how many times an action has already been performed; and sequence (4), a prerequisite subtask’s outcome that decides the next action.”
- Exploration uses reference configuration seed 50; evaluation uses held-out seeds 51 and 52, and reported values average those evaluation configurations.
  - Evidence: [b00068-17f0fcbd2e] “For every task, all exploration runs on a single reference configuration, seed 50; evaluation runs on two held-out configurations, seeds 51 and 52, and every number we report averages the two.”

### Baselines

- Benchmark-reported baselines: π0.5, HiF-VLA, MemoryVLA, MemER, PrediMem with and without ground-truth memory, FrameSamp+Modul, and GPT-5.4 as a frozen VLM-only agent.
  - Evidence: [b00068-17f0fcbd2e] “Reported by the benchmark [18]: reactive π0.5 [12]; the memory-augmented VLAs HiF-VLA, MemoryVLA [29], and MemER [32]; PrediMem, the benchmark’s own dual-system memory VLA, with and without ground-truth memory; FrameSamp+Modul [6]; and GPT-5.4 acting as a frozen VLM agent without a manipulation harness.”
- Author-run baseline: unmodified Harness VLA explores each full task on the reference seed with an exploration budget of 20 episodes, then evaluates on the same held-out seeds as Baton.
  - Evidence: [b00068-17f0fcbd2e] “Run by us: Harness VLA unmodified [40], exploring each task whole on the same seed 50, equipped with all of its own task-specific and global memory and given an exploration budget of 20 episodes per full task, then evaluated on the same held-out seeds.”
- PrediMem with ground-truth memory is treated as an oracle for retrospection and excluded from bolding.
  - Evidence: [b00063-958946756e] “The ground-truth oracle executes with perfect memory of the past and bounds what retrospection alone can achieve; it is excluded from bolding.”

### Metrics

- Task success rate (TSR): all verification stages are satisfied.
  - Evidence: [b00068-17f0fcbd2e] “Metrics are the benchmark’s task success rate (TSR, all verification stages satisfied)”
- Cumulative success rate (CSR): fraction of stages completed.
  - Evidence: [b00068-17f0fcbd2e] “and cumulative success rate (CSR, fraction of stages completed).”
- The authors additionally discuss the ratio of completed tasks to completed stages as a boundary-failure indicator, although it is not introduced as an official benchmark metric.
  - Evidence: [b00074-31393aed59] “It also converts 73% of its completed stages into completed tasks, the highest ratio in the table, indicating that the remaining failures concentrate less at the boundaries.”

### Ablations

- —

### Negative results

- Whole-task Harness VLA never solves an occlusion task during exploration and averages 26.9 TSR.
  - Evidence: [b00074-31393aed59] “it performs strongly on sequence (82.0 TSR) but never solves an occlusion task during exploration, and its average (26.9 TSR) barely exceeds reactive π0.5.”
- GPT-5.4 used as a frozen VLM agent without a manipulation harness obtains 8.7 TSR, which the authors interpret as showing that reasoning alone does not close the gap.
  - Evidence: [b00073-120a1bc97d] “The frozen VLM agent without a manipulation harness fails almost entirely (8.7 TSR), which indicates that a reasoning layer alone does not close the gap either.”
- Occlusion is the hardest category for every reported method, with the oracle reaching only 33.6 TSR.
  - Evidence: [b00073-120a1bc97d] “while occlusion remains the hardest category for every reported method (the oracle itself reaches only 33.6 TSR).”
- One transferring task is reported faulty on held-out seeds and scores zero regardless of execution.
  - Evidence: [b00074-31393aed59] “the BDDL scene definition of one of the four transferring tasks (task 19) is faulty on the held-out seeds, so every rollout of that task scores zero regardless of execution.”


## Limitations

- No component ablation is supplied, so the independent contributions of hierarchical exploration, invocation gating, handoff repair, lookahead scheduling, failure memory, and rival-strategy retention cannot be separated.
  - Evidence: [b00042-51692b33de] “Two designs follow. This section scopes exploration to one subtask at a time and composes verified units outward, boundary by boundary, so that cost stays additive and failures stay attributable; section 3.4 then equips this exploration with a transition-aware memory, one entry for each of the three transitions the chain must cross, written during exploration and read at execution.”; [b00066-32d6c349df] “Our evaluation asks one question: does making the subtask the unit of exploration, and the transition the unit of memory, recover the composite-task performance that stage-level competence fails to predict (table 1)?”
- Evaluation averages only two held-out scene configurations after exploration on one reference configuration; the supplied text reports no repeated exploration runs, confidence intervals, or significance tests.
  - Evidence: [b00068-17f0fcbd2e] “For every task, all exploration runs on a single reference configuration, seed 50; evaluation runs on two held-out configurations, seeds 51 and 52, and every number we report averages the two.”
- The claimed additive exploration advantage is primarily a scaling argument in the supplied blocks; actual exploration episodes, tokens, wall-clock time, or robot steps for Baton are not tabulated.
  - Evidence: [b00046-d98a6014fb] “the chain costs on the order of K​T short episodes, plus the composite runs of the rollout below, rather than TK long ones.”
- The comparison mixes benchmark-reported rows with methods rerun by the authors, which may limit strict apples-to-apples control over implementations and experimental conditions.
  - Evidence: [b00063-958946756e] “Rows in the top group are reported by the benchmark; rows in the middle group we run ourselves.”
- A faulty held-out benchmark task forces zero scores regardless of execution, and the paper reports but does not provide a corrected aggregate excluding or repairing it.
  - Evidence: [b00074-31393aed59] “the BDDL scene definition of one of the four transferring tasks (task 19) is faulty on the held-out seeds, so every rollout of that task scores zero regardless of execution.”
- The method assigns decomposition, verification, scheduling, and exploration roles to one LLM, but the supplied paper does not quantify verifier errors, decomposition failures, scheduler mistakes, or sensitivity to the chosen LLM.
  - Evidence: [b00042-51692b33de] “All roles described below are played by one LLM agent, and no parameters are updated anywhere in the system.”
- Empirical validation is confined to RoboMemArena in the supplied blocks; transfer to real robots, other simulators, other frozen contact policies, or substantially different task families is not demonstrated.
  - Evidence: [b00068-17f0fcbd2e] “Our suite is RoboMemArena [18], described below.”
- The authors state that any compatible contact-rich backend could replace the VLA, but no backend-swap experiment is supplied.
  - Evidence: [b00042-51692b33de] “any contact-rich policy exposing the same call could serve as the backend.”

## Reproducibility

**Status:** weak

The experimental protocol is partially described, but the supplied document lacks the artifacts and operational detail required to independently reconstruct the agent, its memory, and its exploration process. Exact rerunning and verification of the central cost claim are therefore not supported by the supplied material.

**Available artifacts**

- The supplied paper specifies the benchmark, reference and held-out configuration seeds, metrics, baseline families, the frozen π0-family VLA setup, and the whole-task baseline’s exploration budget.
- The method provides qualitative descriptions of decomposition, hierarchical composition, memory structure, verifier gating, handoff restoration, and scheduler retrieval.

**Missing pieces**

- Source code and executable environment
- Exact π0-family checkpoint and exact LLM model/configuration used for Baton
- Agent prompts, role prompts, tool schemas, and decoding parameters
- Complete readiness conditions, handoff contracts, memory entries, and failure-memory format
- Task decompositions and exploration traces for all benchmark tasks
- Baton’s per-subtask and total episode budgets, token use, robot-step cost, wall-clock cost, and stopping rules
- Number of evaluation rollouts per task and seed
- Randomness controls, repeated-run variance, confidence intervals, and statistical tests
- Component ablations and sensitivity analyses
- Corrected evaluation for the faulty transferring task

## AIDB assessment

- Novelty: The strongest conceptual novelty is treating subtask transitions—not only skills or episodic history—as explicit, language-level memory objects. The combination of per-subtask agentic exploration, runtime invocation readiness checks, pair-specific handoff repair, and remaining-plan-conditioned rival-strategy retrieval is distinct within the paper’s comparison framing. First-of-kind claims remain author claims because the supplied evidence does not independently establish literature completeness.
- Usefulness: Potentially high for systems that already expose a frozen contact-rich policy as a callable primitive and need auditable, reusable long-horizon orchestration. The node-edge memory and boundary contracts are practical design abstractions. Adoption risk remains substantial because verifier reliability, agent cost, implementation details, and component causality are not established.
- Confidence: medium
- Recommended action: read
- Rationale: The average RoboMemArena results and direct Harness VLA comparison justify close reading and replication. However, immediate adoption is premature: there are no ablations, no statistical uncertainty, no measured Baton exploration-cost accounting, only two held-out configurations, a known faulty task, and insufficient implementation detail.

## Uncertainties

- **Whether the performance improvement comes mainly from decomposed exploration or from one particular transition-memory mechanism.** — Without component ablations, implementers cannot know which parts are necessary or whether the full system complexity is justified.
  - Evidence: [b00042-51692b33de] “Two designs follow. This section scopes exploration to one subtask at a time and composes verified units outward, boundary by boundary, so that cost stays additive and failures stay attributable; section 3.4 then equips this exploration with a transition-aware memory, one entry for each of the three transitions the chain must cross, written during exploration and read at execution.”
- **Whether exploration is empirically additive in total episodes, tokens, robot steps, and wall-clock time after including composite rollout and boundary repair.** — Reduced exploration cost is a central motivation, but the stated expression explicitly adds unquantified composite runs.
  - Evidence: [b00046-d98a6014fb] “the chain costs on the order of K​T short episodes, plus the composite runs of the rollout below, rather than TK long ones.”
- **How robust the reported averages are to exploration randomness and additional evaluation configurations.** — A single exploration configuration and two held-out configurations do not expose run-to-run variability or support statistical confidence.
  - Evidence: [b00068-17f0fcbd2e] “For every task, all exploration runs on a single reference configuration, seed 50; evaluation runs on two held-out configurations, seeds 51 and 52, and every number we report averages the two.”
- **How often the wrist-image verifier accepts unsafe or unready states, rejects valid states, or fails to restore a boundary condition.** — Verifier errors could dominate safety, exploration cost, and long-horizon success, yet no verifier-specific metric is reported.
  - Evidence: [b00055-dbfc1b6e77] “VLA_ACT may fire only when a stated readiness condition holds on the wrist camera, judged from the live wrist image by an agent role we call the verifier.”
- **Whether transition-type keys transfer reliably across semantically related but visually and geometrically different settings.** — Reusable cross-task memory is central to the claimed amortization, but the supplied evaluation does not isolate transfer of individual edge entries.
  - Evidence: [b00062-65bd54888c] “Edges are keyed by transition type rather than by task, so “release into a container with a narrow lip” transfers from baskets to bins;”
- **How results would change after repairing or excluding the faulty transferring task.** — The defect changes category and potentially average rankings, while the supplied paper gives no corrected table.
  - Evidence: [b00074-31393aed59] “the BDDL scene definition of one of the four transferring tasks (task 19) is faulty on the held-out seeds, so every rollout of that task scores zero regardless of execution.”

## Open questions

- What exact LLM, frozen VLA checkpoint, prompts, decoding settings, and perception/control APIs were used?
- How many exploration episodes, planner tokens, environment steps, and wall-clock hours did Baton consume per subtask, boundary, task, and benchmark overall?
- What are the results of removing hierarchical exploration, invocation gating, handoff restoration, lookahead scheduling, failure memory, and rival-strategy retention one at a time?
- How accurate is the verifier, and what are its false-accept and false-reject rates for invocation and handoff conditions?
- How frequently does the scheduler select an incompatible rival, and how often does constrained re-exploration add a new strategy?
- Do transition entries learned in one task measurably improve unseen tasks that reuse the same transition type?
- Are the gains stable across repeated exploration runs and a broader set of held-out configurations?
- What are the corrected TSR and CSR values after repairing or excluding the faulty transferring task?
- Does Baton retain its advantage with different LLMs, VLA/WAM backends, real-robot observations, and noisy wrist cameras?
- How does memory size, retrieval latency, contradiction rate, and performance evolve as many tasks and rival strategies accumulate?

## Proposed AIDB experiments

- **Hypothesis:** Hierarchical subtask exploration reduces total search cost while preserving or improving full-task success relative to whole-task exploration.
  - Baseline: Unmodified Harness VLA exploring each task whole under an equal total budget.
  - Primary metric: Median environment steps to first full-task success across repeated exploration runs, with planner tokens and wall-clock time reported as secondary costs.
  - Stop condition: Stop when every method reaches the common budget on every task or when the pre-registered confidence interval for the median paired cost difference excludes zero.
- **Hypothesis:** Each transition mechanism provides an independent improvement beyond hierarchical exploration alone.
  - Baseline: Baton with hierarchical exploration and all transition mechanisms enabled.
  - Primary metric: Held-out task success rate under separate removals of invocation gating, handoff restoration, and lookahead scheduling.
  - Stop condition: Stop after the pre-registered number of repeated runs across all held-out configurations; reject an independent contribution when its removal does not reduce task success beyond the pre-specified equivalence margin.
- **Hypothesis:** Explicit invocation and handoff conditions prevent incompatible states from reaching the frozen VLA or successor skill.
  - Baseline: The same trajectories using fixed invocation timing and no boundary restoration.
  - Primary metric: Rate of incompatible transition crossings, adjudicated by task-specific ground-truth readiness predicates or blinded human labels.
  - Stop condition: Stop after each transition type has the pre-registered minimum number of positive and negative examples and the confidence interval on the error-rate reduction reaches the target precision.
- **Hypothesis:** Remaining-plan-conditioned rival retrieval improves downstream completion compared with using one canonical strategy per skill.
  - Baseline: A memory that keeps only the first successful strategy for each subtask and ignores the remaining plan.
  - Primary metric: Success rate of the immediate successor and the complete remaining suffix after executing a strategy-sensitive subtask.
  - Stop condition: Stop after all pre-registered strategy-sensitive boundaries have sufficient repeated trials to test the minimum effect size.
- **Hypothesis:** Transition entries transfer across tasks rather than merely memorizing task-specific sequences.
  - Baseline: Baton with edge-memory transfer disabled, forcing each unseen task to relearn its boundaries.
  - Primary metric: Exploration episodes required to cross reused boundary types on held-out task compositions.
  - Stop condition: Stop when all held-out compositions reach the shared exploration budget or the transfer condition shows a pre-registered reduction with a confidence interval excluding zero.
- **Hypothesis:** The reported ranking remains stable after benchmark repair and across broader evaluation variation.
  - Baseline: The published evaluation protocol and uncorrected task set.
  - Primary metric: Average task success rate after repairing the faulty task and evaluating repeated exploration runs over additional held-out configurations.
  - Stop condition: Stop after the pre-registered seed set is complete; flag instability if Baton’s advantage over the strongest non-oracle comparator crosses zero.
- **Hypothesis:** Baton’s benefit is not specific to one LLM or frozen contact-rich backend.
  - Baseline: The paper’s original LLM-agent and frozen-VLA configuration.
  - Primary metric: Task success rate across a factorial comparison of multiple LLM agents and at least one alternative compatible contact-rich backend.
  - Stop condition: Stop after every pre-registered model-backend pair completes the same tasks and budgets; reject backend independence if the advantage disappears outside the original pair.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-08-19T18:00:47.298444+00:00`
- Document SHA-256: `3b8765f7625f364693ada55871b68b04079bf7749a357220094ba4f04d599574`
- Metadata SHA-256: `7ba5be7ecaa555b443608bd027564a3db0f00a9ff64608f3370f5df57ec8fa7f`
- Blocks: 119
- Deterministic repair attempts: 0
