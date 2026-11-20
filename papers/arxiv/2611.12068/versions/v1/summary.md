# MIRIX-2.0: Multi-Agent Memory System

## Executive summary

MIRIX-2.0 separates immutable typed evidence from a provenance hypergraph used as a bounded index, while AutoDream consolidates entity identities and procedural skills outside the write path. Controlled conversational ablations favor the graph and AutoDream; document QA shows large gains on two tasks but a loss on DetectiveQA. Procedural-memory means lead on ALFWorld and WebShop, yet variance, category regressions, and unmatched MetaClaw baselines weaken causal claims. Efficiency evidence applies to the no-AutoDream M1 variant: it answers faster than HyperMem but makes document ingestion substantially slower. The architecture is promising and unusually traceable, but adoption should await full-system timing, component ablations, merge/provenance audits, and longer-history scaling tests.

## Problem

**Statement.** Long-horizon agents need to preserve exact user and task experience, connect related evidence, and reuse learned procedures without making retrieval grow with the entire history or allowing consolidation to destroy source records.

**Why it matters.** The paper frames practical memory as a three-way requirement: accurate recovery of details and relations, deployment without training and with traceable records, and bounded per-question latency and token cost. Existing consolidation, exhaustive retrieval, graph, file-system, and parametric approaches are argued to sacrifice at least one of these properties.

**Scope.** The study covers user-centric conversational recall, long-document QA, personalized review summarization and generation, plus agent-centric procedural transfer in interactive tasks. It evaluates complete system configurations rather than production deployment, privacy controls, or every individual mechanism.

## Method

MIRIX-2.0 uses a typed evidence plane as the durable system of record and a provenance-preserving n-ary hypergraph as an index for episodic and semantic records. A deterministic query planner selects an operator and fixed row budgets; retrieval enters through anchors, traverses base-recall and relation-citation lanes, and returns graph facts with cited source rows. AutoDream runs separately: semantic consolidation merges eligible entity anchors without rewriting evidence, while procedural consolidation distills judged task sessions into cited reusable skills.

### Key components

- A Meta Memory Manager routes inputs to six writers: Core, Episodic, Semantic, Procedural, Resource, and Knowledge Vault; only episodic and semantic records enter the hypergraph.
- Evidence records retain immutable row identifiers, text, event and mention times, provenance, and embeddings; database commitment precedes graph construction, making indexing fail-soft.
- The hypergraph represents entities or concepts as anchors and assertions as role-typed n-ary frames. Literals retain dates, prices, counts, durations, and measurements on the assertion they qualify.
- Episodic identity uses an explicit event time when available and otherwise an immutable memory identifier, preventing similarly worded undated occurrences from collapsing.
- Retrieval uses operator-specific budgets, anchor caps, predicate filtering, fact scoring, citation-first fusion, and an answer-time verification step that can request one extra search and rewrite.
- Semantic AutoDream considers a bounded frontier of newly written semantic rows, verifies candidate identity pairs, caches explicit rejections, transfers citations and edges on merge, and leaves stored memories unchanged.
- Procedural AutoDream judges transcripts using checked quotations, distills lessons and mistakes, and lets a curator create, edit, delete, defer, or decline skills with checked provenance.

### Assumptions

- Writer, extractor, identity-judge, distiller, curator, and answer-model decisions are sufficiently reliable inside deterministic safety boundaries.
- Fixed candidate and evidence caps preserve enough relevant information across different question operators and history lengths.
- The benchmark protocols and model-based judges adequately represent practical memory quality.
- Cross-method comparisons remain informative despite differing default embeddings and some baseline values not being rerun under a fully matched protocol.
- Preserving source rows and citations improves auditability, but the evaluation does not directly establish citation correctness or retained-detail completeness.

## Main claims

- **The architectural safety contract preserves committed evidence independently of graph indexing and makes returned graph facts traceable to source-memory identifiers.**
  - Evidence: [b00279-d2cdbbf02e] “Graph extraction is a fail-soft indexing hook, so a graph failure is logged but never rolls back a stored memory.”; [b00317-f4dc405442] “Every returned graph fact exposes the identifiers of its source memories.”
- **Bounded retrieval is enforced structurally through operator-dependent evidence budgets rather than by scanning the full history.**
  - Evidence: [b00293-541ae86bf1] “The evidence a question inspects is therefore bounded by its operator and not by the length of the history.”; [b00321-239b156233] “Retrieval and Dream both run under explicit candidate and output caps.”
- **AutoDream deliberately treats semantic and procedural memory differently: it structurally consolidates semantic identities without rewriting evidence, but refines task sessions into skills for procedural memory.**
  - Evidence: [b00102-1b1ef5d430] “Semantic Dream never rewrites the memories in the vector database, and it consolidates neither episodic-only anchors nor fact nodes.”; [b00104-834d9c0abd] “For procedural memory, AutoDream refines instead of merging.”

## Results

- **Conversational ablations show monotonic gains from flat memory to graph retrieval to graph plus AutoDream. On LoCoMo, accuracy moves from 85.7% to 88.4% to 91.4%; on LongMemEval-S, it moves from 58.8% to 70.0% to 72.6%. This is the strongest controlled component evidence, although these are configurations rather than repeated runs.**
  - Context: M0 is flat vector memory, M1 adds the hypergraph with AutoDream disabled, and M2 adds semantic AutoDream. User-memory results are single runs.
  - Evidence: [b00120-3f230e53d3] “On LoCoMo, graph retrieval raises overall accuracy from 85.7% for M0 to 88.4% for M1, and semantic AutoDream raises it to 91.4% for M2.”; [b00120-3f230e53d3] “On LongMemEval-S, the corresponding values are 58.8%, 70.0%, and 72.6%.”
- **With AutoDream disabled, MIRIX reaches 83.0% on SHDocQA and 71.0% on MHDocQA, exceeding HyperMem by 31.0 and 22.0 points. The advantage does not generalize to DetectiveQA: 64.8% trails MemoryBank at 67.6% and HyperMem at 66.2%, leaving retrieval failure versus reasoning failure unresolved.**
  - Context: The document evaluations test the combined M1 pipeline and cannot identify an AutoDream effect or isolate source-faithful writing from graph retrieval.
  - Evidence: [b00128-3235023416] “Its 83.0% on SHDocQA and 71.0% on MHDocQA exceed HyperMem by 31.0 and 22.0 points.”; [b00129-17094fefc8] “M1 reaches 64.8%, below MemoryBank’s 67.6% and HyperMem’s 66.2%.”; [b00129-17094fefc8] “Without an error analysis, we cannot distinguish missed evidence from failures to reason over retrieved evidence.”
- **Procedural memory has the highest observed mean success among compared memory methods: 76.4% on ALFWorld with GPT-6 Luna and 37.4% on WebShop. Evidence of stable superiority is weaker than the means suggest: ALFWorld has a 6.2-point spread, while some ALFWorld task types regress relative to no memory.**
  - Context: Interactive results average three runs with matched actor prompts and backbones within each comparison; procedural subcomponents are not separately ablated.
  - Evidence: [b00137-e98ddb9e28] “ALFWorld uses GPT-6 Luna and GPT-5.6 Luna; WebShop uses GPT-6 Luna.”; [b00161-1d81705644] “MIRIX-2.0 2.253±0.100 3.813±0.490 76.4±6.2”; [b00161-1d81705644] “MIRIX-2.0 1.815±0.054 4.975±0.340 37.4±2.1”; [b00141-34a5e860d3] “Pick, Look, and Pick Two remain below the no-memory scores.”
- **On MetaClaw-Bench with GPT-5.2, MIRIX-2.0 raises mean question score from 44.0% to 49.2% and file-check completion from 17.1% to 27.7%. With Qwen3.6-35B-A3B, the score changes from 51.8% to 52.7% and completion remains 30.8%, demonstrating backbone dependence; the GPT-5.2 comparison uses reported rather than controlled rerun baselines.**
  - Context: MetaClaw-Bench Part I combines partial-credit questions and file checks. No independent-run variation or matched procedural-component ablation is reported.
  - Evidence: [b00148-762ef58f06] “With GPT-5.2, MIRIX-2.0 improves the official mean question score from 44.0% for MetaClaw Skills to 49.2%, and file-check completion from 17.1% to 27.7%.”; [b00148-762ef58f06] “With Qwen3.6-35B-A3B, the score gain is smaller, from 51.8% to 52.7%, and completion is tied at 30.8%.”; [b00148-762ef58f06] “The GPT-5.2 baselines are reported values from the MetaClaw paper, so this comparison is not evidence from a fully controlled rerun.”
- **Efficiency is mixed and applies only to M1 without AutoDream. M1 answers faster than HyperMem on all five timed benchmarks, but document ingestion is 3.8 to 4.0 times slower than flat M0. It also uses 1.16M answer tokens on DetectiveQA versus 0.35M for HyperMem while having lower accuracy, so latency, token cost, and quality do not move together.**
  - Context: No timing characterizes the full M2 system; bounded evidence is a design property, not an empirical latency-scaling result over growing histories.
  - Evidence: [b00362-cbb92dcdf7] “Answering is faster for M1 than for HyperMem on all five benchmarks, by between 0.63 s per question on LongMemEval-S and 5.81 s on DetectiveQA”; [b00153-745f859da4] “Relative to M0, M1 increases ingestion time by 3.8 to 4.0 times across the three document tasks.”; [b00154-6eb3f16bb5] “It uses fewer answer tokens on SHDocQA and MHDocQA, but more on DetectiveQA, at 1.16M versus 0.35M.”

## Experimental evaluation

### Datasets

- LoCoMo conversational recall: 1,540 non-adversarial questions, broken into multi-hop, temporal, open, and single-hop categories.
  - Evidence: [b00121-7e76a47fce] “Table 1: LoCoMo accuracy (%) by question type on 1,540 non-adversarial questions.”
- LongMemEval-S conversational recall: 300 evaluated questions.
  - Evidence: [b00340-069b04a18a] “Table 7: LongMemEval-S accuracy (%) on the evaluated 300 questions.”
- MemoryAgentBench document QA: SHDocQA and MHDocQA use 100 questions each; DetectiveQA uses 71 questions.
  - Evidence: [b00338-d9a133481e] “SHDocQA and MHDocQA ask single-hop and multi-hop questions about long documents and use substring matching on 100 questions each, and DetectiveQA uses letter exact matching on 71 questions.”
- MemoryCD personalized review summarization and generation uses 100 Home_and_Kitchen users and evaluates cross-domain and single-domain memory.
  - Evidence: [b00133-320eb964e0] “Table 2: Review summarization on MemoryCD (100 Home_and_Kitchen users).”; [b00345-3c07e309b0] “cross-domain memory comes from the other three Amazon domains, and single-domain memory and testing use the same domain”
- ALFWorld and WebShop evaluate procedural transfer after memory learning on held-out interactive tasks.
  - Evidence: [b00137-e98ddb9e28] “Memory is then frozen for evaluation on 134 held-out ALFWorld episodes with a 50-step cap and 140 WebShop instructions with a 15-step cap.”
- MetaClaw-Bench Part I spans 30 days and contains 346 questions, including 224 file-check questions.
  - Evidence: [b00149-2177e4dd80] “Table 3: Agent memory on MetaClaw-Bench Part I (346 questions).”; [b00148-762ef58f06] “completion is the completion rate over the 224 file-check questions.”

### Baselines

- User-memory QA baselines are mem0, A-Mem, MemoryBank, Graphiti, and HyperMem.
  - Evidence: [b00112-e0c017dc7c] “We compare with mem0, A-Mem, MemoryBank, Graphiti, and HyperMem on QA”
- MemoryCD comparisons include long-context, RAG, mem0, A-Mem, MemoryBank, and Graphiti.
  - Evidence: [b00134-125a03503e] “Long-context .1493 .1357 .0162 .8745”; [b00134-125a03503e] “RAG .1559 .1430 .0145 .8735 .1670 .1523 .0196 .8759 mem0 .1526 .1420 .0159 .8749 .1593 .1472 .0184 .8767 A-Mem .1567 .1428 .0160 .8746 .1602 .1521 .0184 .8764 MemoryBank .1409 .1291 .0131 .8736 .1584 .1449 .0188 .8760 Graphiti .1534 .1415 .0139 .8741”
- Procedural-memory baselines are no memory, ReasoningBank, Agent Workflow Memory, and MetaClaw Skills where applicable.
  - Evidence: [b00137-e98ddb9e28] “comparing an agent without memory with ReasoningBank (Ouyang et al., 2026), Agent Workflow Memory (AWM) (Wang et al., 2025e), and MIRIX-2.0.”; [b00150-c3dfbfe3b7] “GPT-5.2 Baseline 41.1 14.7 MetaClaw Skills 44.0 17.1 MIRIX-2.0 49.2 27.7”

### Metrics

- User-memory QA uses accuracy; SHDocQA and MHDocQA use substring matching, DetectiveQA uses letter exact matching, and conversational QA uses an LLM judge with majority voting.
  - Evidence: [b00114-ea2d983943] “SHDocQA and MHDocQA use substring matching, and DetectiveQA uses letter exact matching.”; [b00114-ea2d983943] “LoCoMo and LongMemEval-S use a gpt-4o-mini judge with majority-of-3 voting.”
- MemoryCD uses ROUGE-1, ROUGE-L, BLEU-4, and BERTScore-F1.
  - Evidence: [b00114-ea2d983943] “MemoryCD uses ROUGE-1, ROUGE-L, BLEU-4, and BERTScore-F1.”
- Interactive agents report success, action steps, and training and test tokens, with mean and standard deviation over three runs.
  - Evidence: [b00116-0060b4ddea] “For interactive agents, we report success, action steps, and training and test tokens, with mean and standard deviation over three runs.”
- User-memory efficiency reports ingestion wall-clock time, mean retrieval-plus-answer time, answer tokens, and graph size where available.
  - Evidence: [b00116-0060b4ddea] “We report total ingestion wall-clock time, mean time to retrieve and answer a question, total answer tokens, and graph node and edge counts where available.”

### Ablations

- M0 is flat vector memory without graph or AutoDream; M1 adds graph indexing and retrieval; M2 adds AutoDream to the graph configuration.
  - Evidence: [b00109-c6e32136d2] “M0 uses flat vector memory without the graph or AutoDream”; [b00109-c6e32136d2] “M1 adds graph indexing and retrieval but disables AutoDream, and M2 is the full graph plus AutoDream configuration.”
- Conversational benchmarks compare all three variants, while document QA and graph-efficiency experiments use M1 only.
  - Evidence: [b00110-0c3420a9fa] “The conversational tables report all three configurations. The available document QA results and graph efficiency measurements use M1”
- Procedural experiments evaluate the combined judge, distiller, and curator path without subcomponent ablations.
  - Evidence: [b00138-a4638b5df9] “they do not separately ablate the outcome judge, experience distiller, or curator.”

### Negative results

- DetectiveQA is a clear exception: M1 trails MemoryBank and HyperMem.
  - Evidence: [b00129-17094fefc8] “M1 reaches 64.8%, below MemoryBank’s 67.6% and HyperMem’s 66.2%.”
- On ALFWorld with GPT-6 Luna, procedural memory hurts Pick, Look, and Pick Two relative to no memory.
  - Evidence: [b00141-34a5e860d3] “Pick, Look, and Pick Two remain below the no-memory scores.”
- ReasoningBank performs below no memory on both interactive benchmarks under GPT-6 Luna, showing that experience memory can be harmful.
  - Evidence: [b00144-a1601a4fc5] “ReasoningBank falls below no memory on both interactive benchmarks with GPT-6 Luna”
- Graph retrieval costs more than flat retrieval for document ingestion and answer latency.
  - Evidence: [b00153-745f859da4] “M1 also has higher answer latency than M0 on each task, so graph retrieval is not intrinsically cheaper than flat retrieval.”
- Procedural memory increases test-token use relative to no memory on both interactive benchmarks.
  - Evidence: [b00159-57413fcaa2] “Relative to no memory, test tokens rise on both benchmarks”


## Limitations

- Grouped ablations do not identify the effects of n-ary frames, cited rows, occurrence identity, answer verification, or individual procedural components; mechanistic explanations remain interpretations.
  - Evidence: [b00175-17663212c4] “Our ablations add components in groups.”; [b00175-17663212c4] “They do not isolate n-ary frames, cited source rows, occurrence identities, answer-time verification, or the judge, distiller, and curator of procedural memory”
- User-memory results are single runs and partly LLM-judged; agent results use only three runs and sometimes have large spreads; some baseline figures are taken from their authors.
  - Evidence: [b00175-17663212c4] “The user-memory results come from single runs, partly scored by an LLM judge, the agent results average three runs with large spreads, and some baselines are values reported by their authors.”
- Full M2 efficiency is unmeasured because every timing excludes AutoDream, preventing the paper's M1 latency findings from being assigned to the complete system.
  - Evidence: [b00359-7cae1922a0] “None of these measurements includes AutoDream, so they characterize M1 and not the full M2 system.”
- The evaluation does not measure merge precision, source-detail retention, skill-provenance coverage, six-writer routing contribution, memory length, or user-memory ingestion tokens.
  - Evidence: [b00164-78fc1d0aba] “The tables also do not measure merge precision, source-detail retention, skill provenance coverage, or the contribution of the six-writer routing policy”; [b00164-78fc1d0aba] “they do not report memory length or user-memory ingestion tokens”
- Bounded evidence access is not the same as empirically bounded latency; the study does not measure latency as history grows.
  - Evidence: [b00015-5bade6c9c8] “the retrieval bounds cover the evidence a question inspects, not latency measured as the history grows.”
- MemoryCD's automatic generation metrics do not directly test factual consistency, satisfaction of preferences, or user approval, and the recorded configuration cannot attribute gains to the graph or AutoDream.
  - Evidence: [b00132-138b085c9e] “They do not measure factual consistency, preference satisfaction, or user approval directly”; [b00132-138b085c9e] “the available configuration record does not support a MemoryCD-specific claim about graph or AutoDream gains.”
- The deployment-relevant privacy and integrity risks remain: personal data is sent to models, injected content may later be treated as trusted, and learned skills or merged identities require human review in high-stakes settings.
  - Evidence: [b00177-bce92d970f] “stored content is sent to the model.”; [b00177-bce92d970f] “content injected into a conversation can be stored and later retrieved as if it were trusted.”

## Reproducibility

**Status:** partial

The disclosed algorithm, constants, models, and tables support a serious reproduction attempt, and public code is claimed. Reproducibility remains partial because artifact versioning and raw outputs are absent, timing conditions are underspecified, important results lack repeated runs, and the complete system is not timed.

**Available artifacts**

- The metadata states that code is available in a public repository.
- The paper specifies principal user-memory models, temperature, seed, embedding model, scoring procedures, variant definitions, retrieval budgets, AutoDream thresholds and schedules, dataset sizes, and detailed result tables.
- Appendices describe storage technologies, algorithmic invariants, candidate caps, token accounting, and several implementation constants.

**Missing pieces**

- No immutable code commit or release identifier is supplied in the document blocks.
- Hardware, provider region, concurrency, database configuration, and other execution conditions needed to reproduce wall-clock timings are not stated in the supplied blocks.
- No per-example predictions, retrieval traces, merge decisions, learned skill artifacts, or raw run logs are identified.
- User-memory experiments lack repeated-run uncertainty; MetaClaw comparisons lack matched reruns and reported variation.
- The full AutoDream-enabled system lacks direct cost measurements.

## AIDB assessment

- Novelty: The strongest apparent novelty is the layered contract: complete typed records remain authoritative while a provenance-bearing n-ary hypergraph is only a bounded, fail-soft index; semantic consolidation rewires identity without rewriting records, while the same store also supports procedural skill refinement. The paper's first-system claim for jointly serving user- and agent-centric memory is author-asserted rather than independently established here.
- Usefulness: High for teams evaluating auditable long-term agent memory. The explicit provenance, fixed retrieval budgets, failure behavior, and broad evaluation make the design actionable. Current evidence is insufficient for production adoption where end-to-end cost, merge precision, privacy controls, stable procedural gains, and scaling behavior are decisive.
- Confidence: medium
- Recommended action: watch
- Rationale: The conversational ablation and two document-QA gains are compelling, and the architecture addresses traceability unusually directly. However, the full system lacks timing, component-level causality is unresolved, several comparisons are single-run or unmatched, and important negative results show that structured or procedural memory can increase cost or harm tasks. Reproduce and audit before adoption.

## Uncertainties

- **It is unknown whether gains attributed to graph structure arise from n-ary representation, source-row retention, retrieval heuristics, answer-time verification, or their interaction.** — Without factorial ablation, implementers cannot know which expensive components are necessary or whether a simpler design would retain the benefit.
  - Evidence: [b00164-78fc1d0aba] “The tables evaluate complete configurations, so the component explanations in this section remain interpretations”
- **The correctness of AutoDream identity merges and its actual effect on graph compression and evidence recall are not established.** — Incorrect merges can redirect retrieval even if source records remain intact, while negligible compression could add cost without practical benefit.
  - Evidence: [b00157-b5a389ae22] “Its total ingestion cost, answer cost, and graph reduction must be measured directly”; [b00164-78fc1d0aba] “The tables also do not measure merge precision, source-detail retention, skill provenance coverage”
- **Procedural-memory superiority over AWM may be unstable, especially on ALFWorld.** — Production decisions need a reliable improvement, not only the highest sample mean, and category-level regressions indicate possible negative transfer.
  - Evidence: [b00142-105c6aeec0] “It has the highest observed mean, but three runs do not establish a stable advantage over AWM.”
- **The system's latency and retrieval quality at much longer memory horizons remain unknown.** — Fixed output caps bound inspected evidence, but growing indexes, anchor ambiguity, database lookup cost, and cap-induced recall loss may still change operational behavior.
  - Evidence: [b00015-5bade6c9c8] “the retrieval bounds cover the evidence a question inspects, not latency measured as the history grows.”
- **The cause of the DetectiveQA deficit is unresolved.** — If retrieval misses evidence, indexing needs repair; if reasoning fails over correct evidence, further memory engineering may not solve the task.
  - Evidence: [b00129-17094fefc8] “we cannot distinguish missed evidence from failures to reason over retrieved evidence.”

## Open questions

- What are merge precision and recall, and how often does a wrong merge change the evidence returned for a query?
- Which individual components account for accuracy: source-faithful writing, n-ary frames, occurrence identity, citation-balanced retrieval, or answer-time verification?
- How do end-to-end M2 ingestion time, query latency, token use, graph size, and accuracy compare with M1 and HyperMem?
- Does fixed-budget retrieval preserve recall and latency as histories grow by orders of magnitude?
- What fraction of procedural skill statements have valid provenance, and which retrieved skills cause task-level improvements or regressions?
- Would matched reruns with identical models, embeddings, prompts, infrastructure, and multiple seeds preserve the reported advantages?
- How should user deletion, correction, access control, and poisoning defenses propagate through evidence rows, graph citations, aliases, and learned skills?

## Proposed AIDB experiments

- **Hypothesis:** The n-ary hypergraph and cited-row retrieval each contribute independently to multi-hop and temporal accuracy, while answer-time verification contributes mainly to count and intersection questions.
  - Baseline: A matched M1 implementation with a factorial ablation of n-ary frames, cited-row fusion, occurrence identity, and answer-time verification; hold writers, models, embeddings, prompts, budgets, and seeds fixed.
  - Primary metric: Paired per-question accuracy by question type, accompanied by retrieval recall of gold-supporting rows and mean answer latency.
  - Stop condition: Stop when confidence intervals from repeated seeds separate each component's effect from zero or when the interval is narrow enough to rule out a practically meaningful gain chosen before the run.
- **Hypothesis:** Full M2 improves entity-linked recall and reduces graph fragmentation without materially degrading source-detail recovery, but adds measurable ingestion cost.
  - Baseline: M1 without AutoDream, evaluated against M2 on identical ingestion streams and query sets at several controlled history lengths.
  - Primary metric: End-to-end accuracy together with merge precision, source-detail recall, graph-node reduction, ingestion time, and answer latency.
  - Stop condition: Reject deployment if any tested scale shows unacceptable source-detail loss or merge precision below a pre-registered safety threshold; otherwise stop after latency and accuracy trends stabilize across consecutive history-length levels.
- **Hypothesis:** Procedural gains depend on skill quality and can be improved by suppressing skills that cause negative transfer.
  - Baseline: Current procedural AutoDream versus no memory, AWM, and a gated MIRIX variant that retrieves no skill when a calibrated relevance score is low; use matched tasks, prompts, backbones, and substantially more independent runs.
  - Primary metric: Held-out success rate with paired task-level regressions and token cost per additional successful episode.
  - Stop condition: Stop when the gated variant either shows a stable success improvement without increasing regression frequency or fails a pre-registered futility boundary across both interactive benchmarks.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:08.953842+00:00`
- Document SHA-256: `0bc02ed4b852cf0b8067b3092451b7d3eedef4f520ab08e57ec86e50b445282b`
- Metadata SHA-256: `cbc60e5b8d43828f0b60fdd9fe4e4e0013e067261bac57305e2c82bcc6418abe`
- Blocks: 363
- Deterministic repair attempts: 0
