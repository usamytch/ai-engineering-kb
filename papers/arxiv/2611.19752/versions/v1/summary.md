# StaleBench: Isolating Stale Retrieval in Agent Memory, and Pricing the Fix

## Executive summary

StaleBench isolates stale retrieval in agent-owned memory using source-defined temporal labels and value-agnostic questions. Its strongest experiment holds rank 1 fixed across every query while changing only lower-ranked contamination: without dates, reader accuracy differs by 65.6 and 29.5 points, showing that current@k can misrank policies. The benchmark also reveals that lexical anchors make same-fact detection look deceptively easy, while symmetric entity resolution recovers much of the anchor-free loss. Evidence is unusually thorough and artifacts are extensive, but external validity remains limited by templated English facts, optimistic inventories, fixed prompts, clean temporal assumptions, and a narrow deployed-systems track.

## Problem

**Statement.** Long-lived agent memories accumulate superseded versions of facts. For a value-agnostic query, similarity retrieval may identify the correct entity while failing to distinguish its current value from stale values.

**Why it matters.** A retrieval metric that rewards a current first hit but ignores contradictory lower-ranked memories can overstate end-to-end quality or rank memory policies backwards once a reader consumes the context.

**Scope.** The primary instrument covers changing, single-valued TempLAMA facts in English, with chronological statement streams, source-defined final-year labels, controlled paraphrasing and aliasing, plus supplementary multi-valued, larger-corpus, reader, and deployed-system tracks.

## Method

The paper converts temporally qualified Wikidata facts from TempLAMA into chronological natural-language streams. Each fact receives a value-agnostic current-value query. Policies either retain all statements, use temporal reranking, or detect same-fact updates and overwrite or invalidate prior versions. Evaluation separates current, stale, missed, contaminated, and memory-footprint outcomes, then passes each policy’s top-ranked context to readers. A controlled pair fixes rank 1 exactly while varying ranks 2–5.

### Key components

- Source-defined currency labels independent of any system score.
- A lexical-anchor axis that replaces later full subject names with controlled short forms.
- A policy ladder spanning BM25, dense cosine retrieval, temporal reranking, recency weighting, threshold keying, exact gazetteers, fuzzy and alias-equipped entity linking, read-path keying, symmetric keying, and a true-key oracle.
- Reader evaluation with and without stored years, plus constructed contexts and presentation-order interventions.
- Direct evaluation of Mem0, Graphiti, LangMem, and a reimplementation of ERASE under a shared harness.

### Assumptions

- In the clean primary condition, statements arrive as their facts become true and the final value is current.
- Primary top-1 evaluation assumes facts are single-valued in each year.
- Queries name their subject in full, making read-side entity resolution easier than elliptical conversational queries.
- Reader comparisons are conditional on one prompt format and top-5 contexts.
- Entity-linking rungs may receive a complete subject inventory, and one rung receives the alias inventory that generated the stream.

## Main claims

- **StaleBench isolates stale retrieval by deriving current-value labels from the source rather than from retrieval behavior.**
  - Evidence: [b00009-c673075a80] “the label “current” comes from the source (Wikidata validity years via TempLAMA (Dhingra et al., 2022), or a generator schedule), never from a retrieval score”
- **Contamination must be interpreted jointly with answer presence because deleting the answer can improve contamination without improving context quality.**
  - Evidence: [b00125-0ac9552ec1] “A policy can therefore improve contamination by deleting the answer.”; [b00125-0ac9552ec1] “We accordingly never report contamination@k without current@k beside it”
- **Same-fact resolution on both write and query paths addresses different errors: writing reduces contradictory versions and footprint, while query resolution reduces misses.**
  - Evidence: [b00048-09fa1dc308] “Read-path keying fixes top-1: at a=1 it cuts the fuzzy rung’s miss rate from 0.167 to 0.045”; [b00048-09fa1dc308] “Write-path keying fixes the context: alone it holds contamination@5 at 0.032 in 467 slots”
- **No single attribution or scoring convention adequately characterizes all evaluated deployed memory systems.**
  - Evidence: [b00236-61abe0fe3e] “No single scoring convention describes all four.”

## Results

- **Store-all cosine produces stale first-ranked answers on 0.530 of queries. Timestamp reranking raises current@1 from 0.464 to 0.925, but contamination@5 remains 0.974 because the candidate set is unchanged.**
  - Context: This establishes both the stale-retrieval failure and the principal limitation of the inexpensive timestamp repair.
  - Evidence: [b00034-8266a22cfb] “policy current@1 ↑ current@5 ↑ stale@1 ↓ miss@1 ↓ contam@5 ↓ slots ↓”; [b00034-8266a22cfb] “Cosine (store-all) 0.464 [0.419,0.506] 0.985 0.530 0.006 0.974 995”; [b00034-8266a22cfb] “Cosine + time-rerank 0.925 [0.900,0.947] 0.985 0.049 0.026 0.974 995”; [b00035-a1a9742dc9] “contamination@5 stays between 0.936 and 0.991 for every store-all policy”
- **Removing the lexical anchor exposes large same-fact detection costs: exact gazetteer current@1 falls from 0.972 to 0.169, threshold keying from 0.859 to 0.513, while fuzzy linking reaches 0.714 and symmetric keying reaches 0.831 at full aliasing.**
  - Context: The anchored benchmark makes simple string matching look nearly oracle-level; controlled aliasing separates methods and supports entity resolution on both paths.
  - Evidence: [b00039-bc6de08e72] “Table 3: current@1 as the lexical anchor is withdrawn (a= alias_p: the probability a non-introducing statement uses a short form).”; [b00040-023104ab95] “Overwrite: gazetteer (exact) 0.972 0.752 0.575 0.333 0.169 65.8”; [b00040-023104ab95] “Overwrite: threshold τ 0.859 0.765 0.671 0.605 0.513 31.4”; [b00040-023104ab95] “Overwrite: fuzzy linker (no alias table) 0.968 0.908 0.846 0.767 0.714 11.3”; [b00040-023104ab95] “Symmetric key (read+write) 0.989 0.953 0.915 0.865 0.831 −0.4”
- **The controlled reader pair returns the same rank-1 statement for all 468 queries and has identical current@1 of 0.989, yet changing contamination@5 from 0.998 to 0.000 changes no-date accuracy from 0.327 to 0.983 for qwen2.5:14b and from 0.684 to 0.979 for glm-4.6.**
  - Context: This is the paper’s strongest causal evidence that lower-ranked stale versions materially affect readers and that current@1 cannot distinguish important policy differences.
  - Evidence: [b00057-d264902cc0] “they return the same statement at rank 1 for all 468 queries”; [b00057-d264902cc0] “They are identical on current@1 (0.989 for both, exactly)”; [b00057-d264902cc0] “which changes only what fills ranks 2–5: contamination@5 0.998 against 0.000.”; [b00058-507b21106f] “0.983 against 0.327 on qwen2.5:14b (p<10−3, sign-flip permutation), a gap of 65.6 points”; [b00058-507b21106f] “0.979 against 0.684 on glm-4.6 (p<10−3, 29.5 points)”
- **Showing stored years nearly removes the controlled-pair penalty: qwen2.5:14b moves from 0.327 to 0.983 for the retain-everything member, while the symmetric member remains at 0.983; glm-4.6’s dated gap is 1.5 points.**
  - Context: Retention is therefore not the only solution under trustworthy, available timestamps; prompt-level temporal evidence is a strong alternative.
  - Evidence: [b00059-939216cea4] “the retain-everything member goes from 0.327 to 0.983 while the symmetric member stays at 0.983”; [b00059-939216cea4] “for glm-4.6 the dated pair reads 0.957 against 0.972, a gap of 1.5 points.”
- **The deployed-system track finds distinct implementation failures: Graphiti rises from current@1 0.347 to 0.833 and reader accuracy 0.593 to 0.893 when its validity flags are respected, while ERASE with the smaller model loses every retrievable version for 0.133 of facts.**
  - Context: These results argue for pinning versions and read paths, and for evaluating destructive editing as a factual-recall risk rather than only a freshness mechanism.
  - Evidence: [b00225-84182fe04c] “As returned, the system reaches current@1 0.347 by id and 0.347 by text”; [b00067-e3c8008465] “it scores 0.347 as installed, below store-all, and 0.833 with its own validity flags respected; the reader moves from 0.593 to 0.893.”; [b00069-e2b317c321] “With qwen2.5:14b it reaches 0.853, and for 0.133 of facts no version survives anywhere in the returned depth”; [b00225-84182fe04c] “Ranking the system’s own non-invalidated edges first — the read path of the temporal-KG rung, applied post hoc to what the system returned, with no model call — lifts it to 0.833”

## Experimental evaluation

### Datasets

- Primary TempLAMA-derived benchmark: 892 changing facts across nine relations, split into 424 validation and 468 test facts; yearly validity covers 2010–2020.
  - Evidence: [b00023-92c49777ed] “yearly validity (2010–2020)”; [b00023-92c49777ed] “892 facts over nine relations”; [b00023-92c49777ed] “Facts split by key hash into val (424, all tuning) and test (468, all reported numbers).”
- A scale track includes every changing key and evaluates 2,904 test facts, including 2,436 multi-valued facts.
  - Evidence: [b00255-df52155927] “2,904 test facts (2,436 of them multi-valued, mean 1.23 currently valid values each)”
- A realistic-corpus configuration adds 6,083 never-queried distractor statements to form a 7,078-statement stream.
  - Evidence: [b00132-07aa34e179] “6,083 extra statements, a 7,078-statement stream.”

### Baselines

- Store-all BM25 and dense cosine retrieval using all-MiniLM-L6-v2, with all-mpnet-base-v2 as a robustness check.
  - Evidence: [b00028-0e05ce4e34] “BM25 (Robertson and Zaragoza, 2009) and Cosine (dense retrieval over sentence embeddings; all-MiniLM-L6-v2 primary, all-mpnet-base-v2 robustness check”
- Temporal store-all baselines include top-k timestamp reranking and recency-weighted similarity.
  - Evidence: [b00029-3ab5d2a777] “Time-rerank(k) retrieves the top-k by similarity and answers with the most recent candidate”; [b00029-3ab5d2a777] “Recency-weighted scores sim+λ​dage”
- Retention baselines combine threshold, gazetteer, fuzzy-linker, entity-linker, LLM, or oracle keying with overwrite or temporal invalidation.
  - Evidence: [b00030-fd1d5e6def] “Retention = a keyer × a mechanism.”; [b00030-fd1d5e6def] “threshold”; [b00030-fd1d5e6def] “gazetteer”; [b00030-fd1d5e6def] “fuzzy linker”; [b00030-fd1d5e6def] “entity linker”; [b00030-fd1d5e6def] “LLM”; [b00030-fd1d5e6def] “oracle”

### Metrics

- Retrieval metrics: current@1, stale@1, miss@1, current@k, contamination@k, and final slot count.
  - Evidence: [b00018-1b938a02dd] “the top-1 is scored as current@1 (right fact, current value), stale (right fact, outdated value — the isolated failure), or miss (wrong fact).”; [b00018-1b938a02dd] “Over the top-k we report current@k and contamination@k”; [b00018-1b938a02dd] “after the stream, slots (store size).”
- Reader answers are evaluated by normalized containment against current and superseded source values.
  - Evidence: [b00055-460e7cc4e5] “answers are scored by normalized containment against the source-defined current value and against the fact’s superseded values”
- The scale track adds set recall@5 to measure coverage of simultaneously valid values.
  - Evidence: [b00258-c4e58ff4e7] “Set recall@5 charges that: the fraction of a fact’s distinct currently valid values whose statements appear in the top-5.”

### Ablations

- Lexical anchor availability is swept from fully anchored to fully aliased, with every policy retuned at each level.
  - Evidence: [b00039-bc6de08e72] “current@1 as the lexical anchor is withdrawn (a= alias_p: the probability a non-introducing statement uses a short form).”; [b00039-bc6de08e72] “every policy re-tuned on val at every level.”
- Reader contexts are tested with and without surfaced years.
  - Evidence: [b00055-460e7cc4e5] “every condition runs twice, with and without the stored year surfaced in the context”
- Constructed contexts manipulate stale-version presence and position, isolating contamination and ordering effects.
  - Evidence: [b00240-95bf3551c7] “Constructed contexts: reader accuracy when contamination is manipulated rather than observed”; [b00246-4d188d98cc] “the full cost of one stale neighbour ranges from 14.1 to 67.7 points depending only on where it sits.”
- Separate corruption experiments permute timestamps, arrival order, or both.
  - Evidence: [b00153-956e4fcbeb] “clock permuted: timestamps permuted across statements, arrival order intact”; [b00153-956e4fcbeb] “arrival permuted: arrival order permuted, each statement keeping its own timestamp”

### Negative results

- Timestamp reranking’s large retrieval improvement does not consistently transfer to readers and harms one reader under the default ordering.
  - Evidence: [b00056-239ab110ad] “at the reader it is worth -22.9 points for qwen2.5:14b and +6.6 for glm-4.6.”
- The one-shot LLM keyer does not beat the mechanical alternatives in the tested configuration.
  - Evidence: [b00187-7968c49ae5] “The model underperforms every mechanical keyer when the anchor is present, and lands mid-ladder when it is not.”
- Ordinary symmetric fuzzy resolution does not retain its advantage over an alias-equipped write-only linker on natural short forms.
  - Evidence: [b00182-2e90d9c881] “Ordinary resolution applied symmetrically no longer beats a complete alias table applied asymmetrically”
- With both temporal signals corrupted, none of the tested policy families recovers freshness.
  - Evidence: [b00157-3605900227] “With both signals corrupted nothing recovers, because the information is gone.”


## Limitations

- The headline slice is filtered to changing, single-valued facts and is not representative of world-knowledge prevalence.
  - Evidence: [b00264-5cd7a70a2d] “it is a deliberately filtered set of facts that changed.”; [b00264-5cd7a70a2d] “prevalence estimates should not be read off it.”
- The language and reference phenomena are narrow: English templates, mechanical short forms, nine relations, and no natural dialogue or discourse coreference.
  - Evidence: [b00075-548590d9c8] “Validity is yearly, statements are templated, and the anchor-free axis uses mechanically derived short forms”; [b00075-548590d9c8] “English only; nine relations; 468 test facts is enough for tight CIs but not for per-relation claims.”
- The entity-linker result is optimistic because it receives the alias inventory used to generate the stream; even the fuzzy linker knows the queried-subject inventory.
  - Evidence: [b00137-a4d4828918] “The alias rung’s is exhaustive, correct, free, and generated by the same function that inserted the aliases”; [b00137-a4d4828918] “its inventory is still exactly the 468 queried subjects”
- The read-side fix is evaluated on full-name queries, not elliptical conversational queries.
  - Evidence: [b00140-3d2a83a864] “queries in this benchmark always name their subject in full, so the read side is the easy direction for a resolver.”; [b00140-3d2a83a864] “a deployment whose queries are themselves elliptical (“and who does he play for now?”) would pay on the read path too, and we do not measure that.”
- The systems evidence is narrow: four mechanisms, one reimplemented, only 150 facts, and one reader for system-level reader results.
  - Evidence: [b00076-3ba090af50] “four mechanisms, one of them our reimplementation, on 150 facts, with a single reader.”
- Clean-condition conclusions rely on most-recent-equals-current; ambiguous supersession and explicit corrections are excluded.
  - Evidence: [b00077-8a66da55fd] “most-recent-equals-current holds by construction in the clean condition.”; [b00077-8a66da55fd] “Ambiguous updates, where it is unclear whether a statement supersedes an earlier one, and corrections with their own semantics”; [b00077-8a66da55fd] “are out of scope.”
- Reader findings are comparative under a fixed prompt and top-5 context; their magnitude may not generalize across prompts, readers, or context sizes.
  - Evidence: [b00077-8a66da55fd] “The reader track uses 2 models with one prompt format, so its claims are comparative across contexts under a fixed prompt, not absolute accuracy.”; [b00245-50dec2c721] “the gap should be read as the cost of contamination at one context size we fixed in advance, not as a constant.”

## Reproducibility

**Status:** strong

Reproducibility is strong for benchmark and reference-policy results: data, frozen scoring, code paths, cached calls, configurations, checksums, and result records are described as released. The systems track is materially harder and more environment-sensitive, but the paper documents probes, versions, backend failures, and infrastructure requirements rather than hiding them.

**Available artifacts**

- Eight released benchmark configurations as statement and query JSONL for both splits.
- Alias inventories, datasheet, manifest with row counts and MD5s, frozen evaluator, reference baselines, harness, result records, and cached model calls.
- Public repository and archived release are identified in the paper.
- Results are generated from recorded files and injected into the manuscript; controlled-pair premises are asserted by the build.

**Missing pieces**

- Independent reproduction is not reported in the supplied paper.
- The systems track additionally requires pinned library versions, specific vector backends, FalkorDB, and local Ollama infrastructure.
- One ERASE implementation is reconstructed from the paper because no pinned release exists.
- Some hosted-model and backend configurations are incomplete or unusable, limiting exact cross-system replication.

## AIDB assessment

- Novelty: High methodological novelty: the work isolates stale retrieval below general temporal QA, introduces contamination@k with explicit cautions, prices same-fact detection across controlled anchor and inventory axes, and supplies an unusually clean rank-1-controlled reader experiment.
- Usefulness: High for evaluating long-term agent memory, RAG stores, supersession policies, and temporal retrieval. The benchmark is especially useful as a diagnostic suite rather than as a single leaderboard number; practitioners should report answer presence, contamination, reader behavior, footprint, and temporal-signal assumptions together.
- Confidence: high
- Recommended action: adopt
- Rationale: Adopt the benchmark and evaluator as a diagnostic component, while avoiding certification claims and avoiding current@1-only ranking. The controlled reader pair, corruption studies, scale track, and implementation probes provide strong decision-relevant evidence. Deployment conclusions should still be revalidated on natural dialogue, incomplete inventories, elliptical queries, ambiguous updates, and the target reader/prompt.

## Uncertainties

- **It is unresolved how well symmetric keying works when queries themselves use pronouns, nicknames, misspellings, or discourse-dependent references.** — The recommended read-path fix is evaluated in its easier direction; its advantage may shrink when query entity resolution is also difficult.
  - Evidence: [b00140-3d2a83a864] “a deployment whose queries are themselves elliptical (“and who does he play for now?”) would pay on the read path too, and we do not measure that.”
- **The reader penalty’s magnitude across context sizes, prompt templates, and additional model families is unknown.** — The central direction is supported on two readers, but operational decisions require effect sizes for the actual reader and prompt assembly convention.
  - Evidence: [b00245-50dec2c721] “the gap should be read as the cost of contamination at one context size we fixed in advance, not as a constant.”; [b00307-126403da49] “The reader track uses 2 models with one prompt format”
- **The unexplained identifier–text mismatch observed for one Mem0 release may be system behavior, wrapper bookkeeping, or scale-dependent interaction.** — Attribution-based system rankings can change dramatically, but the paper explicitly does not establish the mechanism behind this instance.
  - Evidence: [b00306-1392e0755c] “the effect does not appear at small scale and we offer no mechanism for it, only the measurement.”
- **Contamination@k is useful but may not be the optimal predictor of reader behavior because it ignores stale-item position and can improve when answers are deleted.** — A leaderboard could still tie policies with materially different reader outcomes or reward omission unless contamination is paired with answer-presence metrics and possibly position-aware measures.
  - Evidence: [b00248-fd003d6ee6] “cosine and time-rerank share a contamination@5 of 0.974 by construction (§4) while their reader accuracies are 0.558 and 0.329”; [b00249-f367961819] “What these results actually argue for is a position-aware successor — the rank of the last stale version in the top-k”

## Open questions

- Does the controlled contamination effect persist across larger and smaller contexts, more reader families, and diverse prompt layouts?
- How much does symmetric keying retain on natural conversational streams with incomplete entity inventories and elliptical queries?
- Can a position-aware contamination metric predict reader accuracy better than contamination@k without rewarding answer deletion?
- How should the benchmark represent ambiguous updates, retractions, contested claims, and provenance-preserving history?
- Can an inventory-equipped or task-trained LLM keyer outperform cheap entity-resolution machinery at acceptable latency and cost?
- Which findings from the narrow systems track survive independently reproduced runs across versions, backends, and production workloads?

## Proposed AIDB experiments

- **Hypothesis:** A position-aware metric using the rank of the last stale version predicts reader accuracy more faithfully than current@1 or contamination@5 across prompt layouts and context sizes.
  - Baseline: Compare current@1 and contamination@5 on the same policy and constructed-context tracks.
  - Primary metric: Paired policy-order inversion count against reader accuracy, reported separately for each reader, prompt order, and context size.
  - Stop condition: Stop after preregistered evaluation on at least three context sizes and four readers; reject the hypothesis unless the new metric lowers inversions against both baselines without increasing answer-absent wins.
- **Hypothesis:** Symmetric entity resolution retains a meaningful advantage over write-only resolution when both stored statements and queries contain natural aliases or elliptical references.
  - Baseline: Write-only fuzzy linker, write-only alias-equipped linker, and similarity retrieval with timestamp reranking.
  - Primary metric: Current@1 jointly reported with current@5, contamination@5, miss@1, and reader accuracy on a natural conversational test set.
  - Stop condition: Stop after confidence intervals on the paired current@1 difference are narrower than three points; reject the hypothesis if symmetric resolution fails to improve current@1 or improves it mainly by increasing contamination.
- **Hypothesis:** An inventory-equipped LLM keyer reduces false splits relative to the tested text-only LLM keyer while remaining competitive with the mechanical entity linker.
  - Baseline: Text-only glm-4.6 keyer and the alias-equipped mechanical linker under identical candidate recall and inventory information.
  - Primary metric: Current@1 plus direct clustering split rate and merge-error count, with model calls and latency reported.
  - Stop condition: Stop after the full validation and test protocol; reject the hypothesis if the LLM does not reduce split rate without materially increasing merge errors, or remains below the mechanical linker on current@1.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:25:52.831476+00:00`
- Document SHA-256: `a04a81a70e195b8e72ad02524500460130fa8f9c3ca08b931035faeaf8cf392e`
- Metadata SHA-256: `d9ae3d6fb7702774c09f0d96f9161c7fb3ddbff4d5931fb48134b941ee2cdf9a`
- Blocks: 312
- Deterministic repair attempts: 0
