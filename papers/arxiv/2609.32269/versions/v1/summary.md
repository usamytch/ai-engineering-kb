# Before Answering: Evidence Sufficiency under Size-Matched Memory Construction

## Executive summary

The paper shows that deletion-based evidence-sufficiency benchmarks can leak labels through memory size, then introduces a size-matched construction and MemSafe, a query–unit cross-encoder with set aggregation. Controlled multi-hop QA results are strong, but much of the gain comes from cross-encoded relevance rather than set interaction. The main validity warning is consequential: performance and calibration fall under alternative insufficiency constructions and SQuAD transfer, while small clinical cohorts favor a lexical model. Reader gating reduces errors but remains far from deployable. The benchmark construction is a valuable contribution; broad adoption of the estimator would be premature without construction-diverse, deployment-scale validation.

## Problem

**Statement.** Determine, before answering, whether an agent’s retained memory contains current and sufficient evidence for a query, rather than merely whether a reader is confident in its answer.

**Why it matters.** Long-horizon agents summarize, retrieve, and evict information; missing updates or supporting facts can leave plausible-looking answers unsupported. The paper emphasizes clinical records as a high-consequence setting in which stale measurements may survive after their updates disappear.

**Scope.** The work studies answer-free sufficiency estimation, evidence localization, missing-evidence counting, selective answering, transfer across insufficiency constructions, and clinical numeric records. It does not evaluate memories produced by deployed agents or implement downstream retrieval and abstention policies.

## Method

The authors first construct memory variants whose unit count is fixed within each base query. MemSafe then encodes every query–unit pair, plus a bridge-conditioned pair using the highest-scoring unit, and aggregates the resulting unit tokens with a two-layer set transformer. Separate heads predict unsafe memory, the integrity state, evidence-bearing units, and missing-evidence count. Validation-selected thresholds turn the unsafe score into an answer gate.

### Key components

- Four integrity states: complete, missing, relation-lost, and—only for clinical temporal data—stale; every non-complete state is unsafe.
- Size matching retains the same number of units for every state of a base query and replaces removed evidence with deterministically selected distractors.
- A pretrained MiniLM cross-encoder processes query–unit pairs with a 256-token cap; bridge conditioning is intended to reveal lexically indirect second-hop evidence.
- Cross-fitted encoder fine-tuning predicts unit-level evidence without using integrity labels; Stage B receives embeddings from an encoder not trained on those same units.
- A two-layer set transformer combines cross-encoder outputs with lexical similarity, position, rank, and record-level provenance.
- Training jointly optimizes unsafe classification, integrity-state classification, per-unit evidence detection, and missing-count regression.
- Evaluation includes matched pooling and relevance comparators, lexical and surface controls, joint encoders, an LLM judge, construction transfer, reader gating, and clinical learning curves.

### Assumptions

- Annotated supporting paragraphs approximate the evidence required by a question, although the paper explicitly notes that annotations may omit alternative sufficient evidence routes.
- Size-only leakage is removed within a base query when all integrity variants have equal size; other surface artifacts, including text length, may remain.
- Validation-selected thresholds are assumed useful for selective answering, but they carry no distribution-free risk-control guarantee.
- Gold supporting facts define most benchmark variants and integrity labels, so the central task remains dependent on annotated evidence.
- Clinical learning-curve changes are interpreted mainly as scale effects even though realized patient composition also changes with the question cap.

## Main claims

- **The size-matched construction removes the paragraph-count shortcut under balanced per-query integrity variants and bounds deviations when variant multiplicities differ.**
  - Evidence: [b00034-c9abc0f13b] “if every base query contributes the same numbers of unsafe and complete examples, f has unsafe AUROC exactly 1/2.”; [b00032-f2d3ae8fcd] “Memory size and compression ratio are then constant within each base query.”
- **MemSafe separates query–unit encoding from set-level integrity reasoning and supplies both global sufficiency and localized evidence outputs.**
  - Evidence: [b00042-ffc19768ce] “Two transformer encoder layers let the units attend to one another, as in set transformers”; [b00042-ffc19768ce] “The query token feeds the unsafe, integrity-state, and missing-count heads, and each unit token feeds the per-unit evidence head.”
- **A continuous sufficiency score can gate a reader better than a binary ground-truth integrity label because complete memories vary in reader difficulty.**
  - Evidence: [b00081-7b41f81a22] “Complete memories differ in how difficult their evidence is to use”; [b00164-c2f138f0ad] “selective risk is minimized by accepting the examples with the smallest η⁡(q,M)=Pr⁡(Y=1∣q,M).”
- **Robustness to one synthetic insufficiency construction does not imply robustness to another construction or an independently authored unanswerability benchmark.**
  - Evidence: [b00073-08e8ec2d0c] “H3 is therefore refuted”; [b00063-9ce83f9aca] “the transferred threshold does not control risk.”

## Results

- **Size matching reduced the paragraph-count control from 0.979 unsafe AUROC to 0.5007 on MuSiQue and 0.5000 on the other two QA datasets, but text length still achieved 0.525 to 0.633, showing that count matching does not eliminate all artifacts.**
  - Context: This is the strongest validation of the benchmark intervention, with an explicit residual-artifact warning.
  - Evidence: [b00054-e7e7b9e474] “the paragraph-count control reaches 0.979 unsafe AUROC on MuSiQue”; [b00054-e7e7b9e474] “the control drops to 0.5007 on MuSiQue and to exactly 0.5000 on HotpotQA and 2WikiMultiHopQA”; [b00054-e7e7b9e474] “text length still reaches 0.525 to 0.633 AUROC”
- **On size-matched QA, MemSafe reached 0.9682, 0.9831, and 0.9999 AUROC on MuSiQue, HotpotQA, and 2WikiMultiHopQA; LexSet reached 0.5820, 0.6609, and 0.7351. The near-perfect third-dataset result is treated as saturation rather than decisive evidence of general reasoning.**
  - Context: Five-seed test means are reported, but the full pipeline was not independently retrained for every seed.
  - Evidence: [b00059-13f25d9a7a] “MemSafe (ours) 0.9682 0.7960 0.9831 0.8600 0.9999 0.9894”; [b00059-13f25d9a7a] “LexSet lexical event-set 0.5820 0.3111 0.6609 0.3916 0.7351 0.5029”; [b00075-47e736d339] “we treat this dataset as saturated and rely on MuSiQue to compare strong models.”
- **Component evidence indicates overlapping gains: full MemSafe scored 0.9674, freezing the encoder reduced it to 0.9121, removing bridge conditioning to 0.9423, and replacing the set model with mean pooling to 0.9502. Removing both fine-tuning and the set model yielded 0.7407, closing 41% of the stated gap.**
  - Context: The single-component table is more diagnostic than the attribution ladder, but only three Stage B seeds share one encoder, and the paper cautions against causal credit allocation.
  - Evidence: [b00067-d205867fac] “Full MemSafe 0.9674±0.0008”; [b00067-d205867fac] “w/o encoder fine-tuning (frozen encoder) 0.9121 (−0.0553)”; [b00067-d205867fac] “w/o bridge-conditioned encoding 0.9423 (−0.0251)”; [b00067-d205867fac] “w/o set model (mean pooling) 0.9502 (−0.0173)”; [b00204-3be5786437] “This model reaches 0.7407”; [b00204-3be5786437] “already closes 0.1587 of the 0.3854 gap (41%).”
- **Generalization is weak: family-A-to-B transfer lost 0.0734 AUROC for MemSafe versus 0.0550 for flat TF-IDF, while zero-adaptation SQuAD 2.0 transfer reached 0.6393 AUROC and a 5% source-domain threshold realized 0.2759 risk at 0.0049 coverage.**
  - Context: These are consequential negative results because they challenge deployment of a fixed estimator and threshold outside the construction used for training.
  - Evidence: [b00073-08e8ec2d0c] “loses more under the shift: 0.0734 AUROC, against 0.0550 for flat TF-IDF.”; [b00063-9ce83f9aca] “Applied without adaptation to the SQuAD 2.0 development set (Rajpurkar et al., 2018), whose unanswerable questions are written by crowdworkers rather than produced by deletion, the MuSiQue-trained model reaches 0.6393 AUROC.”; [b00063-9ce83f9aca] “its MuSiQue threshold for a 5% risk budget accepts only 0.0049 of questions yet realizes a risk of 0.2759”
- **For the 7B reader, MemSafe gating lowered answered-question error from 0.8503 to 0.6306±0.0206 at 5% coverage, but roughly two thirds of accepted answers remained wrong; at 10% coverage the LLM judge was better.**
  - Context: The fixed-coverage protocol was adopted after the preregistered reader-risk targets proved unattainable, so this analysis is exploratory rather than confirmatory.
  - Evidence: [b00080-64e89cd74a] “from 0.8503 to 0.6306±0.0206 at 5% coverage”; [b00081-7b41f81a22] “about two thirds of answered questions remain wrong at 5% coverage”; [b00081-7b41f81a22] “The LLM judge, from the reader’s own model family, is the better gate at 10% coverage”; [b00079-614428bf59] “treat this analysis as exploratory.”

## Experimental evaluation

### Datasets

- MuSiQue, HotpotQA in the distractor setting, and 2WikiMultiHopQA; processed totals are reported with exclusions and memory variants.
  - Evidence: [b00047-9e39bcf352] “We use the full processed MuSiQue (Trivedi et al., 2022), HotpotQA (Yang et al., 2018) (distractor setting), and 2WikiMultiHopQA”; [b00178-bb1390f75b] “MuSiQue 44,710 21,902 22,808 65,297”
- MuSiQue-Full unanswerable questions form family B, an equal-context-length alternative construction with split isolation from family A.
  - Evidence: [b00047-9e39bcf352] “Family B consists of the unanswerable questions released with MuSiQue”; [b00047-9e39bcf352] “no test question in one family appears in training in the other.”
- SQuAD 2.0 development data provide independent-construction transfer without adaptation.
  - Evidence: [b00063-9ce83f9aca] “Applied without adaptation to the SQuAD 2.0 development set”
- MIMIC-IV 3.1 OMR and laboratory events test temporal numeric memories, including stale states.
  - Evidence: [b00084-05feb78308] “We use two MIMIC-IV 3.1 sources (Johnson et al., 2023), OMR and laboratory events”

### Baselines

- LexSet lexical event-set estimator, flat TF-IDF logistic classifier, sufficient-context-style TF-IDF, retrieval-similarity proxy, text-length, paragraph-count, provenance-only, and majority controls.
  - Evidence: [b00059-13f25d9a7a] “Flat TF-IDF logistic”; [b00059-13f25d9a7a] “LexSet lexical event-set”; [b00059-13f25d9a7a] “Paragraph-count control”
- Matched encoder comparators use mean pooling or aggregated relevance; joint alternatives concatenate the memory, including an exploratory long-context ModernBERT encoder.
  - Evidence: [b00044-a6e5de5ef8] “mean pooling with the same heads but no attention between units”; [b00061-b0ca1242b3] “A ModernBERT joint encoder (Warner et al., 2025) with an 8,192-token window”
- A pinned Qwen2.5-7B-Instruct sufficiency judge is evaluated zero-shot and four-shot, and reader confidence plus the true integrity label serve as gating comparators.
  - Evidence: [b00195-a42caed8f3] “We evaluate Qwen2.5-7B-Instruct, pinned to a public revision”; [b00229-b5dd576acf] “The oracle row gates on the true integrity label”

### Metrics

- Primary metric: unsafe AUROC; secondary metrics include integrity macro F1, calibration error, per-unit evidence AUPRC, and missing-count MAE.
  - Evidence: [b00049-c1595fc7f1] “Our primary metric is unsafe AUROC”; [b00049-c1595fc7f1] “integrity macro F1, expected calibration error (ECE), the area under the precision-recall curve (AUPRC)”; [b00049-c1595fc7f1] “mean absolute error (MAE) of the missing count.”
- Selective evaluation reports evidence risk, reader risk, coverage, and risk–coverage behavior.
  - Evidence: [b00030-8c1f29990e] “the evidence risk RE​(t)=Pr⁡(z≠complete∣r≤t) and the reader risk RY​(t)=Pr⁡(Y=1∣r≤t)”; [b00218-13e3c281a2] “AURC is lower-is-better; coverage is the test fraction accepted”

### Ablations

- Single-component MuSiQue ablations remove encoder fine-tuning, bridge conditioning, set aggregation, lexical/position features, or localization heads; one row removes both fine-tuning and the set model.
  - Evidence: [b00066-bb1a703853] “Single-component ablations on MuSiQue”; [b00067-d205867fac] “w/o encoder fine-tuning and set model 0.7407 (−0.2268)”
- Silver answer-string supervision tests dependence on gold unit targets and preserves detection more than localization.
  - Evidence: [b00071-55ef0e2760] “lowers AUROC only from 0.9674 to 0.9444, but per-unit AUPRC from 0.9123 to 0.4252”
- A memorization audit restricts evaluation to questions whose gold evidence never appears in training, while acknowledging that population shift and pretraining overlap remain unresolved.
  - Evidence: [b00210-d8270c5454] “Restricting evaluation to questions whose gold evidence never appears in training”; [b00210-d8270c5454] “it does not exclude every form of memorization.”

### Negative results

- The preregistered robustness hypothesis was refuted because MemSafe degraded more than flat TF-IDF across construction families.
  - Evidence: [b00073-08e8ec2d0c] “H3 is therefore refuted”
- The bridge ablation registered for 2WikiMultiHopQA was not run there.
  - Evidence: [b00187-f9f8a0a4ae] “untested on 2WikiMultiHopQA, since the ablation runs on MuSiQue only”
- At the smallest clinical scale, LexSet ranked unsafe memories better than MemSafe.
  - Evidence: [b00084-05feb78308] “LexSet ranks memories better than MemSafe (0.9649 versus 0.9220 AUROC)”
- The preregistered reader-risk criteria were not met and were replaced by fixed-coverage reporting after observing the base error rate.
  - Evidence: [b00189-99bae95ab9] “Criteria (i) and (ii) are not met as stated”; [b00189-99bae95ab9] “we replace them with fixed-coverage reporting after observing the base error rate.”


## Limitations

- The evaluated memories are constructed from benchmarks and retrospective records, not generated by deployed memory agents; ecological validity is therefore unestablished.
  - Evidence: [b00086-bb3711120e] “not produced by deployed agents.”; [b00092-15eedf7007] “Corrupted-memory states are constructed artifacts, not observed clinical failures.”
- Gold evidence annotations still define variants and integrity labels even when silver unit supervision is used, leaving annotation-free construction and localization unresolved.
  - Evidence: [b00086-bb3711120e] “gold annotations still define the memory variants and integrity labels”; [b00086-bb3711120e] “learning from memories without annotated evidence remains open.”
- The five seeds do not represent five independent repetitions of the full pipeline, and bootstrap intervals omit a separate encoder-training level, understating full-pipeline variation.
  - Evidence: [b00049-c1595fc7f1] “the five seeds are not five independent repetitions of the full pipeline.”; [b00049-c1595fc7f1] “they understate full-pipeline variation.”
- The clinical crossover does not isolate training quantity from patient composition, and the smallest cohort favors the engineered lexical estimator.
  - Evidence: [b00237-690c8db3ee] “without isolating training-data quantity from cohort composition.”; [b00084-05feb78308] “it remains the better ranker for small clinical cohorts.”
- Reader gating covers one dataset with greedy decoding, failed its original risk targets, and remains far from a deployable error level.
  - Evidence: [b00086-bb3711120e] “the reader study covers one dataset with greedy decoding.”; [b00081-7b41f81a22] “without yielding a deployable operating point on MuSiQue.”
- The size-matched benchmark still contains surface cues and the saturated 2WikiMultiHopQA setting cannot distinguish strong models reliably.
  - Evidence: [b00054-e7e7b9e474] “The construction is therefore count-matched rather than free of artifacts.”; [b00075-47e736d339] “we treat this dataset as saturated”
- Thresholds are selected empirically on validation data and offer no formal finite-sample risk guarantee under either in-domain sampling or distribution shift.
  - Evidence: [b00026-5b5836292f] “choose its threshold on validation data without such a guarantee”; [b00063-9ce83f9aca] “the transferred threshold does not control risk.”

## Reproducibility

**Status:** partial

The paper provides unusually detailed procedural reporting and claims strong run-level provenance, checksums, per-seed records, and verification tooling. Reproduction is nevertheless only partial from the supplied material: the artifact location and software environment are absent, clinical data access is restricted, and the replication design does not independently repeat every training stage.

**Available artifacts**

- The appendix is stated to contain proofs, dataset construction and exclusion counts, training configuration, selection grid, and preregistered criteria and outcomes.
- Accompanying code is stated to record raw and processed-data checksums, per-seed metrics, and run fingerprints.
- A verification script is stated to re-check the chain from raw files to run coverage.
- Runs report one NVIDIA RTX 3090, fixed seeds, deterministic hashing, and recorded exclusion reasons.

**Missing pieces**

- No code repository URL, artifact identifier, software environment, dependency lockfile, or license is present in the supplied metadata and blocks.
- MIMIC-IV records are not redistributed and require credentialed access.
- The supplied blocks do not independently verify that the stated code and verification script are accessible or executable.
- Full-pipeline uncertainty is not captured because some Stage B seeds reuse encoders and bootstrap intervals omit encoder-training variation.

## AIDB assessment

- Novelty: The most convincing novelty is methodological rather than architectural: the paper identifies a severe size leak, formalizes when size-only estimators must be at chance, and evaluates sufficiency under a count-matched construction. MemSafe itself combines established cross-encoding and set attention, with careful attribution showing that the cross-encoder supplies most of the signal.
- Usefulness: Highly useful for benchmark design and review practice: future evidence-sufficiency work should include size-matched controls, alternative construction families, calibrated operating points, and scale-matched domain baselines. MemSafe is a strong research baseline but is not ready as a general-purpose or clinical gate because transfer, threshold control, sample efficiency, and reader error remain problematic.
- Confidence: high
- Recommended action: read
- Rationale: Read and use the construction and evaluation protocol as a benchmark-design reference. Do not adopt the estimator as a deployment component without new tests on naturally occurring agent-memory failures, construction-diverse training, independently repeated pipelines, and deployment-specific risk calibration. The paper’s own negative results materially qualify its headline in-domain scores.

## Uncertainties

- **Whether size-matched synthetic corruptions resemble the failure modes produced by real summarization, retrieval, and eviction systems.** — If real failures differ structurally, high in-construction AUROC may not predict operational safety.
  - Evidence: [b00086-bb3711120e] “not produced by deployed agents.”; [b00092-15eedf7007] “Corrupted-memory states are constructed artifacts”
- **Whether MemSafe’s continuous score captures reader-specific answerability or merely correlates with it on the tested MuSiQue readers.** — The LLM judge wins at one operating point, and no combined gate or model-family isolation experiment is reported.
  - Evidence: [b00226-527f0081b6] “we do not isolate a model-family effect or test a combined gate.”
- **How much full-pipeline performance varies under independently trained encoders and more seeds.** — Reported stability may be optimistic when encoders are reused across Stage B seeds.
  - Evidence: [b00049-c1595fc7f1] “Stage B seeds 71 and 101 reuse the encoders of seeds 17 and 29”; [b00049-c1595fc7f1] “they understate full-pipeline variation.”
- **Whether the clinical crossover is caused by training volume, broader patient coverage, or cohort composition.** — The answer determines when a learned estimator should replace explicit numeric-trend features in small clinical cohorts.
  - Evidence: [b00084-05feb78308] “patient counts also grow along it (929 to 3,934).”; [b00237-690c8db3ee] “without isolating training-data quantity from cohort composition.”

## Open questions

- Can an insufficiency benchmark be built from naturally observed agent-memory failures while preserving auditable evidence labels?
- Would training jointly across several corruption mechanisms improve family-B and SQuAD transfer without sacrificing in-domain discrimination?
- Can reader-aware and answer-free sufficiency scores be combined to outperform each component across all coverage levels?
- How should thresholds be calibrated to provide finite-sample risk guarantees under prevalence and construction shift?
- Can missing evidence be localized accurately without gold supporting-fact annotations?
- Does the clinical crossover persist when training variants increase while the patient cohort is held fixed?

## Proposed AIDB experiments

- **Hypothesis:** Training on multiple insufficiency mechanisms improves out-of-construction discrimination and threshold transfer while retaining most size-matched MuSiQue performance.
  - Baseline: MemSafe trained only on size-matched family A, evaluated unchanged on family B and SQuAD 2.0.
  - Primary metric: Unsafe AUROC plus realized evidence risk and coverage at a validation-selected target, reported separately for each held-out construction.
  - Stop condition: Reject the hypothesis if construction-diverse training fails to improve both held-out AUROC and absolute risk-target error, or reduces family-A AUROC beyond a preregistered non-inferiority margin.
- **Hypothesis:** A learned combination of MemSafe and a reader-family judge yields lower reader risk than either score alone across coverage levels.
  - Baseline: MemSafe unsafe score, zero-shot LLM judge, reader sequence confidence, and ground-truth integrity gating.
  - Primary metric: Area under the reader risk–coverage curve on held-out questions, with fixed-coverage error as secondary analysis.
  - Stop condition: Stop if the combined gate’s paired confidence interval does not exclude zero improvement over the best single gate on a construction-disjoint test set.
- **Hypothesis:** MemSafe’s clinical crossover is driven by training-example volume rather than changing patient composition.
  - Baseline: LexSet and MemSafe trained at increasing variant counts on one fixed patient cohort.
  - Primary metric: Unsafe AUROC difference between MemSafe and LexSet, with macro F1 and evidence-risk coverage as secondary metrics.
  - Stop condition: Stop when the confidence interval for the AUROC difference remains on the same side of zero across two successive sample sizes, or when the fixed cohort is exhausted.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:25:56.821467+00:00`
- Document SHA-256: `5a067d7c253070d8f10127c21b74e05432eecc1c5cebd94fc94760c77e4a19de`
- Metadata SHA-256: `0695fb5ebb4b0815ef8d199fd450ce8f3ba0c030ca45b922869e413163d25914`
- Blocks: 250
- Deterministic repair attempts: 1
