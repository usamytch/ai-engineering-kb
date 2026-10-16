# Weekly discovery — 2026-W36

> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.
>
> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.

Сгенерировано: 2026-09-03T09:29:38+00:00

## Кандидаты

- [ ] **[Discriminative World Models for Web Agents](https://arxiv.org/abs/2609.02885v1)**
  <!-- aidb:id=arxiv:2609.02885v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Kelvin Li, Dhruv Pendharkar, Anish Pahilajani, Chuyi Shang, Leon Oks, Leonid Karlinsky, Rogerio Feris, Trevor Darrell, Roei Herzig
  - Categories: cs.AI, cs.LG
  - Abstract: Recent web agents use world models for test-time action selection by sampling candidate actions, predicting the resulting web states, and ranking them with a ranker model or a Process Reward Model (PRM). These world models are typically trained via supervised next-state prediction to generate fixed representations like HTML or AXTree snapshots. However, this objective is misaligned with the downstream ranker, which relies on predicted states being discriminative across candidates to accurately score them. To address this, we introduce predicted-state matching, a training objective where the predicted representation must distinguish the true resulting state from those reached by alternative…
- [ ] **[Approximately Efficient Multidimensional Bilateral Trade](https://arxiv.org/abs/2609.02872v1)**
  <!-- aidb:id=arxiv:2609.02872v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Aviad Rubinstein, Xizhi Tan, Zixin Zhou
  - Categories: cs.GT
  - Abstract: A central challenge in mechanism design is to develop truthful trade mechanisms that maximize the expected gains-from-trade (GFT) in two-sided markets. Because achieving the full GFT is generally impossible, the literature has focused on constant-factor approximations---a notoriously difficult problem even in simple settings. It was only recently that a breakthrough result by [DMSW22] achieved a constant-factor approximation for single-item bilateral trade. The same guarantee was later extended to single-dimensional matching markets with general downward-closed constraints [BRTW26]. Most existing results, however, are limited to single-dimensional agents. A notable multi-dimensional excepti…
  - Comment: To appear in the 67th IEEE Symposium on Foundations of Computer Science (FOCS 2026)
- [ ] **[VibeVoice-ASR-Streaming Technical Report](https://arxiv.org/abs/2609.02812v1)**
  <!-- aidb:id=arxiv:2609.02812v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Yujie Tu, Zhiliang Peng, Jianwei Yu, Li Dong, Songchen Xu, Yaoyao Chang, Wenhui Wang, Zilong Wang, Zehua Wang, Yan Xia, Jiajun Zhang, Xie Chen, Furu Wei
  - Categories: eess.AS
  - Abstract: Traditional speaker-attributed ASR systems treated ASR and speaker diarization as two separate tasks. Recently, end-to-end models such as VibeVoice-ASR have unified the two tasks within a single model. However, existing unified models still mainly support offline recognition, making it difficult to meet the low-latency requirements of real-time voice assistants and agents. To tackle this issue, we present VibeVoice-ASR-Streaming, one of the first LLM-based end-to-end approaches to streaming speaker-attributed ASR. It interleaves fixed-size audio chunks, a small amount of lookahead audio and previous text. This allows the model to produce ''who said what'' as speech arrives, without a separa…
- [ ] **[Large Language Models (LLMs) for Telecom Root Cause Analysis (RCA): A Structured Reasoning Framework for Evidence-Grounded Diagnosis](https://arxiv.org/abs/2609.02805v1)**
  <!-- aidb:id=arxiv:2609.02805v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Hao Zhou, Mandar Kulkarni, Hao Chen, Yan Xin, Charlie, Zhang
  - Categories: cs.AI
  - Abstract: Root cause analysis (RCA) is a critical task in telecom network operations, but diagnosing performance degradations in modern 5G and emerging 6G networks remains challenging due to complex cross-layer dependencies. While large language models (LLMs) offer promising capabilities for reasoning and knowledge integration, directly applying vanilla LLMs to telecom RCA often leads to hallucination, unstable reasoning, and poor alignment with structured network evidence. This work first reviews the evolution of telecom RCA from rule-based and machine learning (ML) approaches to emerging LLM-enabled techniques, and provides an overview of recent paradigms, including structured reasoning, retrieval-…
- [ ] **[SafeEvolve: Harness-Policy Co-Evolution from Agent Experience for Safety Alignment](https://arxiv.org/abs/2609.02786v1)**
  <!-- aidb:id=arxiv:2609.02786v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Qinghua Mao, Wanying Qu, Dadi Guo, Leitao Yuan, Qingyu Liu, Yu Li, Guanxu Chen, Yanwei Fu, Xi Lin, Xia Hu, Dongrui Liu
  - Categories: cs.AI, cs.CR
  - Abstract: The performance of LLM-based agents is jointly shaped by the base model and the harness used when interacting with the environment. This exposes them to safety risks in both harmful final responses and multi-step execution trajectories. Existing safety alignment mechanisms often rely on either external harness updates or policy optimization, yet applying either paradigm in isolation fails to bridge runtime control with intrinsic safety. We propose SafeEvolve, an experience-driven self-evolving framework for agent safety alignment. SafeEvolve leverages safety experience from completed on-policy trajectories to drive a continual loop of harness-policy co-evolution. On the harness side, SafeEv…
  - Comment: Project: https://github.com/MaoPopovich/SafeEvolve
- [ ] **[EarlyEval: Cheaper Agent Evaluation via Early Outcome Prediction](https://arxiv.org/abs/2609.02783v1)**
  <!-- aidb:id=arxiv:2609.02783v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Yuling Shi, Zhensu Sun, Junsen Dong, Chengcheng Wan, David Lo, Xiaodong Gu
  - Categories: cs.CL
  - Abstract: Evaluating LLM agents is essential for guiding their development, yet it has grown prohibitively expensive: a single pass of a frontier model over an agentic benchmark can cost hundreds to thousands of dollars, a price paid repeatedly across iterative development cycles. Prior efforts, centered on benchmark distillation, reduce the number of evaluation tasks but leave the cost of executing each retained task untouched. In this work, we introduce early outcome prediction, a complementary axis of efficiency that instead cuts cost within each task. Our key insight is that an agent's final outcome is often evident from its intermediate behavior well before execution completes. We instantiate th…
  - Comment: Code and data available at https://github.com/inphotoo/earlyeval
- [ ] **[Measurement-Driven Sub-Network Selection for On-Premise Retrieval-Augmented Factory Agents](https://arxiv.org/abs/2609.02760v1)**
  <!-- aidb:id=arxiv:2609.02760v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Vasileios Rizeakos, Georgios Paisios, Alexandros Machairas, Michael Birbas, Athanasios Bachoumis
  - Categories: cs.AI
  - Abstract: On-premise assistants can give factory workers conversational access to machine documentation, but models capable of the task rarely fit shop-floor hardware. We show that after structural compression and retrieval-grounded adaptation, model size is no longer a reliable predictor of adapted answer quality: general capability falls almost linearly with parameter count, while judged retrieval-augmented answer quality does not. We therefore treat deployment as a post-adaptation selection problem, committing one sub-network per device on judged answer quality and measured on-device throughput under a configurable general-capability floor and memory budget; rules that optimize size, speed, or qua…
  - DOI: 10.5281/zenodo.22255631
- [ ] **[Bilevel Coordinated Reflection: A Game-Theoretic Approach to Multi-Agent LLM Systems](https://arxiv.org/abs/2609.02750v1)**
  <!-- aidb:id=arxiv:2609.02750v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Yihang Chen, Yuxiang Chen, Yuxuan Huang, Meng Fang, Weilin Luo, Jun Wang
  - Categories: cs.AI
  - Abstract: Multi-agent LLM systems commonly use an orchestrator to decompose a task for a team of workers and then improve through textual reflection. Despite strong empirical results, these systems lack a unified account of coordination, memory improvement, and the role of external verification. We model orchestrator-worker interaction as a bilevel coordination game: under bounded coupling, the workers' local-update game is an approximate potential game whose equilibrium slack is controlled by decomposition quality. We then analyse reflection as stochastic movement over semantic memory states. For free-form reflection, we derive a finite-time upper bound, prove worst-case tightness, and give a positi…
- [ ] **[Repo-To-Skill: Distilling GitHub Repositories Into AI4AI Skills](https://arxiv.org/abs/2609.02749v1)**
  <!-- aidb:id=arxiv:2609.02749v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Jianlyu Chen, Yuyang Hu, Hongjin Qian, Jiawei Liu, Wenqing Wei, Xiaolong Chen, Defu Lian, Zhicheng Dou, Chaozhuo Li, Qiwei Ye, Zheng Liu
  - Categories: cs.AI, cs.CL
  - Abstract: Autonomous agents are beginning to carry out machine-learning (ML) research end to end. These agents combine a model backbone with a harness for planning, execution, memory, and verification, but this architecture still leaves domain-specific know-how outside the agent. We call this missing layer operational knowledge, the know-how that separates knowing a method from making it work. That knowledge is not absent from the field. It appears in repositories and papers, but in forms written for human readers and too large to load during a task. Once distilled into compact, verified skills, this knowledge can be reused across tasks rather than rediscovered during each run. We present DisCo, a sk…
  - Comment: 48 pages, 3 figures
- [ ] **[CORAL: An LLM-Native Harness for Production Recommender Systems](https://arxiv.org/abs/2609.02730v1)**
  <!-- aidb:id=arxiv:2609.02730v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Topics: agents, rag, research
  - Authors: Muhammad Rafay Azhar, Yuhang Zhou, Gilbert Jiang, Yuchen Wang, Rahul Sharma, Matthew DeSousa, Jiayi Liu, Xin Guo, Lizhu Zhang, Xiangjun Fan
  - Categories: cs.CL
  - Abstract: Production recommender systems shape what billions of people see, and sustaining their performance requires continual optimization: as content, user behavior, and upstream models shift, the choices governing retrieval, ranking, and serving must be revisited. Traditionally, human engineers test such changes through online experiments--a slow, reactive process limited by engineering effort, leaving parts of the system unrevised as conditions change. Although large language models have been applied to ranking, user modeling, and offline model development, few systems place an agent in a continual closed loop that acts on a live recommender and learns from the measured effects of its decisions.…
  - Comment: Accepted by RecSys '26 OARS Workshop
- [ ] **[v0.29.0rc1: [Bugfix] Handle padded routes in CUTLASS MoE permutations (#54747)](https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc1)**
  <!-- aidb:id=url:6f7bff52e7b0a23b16af -->
  - Feed: vLLM releases
  - Published: 2026-09-02
  - Topics: inference, production
  - Authors: khluu
- [ ] **[v1.39.1](https://github.com/google/adk-python/releases/tag/v1.39.1)**
  <!-- aidb:id=url:e6b8ad21c90c2d180c17 -->
  - Feed: Google ADK Python releases
  - Published: 2026-08-27
  - Topics: agents, sdk
  - Authors: wukath
- [ ] **[langgraph-sdk==0.4.4](https://github.com/langchain-ai/langgraph/releases/tag/sdk%3D%3D0.4.4)**
  <!-- aidb:id=url:950926fcf62eba148f50 -->
  - Feed: LangGraph releases
  - Published: 2026-08-27
  - Topics: agents, runtime
  - Authors: github-actions[bot]
- [ ] **[v0.28.1rc0](https://github.com/vllm-project/vllm/releases/tag/v0.28.1rc0)**
  <!-- aidb:id=url:bafbda7f83d741eeb484 -->
  - Feed: vLLM releases
  - Published: 2026-08-27
  - Topics: inference, production
  - Authors: louie-tsai
- [ ] **[v2.8.0](https://github.com/google/adk-python/releases/tag/v2.8.0)**
  <!-- aidb:id=url:2190af585be2464840fd -->
  - Feed: Google ADK Python releases
  - Published: 2026-08-26
  - Topics: agents, sdk
  - Authors: wukath

## Suppressed duplicates

1 уже встречавшихся записей сохранены в `manifest.json`, но не требуют повторного triage.

## После triage

Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.
