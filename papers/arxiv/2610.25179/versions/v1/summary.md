# Memory, Know Your PLACE: Governing Lifecycle State and Query-Time Eligibility in Persistent-Memory Agents

## Executive summary

PLACE separates persistent-memory governance into write-side state certification (CSS) and read-side query authorization (QASC). A controlled factorial study on Mem0 reports that CSS makes the evaluated stored state fully correct at both Qwen2.5 scales, while QASC removes measured leakage when paired with a correct state. The combination gives the best joint success and preserves all measured required support. The causal factorization is thoughtful, but evidence comes from one prespecified long trajectory, trusted semantic inputs, one backend, and two sizes of one model family. The paper therefore supports the mechanism under its constructed setting, not broad deployment reliability.

## Problem

**Statement.** Persistent-memory systems may preserve obsolete or contradictory facts, or allow memory that is ineligible for a particular query to affect an answer. Final-answer quality alone cannot distinguish a storage-state failure from a query-time influence failure.

**Why it matters.** Persistent errors can survive across sessions and affect later behavior. A system may also produce a correct answer despite an incorrect backend state, so answer accuracy or retrieval quality alone is an inadequate safety and reliability diagnostic.

**Scope.** The paper studies two controls: correctness of the semantic state physically maintained over lifecycle updates, and correctness of the subset of represented memory allowed to influence a query. It evaluates these controls on Mem0 with two Qwen2.5 model scales.

## Method

PLACE is a factorized layer around an unchanged memory backend and answer model. CSS accepts a trusted user-level update event, derives a governed state transition, realizes it through backend operations, and verifies the physical state through semantic readback. QASC applies entity, predicate, scope, temporal, and lifecycle eligibility constraints before context-budget truncation, exposing only authorized support. A two-by-two design crosses Native or CSS writing with Native or QASC reading, producing Native, CSS, QASC, and PLACE conditions while sharing producer states across the relevant read-policy pairs.

### Key components

- Physical-state readback maps only backend-evidenced records into semantic facts; a separate reference state is reserved for evaluation.
- CSS governs write-side state formation from a previous governed state and a trusted user-level event, then verifies the realized backend state.
- QASC is a deterministic, read-only authorization policy over physically represented memory; it cannot repair missing stored facts.
- The factorial design isolates write effects by comparing Native with CSS and read effects by comparing conditions sharing the same producer state.
- Causal leakage pairs hold the query and correct authorized state fixed while changing only irrelevant history.
- Utility and closed-loop diagnostics examine support preservation, inappropriate exposure, conflicting evidence, and retained assistant responses.

### Assumptions

- User-level update intent and query semantics are trusted rather than inferred end to end.
- Evaluator semantic readback faithfully represents only facts physically evidenced in storage.
- The reference state and authorization semantics used by evaluation are correct.
- Paired read-policy conditions receive identical producer states; otherwise the read-side comparison is invalid.
- Assistant responses retained in the closed-loop diagnostic are treated as non-authoritative context.

## Main claims

- **The paper's central conceptual claim is that reliable persistent memory requires separate but complementary controls over maintained state and query-time influence.**
  - Evidence: [b00008-62a38b357d] “We argue that reliable persistent memory requires governance over two distinct but complementary problems.”; [b00062-3aa6971be6] “state correctness and influence correctness are distinct but complementary requirements for reliable persistent memory”
- **CSS is intended to prevent stale or conflicting stored states by governing state transitions, realizing them in the backend, and verifying physical readback.**
  - Evidence: [b00026-c85bdaa716] “CSS prevents stale or conflicting states from persisting”; [b00030-6ab3fbab1a] “CSS then derives the required state change, realizes Gt through backend operations, and verifies resulting physical state through Eq. 1.”
- **QASC authorizes memory before truncation and is unable to reconstruct information missing from physical storage.**
  - Evidence: [b00032-bec2b971fc] “Authorization precedes context-budget truncation, preventing an ineligible item from reaching the answer model merely because it ranks highly under retrieval.”; [b00022-eb90c44732] “read-side governance can filter represented information but cannot reconstruct facts absent from physical memory.”
- **The evaluation is designed to isolate write-side and read-side contributions by crossing two write policies with two read policies and sharing producer states between paired conditions.**
  - Evidence: [b00036-c1ec5c0770] “We cross Native and CSS writing with Native and QASC reading, yielding Native, CSS, QASC, and PLACE.”; [b00036-c1ec5c0770] “Native and QASC share the same Native-produced state, while CSS and PLACE share the same CSS-produced state.”

## Results

- **CSS raised StateCorrectness from 0.488 to 1.000 for 7B and from 0.414 to 1.000 for 3B; the corresponding StateGain values were 0.512 and 0.586.**
  - Context: This is the primary write-side comparison. The reported factorization check covered all 153 semantic checkpoints and found the expected producer-state matches, supporting attribution to state formation rather than retrieval policy.
  - Evidence: [b00054-dbc729af82] “StateCorrectness increases from 0.488 to 1.000 at 7B and from 0.414 to 1.000 at 3B, corresponding to StateGain values of 0.512 and 0.586, respectively.”; [b00054-dbc729af82] “The factorization check also holds across all 153 semantic checkpoints, with Native matching QASC and CSS matching PLACE at both model scales.”
- **Within the state-correct CSS-versus-PLACE contrast, LeakageRate fell from 0.125 to 0.000 for 7B and from 0.083 to 0.000 for 3B. The reported 95% intervals for LeakageDrop were [0.042,0.229] and [0.021,0.167].**
  - Context: This is the cleanest read-side causal contrast because both conditions realize the reference-correct state and differ only in read policy. It establishes zero observed leakage in this finite test, not a universal zero leakage rate.
  - Evidence: [b00056-a23903d55f] “LeakageRate decreases from 0.125 to 0.000 at 7B and from 0.083 to 0.000 at 3B”; [b00056-a23903d55f] “with 95% pair-bootstrap intervals of [0.042,0.229] and [0.021,0.167] for LeakageDrop.”
- **PLACE preserved 1.000 NeededSupport at both model scales while reducing ExposureRate to 0.000.**
  - Context: The utility diagnostic argues against the trivial explanation that leakage was removed by suppressing all memory. The conclusion remains limited to the measured support and exposure probes.
  - Evidence: [b00057-9f00e529f6] “PLACE preserves 1.000 NeededSupport at both model scales while reducing ExposureRate to 0.000.”; [b00057-9f00e529f6] “preserving all measured query-required support.”
- **PLACE achieved JointSuccess of 0.667 for 7B and 0.625 for 3B, versus 0.417 and 0.354 for CSS. InteractionGain was 0.250 and 0.271, with sensitivity intervals [0.060,0.377] and [0.069,0.377].**
  - Context: The combined control was strongest on the strict joint endpoint. The authors appropriately characterize this as evidence consistent with complementarity, not population-level statistical synergy.
  - Evidence: [b00059-cbf54091cf] “PLACE reaches a JointSuccess of 0.667 at 7B and 0.625 at 3B, compared with 0.417 and 0.354 for CSS, respectively”; [b00059-cbf54091cf] “InteractionGain is 0.250 at 7B and 0.271 at 3B, with sensitivity intervals of [0.060,0.377] and [0.069,0.377].”; [b00059-cbf54091cf] “evidence consistent with complementarity rather than as population-level statistical synergy.”
- **In the closed-loop diagnostic, PLACE retained StateCorrectness of 1.000 and ExposureRate of 0.000 at both scales, while JointSuccess was 0.667 for 7B and 0.458 for 3B.**
  - Context: This diagnostic retains earlier assistant responses as non-authoritative context. The lower 3B joint result relative to the primary evaluation shows that perfect governed state and exposure control do not guarantee correct final answers.
  - Evidence: [b00060-bcfb042396] “PLACE maintains StateCorrectness of 1.000 and ExposureRate of 0.000 at both model scales, with JointSuccess of 0.667 at 7B and 0.458 at 3B.”

## Experimental evaluation

### Datasets

- Primary constructed benchmark: one prespecified 302-turn trajectory across four conversations, retaining persistent memory over resets, with 105 state checkpoints and 48 queries from six governance families.
  - Evidence: [b00037-bb15ffa1cc] “Experiments use one prespecified 302-turn trajectory spanning four conversations, with persistent memory retained across session resets.”; [b00037-bb15ffa1cc] “It contains 105 state checkpoints and 48 queries across six governance families.”
- Read-side causal evaluation: 48 paired cases in which query and authorized state are fixed and only irrelevant history changes.
  - Evidence: [b00037-bb15ffa1cc] “48 causal pairs that hold the query and authorized state fixed while varying only irrelevant history.”
- Utility diagnostic: 72 probes covering required support, inappropriate exposure, and conflicting evidence; Closed Loop retains prior assistant responses as non-authoritative context.
  - Evidence: [b00038-6ee145a538] “Utility evaluates needed support, inappropriate exposure, and conflicting evidence over 72 probes.”; [b00038-6ee145a538] “Closed Loop repeats the factorial setting while retaining prior assistant responses as non-authoritative dialogue context.”

### Baselines

- Native Mem0 writing with Native reading, using the same model for memory updates and answer generation.
  - Evidence: [b00035-f909453718] “The same model drives Native memory updates and answer generation”; [b00036-c1ec5c0770] “yielding Native, CSS, QASC, and PLACE.”
- CSS-only condition: governed writing with Native reading.
  - Evidence: [b00036-c1ec5c0770] “We cross Native and CSS writing with Native and QASC reading”
- QASC-only condition: Native-produced state with governed reading.
  - Evidence: [b00036-c1ec5c0770] “Native and QASC share the same Native-produced state”

### Metrics

- StateCorrectness: semantic F1 between physical-state readback and the reference state across checkpoints.
  - Evidence: [b00040-84575caf7e] “Across the C=105 state checkpoints, we compute”; [b00041-bbdb46207f] “StateCorrectness=1C​∑c=1CF1​(Scphys,Sc⋆). (4)”
- LeakageRate: probability that semantic answer outcomes differ across paired worlds, conditional on both realizing the same reference-correct authorized state.
  - Evidence: [b00045-1fc1ef5bfa] “LeakageRate=Pr⁡(Ω(a)≠Ω(b)∣Qeval(a)=Qeval(b)=Q⋆) (5)”
- AnswerCorrectness: deterministic semantic F1 over generated answers.
  - Evidence: [b00047-79785441ff] “AnswerCorrectness is deterministic semantic F1 over generated answers.”
- JointSuccess: requires correct persistent state and authorized support, retained required support, no governance violation, and a correct final answer.
  - Evidence: [b00047-79785441ff] “JointSuccess is stricter and requires the persistent state and authorized support to be correct, required support to remain available, no governance violation to occur, and the final answer to be correct.”
- Utility metrics: NeededSupport, ExposureRate, and ConflictHarm.
  - Evidence: [b00048-456f4f11e1] “NeededSupport measures whether query-required memory remains visible to the answer model, while ExposureRate measures whether ineligible memory is exposed.”; [b00048-456f4f11e1] “ConflictHarm records whether injected conflicting evidence contributes to an incorrect answer.”

### Ablations

- Two-by-two mechanism ablation comparing Native, CSS-only, QASC-only, and combined PLACE.
  - Evidence: [b00036-c1ec5c0770] “We cross Native and CSS writing with Native and QASC reading, yielding Native, CSS, QASC, and PLACE.”
- Closed-loop diagnostic adds retained assistant responses while preserving the factorial setting.
  - Evidence: [b00038-6ee145a538] “Closed Loop repeats the factorial setting while retaining prior assistant responses as non-authoritative dialogue context.”

### Negative results

- QASC alone does not improve the incorrect Native physical state because it is read-only.
  - Evidence: [b00054-dbc729af82] “QASC does not change these values because it shares the Native state producer and does not modify persistent memory.”
- QASC alone cannot recover failures caused by incorrect stored state.
  - Evidence: [b00059-cbf54091cf] “QASC alone cannot recover failures caused by an incorrect Native state.”
- Native-versus-QASC provides fewer leakage-eligible pairs because write-side errors make their authorized states unsuitable for the primary read-side contrast.
  - Evidence: [b00056-a23903d55f] “The smaller eligible sets for Native and QASC arise from write-side state errors and are therefore not used as the primary read-side contrast.”


## Limitations

- The main benchmark is a single prespecified longitudinal trajectory, so checkpoint results are descriptive and do not support population-level inference.
  - Evidence: [b00049-e5e85f643a] “the primary benchmark contains one prespecified four-conversation trajectory”; [b00049-e5e85f643a] “longitudinal results are reported descriptively with conversation-block sensitivity intervals rather than population-level inference.”
- Governance receives trusted user-level event and query semantics; the experiment does not test end-to-end automatic interpretation, which may introduce additional errors.
  - Evidence: [b00062-3aa6971be6] “Our current evaluation isolates governance using trusted user-level semantics rather than end-to-end automatic interpretation.”
- External validity is narrow: the supplied evaluation covers Mem0 and two sizes of the Qwen2.5 family, not diverse backends, model families, domains, or naturally occurring user histories.
  - Evidence: [b00035-f909453718] “We evaluate PLACE on Mem0 [1] with Qwen2.5-3B and Qwen2.5-7B [9] through Ollama, using Qdrant storage and Nomic embeddings.”
- Zero measured leakage is based on finite eligible causal pairs and should not be read as proof that leakage is impossible outside the tested cases.
  - Evidence: [b00056-a23903d55f] “both realize the reference-correct state for all 48 causal pairs”; [b00056-a23903d55f] “LeakageRate decreases from 0.125 to 0.000 at 7B and from 0.083 to 0.000 at 3B”
- Read-side governance cannot repair facts absent from physical storage, placing a hard ceiling on QASC-only performance.
  - Evidence: [b00032-bec2b971fc] “It cannot modify persistent state or recover information absent from the backend.”

## Reproducibility

**Status:** partial

The experimental structure and metric definitions are unusually explicit, and an artifact URL is stated. However, the supplied document blocks do not contain enough operational detail to establish exact reproduction. Reproducibility is therefore partial rather than strong.

**Available artifacts**

- The paper states that project materials are available online.
- The implementation stack is identified as Mem0, Ollama, Qdrant, Nomic embeddings, Qwen2.5-3B, and Qwen2.5-7B.
- The factorial conditions, trajectory size, checkpoint and query counts, causal-pair construction, metrics, and bootstrap resampling count are described.

**Missing pieces**

- The supplied blocks do not enumerate artifact contents, source-code version identifiers, dependency versions, model decoding parameters, prompts, hardware, random seeds, or exact runtime configuration.
- The supplied blocks do not provide the full trajectory, probe records, evaluator annotations, semantic readback implementation, eligibility rules, or answer-scoring implementation.
- No independent replication or human-validation results are reported.

## AIDB assessment

- Novelty: The main novelty is the explicit factorization of persistent-memory reliability into certified write-side state and authorized read-side influence, coupled with a factorial and paired-world evaluation that distinguishes state-mediated failures from causal leakage.
- Usefulness: High conceptual and diagnostic usefulness for memory-agent evaluation: it warns against treating final-answer accuracy or retrieval relevance as sufficient and supplies separable endpoints. Immediate production adoption is premature because semantic inputs are trusted and external validation is narrow.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled comparisons strongly support the paper's mechanism within its constructed benchmark, especially the state-correct CSS-versus-PLACE leakage contrast. Confidence is moderated by one trajectory, finite probes, a single backend, one model family, and the absence of end-to-end semantic interpretation or independent replication.

## Uncertainties

- **It is unclear how robust CSS and QASC remain when update intent, entity identity, temporal scope, lifecycle status, or query semantics must be inferred automatically.** — The trusted semantics remove a likely source of real-world governance errors; mistakes upstream could corrupt state transitions or authorization decisions.
  - Evidence: [b00062-3aa6971be6] “using trusted user-level semantics rather than end-to-end automatic interpretation.”
- **The generality of the observed gains across independent histories, users, domains, backends, and model families is unresolved.** — The present design treats two sizes of one family as scale replications but does not establish broad external validity.
  - Evidence: [b00049-e5e85f643a] “Results from Qwen2.5-3B and Qwen2.5-7B are treated as model-scale replications.”; [b00037-bb15ffa1cc] “one prespecified 302-turn trajectory spanning four conversations”
- **The reliability and independence of deterministic semantic answer scoring and evaluator-side state readback are not established in the supplied blocks.** — Both primary endpoints depend on semantic mappings; evaluator error could alter apparent correctness or leakage.
  - Evidence: [b00019-69ad5b14be] “where β maps only physically evidenced records to semantic facts and cannot introduce unsupported values.”; [b00047-79785441ff] “AnswerCorrectness is deterministic semantic F1 over generated answers.”
- **The operational cost, latency, failure recovery, and scalability of certified writes and per-query authorization are unreported.** — A governance layer may be accurate in a benchmark yet impractical for long-running production agents.
  - Evidence: [b00026-c85bdaa716] “PLACE (Persistent-memory Lifecycle Alignment and Contextual Eligibility) adds governance at the write and read boundaries of an existing persistent-memory system”

## Open questions

- How accurately can learned semantic interpretation recover trusted update and query semantics, and how do its errors propagate separately into CSS and QASC?
- Do the factorial effects replicate over independently sampled long-horizon trajectories with human-validated states, eligibility decisions, and answers?
- How does PLACE perform with other memory backends, embedding systems, retrieval strategies, model families, and domains?
- What are the added write latency, query latency, storage overhead, and recovery behavior under backend failures or concurrent updates?
- How sensitive are the conclusions to alternative semantic readback functions, authorization policies, and human adjudication of answer equivalence?

## Proposed AIDB experiments

- **Hypothesis:** PLACE with automatically inferred semantics retains most of the joint-governance benefit of PLACE with trusted semantics, and interpretation errors can be localized to write or read decisions.
  - Baseline: Trusted-semantics PLACE, Native Mem0, CSS-only, and QASC-only on the same independently sampled trajectories.
  - Primary metric: JointSuccess, supplemented by semantic-interpretation accuracy and separate write-transition and authorization error rates.
  - Stop condition: Stop after a preregistered trajectory count is complete; reject practical equivalence if the lower confidence bound for automatic-versus-trusted JointSuccess falls below the prespecified non-inferiority margin.
- **Hypothesis:** The write-side and read-side gains replicate across independent trajectories, domains, memory backends, and model families rather than being specific to the reported configuration.
  - Baseline: Native operation for each backend-model combination, with the same factorial CSS-only, QASC-only, and PLACE conditions.
  - Primary metric: Mean paired PLACE-minus-Native JointSuccess across independently sampled trajectories, with StateCorrectness and LeakageRate as mechanism checks.
  - Stop condition: Stop at the preregistered sample size; withhold adoption if the gain changes sign across most backend-model strata or if state matching fails in any primary read-policy comparison.
- **Hypothesis:** QASC continues to block ineligible influence under adversarially ranked, semantically similar, temporally stale, or scope-conflicting memories without removing required support.
  - Baseline: Native reading and a relevance-only filter, both operating on the same CSS-certified physical states.
  - Primary metric: LeakageRate on eligible paired worlds, jointly constrained by NeededSupport.
  - Stop condition: Stop when the preregistered adversarial suite is exhausted; reject the hypothesis if any attack family produces leakage above the declared safety threshold or NeededSupport below the declared utility threshold.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:37:16.434870+00:00`
- Document SHA-256: `81cced3649a3f663453bee970f6142faf186b5ad39a39b900f4c787cde9ede6d`
- Metadata SHA-256: `2d3a18975958e55efe4b300e6ac18d7d7b1845d8e38e29c0584228a7601d37b5`
- Blocks: 84
- Deterministic repair attempts: 0
