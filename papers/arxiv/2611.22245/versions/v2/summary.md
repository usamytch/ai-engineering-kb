# Multi-Agent Memory Inconsistency: Where Factual Conflicts Disappear in LLM Agents

## Executive summary

The paper introduces a controlled benchmark and evidence-flow profiler for locating factual-conflict loss in delegated LLM document review. Mandatory delegation retrieves more complete conflicting pairs than single-agent execution but detects fewer conflicts; most measured loss occurs before evidence reaches the lead. Matched comparisons associate success with one worker holding both claims and failure with claims split across workers. This is useful diagnostic evidence, but causal attribution remains limited: the mandatory condition changes delegation, partitioning, and lead access together; cohorts are selected by observed behavior; runs are few; grading has known errors; and artifact availability is not stated.

## Problem

**Statement.** In lead–worker LLM systems, relevant evidence is distributed across private contexts, messages, and shared artifacts. The study asks whether both sides of a factual conflict remain available to the agent responsible for the joint conclusion, and where either side disappears between source retrieval and the final report.

**Why it matters.** End-to-end accuracy can conceal opposing effects: delegation may broaden retrieval while communication and synthesis discard the combinations needed for verification. Locating the loss stage is therefore necessary before deciding whether to improve retrieval, worker reporting, lead synthesis, or memory interfaces.

**Scope.** The empirical scope is document due diligence using controlled numerical conflicts inserted into Harvey LAB tasks. It compares no delegation, discretionary delegation, and mandatory partitioned delegation across three model configurations. The conclusions do not directly establish behavior for non-numerical conflicts, other domains, other agent architectures, or fixed evidence assignments.

## Method

The authors preserve each Harvey LAB task prompt and document collection, replace selected occurrences of recurring numerical values to create known contradictions, and grade a red-flags report against hidden conflict specifications. A proxy-based profiler correlates model traffic, SDK events, traces, tool outputs, messages, and report artifacts. For each planted pair, it records whether both endpoints appear at Source Reads, Worker Reports, Lead Evidence, and Final Report, then separately evaluates semantic conflict detection with an LLM judge. Evidence provenance is classified as Same when one contributor supplies both claims and Split when only the union of contributors contains both. Policies receive common generation allowances and are compared both in pooled aggregates and in matched case cohorts.

### Key components

- A benchmark of controlled numerical contradictions embedded in otherwise retained document-review tasks.
- Three policies: None uses one source-reading report writer; Optional permits lead reads and discretionary, potentially overlapping delegation; Required restricts source inspection to workers assigned document partitions while the lead coordinates and synthesizes.
- A stage-wise evidence-flow profiler that detects conflict endpoints in source-tool returns, worker outputs, evidence received by the lead, and the graded report.
- Pair Recall, which gives credit only when both endpoints of a planted conflict are present at a stage, separated from semantic Judge Pass.
- Same/Split provenance analysis and matched comparisons using identical model, run, task, and conflict instances for Required and None.
- Generation-cost accounting across lead and worker calls, including revision and compaction, but excluding judging.

### Assumptions

- Fact-specific anchors and verified equivalent representations identify endpoint presence accurately enough for stage comparisons.
- The selected graded checkpoint and cumulative evidence prefix faithfully represent what was available for producing the evaluated report.
- The LLM judge reliably distinguishes explicit detection of the planted conflict from nearby quantitative comparisons.
- Common dollar allowances make generation spending sufficiently comparable despite different models, SDKs, continuation behavior, and slight budget overshoot.
- Pooling observations across models and runs is informative even though conflicts repeat within tasks and model behavior differs substantially.
- Same/Split provenance is a meaningful proxy for distributed-memory difficulty, although those cohorts arise from agents’ own retrieval and reporting choices.

## Main claims

- **The paper claims a stage-wise benchmark and profiler that separates complete-pair evidence coverage from semantic conflict detection under multiple delegation policies.**
  - Evidence: [b00011-60c0d99012] “We construct 73 controlled numerical conflicts across 11 Harvey LAB document-review tasks”; [b00011-60c0d99012] “Pair Recall measures evidence coverage separately from semantic conflict detection under the three delegation policies.”
- **The authors identify worker reporting, before evidence reaches the lead, as the largest measured preservation failure under mandatory delegation.**
  - Evidence: [b00009-500a05bc3d] “Pair Recall falls from 68.7% at Source Reads to 24.4% at Lead Evidence.”; [b00068-47a59bf689] “Worker Reports and Lead Evidence have identical labels, locating the observed handoff gap between source inspection and worker reporting.”
- **The paper argues that evidence distribution matters: mandatory delegation performs better when one worker retrieves both claims but worse when the pair is distributed across workers.**
  - Evidence: [b00015-927348d760] “Required detects more conflicts than None on identical cases when one worker reads both claims (34.2% versus 22.5%)”; [b00015-927348d760] “but fewer when the claims are split across workers (10.0% versus 18.9%).”

## Results

- **Mandatory delegation raised pooled Source Reads Pair Recall from 50.2% to 68.7%, while Judge Pass declined from 16.2% to 13.2%. Optional achieved 62.8% source-pair recall and the best pooled detection rate, 24.2%.**
  - Context: This is the strongest end-to-end controlled comparison under comparable generation allowances. It shows that broader collective retrieval did not translate into better conflict detection. However, Optional is not a clean architectural ablation because models chose different delegation behavior, while Required simultaneously imposed delegation, source partitioning, and restricted lead access.
  - Evidence: [b00065-579afe43bb] “Required increases Source Reads Pair Recall to 68.7%, compared with 50.2% under None, but Judge Pass falls from 16.2% to 13.2%”; [b00065-579afe43bb] “Optional reaches 62.8% Source Pair Recall and 24.2% detection.”
- **Among 438 mandatory-delegation observations, source reads contained both claims in 301 cases (68.7%), but Worker Reports and Lead Evidence retained complete pairs in only 107 cases (24.4%). Of the 301 retrieved pairs, 106 appeared in Worker Reports (35.2%).**
  - Context: The equality of Worker Reports and Lead Evidence localizes the measured loss to selection or omission in worker reporting rather than an additional transport loss after messages were sent. Because measurement is cumulative, it does not establish precisely when claims first became jointly available or why workers omitted them.
  - Evidence: [b00068-47a59bf689] “Across all 438 Required observations, Source Reads contain both claims in 301 cases (68.7%), compared with 107 (24.4%) at Worker Reports and Lead Evidence.”; [b00068-47a59bf689] “Of the 301 pairs present at Source Reads, 106 also appear in Worker Reports (35.2%).”
- **In matched Source Reads cohorts, Required passed 38/111 cases (34.2%) when one worker read both claims, versus 25/111 (22.5%) for None; when claims were split, Required passed 19/190 (10.0%), versus 36/190 (18.9%) for None.**
  - Context: Matching holds model, run, task, and conflict instance fixed, making this more informative than an unmatched aggregate. It remains observational conditioning: cohort membership is defined by Required’s own retrieval pattern, so the result supports an association between distribution and detection rather than isolating distribution causally.
  - Evidence: [b00071-aa4b518ce1] “Required achieves Judge Pass on 38/111 observations (34.2%) in the Source Reads Same group, compared with 25/111 (22.5%) under None.”; [b00071-aa4b518ce1] “In the Split group, it detects 19/190 (10.0%), compared with 36/190 (18.9%).”
- **Conditioning on Lead Evidence preserved the same direction: Required versus None was 72.2% versus 33.3% for Same evidence and 17.1% versus 28.6% for Split evidence.**
  - Context: Even after complete pairs reached the lead, provenance correlated strongly with whether the conflict was flagged. This suggests that placing both claims in one contributor’s report may aid synthesis, but the design does not distinguish provenance effects from differences in wording, salience, retrieval difficulty, or worker behavior.
  - Evidence: [b00071-aa4b518ce1] “Conditioning on Lead Evidence gives the same direction: 72.2% versus 33.3% for Same, and 17.1% versus 28.6% for Split.”

## Experimental evaluation

### Datasets

- Eleven Harvey LAB due-diligence document-review tasks, retaining their original instructions and document collections while adding controlled factual edits and conflict-specific grading criteria.
  - Evidence: [b00036-614e354a6a] “We build on 11 Harvey LAB due-diligence tasks in which agents review document directories and write red-flags reports”; [b00036-614e354a6a] “Each task retains its original instructions and document collection, with controlled factual edits and conflict-specific grading criteria.”
- Seventy-three planted numerical conflicts, with five to seven conflicts per task; each specification records values, locations, permitted equivalents, edits, and grading criteria.
  - Evidence: [b00037-6389d724d9] “Five to seven conflicts appear per task, totaling 73”; [b00037-6389d724d9] “Each conflict specification records the values, source locations, permitted equivalent representations, edits, and grading criteria.”

### Baselines

- None: one agent inspects documents and writes the report; this is the principal single-agent baseline.
  - Evidence: [b00040-7990f5ebdb] “Under None, one agent inspects documents and writes the report.”
- Optional: the lead can read sources, create workers, and assign overlapping reviews; it measures discretionary delegation rather than a fixed multi-agent treatment.
  - Evidence: [b00040-7990f5ebdb] “Under Optional, the lead may inspect sources itself, create workers, and assign overlapping reviews.”; [b00041-920f3d7ccc] “Optional measures whether models choose to delegate”
- Required: workers inspect partitioned sources while the lead synthesizes without direct source access; this is the mandatory-delegation treatment.
  - Evidence: [b00040-7990f5ebdb] “Under Required, workers inspect assigned document partitions while the lead coordinates and synthesizes their findings without reading source documents.”

### Metrics

- Pair Recall: the proportion of conflict observations for which both planted endpoints are present at a measurement stage; unrelated evidence does not affect credit.
  - Evidence: [b00051-c66144d6d4] “A conflict earns pair credit when both endpoints are present, regardless of unrelated evidence.”
- Same and Split provenance: Same means one individual supplies both endpoints; Split means only the union of contributors supplies both, with Same taking precedence.
  - Evidence: [b00052-13d4f9b7ef] “we separate Same, where one individual supplies both endpoints, from Split, where only the contributors’ union contains both.”
- Judge Pass: an LLM judge requires both identification of the specified discrepancy and accurate treatment of its quantitative comparison.
  - Evidence: [b00053-cc50ff8d4d] “Our rubric has two criteria per conflict: identifying the discrepancy and accurately treating its quantitative comparison.”; [b00053-cc50ff8d4d] “Judge Pass requires both criteria, including an explicit flag for the specified conflict”
- Cost: mean generation spending divided by the common per-round allowance, including lead and worker generation but excluding judging.
  - Evidence: [b00048-34245c7b8f] “Cost is mean generation spending divided by the common $59.60 per-round allowance, excluding judging.”

### Ablations

- Delegation-policy comparison across None, Optional, and Required changes how source inspection and coordination are allocated. It is policy comparison rather than a single-factor ablation because Required bundles several constraints.
  - Evidence: [b00041-920f3d7ccc] “this policy combines mandatory delegation, partitioned source assignments, and restricted lead access.”
- Matched Same/Split analysis conditions on Required’s observed source or lead evidence and compares None on identical model, run, task, and conflict instances.
  - Evidence: [b00070-fb9b92c08e] “Same and Split cohorts are defined by Required’s observed evidence distribution”; [b00070-fb9b92c08e] “with None evaluated on the identical model, run, task, and conflict instances.”

### Negative results

- More complete source retrieval under mandatory delegation did not improve pooled conflict detection; detection decreased relative to the single-agent baseline.
  - Evidence: [b00065-579afe43bb] “Collecting more evidence at the source stage therefore does not guarantee higher conflict detection in the final report.”
- Mandatory delegation produced a larger Source Reads-to-Final Report Pair Recall decline than no delegation for every tested model.
  - Evidence: [b00067-96fe5459d2] “Required has a larger total decline than None for every model, with most of its decline occurring before the lead.”
- Optional delegation did not reliably yield useful worker evidence for the two GPT configurations: worker-report pair recall remained extremely low despite some executions creating workers.
  - Evidence: [b00062-0fc0126d83] “both GPT models’ Worker Reports achieve Pair Recall of only 0.7% (1/146) under Optional”


## Limitations

- External validity is narrow: the benchmark covers one document-review family, planted numerical contradictions, and few repeated runs. Generalization to natural conflicts, non-numerical reasoning, other domains, and other agent topologies is untested.
  - Evidence: [b00077-7a43091556] “Our evidence comes from 11 Harvey LAB tasks with planted numerical conflicts and two runs per model.”; [b00077-7a43091556] “Broader document domains, non-numerical conflicts, and more repetitions would test how widely the observed patterns hold”
- The profiler measures cumulative presence, not the time at which both claims first become jointly available. It therefore cannot fully resolve temporal availability or distinguish late reconstruction from preserved evidence.
  - Evidence: [b00077-7a43091556] “The profiler measures cumulative evidence presence; tracing when both claims become jointly available would extend this analysis.”
- Known grading errors weaken outcome validity: manual inspection found saved passes that rewarded neighboring comparisons rather than the planted target, and broader human validation was not reported.
  - Evidence: [b00077-7a43091556] “Manual inspection identified three saved Judge Pass labels that credited neighboring comparisons rather than the planted conflict”; [b00077-7a43091556] “broader human review could refine endpoint matching and semantic grading.”
- Required is a bundled intervention: mandatory delegation, partitioned assignments, and blocked lead source access change simultaneously. Differences cannot be uniquely attributed to any one component.
  - Evidence: [b00078-1795531387] “Required combines mandatory delegation, partitioned source assignments, and restricted lead access”
- Matched Same/Split cohorts remain behaviorally selected rather than randomized. Retrieval and reporting choices may correlate with intrinsic conflict difficulty, salience, or document structure.
  - Evidence: [b00078-1795531387] “The matched groups also reflect agents’ observed retrieval and reporting choices.”
- Model families use different SDKs, introducing a possible implementation confound alongside model differences.
  - Evidence: [b00078-1795531387] “while model families use different SDKs.”
- Budgeting and checkpoint selection were not fully prospective; spending-based calibration and retrospective checkpoint selection create researcher-decision and comparability risks.
  - Evidence: [b00078-1795531387] “Budgets were calibrated from observed spending, and GPT-5.6 Required checkpoints were selected retrospectively”; [b00078-1795531387] “future evaluations should fix budgets and checkpoint rules in advance.”

## Reproducibility

**Status:** partial

The paper gives a comparatively clear conceptual protocol and enough aggregate counts to understand the analysis, but the supplied document does not establish artifact availability or provide the operational detail needed for an independent rerun. Reproduction would also require access to the edited Harvey LAB corpus and hidden conflict specifications. The retrospective checkpoint choice and known judge-label errors further limit exact replication of the reported outcomes.

**Available artifacts**

- A described benchmark construction procedure based on controlled edits to Harvey LAB tasks.
- A described profiler architecture correlating captured model traffic, SDK events, traces, tool outputs, messages, and report artifacts.
- Explicit definitions of delegation policies, evidence-flow stages, Pair Recall, Same/Split provenance, Judge Pass, budget accounting, model configurations, run counts, and observation counts.

**Missing pieces**

- No supplied block states that benchmark files, conflict specifications, profiler source code, execution traces, prompts, grading rubrics, or generated reports are publicly released.
- No supplied block provides exact model snapshots, decoding parameters, random seeds, worker partition algorithm, continuation thresholds, or complete controller configuration.
- No supplied block reports uncertainty intervals, task-clustered statistical tests, inter-rater validation, or a corrected analysis after the known grading errors.
- The exact retrospective checkpoint-selection rule and per-condition spending records are not supplied.

## AIDB assessment

- Novelty: The strongest novelty is not merely another multi-agent accuracy comparison, but a stage-wise decomposition of known conflicting claim pairs across retrieval, worker reporting, lead evidence, and final output, coupled with Same/Split provenance. The benchmark operationalizes multi-agent memory consistency as observable evidence preservation rather than treating final correctness as the only signal.
- Usefulness: High diagnostic value for designers of delegated research, review, and verification agents. It identifies worker-to-lead reporting and split-provenance synthesis as intervention points, and its measurements can guide structured handoff protocols. Adoption should be methodological rather than numerical: the reported rates are specific to bundled policies, planted numerical conflicts, and tested harnesses.
- Confidence: medium
- Recommended action: read
- Rationale: The central pattern is supported by transparent aggregate counts and matched comparisons across multiple models, and it exposes a consequential failure hidden by retrieval metrics. Confidence stops short of high because distribution is not randomized, Required bundles multiple changes, repetitions are limited, model SDKs differ, checkpoints were partly retrospective, and known grading errors were not comprehensively re-adjudicated.

## Uncertainties

- **Whether evidence distribution itself causes lower detection, independent of retrieval difficulty, wording, salience, and worker reporting behavior.** — This is the main causal interpretation behind recommendations for conflict-preserving memory and structured reporting. The matched cohorts control instance identity but are selected using Required’s observed behavior rather than randomized evidence assignments.
  - Evidence: [b00078-1795531387] “Supplying identical evidence while varying which agents receive it would help separate the effect of distribution from retrieval difficulty.”
- **Whether the apparent handoff loss reflects intentional worker selection, endpoint-matcher misses, insufficient report capacity, or workers never recognizing locally innocuous values as globally conflicting.** — Each mechanism implies a different remedy: richer summaries, structured extraction, cross-worker comparison, greater overlap, or improved measurement.
  - Evidence: [b00074-a9ad9b3796] “workers summarizing isolated partitions lack the cross-document context needed to recognize figures that appear unproblematic in isolation as conflicting across documents”
- **How much the Judge Pass findings would change after comprehensive human review and correction of miscredited neighboring comparisons.** — Judge Pass is the primary semantic outcome; even a small number of systematic label errors can affect small conditioned cohorts and model-level comparisons.
  - Evidence: [b00077-7a43091556] “broader human review could refine endpoint matching and semantic grading.”
- **Whether Optional’s advantage comes from overlapping access, direct lead inspection, adaptive delegation, model-specific behavior, or another interaction.** — Optional is presented as the best pooled policy, but it does not isolate which design choice produces that advantage.
  - Evidence: [b00075-1e3d5868d0] “permitting overlapping source access and lead source inspection (Optional) consistently outperforms both single-agent and strictly partitioned execution.”

## Open questions

- Will the Same/Split effect persist when identical evidence text is randomly assigned to one or multiple workers while retrieval is held fixed?
- Which worker-report protocol best preserves conflict pairs: structured claim ledgers, mandatory source-value extraction, uncertainty flags, or full trace sharing?
- Does direct lead access rescue split evidence because the lead retrieves missing claims, validates provenance, or simply sees both claims in one context?
- How robust are the findings after human re-adjudication, task-clustered uncertainty estimation, more runs, and prospectively fixed checkpoints?
- Do naturally occurring semantic, temporal, and entity conflicts show the same stage-wise loss pattern as planted numerical discrepancies?
- What report-capacity, latency, and generation-cost tradeoffs arise when handoffs preserve more raw evidence?

## Proposed AIDB experiments

- **Hypothesis:** With evidence text and task instance held fixed, assigning both conflicting claims to one worker yields higher conflict detection than splitting the claims across two workers.
  - Baseline: Randomized single-worker assignment of both claims versus randomized two-worker split assignment, using identical claim text, lead prompt, total generation allowance, and no direct lead source access.
  - Primary metric: Difference in Judge Pass between randomized assignments, with task-clustered confidence intervals; secondary metrics are Worker Reports and Lead Evidence Pair Recall.
  - Stop condition: Pre-register the sample size and stop after the planned balanced assignments are complete; reject the hypothesis if the confidence interval for the detection difference includes zero or favors split assignment.
- **Hypothesis:** A structured worker handoff that requires claim, value, source, and possible-conflict fields increases complete-pair retention and final detection under partitioned delegation.
  - Baseline: The paper’s free-form Required worker-report protocol under the same model, documents, partitions, lead access, checkpoints, and generation allowance.
  - Primary metric: Lead Evidence Pair Recall; Judge Pass and generation cost are co-primary safety checks against evidence-preservation gains that do not improve outcomes or require disproportionate spending.
  - Stop condition: Stop adoption if Lead Evidence Pair Recall does not improve, if Judge Pass decreases, or if a pre-registered cost ceiling is exceeded.
- **Hypothesis:** Allowing the lead targeted source verification only after receiving split-provenance evidence recovers conflict detection more efficiently than unrestricted lead source access.
  - Baseline: Strict Required without lead reads, plus Optional as an upper-flexibility comparator, with identical prospective budgets and checkpoint rules.
  - Primary metric: Judge Pass per unit of generation spending, stratified by Same and Split provenance at the first lead checkpoint.
  - Stop condition: Reject the targeted-verification policy if it fails to improve split-cohort Judge Pass over strict Required or if its cost-adjusted performance does not match unrestricted lead access within a pre-registered equivalence margin.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:55:25.965647+00:00`
- Document SHA-256: `9a670d04ba2fd1a7fd572dc993cae74b09c95d235b85f3b493eb1410b947ee99`
- Metadata SHA-256: `19e7ad4c0777d64cb0b1d05a9af8ac6445f05dae6e8776318232a0eb37e0bde7`
- Blocks: 147
- Deterministic repair attempts: 0
