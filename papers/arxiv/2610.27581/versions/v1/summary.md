# DuplexLedger: Benchmarking Transactional Memory in Full-Duplex Speech Agents

## Executive summary

DuplexLedger aligns adaptive speech events with explicit Write/Update/Ignore/Retain transitions and same-session QA. Five baseline systems reveal a severe interaction–memory gap: the best final-state coverage is only 2.01%. ACT-Mem adds an event controller, versioned ledger, and typed retriever to a frozen MiniCPM-o 4.5 backbone. In a paired held-out comparison, latest-value accuracy rises from 4.11% to 8.68%, but final-state evidence is inconclusive and interruption stopping worsens. The benchmark is diagnostically valuable, yet external validity is limited by synthetic short sessions, and interpretation depends on the auxiliary metadata supplied to ACT-Mem. Independent reproduction should precede adoption.

## Problem

**Statement.** Full-duplex agents must decide whether concurrent, incomplete, revised, backchannel, or non-addressed speech should alter persistent memory. Existing evaluations separate interaction timing from memory outcomes, obscuring the state transitions behind a correct answer.

**Why it matters.** Persistent-memory errors can preserve obsolete values, admit irrelevant side speech, or answer from transient context. Joint event and state supervision is needed to distinguish admission, supersession, retrieval, and answer-generation failures.

**Scope.** The paper studies bilingual Chinese–English same-session memory under interruption, backchannel, within-turn pause, and speech addressed to another person. It does not establish natural-dialogue, hour-scale, cross-day, deletion, privacy-management, or broad multilingual performance.

## Method

DuplexLedger represents persistent sessions as ordered event streams with item-level Write, Update, Ignore, or Retain targets and explicit states. Adaptive scheduling injects interruptions and backchannels only after decoded assistant speech satisfies a trigger; pauses and side-talk use observation windows. Six spoken targets per session test revision, recall, distractor rejection, consolidation, and behavior. ACT-Mem uses frozen ASR/VAD observations, predicts event operation, addressee, completeness, and confidence, commits admissible entity–value slots to a versioned ledger, and supplies typed active-state evidence to the frozen backbone at QA boundaries.

### Key components

- A synthetic bilingual benchmark with event-level operations, supersession links, oracle states, supporting and forbidden evidence, and persistent same-session QA.
- A closed-loop protocol separating planned from realized challenges and retaining failures, timeouts, unanswered questions, decoded audio, and timing traces.
- An event controller assigning proposals to Prepare, Commit, Abort, or Uncertain states.
- A versioned ledger retaining provenance and supersession links while exposing active values to retrieval.
- A typed retriever that varies evidence scope by question type and injects evidence cards through QA-only text prefill.
- Session-level macro-aggregation and paired session bootstrap for the controlled comparison.

### Assumptions

- The deterministic bilingual lexical scorer adequately represents semantic answer correctness.
- Frozen-ASR transcripts preserve the facts and boundaries needed by the controller and scorer.
- Fixed question denominators appropriately combine missed delivery, silence, and downstream memory errors for end-to-end evaluation.
- Controlled synthetic scenarios represent meaningful components of real full-duplex memory.
- The controlled comparison is interpretable only when auxiliary metadata access and question-routing mode are declared.

## Main claims

- **DuplexLedger jointly exposes adaptive interaction, event admission, revision, exclusion, explicit state transitions, and spoken memory QA.**
  - Evidence: [b00008-fc41d0f0b9] “We introduce DuplexLedger, a bilingual benchmark of 1,094 persistent sessions aligning pause handling, speech to others, backchannels, and interruptions with write, update, ignore, and retain operations”; [b00029-e78c3958d6] “Each question is aligned with supporting memory identifiers, forbidden superseded or distractor identifiers, and a reference answer.”
- **Current full-duplex systems do not jointly achieve strong interaction behavior and coherent persistent memory.**
  - Evidence: [b00046-a1d5258eba] “No model jointly dominates full-duplex interaction and memory fidelity.”; [b00056-9c52d8e7d2] “Current systems can coordinate speech, recover isolated revisions, or reject irrelevant content, yet none jointly supports event admission, supersession, exclusion, and state consolidation.”
- **ACT-Mem makes memory transitions explicit and auditable while leaving speech-generation components frozen.**
  - Evidence: [b00059-1ff3d27f73] “The latter supplies transcripts and timing to a trainable event controller, which manages a transactional ledger implemented as versioned memory.”; [b00059-1ff3d27f73] “Only these cards enter the backbone through QA-only text prefill; all speech-generation components remain frozen.”
- **The controlled evidence supports improved local revision but not complete session-wide state reconstruction.**
  - Evidence: [b00084-6f83dde195] “The controlled evidence therefore supports improved local state revision, but not yet complete reconstruction of the session-wide memory state.”

## Results

- **Across the five baselines, the strongest final-state fact coverage is 2.01%; the system with the best latest-value accuracy reaches 25.50% but adopts 48.17% of distractors and covers 1.06% of final-state facts.**
  - Context: This supports the reported interaction–memory gap. Cross-model results remain descriptive because architectures, response tendencies, interfaces, and realized exposure differ.
  - Evidence: [b00056-9c52d8e7d2] “Even the best final-state coverage is only 2.01%.”; [b00055-7ccabbffc2] “Lychee-FD reaches 25.50% latest-value accuracy but covers only 1.06% of final-state facts and adopts 48.17% of distractors.”; [b00044-2a7a1b7237] “Since model architectures and response tendencies differ, cross-model results are descriptive.”
- **On 219 held-out sessions, ACT-Mem raises latest-value accuracy from 4.11% to 8.68%, with a 95% CI of [1.60,7.53]. Final-state coverage rises from 1.27% to 2.00%, but its 95% CI of [−0.49,1.99] crosses zero.**
  - Context: The paired comparison retains the frozen MiniCPM-o 4.5 backbone. It supports improved local revision, not comprehensive final-state reconstruction.
  - Evidence: [b00081-fa9e195306] “We evaluate ACT-Mem on the same 219 held-out sessions used for the baseline study”; [b00084-6f83dde195] “Latest-value accuracy increases from 4.11% to 8.68% (+111.2%; +4.57 percentage points, 95% CI [1.60,7.53])”; [b00084-6f83dde195] “final-state coverage rises from 1.27% to 2.00% (+57.5%; +0.73 points, 95% CI [−0.49,1.99]).”
- **ACT-Mem improves exposed-challenge boundary measures but worsens interruption recovery: cFD increases by 10.8%, Stop@0.8 declines from 51.06% to 45.00%, and median stopping latency rises from 1.123 to 1.340 seconds.**
  - Context: The interaction comparison is not cleanly causal: cFD is conditional, challenge realization changes, and evidence injection begins after preceding interaction events.
  - Evidence: [b00088-a681f71771] “cFD increases by 10.8%, while early response, pre-end speech, and windowed intrusion decrease by 18.6%, 7.6%, and 5.1%, respectively.”; [b00088-a681f71771] “Stop@0.8 falls from 51.06% to 45.00%, and median stopping latency increases from 1.123 to 1.340 seconds.”; [b00430-01066ab0e6] “Cross-variant differences in pre-QA interaction metrics are therefore descriptive whole-run differences, rather than isolated causal effects of retrieval or ledger maintenance.”
- **Untyped retrieval obtains 9.59% latest-value accuracy versus 8.68% for ACT-Mem, while stale assertions and distractor adoption reach 1.60% and 19.63%, compared with 0.46% and 11.42% for ACT-Mem.**
  - Context: These inference-time ablations support a selectivity trade-off but do not isolate training-time contributions or repeated-run variability.
  - Evidence: [b00090-c0efd02b99] “We evaluate three inference-time variants with fixed memory-model weights.”; [b00093-5e5f125a19] “Untyped retrieval 40.33 29.98 44.61 9.59 1.60 19.63 1.82 ACT-Mem 41.19 16.03 41.82 8.68 0.46 11.42 2.00”; [b00094-a94c8918f8] “All values are percentages.”
- **Latest-value accuracy decreases under user interruption from 3.85% to 2.88%, while backchannel final-state coverage falls from 2.34% to 1.10%.**
  - Context: These subgroup results are exploratory, identifying interruption-time updating as a targeted weakness rather than establishing a general causal effect.
  - Evidence: [b00097-b6813d87f4] “Under user interruption, however, latest-value accuracy decreases from 3.85% to 2.88%; backchannel final-state coverage also falls from 2.34% to 1.10%.”; [b00483-b9c62ba558] “These stratified analyses are not treated as independent confirmatory tests”

## Experimental evaluation

### Datasets

- DuplexLedger is a controlled synthetic Chinese–English corpus covering four full-duplex scenarios, with event operations, explicit memory states, and same-session spoken targets.
  - Evidence: [b00033-04f3c65dbc] “Total 577 517 1,094 8,239 3,304 6,564”; [b00149-cf40c53d50] “All dialogue content is synthetic.”; [b00036-7852c2451d] “method train/validation/calibration/held-out splits contain 660/175/40/219 sessions.”

### Baselines

- The descriptive benchmark evaluates MiniCPM-o 4.5, Freeze-Omni, Moshi, Lychee-FD, and PersonaPlex-7B-v1.
  - Evidence: [b00353-38e71af68b] “We evaluate five publicly available full-duplex speech models: MiniCPM-o 4.5 (Cui et al., 2026), Freeze-Omni (Wang et al., 2025c), Moshi (Défossez et al., 2024), Lychee-FD (Liu et al., 2026), and PersonaPlex-7B-v1”
- The controlled baseline is the frozen MiniCPM-o 4.5 backbone without ACT-Mem.
  - Evidence: [b00081-fa9e195306] “The controlled comparison retains the frozen MiniCPM-o 4.5 backbone”

### Metrics

- Interaction evaluation includes challenge realization, conditional full-duplex behavior, onset and overlap errors, intrusion, stopping success, and stopping latency; conditional measures require coverage variables.
  - Evidence: [b00322-17fb7bbba0] “challenge_realization_rate ↑ Distinct planned challenge identifiers. conditional_cfd ↑† Challenge instances eligible for conditional behavioral scoring.”; [b00323-aff4b5868b] “† Conditional or auxiliary measures that must be interpreted with challenge realization, trigger timeout, and observability statistics.”
- Memory evaluation includes response rate, latest-value accuracy, superseded-value error, distractor adoption/rejection, and summary fact coverage.
  - Evidence: [b00347-3fef40b34d] “latest_value_accuracy ↑ All latest-value questions, including unanswered questions. superseded_value_error ↓ All latest-value questions.”; [b00347-3fef40b34d] “distractor_adoption_rate ↓ All distractor-ignore questions. distractor_rejection_accuracy ↑ All distractor-ignore questions; rejection additionally requires a response.”; [b00347-3fef40b34d] “summary_fact_coverage ↑ Atomic reference facts in final-summary questions.”
- Primary uncertainty intervals use paired session-level bootstrap.
  - Evidence: [b00473-a361a06654] “We therefore use a paired percentile bootstrap at the session level.”; [b00476-92b184f2fe] “We generate 20,000 bootstrap replicates using random seed 20260807.”

### Ablations

- FIFO memory removes versioned supersession and latest-only selection.
  - Evidence: [b00090-c0efd02b99] “FIFO memory replaces the versioned ledger with a 32-slot queue and removes supersession and latest-only selection.”
- Removing addressee gating disables speaker/addressee rejection and the learned gate.
  - Evidence: [b00090-c0efd02b99] “Without addressee gating removes speaker/addressee rejection and the learned gate.”
- Untyped retrieval applies top-4 retrieval to every question type.
  - Evidence: [b00090-c0efd02b99] “Untyped retrieval applies top-4 retrieval to every question type, including rejection questions.”
- Threshold sensitivity is assessed on calibration sessions; stricter admission reduces recall and F1.
  - Evidence: [b00104-3e6f89971d] “Increasing the threshold from 0.35 to 0.75 reduces recall from 55.26% to 48.95% and F1 from 71.19% to 65.72%.”

### Negative results

- Final-state reconstruction remains weak, and its controlled improvement is inconclusive.
  - Evidence: [b00084-6f83dde195] “Final-state coverage, however, remains low and its interval crosses zero.”
- ACT-Mem slows interruption stopping.
  - Evidence: [b00088-a681f71771] “ACT-Mem improves most interaction-boundary metrics but slows interruption stopping.”
- Distractor rejection and response rate decline despite fewer explicit adoptions.
  - Evidence: [b00085-52ad514fca] “Distractor rejection and response rate decline by 2.28 and 1.45 points”; [b00085-52ad514fca] “their joint decline means that ACT-Mem produces fewer explicit adoptions but also fewer credited rejections.”
- Interruption-time latest-value performance declines.
  - Evidence: [b00097-b6813d87f4] “Under user interruption, however, latest-value accuracy decreases from 3.85% to 2.88%”


## Limitations

- The fully synthetic, short sessions underrepresent spontaneous speech conditions and do not validate long-term memory.
  - Evidence: [b00234-91e2eb5c0a] “DuplexLedger is fully synthetic and therefore does not reproduce the complete distribution of spontaneous human speech.”; [b00234-91e2eb5c0a] “The sessions last approximately one to three minutes and do not establish performance on hour-scale or cross-day memory.”
- The task lacks explicit deletion and is not a complete privacy-aware memory benchmark.
  - Evidence: [b00235-6c2397e808] “it does not currently contain an explicit memory-deletion operation. It should therefore not be interpreted as a complete benchmark for privacy-aware memory management.”
- Fixed-denominator scores combine missed challenge delivery with downstream memory and response failures.
  - Evidence: [b00264-4a9a615ca2] “Fixed-denominator memory scores therefore measure end-to-end task completion and can reflect both missed evidence delivery and subsequent memory or response errors.”; [b00264-4a9a615ca2] “They do not isolate retention conditional on receiving the supporting evidence.”
- Bootstrap intervals omit repeated-generation variability, ASR errors, and scorer validity.
  - Evidence: [b00480-fce19e81fe] “they do not account for repeated-run generation variability, ASR errors, or scoring-rule validity.”
- Corpus quality-control issues include missing forced alignments and trailing residual audio.
  - Evidence: [b00220-7cce215b27] “Of 7,687 speech events, 7,589 have forced-alignment boundaries.”; [b00220-7cce215b27] “3,007 aligned events contain more than 0.5 s of trailing residual audio”
- Qualitative traces expose unresolved entity normalization, supersession, and clause-level admission failures.
  - Evidence: [b00532-10a1426bba] “The high-level Update decision was correct, but the correction did not supersede the provisional entries because the extracted entity representation was inconsistent.”; [b00533-32ec4c8570] “The same trace also reveals a limitation of clause-level admission.”

## Reproducibility

**Status:** partial

The documentation supports score reconstruction in principle, but reproducibility is partial from the supplied evidence. A code link and artifact specification do not verify release completeness. Reproduction must declare auxiliary metadata access, routing mode, model revisions, and recorded outputs.

**Available artifacts**

- The abstract reports a public code repository.
- The paper specifies splits, optimization stages, hyperparameters, seeds, parameter counts, hardware, calibration, timing, metric denominators, and bootstrap procedures.
- The artifact manifest describes inputs, manifests, memory supervision, runtime logs, outputs, scores, ACT-Mem traces, configurations, and scripts.
- Stable identifiers connect sessions, questions, schedules, outputs, evidence, and scores.

**Missing pieces**

- The supplied document does not verify that the repository contains every promised artifact, checkpoint, waveform, output, license, prompt, checksum, and validation report.
- The reported ACT-Mem question-routing mode is unresolved: the implementation permits annotation-assisted types or deterministic text routing.
- The controller receives scheduler-provided speaker/addressee metadata, but its contribution relative to learned inference is not quantified.
- No repeated-run variance or uncertainty from ASR and scorer validity is reported.

## AIDB assessment

- Novelty: High at the evaluation-design level: the work combines adaptive full-duplex execution with transactional supervision, explicit memory states, forbidden evidence, and auditable traces. The individual ACT-Mem components are less novel than their integration.
- Usefulness: High for diagnosing admission, supersession, exclusion, retrieval, and answer-realization failures separately. Deployment value is limited because absolute memory performance remains low and the benchmark is synthetic and short.
- Confidence: medium
- Recommended action: read
- Rationale: The benchmark design, denominator discipline, paired comparison, and traceability merit close reading and reproduction. Adoption is premature because final-state performance remains near the floor, interruption behavior worsens, external validity is narrow, and metadata access is insufficiently explicit.

## Uncertainties

- **The reported ACT-Mem question-routing mode is unclear.** — Annotation-assisted routing may simplify retrieval and alter whether results represent end-to-end audio-only performance.
  - Evidence: [b00419-97a2a9b651] “an annotated type is loaded from the configured QA metadata when available; otherwise, a deterministic rule routes the ASR-transcribed question.”; [b00419-97a2a9b651] “These annotation-assisted and text-routed modes must be distinguished when interpreting results.”
- **Evaluator-side structural metadata is not cleanly separated from learned perception in the headline comparison.** — Explicit addressee metadata can veto admission, potentially overstating performance relative to an audio-only controller.
  - Evidence: [b00399-5a2b316fbf] “The scheduler supplies the event index and speaker/addressee metadata.”; [b00399-5a2b316fbf] “a non-user or non-addressed event can veto admission through an explicit gate.”
- **Cross-model differences may partly reflect unequal challenge delivery and native interfaces.** — The baseline table should not be treated as a controlled architectural ranking.
  - Evidence: [b00353-38e71af68b] “the subset of challenge clips actually delivered can differ across models.”; [b00360-4c3a0106db] “The native interfaces do not expose identical user-turn controls.”
- **The lexical scorer’s validity for bilingual semantic correctness is not independently established.** — Small improvements may be sensitive to transcription and lexical thresholds.
  - Evidence: [b00330-13e7b2b43e] “A value is considered present when its normalized form is an exact substring of the answer or when token F1 reaches 0.80 for values of at most two tokens and 0.60 for longer values.”; [b00480-fce19e81fe] “they do not account for repeated-run generation variability, ASR errors, or scoring-rule validity.”

## Open questions

- Which question-routing mode and scheduler metadata fields were enabled for each reported ACT-Mem result?
- How does ACT-Mem compare with an audio-only controller receiving neither evaluator addressee labels nor annotated question types?
- Do gains persist with spontaneous speech, natural overlap, accents, noise, longer sessions, and cross-day state?
- What fraction of held-out errors originates at ASR, operation classification, slot extraction, normalization, supersession, retrieval, and spoken realization?
- Are differences stable across repeated generation runs and alternative semantic or human scoring?
- Can the ledger support deletion, consent, and retention limits without weakening auditability?

## Proposed AIDB experiments

- **Hypothesis:** ACT-Mem’s latest-value advantage remains positive after removing evaluator-supplied addressee labels and annotated question types.
  - Baseline: Reported ACT-Mem versus a strictly audio-derived variant using frozen-ASR transcripts, deterministic question routing, and learned addressee prediction.
  - Primary metric: Paired latest-value accuracy, accompanied by distractor adoption, explicit rejection, response rate, and final-state fact coverage.
  - Stop condition: Reject the hypothesis if the paired latest-value interval includes zero or distractor adoption rises without improved explicit rejection.
- **Hypothesis:** The versioned ledger, rather than QA conditioning alone, reduces stale answers under identical interaction histories.
  - Baseline: Replay fixed transcripts and questions through FIFO memory, an unversioned active store, and the full versioned ledger while holding controller outputs, retrieval weights, and generation seeds fixed.
  - Primary metric: Superseded-value error, with failed-supersession rate as the mechanistic secondary metric.
  - Stop condition: Stop if the versioned ledger fails to reduce both superseded-value error and failed-supersession rate relative to every baseline.
- **Hypothesis:** ACT-Mem’s revision advantage transfers to spontaneous, longer conversations without worsening interruption stopping.
  - Baseline: Frozen MiniCPM-o 4.5 versus ACT-Mem on newly recorded bilingual sessions containing natural disfluency, accents, noise, unplanned overlap, and longer contexts.
  - Primary metric: Paired latest-value accuracy, jointly gated by final-state fact coverage and interruption Stop@0.8.
  - Stop condition: Stop deployment-oriented evaluation if the latest-value interval includes zero, final-state coverage remains near the benchmark floor, or interruption Stop@0.8 is materially lower than the backbone.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T09:05:16.092883+00:00`
- Document SHA-256: `187028f535eb0092c4659d8f3bc2ff191d166a97fe49cfa12f80006fb77984ed`
- Metadata SHA-256: `66082b7ce18c23e77c5af1e6525224b2101f7b7bcd71ec42f640a11b1f3d9a7d`
- Blocks: 555
- Deterministic repair attempts: 1
