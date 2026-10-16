# Weekly discovery — 2026-W37

> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.
>
> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.

Сгенерировано: 2026-09-07T13:34:01+00:00

## Кандидаты

- [ ] **[v0.29.0rc4: [Bugfix] Avoid sync in TRT-LLM ragged prefill](https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc4)**
  <!-- aidb:id=url:6f73b26a4c79e38f3a96 -->
  - Feed: vLLM releases
  - Published: 2026-09-04
  - Topics: inference, production
  - Authors: codex
- [ ] **[Multi-Step Tool-Calling over Korean Open Public APIs: A Benchmark and a Data-Synthesis Recipe](https://arxiv.org/abs/2609.05395v1)**
  <!-- aidb:id=arxiv:2609.05395v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Dain Kim, Eungi Cho, Kyumin Kim, Shinyeong Noh, Kyuseong Lim
  - Categories: cs.AI, cs.CL
  - Abstract: Data-sovereignty regulations increasingly require public institutions to deploy open-source, on-premise LLM agents that chain multiple tool-calls across live government APIs. However, open-source models consistently underperform in this multi-step setting, and no existing benchmark measures the gap. We introduce the Korean Open Public API Benchmark (KOPA-Bench), comprising 145 real-world tasks. To close this gap, we present EDGE, an Execution-grounded Dynamic Graph for tool-calling data synthEsis driven by live execution. EDGE builds a graph of how each tool's output can feed another's input, keeps only the links that succeed when actually called against the live APIs, and traverses these v…
  - Comment: 30 pages, 7 figures, 26 tables. Accepted to EMNLP 2026 Industry Track
- [ ] **[Necessary or Sufficient? Evaluating LLM Explanations With Behavioural Evidence](https://arxiv.org/abs/2609.05385v1)**
  <!-- aidb:id=arxiv:2609.05385v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Urja Pawar, Rajitha Ramanayake, Nabeel Kemal, Ashwin Kandath, Owen O'Neill, Guillaume Bourgeon, Houssem Chatbri
  - Categories: cs.AI
  - Abstract: LLM decision components that can operate within agent workflows often produce action-relevant recommendations or judgements together with explanations. Operators may use the named factors to monitor a system, diagnose errors, or decide when to escalate an output. Such use assumes that the explanations agree with the component's observable decision behaviour. We test two interpretations of the named factors: necessity, meaning that changing a factor would change the output, and sufficiency, meaning that retaining it while removing other changeable information would preserve the output. We evaluate these interpretations in two synthetic use cases: recommending advisors to clients and judging…
- [ ] **[CUA-Universe: A Scalable and Dynamic Environment for Hybrid GUI+CLI Agents](https://arxiv.org/abs/2609.05374v1)**
  <!-- aidb:id=arxiv:2609.05374v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Haoting Shi, Wenhao Wang, Weicheng Fang, Yaozhong Liang, Tian Jin, Pengxiang Zhao, Guangyi Liu, Siheng Chen, Yanfeng Wang
  - Categories: cs.AI
  - Abstract: Computer-use agents have advanced on benchmarks like OSWorld and AndroidWorld, but still act mostly through the GUI, often producing inefficient trajectories. Real-world computer work is hybrid, combining visual-state inspection with precise, high-throughput command-line operations, so capable agents must coordinate both modalities over shared application state. Yet scalable hybrid environments remain scarce because supporting both GUI and CLI over real applications typically requires substantial manual engineering for each application. Existing agents also struggle to use the two interfaces complementarily: CLI-native agents lack visual perception for tasks involving interface state or lay…
  - Comment: 21 pages, 9 figures
- [ ] **[Design Docs Are All You Need: An AI-native Machine-Learning Performance Tool](https://arxiv.org/abs/2609.05364v1)**
  <!-- aidb:id=arxiv:2609.05364v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Samuel Kushnir, Kimia Noorbakhsh, Kavya Sreedhar, Liqun Cheng, Ming Liu, Parthasarathy Ranganathan, Mohammad Alizadeh, Fred Kjolstad, Suvinay Subramanian
  - Categories: cs.PL, cs.AI
  - Abstract: Machine-learning performance modeling is a uniquely hostile terrain for long-lived software: the assumptions baked into today's abstractions are invalidated by tomorrow's models and systems, forcing perpetual refactoring of performance-modeling frameworks. Meanwhile, AI coding agents have become fast and capable enough that regenerating an entire library is cheaper than paying down the tech debt of incrementally patching it. We describe SMART, a rigorous symbolic performance-modeling library for ML systems whose main branch contains almost no code: the repository is a DAG of self-contained natural-language design docs, coding sub-agents regenerate the implementation from only the docs on ne…
- [ ] **[Mitigating Disease Spread by Design in Refugee and IDP Camps](https://arxiv.org/abs/2609.05342v1)**
  <!-- aidb:id=arxiv:2609.05342v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Giulia Zarpellon, Joseph Aylett-Bullock, Frank Krauss, Miguel Luengo-Oroz
  - Categories: physics.soc-ph, cs.CY, cs.MA
  - Abstract: Disease spread represents an increasing challenge in refugee and internally displaced person (IDP) settlements. The movement and interaction of people within camps is influenced by their layout, which therefore has the potential to significantly affect disease spread. This work aims at creating a methodology to explore the potential effects of different camp layouts as mitigating factors in the spread of diseases within settlements. We showcase proof-of-concept experiments by leveraging the JUNE agent-based epidemic model, discuss the kind of operational insights this methodology can facilitate, and provide a framework for future investigations.
  - Comment: 9 pages, 9 figures
- [ ] **[Trust-Aware Adaptive Disclosure for Inference Privacy Preservation in Multi-Agent Networks](https://arxiv.org/abs/2609.05340v1)**
  <!-- aidb:id=arxiv:2609.05340v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Puspanjali Ghoshal, Tobias J. Oechtering
  - Categories: cs.MA, cs.CR
  - Abstract: Agent based systems are increasingly deployed in information critical systems including healthcare management systems, and smart grids. In this paper, we consider a multi-agent system where each agent has a latent goal that needs to be kept hidden from observing adversaries. More specifically, this paper studies privacy-preserving consensus in networked multi-agent systems under goal inference attacks. We propose a Trust-Aware Privacy Control framework that adapts message disclosure based on the dynamic trust relationships between agents. The proposed method controls information release using a trust-dependent stochastic policy. This enables a tradeoff between consensus performance and priv…
  - Comment: Accepted and to be published in proceedings of 2026 IEEE International Conference on Advanced Networks and Telecommunications Systems (ANTS)
- [ ] **[Does Your Agent's Memory Survive a Model Upgrade? A Controlled Study of Memory Portability](https://arxiv.org/abs/2609.05339v1)**
  <!-- aidb:id=arxiv:2609.05339v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Ankit Goyal, Jaideep Ray
  - Categories: cs.AI, cs.CL, cs.IR
  - Abstract: Model upgrades are routine; memory migrations are not. An agent can keep the same memory store and still forget: a new model may interpret old notes differently, mixed embedding versions may break retrieval, and repair may fail without the original evidence. We compare memory as the same history is preserved verbatim for long-context reading (LC-RAW), divided into chunks for retrieval-augmented generation (RAG), compressed by a model into natural-language notes (NOTES), or normalized into a fixed-schema knowledge graph (KG-fixed). The study uses 48 synthetic histories with randomized answer codes, exact scoring, and two open-weight models with sub 10 billion parameters. Our measurements sho…
  - Comment: 18 pages, 3 figures, 7 tables, under review
- [ ] **[The History Is the Detector: Executing CVE Patch History, End-to-End](https://arxiv.org/abs/2609.05335v1)**
  <!-- aidb:id=arxiv:2609.05335v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Qiushi Wu, Kevin Eykholt, Youngja Park, Xiaokui Shu, Dhilung Kirat, Douglas Lee Schales, Ian Molloy
  - Categories: cs.CR, cs.AI, cs.SE
  - Abstract: Public vulnerability databases collect rich information about known software flaws, including their weakness types, affected components, and related patches. Fixing commits provide the exact code changes that removed these flaws. While these records capture why the original code was unsafe, they are documented mainly for human inspection rather than automated reuse. Consequently, the same unsafe conditions may still exist elsewhere in code without a known advisory, leaving much of this detection knowledge unused. We present BUGSTONE-E2E, a framework that transforms vulnerability history into executable detection rules and validates their findings. First, BUGSTONE-E2E mines reusable rules fr…
- [ ] **[RoboSPA: Can VLA Models Go Beyond Simple Scenes and Short-Horizon Tasks?](https://arxiv.org/abs/2609.05324v1)**
  <!-- aidb:id=arxiv:2609.05324v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: Zhenxuan Fan, Bo Zhang, Yutong Lin, Yuqian Yuan, Juekai Lin, Liang Liang, Zhuoyi Huang, Wenqiao Zhang, Juncheng Li, Siliang Tang, Jun Xiao, Yueting Zhuang
  - Categories: cs.RO, cs.AI, cs.CV
  - Abstract: Vision-Language-Action (VLA) models have shown promising progress in language-conditioned robotic manipulation. However, existing datasets and benchmarks mainly evaluate task completion under predefined settings, offering limited insight into model reasoning under increasing spatial and procedural complexity. We introduce \textbf{RoboSPA} (\textbf{Robo}t \textbf{S}patial-\textbf{P}rocedural \textbf{A}ssessment), a large-scale robotic manipulation dataset and benchmark for diagnosing embodied reasoning in VLA models. \texttt{RoboSPA} focuses on two core dimensions, Fine-Grained Spatial Reasoning and Long-Horizon Procedural Planning, covering 10 task categories and 56 base tasks. Each task is…
  - Comment: Accepted at the EMNLP 2026 Main Conference
- [ ] **[Optimal Rates for Agentic Networked Information Aggregation](https://arxiv.org/abs/2609.05318v1)**
  <!-- aidb:id=arxiv:2609.05318v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-04
  - Topics: agents, rag, research
  - Authors: MohammadHossein Bateni, Zahra Hadizadeh, MohammadTaghi Hajiaghayi, Mahdi JafariRaviz, Shayan Taherijam
  - Categories: cs.LG, cs.GT, econ.TH
  - Abstract: Building on the pioneering paper of Kearns, Roth, and Ryu (SODA'26), we study information aggregation in a networked learning model. The model captures a central pattern in agentic AI: each agent sees only part of the data and passes on only its own conclusion. Their model considers a linear regression problem with the mean squared error (MSE) loss. Agents sit in a DAG and each sees only a subset of the features and its parents' predictions, fits a linear predictor, and passes only its prediction forward. The benchmark is the full-feature learner that sees all raw features. A path of depth $D$ is $M$-covered if every block of $M$ consecutive agents collectively sees all raw features. Kearns…
  - Comment: Initial version submitted to SODA 2027 on July 9, 2026
- [ ] **[v0.29.0rc3](https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc3)**
  <!-- aidb:id=url:6afbe34d536f453c4535 -->
  - Feed: vLLM releases
  - Published: 2026-09-04
  - Topics: inference, production
  - Authors: khluu
- [ ] **[v0.29.0rc2](https://github.com/vllm-project/vllm/releases/tag/v0.29.0rc2)**
  <!-- aidb:id=url:4ffff060b6f7c2b8dc0f -->
  - Feed: vLLM releases
  - Published: 2026-09-03
  - Topics: inference, production
  - Authors: waizuichougou

## Suppressed duplicates

1 уже встречавшихся записей сохранены в `manifest.json`, но не требуют повторного triage.

## После triage

Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.
