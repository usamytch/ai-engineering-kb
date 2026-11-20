# When Is a Memory Safe Enough to Act On? Action-Conditioned Verification for Long-Lived Agents

## Executive summary

The paper reframes stale-memory handling as a decision about a proposed action rather than an intrinsic property of a memory. AMV-Guard extracts action premises, calibrates error beliefs, applies asymmetric loss screens, and adaptively selects verification through bounded value of information. ToolSandbox provides a strong controlled result: lower verification cost than an information-matched static policy with unchanged measured gate safety and higher coverage. However, AppWorld transfers only the gate core and shows small losses in recall, coverage, and task success; out-of-distribution extraction retains nonzero gate harm. Evidence is extensive and unusually explicit about metrics and failure ownership, but remains simulator-bound and depends on approximate premise, observation, and loss models.

## Problem

**Statement.** For a proposed consequential action, decide which memory-supported premises to verify, when to execute, and when to abstain, while trading off execution loss, refusal cost, and verification cost. The central distinction is between memories that are merely relevant, those supporting the action, and those whose error materially changes action loss.

**Why it matters.** Persistent agents may turn stale memories directly into irreversible external actions. Memory quality alone cannot determine verification demand because identical memory evidence can rationally support proceeding, checking, or refusing when action consequences differ.

**Scope.** The formulation covers candidate-local commit decisions with verification operations of differing cost, reliability, availability, and premise coverage. The empirical scope is simulated tool use in ToolSandbox and a limited gate-core transfer to AppWorld; replanning occurs outside the terminal VOI decision.

## Method

AMV-Guard is inserted between planner and executor. It derives candidate premises from the action, tool contract, plan prefix, and retrieved memory graph; predicts and calibrates claim-error probabilities; converts them to action-precondition risks; combines those risks with an action-dependent loss; then repeatedly chooses the highest positive one-step VOI verification, optionally using depth-two lookahead when no one-step query is valuable. It proceeds only when execution passes expected-loss and harm-probability screens, abstains when execution is inadmissible and no useful check remains, and requests replanning when evidence invalidates a required premise.

### Key components

- Premise extraction combines independent LLM proposals with public tool-contract rules, grounding proposed premises to memory identifiers, verifiers, or public targets and filtering recurring irrelevant tool–target pairs.
- A logistic error model uses recency, source, consistency, graph, dependency, action, and model signals; Platt, beta, and bounded-isotonic calibration are selected on held-out families.
- The stopping rule compares proceeding and abstaining under asymmetric loss, expected-loss and posterior-harm screens, and an explicit abstention penalty.
- Adaptive verification recomputes posterior beliefs and VOI after each observation; a depth-two fallback targets complementary checks missed by greedy one-step selection.
- An information-constrained exact dynamic program uses the deployable gate's predicted inputs rather than hidden truth and serves as a regret and agreement reference, not supervision.

### Assumptions

- Verifier costs, reliabilities, coverage, and observation likelihoods are available and sufficiently well specified for Bayesian updates.
- The loss function supplies meaningful action consequences and whose costs count; otherwise asymmetry must be manually specified.
- ToolSandbox verification observations are binary, and multi-premise observations and joint dependencies are represented through simplified shared observations or latent draws.
- The candidate is frozen for gate evaluation; invalidation returns control to an external replanning loop rather than making replanning a terminal VOI action.
- The exact-planner comparison is exact only inside the finite predicted-premise, verifier, budget, and observation model used by the experiment.

## Main claims

- **The paper claims that verification demand is action-conditioned: criticality depends on the action and loss, so a memory-only score cannot generally reproduce the optimal decision.**
  - Evidence: [b00028-aaa321e3fe] “Criticality is a property of (a,L), while every memory-side feature is a property of m alone.”; [b00035-1a2d3adf0f] “The regimes are traversed by varying θ with the memory held fixed: a score computed from m and GM alone is constant in θ while the optimal decision is not.”
- **The formal result states that, under its specified reliability and cost conditions, increasing consequence can move a fixed memory through proceeding, verification, and direct abstention regimes.**
  - Evidence: [b00032-9d2066f3a8] “there are thresholds θ1≤θ2 such that the optimal initial decision is Proceed for θ<θ1, Verify for θ1≤θ<θ2, and Abstain for θ≥θ2.”; [b00034-6539550184] “it is empty when c is large”; [b00035-1a2d3adf0f] “With an imperfect verifier there is a consequence level past which even a confirming observation cannot license execution”
- **The paper argues that expected loss reduction for an unchanged action is a degenerate verification objective; information has value here only if it can alter the terminal decision.**
  - Evidence: [b00049-f5f3370c42] “so VOI⁡(q)≡−λ​C​(q)≤0 for every q, strictly negative whenever λ​C​(q)>0.”; [b00050-5430f2b86d] “information has value only through the ability to change the terminal decision”
- **The deployed policy is explicitly a bounded receding-horizon approximation rather than a globally optimal planner.**
  - Evidence: [b00064-689167e0ef] “a bounded receding-horizon approximation to Equation (3), not a claim of globally optimal planning.”; [b00055-05c61f9c09] “This is a depth-two lookahead, not the full Bellman policy.”

## Results

- **On ToolSandbox, AMV-Guard versus AMV-Static reduced mean verification cost by 33.9%, retained 100% safe-proceed recall and 0% Gate harmful, increased Proceed coverage by 5.33 points, and increased task success by 1.56 points; raw end-to-end harm was 0.21 points higher. This is the strongest information-matched main comparison, but the measured zero gate harm excludes initial action or intent errors from the gate-evaluable denominator.**
  - Context: Full live Agent–Gate episodes over frozen ToolSandbox candidates and three observation seeds. The static comparator receives the same predicted dependencies, beliefs, costs, and reliabilities but does not reselect verifiers based on posterior observations.
  - Evidence: [b00090-ece4420248] “Relative to AMV-Static, it reduces cost by 33.9% while both methods retain 100% safe-proceed recall, 0% Unsafe Pass, and 0% Gate harmful.”; [b00090-ece4420248] “This saving accompanies 5.33 points more Proceed coverage and 1.56 points more task success, with raw harm 0.21 points higher.”; [b00086-b7bdfb6086] “these metrics exclude the 40 test instances with initial-candidate action or intent errors”
- **Cost savings generalized across the three tested backbones—33.9%, 42.3%, and 58.9%—with zero measured Gate harm for both policies, but coverage did not consistently improve: it rose by 5.33 points, was unchanged, and fell by 5.68 points. The evidence therefore supports cheaper verification more consistently than better downstream utility.**
  - Context: Each backbone used its own candidates, calibration, and thresholds, so this is replication across independently configured pipelines rather than evaluation on an identical candidate set.
  - Evidence: [b00091-ad8097b60c] “adaptive VOI reduces mean verification cost for all three backbones, by 33.9%, 42.3%, and 58.9%”; [b00091-ad8097b60c] “Both Static and adaptive policies have zero measured Gate harm for all three backbones.”; [b00091-ad8097b60c] “Coverage increases by 5.33 points for Qwen3.5-35B-A3B, is unchanged for Qwen3.5-27B, and decreases by 5.68 points for DeepSeek-V4.1-Flash.”
- **The controlled consequence intervention isolated loss conditioning: AMV-Guard verified 0%, 15.8%, and 62.8% across low-, medium-, and high-loss conditions, and its high-loss harmful-proceed rate was 0% versus 64.2% without loss conditioning. This directly supports the mechanism that action consequence should alter verification behavior.**
  - Context: The candidate action and memory evidence were held fixed while only total loss was rescaled, with 500 instances per level; it tests consequence weighting rather than distinct-action conditioning.
  - Evidence: [b00206-fe05d92079] “500 instances per consequence level”; [b00206-fe05d92079] “The candidate action and memory evidence are held fixed while only total loss is rescaled.”; [b00096-e093055141] “AMV verifies 0%, 15.8%, and 62.8% of low-, medium-, and high-loss cases; its high-loss harmful-proceed rate is 0%, versus 64.2% without loss conditioning.”
- **The AppWorld gate-core transfer was mixed: verification cost fell by 21.28%, but safe-proceed recall declined from 72.63% to 70.53%, task success from 30.50% to 28.00%, and coverage from 59.47% to 57.37%; Gate harmful changed from 8.42% to 7.89%. Broad bootstrap intervals and the compound-premise adaptation limit any claim of robust transfer.**
  - Context: This was not a full pipeline transfer: AppWorld used recalibration and mapped each commit to one compound premise and verifier, omitting premise extraction, multi-verifier selection, and the two-step fallback.
  - Evidence: [b00104-d3138ef02a] “AMV lowers verification cost by 21.28% relative to AMV-Static (2.090 vs. 2.655)”; [b00106-3b6cf91c35] “AMV-Static 72.63 8.42 2.655 30.50 10.50 59.47 AMV-Guard 70.53 7.89 2.090 28.00 10.00 57.37”; [b00082-efb390f03e] “it transfers the calibrated stopping/VOI core, not the premise extractor, multi-verifier selection, or two-step fallback.”; [b00228-be397298ba] “The broad intervals reflect the 100-task transfer set”
- **Multi-step verification helped under constructed complementarity but was not universally favorable: on the controlled subset it improved safe completion by 4.15 percentage points and reduced exact-planner regret from 0.0746 to 0.0431 while adding 0.257 mean verifier cost; the multi-step rate was only 6.8%.**
  - Context: The controlled subset deliberately added more premises, heterogeneous verifier properties, overlapping coverage, and cases needing multiple observations. It evaluated repeated one-step greedy reselection without the depth-two fallback.
  - Evidence: [b00100-33ec3ea2c5] “increases safe completion by 4.15 percentage points, and reduces regret to the exact planner from 0.0746 to 0.0431, at 0.257 additional mean verifier cost.”; [b00100-33ec3ea2c5] “Its 6.8% multi-step rate shows that the gain is concentrated in these controlled conditions rather than universal.”

## Experimental evaluation

### Datasets

- ToolSandbox: 3,520 frozen instances split into 2,240 training, 640 development, and 640 test instances. The main test repeats three observation seeds; gate metrics exclude initial-candidate action or intent errors where specified.
  - Evidence: [b00080-d8d6aaaf39] “ToolSandbox contains 3,520 frozen instances split into 2,240/640/640 train/development/test instances; the main test is repeated with three observation seeds.”; [b00086-b7bdfb6086] “leaving 600 per seed and 1,800 over three seeds.”
- AppWorld: 100 state-mutating tasks evaluated in clean and stale-memory conditions, producing 200 episodes; 190 are gate-evaluable. It is a gate-core transfer, not a full structured-pipeline migration.
  - Evidence: [b00080-d8d6aaaf39] “contains 100 state-mutating tasks under clean and stale-memory conditions (200 episodes).”; [b00105-11d54d1346] “100 tasks, 200 clean/stale episodes per method; 190 Gate-evaluable”
- Controlled studies include paired action-conditioning profiles, consequence-rescaling cases, a multi-step subset, calibration records, and four premise-extraction distribution-shift strata.
  - Evidence: [b00094-da6305a138] “A paired intervention (n=500 profiles) fixes the memory graph”; [b00101-a9f6e61830] “Controlled adaptive subset (n=2,000).”; [b00203-bdf0bf733b] “On the calibration test split (n=1,240 premise records)”; [b00211-4097bcefa0] “Extraction metrics use all 160 candidates per stratum”

### Baselines

- Always Proceed and Always Verify provide behavioral extremes.
  - Evidence: [b00194-643c40e3bd] “Always Proceed accepts every candidate without verification.”; [b00194-643c40e3bd] “Always Verify repeatedly calls the cheapest remaining verifier that is available, reliable (r>0.5), covers at least one candidate premise”
- EnvProbe-Simple or native EnvProbe and CTA represent adapted environment-probing and cost-aware acquisition approaches.
  - Evidence: [b00084-bc9b127e5b] “adapted environment-probing and cost-aware baselines”; [b00194-643c40e3bd] “EnvProbe-Simple is the ToolSandbox environment-probing adaptation; AppWorld uses the corresponding native-agent adaptation.”
- AMV-Static is the primary information-matched comparator; it shares predicted dependencies, calibrated beliefs, costs, and reliabilities but lacks posterior-dependent verifier reselection.
  - Evidence: [b00194-643c40e3bd] “AMV-Static receives the same predicted dependencies, calibrated beliefs, costs, and reliabilities as the main method”; [b00194-643c40e3bd] “but commits to its verifier selection without posterior-dependent reselection.”
- ExactPlanner-PredictedDep is a non-privileged exact-model reference for decision agreement and regret, not a deployable baseline or training signal.
  - Evidence: [b00076-d8a5ad585d] “This ExactPlanner-PredictedDep is a decision-agreement and regret reference; it does not supervise the main method.”

### Metrics

- Safe-proceed recall measures execution of ground-truth-safe, gate-evaluable original candidates during the initial gate episode; Unsafe Pass Rate is the harmful-candidate analogue.
  - Evidence: [b00086-b7bdfb6086] “Safe-proceed recall is the fraction of ground-truth-safe, Gate-evaluable original candidates executed during the initial Gate episode”; [b00086-b7bdfb6086] “the harmful-candidate analogue, Unsafe Pass Rate, is reported as a diagnostic.”
- Gate harmful uses harmful executions over all gate-evaluable instances, whereas raw harm includes planning and intent failures; these metrics attribute failure to different system components.
  - Evidence: [b00086-b7bdfb6086] “The primary Gate harmful metric uses the same harmful-execution numerator over all Gate-evaluable instances.”; [b00086-b7bdfb6086] “raw harm records any executed action whose observed loss exceeds the threshold, including planning or intent failures.”
- Proceed coverage includes gate-approved actions after replanning; task success is end-to-end; verification cost accumulates across all gate entries in an episode.
  - Evidence: [b00086-b7bdfb6086] “Proceed coverage is the fraction of Gate-evaluable instances in which any Gate-approved action executes, including after replanning.”; [b00086-b7bdfb6086] “Task success is end-to-end”; [b00086-b7bdfb6086] “Verification cost accumulates across all Gate entries in an episode.”
- Calibration is evaluated with ECE, Brier score, and NLL; controlled planning also reports objective, safe completion, multi-step rate, and regret to the exact planner.
  - Evidence: [b00098-9be7c6b974] “Calibration lowers ECE/Brier/NLL”; [b00101-a9f6e61830] “Multi-step: share using more than one verifier; objective: decision loss plus weighted verification cost.”

### Ablations

- Action-conditioned premise selection holds the memory graph and gate settings fixed while changing only the candidate action; high-risk actions verified and low-risk actions proceeded across all profiles.
  - Evidence: [b00094-da6305a138] “changes only the candidate”; [b00094-da6305a138] “The high-risk action verifies and the low-risk action proceeds in 100% of profiles”
- Consequence conditioning holds action and memory evidence fixed and rescales only total loss, comparing AMV-Guard with AMV-NoLoss, EnvProbe-Simple, Freshness-Only, and Uncertainty-Only.
  - Evidence: [b00206-fe05d92079] “This isolates consequence weighting, not distinct-action conditioning.”; [b00207-cfbadae2e7] “AMV-NoLoss Low 15.8 0.0 97.8 0.164”; [b00207-cfbadae2e7] “Freshness-Only Low 0.0 0.0 100.0 0.000”
- Calibration data-efficiency compares raw confidence with calibrated models fitted on increasing fractions of training data; calibration materially improves probability metrics and gate harm.
  - Evidence: [b00209-8659e13241] “Raw confidence 0.319 0.319 4.401 100.00 65.83 99.17 0.000”; [b00209-8659e13241] “100% 0.082 0.209 0.588 100.00 0.00 33.33 1.167”
- Premise-extraction distribution shift compares LLM-only, graph-only, combined, and counterfactually filtered union extractors across seen schemas, unseen tool families, unseen domain schemas, and unstructured language.
  - Evidence: [b00211-4097bcefa0] “Premise-extraction OOD ablation.”; [b00212-5ca4b980ff] “Unstructured language LLM-only 100.00 94.97 97.42 61.92 10.13 1.025”
- Two-step fallback is compared against the corresponding fixed development configuration, showing a large recall and coverage increase at substantial verification cost.
  - Evidence: [b00100-33ec3ea2c5] “raises safe-proceed recall from 17.0% to 100% and Proceed coverage from 5.31% to 31.25%”; [b00100-33ec3ea2c5] “mean verification cost rises from 0.059 to 1.213.”

### Negative results

- AppWorld transfer did not improve task success or safe-proceed recall and retained nonzero gate harm.
  - Evidence: [b00104-d3138ef02a] “does not improve task success (28.00% vs. 30.50%) or safe-proceed recall (70.53% vs. 72.63%).”; [b00104-d3138ef02a] “with 7.89% vs. 8.42% Gate harmful”
- Adaptive coverage decreased for one tested backbone, accompanied by less favorable downstream outcomes.
  - Evidence: [b00091-ad8097b60c] “decreases by 5.68 points for DeepSeek-V4.1-Flash.”; [b00091-ad8097b60c] “Table 11 also reports the less favourable downstream outcomes.”
- In the controlled adaptive subset, AMV-Adaptive had slightly higher harmful rate and verifier cost than AMV-Static despite improving objective and safe completion.
  - Evidence: [b00102-b7c4f5130b] “AMV-Static 1.10 3.750 0.00 77.35 0.4550 0.0746 AMV-Adaptive (one-step) 1.20 4.007 6.80 81.50 0.4236 0.0431”
- The deployed extractor produced nonzero gate harm under all three reported out-of-distribution strata, and dependency accuracy degraded sharply for unstructured language.
  - Evidence: [b00104-d3138ef02a] “Gate harmful 8.23%, 15.19%, and 10.13% on unseen tool families, unseen domain schemas, and unstructured language”; [b00104-d3138ef02a] “dependency accuracy falling to 61.92% on unstructured language”
- The paper does not report a runtime ablation of hypergraph versus flat dependency handling because the deployed engine cannot consume distinct hyperedge identifiers.
  - Evidence: [b00203-bdf0bf733b] “We do not report a hypergraph-versus-flat runtime ablation because the present risk engine does not consume distinct hyperedge IDs.”


## Limitations

- Premise extraction is partly model-driven and cannot recover a premise never proposed; missed critical premises therefore cap the safety of the entire pipeline.
  - Evidence: [b00119-045e65fb37] “cannot recover one never proposed, so extractor recall upper-bounds the pipeline”
- The planner's greedy and depth-two policy can miss longer complementary verification sequences and need not match the full exact planner.
  - Evidence: [b00119-045e65fb37] “it need not match the full exact planner on longer complementary sequences.”
- Multi-premise verifier observations and conjunction-only dependencies use approximations rather than exact joint inference; several distinct joint hyperedges cannot be represented in one candidate.
  - Evidence: [b00119-045e65fb37] “This is an approximation rather than an exact joint observation model.”; [b00119-045e65fb37] “It therefore cannot represent several distinct joint hyperedges in one candidate.”
- The loss model requires executable consequence signals or explicit policy specification, and manually supplied asymmetry can silently shift the proceed-versus-decline boundary.
  - Evidence: [b00120-ca8a6e8024] “where neither exists the asymmetry must be supplied by hand”; [b00122-7c9cd00b46] “a mis-specified asymmetry silently moves the boundary between proceeding and declining.”
- All empirical environments and users are simulated, and scored harms omit reputational damage, delayed effects, downstream human cost, linguistic diversity, accessibility needs, and cultural variation.
  - Evidence: [b00120-ca8a6e8024] “reputational damage, downstream human cost, and delayed effects are outside what the evaluators score”; [b00241-022f607c12] “the simulators do not capture the full distribution of language, accessibility needs, cultural conventions, or harms faced by marginalized populations.”
- The paper lacks per-perturbation-family and per-action-class breakdowns and does not measure scaling with premise count, verifier count, or dependency depth.
  - Evidence: [b00120-ca8a6e8024] “We also do not yet report per-perturbation-family and per-action-class breakdowns or scalability over premise count, verifier count, and dependency depth.”
- Exact-planner agreement is only model-internal and cannot certify premise completeness, calibration correctness, or observation-model correctness.
  - Evidence: [b00192-b73ad788a2] “It does not certify premise completeness, calibration correctness, or observation-model correctness.”

## Reproducibility

**Status:** partial

Reproducibility is better documented than usual: benchmark revisions, deterministic replay, frozen splits, model services, decoding, package versions, manifests, and repository locations are specified. The rating remains partial because several high-value artifacts are future-tense releases and substantial compute accounting is estimated. Deterministic replay validates repeatability within the recorded simulator and model caches, not correctness of premise extraction, calibration, or the observation model.

**Available artifacts**

- Anonymous repositories for the main experiments and two cross-backbone branches are stated as available.
- Snapshots, seeds, cached external-model outputs, frozen splits, configurations, audits, and fitted calibration artifacts are described.
- ToolSandbox and AppWorld revisions, principal software versions, decoding settings, and model identifiers are reported.
- The paper states that an environment lock file, prompts, caches, row-level files, traces, and oracle trees will accompany the final artifact.

**Missing pieces**

- Large row-level premise files, per-step decision traces, and oracle policy trees are promised for a future final artifact rather than confirmed present.
- The complete environment lock file, prompts, seeds, and input-hash-keyed caches are likewise described as forthcoming.
- Token usage is missing for part of the logged calls, and total requests, tokens, and wall-clock compute are partly reconstructed estimates.
- The supplied blocks do not report an independent reproduction or verification that the anonymous repositories execute end to end.

## AIDB assessment

- Novelty: Moderate to high at the systems-problem level. Classical VOI, Bayesian stopping, and abstention are explicitly not claimed as new; the contribution is their action-conditioned application to persistent-memory premises with heterogeneous verifiers, overlapping coverage, replanning, and asymmetric consequences.
- Usefulness: High for researchers designing safety gates for persistent tool-using agents. The paper supplies a clear formal decomposition, information-matched comparisons, metric definitions that separate gate-local from end-to-end failures, controlled interventions, and detailed reproducibility material. Production usefulness is currently limited by simulator scope and model-dependent premise and loss specification.
- Confidence: medium
- Recommended action: read
- Rationale: The ToolSandbox evidence convincingly supports a narrower conclusion: adaptive, stopping-based verification can remove unnecessary checks under the paper's modeled conditions while preserving measured gate safety. The consequence intervention also isolates the key mechanism. Confidence should not be elevated to adoption because the only cross-environment result transfers a reduced gate core and is mixed, distribution-shift extraction retains nonzero harm, and the observation, dependency, and loss models are acknowledged approximations.

## Uncertainties

- **Whether the apparent ToolSandbox safety survives realistic, incomplete premise enumeration and misspecified verifier likelihoods.** — The gate can only protect premises it represents, while the zero measured gate-harm result is obtained in a simulator with structured intervention labels and explicit verifier metadata.
  - Evidence: [b00192-b73ad788a2] “It does not guarantee that premise enumeration is complete”; [b00192-b73ad788a2] “or that the observation model is correctly specified.”
- **Whether AMV-Guard improves end-to-end utility outside the main ToolSandbox backbone and operating point.** — Verification cost improves consistently, but coverage and task success do not; deployment decisions require the complete safety–utility trade-off rather than cost alone.
  - Evidence: [b00091-ad8097b60c] “Coverage increases by 5.33 points for Qwen3.5-35B-A3B, is unchanged for Qwen3.5-27B, and decreases by 5.68 points for DeepSeek-V4.1-Flash.”; [b00104-d3138ef02a] “does not improve task success (28.00% vs. 30.50%)”
- **How sensitive conclusions are to loss weights that encode action consequence and abstention cost.** — Action conditioning operates through the loss model, so incorrect valuations may produce apparently principled but socially or operationally wrong decisions.
  - Evidence: [b00120-ca8a6e8024] “sensitivity analysis characterises but does not remove that dependence.”; [b00122-7c9cd00b46] “The loss function encodes whose costs count and how much.”
- **Whether longer planning horizons justify their computational and verification costs in naturally occurring workloads.** — The controlled subset concentrates complementarity by design, while the deployed fallback only looks two steps ahead and the measured multi-step usage is sparse.
  - Evidence: [b00100-33ec3ea2c5] “Its 6.8% multi-step rate shows that the gain is concentrated in these controlled conditions rather than universal.”; [b00180-8773db5d77] “The two-step fallback requires at most O⁡(m2​k2) such evaluations”

## Open questions

- Can a full structured-pipeline transfer—premise extraction, multiple heterogeneous verifiers, and fallback planning—retain safety and improve task success in an environment unlike ToolSandbox?
- How does gate performance degrade under systematically misspecified verifier reliability, correlated observation errors, or adversarially missing critical premises?
- What are the safety, coverage, and runtime curves as premise count, verifier count, verification horizon, and dependency depth increase?
- Can consequence and abstention costs be elicited, audited, and stress-tested without encoding unacceptable stakeholder biases?
- Do per-action-class and per-perturbation-family results reveal concentrated failure modes hidden by aggregate gate-harm metrics?
- Would exact joint dependency and observation modeling materially outperform the current shared-binary and shared-latent approximations?

## Proposed AIDB experiments

- **Hypothesis:** A full AMV-Guard pipeline transferred to a new executable environment will reduce verification cost relative to an information-matched static policy without materially worsening gate harm, safe-proceed recall, coverage, or task success.
  - Baseline: AMV-Static with identical extracted premises, calibrated beliefs, verifier interfaces, costs, reliabilities, budgets, action agent, and replanning loop; also report Always Proceed and Always Verify as boundary references.
  - Primary metric: Primary: paired difference in verification cost subject to prespecified non-inferiority margins for Gate harmful and safe-proceed recall. Secondary: task success, Proceed coverage, raw harm, and Unsafe Pass Rate with paired confidence intervals.
  - Stop condition: Reject the hypothesis if the upper confidence bound for Gate-harm increase or the lower confidence bound for safe-recall change crosses its prespecified non-inferiority margin, regardless of cost savings; otherwise require a positive lower confidence bound for cost reduction.
- **Hypothesis:** Exact joint modeling of multi-premise verifiers and conjunction-only dependencies will reduce harmful passes and decision regret compared with the current shared-observation and shared-latent approximation, especially when multiple distinct joint hyperedges occur in one candidate.
  - Baseline: The deployed AMV-Guard risk engine using one shared binary observation for multi-premise coverage and one shared latent draw for jointly tagged premises.
  - Primary metric: Gate harmful and regret to an exact planner defined over the true joint observation and dependency model, stratified by number of hyperedges and correlation strength; report verification cost and coverage as trade-offs.
  - Stop condition: Stop for futility if confidence intervals exclude a practically meaningful reduction in both Gate harmful and regret on the multi-hyperedge strata, or stop for harm if verification cost rises beyond a prespecified budget without safety improvement.
- **Hypothesis:** AMV-Guard's safety advantage remains robust under bounded calibration and verifier-model misspecification, but fails beyond identifiable error thresholds that can be detected by monitoring.
  - Baseline: AMV-Guard under correctly specified calibrated beliefs and verifier likelihoods, plus AMV-Static under the same perturbations.
  - Primary metric: Worst-stratum Gate harmful across a factorial sweep of calibration shift, reliability bias, correlated verifier errors, and missing-premise rates; secondary metrics are safe-proceed recall, coverage, cost, and calibration error.
  - Stop condition: Declare the method non-robust when the lower confidence bound of worst-stratum Gate harmful exceeds a prespecified safety ceiling, or when no monitored calibration or residual statistic predicts entry into that failure region with acceptable sensitivity.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T09:01:24.995687+00:00`
- Document SHA-256: `5e9e6c167269d5b0cff1789146327dea2506f6b63a89965b4839f892320a3598`
- Metadata SHA-256: `e4ee10c4f28df3c19b926f8ac24c5b253fa149ab156e6762b716e56c989584ad`
- Blocks: 249
- Deterministic repair attempts: 0
