# LEDGER: Auditable Agent Memory Under Change

## Executive summary

LEDGER separates fallible language-model extraction and routing from deterministic rules for supersession, source trust, temporal validity, and deletion; LEDGER+EP optionally retrieves scrubbed raw turns. Its strongest evidence is on an author-built synthetic coding workload: fallback substantially improves answer accuracy over full replay while exposing far fewer forbidden values and no deleted values in evaluated description-only deletion probes. Held-out seeds preserve but reduce the advantage. On LongMemEval, augment matches full replay’s observed accuracy with much less context, but confidence intervals do not establish equivalence or superiority. The design is promising for auditable memory, yet downstream agent utility, real-world deletion safety, delayed facts, broader models, and independent workloads remain unvalidated.

## Problem

**Statement.** Persistent agent memories must decide which changing fact is current, resolve conflicts between sources of unequal reliability, answer historical questions, abstain when evidence is absent, and honor deletion without resurfacing erased values.

**Why it matters.** Answer-only evaluation can conceal unsafe evidence: a model may select the right answer from stale or conflicting context, while deleted information has still been disclosed to the answering provider.

**Scope.** The paper studies single-current-value facts in English coding-agent sessions and LongMemEval chats. It evaluates evidence packets and question answers, not an agent completing downstream software-engineering tasks.

## Method

A language-model extractor converts session events into slot-value claims and a router maps questions or deletion descriptions to known slots. A deterministic ledger core applies source-precedence, supersession, temporal-history, deduplication, abstention, and deletion rules. Each entry records validity, source kind, trust, and provenance. LEDGER+EP adds a BM25 episode store: fallback searches raw turns only when the ledger returns no fact, whereas augment always fills remaining context with turns. Deletion erases ledger records, retains value-free tombstones, blocks source events, and scrubs related episode turns.

### Key components

- Per-user entity/attribute slots containing value entries with validity intervals and event provenance.
- Five deterministic ingestion rules for restatement, trusted supersession, lower-trust disputes, trusted introduction, and unconfirmed low-trust claims.
- Lexical grounding and enumerated-event safeguards applied before ledger writes.
- Question and deletion routing over known slots, with explicit abstention reasons.
- A scrubbed raw-turn episode store using BM25 retrieval in fallback or augment mode.
- Evidence-level scoring that separately labels stale, future, contaminated, resurrected, and deleted values.

### Assumptions

- Extraction must produce the correct value and stable slot key and must avoid claims from questions, plans, or negations.
- Routing must find every relevant slot and no irrelevant slot; a missed deletion slot is a privacy failure.
- The configured source ranking must reflect actual reliability.
- Valid time begins when a value is stated; dates expressed inside text are not interpreted.
- The caller must supply the correct user identifier and all reads and deletions must use the partitioned interface.

## Main claims

- **The architectural contribution is a division of responsibility: language models propose and route facts, while fixed rules alone determine currency, trust conflicts, and deletion state.**
  - Evidence: [b00053-5dae3b6f24] “The ledger core applies fixed write rules to each claim, and it alone decides what is current, trusted or deleted.”
- **The evaluation is designed to audit both memory evidence and the answer produced by a shared answering model.**
  - Evidence: [b00020-e18f238676] “We introduce an evaluation protocol that audits both the evidence packet supplied to a fixed answering model and the resulting answer”
- **The claimed deletion guarantee is conditional rather than absolute because it depends on successful extraction and identification of affected slots.**
  - Evidence: [b00093-adb9c35d66] “This holds when the affected slots are found (A2) and the extractor captured the statements of the value (A1).”
- **Episode retrieval broadens recall but can reintroduce old or less-trusted content that bypasses ledger rules.**
  - Evidence: [b00061-04b32870c0] “Raw turns are not filtered by the rules, so they can carry an old or less trusted value”

## Results

- **On development coding seeds, LEDGER+EP fallback achieved 94.3 ± 4.2 answer accuracy, versus 82.1 ± 3.0 for full replay; its evidence contained forbidden values in 16 probes versus 249 for full replay.**
  - Context: This is the strongest controlled comparison, but it uses the development seeds on which the rules and safeguards were developed.
  - Evidence: [b00119-9a2f3124ac] “Full replay 82.1 ± 3.0 21.9 ± 1.8 65 249 (129/93/93)”; [b00119-9a2f3124ac] “Ledger+Ep fallback 94.3 ± 4.2 66.8 ± 4.6 10 16 (6/8/3)”
- **On held-out coding seeds, LEDGER+EP fallback scored 91.1 ± 5.4, while full replay scored 83.3 ± 2.8; the reported lead contracted to 7.8 points.**
  - Context: The held-out result preserves the ranking but shows that development results favored the proposed systems.
  - Evidence: [b00127-a0698dace9] “Full replay 83.3 ± 2.8 21.1 ± 0.7 58”; [b00127-a0698dace9] “Ledger+Ep fallback 91.1 ± 5.4 64.2 ± 4.8 15”; [b00128-75f073c710] “so its lead shrinks from 12.2 to 7.8 points.”
- **For description-only deletion requests, full replay exposed deleted values in 46 evidence probes and repeated them in 4 answers; Mem0 exposed them in 18 probes and 17 answers, whereas LEDGER and both LEDGER+EP modes exposed none in the evaluated probes.**
  - Context: This comparison applies only to the evaluated adapters: transcript baselines deleted only by event identifier, and Mem0 relied on its ordinary update step.
  - Evidence: [b00123-75e78e0368] “Full replay sends the deleted value to the model in 46 probes and repeats it to the user in 4”; [b00123-75e78e0368] “it reached the model in 18 probes and the user in 17”; [b00123-75e78e0368] “Ledger and Ledger+Ep sent no deleted value, in either mode.”
- **On the 210-question LongMemEval subset, LEDGER+EP augment and full replay both observed 74.8% accuracy; LEDGER+EP used 1,087 injected tokens, described as 1% of full replay’s context, but the paired 95% difference interval was −6.2 to +6.2 points.**
  - Context: The observation supports context compression, not statistical equivalence or superiority.
  - Evidence: [b00129-2c652fba7c] “LongMemEval_S, stratified subset of 210 questions (30 per category).”; [b00131-a70d9b6441] “Ledger+Ep (augment) has the same observed accuracy, 74.8%, with 1,087 injected tokens, 1% of the context.”; [b00131-a70d9b6441] “The paired 95% interval of the difference (−6.2 to +6.2 points) still allows a real difference of several points either way”
- **Across the simulated 540-day replay, full replay fell from 89.4% to 70.5%, while LEDGER stayed between 85.0% and 93.3% and LEDGER+EP fallback between 89.7% and 96.2%.**
  - Context: This tests growing facts and updates more strongly than truly long context because the histories remained comparatively short.
  - Evidence: [b00134-b5d4d0e079] “Fig. 2 replays 540 simulated days on the long preset, with eight checkpoints.”; [b00134-b5d4d0e079] “full replay falls from 89.4% to 70.5%”; [b00134-b5d4d0e079] “Ledger stays between 85.0% and 93.3%”; [b00134-b5d4d0e079] “Ledger+Ep (fallback) between 89.7% and 96.2%”

## Experimental evaluation

### Datasets

- Synthetic multi-user, multi-session coding-agent workload with planted state transitions, controlled source conflicts, deletions, six probe types, development and held-out seeds, plus a long replay preset.
  - Evidence: [b00098-ec32b656ef] “A seeded generator produces multi-user, multi-session coding-agent timelines.”; [b00098-ec32b656ef] “At checkpoints the generator asks probes of six types: current, post-update, historical (with an as-of time), contamination, post-delete and abstention.”
- A stratified LongMemEval_S subset containing 210 questions, sampled as 30 questions from each of seven categories.
  - Evidence: [b00104-ac54c6e398] “We group the questions into seven categories (six question types and abstention) and draw 30 from each”; [b00104-ac54c6e398] “210 questions; ids in the artifact”

### Baselines

- No memory; unbounded full-history replay; BM25 transcript RAG; Mem0 in its original and coding-prompt configurations; and a rule-based LEDGER extractor as a model-free floor.
  - Evidence: [b00108-6d6d02795b] “No memory; full replay (the whole history, unbounded); transcript RAG (BM25 over events, top 5, within the budget); Mem0 [10]”; [b00108-6d6d02795b] “Ledger with the LLM extractor and with a rule-based extractor”

### Metrics

- Answer accuracy and evidence accuracy, with verdicts for correct, polluted, wrong, missed, leaked, false abstention, and no abstention; forbidden values are typed as resurrected, stale, future, or contaminated.
  - Evidence: [b00110-2ef6ee640d] “Each probe of the coding workload is scored twice. The evidence verdict scores what memory sent to the model; the answer verdict applies the same rules”; [b00111-95d1ddddcb] “false abstention if the system abstained; otherwise correct”; [b00110-2ef6ee640d] “resurrected (stated before the last deletion), and after it stale (set before the target time), future (set after the as-of time) or contaminated”
- Efficiency metrics include injected tokens, write/read/answering cost, ingest and retrieval latency, model calls, and storage size.
  - Evidence: [b00113-a1620a154d] “We report write cost per session or history, read and answering cost per question, injected tokens, latency and store size.”

### Ablations

- Replacing the rule-based extractor with the language-model extractor raised evidence accuracy from 38.7 to 91.7, but changed the entire extraction method.
  - Evidence: [b00149-5e6b5b3efe] “Rule-based → LLM extractor evidence 38.7 91.7”; [b00151-bd7d22d1e4] “The extractor row changes the whole extraction method.”
- Adding the episode configuration raised answer accuracy from 90.9 to 94.3, but also changed low-trust-event extraction and therefore does not isolate the episode store.
  - Evidence: [b00149-5e6b5b3efe] “Ledger → Ledger+Ep fallback answer 90.9 94.3”; [b00151-bd7d22d1e4] “it does not isolate the episode store.”
- A single-factor trust change that also held document-first values reduced evidence accuracy from 91.5 to 89.7; the authors report that it cost correct answers without fixing errors.
  - Evidence: [b00149-5e6b5b3efe] “Hold document-first values too (trust 3)∗ evidence 91.5 89.7”; [b00150-101d79a953] “Holding documents as well (trust 3) costs nine correct answers and fixes none”

### Negative results

- The ledger alone performed poorly on LongMemEval because the benchmark often asks for isolated details outside its single-current-fact representation.
  - Evidence: [b00131-a70d9b6441] “The ledger alone answers only 41.0%: the benchmark mostly asks for one detail buried in unrelated chats”
- Fallback still produced forbidden answers from stale ledger facts and raw turns, while BM25 often failed to retrieve the needed turn.
  - Evidence: [b00146-536c046223] “Ten answers carry a forbidden value: four are the ledger’s own stale facts above, and six are old values taken from a raw turn.”; [b00146-536c046223] “mostly because BM25 did not find the right turn.”
- The final system lacks leave-one-out ablations for safeguards, trust ranking, the episode retriever, and token budget.
  - Evidence: [b00152-db0f2ffb03] “We did not run leave-one-out ablations of the final system, or ablate the trust ranking itself, the episode retriever or the token budget.”


## Limitations

- The primary coding workload, oracle, and system were co-developed, use templates, and encode the same trust policy; the experiment tests compliance with that policy rather than whether it is correct in real deployments.
  - Evidence: [b00099-b900820beb] “We wrote the workload, the oracle and Ledger together, and the workload encodes the same trust policy”; [b00099-b900820beb] “It therefore tests whether a memory follows this policy, not whether the policy is right (A3).”
- No downstream agent task was evaluated, so better memory evidence has not been shown to improve bug fixing, deployment, or other operational outcomes.
  - Evidence: [b00116-1b36d3c93d] “the main gap, no agent performs a downstream task.”
- Deletion does not cover prior snapshots, response caches, or run logs, and LEDGER+EP retains an open exposure case when extraction and lexical scrubbing both miss a trusted turn.
  - Evidence: [b00093-adb9c35d66] “One case remains open in Ledger+Ep: a trusted turn whose value the extractor missed”; [b00093-adb9c35d66] “Deletion does not reach earlier snapshots, the response cache or run logs”
- Episode scrubbing may remove useful information, but the resulting recall loss was not measured.
  - Evidence: [b00092-93ac720f4c] “Scrubbing more turns lowers the risk of exposure but can also remove useful details; we did not measure this loss of recall.”
- External validity is narrow: English text, templated facts, one main model family, and only one dedicated memory product baseline.
  - Evidence: [b00161-4bacef868b] “All extraction, routing and answering use one model family”; [b00161-4bacef868b] “all text is English.”; [b00161-4bacef868b] “Besides the baselines, we compare against one memory product, Mem0; Zep and A-MEM are not evaluated.”
- LongMemEval mode selection used a pilot overlapping the evaluation subset, and only part of the judge behavior was human-audited.
  - Evidence: [b00105-8ca86379a6] “Ten pilot questions are also in the 210, so mode selection saw part of the evaluation set”; [b00106-9fbf710c7d] “Mem0, Ledger and fallback mode were not audited”

## Reproducibility

**Status:** strong

The paper provides unusually extensive artifacts, fixed model snapshots, deterministic workload scoring, sampled identifiers, logs, caches, and per-seed outputs. Reproduction should be practical, although external model access and the lack of reported independent replication remain concerns.

**Available artifacts**

- Code
- Synthetic workloads and generator settings
- Pinned model snapshot and sampling settings
- On-disk response cache keyed by provider, model, prompt, and schema
- Pinned prices and cost breakdown
- Run logs and per-seed results
- Sampled LongMemEval identifiers and pilot analysis
- Supplement

**Missing pieces**

- Independent reproduction is not reported.
- The supplied document does not report immutable artifact commit hashes or archival identifiers.
- Provider-side determinism beyond cached responses is not guaranteed.
- Crash behavior during non-atomic snapshot writes was not tested.

## AIDB assessment

- Novelty: High at the evaluation-and-systems boundary: the central contribution is not a new storage primitive, but an auditable combination of temporal entries, source precedence, explicit deletion, evidence-level scoring, and scrubbed episodic fallback.
- Usefulness: Potentially high for agent systems where facts change and privacy-sensitive deletion matters. Fallback is the most defensible configuration for conflicting facts; augment is better suited to one-off conversational details but transfers correctness responsibility back to the answer model.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled evidence-level results, held-out seeds, cost accounting, and explicit failure taxonomy justify close study and replication. Adoption would be premature because the strongest advantage comes from a co-designed synthetic workload, deletion guarantees are conditional and incomplete across storage surfaces, and no downstream-agent benefit has been demonstrated.

## Uncertainties

- **Whether the fixed source hierarchy remains beneficial when documents or tools are more reliable than users in real repositories.** — The ledger deterministically enforces the hierarchy, so a mismatched policy can preserve an older incorrect value and reject a newer correct one.
  - Evidence: [b00083-5ec19051bb] “When this assumption is wrong, the policy fails in a known way: a newer and correct document cannot override an older user statement”
- **Whether delayed reports and dates embedded in natural language can be supported without breaking temporal correctness.** — The current implementation equates recording time with valid-time start, so retrospective updates are assigned the message timestamp.
  - Evidence: [b00048-baf4872edd] “We do not read dates written in the text.”; [b00048-baf4872edd] “A change reported late, such as “we migrated last Tuesday”, is therefore dated to the message that reports it.”
- **Whether equal observed LongMemEval accuracy persists on the full benchmark or under other question mixtures.** — The evaluated subset is balanced rather than representative of the benchmark mix, and the confidence interval permits meaningful differences in either direction.
  - Evidence: [b00112-79ceb6cb57] “accuracy describes the balanced subset, not the benchmark’s own mix.”; [b00131-a70d9b6441] “this is not evidence of equivalence.”
- **How much useful recall episode scrubbing sacrifices and whether the remaining open deletion case appears in realistic conversations.** — Privacy and recall are directly traded off, but only exposure—not lost utility from scrubbing—was measured.
  - Evidence: [b00092-93ac720f4c] “we did not measure this loss of recall.”

## Open questions

- Can source trust be learned or configured per domain while remaining auditable and resistant to manipulation?
- How should valid and recording time be separated when users report changes retrospectively?
- Can deletion be made end-to-end across snapshots, caches, logs, embeddings, backups, and provider requests?
- Does cleaner evidence improve success and safety on real multi-session coding tasks rather than checkpoint question answering?
- Which component causes the gain: deterministic rules, extraction quality, routing, episode retrieval, scrubbing, or their interaction?

## Proposed AIDB experiments

- **Hypothesis:** On real multi-session repository work, deterministic ledger evidence improves downstream task success and reduces regressions caused by stale configuration facts.
  - Baseline: Full replay and transcript RAG using the same agent, model, tools, task budget, and repositories.
  - Primary metric: Blindly graded downstream task success, paired with the rate of actions attributable to stale, conflicting, or deleted evidence.
  - Stop condition: Stop after the preregistered task set is complete, or earlier if a safety rule is violated; reject the hypothesis if the paired confidence interval does not exclude no improvement.
- **Hypothesis:** End-to-end deletion testing with adversarial paraphrases will reveal exposure paths not covered by slot routing and lexical episode scrubbing.
  - Baseline: Current LEDGER+EP deletion pipeline, compared with a stricter semantic scrubber and storage-wide deletion across snapshots, caches, logs, and indexes.
  - Primary metric: Deleted-value exposure rate across evidence, restored state, caches, logs, and answer outputs, plus retained-answer accuracy on unrelated facts.
  - Stop condition: Stop when the preregistered adversarial suite is exhausted; require zero observed exposure and a predefined bound on unrelated recall loss before considering the stronger pipeline acceptable.
- **Hypothesis:** Factorial ablation will show that deterministic conflict and temporal rules, rather than co-varying extraction changes, account for most of the coding-workload advantage.
  - Baseline: The final fallback configuration with extraction, routing, trust rules, episodic retrieval, scrubbing, and token budget independently removed or replaced.
  - Primary metric: Held-out evidence accuracy and answer accuracy, supplemented by stale, contaminated, deleted, and false-abstention rates.
  - Stop condition: Stop after all preregistered component combinations and independent workload seeds are evaluated; reject the hypothesis if rule removal does not cause the largest reproducible degradation.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:07.944210+00:00`
- Document SHA-256: `3f209bc3d1b371590c229bdae1ec03ae309324e0286dd14d83440a7e8449672c`
- Metadata SHA-256: `1ef1a6c98944ad7c9bac6719b1b1c478159b0dfa0ae13c408daaf283d2bb8bca`
- Blocks: 189
- Deterministic repair attempts: 0
