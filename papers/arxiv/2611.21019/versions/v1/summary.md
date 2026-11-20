# MemDoctor: Stage-wise Error Attribution and Repair for MLLM Agent Memory

## Executive summary

The paper decomposes multimodal agent memory into Write, Update, Retrieve, and Answer, then introduces MemDoctor: a test-time loop that traces required facts backward through logged memory, accepts only evidence-grounded diagnoses, repairs the implicated stage, and answers again. Controlled injections show that erroneous records can persist and appear as valid evidence, especially when no redundant evidence exists. On the reported benchmarks, a 4B MemDoctor system improves over its unrepaired version and all evaluated 8B baselines. The evidence is promising but bounded by model-judge scoring, one model family, single-error injections, per-question nonpersistent repairs, small samples for several error types, and no reported latency or token-cost analysis.

## Problem

**Statement.** A wrong memory-dependent answer does not reveal whether the originating failure occurred while writing, updating, retrieving, or using memory. The paper asks how to attribute a failure to its source stage and repair it without access to the gold answer.

**Why it matters.** A corrupted record may be retrieved and cited as apparently valid support, allowing an early error to affect later questions. Repairing only the final answer can therefore leave the underlying faulty memory or retrieval path intact.

**Scope.** The work studies multimodal, multi-session question answering with versioned external memory. It covers stage attribution, controlled propagation analysis, self-diagnosis, and local repair on Mem-Gallery and MemLens, plus attachment to MuRAG and A-Mem.

## Method

The authors model the pipeline as Write, Update, Retrieve, and Answer. A needed fact is followed through record versions and retrieval to identify the earliest stage where correct input ceases to produce correct output. Offline, known errors are injected and replayed against fact-preserving controls while tainted records are tracked. At test time, MemDoctor uses the same MLLM as the memory system: it enumerates needed facts, checks stages backward from Answer, verifies each diagnosis against records, earlier versions, or retained images, applies a stage-specific repair, re-retrieves, and answers again.

### Key components

- A four-stage, intervenable memory pipeline and nine-error taxonomy, including multimodal-specific visual loss and visual misdescription.
- Source-stage attribution defined by the earliest break in a needed fact’s provenance chain.
- Controlled error injection paired with neutral edits to separate propagation effects from stochastic replay changes.
- Taint tracking through final memory, retrieval, citation, and answer correctness.
- Backward diagnosis: verify Answer evidence, search below the retrieval cutoff, inspect prior record versions, then attribute remaining omissions or consistent misstatements to Write.
- Stage-specific repair: re-answer, re-query, reconstruct an update, or rewrite a record from its source turns.
- A multi-round case file that records located facts, attempted repairs, changes, and resulting answers; unsupported proposals are rejected.

### Assumptions

- The memory system logs record versions, retrieval ranks, retained images, and provenance sufficient for inspection and repair.
- Facts needed for a question can be decomposed into a small set that the model can state and verify against stored evidence.
- The same MLLM can reliably judge whether a fact is present in a record or image, despite also having produced the memory and answer.
- Source turns remain available for Write repair, even though ordinary diagnosis does not directly receive them.
- Local evidence agreement is meaningful; a consistently wrong memory cannot be detected without contradictory or external evidence.

## Main claims

- **Memory failures should be attributed to the stage where a required fact’s provenance chain first breaks, rather than where the failure becomes visible.**
  - Evidence: [b00034-7a46a1ea55] “the source stage sq⋆ is the earliest faulty stage over the chains of all facts in Fq”; [b00015-e832834dde] “failures of a multimodal memory system can be attributed to the stage where they begin rather than the stage where they surface.”
- **MemDoctor performs self-diagnosis without a gold answer and accepts only diagnoses grounded in stored memory evidence.**
  - Evidence: [b00040-b4ad94bc0a] “g sees neither aq⋆, nor the evidence turns, nor whether a^q is correct”; [b00040-b4ad94bc0a] “every output must be supported by content that can be located in Vq—in a record, in an earlier version of it, or in a kept image”
- **Early memory errors can survive later operations and be cited as apparently valid evidence in a wrong answer.**
  - Evidence: [b00095-5505cf32c4] “wrong values can persist through memory updates and reach the answer as apparently valid evidence.”; [b00055-0a32a1c2b2] “the answer quotes a tainted record as evidence”
- **The diagnosis-and-repair loop is presented as reusable across memory backends with different supported stages.**
  - Evidence: [b00186-166e71e270] “The adapters expose only the operations each backend supports.”; [b00186-166e71e270] “the comparison tests the applicability of MemDoctor across different backend capabilities”

## Results

- **On Mem-Gallery, the reported 4B system rises from 72.71% to 75.63% after repair; it recovers 94 initial failures but damages 44 initially correct answers.**
  - Context: This is the strongest end-to-end result, but the net improvement combines beneficial and harmful repairs and is based on final answers scored by the paper’s judge protocol.
  - Evidence: [b00087-69e12d734a] “our memory system on a 4B backbone reaches 72.71%”; [b00087-69e12d734a] “MemDoctor raises accuracy to 75.63% (+2.92 points; mean judge score 0.740 to 0.771)”; [b00087-69e12d734a] “It recovers 94 of the 467 initial failures (20.1%) and breaks 44 of the 1,244 correct answers (3.5%)”
- **On MemLens, repair increases reported accuracy from 51.8% to 55.4%, while the strongest evaluated 8B baseline reaches 46.7%; repair recovers 10 failures and breaks 3 correct answers.**
  - Context: The smaller backbone already leads the evaluated baselines before repair, so this comparison supports the full system but does not isolate repair from the authors’ underlying memory design.
  - Evidence: [b00093-23dbeacb84] “our 4B memory system reaches 51.8%, above every 8B baseline (the strongest, V-Mem, reaches 46.7%).”; [b00093-23dbeacb84] “MemDoctor reaches 55.4% (+3.6 points), 8.7 points above V-Mem.”; [b00093-23dbeacb84] “It recovers 10 of the 94 initial failures (10.6%) and breaks 3 of the 101 correct answers (3.0%).”
- **Controlled propagation shows a strong distortion effect: failure rate increases by 43 points over control, 80% of distortions remain in memory, and tainted records are cited in 97% of wrong answers.**
  - Context: Matched controls strengthen causal interpretation, although the same large model family participates as memory system, editor, and judge in this analysis.
  - Evidence: [b00095-5505cf32c4] “Distortions increase the failure rate by 43 points over the control, and the tainted record is cited in 97% of the wrong answers.”; [b00095-5505cf32c4] “By the end of the dialogue, 80% of distortions remain in memory”
- **Redundancy materially moderates distortion harm: the increase is 68 percentage points without alternative evidence and 10 points when another record or retained image supports the answer.**
  - Context: This supports the mechanism that errors are most consequential when they corrupt the sole evidence path, rather than merely showing that any edited record causes failure.
  - Evidence: [b00096-4b67e699ce] “distortions increase the failure rate over the control by 68 percentage points when no alternative evidence is available, compared with 10 points”; [b00170-19988b2a6a] “Redundant: after the edit, other records or the images still attached still answer the target question.”
- **As an attachment to existing backends on MemLens, MemDoctor improves MuRAG from 44.10% to 51.79% and A-Mem from 43.59% to 47.69%, exceeding the corresponding Reflexion results of 48.72% and 45.64%.**
  - Context: This is the most direct comparison with a generic reflection baseline, although the paper notes that answer conditioning and action selection are not isolated.
  - Evidence: [b00196-e00503a08c] “MemDoctor improves overall MuRAG accuracy from 44.10% to 51.79% (+7.69 points) and A-Mem from 43.59% to 47.69% (+4.10 points).”; [b00196-e00503a08c] “The corresponding Reflexion results are 48.72% and 45.64%.”

## Experimental evaluation

### Datasets

- Mem-Gallery: multimodal multi-session conversations; the main comparison covers all 20 scenes and 1,711 questions.
  - Evidence: [b00074-1479e58afd] “Mem-Gallery (Bei et al., 2026) consists of multimodal multi-session conversations, each a scene with its own question set.”; [b00076-c68f9506c5] “all 20 Mem-Gallery scenes (1,711 questions)”
- MemLens: the 195-question agent subset at 32K history length, with memory rebuilt independently for each question.
  - Evidence: [b00074-1479e58afd] “MemLens (Ren et al., 2026) gives each question its own history, so memory is built once per question; we use its 195-question agent subset at the 32K length.”

### Baselines

- Six external baselines: TextRAG, MuRAG, A-Mem, Mem0, Omni-SimpleMem, and V-Mem, all using Qwen3-VL-8B-Instruct for answering.
  - Evidence: [b00182-b2324d02ea] “We evaluate six baselines—TextRAG, MuRAG, A-Mem, Mem0, Omni-SimpleMem, and V-Mem”; [b00182-b2324d02ea] “All six use Qwen3-VL-8B-Instruct for answering”
- The authors’ unrepaired 4B memory system is the paired baseline that isolates the incremental effect of MemDoctor in the main tables.
  - Evidence: [b00080-d5d33dc16c] “We also report the initial answers of our own 4B memory system before repair (Ours w/o repair).”
- For backend attachment, Reflexion receives the same trace representation and common control rules, but rewrites queries and re-answers without stage localization or memory editing.
  - Evidence: [b00189-b9d97008e9] “Reflexion and MemDoctor receive the same trace representation and share the non-stage control rules.”; [b00189-b9d97008e9] “Reflexion rewrites queries and re-answers without stage localization or memory editing.”

### Metrics

- Accuracy; on Mem-Gallery, mean judge score is also reported.
  - Evidence: [b00084-e922cac2ca] “We report accuracy, and on Mem-Gallery also the mean judge score”
- Localization accuracy against the source stage.
  - Evidence: [b00084-e922cac2ca] “localization accuracy against the source stage”
- Net repair gain, which subtracts correct answers damaged by repair from incorrect answers fixed by repair.
  - Evidence: [b00045-74ed6db1df] “Grepair=1|𝒬|​∑q∈𝒬(cq′−cq)=N0→1−N1→0|𝒬|”; [b00046-aff0a9ecf9] “where N1→0 counts answers that repair damaged”
- Propagation excess failure rate relative to a fact-preserving control edit, with confidence intervals reported for injected errors.
  - Evidence: [b00042-1ebd95ae04] “an injected error of type ε is compared with a neutral edit at the same place that preserves every fact”; [b00071-bf043af737] “Δ: paired difference in points (95% CI over scenes).”

### Ablations

- With versus without self-diagnosis and repair on the authors’ 4B memory system.
  - Evidence: [b00068-62c0012ab7] “Small numbers next to Ours give the change from Ours w/o repair, in points.”
- Trajectory-level one-call diagnosis versus simple step-by-step re-answering versus an early stage-wise diagnoser.
  - Evidence: [b00162-487745d991] “its repairs recovered no more failures than answering again with step-by-step analysis (32% vs. 31% of the failures that are not yes/no questions).”; [b00162-487745d991] “A first stage-wise version, which checked one stage at a time, recovered 60%”
- Injected errors split by whether alternative evidence remains available.
  - Evidence: [b00168-003a298590] “Table 5 splits the accepted injections of Table 3 by whether the memory can still answer the target question after the edit”
- Backend attachment compared against original answers and Reflexion.
  - Evidence: [b00189-b9d97008e9] “We compare the original answers, Reflexion (Shinn et al., 2023), and MemDoctor.”

### Negative results

- Repair harms some task categories on Mem-Gallery, particularly answer refusal, knowledge resolution, and factual retrieval.
  - Evidence: [b00087-69e12d734a] “answer refusal (−4.3), knowledge resolution (−2.5) and factual retrieval (−0.5) lose slightly.”
- Retrieval distraction shows no observed excess failure over its control.
  - Evidence: [b00096-4b67e699ce] “Retrieval distraction produces no observed increase in failures (8% under both conditions, over 320 injections).”
- Multi-session reasoning remains unchanged in backend attachment because aggregate answers are not stated in a single record.
  - Evidence: [b00202-d7942afa8d] “On multi-session reasoning, accuracy is unchanged under both methods, since a count or a sum over several sessions is stated in no single record.”
- Without feedback, consistent distortions are frequently accepted as supported memory.
  - Evidence: [b00104-abfc2586c5] “without feedback the model finds nothing wrong in two thirds of the injected distortions.”


## Limitations

- The propagation study injects one error at a time and does not test interacting or compound errors.
  - Evidence: [b00104-abfc2586c5] “Our propagation analysis plants one error at a time, so it shows how a single error travels through memory but not how several errors interact”
- Evidence-grounded diagnosis cannot detect an error consistently repeated across every record and version when no retained image contradicts it.
  - Evidence: [b00104-abfc2586c5] “when every record and every version states the same wrong value and no kept image contradicts it, every check grounded in memory passes”
- Checking every answer adds inference calls and can overturn correct answers and refusals.
  - Evidence: [b00106-eb273d998e] “on Mem-Gallery, 3.5% of the correct answers are broken, and answer refusal loses 4.3 points”; [b00106-eb273d998e] “Checking every answer also adds model calls to every question.”
- Repairs are discarded between questions, so the evaluation does not establish durable benefits or cumulative corruption risk.
  - Evidence: [b00108-b3da1c88ac] “a repair made for one question is discarded before the next”; [b00108-b3da1c88ac] “we do not measure whether a repaired record also helps later questions, or whether repairs accumulate new errors over time.”
- Several visual and update propagation estimates have very small accepted samples.
  - Evidence: [b00096-4b67e699ce] “Visual and update errors have fewer accepted injections, with only 11–12 cases per type.”
- The same model family occupies multiple roles, and the propagation analysis uses the same model as memory system, editor, and judge, raising correlated-error concerns.
  - Evidence: [b00076-c68f9506c5] “The propagation analysis (Table 3) uses Qwen3-VL-30B-A3B-Instruct as the memory system, the editor that injects errors and the judge.”
- The plug-in comparison does not isolate stage localization from reflection-conditioned answering and action selection.
  - Evidence: [b00204-5c6e1d27e2] “the comparison therefore measures the combined effects of action selection and answer conditioning, rather than isolating stage localization.”

## Reproducibility

**Status:** partial

The paper provides unusually detailed procedural descriptions and says its prompts are reproduced verbatim, which supports reimplementation. Independent replication remains incomplete without code, exact inference settings, raw outputs, and repeated-run uncertainty. Reproducibility is therefore partial rather than strong.

**Available artifacts**

- The document states that MemDoctor prompts are listed verbatim in Appendix D.
- Memory-system prompts are identified in Appendix E.
- Error-injection prompts and acceptance/control procedures are described in Appendix F and Appendix B.
- Benchmarks, model variants, retrieval budgets, judging rules, round limits, and error-injection protocols are specified.

**Missing pieces**

- No code repository or executable implementation is identified in the supplied material.
- No random seeds, decoding parameters, hardware configuration, runtime, token usage, or monetary cost are reported in the supplied blocks.
- No repeated-run variance is reported for the main end-to-end comparisons; the attachment table explicitly describes one observed run.
- The supplied blocks do not provide raw predictions, complete trajectories, injected-edit files, or per-question scores.
- Exact benchmark versions or immutable dataset snapshots are not specified in the supplied material.

## AIDB assessment

- Novelty: The distinctive contribution is not generic reflection, but a provenance-based decomposition of multimodal memory failures into intervenable stages, coupled to backward, evidence-verified self-diagnosis and stage-specific repair. Controlled taint-style propagation analysis is also a useful methodological contribution.
- Usefulness: High for researchers building auditable multimodal memory agents: the taxonomy, logging requirements, matched-control injection design, net repair metric, and explicit accounting of damaged correct answers are directly reusable. Production usefulness is not yet established because persistent repairs, cost, latency, and compound-error behavior remain untested.
- Confidence: medium
- Recommended action: read
- Rationale: The paper presents coherent mechanisms and multiple controlled comparisons, including an unrepaired paired baseline, Reflexion, propagation controls, and two external backends. The reported improvements are meaningful, but confidence is moderated by model-judge dependence, a single model family, small samples for some injected errors, one-run reporting, nonpersistent repairs, and absence of cost analysis.

## Uncertainties

- **It is unclear how much of the gain comes from correct source-stage localization versus additional inference, verified-fact prompting, or reflection-conditioned re-answering.** — Without a factorial comparison, adopters cannot know which component justifies the added complexity and inference cost.
  - Evidence: [b00204-5c6e1d27e2] “the comparison therefore measures the combined effects of action selection and answer conditioning, rather than isolating stage localization.”
- **Judge and system errors may be correlated because Qwen3-VL variants are used throughout construction, diagnosis, editing, and evaluation.** — Shared inductive biases could overstate both edit validity and final-answer gains, especially for ambiguous multimodal questions.
  - Evidence: [b00076-c68f9506c5] “The propagation analysis (Table 3) uses Qwen3-VL-30B-A3B-Instruct as the memory system, the editor that injects errors and the judge.”
- **The long-run effect of retaining repaired records is unknown.** — A repair layer for persistent agent memory must demonstrate that benefits transfer to later questions without accumulating new corruption.
  - Evidence: [b00108-b3da1c88ac] “we do not measure whether a repaired record also helps later questions, or whether repairs accumulate new errors over time.”
- **Performance under multiple simultaneous or mutually reinforcing errors is unresolved.** — Real memory stores may contain correlated failures that defeat evidence-consistency checks and invalidate single-error propagation estimates.
  - Evidence: [b00104-abfc2586c5] “it shows how a single error travels through memory but not how several errors interact”

## Open questions

- Does MemDoctor retain a net benefit when repaired records persist across an entire conversation or user lifetime?
- How does performance change with independent model families for diagnosis, repair, and judging?
- What fraction of the improvement remains after matching baselines for model calls, token budget, and retrieval depth?
- Can diagnosis represent compositional evidence—counts, sums, comparisons, and temporal intervals—rather than searching for one stored fact?
- How robust is the method to several simultaneous errors, conflicting records, and consistently wrong source memories?
- What are the latency, token, and monetary costs per corrected answer, and can selective triggering preserve gains while reducing damaged correct answers?

## Proposed AIDB experiments

- **Hypothesis:** Persistent, provenance-checked repairs improve later questions about the same entity without causing an unacceptable accumulation of new errors.
  - Baseline: The evaluated policy that discards every repair before the next question, plus the unrepaired memory system.
  - Primary metric: Conversation-level net repair gain across subsequent questions, reported with corrected answers, damaged correct answers, and persistent record corruption rate.
  - Stop condition: Reject persistent repair if its confidence interval for conversation-level net gain includes zero or if cumulative damaged-correct-answer rate exceeds the nonpersistent policy.
- **Hypothesis:** Stage localization provides benefit beyond extra inference and reflection-conditioned re-answering.
  - Baseline: A compute-matched factorial set: re-answer only, generic reflection, verified-fact prompting without stage actions, stage actions without reflection conditioning, and full MemDoctor.
  - Primary metric: Accuracy gain per additional model call, with source-stage localization accuracy as a secondary metric.
  - Stop condition: Reject the incremental value of stage localization if full MemDoctor does not outperform the strongest compute-matched non-localizing variant with a confidence interval excluding zero.
- **Hypothesis:** Independent diagnosis and judging reduce correlated acceptance of consistently wrong memory evidence and improve distortion detection.
  - Baseline: The paper’s same-family configuration using Qwen3-VL variants for the memory system, diagnosis, editing, and judging.
  - Primary metric: Distortion source-stage localization accuracy under no feedback, stratified by redundant versus sole evidence, with independently adjudicated answer accuracy.
  - Stop condition: Reject the hypothesis if cross-family diagnosis fails to improve localization or increases the rate of damaged initially correct answers enough to eliminate net repair gain.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:40:56.290532+00:00`
- Document SHA-256: `444eb097bc5de1bd57debbeae5051b5470568b89222c06a1d422c960a05dd87d`
- Metadata SHA-256: `b699e19642ce171a4864d4fbc95742dd2d4c387d16357660c7d2174d0bd6650a`
- Blocks: 220
- Deterministic repair attempts: 1
