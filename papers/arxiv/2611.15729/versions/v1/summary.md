# DISCERN: Preserve at Write, Resolve at Read for Persistent LLM-Agent Memory

## Executive summary

DISCERN reframes persistent memory as preservation at ingestion and query-specific resolution at read time. Its append-only event log feeds rebuildable entity-family, bi-temporal fact, and episodic views; an agent navigates deterministic tools before committing to answer, update, clarify, or abstain. It leads the paper’s ENT-310 macro correctness and abstention evaluations and transfers competitively to LoCoMo. The strongest evidence is the controlled eight-baseline comparison plus navigation ablations. Confidence is tempered by a synthetic primary benchmark, only 15 entity-resolution items, unequal seed counts, LLM-built graph views, judge-model evaluation, backbone sensitivity, and incomplete release details.

## Problem

**Statement.** Persistent enterprise-agent memories contain contradictory, superseded, and similarly named facts. The paper argues that retrieving relevant evidence is insufficient: the reader must resolve the intended entity, select the applicable time-state, and decide whether evidence warrants an answer or a decline.

**Why it matters.** A system may retrieve the correct passage yet still blend entities, report a stale value, hallucinate an absent attribute, or decline an answerable query. Evaluating only retrieval therefore misses the terminal decision that users actually experience.

**Scope.** The study covers warm-start conversational memory, with controlled evaluation on synthetic enterprise sales sessions and zero-tuning transfer to personal multi-session conversations. It evaluates answer correctness separately from answer-versus-abstain calibration; it does not establish performance on live enterprise data or arbitrary memory backends.

## Method

DISCERN separates a lossless write path from an adaptive read path. Each actor has an immutable event log. LLM extraction materializes rebuildable graph views without merging similar entities or deleting superseded values. At query time, an agent traverses profile, entity/session, fact, and transcript levels through deterministic read-only tools. Graph predicates and governance gates constrain the final action to answer, update, clarify, or abstain, with cited evidence required for committed answers.

### Key components

- An immutable, append-only per-actor event log serves as the source of truth; derived views can be rebuilt from it.
- Schema-free extraction creates entity, attribute, and value representations; similarly named entities remain separate but connected by SIMILAR_NAME edges.
- Bi-temporal fact edges retain both recording time and validity intervals; superseded values are soft-invalidated rather than erased.
- The read policy adaptively uses profile orientation, similar-entity search, temporal-chain inspection, targeted fact lookup, enumeration, hybrid retrieval, and transcript access.
- EarnedAnswerGate, EarnedAbstainGate, DeclineRouter, a near-miss guard, and citation-or-abstain rendering govern terminal commitments.
- A four-model judge council scores answer correctness and answer-versus-abstain classification.

### Assumptions

- The LLM-extracted graph contains sufficiently correct entities, facts, attributes, edges, and supersession chains for deterministic gates to operate meaningfully.
- An actor-specific memory scope is appropriate and cross-actor evidence should not be used.
- Similar-name candidate generation and its configurable threshold expose the relevant confusable entities without destructive merging.
- The four-judge council is an adequate proxy for human correctness assessment despite only substantial, not perfect, inter-judge agreement.
- Equal weighting of capability pillars is the appropriate headline aggregation because the recall-oriented pillars are near saturation.

## Main claims

- **The authors’ central claim is that persistent-memory performance is limited more by resolution and terminal commitment than by retrieval ranking.**
  - Evidence: [b00008-ed7eb3e7e6] “On these benchmarks, recall is largely solved; resolution is not.”; [b00008-ed7eb3e7e6] “Those numbers measure whether the evidence was retrieved, not whether the committed answer was right”
- **DISCERN preserves potentially conflicting evidence at write time and postpones irreversible, query-dependent resolution until read time.**
  - Evidence: [b00009-e473553f88] “Confusable entities are linked but never merged, superseded facts are invalidated softly rather than deleted”; [b00009-e473553f88] “Read time then carries the query-specific resolution”
- **The terminal decision is governed by graph-computable predicates rather than an unconstrained judgment over retrieved prose.**
  - Evidence: [b00039-cbe5365eac] “the committed action reduces to a decidable function of the graph rather than a judgment over retrieved prose”; [b00041-05950263c0] “Eq. 1 is the decision rule given that graph rather than a claim of ground-truth correctness”
- **The evaluation deliberately separates correctness on answerable questions from calibration of non-commitment on false-premise or otherwise unanswerable questions.**
  - Evidence: [b00050-371beb1f19] “We report two axes. Answer correctness is accuracy on the answerable questions.”; [b00050-371beb1f19] “The answer-versus-abstain decision is scored as a classification problem”

## Results

- **On ENT-310, DISCERN achieves macro answer correctness of 0.861 versus 0.806 for Extract-Retrieve and 0.788 for RAG-Agentic. Its entity-resolution score is 0.800, while the strongest reported baseline value is 0.400.**
  - Context: This is an equal-weight mean across retention, currency, contamination, and entity resolution on answerable queries. The aggregation prevents the larger, near-saturated recall pillars from dominating, but the entity-resolution subset is small.
  - Evidence: [b00053-73e4d2d80a] “Table 1: ENT-310 answer correctness on the 210 answerable queries, four-judge council.”; [b00054-b9f9bede20] “DISCERN 0.861 0.929 0.900 0.817 0.800 Extract-Retrieve 0.806 0.976 0.975 0.873 0.400 RAG-Agentic 0.788”; [b00053-73e4d2d80a] “The average is the macro (equal-weight) mean over the four pillars”
- **On ENT-310 answer-versus-abstain classification, DISCERN reports precision 0.938, recall 0.910, F1 0.924, and false-decline 0.029; the next-highest F1 is HippoRAG2 at 0.802.**
  - Context: The positive class consists of unanswerable queries, while false-decline measures answerable queries incorrectly declined. This joint view exposes systems that obtain high recall by refusing too often.
  - Evidence: [b00055-6b259e76b7] “Table 2: ENT-310 answer-versus-abstain as classification, four-judge council”; [b00056-09807c83f2] “DISCERN 0.938 0.910 0.924 0.029 HippoRAG2 0.890 0.730 0.802 0.043”; [b00055-6b259e76b7] “False-decline is the fraction of answerable queries wrongly declined (lower is better).”
- **With zero tuning on LoCoMo, DISCERN records macro answer correctness of 0.663 versus 0.638 for HippoRAG2. Its abstention F1 is 0.820, slightly below RAG-Agentic at 0.827 and above HippoRAG2 at 0.805.**
  - Context: Transfer supports generality beyond the enterprise benchmark, but DISCERN does not lead the LoCoMo abstention axis. The strongest interpretation is combined accuracy and calibration, not universal metric dominance.
  - Evidence: [b00063-509b6cb739] “DISCERN 0.663 0.815 0.713 0.592 0.531 HippoRAG2 0.638”; [b00065-3edfe67f55] “RAG-Agentic 0.879 0.780 0.827 0.031 DISCERN 0.875 0.772 0.820 0.032 HippoRAG2 0.917 0.717 0.805 0.019”; [b00060-de17cafe22] “Applied with zero tuning to the full LoCoMo corpus”
- **The navigation ablation rises from a tools-off overall accuracy of 0.329 to 0.887 in the full setting. Removing find_similar_entities yields overall accuracy 0.877 but worsens unanswerable accuracy to 0.72 and over-commitment to 0.28.**
  - Context: This is the clearest mechanism test for the read policy and ambiguity operator. It is weaker than the headline evaluation because it uses a single seed and shared judge, and the reported navigation condition excludes the deterministic governance gate.
  - Evidence: [b00071-d6d235eb4e] “Full (8 turns, 3 tools/turn) 0.887 0.933 0.79 0.21”; [b00071-d6d235eb4e] “− find_similar_entities 0.877 0.933 0.72 0.28”; [b00071-d6d235eb4e] “Tools-off (parametric floor) 0.329 0.133 1.00 0.00”; [b00069-bd934387a3] “These ablations use one Sonnet judge and one seed with the governance gate disabled”

## Experimental evaluation

### Datasets

- ENT-310: a frozen synthetic enterprise sales-memory benchmark with answerable questions across retention, currency, contamination, and entity resolution, plus unanswerable attribute-swap and near-miss traps. Confusable companies are intentionally placed inside an actor’s memory.
  - Evidence: [b00046-2f7d107747] “ENT-310 is a frozen enterprise sales-memory benchmark: 10 sales users, 50 target companies, and 31 warm-start sessions”; [b00046-2f7d107747] “Its 210 answerable queries span four pillars”; [b00046-2f7d107747] “A further 100 unanswerable queries probe calibrated abstention”
- LoCoMo: an out-of-domain personal-conversation corpus used without tuning. It covers single-hop, multi-hop, temporal, open-domain, and adversarial categories but does not test entity contamination.
  - Evidence: [b00046-2f7d107747] “LoCoMo [4] is an out-of-domain corpus of personal multi-session conversations (1,986 questions”; [b00046-2f7d107747] “used with zero tuning as a transfer test”; [b00046-2f7d107747] “it exercises recall and reasoning but not entity contamination”

### Baselines

- Lossless retrieval readers: BM25, Dense, reciprocal-rank fusion, and an agentic RAG ReAct loop; these preserve the per-actor corpus and retrieve passages.
  - Evidence: [b00048-dd53d7fee4] “Four lossless readers index a per-actor corpus that discards nothing at write time”; [b00048-dd53d7fee4] “BM25, Dense (a commercial dense embedding model), RRF”; [b00048-dd53d7fee4] “an Agentic RAG ReAct loop issuing multiple searches”
- Extract-and-retrieve baseline: SEM+SUM+QE, using semantic memories, summaries, and query enrichment with top-k retrieval.
  - Evidence: [b00048-dd53d7fee4] “SEM+SUM+QE is an extract-and-retrieve reader in its full semantic-plus-summary-plus-query-enrichment profile (top-​k=10)”
- Graph and agent-memory systems: GraphRAG, HippoRAG2, and Mem0.
  - Evidence: [b00048-dd53d7fee4] “GraphRAG [2], HippoRAG2 [3], and Mem0 [1] are graph- and agent-based memory systems.”

### Metrics

- Answer correctness: judge-council accuracy on answerable questions, aggregated as an equal-weight macro mean across benchmark pillars or categories.
  - Evidence: [b00050-371beb1f19] “Answer correctness is accuracy on the answerable questions.”; [b00052-0fa2a592ba] “We report answer correctness as the macro (equal-weight) mean over the four pillars”
- Answer-versus-abstain classification: precision, recall, F1, and false-decline rate, with unanswerable or false-premise queries as the positive non-commitment class.
  - Evidence: [b00050-371beb1f19] “precision, recall, F1, and a false-decline rate”; [b00055-6b259e76b7] “the 100 unanswerable queries are the positive class (should not commit)”
- Four-judge majority vote using Claude Sonnet, Claude Opus, Qwen, and GPT-oss; reported agreement with the Sonnet judge is substantial rather than perfect.
  - Evidence: [b00050-371beb1f19] “Every reported metric is scored by a four-judge council, a majority vote over Claude Sonnet 4.6, Claude Opus 4.8, Qwen3-235B, and GPT-oss-120B”; [b00050-371beb1f19] “Cohen’s κ of 0.61 to 0.80 against the Sonnet judge”

### Ablations

- Navigation-depth and tools-off ablation: shallow readers collapse to the abstaining floor, while deeper navigation substantially raises overall and entity-resolution accuracy.
  - Evidence: [b00069-bd934387a3] “With one or two turns the system collapses to 0.33, identical to the tools-off floor”; [b00069-bd934387a3] “Four turns reach 0.78, eight reach 0.89”
- Leave-one-operator-out and per-turn tool-budget ablations: single operator removal changes overall accuracy modestly, but removing similar-entity search harms abstention calibration.
  - Evidence: [b00069-bd934387a3] “DISCERN is robust to removing any single operator (0.88 to 0.91)”; [b00069-bd934387a3] “the exception is find_similar_entities, whose removal keeps accuracy high but degrades abstention (over-commit →0.28)”
- Backbone sensitivity: performance is comparable on the two Anthropic backbones and materially lower on the tested Qwen and open-weight OpenAI backbones.
  - Evidence: [b00073-3e8a16a926] “Sonnet 4.6 0.887, Opus 4.8 0.890”; [b00073-3e8a16a926] “drops on Qwen3-235B (0.707) and the open-weight OpenAI model (0.610)”

### Negative results

- Very shallow navigation does not improve on the parametric floor and tends to abstain on nearly everything.
  - Evidence: [b00069-bd934387a3] “With one or two turns the system collapses to 0.33, identical to the tools-off floor: it cannot gather evidence and abstains on nearly everything.”
- DISCERN does not have the best abstention F1 on LoCoMo; RAG-Agentic is slightly higher.
  - Evidence: [b00065-3edfe67f55] “RAG-Agentic 0.879 0.780 0.827 0.031 DISCERN 0.875 0.772 0.820 0.032”
- The method is sensitive to backbone capability, with weaker tool use and structured-output adherence associated with worse results.
  - Evidence: [b00073-3e8a16a926] “its agentic tool-use and structured governance interact with model capability”; [b00073-3e8a16a926] “weaker tool-use and structured-output adherence degrade contamination handling and grounding”
- Mem0’s high non-commitment recall on ENT-310 is accompanied by extensive false declines, illustrating that recall alone rewards reflexive refusal.
  - Evidence: [b00052-0fa2a592ba] “Mem0 reaches recall 0.990 but false-declines 0.867 of the answerable queries”


## Limitations

- The primary benchmark is synthetic and generated with a model, so its dialogue patterns, ambiguities, and error distribution may not represent deployed enterprise memory.
  - Evidence: [b00091-39ce45db2d] “The corpus is synthetic and generated in three stages with Claude Opus 4.8.”
- The entity-resolution pillar is small, making its large apparent advantage directional rather than a precise effect estimate.
  - Evidence: [b00067-a1e47e409a] “Per-pillar counts on ENT-310 are small (entity resolution n=15), so pillar-level differences are directional.”
- Seed coverage is unequal: headline DISCERN and HippoRAG2 results average multiple runs, while other baselines use only one, weakening variance-aware comparisons.
  - Evidence: [b00067-a1e47e409a] “DISCERN and HippoRAG2 headline numbers are three-seed means (sd 0.004 and 0.002); the remaining baselines are single-seed.”
- The navigation ablation has reduced evaluation rigor because it uses one seed, one judge, and disables the governance gate.
  - Evidence: [b00069-bd934387a3] “These ablations use one Sonnet judge and one seed with the governance gate disabled”
- The deterministic decision rule inherits errors from LLM extraction; graph-decidable commitment is not equivalent to ground-truth correctness.
  - Evidence: [b00041-05950263c0] “The predicates |C|, active⁡(⋅), and ℓ⁡(⋅) are computed over the LLM-extracted graph”; [b00041-05950263c0] “rather than a claim of ground-truth correctness”
- Transfer evaluation does not test entity contamination, the capability most aligned with DISCERN’s design and strongest claimed advantage.
  - Evidence: [b00046-2f7d107747] “it exercises recall and reasoning but not entity contamination”
- Read-time operation adds several navigation turns, tool calls, and nontrivial latency; the hardest entity-resolution queries cost more.
  - Evidence: [b00067-a1e47e409a] “DISCERN averages 4.1 navigation turns and 5.7 tool calls per query”; [b00067-a1e47e409a] “at a mean read latency of 7.6 s”; [b00067-a1e47e409a] “entity-resolution queries, 8.5 tool calls”
- Evaluation relies on LLM judges, and measured inter-judge agreement leaves meaningful disagreement.
  - Evidence: [b00050-371beb1f19] “inter-judge agreement is substantial (Cohen’s κ of 0.61 to 0.80 against the Sonnet judge)”

## Reproducibility

**Status:** partial

The paper provides unusually concrete architectural and evaluation descriptions, including its navigation prompt and several ablations, so conceptual reimplementation is plausible. Exact numerical reproduction is not supported by the supplied material because essential code, data access, model settings, baseline manifests, and raw outputs are absent.

**Available artifacts**

- A detailed read-time system prompt is included in the supplied document.
- The paper specifies datasets, query categories, baseline families, judge council, terminal actions, and headline evaluation protocol.
- ENT-310 construction stages, frozen set composition, actor scoping, and human vetting are described.
- Tables report store composition, navigation settings, tool budgets, backbone variants, and read-time cost.
- The reference implementation’s storage choice is identified as one SQLite file per actor.

**Missing pieces**

- No code repository, executable package, or archival artifact is identified in the supplied metadata or blocks.
- No downloadable ENT-310 dataset location or license is provided.
- No exact model endpoints, decoding parameters, random seeds, embedding model identity, or prompt set for every extraction and judging stage is supplied.
- No complete baseline configuration and version manifest is supplied, including the unnamed commercial dense embedding model.
- No raw predictions, per-question judge votes, confidence intervals, or statistical significance tests are supplied.
- The configurable similar-name threshold is described but its validated numeric setting is not reported.
- Compute requirements, write-time extraction cost, and full end-to-end cost are not reported.

## AIDB assessment

- Novelty: The most distinctive contribution is the combined contract: lossless, reversible graph construction at write time; adaptive tool navigation at read time; and explicit, deterministic governance of answer, update, clarify, or abstain. Individual elements are familiar, but their integration and terminal-decision evaluation are meaningfully differentiated.
- Usefulness: High for builders of long-lived agents facing entity collisions, supersession, and false-premise queries. The separate correctness and abstention axes are especially useful as an evaluation template. Adoption should wait for validation on real organizational data, released artifacts, and cost-controlled comparisons.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled comparisons, transfer test, negative results, and mechanism ablations make the paper decision-relevant. However, the central advantage is demonstrated primarily on a synthetic benchmark with a very small entity-resolution slice; graph quality depends on LLM extraction, baseline seeds are unequal, and exact reproduction is not currently supported by the supplied material.

## Uncertainties

- **It is unclear how much of the gain comes from the memory representation, the navigation prompt, the deterministic governance gates, or their interaction.** — The paper claims the read policy drives performance, but the principal ablation disables governance and does not fully cross store, policy, and gates under the headline council protocol.
  - Evidence: [b00069-bd934387a3] “These ablations use one Sonnet judge and one seed with the governance gate disabled”; [b00069-bd934387a3] “re-enabling the deterministic gate raises unanswerable accuracy from 0.79 to ∼0.96”
- **The robustness of graph construction to extraction errors, attribute synonyms, aliases, and excessive node drift is not quantified.** — Deterministic commitment can only be as reliable as the candidate sets, active facts, and temporal chains produced by extraction and consolidation.
  - Evidence: [b00030-384f5acd29] “Its only failure mode is extra nodes (drift)”; [b00041-05950263c0] “The predicates |C|, active⁡(⋅), and ℓ⁡(⋅) are computed over the LLM-extracted graph”
- **The claimed benchmark advantage may change under matched multi-seed runs and human adjudication.** — Most baselines are single-seed, while the primary scorer is an LLM council with incomplete agreement; neither uncertainty intervals nor human comparison are reported.
  - Evidence: [b00067-a1e47e409a] “the remaining baselines are single-seed”; [b00050-371beb1f19] “Cohen’s κ of 0.61 to 0.80 against the Sonnet judge”
- **The operational tradeoff between improved resolution and added latency or model/tool cost remains unresolved.** — Enterprise adoption depends on whether gains persist under stricter latency and budget constraints, especially for ambiguous queries.
  - Evidence: [b00067-a1e47e409a] “at a mean read latency of 7.6 s”; [b00067-a1e47e409a] “the eight-turn budget binds on 1.4% of queries”

## Open questions

- How does DISCERN compare with the same baselines when every system receives matched seeds, model budgets, latency budgets, and complete hyperparameter disclosure?
- What are entity-resolution and abstention results on real enterprise conversations with naturally occurring aliases, typos, organizational changes, access-control boundaries, and incomplete records?
- How accurately does the write path construct entities, similar-name families, attributes, and temporal chains, and which extraction errors most often cause terminal-decision failures?
- Would human judges reproduce the council’s rankings and its treatment of clarification, premise correction, partial answers, and cited evidence?
- How do write-time extraction cost, storage growth, graph drift, and query latency scale across months or years of sessions?
- What numeric similar-name threshold was used, and how sensitive are contamination, clarification, and abstention to that threshold?
- Can a trained routing policy reduce tool calls and latency without sacrificing calibration or grounding?

## Proposed AIDB experiments

- **Hypothesis:** DISCERN’s advantage persists on naturally occurring enterprise memory, rather than depending on synthetic entity pairs and generated dialogue structure.
  - Baseline: Run DISCERN, SEM+SUM+QE, HippoRAG2, and RAG-Agentic with matched backbones, budgets, and at least five seeds on a de-identified human enterprise corpus; use independent human adjudication.
  - Primary metric: Equal-weight macro answer correctness plus abstention F1, with entity-resolution accuracy and false-decline rate reported separately with bootstrap confidence intervals.
  - Stop condition: Reject the hypothesis if DISCERN’s confidence interval overlaps the strongest baseline on both macro correctness and abstention F1, or if its entity-resolution advantage disappears.
- **Hypothesis:** The full gain requires both adaptive navigation and deterministic governance, not merely the graph store or a stronger prompt.
  - Baseline: A factorial study crossing DISCERN versus lossless stores, fixed retrieval versus adaptive navigation, and governance gates off versus on, under the same backbone, judge council, seeds, and tool budget.
  - Primary metric: Answer correctness, abstention F1, false-decline rate, over-commit rate, tool calls, and latency for each factorial cell.
  - Stop condition: Stop attributing the gain to the combined design if navigation and gates show no reproducible main effects or interaction after matched-seed confidence intervals are computed.
- **Hypothesis:** Graph-extraction errors and similar-name threshold choice are the dominant remaining failure sources, and calibrated uncertainty can improve outcomes without excessive clarification.
  - Baseline: Compare the current fixed-threshold graph with threshold sweeps and an uncertainty-aware candidate generator on manually annotated entity links, attributes, and supersession chains.
  - Primary metric: End-to-end entity-resolution accuracy and abstention F1, accompanied by graph entity-link precision/recall, temporal-chain accuracy, clarification rate, and storage growth.
  - Stop condition: Stop if no threshold or uncertainty-aware variant improves end-to-end calibration without reducing answer correctness or causing materially higher graph growth and clarification rates.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:14:14.160284+00:00`
- Document SHA-256: `2097e5a9c2f7004c4213d7553235396a4987d8bf9c1988c2c44527b937cb77c6`
- Metadata SHA-256: `f7653b9914be7428a2ca71f03e89f6e3f865e0f0f4ea1ed542c63ac8cec14cf4`
- Blocks: 104
- Deterministic repair attempts: 1
