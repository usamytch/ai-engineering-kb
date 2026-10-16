# Contract Memory Compiler: Resolve, Then Traverse

## Executive summary

The paper identifies update-dependent evidence selection as a distinct failure mode in long-term agent memory: an updated relation can change which older record is needed downstream. CMC extracts provenance-linked relations offline, resolves each subject–relation key by source order, traverses the resulting current graph from entities explicitly named in a question, and renders original records for one answer-model call. Fixed-extraction controls strongly support the central ordering claim on FactConsolidation, and a constructed MQuAKE-MemStream test shows a similar effect. The evidence is unusually well controlled and artifact-rich, but external validity is limited by ordered, single-valued assertions, exact surface-form anchoring, a fixed traversal cap, development-grid use, constructed chronology, and partially unpinned reader infrastructure.

## Problem

**Statement.** Select the original memory records needed to answer a multi-hop question after later assertions have overwritten earlier relations, especially when an updated value introduces a downstream entity not named in the question.

**Why it matters.** Refreshing values inside evidence chosen from an earlier state cannot recover a newly relevant record that was omitted; this makes update resolution and evidence selection inseparable for multi-hop reading.

**Scope.** The demonstrated mechanism targets ordered assertion streams with last-write-wins, single-valued subject–relation keys and one bounded evidence-selection pass before a single answer-model call.

## Method

CMC compiles an ordered assertion history into a provenance-linked current graph before answering questions. At query time it anchors explicit subject strings, performs bounded breadth-first traversal over current edges, retrieves their original source records plus unresolved records, restores source order, applies an evidence budget, and invokes a frozen reader once.

### Key components

- Classify each source record as facts, unresolved, or no_fact; validate structured triples and retain source positions and original wording.
- Align equivalent relation slots and normalize entity keys while preserving unresolved records as residual evidence.
- Replay accepted assertions in source order and keep the latest edge for each normalized subject–relation key.
- Anchor graph subjects by whole normalized spans explicitly present in the question, preferring longer overlapping matches.
- Traverse every current outgoing edge breadth-first from the anchors through the bounded depth, allowing updated objects to redirect later evidence selection.
- Deduplicate supporting records by source position, restore source order, add unresolved records, and retain a newest contiguous suffix if the evidence budget overflows.
- Pass the rendered evidence and question to the reader in one generation call.

### Assumptions

- Source position provides the relevant recency order.
- Each modeled subject–relation key has one active value under last-write-wins semantics.
- Answer-bearing relations can be extracted or retained as unresolved source text.
- The question contains an explicit surface-form anchor matching a graph subject.
- Required support is reachable within the bounded traversal depth.
- The reader can choose the relevant relation from the potentially branching closure.
- The selected records fit the reader contract or remain useful after suffix clipping.

## Main claims

- **An update may change not only a value but also which downstream memory key and source record must be read.**
  - Evidence: [b00034-8c8bf0d4c1] “The second lookup must change from Room A’s floor to Room B’s floor.”
- **CMC resolves current relations before bounded traversal and returns the supporting original records for one reader call.**
  - Evidence: [b00038-ccdd4f1f3a] “For each question, it finds explicit subject anchors, traverses current outgoing edges up to five hops, and renders the supporting source records.”; [b00040-d0e89a12b2] “The selected facts are returned as original text, together with unresolved records, for one frozen-reader generation.”
- **The read contract guarantees currency and bounded graph coverage only for selected interpreted edges, not semantic completeness of unresolved text.**
  - Evidence: [b00032-c8c684e581] “Currency: every edge in Ch is the last-written parsed edge for its key.”; [b00032-c8c684e581] “Bounded graph coverage: every current outgoing edge in Gt from a subject reachable at depth less than h is included.”; [b00032-c8c684e581] “These graph properties do not assign versions to unresolved source text retained alongside the selected edges.”
- **The primary mechanism comparison holds extraction, reader, prompt, histories, and evidence cap fixed while changing the records shown to the reader.**
  - Evidence: [b00058-43d9813cf7] “Every view uses the same source histories, HY4-preview reader, prompt, and 60,000-character evidence cap; only the evidence presented to the reader changes.”
- **MQuAKE-MemStream is a controlled supplied-memory test rather than a test of parametric knowledge editing or unrestricted evidence discovery.**
  - Evidence: [b00081-ef103b0198] “Every method receives the answer-bearing support facts, so this is a controlled test of version resolution and evidence selection rather than the original model-editing task.”
- **The demonstrated contribution is deliberately narrower than adaptive pipelines that can perform additional reads or modify memory state.**
  - Evidence: [b00302-0cf3edeab4] “These policies can issue further reads or change their stored state; the CMC mechanism comparison holds source extraction and the answer call fixed.”

## Results

- **On FactConsolidation with shared extraction and the HY4-preview reader, CMC obtained 97.25% single-hop and 78.25% multi-hop accuracy with 185 mean input tokens and no clipped contexts.**
  - Context: Primary pooled comparison across the benchmark’s four history lengths.
  - Evidence: [b00060-13813e918c] “CMC 97.25 78.25 185 0”
- **Resolving updates before selecting evidence produced a 56.75-point multi-hop advantage over selecting keys from prior values and then refreshing them: 78.25% versus 21.50%, while both scored 97.25% on single-hop questions.**
  - Context: Fixed extraction and reader order-of-operations control; all returned parsed facts in the control are current.
  - Evidence: [b00064-b63457ff04] “CMC ties this control at 97.25% single-hop and scores 78.25% versus 21.50% multi-hop.”; [b00064-b63457ff04] “With extraction and reader fixed, the 56.75-point gap isolates record selection (Appendix G).”
- **Against retrieval over the same current facts, CMC scored 78.25% multi-hop versus 20.75% for BM25 while using 185 versus 1,528 mean reader-input tokens; dense BGE-M3 reached 33.25% with 1,535 tokens.**
  - Context: Shared direct-LLM extraction, same reader, and untruncated structured contexts.
  - Evidence: [b00237-0d59ca7953] “CMC 97.25 78.25 185 0 Fact BM25 97.50 20.75 1,528 0”; [b00237-0d59ca7953] “Fact dense (BGE-M3) 96.50 33.25 1,535 0”
- **At nearly matched evidence length, BM25 reached 7.25% multi-hop accuracy with 182 mean input tokens, whereas CMC reached 78.25% with 185.**
  - Context: Evidence-length control packing whole current facts from a fixed BM25 ranking.
  - Evidence: [b00237-0d59ca7953] “CMC 97.25 78.25 185 0”; [b00237-0d59ca7953] “Fact BM25, size matched 97.00 7.25 182 0”
- **The evidence-selection advantage persisted after changing readers: CMC versus fact BM25 was 76.50% versus 20.50% multi-hop with Qwen3.5-4B and 55.00% versus 11.50% with Llama-3.1-8B.**
  - Context: Reader swaps using fixed shared-LLM extraction and evidence packets.
  - Evidence: [b00076-814a68dabf] “With Qwen3.5-4B, CMC reaches 76.50% multi-hop versus 20.50% for fact BM25; with Llama-3.1-8B, it reaches 55.00% versus 11.50%.”
- **On MQuAKE-MemStream, CMC reached 96.62% multi-hop accuracy, compared with 53.38% for all current facts and 13.41% for stale values; the reported gains were 43.23 and 83.21 points.**
  - Context: Constructed two-hop memory streams with a frozen Qwen3.5-4B reader and supplied answer-bearing facts.
  - Evidence: [b00084-96f0eb7018] “CMC reaches 96.62% multi-hop accuracy, versus 53.38% when the reader sees all current facts and 13.41% when the selected relations use earlier values.”; [b00084-96f0eb7018] “Selecting a connected read from the current state gains 43.23 points over presenting that state in full.”; [b00084-96f0eb7018] “Resolving values within the selected relations gains 83.21 points over stale values.”
- **Increasing the traversal cap raised multi-hop accuracy from 5.50% at one hop to 54.00%, 71.75%, and 78.25% at two, three, and five hops, with mean reader inputs rising from 115.29 to 184.64 tokens.**
  - Context: Depth ablation with extraction, current state, anchors, renderer, evidence cap, and reader fixed.
  - Evidence: [b00281-1bc13caf9a] “Multi-hop accuracy rises from 5.50% at one hop to 54.00%, 71.75%, and 78.25% at two, three, and five hops.”; [b00281-1bc13caf9a] “The corresponding mean reader inputs are 115.29, 138.42, 158.41, and 184.64 tokens.”
- **On the 262K FactConsolidation split, CMC reached 95.0% single-hop and 61.0% multi-hop, versus 8.0% and 1.0% for a history suffix and 30.0% and 2.0% for same-reader BM25.**
  - Context: The official long-history split within the broader MemoryAgentBench evaluation.
  - Evidence: [b00089-14c6ae9de9] “CMC reaches 95.0% single-hop and 61.0% multi-hop, versus 8.0% and 1.0% for the suffix and 30.0% and 2.0% for same-reader BM25.”
- **CMC did not dominate the broader suite: it scored 10.2 versus 15.2 for dense+BM25 on summarization and 67.6 versus 78.9 on DetectiveQA.**
  - Context: Same-reader MemoryAgentBench comparison using task-specific interfaces; only selective forgetting used the current-graph read.
  - Evidence: [b00090-f930bd0a62] “but trails dense+BM25 on summarization (10.2 versus 15.2) and DetectiveQA (67.6 versus 78.9).”
- **At 262K, CMC’s CPU read measured 13.78 ms median and 144.34 ms at the 95th percentile, compared with 14.33 ms and 17.96 ms for fact BM25.**
  - Context: Local timing on frozen extraction; answer generation and one-time BM25 index construction were excluded.
  - Evidence: [b00311-1db2a8d9b7] “262K 0.204 13.78 / 144.34 14.33 / 17.96”

## Experimental evaluation

### Datasets

- FactConsolidation: 800 questions split equally between single-hop and multi-hop sets across 6K, 32K, 64K, and 262K histories with contradictory updates.
  - Evidence: [b00056-50ae2af981] “Its 800 questions comprise equal single- and multi-hop sets across 6K, 32K, 64K, and 262K histories”
- MQuAKE-MemStream: a derived controlled dataset from two-hop MQuAKE-Remastered counterfactual cases, ending with 800 single-hop and 798 multi-hop questions.
  - Evidence: [b00082-c13c288674] “Frozen Qwen3.5-4B reader; 800 single-hop and 798 multi-hop questions.”; [b00263-6c34752fb6] “The final dataset has 798 multi-hop and 800 single-hop questions.”
- The broader MemoryAgentBench campaign spans 14 source datasets and 130 histories across accurate retrieval, test-time learning, long-range understanding, and fact consolidation.
  - Evidence: [b00285-095f6b7b10] “These span 14 source datasets and 130 histories.”

### Baselines

- Prior read + refresh: traverse a graph built from earlier differing values, then replace selected values with current assertions; isolates selection before update resolution.
  - Evidence: [b00272-b5a9bc747f] “We traverse the constructed graph to depth five, then replace each selected key’s value with its current assertion.”; [b00272-b5a9bc747f] “Thus all returned parsed facts are current, while the selected keys can differ.”
- Stale closure: hold CMC’s selected keys fixed but substitute immediately preceding versions where available; isolates version choice.
  - Evidence: [b00191-3897a138a1] “Stale closure takes the closure our compiler admitted and substitutes the immediately preceding version when one exists”
- Latest state and raw history: present all current assertions or retained history subject to the reader window and rendering policy.
  - Evidence: [b00265-53a9242514] “The latest-state control returns all current assertions.”; [b00265-53a9242514] “The raw-history control retains every version before applying the reader’s window policy.”
- Lexical and dense retrieval over current facts: fact BM25, size-matched BM25, BGE-M3, and a dense-plus-reranker pipeline.
  - Evidence: [b00237-0d59ca7953] “Fact BM25, size matched 97.00 7.25 182 0 Fact dense (BGE-M3) 96.50 33.25 1,535 0”; [b00206-a3b0dadd11] “Qwen3-Embedding-8B dense top-100 retrieval, Qwen3-Reranker-4B top-10 reranking”
- A disjoint random negative control excludes CMC-selected keys while matching evidence cardinality.
  - Evidence: [b00212-6965d720d1] “The disjoint random negative control draws from the active state while excluding the query projection keys, matching cardinality exactly on all 800 questions”
- End-to-end and ported comparisons include adapted SH-Conflict/CAR, G-Walk, MeLLo, suffix retrieval, BM25, dense+BM25, and published MemoryAgentBench systems.
  - Evidence: [b00200-3bc8938e8e] “The G-Walk and MeLLo rows in Table 5 use the released MQuAKE-Remastered implementations and prompts”; [b00247-518fa1e721] “Both systems receive the original histories and use HY4-preview.”

### Metrics

- Primary FactConsolidation metric: released substring exact-match accuracy, reported separately for single-hop and multi-hop questions.
  - Evidence: [b00056-50ae2af981] “we use the released substring exact-match score.”
- Strict normalized exact match is reported as a sensitivity analysis.
  - Evidence: [b00202-570ee15996] “Requiring each saved parsed answer to equal a reference alias after the released normalization”
- Efficiency measurements include mean reader-input tokens, clipped-context counts, CPU replay/read time, and recorded request duration.
  - Evidence: [b00059-e1189d1065] “SH and MH are accuracy (%); Tokens is mean reader-input length; Trunc. counts clipped contexts.”; [b00310-5a175d43b5] “Read columns give median / 95th percentile in milliseconds.”
- Paired comparisons report win, tie, and loss counts with query-cluster percentile bootstrap intervals.
  - Evidence: [b00214-b8e0475897] “paired contrasts use query-cluster percentile bootstrap at 10,000 replicates.”

### Ablations

- Ordering ablation: compare resolve-then-traverse with traversal on prior values followed by current-value refresh.
  - Evidence: [b00276-1b753170c8] “Multi-hop 400 21.50 78.25 56.75”
- Version-choice ablation: stale closure preserves selected keys while replacing active values with earlier ones.
  - Evidence: [b00071-5befc7b4d8] “Stale closure keeps CMC’s selected relations but substitutes previous values where available”
- Traversal-depth ablation evaluates one-, two-, three-, and five-hop caps under otherwise fixed conditions.
  - Evidence: [b00280-6f143cd6cd] “We vary the traversal cap over h∈{1,2,3,5} while keeping the LLM extraction, current-state construction, anchors, source-record renderer, 60,000-character cap, and HY4 reader fixed.”
- Frontend ablation compares a manually specified grammar adapter, direct LLM extraction, and a source-induced hybrid using the same CMC read and reader.
  - Evidence: [b00221-74e2424fd1] “The grammar adapter uses manually specified patterns; direct LLM extraction names relations from source records; the hybrid induces literal patterns from source examples.”
- Reader ablation swaps HY4-preview for Qwen3.5-4B and Llama-3.1-8B while reusing fixed extraction and evidence.
  - Evidence: [b00241-fa28705229] “Only the reader and its chat template change: Qwen3.5-4B”; [b00245-e7e04f147a] “This is a reader replacement on fixed extracted evidence.”
- Evidence-budget ablation compares CMC with BM25 packed to each question’s CMC evidence allowance.
  - Evidence: [b00254-0126ab9e0e] “For each question, its evidence allowance equals the cl100k token count of CMC’s rendered evidence”

### Negative results

- CMC trails dense+BM25 on summarization and DetectiveQA in the broader same-reader suite.
  - Evidence: [b00090-f930bd0a62] “but trails dense+BM25 on summarization (10.2 versus 15.2) and DetectiveQA (67.6 versus 78.9).”
- The hybrid extraction frontend has lower observed accuracy than direct extraction and suffers a failed reader request after an oversized no-anchor fallback.
  - Evidence: [b00223-9872a7c8f6] “The hybrid has one failed reader request after a no-anchor read falls back to an oversized history; the failure remains in the denominator.”
- The larger MQuAKE-MemStream pooling run is not used as confirmatory evidence because cross-case overwrites alter released support hops.
  - Evidence: [b00267-b2d1b97157] “Extending the same construction to all 3,000 CF-3k cases alters at least one released post-edit hop in 431 cases.”; [b00267-b2d1b97157] “We therefore do not use that larger run as confirmatory evidence.”
- The runtime audit does not establish a CPU latency advantage for CMC, whose high-tail latency is worse in the reported long-history measurement.
  - Evidence: [b00312-25bc935b77] “At 262K, the two read medians are close, but CMC has a higher 95th percentile.”; [b00312-25bc935b77] “these measurements do not establish a CPU latency advantage.”
- CMC’s summary outputs exhibit substantial judge-format and length failures, preventing a clean interpretation of the low summary score.
  - Evidence: [b00307-59e83c6a4b] “On the 100 summary questions, 12 history-suffix and 73 CMC outputs have invalid judgments.”; [b00307-59e83c6a4b] “CMC summaries exceed the requested 1,200-word limit on 76 items”


## Limitations

- The demonstrated guarantee and gain apply to ordered, single-valued relations with last-write-wins semantics, not simultaneous values, multi-agent conflicts, or other update models.
  - Evidence: [b00303-0d98a51923] “CMC’s last-write-wins rule is specific to the benchmark’s ordered, single-valued relations; it does not resolve simultaneous values or multi-agent conflicts.”
- Exact surface-form anchoring cannot disambiguate entities or infer aliases.
  - Evidence: [b00046-80ec254de0] “This is a deterministic surface-form rule; entity disambiguation and alias inference are outside this implementation.”
- Coverage depends on successful parsing, reachability from explicit anchors, and the fixed hop bound.
  - Evidence: [b00032-c8c684e581] “Its usefulness depends on the supporting facts being parsed and reachable within h hops of an explicit anchor.”; [b00099-4c3b9702dc] “exact anchoring, missing links, and the hop limit restrict coverage.”
- The primary FactConsolidation evidence comes from a broader development grid rather than an independent confirmatory evaluation.
  - Evidence: [b00099-4c3b9702dc] “FactConsolidation came from a broader development grid, so independent confirmation remains needed.”
- Official FactConsolidation labels may contain superseded answers, and the automated flags still require manual adjudication.
  - Evidence: [b00203-d274ab7fdb] “These flags need manual adjudication.”; [b00099-4c3b9702dc] “An automated screen flags 33 of 800 reference answers as possibly superseded; all remain in the official scores.”
- MQuAKE-MemStream imposes chronology not present in the source benchmark and tests grammar-parsed supplied facts rather than open-form extraction.
  - Evidence: [b00263-6c34752fb6] “This ordering is imposed by our adaptation: MQuAKE does not provide a chronological agent-memory stream.”; [b00263-6c34752fb6] “these results do not test extraction from open-form language.”
- The primary HY4-preview reader is a provider alias rather than an immutable checkpoint.
  - Evidence: [b00239-44762da7f0] “HY4-preview is a provider alias rather than a pinned weight revision; we record the model identifier returned for each request.”
- Reported token accounting excludes offline parsing, indexing, embeddings, graph construction, and storage, limiting end-to-end cost conclusions.
  - Evidence: [b00216-3b39f05a3a] “They exclude offline parsing, indexing, embedding, graph construction, and storage”
- When the evidence window binds, CMC uses suffix clipping rather than optimizing among competing graph closures.
  - Evidence: [b00036-78582184c7] “Selecting among competing closures when the window binds remains a separate extension of this read interface.”
- Broader-suite interfaces are task-specific; only selective forgetting uses the current-graph read, so the full table is not a pure evaluation of Algorithm 1.
  - Evidence: [b00086-208cf8001c] “Only SF uses the current-graph read; direct comparisons use the four local HY4-preview rows.”

## Reproducibility

**Status:** strong

Reproducibility is strong by paper standards: the authors claim code, data, predictions, detailed frozen protocols, pinned revisions for local readers and scorers, replay checks, and a timing script. Confidence is reduced by the unpinned HY4-preview alias, replay checks that do not regenerate all model outputs or extraction, incomplete end-to-end cost accounting, and unresolved label audits.

**Available artifacts**

- Compiler
- Evaluation scripts
- MQuAKE-MemStream data
- Per-example predictions
- Dataset reconstruction and evaluation code
- Runtime timing script
- Recorded inputs, model identifiers, prompts, settings, outputs, and native scores

**Missing pieces**

- An immutable checkpoint for HY4-preview
- Independent rerun of GPU generation and original source extraction in the replay checks
- Finish reasons for broad-suite generations
- A complete end-to-end wall-clock and cost measurement including offline extraction, indexing, embeddings, storage, and answer generation
- Manual adjudication of possibly superseded FactConsolidation references
- Independent confirmatory evaluation outside the development grid

## AIDB assessment

- Novelty: The key novelty is an explicit read-order contract: resolve overwritten relations into a current graph before traversing it to select provenance-linked original records. The fixed-extraction order control distinguishes this from merely refreshing values in an already selected context. The derived MQuAKE-MemStream dataset is also a useful controlled instrument, though its chronology is synthetic.
- Usefulness: High for long-lived assistants whose memory can be represented as ordered, mostly single-valued relational assertions and whose serving architecture permits offline compilation. The method is less immediately applicable to ambiguous entities, simultaneous truths, multi-agent disagreement, open-ended dialogue, or adaptive multi-call retrieval.
- Confidence: medium
- Recommended action: read
- Rationale: The central causal comparison is compelling: extraction, reader, prompt, and budget are fixed while evidence-selection order changes, and the effect persists across readers, retrieval controls, matched evidence length, and a second constructed dataset. Adoption should wait for independent confirmation on naturally occurring update streams, stronger entity resolution, immutable reader replication, and end-to-end cost evaluation.

## Uncertainties

- **How much of the gain transfers to natural conversational histories with ambiguous references, aliases, negation, simultaneous values, and relations outside the extraction schema?** — The main benchmarks largely present ordered assertion-like records, while the second dataset is grammar parsed; production memory is substantially less regular.
  - Evidence: [b00223-9872a7c8f6] “It does not establish generalization to unseen writing styles or relation types.”; [b00263-6c34752fb6] “these results do not test extraction from open-form language.”
- **Would the headline scores reproduce with the same immutable reader weights?** — The principal HY4-preview runs record returned identifiers but do not pin a model-weight revision across execution dates.
  - Evidence: [b00274-1f1ab0ebdd] “The HY4 alias is unpinned, so the recorded reader settings do not establish an immutable model checkpoint across execution dates.”
- **What is the true accuracy after manual adjudication of potentially superseded reference answers?** — Official scores retain flagged labels, and the paper supplies only conditional lower bounds rather than corrected absolute accuracy.
  - Evidence: [b00203-d274ab7fdb] “These flags need manual adjudication.”; [b00203-d274ab7fdb] “this conditional bound does not establish absolute accuracy.”
- **How does CMC behave when relevant closures exceed the evidence budget?** — The main structured comparison fits the window, while the current implementation clips to a recent suffix rather than selecting among competing closures.
  - Evidence: [b00036-78582184c7] “All CMC contexts in the shared direct-extraction comparison fit its window.”; [b00036-78582184c7] “Selecting among competing closures when the window binds remains a separate extension of this read interface.”
- **Is CMC cheaper end to end than strong retrieval or adaptive pipelines once extraction, alignment, indexing, graph maintenance, and generation are included?** — Reported reader-token and CPU-read advantages omit substantial offline and serving components and do not establish full wall-clock cost.
  - Evidence: [b00313-634ebd03e2] “The present numbers are not a full end-to-end wall-clock cost.”
- **How much do summary and DetectiveQA regressions reflect memory selection versus output-format and judging interactions?** — The broader-suite weaknesses cannot be cleanly attributed to the graph mechanism because task interfaces differ and many summary judgments are invalid.
  - Evidence: [b00307-59e83c6a4b] “These observations suggest an output-format interaction, but do not establish what another judging contract would score.”

## Open questions

- Can the read contract be extended from last-write-wins keys to temporally scoped, multi-valued, uncertain, or conflicting assertions?
- Can learned alias resolution and entity disambiguation improve recall without introducing unacceptable false anchors?
- What strategy should select among branches or closures when the rendered evidence exceeds the reader window?
- Does resolve-then-traverse retain its advantage on independently collected, naturally chronological multi-session conversations?
- What are extraction precision, relation-alignment error rates, and downstream sensitivity to individual parsing failures?
- How does CMC compare with adaptive iterative retrieval under matched total calls, tokens, latency, and source-processing cost?
- Can summary and DetectiveQA regressions be separated from formatting and judge failures through a corrected evaluation contract?

## Proposed AIDB experiments

- **Hypothesis:** Resolve-then-traverse improves multi-hop accuracy on natural multi-session dialogue updates, not only assertion-style or constructed streams.
  - Baseline: Prior read + refresh and current-fact BM25 using the same frozen extraction, reader, prompt, and evidence budget.
  - Primary metric: Paired multi-hop exact-match accuracy on a preregistered held-out dialogue set with manually verified current answers and evidence paths.
  - Stop condition: Stop after the preregistered sample is complete; reject the hypothesis if the lower bound of the paired confidence interval against both baselines is not above zero.
- **Hypothesis:** Alias-aware anchoring increases coverage without materially increasing false graph closures.
  - Baseline: The paper’s exact whole-span anchoring rule.
  - Primary metric: Answer accuracy stratified by alias requirement, accompanied by anchor precision and evidence-path recall.
  - Stop condition: Stop after all preregistered alias strata are evaluated; reject if answer accuracy fails to improve or anchor precision falls below the preregistered safety threshold.
- **Hypothesis:** A budget-aware closure selector preserves CMC’s multi-hop advantage when complete bounded closures exceed the reader window.
  - Baseline: Newest-contiguous-suffix clipping of rendered CMC records.
  - Primary metric: Multi-hop exact-match accuracy on overflow cases at identical character budgets.
  - Stop condition: Stop after the fixed overflow suite is exhausted; reject if the selector does not outperform suffix clipping under paired evaluation.
- **Hypothesis:** CMC remains competitive after all offline and online costs are included.
  - Baseline: Fact BM25, dense retrieval, and an adaptive iterative-retrieval pipeline under identical hardware and reader models.
  - Primary metric: End-to-end cost per correct multi-hop answer, including extraction, alignment, indexing, updates, retrieval, rendering, and generation.
  - Stop condition: Stop after each method processes the same frozen workload and update stream; reject if CMC is Pareto-dominated on accuracy, latency, and total cost.
- **Hypothesis:** Extending the state model beyond last-write-wins improves correctness for simultaneous and conflicting facts without degrading ordinary overwrite cases.
  - Baseline: Original CMC with one active value per subject–relation key.
  - Primary metric: Macro-averaged exact match across overwrite, simultaneous-value, temporal-scope, and conflict-resolution subsets.
  - Stop condition: Stop after the preregistered balanced suite is complete; reject if macro accuracy does not improve or overwrite-only accuracy drops beyond the allowed margin.
- **Hypothesis:** Correcting summary output and judging contracts explains a substantial portion of CMC’s broader-suite summarization deficit.
  - Baseline: The reported summary prompt, generation cap, word-limit instruction, and judge parser.
  - Primary metric: Valid-judgment rate and summary score under a format-constrained decoder with blind human adjudication of disagreements.
  - Stop condition: Stop after every summary item has both protocol scores and adjudication; reject if validity improves but the CMC score gap remains within the preregistered equivalence band of the original deficit.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:05:15.481825+00:00`
- Document SHA-256: `5b0355f4ae679571a580a79ce5aa53db445bc7823cc0834870107a4ac5b48a49`
- Metadata SHA-256: `a05a9c92b961e95c4ba7c8cef124c41d20d554d4df87f40c4c344902f3428148`
- Blocks: 315
- Deterministic repair attempts: 0
