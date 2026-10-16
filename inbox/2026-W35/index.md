# Weekly discovery — 2026-W35

> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.
>
> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.

Сгенерировано: 2026-08-25T08:49:20+00:00

## Кандидаты

- [ ] **[v0.28.0: [CI/Build] Pin Cython below 3.3 for arm64 tilelang sdist (#53358)](https://github.com/vllm-project/vllm/releases/tag/v0.28.0)**
  <!-- aidb:id=url:99ece13e787f34878e1a -->
  - Feed: vLLM releases
  - Published: 2026-08-24
  - Topics: inference, production
  - Authors: khluu
- [ ] **[SWE Refactor Bench: Can Coding Agents Complete a Long-Horizon, Whole-Repository Stack Migration?](https://arxiv.org/abs/2608.23564v1)**
  <!-- aidb:id=arxiv:2608.23564v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Deyao Hong, Yizhe Chi, Wenyi Li, Xiaoqiu Wang, Mingju Gao, Kaisen Yang, Bingxiang He, Youjie Zheng, Calvin Xiao, Qinhuai Na
  - Categories: cs.CL, cs.AI, cs.SE
  - Abstract: Modern software systems accumulate technical debt over decades of development, which makes migration expensive and largely manual. As coding agents become increasingly capable at bug fixing, can they autonomously perform such migrations? Existing benchmarks cannot answer this question because they evaluate only behavioural correctness, not whether the migration actually occurred. This leads an easy hack: agents copy the original implementation to make tests pass. We call this Blindness. To address this problem, we introduce SWE Refactor Bench, a benchmark comprising 20 whole-repository migrations, covering 4 kinds of technical debt. A three-stage evaluation protocol measures both migration…
- [ ] **[Prime Agent: A Self-Improving RLM Harness](https://arxiv.org/abs/2608.23552v1)**
  <!-- aidb:id=arxiv:2608.23552v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Seth Karten, Alex L. Zhang, Kevin Thomas, Sebastian Müller, Elie Bakouch, Daniel Auras, Mika Senghaas, Fares Obeid, Konstantin Dunas, Johannes Hagemann, Sami Jaghouar
  - Categories: cs.AI, cs.CL, cs.SE
  - Abstract: Language models are sequential processors, but long-horizon agency requires external information and computation beyond model weights and active context. Prime Agent is an open-source harness for long-horizon evaluation and coding-agent workflows. A persistent IPython REPL follows the Recursive Language Model abstraction for programmatic context processing and test-time compute, while Continual Harness preserves histories, memories, skills, prompts, and subagent specifications across trajectories. Recursive subagents coordinate through direct agent-to-agent communication, and the Agents View lets humans inspect and manage daemon-backed sessions. Prime Agent standardizes execution, recovery,…
  - Comment: 16 pages, 10 figures. Technical report. Code: https://github.com/PrimeIntellect-ai/prime-agent
- [ ] **[When "Do Not" Is Not Deny: Security Rules in CLAUDE.md vs Built-In Controls](https://arxiv.org/abs/2608.23550v1)**
  <!-- aidb:id=arxiv:2608.23550v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Ting Yan
  - Categories: cs.HC, cs.CR
  - Abstract: In CLAUDE.md, "do not" is a natural-language instruction that the model interprets. Claude Code's deny is a built-in control that blocks an action before the agent can take it. Both can express the same security goal, but they control the agent in different ways. We measure this gap in 481 public CLAUDE.md files. An LLM matched the extracted candidate rules against Claude Code's documented controls, and two security practitioners independently checked a sample without seeing the model's answers or each other's labels. Depending on how closely a control had to match the written rule, only about 4-16% of the retrieved security rules had a matching built-in control. Under the strictest standar…
  - Comment: 11 pages, 5 figures
- [ ] **[The Interaction Tax: When Communication Erases Diversity in Multi-Agent Teams](https://arxiv.org/abs/2608.23541v1)**
  <!-- aidb:id=arxiv:2608.23541v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Summer Eunhyung Ann, Haokun Liu, Chenhao Tan
  - Categories: cs.MA, cs.AI
  - Abstract: Does multi-agent LLM interaction help or hurt? Some work reports gains from debate (Du et al., 2024), critique loops (Chen et al., 2025), and mixture-of-agents synthesis (Wang et al., 2025), while other work finds that interaction adds cost without improving quality under equal budgets (Tran & Kiela, 2026; Xu et al., 2026; Jarrett et al., 2025), or that independent sampling already captures multi-agent gains (Li et al., 2024). We argue this contradiction partly reflects a missing distinction, because not all multi-agent communication is equal. Different model families find structurally different solutions, but when agents read each other's complete outputs, their proposals converge within o…
  - Comment: 14 pages, 3 figures. Accepted at ICML 2026 (PMLR 306)
- [ ] **[EarthVerse: Benchmarking Scientific Agents Across Dynamic Earth Systems and Natural Hazards](https://arxiv.org/abs/2608.23525v1)**
  <!-- aidb:id=arxiv:2608.23525v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Zhiqing Cui, Xinxiang Yin, Yihong Tang, Xinglang Zhang, Yuanzhe Hu, Siru Zhong, Weidong Tang, Yuxuan Liang, Weijia Li, Ming Jin, Shirui Pan, Yuhao Kang, Dingyi Zhuang, Jinhua Zhao
  - Categories: cs.AI
  - Abstract: Earth-system analysis reconstructs changing physical processes from observations that differ in source, scale, timing, and modality. Natural hazards make this work consequential because incomplete evidence can change estimates of severity, exposure, and mechanism. We introduce EarthVerse, a benchmark that evaluates scientific agents through package-scoped investigations. Its 405 reproducible tasks are grounded in 199 documented events and 19 hazard families. Agents inspect heterogeneous event packages, choose compatible evidence, execute transparent calculations, reconcile source differences, and preserve provenance in the final answer. We provide executable ground truth that decomposes eac…
- [ ] **[An Interactive Agent for Requirement-Driven Candidate Sourcing](https://arxiv.org/abs/2608.23501v1)**
  <!-- aidb:id=arxiv:2608.23501v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Yuanpeng He, Fangjing Li, Xiangyu Ru, Kexin Sun, Kun Yang, Lijian Li, Chi-Man Pun, Qingsong Wen, Wenpin Jiao, Mingkai Guo, Yirong Feng, Daiheng Gao, Zhi Jin
  - Categories: cs.SE
  - Abstract: Finding people from a natural-language description (``ML engineers transitioning to research roles in biotech'') is increasingly delegated to LLM agents and framed as information retrieval. We argue that it is fundamentally a requirements engineering task: such a request is an under-determined requirement with implicit constraints, many valid answers, and no acceptance criterion, so useful answers require eliciting, validating, and verifying the requirement before search can matter. We present \sys{}, to our knowledge the first interactive, requirements-driven candidate-sourcing agent (it elicits, validates, retrieves, and verifies a vague people-request into a justified slate through bound…
  - Comment: 12 pages
- [ ] **[SRPO: Self-Reflective Policy Optimization for Long-Horizon Reasoning](https://arxiv.org/abs/2608.23493v1)**
  <!-- aidb:id=arxiv:2608.23493v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Jialong Liu, Yuling Shi, Ning Yang, Xiaodong Gu, Zuchao Li
  - Categories: cs.AI
  - Abstract: Self-reflection is a powerful mechanism for credit assignment in human learning, converting sparse outcome feedback into actionable guidance. However, its potential for post-training Large Language Models (LLMs) remains underexplored. We propose Self-Reflective Policy Optimization (SRPO), a framework that internalizes this capability. SRPO enables LLMs to analyze their own completed trajectories, synthesize errors into concise "reflection patches," and use reflection-conditioned teacher scores on student on-policy rollouts as dense token-level training signals. This process effectively transforms sparse terminal supervision into dense, token-level learning signals without requiring external…
  - Comment: Accepted to ICML 2026
- [ ] **[MetaCaster: Meta-Harness-Optimized Agent for End-to-End Few-Shot Learning of Lightweight Time Series Forecasters](https://arxiv.org/abs/2608.23473v1)**
  <!-- aidb:id=arxiv:2608.23473v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: ChengAo Shen, Wenchao Yu, Fangyu Wu, Dongjin Song, Hanghang Tong, Dongsheng Luo, Wei Cheng, Haifeng Chen, Jingchao Ni
  - Categories: cs.LG, cs.AI
  - Abstract: Time series forecasting (TSF) is evolving toward multimodal and agentic settings, yet using foundation models remains uneconomical in resource-constrained scenarios, where compact, specialized forecasters are more desirable. However, lightweight forecasters typically require substantial training data, limiting their use in domains with scarce, slowly accumulated, or privacy-sensitive time series. To address this dilemma, we investigate the challenging problem of few-shot learning for lightweight forecasters. We propose MetaCaster, a meta-harness-optimized multi-agent framework that uses agentic data generation to automatically train specialized lightweight forecasters from only a few exampl…
  - Comment: Accepted by EMNLP 2026
- [ ] **[InjecMEM: Memory Injection Attack on LLM Agent Memory Systems](https://arxiv.org/abs/2608.23471v1)**
  <!-- aidb:id=arxiv:2608.23471v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Hanling Tian, Gengyu Zhang, Zeyang Sha, Jingying Wang, Yuhang Liu, Zhehao Huang, Kun Yang, Xiaolin Huang
  - Categories: cs.CR, cs.AI
  - Abstract: Memory is becoming a default subsystem in deployed LLM agents to provide persistent personalization and continuity. This naturally prompts a question: will memory system introduce new vulnerabilities into agents? Thus we propose InjecMEM, a novel memory injection attack paradigm that requires only a single interaction (no read/edit access to memory store) to steer later responses of related queries toward a pre-specified output. Guided by the retrieval-then-generate mechanism of memory systems, we craft the injection with a retriever-agnostic anchor and an adversarial command. The anchor contains high-recall topical cues so that downstream retrieval consistently associates the record with t…
  - Comment: 29 pages, 3 figures. Accepted at COLM 2026
- [ ] **[Reward-Free Continual Adaptation for Resilient Space Robots](https://arxiv.org/abs/2608.23452v1)**
  <!-- aidb:id=arxiv:2608.23452v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-24
  - Topics: agents, rag, research
  - Authors: Andrej Orsula, Miguel Olivares-Mendez, Carol Martinez
  - Categories: cs.RO, cs.AI, cs.LG
  - Abstract: Space robots operate in extreme environments where hardware degradation can critically compromise traditional control strategies. While continual reinforcement learning offers a promising mechanism for online adaptation, it inherently requires access to a reward signal during deployment. However, precise reward computation in space is often infeasible due to the lack of external tracking systems and the overall complexity of the environment. To address the challenge of unobservable rewards, we introduce a reward-free continual learning framework that leverages latent-state world models. By pre-training a model-based agent across diverse simulations, the world model learns a robust predictor…
  - Comment: Accepted for publication at the Third Conference on AI in and for Space (SPAICE 2026) | The source code is available at https://github.com/AndrejOrsula/space_robotics_bench
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

3 уже встречавшихся записей сохранены в `manifest.json`, но не требуют повторного triage.

## После triage

Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.
