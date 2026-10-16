# TRACE: Governing Memory Validity in Evolving Multi-Agent Systems

## Executive summary

The paper distinguishes retrieving a historically correct memory from authorizing it for present action after an agent’s absence. TRACE is a training-free return-time admission layer that reconciles a departure checkpoint with intervening updates, tests explicit and implicit invalidation, applies authorization, temporal, applicability, and provenance gates, and emits a bounded Return View only when obligations are covered. Its strongest evidence concerns implicit invalidation and propagated conflict: TRACE improves joint preservation and rejection relative to simple memory policies and remains stable in the tested scale diagnostic. The evidence does not support universal superiority: TRACE has no consistent gain on explicit-update Memora, consumes substantially more tokens than cheaper policies, remains less accurate than CUPMem on a controlled STALE subset, and depends on authenticated identity, checkpoints, source bindings, candidate coverage, and verifier calibration. It is a promising governance mechanism worthy of replication, but not yet an adoption-ready universal memory layer.

## Problem

**Statement.** A returning agent may retrieve information that was correct when recorded and relevant now, yet no longer admissible for action because the shared state changed during its absence.

**Why it matters.** Persistent-memory systems need to preserve useful continuity without reactivating superseded, unauthorized, or dependency-invalidated premises. Evaluating only final-answer accuracy can conceal whether a system retained valid state or rejected stale state.

**Scope.** The paper studies authenticated agent return under explicit replacement, implicit contextual invalidation, and propagated conflict. It does not establish robustness to forged evidence or arbitrary memory poisoning, and it treats return-time admission rather than the full write-to-retrieval security lifecycle.

## Method

TRACE inserts a training-free governance boundary between a memory backend and a returning agent. It constructs a single return-cycle checkpoint from the departure view and absence-period delta, proposes and verifies implicit dependencies, filters candidate records through separate eligibility gates, selects an obligation-covering set under item and character budgets, validates and signs a Return View, and conditionally readmits private experience only when its bound work-state source survives.

### Key components

- Departure checkpoint containing visible state, source receipts, and epoch; private episodic memory is quarantined until admission.
- Direct handling of epoch conflicts, expired validity, supersession, and revocation, followed by a high-recall dependency scan and grounded verifier for implicit invalidation.
- Four item-level gates: authorization, temporal validity, task applicability, and provenance.
- Obligation-aware, budgeted selection that prioritizes mandatory obligations, progress frontiers, and uncovered critical dependencies.
- Fail-closed coverage gate: incomplete admission triggers reset or blocking rather than release of a partial view.
- Signed Return View bound to return event, identity, role, task, epoch, expiry, item digests, and coverage; private memory is readmitted only through admitted source state.

### Assumptions

- The return is authenticated and preserves the agent’s principal and role.
- A departure checkpoint, absence-period delta, and source receipts or bindings are available.
- Task adapters can specify open obligations, progress frontiers, and evidence dependencies.
- Model-based dependency scanning and verification are sufficiently calibrated to detect consequential implicit invalidations.
- The tested backend adapters retain source associations at enough granularity for admission decisions.

## Main claims

- **Temporal memory admission is distinct from relevance and historical correctness: current action eligibility depends on identity, current state, purpose, obligations, and evidence.**
  - Evidence: [b00009-72b5cbb713] “the returning agent reassesses retained memory against current state, identity, task purpose, and open obligations.”; [b00025-202f2a003e] “turns on authority and state dependence rather than on similarity or recency”
- **TRACE provides an auditable return-time mechanism combining implicit-invalidation verification, item eligibility, obligation-aware selection, and source-bound private-memory readmission.**
  - Evidence: [b00016-c0684e11ac] “combines source-verified implicit invalidation with item-level eligibility checks and obligation-aware memory selection.”; [b00048-fd0c175b45] “A private experience is reinstated only if the work-state item it was bound to remains in the signed view.”
- **The method is intended to jointly preserve valid information and reject invalid information, failing closed when critical obligations cannot be covered.**
  - Evidence: [b00030-a896ec3b02] “preserve the valid information the fresh workload needs, reject items that no longer support current action, and fail closed”; [b00046-e16bce6f36] “the return is reset or blocked rather than issued with an obligation silently omitted.”

## Results

- **On STALE Type II, TRACE improves Overall over the strongest listed comparison policy by 22.3 points for Qwen, 18.5 for Gemini, and 27.5 for DeepSeek; Lifecycle Success reaches 39.00%, 84.20%, and 42.94%, respectively.**
  - Context: This is the paper’s strongest cross-actor evidence for implicit contextual invalidation. Lifecycle Success is a within-episode conjunction of all three probes, so it is stricter than marginal probe accuracy. Aggregation differs: Qwen pools episodes, while Gemini and DeepSeek average strata equally.
  - Evidence: [b00012-a6d187984a] “22.3 points with Qwen, 18.5 with Gemini, and 27.5 with DeepSeek”; [b00065-fd2ca0d2cf] “TRACE reaches 39.00% LS with Qwen, 84.20% with Gemini, and 42.94% with DeepSeek.”; [b00314-cc4125f965] “Cross-model score differences therefore may also reflect the aggregation rule.”
- **On ManBench-Return, TRACE jointly preserves and rejects state across actors: VIA ranges from 92.58% to 98.34% and IIR from 98.44% to 99.47%, while its Overall remains within 3.8 points of the best single-policy baseline.**
  - Context: Reset can score highly on final-answer accuracy while retaining no valid inherited state, and Restore averages incompatible condition-specific behaviors. This supports the paper’s argument that Overall alone is inadequate for evaluating memory admission.
  - Evidence: [b00072-b7ca859dcd] “VIA and IIR are 95.96% and 98.78% with Qwen and 92.58% and 98.44% with DeepSeek”; [b00072-b7ca859dcd] “With Gemini, TRACE reaches 98.32% Overall against Restore’s 98.40%, with 98.34% VIA and 99.47% IIR.”; [b00012-a6d187984a] “within 3.8 points of the best single-policy baseline’s overall accuracy”
- **The component ablation attributes the largest loss to removing implicit invalidation: Overall falls from 52.33% to 26.50%, IIR from 50.50% to 19.50%, and Lifecycle Success from 39.00% to 18.00%. Removing obligation-aware selection, the complete-view gate, or source-bound private readmission also lowers Overall.**
  - Context: The controlled Qwen STALE Type II ablation supports contributions from all four mechanisms, with implicit invalidation dominant. Because each variant removes one component, interactions among components are not isolated.
  - Evidence: [b00324-c509a762d4] “Full TRACE 52.33 52.50 50.50 39.00 w/o II 26.50 34.00 19.50 18.00”; [b00324-c509a762d4] “w/o OAS 38.67 35.50 36.00 29.00 w/o CVG 47.33 48.00 44.00 35.00 w/o SBPR 42.00 43.00 38.50 31.00”
- **TRACE occupies a middle point in the STALE subset’s accuracy–token trade-off: 58.89% Overall at 499,659 tokens per episode, versus CUPMem at 80.56% and 1,994,815 tokens per episode; cheaper policies use 216,006–218,227 tokens per episode.**
  - Context: CUPMem is more accurate but substantially more expensive. Its accounting includes a deterministic failed episode and retries, while token totals do not establish latency, monetary cost, or peak context.
  - Evidence: [b00285-74f44a19ed] “CUPMem 80.56 81.67 85.00 75.00 81.67 63.33 1,994,815”; [b00285-74f44a19ed] “TRACE (Ours) 58.89 61.67 55.00 60.00 53.33 40.00 499,659”; [b00067-2df8eb4952] “216,006–218,227 used by the cheaper methods”; [b00287-9e046859cc] “They are not measurements of latency, monetary cost, or peak context.”
- **The scale diagnostic is stable but limited: across 4, 8, 16, and 32 active agents, TRACE varies by 0.36 points in Overall, 0.30 in VIA, and 0.22 in IIR. Backend integration raises IIR in all four tested pairs but lowers VIA and produces mixed FAMA changes.**
  - Context: These studies support stability in the tested range and interface feasibility, not growing benefits with team size or uniform backend-quality gains.
  - Evidence: [b00081-6a30cc726c] “Varying the number of active agents over 4, 8, 16, and 32”; [b00081-6a30cc726c] “TRACE’s Overall, VIA, and IIR vary by 0.36, 0.30, and 0.22 percentage points”; [b00083-8763cfc934] “IIR increases in all four pairs, by +0.39 to +6.42 points, while VIA decreases by 0.05 to 3.03 points”; [b00083-8763cfc934] “FAMA changes range from −1.35 to +0.48 percentage points.”

## Experimental evaluation

### Datasets

- Memora, recast for return episodes, evaluates selective retention and forgetting across 137 questions from 30 persona–period clusters and three departure positions.
  - Evidence: [b00252-dae1a67a64] “The evaluation includes 137 questions from 30 persona–period clusters.”; [b00252-dae1a67a64] “The same questions are evaluated at three departure positions”
- STALE Type II evaluates implicit invalidation across 200 cases, each with a 50-session history and three probes; strata contain 64, 64, and 72 cases.
  - Evidence: [b00259-1f63ee7954] “The evaluation comprises 200 Type II cases, each with a 50-session history and three probes.”; [b00259-1f63ee7954] “The Early, Middle, and Late strata contain 64, 64, and 72 cases”
- ManBench-Return is a derived adaptation with Old-Valid and Old-Stale conditions, scheduling 4,838 examples from 20 tasks.
  - Evidence: [b00263-01ff087d4c] “Our adaptation has two conditions: Old-Valid tests resistance to misleading updates”; [b00264-910b99733c] “The experiment schedules 4,838 examples from 20 tasks.”

### Baselines

- The common harness compares Static, Restore, Reset, MemStrata, MemTX, and TRACE; CUPMem appears only in the separate STALE subset.
  - Evidence: [b00055-58d3435cd5] “The common harness compares Static, Restore, Reset, MemStrata, MemTX, and TRACE”; [b00055-58d3435cd5] “CUPMem is limited to the STALE subset”
- MemStrata and MemTX are mechanism-faithful reimplementations within the common harness rather than necessarily their original end-to-end systems.
  - Evidence: [b00055-58d3435cd5] “MemStrata and MemTX are mechanism-faithful reimplementations”; [b00213-9dc1a1bb09] “use mechanism-faithful adaptations within the common evaluation harness.”

### Metrics

- Overall is benchmark-specific final accuracy; VIA measures valid-state availability, IIR invalid-state rejection, and WSAR is the complement of IIR.
  - Evidence: [b00057-a9d24a229b] “Overall is benchmark-specific accuracy. VIA and IIR measure valid-state availability and invalid-state rejection, with WSAR as the complement of IIR.”
- On STALE, the native probes are State Resolution, Premise Resistance, and Implicit Policy Adaptation; VIA maps to IPA, IIR requires SR and PR jointly, and Lifecycle Success requires all three within an episode.
  - Evidence: [b00260-b64de4f10c] “Our return metrics map VIA to IPA, IIR to jointly passing SR and PR, and LS to passing all three within the same episode.”
- Memora additionally reports FAMA, while ManBench-Return reports final-answer correctness and an adapted Reality Shift Rate for Old-Valid.
  - Evidence: [b00256-d0371c5ce6] “FAMA applies Equation 13 per question before averaging.”; [b00074-fd128b5f89] “ManBench’s Reality Shift Rate (RSR) measures how often an initially correct answer becomes incorrect after interaction”

### Ablations

- Four single-component removals test implicit invalidation, obligation-aware selection, the complete-view gate, and source-bound private readmission on Qwen STALE Type II.
  - Evidence: [b00322-d0611ab4fa] “This study examines four mechanisms in TRACE using Qwen on STALE Type II.”; [b00070-09afe14ab1] “We ablate implicit invalidation (II), obligation-aware selection (OAS), the complete-view gate (CVG), and source-bound private readmission (SBPR)”

### Negative results

- TRACE does not consistently improve explicit-update Memora and trails Reset on Overall; its average FAMA is below MemTX for all three actors.
  - Evidence: [b00012-a6d187984a] “TRACE offers no consistent gain and trails a Reset policy on overall accuracy.”; [b00063-9fb790f8a3] “its FAMA is 40.14%, 42.80%, and 42.58%”; [b00063-9fb790f8a3] “MemTX obtains 42.14%, 44.12%, and 44.72%.”
- CUPMem is more accurate than TRACE on every reported score in the separate STALE subset, though at much higher token use.
  - Evidence: [b00012-a6d187984a] “CUPMem remains more accurate still on every reported score, at 3.99 times TRACE’s token total.”
- Performance worsens with longer absence in the STALE subset while token use rises.
  - Evidence: [b00094-ed0b8b2955] “Overall falls from 73.33% to 43.33% while tokens per episode rise from 316,750 to 664,860.”


## Limitations

- TRACE assumes authenticated lifecycle identity, a preserved departure checkpoint, and trustworthy source receipts or bindings; these may be demanding deployment prerequisites.
  - Evidence: [b00094-ed0b8b2955] “TRACE assumes an authenticated return, a preserved departure checkpoint, and source receipts.”; [b00213-9dc1a1bb09] “TRACE assumes trustworthy lifecycle identity and source bindings.”
- Implicit invalidation is model-dependent: missed dependencies can admit stale state, while broad checks can discard useful context; the design provides no guarantee that every dependency is found.
  - Evidence: [b00094-ed0b8b2955] “missed dependencies admit stale state, over-broad checks discard useful context”; [b00199-e3e606b071] “this design does not guarantee that every implicit dependency will be found.”
- The derived benchmark, diagnostic scale study, and portability study constrain external validity; portability does not imply uniform quality gains or compatibility with arbitrary stores.
  - Evidence: [b00094-ed0b8b2955] “ManBench-Return is derived, the agent-scale study diagnostic, and the backend study tests portability rather than quality.”; [b00350-d30501ca60] “The results also do not establish compatibility with arbitrary stores”
- The evaluation does not establish resistance to arbitrary memory poisoning or forged evidence.
  - Evidence: [b00213-9dc1a1bb09] “it does not establish resistance to arbitrary memory poisoning or forged evidence.”
- Token totals omit latency, retry-cost characterization beyond the reported case, monetary cost, and peak-context behavior.
  - Evidence: [b00094-ed0b8b2955] “supporting no claim about latency, retry cost, or peak context.”; [b00287-9e046859cc] “They are not measurements of latency, monetary cost, or peak context.”

## Reproducibility

**Status:** partial

The documentation is unusually detailed for an empirical agent-memory paper: protocols, parameters, aggregation rules, failure denominators, detailed tables, and an anonymous artifact are described. The rating remains partial because the artifact was not inspected, excluded provider evidence limits exact auditability, and no independent rerun is reported.

**Available artifacts**

- Anonymous read-only mirror with implementation, frozen configurations, benchmark inputs, and reproduction instructions.
- Per-arm result roots, frozen checkpoints, failure manifests, configuration receipts, and reason-coded Return Views are reported as preserved.
- Public code URL is supplied in the paper metadata and abstract.

**Missing pieces**

- API credentials and raw provider logs are explicitly excluded.
- Author repository history is explicitly excluded.
- Independent reproduction results are not present in the supplied document blocks.
- The supplied blocks do not establish whether all provider-side model versions and nondeterministic settings remain reproducible over time.

## AIDB assessment

- Novelty: The central contribution is a clear lifecycle abstraction: memory at re-entry is treated as an authorization and obligation-coverage decision rather than merely storage, retrieval, or recency filtering. The combination of temporal invalidation, separate eligibility gates, bounded obligation-aware selection, and source-bound private-memory readmission is conceptually coherent within the supplied paper.
- Usefulness: High for designers of persistent multi-agent systems whose members pause and return to evolving shared state. The admission-plane evaluation is particularly useful because it exposes failures hidden by final-answer accuracy. Practical value depends on whether deployments can provide authenticated lifecycle boundaries, source bindings, obligation graphs, and acceptable verifier cost.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled results strongly motivate measuring preservation and rejection separately, and the ablations support the proposed mechanisms. Adoption should wait for matched-budget evaluation, independent artifact reproduction, latency and peak-context measurements, broader open-ended tasks, and adversarial tests. The explicit-update and backend results already show that TRACE is not a universal accuracy improvement.

## Uncertainties

- **It is unclear how much of TRACE’s gain comes from admission structure versus additional model calls, tokens, and verification information.** — Without a matched-budget verifier control, the comparison cannot cleanly attribute improvements to the governance design rather than extra computation or evidence processing.
  - Evidence: [b00096-754bad5100] “Matched-budget verifier controls and held-out return tasks will separate admission gains from extra verification information.”
- **The dependency scanner’s recall is not measured, although verifier selectivity is reported.** — A low acceptance rate does not show whether consequential dependencies were missed; recall failures directly threaten stale-state rejection.
  - Evidence: [b00275-c4bb7d7d31] “they do not change the 200-episode score denominators above or by themselves measure dependency-recall accuracy.”
- **Cross-model STALE comparisons are partly confounded by different aggregation rules.** — Observed actor differences may reflect pooling versus equal-stratum weighting rather than only model capability or method behavior.
  - Evidence: [b00314-cc4125f965] “Cross-model score differences therefore may also reflect the aggregation rule.”
- **Backend effects cannot be attributed to a specific representation or source-binding decision.** — The portability study demonstrates feasibility but offers limited guidance for engineering adapters or predicting retention losses on new stores.
  - Evidence: [b00350-d30501ca60] “They do not isolate which representation or source-binding choice causes a particular gain or loss.”

## Open questions

- Does TRACE retain its preservation–rejection advantage under equal token, call, and context budgets?
- How accurately does the dependency scanner recall truly consequential implicit dependencies, not merely how selectively the verifier accepts proposed pairs?
- What are end-to-end latency, monetary cost, retry rate, and peak-context requirements under realistic concurrent workloads?
- How does the system behave on open-ended tasks where obligations and dependency graphs cannot be reliably supplied by an adapter?
- Can forged provenance, colluding agents, or poisoned absence-period updates defeat the admission boundary?
- Are the reported gains reproduced independently from the frozen artifact across changing model-provider infrastructure?

## Proposed AIDB experiments

- **Hypothesis:** TRACE’s joint VIA–IIR advantage remains after equalizing total model calls, billed tokens, and maximum context against a verification-enhanced baseline.
  - Baseline: A matched-budget Static or MemTX variant using the same actor, retrieval candidates, verification-call budget, and total token ceiling as TRACE.
  - Primary metric: Macro-average of VIA and IIR, with Overall and Lifecycle Success reported as secondary metrics.
  - Stop condition: Reject the hypothesis if TRACE’s paired confidence interval for the macro-average improvement includes zero, or if its token or call budget exceeds the matched ceiling.
- **Hypothesis:** Measured recall of consequential dependency pairs predicts stale-state admission more strongly than verifier acceptance rate alone.
  - Baseline: Current high-recall scanner and grounded verifier, compared with oracle dependency candidates and with scanner-disabled TRACE.
  - Primary metric: Dependency-pair recall against held-out human annotations, jointly reported with IIR and WSAR.
  - Stop condition: Stop if oracle candidates do not materially improve IIR, or if scanner recall reaches a prespecified ceiling while WSAR remains unchanged, indicating another bottleneck.
- **Hypothesis:** TRACE remains beneficial on open-ended return tasks after accounting for latency and incomplete obligation extraction.
  - Baseline: Restore, Reset, Static, and the strongest write-time consolidation baseline under a common end-to-end service budget.
  - Primary metric: Lifecycle Success per unit of p95 latency, with VIA, IIR, peak context, retries, and abstention rate as safeguards.
  - Stop condition: Reject deployment readiness if TRACE fails the service latency budget, has higher wrong-state admission than the strongest baseline, or blocks or resets more often than a prespecified operational threshold.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:07:56.906574+00:00`
- Document SHA-256: `3c6b5116c97b61446faabc2b502ae3fa72a2d86e9b2244c1f0707fe3dd22ed8b`
- Metadata SHA-256: `cd6b3074db7141f8e8afecf874c08d3216d541aefede53842085db37e423888b`
- Blocks: 350
- Deterministic repair attempts: 1
