# A State Change Is Local, Its Consequences Are Not: Dependency-Aware State Revision for Long-Term Agent Memory

## Executive summary

StateGraph targets a real failure mode in long-term agent memory: downstream beliefs and actions can remain accepted after their premise becomes stale. It builds a persistent dependency graph, counterfactually verifies candidate edges, and propagates revision only when strict support fails without an alternative path. On the small, author-constructed StateChangeBench, it substantially outperforms the reported baselines, especially on deeper cascades, and ablations support the contribution of verification and conservative propagation. The evidence is promising but preliminary: run counts and an annotation-subset size are missing, action results were omitted, no significance tests were run, and evaluation is confined to one backbone and English cases.

## Problem

**Statement.** Long-term memory systems may revise a directly contradicted state while retaining downstream beliefs, plans, or pending actions whose evidential support has disappeared. The paper formulates dependency-aware state revision as identifying both the changed states and the dependent states that require revision.

**Why it matters.** A locally correct memory update can still permit an infeasible or unsafe downstream action. Correctness therefore requires tracking loss of support, not merely detecting direct contradiction or retrieving temporally current facts.

**Scope.** The paper addresses persistent natural-language agent memory, including evidence, factual or derived states, and pending actions. Its controlled evaluation covers direct revision, dependency recovery, and cascades of depth 0–3+; action-decision evaluation is explicitly absent from this version.

## Method

StateGraph represents memory as an evolving directed graph of evidence, states, and pending actions. New evidence first triggers direct revision. Six bounded structural, provenance, temporal, and linguistic sources propose dependency candidates; direction and relation type are assigned before a counterfactual verifier asks whether the dependent state survives removal of the premise. Accepted edges are graded Strict or Weak. Breadth-first propagation follows verified edges, checks scope and independent support, and maps failures to Stale, Needs-Recompute, Uncertain, or action replanning rather than invalidating every reachable node. A use-time gate then checks query premises and action preconditions.

### Key components

- Typed state graph with provenance, temporal and conditional scope, confidence, and status.
- Canonical matching and write-time adjudication for direct updates, conflicts, implicit invalidations, and scoped exceptions.
- Bounded candidate discovery from shared context, explicit derivation, execution provenance, action preconditions, temporal co-scoping, and linguistic cues.
- Bidirectional relation typing into depends-on, derived-from, or affects-action.
- Counterfactual edge verification with Strict, Weak, and None outcomes.
- Alternative-support assessment at revision time, excluding failed-path, circular, and self-support.
- Conservative breadth-first cascade propagation with lineage-aware cycle handling.
- Premise-aware query correction and action gating.

### Assumptions

- A model can reliably extract canonical states, scopes, provenance, and candidate relations from interaction history.
- Counterfactual judgments approximate genuine support dependence rather than merely reproducing correlated model beliefs.
- Independent support can be found within the bounded graph and verification context.
- Gold benchmark dependency paths and post-revision statuses adequately represent the intended semantics.
- The same-model pipeline is informative despite potentially correlated proposal, verification, and support-assessment errors.

## Main claims

- **The principal methodological contribution is recovery and counterfactual verification of latent support dependencies; propagation applies dependency-directed revision with explicit support and scope checks.**
  - Evidence: [b00056-18b339842e] “StateGraph’s main methodological contribution lies in recovering and verifying support dependencies from interaction histories.”; [b00056-18b339842e] “Its propagation stage applies established dependency-directed revision principles (Doyle, 1979) with explicit support and scope checks.”
- **Counterfactual verification is intended to distinguish support dependence from mere topical relatedness and to grade accepted dependencies by strength.**
  - Evidence: [b00088-7d01f4e190] “The counterfactual probe is designed to distinguish support dependence from topical relatedness by testing whether the dependent claim loses its warrant”; [b00088-7d01f4e190] “it also grades the dependency as Strict or Weak”
- **Conservative revision preserves independently supported states and treats weak dependencies as uncertainty rather than wholesale invalidation.**
  - Evidence: [b00054-c8ef13088e] “Weakly dependent states are flagged, while independently supported states remain valid.”; [b00094-6f58f55216] “Strict survives Current (re-grounded) Weak none Uncertain / Downweight”
- **The authors present the evidence as initial rather than conclusive and call for larger independent evaluations.**
  - Evidence: [b00010-aa75bd3754] “These results provide initial evidence that explicit dependency tracking can improve selective memory revision when upstream facts change”; [b00010-aa75bd3754] “establishing this beyond a small controlled benchmark requires larger independent evaluations.”

## Results

- **On StateChangeBench cascade revision, StateGraph obtained 82.7, 79.3, and 75.1 Impact-F1 at D1, D2, and D3+, with 79.5 overall. CUPMem obtained 75.8, 62.9, and 49.1, with 64.3 overall; the observed margin therefore widened on deeper strata.**
  - Context: All F1 is a case-count-weighted mean over the 40 depth 1–3+ cases, excluding depth 0. Each stratum contains only 10–15 cases, so this is an observed benchmark pattern, not an established general depth law.
  - Evidence: [b00201-3152e421d9] “Method D1 F1 ↑ D2 F1 ↑ D3+ F1 ↑ All F1 ↑ Over-Inv. ↓ Under-Inv. ↓ CVR ↓ Tokens / Latency ↓”; [b00201-3152e421d9] “CUPMem 75.8 62.9 49.1 64.3 10.6 29.6 35.1 90.6K / 340.6s”; [b00201-3152e421d9] “StateGraph 82.7 79.3 75.1 79.5 5.2 10.8 7.6 12.5K / 92.0s”; [b00128-c0df8455b6] “All F1 weights D1/D2/D3+ by 15/15/10 cases (40 total), excluding depth 0.”
- **StateGraph reported lower revision-error rates than CUPMem: over-invalidation 5.2 versus 10.6, under-invalidation 10.8 versus 29.6, and closure violation rate 7.6 versus 35.1.**
  - Context: These are percentages on StateChangeBench. CVR measures one-way conditional closure on shared reference dependency pairs; it does not independently validate whether the system's support judgments are correct.
  - Evidence: [b00127-14913786e7] “CUPMem 10.6 29.6 35.1”; [b00127-14913786e7] “StateGraph 5.2 10.8 7.6”; [b00128-c0df8455b6] “All values are percentages.”
- **Ablations materially degraded performance: removing counterfactual verification changed overall Impact-F1 from 79.5 to 65.9 and over-invalidation from 5.2 to 19.0; removing conservative revision produced 62.8 Impact-F1 and 25.0 over-invalidation; removing cascade propagation produced 45.6 Impact-F1 and 51.0 CVR.**
  - Context: These ablations use DeepSeek-v4-Flash on the full 50-case benchmark. They support the internal contribution of the components, but remain within the same constructed dataset and model pipeline.
  - Evidence: [b00133-ca2db9bf47] “Full StateGraph 79.5 5.2 7.6”; [b00133-ca2db9bf47] “w/o Counterfactual Verification 65.9 19.0 23.0”; [b00133-ca2db9bf47] “w/o Conservative Revision 62.8 25.0 28.0”; [b00133-ca2db9bf47] “w/o Cascade Propagation 45.6 7.0 51.0”
- **Dependency recovery remained imperfect: candidate recall was 62.5%, type recall 47.0%, verification F1 55.5%, and final edge F1 61.7%. This indicates substantial edge-level errors even though downstream Impact-F1 was higher.**
  - Context: The edge metrics use gold dependency edges across all 50 cases, whereas Impact-F1 scores propagated invalidations in the 40 nonzero-depth cases; the paper cautions that they are not interchangeable.
  - Evidence: [b00121-d44a90f913] “candidate recall, typing recall, verification F1 and final edge F1 are 62.5%, 47.0%, 55.5% and 61.7%, respectively”; [b00121-d44a90f913] “The two are linked but not interchangeable”
- **On six public memory benchmarks, StateGraph was comparable to or above the evaluated baselines on five, but scored 36.6% on MemoryAgentBench versus A-MEM's 43.1%; no significance tests were performed.**
  - Context: This supplementary evaluation used State Answer Accuracy and was designed to check for coincident degradation on standard memory tasks, not to evaluate dependency cascades directly.
  - Evidence: [b00130-7e27718522] “On MemoryAgentBench it scores 36.6%, below A-MEM’s 43.1% and above CUPMem’s 28.1%.”; [b00130-7e27718522] “Its point estimates are comparable to or higher than those of the evaluated baselines on five of the six benchmarks.”; [b00130-7e27718522] “We did not run significance tests, so these results do not establish the absence of degradation.”

## Experimental evaluation

### Datasets

- StateChangeBench: 50 author-constructed English cases with depths 0–3+, dependency structure, hard negatives, preservation conditions, and action consequences. It includes 17 hard negatives and 36 action-consequence cases.
  - Evidence: [b00106-7128719fdd] “StateChangeBench has 50 cases: 10/15/15/10 at depth 0/1/2/3+”; [b00106-7128719fdd] “including 17 hard negatives (34%) and 36 action-consequence cases (72%).”
- Public supplementary benchmarks: LongMemEval, LME-V2, MemoryAgentBench, Memora, STALE, and LoCoMo.
  - Evidence: [b00204-414aaa8a78] “Method LongMemEval ↑ LME-V2 ↑ MemoryAgentBench ↑ Memora ↑ STALE ↑ LoCoMo ↑”

### Baselines

- Vector RAG, time-decay RAG, summary memory, Mem0, Zep/Graphiti, A-MEM, a CUPMem reimplementation, and Full Context.
  - Evidence: [b00113-91bc330223] “Baselines are vector RAG (Lewis et al., 2020), time-decay RAG, summary memory, Mem0”; [b00113-91bc330223] “Zep/Graphiti (Rasmussen et al., 2025), A-MEM (Xu et al., 2025), CUPMem (Chao et al., 2026) and Full Context.”
- Ported-mechanism variants Mem0 + Cascade and CUPMem + Cascade retain the host systems' extraction and retrieval while adding cascade revision.
  - Evidence: [b00115-18fcbbadeb] “Mem0 and CUPMem augmented with cascade revision isolate the mechanism’s contribution while retaining their extraction and retrieval.”
- LLM-only Revision is used in the ablations as a graph-free full-history comparison.
  - Evidence: [b00140-0bb90181d7] “LLM-only revision uses full history without a persistent graph”

### Metrics

- Direct update accuracy, stale detection, and STALE State Resolution evaluate direct revision.
  - Evidence: [b00119-83cf097808] “direct update accuracy and stale detection are 84.9%/86.5% versus 82.7%/80.3%”; [b00119-83cf097808] “STALE State Resolution is 75.4% versus 72.1%”
- Candidate recall, type recall, verification F1, and edge F1 separately evaluate dependency discovery, typing, verification, and final edge recovery.
  - Evidence: [b00121-d44a90f913] “These measure discovery, typing and verification separately from cascade revision.”
- Impact-F1 evaluates downstream invalidation targets while excluding directly revised roots; over-invalidation, under-invalidation, and CVR diagnose selective-revision errors.
  - Evidence: [b00222-791364626f] “Impact-F1 evaluates downstream state invalidation against explicit gold propagated-invalidation targets, excluding directly revised roots.”; [b00227-7ed248df5e] “Over-invalidation is the proportion of gold-preserved states incorrectly invalidated.”; [b00227-7ed248df5e] “Under-invalidation is the proportion of gold downstream invalidation targets that remain uninvalidated.”
- State Answer Accuracy evaluates the six public long-term-memory benchmarks; total tokens and latency per case measure computational cost.
  - Evidence: [b00205-386f1fc073] “State Answer Accuracy (%) across six public long-term memory benchmarks.”; [b00211-67f9cce583] “lower is better for error rates and computational cost.”

### Ablations

- Remove counterfactual verification, alternative-support assessment, conservative revision, or cascade propagation one at a time; compare against full StateGraph and LLM-only revision.
  - Evidence: [b00132-e86696360a] “We remove one mechanism at a time using DeepSeek-v4-Flash on all 50 StateChangeBench cases and depths”; [b00133-ca2db9bf47] “w/o Counterfactual Verification 65.9 19.0 23.0 w/o Alternative Support 68.2 21.0 19.0”

### Negative results

- StateGraph underperformed A-MEM on MemoryAgentBench.
  - Evidence: [b00130-7e27718522] “On MemoryAgentBench it scores 36.6%, below A-MEM’s 43.1%”
- Action-decision results were not reported in this version.
  - Evidence: [b00110-d2bd2dcc16] “Action-decision results are not reported in this version (see Limitations).”
- Dependency recovery scores show substantial misses and classification errors.
  - Evidence: [b00121-d44a90f913] “candidate recall, typing recall, verification F1 and final edge F1 are 62.5%, 47.0%, 55.5% and 61.7%, respectively”


## Limitations

- The primary benchmark is small, author-constructed, and English-only, with only 10–15 cases per depth stratum; depth-wise differences are therefore preliminary.
  - Evidence: [b00149-e33e6306ef] “StateChangeBench isolates cascade reasoning through author-constructed English cases”; [b00149-e33e6306ef] “With 50 cases and 10–15 cases per depth stratum, and without significance tests, the depth-wise differences should be read as initial evidence.”
- The number of repeated runs and the size of the double-annotated subset were not retained, preventing assessment of sampling variability and annotation-reliability coverage.
  - Evidence: [b00150-69d0a344df] “They do not preserve the number of evaluation runs per configuration or the size of the double-annotated subset”
- Action-decision evaluation and the premise-gate ablation were omitted because their aggregation could not be reconstructed.
  - Evidence: [b00150-69d0a344df] “this version omits the action-decision evaluation and the premise-gate ablation: their aggregation could not be reconstructed from the remaining records.”
- All reported experiments use one model backbone, and the results do not establish generalization to other backbones, languages, multimodal inputs, or multi-agent deployments.
  - Evidence: [b00117-3a3a7b0d57] “The reported experiments use DeepSeek-v4-Flash.”; [b00150-69d0a344df] “These results do not establish performance across other backbones, languages, multimodal inputs or multi-agent deployments.”
- Relation typing, verification, and support assessment use the same LLM, allowing correlated errors; CVR is not an independent check of those judgments.
  - Evidence: [b00151-6502816e62] “Relation typing, counterfactual verification and alternative-support assessment use the same LLM, so their errors can be correlated.”; [b00151-6502816e62] “CVR checks closure using the system’s support judgments and is not an independent validation of those judgments”
- No significance tests were run for the public-benchmark comparisons.
  - Evidence: [b00130-7e27718522] “We did not run significance tests, so these results do not establish the absence of degradation.”

## Reproducibility

**Status:** partial

The paper provides unusually detailed pipeline settings, prompts, metric definitions, filenames, and one data hash, which supports conceptual reimplementation. Exact numerical reproduction remains blocked by missing run counts, incomplete retained records, and no supplied evidence of accessible code or data artifacts. The action-facing portions of the claimed system are also not experimentally reproducible from the reported results because their evaluation was omitted.

**Available artifacts**

- Prompt-template sections for state extraction, direct revision, candidate discovery, relation typing, verification, alternative support, premise checking, and answer generation are included in the supplied document.
- Named implementation source files and a benchmark annotation SHA-256 are reported.
- Model, thinking setting, output ceilings, retry settings, candidate limits, retrieval limits, metric formulas, and depth aggregation are described.

**Missing pieces**

- Number of evaluation runs per configuration.
- Size of the double-annotated subset.
- Reported action-decision evaluation and premise-gate ablation.
- Evidence in the supplied blocks of a public code repository, downloadable benchmark artifact, environment lockfile, model checkpoint/version pin, random seeds, or executable reproduction commands.

## AIDB assessment

- Novelty: The useful novelty is the operational combination of latent dependency recovery, counterfactual edge verification, revision-time alternative-support checks, and selective cascade propagation for persistent agent memory. The propagation principle itself is acknowledged as established; the original emphasis is discovering and verifying support dependencies from interaction histories.
- Usefulness: High potential for agents that maintain plans, bookings, permissions, or user preferences over time. The benchmark and diagnostics expose a consequential failure mode that ordinary recall metrics miss. Adoption should wait for independent, larger-scale, action-level validation and cross-model replication.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled comparisons and component ablations are internally coherent and practically relevant, but the decisive evidence comes from a small author-constructed benchmark. Missing run counts, incomplete annotation records, omitted action results, lack of significance tests, and same-model correlated judgments prevent an adopt recommendation.

## Uncertainties

- **It is unknown whether the depth advantage generalizes beyond StateChangeBench.** — The strongest headline advantage appears on deeper cascades, but those strata are small and the proposed explanation was not separately tested.
  - Evidence: [b00145-610d4098cb] “the following explanation is consistent with the ablations but is not separately tested.”; [b00126-e835898e18] “we report this as an observed pattern on StateChangeBench rather than a general depth trend.”
- **The statistical stability of all pooled results cannot be reconstructed.** — Unknown run counts prevent confidence intervals, variance estimates, and correct interpretation of pooled counts.
  - Evidence: [b00117-3a3a7b0d57] “the number of runs per configuration was not preserved in our retained records.”
- **Annotation agreement coverage is unknown, while dependency-type agreement is weaker than status and depth agreement.** — Dependency labels are central to both edge recovery and cascade evaluation; an unrecorded subset size prevents judging the precision of agreement estimates.
  - Evidence: [b00108-db2945b892] “Agreement on a double-annotated subset, whose size was not recorded”; [b00108-db2945b892] “Cohen’s κ values of 0.7915, 1.0000 and 0.5583, respectively.”
- **The system may share blind spots across candidate typing, verification, and alternative-support assessment.** — Correlated errors can make the graph appear internally consistent while still encoding an incorrect dependency structure.
  - Evidence: [b00147-055f47be24] “the current pipeline provides no independent guarantee of detecting correlated errors across proposal, verification and support assessment.”

## Open questions

- Can independently trained or rule-based verifiers reduce correlated dependency errors without unacceptable recall or cost loss?
- How does StateGraph perform on independently authored, naturally occurring interaction histories with longer horizons and noisier provenance?
- Do improved state-revision metrics translate into safer and more accurate action decisions, especially under irreversible or high-impact actions?
- How sensitive are results to model backbone, language, candidate-pool limits, and answer-context limits?
- Can cycles and mutually supporting beliefs be validated without either preserving unsupported loops or over-invalidating legitimate support?
- What are the variance and statistical significance of the reported gains when run counts are fixed and fully logged?

## Proposed AIDB experiments

- **Hypothesis:** An independent verifier reduces correlated edge errors and over-invalidation while preserving cascade recall relative to the same-model verifier.
  - Baseline: Full StateGraph with DeepSeek-v4-Flash used for relation typing, counterfactual verification, and alternative-support assessment.
  - Primary metric: Impact-F1 on a preregistered independently authored cascade test set, accompanied by over-invalidation and final edge F1.
  - Stop condition: Reject the hypothesis if the independent verifier fails to improve Impact-F1 or if over-invalidation increases; otherwise require a confidence interval excluding zero for the Impact-F1 difference.
- **Hypothesis:** StateGraph's advantage over CUPMem increases with true cascade depth on independently authored natural interaction histories.
  - Baseline: The shared-framework CUPMem reimplementation and CUPMem + Cascade under matched model, context, and compute budgets.
  - Primary metric: Depth-stratified Impact-F1 with a preregistered interaction between method and cascade depth.
  - Stop condition: Stop claiming a general depth effect if the interaction is not statistically distinguishable from zero or reverses on any replicated domain.
- **Hypothesis:** Premise and action gating reduces unsupported action execution without causing excessive unnecessary blocking.
  - Baseline: Full StateGraph with action gating disabled, plus CUPMem + Cascade under the same action generator.
  - Primary metric: Unsafe-proceed rate on gold action-consequence cases; report unnecessary-block rate as a co-primary safety tradeoff.
  - Stop condition: Reject deployment readiness if unsafe-proceed does not decrease or if unnecessary-block exceeds a preregistered operational threshold on any consequential-action stratum.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:59:25.373788+00:00`
- Document SHA-256: `b20aee9f8dcc58cc1249271d5b17669da705a4c11339a7ca440dc14a1acbd9f0`
- Metadata SHA-256: `2dc756c495251bf6211c027c6d6a0ebd6f344803774032641f0b9d5150a5938b`
- Blocks: 283
- Deterministic repair attempts: 1
