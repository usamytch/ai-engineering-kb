# Weekly discovery — 2026-W35

> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.
>
> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.

Сгенерировано: 2026-08-24T07:31:33+00:00

## Кандидаты

- [ ] **[AI with Authority, from Application to Silicon](https://arxiv.org/abs/2608.21356v1)**
  <!-- aidb:id=arxiv:2608.21356v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Jason Hickey
  - Categories: cs.SE, cs.AI, cs.AR, cs.LO
  - Abstract: For sixty years, machine verification has been a major cost overhead, affordable only for exceptional artifacts. Here we report that generative AI inverts this relationship: at AI speed, machine verification is not only economical but essential to productivity --- it is the incorruptible referee that lets one person safely direct autonomous machine work at scale. In five weeks, one researcher on consumer AI subscriptions directed a small fleet of AI agents from application code, through a verified compiler and executive, to a RISC-V processor taped out on a community silicon shuttle; no proof passed through human review, and no RTL was written by a human. The working discipline --- the Salt…
  - Comment: 17 pages, 6 figures
- [ ] **[Asymmetric Capacity Allocation in Self-Refinement Pipelines](https://arxiv.org/abs/2608.21345v1)**
  <!-- aidb:id=arxiv:2608.21345v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Zhuoyi Yang, Ian G. Harris, Salar Hashemitaheri, Cassie Huang, Yuangang Li, Hyunwoo Oh, Paul Dourish, Tony Givargis, Mohsen Imani, Li Zhang
  - Categories: cs.LG
  - Abstract: Self-refinement, typically structured as generation, critique, and revision, is a widely adopted paradigm for improving LLM generation and serves as a core mechanism in many LLM agents. While the three stages involve different cognitive demands, most existing approaches conveniently treat the model size as an implementation detail rather than a subject of study, which may lead to a waste of resources. Little work has systematically examined how model size affects each stage or whether effective self-refinement requires equally capable models for generation, critique, and revision. We present the first stage-wise model size study of the self-refinement pipeline on 5 benchmarks from different…
- [ ] **[Natural-Language Workflows Are Not Software Yet: Artifact-Driven Compilation for Reliable Agent Execution](https://arxiv.org/abs/2608.21341v1)**
  <!-- aidb:id=arxiv:2608.21341v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Xiangzhe Xu, Hanxi Guo, Guangyu Shen, Siyuan Cheng, Xiangyu Zhang
  - Categories: cs.SE
  - Abstract: Natural-language workflows offer a software-like interface for agents: domain experts can write reusable procedures, and agents can execute them as instructions. This promise is not yet reliable. Workflow descriptions often leave data dependencies implicit, so the executor must infer which prior results a step should use; agents can also fail to follow long or branching instructions under context pressure. We propose Artic, an artifact-driven workflow compiler that transforms a natural-language workflow into an artifact-driven workflow in which each step declares the artifacts it reads and writes, constraints gate produced artifacts, and explicit control transfers route execution. This repr…
  - Comment: The first two authors contributed equally
- [ ] **[Invisible Agents, Uninformed Patients: Towards Responsible Deployment Of Autonomous AI Diagnostic Agents In Sub-Saharan Africa](https://arxiv.org/abs/2608.21326v1)**
  <!-- aidb:id=arxiv:2608.21326v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Percy Brown, Kweku Yamoah
  - Categories: cs.CY
  - Abstract: Autonomous AI diagnostic agents, systems that analyse patient-specific clinical data and produce diagnostic outputs or triage decisions without mandatory real-time human review, are increasingly deployed across eHealth platforms in sub-Saharan Africa at a pace that has outrun the governance infrastructure needed to oversee them. While significant bodies of work address AI accountability, transparency and explainability in healthcare, existing frameworks are largely clinician-centered and assume regulatory conditions that do not uniformly exist in low-resource settings. A patient-centered analysis of the disparity in patient awareness regarding autonomous agents, which results in a structura…
  - Comment: 10 pages, 4 figures
- [ ] **[AI-to-AI Code Reviews of GitHub Pull Requests](https://arxiv.org/abs/2608.21311v1)**
  <!-- aidb:id=arxiv:2608.21311v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Niruthiha Selvanayagam, Taher A. Ghaleb
  - Categories: cs.SE
  - Abstract: AI coding agents are increasingly integrated into software development workflows, operating on both sides of the pull-request (PR) process: AI authoring agents create or modify PRs, while AI reviewers evaluate them. This creates a closed loop in which one AI coding agent reviews a contribution attributed to another. We construct a large-scale dataset of AI-to-AI code review by linking AI-attributed PRs with AI-attributed review events from CodAGE, a public dataset of coding-agent-generated GitHub events. Our dataset contains 248,641 unique AI-attributed PRs that received at least one AI-attributed review. Of these, 45,269 received cross-product review and 208,145 received same-product revie…
  - Comment: Accepted at the 20th International Symposium on Empirical Software Engineering and Measurement (ESEM 2026), Emerging Results, Vision, and Reflection Papers Track
- [ ] **[Beyond Fault Localization: A Trajectory-Level Study of LLM Agents for Microservice Root Cause Analysis](https://arxiv.org/abs/2608.21310v1)**
  <!-- aidb:id=arxiv:2608.21310v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Qisheng Lu, Aoyang Fang, Junjielong Xu, Jin'ao Shang, Songhan Zhang, Yifan Yang, Xiaochuan Yan, Pinjia He
  - Categories: cs.SE
  - Abstract: Existing evaluations of automated root cause analysis (RCA) for microservices assess diagnostic performance mainly by endpoint correctness: whether a method localizes the responsible service. This criterion enables comparison but does not reveal the evidentiary basis of a diagnosis or the fault-propagation route connecting the source to observed symptoms, both of which an on-call site reliability engineer needs to judge whether action is warranted. We therefore treat RCA as an observable diagnostic process. Our trajectory-level framework evaluates agent executions against manually curated service-level fault-propagation paths. Applied to a public microservice RCA benchmark, it analyzes 3,50…
  - Comment: 13 pages, 7 figures, 5 tables
- [ ] **[AUSO: Action-Level Unified Skill Optimization from Internalization to Utilization](https://arxiv.org/abs/2608.21292v1)**
  <!-- aidb:id=arxiv:2608.21292v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Huizu Lin, Chengkai Huang, Tianqi Gao, Tao Huang, Daijiao Liu, Tongxin Li, Xiaoyan Sun, Lina Yao
  - Categories: cs.AI
  - Abstract: Skills play different roles as an agent's policy evolves: they should first provide learnable knowledge, then support capability formation, and finally be invoked only when they improve individual decisions. Existing methods rarely model this lifecycle. They either keep skills outside the model, fully internalize them, or select among internalization and utilization objectives through noisy task-level success rates. Such designs fragment training and assign uniform importance to actions within the same trajectory, even though skill guidance may help some decisions while distracting others. To solve these problems, we introduce AUSO (Action-level Unified Skill Optimization), which unifies sk…
- [ ] **[EnSI-RAG: Entity-Structure-Indexed Retrieval-Augmented Generation for Long-Document Question Answering](https://arxiv.org/abs/2608.21252v1)**
  <!-- aidb:id=arxiv:2608.21252v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Xuanyu Meng, Jiashuo Sun, Jash Rajesh Parekh, Jiawei Han
  - Categories: cs.CL, cs.AI, cs.DB, cs.IR
  - Abstract: Question answering (QA) over long, connected documents remains challenging because relevant evidence may span multiple entities and their relationships. Existing retrieval-augmented generation (RAG) methods typically index documents as raw chunks and retrieve them through embedding similarity. Their performance degrades when chunk boundaries separate entities from supporting evidence or when a question requires multi-hop reasoning across the corpus. We propose EnSI-RAG (Entity-Structure-Indexed Retrieval-Augmented Generation), a framework that constructs a query-independent, entity-centered index. Each record (e, t, k, v) represents an entity e, its type t, a semantic category k in {propert…
  - Comment: 21 pages, preprint
- [ ] **[Benchmarking Patent Drafting from Inventor-Style Disclosures](https://arxiv.org/abs/2608.21249v1)**
  <!-- aidb:id=arxiv:2608.21249v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Lekang Jiang, Wenjun Sun, Stephan Goetz
  - Categories: cs.CL
  - Abstract: While recent large language models (LLMs) have achieved promising results on individual patent drafting tasks, they fundamentally fail to investigate the core challenge of real-world patent drafting: generating a complete and legally coherent patent application directly from early-stage invention materials. Prior work predominantly assumes later-stage, highly structured, or already legalistic inputs. However, real patenting workflows begin with informal, de-legalized disclosures authored by inventors. To bridge the gap, we introduce Dis2Pat, a disclosure-to-patent dataset that reflects realistic patenting workflows by requiring the generation of complete patent applications directly from in…
  - Comment: Accepted to EMNLP 2026
- [ ] **[Just Noticeable Difference Modeling for Token Compression in Vision-Language-Action Models](https://arxiv.org/abs/2608.21247v1)**
  <!-- aidb:id=arxiv:2608.21247v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-21
  - Topics: agents, rag, research
  - Authors: Zhuoyuan Li, Rui Zhao, Jin Wang, Hanwei Zhu, Cong Zhang, Giuseppe Valenzise, Weisi Lin, Kin-Man Lam
  - Categories: cs.CV, cs.RO
  - Abstract: Token compression has become a key technique for reducing the inference cost of large foundation models, with approaches such as token pruning and KV-cache reuse widely adopted in vision-language models and recently explored for embodied agents. In embodied agents, tokens not only support perception and semantic understanding but also directly affect latency-sensitive closed-loop robot action prediction. Existing schemes typically guide compression using redundancy or importance cues, such as visual similarity, attention scores, and saliency. However, these cues only indirectly measure the key factor for safe compression: how much a token can change before causing an unacceptable deviation…
  - Comment: 15 pages, 5 figures
- [ ] **[v3.1.2](https://github.com/microsoft/graphrag/releases/tag/v3.1.2)**
  <!-- aidb:id=url:2f29d7be4ad3466fc62d -->
  - Feed: Microsoft GraphRAG releases
  - Published: 2026-08-21
  - Topics: rag, graph
  - Authors: dworthen
- [ ] **[v0.28.0rc2: [Spec Decode] DFlash2: local convolution + candidate selector (#52816)](https://github.com/vllm-project/vllm/releases/tag/v0.28.0rc2)**
  <!-- aidb:id=url:31c6f260de9b1ca31ac7 -->
  - Feed: vLLM releases
  - Published: 2026-08-21
  - Topics: inference, production
  - Authors: SubSir
- [ ] **[v0.28.0rc1](https://github.com/vllm-project/vllm/releases/tag/v0.28.0rc1)**
  <!-- aidb:id=url:3d23242522a95e0119db -->
  - Feed: vLLM releases
  - Published: 2026-08-20
  - Topics: inference, production
  - Authors: jperezdealgaba
- [ ] **[langgraph-sdk==0.4.3](https://github.com/langchain-ai/langgraph/releases/tag/sdk%3D%3D0.4.3)**
  <!-- aidb:id=url:72c1c65856af7651e1ca -->
  - Feed: LangGraph releases
  - Published: 2026-08-19
  - Topics: agents, runtime
  - Authors: github-actions[bot]

## Suppressed duplicates

4 уже встречавшихся записей сохранены в `manifest.json`, но не требуют повторного triage.

## После triage

Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.
