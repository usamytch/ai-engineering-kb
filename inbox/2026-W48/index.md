# Weekly discovery — 2026-W48

> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.
>
> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.

Сгенерировано: 2026-11-23T18:24:04+00:00

Период по дате обновления или публикации (UTC): 2026-11-15T18:24:04.287122+00:00 → 2026-11-23T18:24:04.287122+00:00.
Покрытие: обход завершён в границах источников, указанных в manifest.json. Кандидатов после дедупликации: 230; повторов: 937.

## Кандидаты

- [ ] **[Supercharging transformer residual connections](https://research.google/blog/supercharging-transformer-residual-connections)**
  <!-- aidb:id=url:8a952e6dea4cd3758252 -->
  - Feed: Google Research blog
  - Published: 2026-11-23
  - Topics: research
  - Categories: Algorithms & Theory
  - Abstract: Algorithms & Theory
- [ ] **[RoboTrack: Point tracking for real-world robotic manipulation](https://huggingface.co/blog/allenai/robotrack)**
  <!-- aidb:id=url:eb2701ff66febea27293 -->
  - Feed: Hugging Face and community engineering
  - Published: 2026-11-23
  - Topics: engineering, research
- [ ] **[Finding faster quantum algorithms with agents and formal verification](https://deepmind.google/blog/finding-faster-quantum-algorithms-with-agents-and-formal-verification)**
  <!-- aidb:id=url:895b540db6a8889e694c -->
  - Feed: Google DeepMind blog
  - Published: 2026-11-23
  - Topics: research, agents
  - Abstract: Using agent teams and formal verification to improve quantum algorithms for fusion and chemistry.
- [ ] **[How to build and maintain an agentic evaluation](https://huggingface.co/blog/agentic-evals)**
  <!-- aidb:id=url:00d52199bef25f9eda98 -->
  - Feed: Hugging Face and community engineering
  - Published: 2026-11-23
  - Topics: engineering, research
- [ ] **[Perplexity and Intelligence](https://openai.com/index/perplexity-and-intelligence)**
  <!-- aidb:id=url:1a10f1676d46fc01a909 -->
  - Feed: OpenAI research and engineering
  - Published: 2026-11-22
  - Topics: research, engineering
  - Categories: Research
  - Abstract: How perplexity measures progress in AI models, and why it could help developers establish a shared approach to evaluating emerging capabilities.
- [ ] **[How Google Duplex evolved to also call businesses for you in Gemini](https://research.google/blog/how-google-duplex-evolved-to-also-call-businesses-for-you-in-gemini)**
  <!-- aidb:id=url:84a578f05a50fce6cc76 -->
  - Feed: Google Research blog
  - Published: 2026-11-20
  - Topics: research
  - Categories: Generative AI, Machine Intelligence, Natural Language Processing, Speech Processing
  - Abstract: Generative AI
- [ ] **[Agents SDK v1.0.0-alpha.1](https://github.com/openai/openai-agents-python/releases/tag/v1.0.0-alpha.1)**
  <!-- aidb:id=url:4bdc26fb87f803ab1bbf -->
  - Feed: OpenAI Agents SDK releases
  - Published: 2026-11-20
  - Topics: agents, sdk
  - Authors: markstuart-oai
  - Abstract: # Agents SDK v1.0.0-alpha.1 This first preview from `feat/simple-codex` adds Codex as an opt-in model provider for the Python Agents SDK. The prebuilt `openai-agents` wheels (version `1.0.0a1`) are available exclusively through GitHub Releases. ## Highlights - **Choose Codex per run.** Import `CodexProvider` from `agents.models.codex` and create `provider = CodexProvider()`. Pass `RunConfig(model_provider=provider)` to the Runner. Codex uses your saved login. For API key authentication, use `CodexProvider(api_key=...)`. The provider selects the model for agents that use a model name or the default model. [Run the same agent with either provider](https://github.com/openai/openai-agents-pytho…
- [ ] **[EMA Policy Gradient: Taming Reinforcement Learning for LLMs with EMA Anchor and Top-k KL](https://arxiv.org/abs/2602.04417v3)**
  <!-- aidb:id=arxiv:2602.04417v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-02-04
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Lunjun Zhang, Jimmy Ba
  - Categories: cs.LG, cs.AI
  - Abstract: Reinforcement Learning (RL) has enabled Large Language Models (LLMs) to acquire increasingly complex reasoning and agentic behaviors. In this work, we propose two simple techniques to improve policy gradient algorithms for LLMs. First, we replace the fixed anchor policy during RL with an Exponential Moving Average (EMA), similar to a target network in deep Q-learning. Second, we introduce Top-$k$ KL estimator, which allows for flexible interpolation between exact KL and sampled KL. We derive the stability conditions for using EMA anchor; moreover, we show that our Top-$k$ KL estimator yields both unbiased KL values and unbiased gradients at any $k$, while bringing the benefits of exact KL.…
- [ ] **[Task2Hand: A Contact-Grounded Skill for Parametric Dexterous-Hand Morphology Design](https://arxiv.org/abs/2611.27967v1)**
  <!-- aidb:id=arxiv:2611.27967v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Haoyang Wang, Weibo Gao, Zhengxiong Li, Lingfeng Tao
  - Categories: cs.RO
  - Abstract: Dexterous hand design demands repeated expert work across geometry, robot-description code, collision debugging, grasp initialization, and policy training. We present Task2Hand, a Skill: a specification package that turns a functional manipulation brief into a parameterized hand model and routes every candidate through cost-ordered contact, dynamics, and learning gates. Each gate returns a status and an evidence record; on failure, the Skill records the earliest blocker, revises one bounded parameter group, and reruns the cheaper gates. The agent generates, validates, and trains autonomously within declared bounds, and escalates trade-offs, plateaus, and conflicting evidence to a human who…
  - Comment: 9 pages, 7 figures, 3 tables
- [ ] **[MemLife: Curating and Reasoning over Long-Term Egocentric Video Memories](https://arxiv.org/abs/2609.40195v2)**
  <!-- aidb:id=arxiv:2609.40195v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-30
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Guangzhi Xiong, Xinyuan Zhang, Xiao Yang, Hyokun Yun, Kai Zhang, Shiun-Zu Kuo, Hyeonjeong Ha, Xilun Chen, Kai Sun, Lucas Liang, Guangqiang Dong, Ejaz Ahmed, Ahmed A Aly, Anuj Kumar, Raffay Hamid, Aidong Zhang, Xin Luna Dong
  - Categories: cs.CV, cs.AI, cs.CL
  - Abstract: Long-term egocentric video enables personalized AI assistants to reason about daily life. However, as video histories grow to hundreds of hours spanning months or years, reprocessing raw clips for every query becomes computationally prohibitive. Memory systems offer a scalable alternative by compacting videos into text representations, but often fail on practical benchmarks: either the memory does not preserve key evidence, or the retriever fails to locate relevant entries due to retrieval competition in growing search spaces. To address these challenges, we introduce MemLife, a multimodal memory system that constructs entity-grounded, first-person text episodes and retrieves them via a tim…
- [ ] **[ScopeAct: Scoping Decision Models for Reliable Multi-Step Execution in Mobile GUI Agents](https://arxiv.org/abs/2609.30186v2)**
  <!-- aidb:id=arxiv:2609.30186v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-24
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Linghua Zhang
  - Categories: cs.AI, cs.SE
  - Abstract: Vision-language models (VLMs) enable mobile GUI agents to execute complex tasks, but frequent VLM invocations incur substantial latency and API costs. Prior work mitigates this overhead by delegating low-level action selection to lightweight decision models that choose among executable candidates. However, candidate selection alone lacks the task-level control needed to prevent premature termination and recover from failures, while candidates derived from accessibility trees (AXTrees) may not cover all actions required for task completion. To address these challenges, we introduce ScopeAct. This training-free mobile GUI agent framework combines frequent action selection with sparse VLM reas…
- [ ] **[Can Agents Keep Secrets They Were Never Told? Benchmarking Latent Privacy Risks Across Sessions with MemJoin](https://arxiv.org/abs/2610.24359v2)**
  <!-- aidb:id=arxiv:2610.24359v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-17
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Qishun Yang, Shu Yang, Difei Xu, Di Wang, Meng Ding
  - Categories: cs.CR, cs.LG
  - Abstract: To support sustained interactions and personalized assistance, agents use long-term memory to retain and combine user information across sessions. Reusing such memories can lead an agent to state a sensitive relation while completing an ordinary task that does not require it. The relation to protect and the combination of clues that reveal it may remain hidden at memory write time, when later records and tasks are still unknown. In this paper, we introduce MemJoin, a privacy benchmark of 288 synthetic analysis cases in which the complete history entails a sensitive relation, but every individual session is insufficient. We evaluate six memory systems with the same answer-generating model, a…
- [ ] **[Advancing AI Capabilities and Evolving Labor Outcomes](https://arxiv.org/abs/2507.08244v4)**
  <!-- aidb:id=arxiv:2507.08244v4 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-07-11
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Jacob Dominski, Tyler Boes, Yong Suk Lee
  - Categories: econ.GN
  - Abstract: This paper examines how labor market outcomes changed across occupations as AI capabilities advanced from chatbots to reasoning models and AI agents. We construct an occupational AI exposure score for each capability stage and relate its change to the Current Population Survey through June 2026. In aggregate, occupations whose exposure rose more did not lose employment or see higher unemployment over three years. However, the number of workers under 30 in these occupations fell by about 8 percent per standard deviation of the exposure change, and the decline is concentrated among young workers without a college degree and in office and customer service occupations rather than in technical o…
  - Comment: 106 pages, 8 figures, 5 tables, plus Online Appendix
- [ ] **[Quantum Encoding Agents: A Natural Language Interface for Data Embedding Strategy Selection in Quantum Machine Learning](https://arxiv.org/abs/2609.31902v2)**
  <!-- aidb:id=arxiv:2609.31902v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-25
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Ana Paula Appel
  - Categories: quant-ph
  - Abstract: Selecting a data encoding is a central and poorly tooled decision in quantum machine learning. The feature map fixes the geometry of the Hilbert space, the expressibility of quantum kernels, and whether the circuit can run on near-term hardware. This paper presents Quantum Encoding Agents, an open-source system that turns encoding selection into a natural-language interaction. Given a dataset and an optional task description, it profiles the data, applies a hardware-aware policy using the gate-error threshold p* approximately 10^{-3}, returns a copyable Qiskit circuit with a justification in Portuguese or English, and scores the quantum kernel by Kernel-Target Alignment (KTA). When a numeri…
  - Comment: 12 pages, 8 Tables, 6 Figures
- [ ] **[SUAF: Spectral Universal Advantage Features for Zero-Shot Policy Improvement](https://arxiv.org/abs/2611.27919v1)**
  <!-- aidb:id=arxiv:2611.27919v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Huaze Tang, Runqing Miao, Tianren Peng, Lam Nguyen, Chao Wang, Jairong Li, Wenbo Ding
  - Categories: cs.LG, cs.AI
  - Abstract: Reward-independent representations enable reinforcement learning agents to reuse knowledge across tasks, but limited representation capacity raises three fundamental questions: what statistical dependence should these representations capture, which components of that dependence should be retained for policy improvement, and how does discarding the remaining components affect decision-making? We address these questions through canonical dependence analysis. For a reference policy, we construct an action-centered, positive-lag canonical dependence matrix (CDM) that isolates the additional predictive contribution of the current action beyond the current state. Its singular value decomposition…
- [ ] **[CodeTeam: An LLM-Powered Multi-Agent Framework for Repository-Level Code Generation](https://arxiv.org/abs/2606.22082v2)**
  <!-- aidb:id=arxiv:2606.22082v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-20
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yifei Wang, Ruiyin Li, Peng Liang, Qiong Feng, Zengyang Li, Mojtaba Shahin, Arif Ali Khan
  - Categories: cs.SE, cs.AI
  - Abstract: Natural language to repository generation (NL2Repo) requires a system to construct an entire software repository from a natural-language requirements document. Compared with function-level code generation, this task demands longer planning horizons, stable interfaces across files, and iterative debugging of cross-file inconsistencies. To address these challenges, we propose CodeTeam, an LLM-based multi-agent framework that separates planning, decision making, and implementation into distinct, coordinated stages. In the planning stage, multiple Architect agents draft competing software design sketches (SDSs), optionally grounded by retrieved design references. A cto (Chief Technical Officer)…
  - Comment: 33 pages, 1 images, 20 tables, Manuscript revision to a Journal (2026)
- [ ] **[Decision Columns as an Index: Interpretable Embeddings for Explainable Entity Matching and Search](https://arxiv.org/abs/2611.27910v1)**
  <!-- aidb:id=arxiv:2611.27910v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Aadharsh Kannan, Robert Bruckner, Philip A. Bernstein
  - Categories: cs.IR, cs.AI, cs.DB
  - Abstract: Business data systems must determine whether records refer to the same entity and retrieve records satisfying requests whose decisive properties are implicit. As agents act on these records, both tasks require auditable reasons. Dense embeddings perform well but offer opaque coordinates, cannot be filtered by meaning, and require corpus re-encoding to add new properties. We propose interpretable embeddings built from decision columns: each column stores a decision model's calibrated answer to a natural-language question, with outcomes yes, no, or not stated. A record's embedding is its answers across an ordered set of questions. Similarity decomposes exactly into per-question contributions,…
  - Comment: 25 pages, 7 figures, including appendices. Evaluations on WDC Products and STaRK-Amazon
- [ ] **[TEA-Bench-BR: Can Coding Agents Turn a Branching Clinical Specification into Correct Code?](https://arxiv.org/abs/2611.27895v1)**
  <!-- aidb:id=arxiv:2611.27895v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Marcio Andre de Souza Estevam
  - Categories: cs.SE, cs.AI, cs.CL
  - Abstract: Coding agents increasingly implement rules written by domain experts, and bugs in such code are silent: it runs and returns a plausible answer. We introduce TEA-Bench-BR, a benchmark built on the Brazilian pathway for early autism (TEA) screening: three fictitious instruments with the structure of real ones, a multi-professional referral flow, and export to FHIR R4 with the national RNDS profiles, all specified in Portuguese. A generator samples each task's parameters (144 tasks, 6,798 hidden cases), and the hidden cases kill all 1,955 non-equivalent mutants of the reference. With Gemma 4 as the agent, the 12B solves 38.0% of single-instrument tasks and none at the FHIR level; the 31B solve…
  - Comment: 7 pages, 2 figures. Submitted to the Google Gemma 4 Developer Agent Paper Track (Kaggle, November 2026). Benchmark, code and results: https://doi.org/10.5281/zenodo.24143388
- [ ] **[The Voice on the Line](https://arxiv.org/abs/2610.35272v2)**
  <!-- aidb:id=arxiv:2610.35272v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-26
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Husein Zolkepli
  - Categories: cs.SD, cs.CL
  - Abstract: A transcriber listening through one microphone also hears everyone near it. We train causal voice isolators that keep only the caller for a speech recogniser: masking transformers with 20 ms of latency that enroll the caller from the call itself. Short evaluation windows hide two failures that real calls expose: forgetting the caller when another voice talks alone for a while, and damaging a caller who is alone. Long calls with turns, memory beyond the attention window and real headset crosstalk address the first, at a cost to the second. WavLM-Large's own weights, made causal and trained inside the model, move that trade, and training windows cut from longer calls remove most of a lone cal…
- [ ] **[LesionAgent: Training-Free Agentic Tumor Tracking and Response Assessment in Longitudinal CT](https://arxiv.org/abs/2611.27876v1)**
  <!-- aidb:id=arxiv:2611.27876v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Maximilian Rokuss, Jeya Maria Jose Valanarasu, Alejandro Lozano, Benjamin Hamm, Yannick Kirchhoff, Fabian Isensee, Klaus Maier-Hein
  - Categories: cs.CV, cs.AI, cs.MA
  - Abstract: Every few months, a cancer patient's CT scans decide whether treatment continues. 3D foundation models can now detect, segment, register and track lesions, yet none of them reads the scans as a radiologist does. A radiologist decides which findings are lesions, which are the same lesion months later and whether a new spot means progression, and checks each decision against the extensive rules of a clinical guideline. We introduce LesionAgent, an LLM agent that performs this read end to end without task-specific training. It operates frozen 3D models as tools, acts in 3D through coordinate-labelled views, remembers every lesion across visits in a registry, verifies every model output it reli…
- [ ] **[Benchmarks Are Surprisingly Compaction-Friendly](https://arxiv.org/abs/2610.31778v2)**
  <!-- aidb:id=arxiv:2610.31778v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-22
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Jeanne Salle, Hardik Bhatnagar, Matthias Bethge, Sahar Abdelnabi, Maksym Andriushchenko
  - Categories: cs.LG, cs.AI
  - Abstract: Long horizon agentic tasks are now pushing LLM agents past their context window. To continue the task, the agent scaffold has to free up the context window, a process known as context compaction. Compaction is generally lossy by design: agents can silently lose task constraints, instructions, or their reasoning behind earlier decisions. Although compaction is a standard component of coding agent scaffolds, it has not been studied systematically with frontier models on realistic, long horizon agentic tasks. Previous work evaluate smaller open weight models on toy or synthetic trajectories. We fix the agent scaffold (OpenCode), implement five compaction strategies inside it, and evaluate thre…
  - Comment: 28 pages, 12 figures
- [ ] **[Network versus market information in coupled opinion-return dynamics](https://arxiv.org/abs/2611.27874v1)**
  <!-- aidb:id=arxiv:2611.27874v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yue Yu, Luis Enrique Correa Rocha
  - Categories: physics.soc-ph, physics.pop-ph
  - Abstract: When making investment decisions, investors can use common signals from the market and local signals from their social networks. We develop an agent-based opinion-return model in which agents follow fixed trading strategies and respond to either local network information or a common market signal. In our model, trend followers and contrarians select either a local network signal or a common market signal and then update their buy, hold, or sell opinions by following or opposing the signal, respectively. The aggregate opinion imbalance determines the return, which sets the market signal. We find that three collective regimes emerge depending on how much network information is used and the fr…
  - Comment: Comments welcomed
- [ ] **[SafeRoute-MAS: Coverage-Aware and Risk-Calibrated Message Routing for Multi-Agent Scientific Reasoning](https://arxiv.org/abs/2611.13454v2)**
  <!-- aidb:id=arxiv:2611.13454v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-10
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Zhiming Xue, Jianan Liu, Sichen Zhao, Weiran Yan, Aichen Xie, Jing Yang
  - Categories: cs.AI
  - Abstract: We introduce SafeRoute-MAS, a coverage-aware, risk-calibrated procedure that keeps all specialist messages or removes one using only pre-integration information. On a sealed cache of 5,328 committees, its source-compatible operating point gains +1.80 percentage points (95% CI [+1.13, +2.52]) while removing 12.76% of message tokens. We also run 4,580 controlled integrations over a stratified 458-committee sample on a public gpt-oss-120b endpoint. The sample estimate is -0.09 points; design weighting to the original workload gives +0.94 points (95% CI [-1.31, +3.50]) and 18.72% acted-input reduction. A weighted token-matched comparison likewise does not establish a selector advantage (+1.68 p…
- [ ] **[SLICR: Strategy Logic-Guided Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2611.27865v1)**
  <!-- aidb:id=arxiv:2611.27865v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Arshia Rafieioskouie, Matthew Lucas, Tzu-Han Hsu, Borzoo Bonakdarpour
  - Categories: cs.AI, cs.LO
  - Abstract: Specification-guided reinforcement learning (RL) translates formal specifications of desired behavior of agents into shaped rewards. This paper introduces SLICR, a significant paradigm shift that advances the state of the art to specification-guided RL in adversarial settings under partial observability. We employ Strategy Logic (SL), which allows explicit quantification over agents' strategies and uses the linear temporal logic (LTL) to specify the agents' objectives and constraints. This enables reasoning not only about how agents should act to satisfy a specification, but also about how they should respond to the strategies and behaviors of other agents. We evaluate SLICR on three popula…
- [ ] **[Multi-Task Self-Evolving Harnesses with the Agent as Its Own Optimizer](https://arxiv.org/abs/2609.38372v3)**
  <!-- aidb:id=arxiv:2609.38372v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-29
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Qiankai Xu
  - Categories: cs.AI, cs.LG
  - Abstract: A harness is the code around a language model agent that organizes prompts, calls tools, manages context, and controls execution. As models grow stronger, recent work has begun to let agents improve their own harnesses, a line of work known as self-evolving harnesses. In most existing methods, a separate proposer running on a human-designed harness modifies the solver's harness, and a separate harness is evolved for each benchmark. Real-world tasks come from many domains, so both the evolution and the evaluation of a harness should cover a diverse range of tasks. We propose a framework close to recursive self-improvement: the same frozen model, on the same version of the harness, first solv…
- [ ] **[Who Grades the Agent? Privilege Separation for Coding-Agent Benchmarks](https://arxiv.org/abs/2611.27860v1)**
  <!-- aidb:id=arxiv:2611.27860v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Nathan Nour Houlamy, Mattia Favretto, Earlence Fernandes, Mauro Conti
  - Categories: cs.CR, cs.AI
  - Abstract: Benchmarks for AI-based coding agents are a staple of the current AI landscape, because they are the leading way to measure the performance of LLMs. Their scores guide business and research decisions. Evaluating coding agents is challenging, since they are able to manipulate their evaluation infrastructure to artificially achieve better scores. Grading an agent's solution often requires running its code, which can then manipulate the evaluation process. BenchJack, an automated benchmark auditor, recently reached near-perfect scores on nine of ten popular agent benchmarks without actually solving their tasks. Agents already do this unprompted, as OpenAI's July 2026 Hugging Face incident show…
  - Comment: 18 pages
- [ ] **[Beyond Self-Critique: Epistemic Convergence Control for Multi-Agent Research Verification](https://arxiv.org/abs/2611.27839v1)**
  <!-- aidb:id=arxiv:2611.27839v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Chrisantus Eze
  - Categories: cs.AI, cs.MA
  - Abstract: Multi-agent systems for scientific claim verification increasingly rely on role-structured LLM debate to pressure-test hypotheses. However, when debating agents are instantiated from the same underlying base model, they share identical latent representations, making self-critique bias structurally inevitable. Static fixed-iteration protocols compound this by either halting prematurely before evidence stabilizes or wasting inference compute after convergence. We present \sys{}, a multi-agent research verification framework that addresses both failure modes. First, we introduce an asymmetric role architecture comprising an Advocate, Skeptic, and Arbitrator with opposing epistemic directives,…
  - Comment: Accepted at ICAART 2027
- [ ] **[Auditable Financial Knowledge Graphs: Schema-Driven Construction and Intrinsic Quality Evaluation](https://arxiv.org/abs/2611.27835v1)**
  <!-- aidb:id=arxiv:2611.27835v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Samarth Sarin, Lovepreet Singh, Dhagash Mehta
  - Categories: cs.AI, cs.CE
  - Abstract: Financial documents combine narrative disclosures, accounting metrics, corporate structures, management commentary, and time-dependent facts, making them difficult to represent using conventional chunk-based retrieval-augmented generation systems. This paper presents an auditable, schema-driven methodology for constructing temporal financial knowledge graphs from page-delimited documents parsed using a general purpose document intelligence service. Overlapping document windows undergo phased large language model extraction of structural entities, quantitative observations, and domain-specific relationships. Candidate graph elements are validated against predefined schemas and consolidated t…
  - DOI: 10.1145/3858063.3858826
  - Comment: The paper was accepted in ICAIF Conference 2026 and presented in Milan, Italy
- [ ] **[ChildAI-Gov: An Evidence-Linked AI System for Assessing EdTech Policies Against Children's Digital Rights](https://arxiv.org/abs/2611.27799v1)**
  <!-- aidb:id=arxiv:2611.27799v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Naveen Sigalapalli, Huizhi Liang, Clara Crivellaro
  - Categories: cs.AI
  - Abstract: We present ChildAI-Gov, an explainable AI system for assessing whether education-technology (EdTech) policies respect children's digital rights. Generative AI is reaching children's education faster than its governance can keep pace, yet checking a tool against children's rights remains manual, expert-dependent, and slow. We propose the Child Rights Impact Score (CRIS), an evidence-linked measure across five dimensions: safety, privacy, transparency, autonomy, and non-discrimination. ChildAI-Gov reads an EdTech tool's privacy or AI policy and scores each dimension by combining a large-language-model judgement (gpt-4o-mini) with a deterministic rule check. A retrieval-augmented generation (R…
- [ ] **[EvoTER: Evolving Embodied Agents via Tool-Use Experience and Reflection](https://arxiv.org/abs/2611.27797v1)**
  <!-- aidb:id=arxiv:2611.27797v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yingting Zhou, Yuyin Zhou, Yongliang Wang, Haoran Li, Dongbin Zhao
  - Categories: cs.RO
  - Abstract: Long-horizon embodied tasks require agents to ground instructions in changing observations, coordinate heterogeneous tools, and recover from failures that can propagate through downstream operations. Although existing LLM-based agents retain experience and refine reusable skills, successful local repairs do not by themselves establish complete-task gains over the current shared procedure library. We present EvoTER, an experience-driven framework that enables embodied agents to self-evolve tool-use skills without updating model parameters. EvoTER operates through a three-role evolution loop: Explorer records tool-use trajectories; Diagnoser distills successful and failed executions into skil…
- [ ] **[AI Safety Considerations for Agents With Limited Time to Act](https://arxiv.org/abs/2610.10285v2)**
  <!-- aidb:id=arxiv:2610.10285v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-07
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Leo Zeitler, Jack Richings, Victoria Nockles
  - Categories: cs.AI, cs.LG
  - Abstract: In the wake of the increasingly public discussion about AI alignment, recent work has tried to propose specific AI architectures that behave safely. However, the proposed arguments that seemingly demonstrate proved alignment mostly neglect the environment the agent needs to act in. We discuss theoretical bounds for agent-agnostic safety guarantees in environments that can only be partially observed and within which an action is required within limited time. We introduce two realistic scenarios, one with an infinite state space and one with signal mixture. In these scenarios, we prove that even a perfect agent cannot guarantee safe behaviour. It will be argued that for any proof of AI safety…
- [ ] **[SYSEVOLVE: Safe, Autonomous Attack-Defense Co-evolution for Evolving Cyber Defense](https://arxiv.org/abs/2608.15012v2)**
  <!-- aidb:id=arxiv:2608.15012v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-15
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yuhan Meng, Jiandong Jin, Shaofei Li, Jionghao Huang, Puyi Wang, Hanlin Jiang, Anis Yusof, Peng Jiang, Changling Zhou, Zhenkai Liang, Yao Guo, Ding Li
  - Categories: cs.CR, cs.AI, cs.MA
  - Abstract: The offensive capability of large language models (LLMs) has crossed from research demonstration into documented reality. Frontier models have autonomously breached real production systems, and open-weight models now deliver frontier-level exploitation at negligible cost. Existing defenses cannot keep pace with such attacks: human-intensive defense updates over days to weeks, while AI-based defense, on the other side, trained on fixed historical data, does not adapt to an evolving attacker. We trace these persistent failures to one root cause: defense evolves in isolation, cut off from the adversary that should be driving its evolution. That isolation manifests at three layers: the deployme…
  - Comment: Technical Report For SysEvolve System, version 261120
- [ ] **[LUCA: A Synthetic World for Experimental Reasoning](https://arxiv.org/abs/2611.03100v4)**
  <!-- aidb:id=arxiv:2611.03100v4 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-02
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Anna Gogleva, Thomas Charman, Martin Balla, Karl Gemayel
  - Categories: cs.AI
  - Abstract: An experimental agent can succeed for the wrong reasons. Evaluations, however, often focus on the outcome, not the experiments, evidence, and inferences that produced it. We introduce LUCA, a configurable synthetic world for evaluating this process under fully known ground truth. Agents learn unknown regulatory systems through budgeted experimentation, then predict unseen interventions, diagnose hidden faults, and attempt rescues. This setup allows us to evaluate experiment selection, prediction, diagnosis, and intervention separately. Across seven frontier LLMs and three baselines, these capabilities dissociate sharply. Agents frequently rescue malfunctioning systems while diagnosing the w…
  - Comment: v4: softened author note. 20 pages (9 pages main text, remainder appendix), 6 figures, 14 tables. NeurIPS 2026 Workshop on Evaluation of Interactive Agents (IAEval); non-archival
- [ ] **[Search-RSI: Expanding Search Worlds Along Multimodal Agents' Capability Frontier](https://arxiv.org/abs/2611.27780v1)**
  <!-- aidb:id=arxiv:2611.27780v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Chengchao Lv, Yin Wang, Chunzheng Zhu, Wanli Chang
  - Categories: cs.CV, cs.AI
  - Abstract: Multimodal search agents answer knowledge intensive visual questions by grounding them in retrieved evidence, and recent recipes train them on multi hop tasks that are synthesized from knowledge graphs and grown online to keep pace with the agent. These recipes, however, treat the searchable world as fixed: a new question can be well formed and verifiable while its evidence is absent from the retrieval backend, so the agent issues the right query, retrieves nothing, and is penalized as if its policy were at fault. Such unreachable negatives accumulate with every round of growth. We propose Search-RSI, a recursive self improvement framework that expands the search world along the agent's cap…
  - Comment: 25 pages, including supplementary material
- [ ] **[QuASAR: Toward an LLM-Assisted Framework for Screening, Prototyping, and Assessing Quantum-Advantage Opportunities in Scientific Computing](https://arxiv.org/abs/2611.27778v1)**
  <!-- aidb:id=arxiv:2611.27778v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Mark L. Carroll, Jordan A. Caraballo-Vega, Brian P. Powell, John L. Schnase
  - Categories: cs.AI
  - Abstract: Identifying scientific computations that could benefit from quantum algorithms requires both domain knowledge and fluency in quantum algorithm design, expertise that rarely resides in one person. We report results from QuASAR, an experimental, two-agent, LLM-driven pipeline intended to bridge this gap. One agent screens scientific literature for computational kernels with a plausible quantum-algorithmic analogue and proposes candidates, each backed by citations. A second agent independently verifies those citations. For candidates that survive verification, it reconstructs the source's computational structure, formulates a quantum mapping, builds and executes a prototype, and benchmarks it…
- [ ] **[SkillForgeBench: Evaluating Agent Reliability Grounded in Agent Skill Specifications](https://arxiv.org/abs/2610.14918v2)**
  <!-- aidb:id=arxiv:2610.14918v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-10
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Zhengxi Li, Junyi Zhou, Qiyuan Zhang, Chuhan Wu, Fuyuan Lyu, Le Tian, Xiao Zhou, Chen Ma, Yufei Wang
  - Categories: cs.AI, cs.CL
  - Abstract: Evaluating an agent's ability to strictly satisfy diverse and procedurally complex requirements is essential to determining its practical reliability. Conducting such an evaluation demands agentic tasks that reconcile broad domain coverage with deep procedural complexity. Existing paradigms face a fundamental trade-off: expert-curated benchmarks achieve procedural depth but suffer from domain diversity bottlenecks, whereas crowdsourced benchmarks span diverse scenarios but lack execution rigor. To resolve this tension, we present SkillForgeBench, which leverages agent skills as unifying execution blueprints across three co-designed stages: (1) Resource Preparation uses domain-balanced skill…
  - Comment: 38 pages, 9 figures, 7 tables, including appendices. The first two authors contributed equally to this work
- [ ] **[TopoPilot: Reliable Conversational Workflow Automation for Topological Data Analysis and Visualization](https://arxiv.org/abs/2603.25063v3)**
  <!-- aidb:id=arxiv:2603.25063v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-03-26
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Nathaniel Gorski, Shusen Liu, Bei Wang
  - Categories: cs.HC, cs.AI, cs.GR, cs.LG
  - Abstract: Recent agentic systems demonstrate that large language models can generate complex codebases from natural language prompts. Despite this progress, they present reliability concerns for scientific visualization due to invalid operations, subtle errors, and failure to resolve underspecified inputs. In this work, we introduce TopoPilot, a reliable and extensible agentic framework for automating complex scientific visualization workflows. We focus on topological data analysis and visualization as a primary use case, while designing the framework to generalize to broader visualization domains. TopoPilot employs a two-agent architecture: an orchestrator translates user prompts into workflows comp…
  - Comment: 21 pages, 10 figures
- [ ] **[Computation, Not Memory: Chain-of-Thought and State Tracking in LLM Agents](https://arxiv.org/abs/2610.25760v2)**
  <!-- aidb:id=arxiv:2610.25760v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Pedram Mouseli, Massieh Moayedi
  - Categories: cs.LG, cs.AI, cs.CL
  - Abstract: Language-model agents often reason before they act, and the value of monitoring that reasoning depends on how it relates to their actions. We ask how an agent's actions depend on its reasoning when the correct action depends on a changing state. In a small file-system task, background events announce which file's lock has been toggled but not its new value. The agent therefore has to reconstruct the current locks from its history before it can move files safely. With Qwen3-8B and Qwen3.5-9B, we separate two roles of reasoning: generating it before each action, and retaining earlier reasoning in the prompt. Most of the reduction in lock-violating commands comes from reasoning written at the…
  - Comment: v2: adds retention without current reasoning and in longer episodes, tests of retained notes and current reasoning after a state change, explicit event labels, counterfactual pairs with a toggled lock, and readouts on outdated values
- [ ] **[RoSci: Exploring Robustness in Science VLMs](https://arxiv.org/abs/2611.27750v1)**
  <!-- aidb:id=arxiv:2611.27750v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Junying Wang, Yijin Guo, Yalun Wu, Ziheng Jiao, Farong Wen, Qihang Yan, Wenzhe Li, Ye Shen, Qi Jia, Chunyi Li, Zicheng Zhang, Guangtao Zhai
  - Categories: cs.CL, cs.AI, cs.CV
  - Abstract: Recent advancements in Vision-Language Models (VLMs) enable significant progress in scientific tasks. However, these models are generally assumed to be presented with complete and accurate information, overlooking the challenges of erroneous/missing information in wild scenarios. To address this gap, we introduce the concept of Scientific Model Robustness, which defines a model's ability to detect anomalies, assess solvability, and perform self-calibration when faced with Information Error (inconsistencies) or Information Loss (insufficiency). Specifically, we present RoSci-Bench, a diagnostic benchmark of 1,220 samples using a seed-variant strategy across six degradation types. To address…
  - Comment: 18 pages, 9 figures, 10 tables
- [ ] **[Shared Understanding in Human-AI Teams: Coordination Continuity in Evolving Work](https://arxiv.org/abs/2611.27746v1)**
  <!-- aidb:id=arxiv:2611.27746v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Siân Lindley, Britta Burlin, Christian Poelitz, Lev Tankelevitch, Richard Banks
  - Categories: cs.HC, cs.AI
  - Abstract: People are increasingly working with AI agents as part of extended, asynchronous workflows. In these settings, shared access to information does not guarantee a shared basis for action: goals, plans, and roles may persist while their current significance changes. We introduce coordination continuity, the extent to which collaborators sustain a workable basis for interdependent action as work progresses. Drawing on research on collaborative work, along with two qualitative team studies and a reflexive case from our own repository-based environment, we present a framework of three elements: durable representations of collaborative work; relative coordination properties that support interpreta…
  - Comment: 25 pages
- [ ] **[Can Vision-Language Models Synthesize Executable Game-Playing Programs?](https://arxiv.org/abs/2611.27741v1)**
  <!-- aidb:id=arxiv:2611.27741v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yao Tong, Jiaxin Qi, Dingyu Zhang, Jianqiang Huang
  - Categories: cs.AI
  - Abstract: Recent advances in vision-language models (VLMs) have endowed multimodal agents with increasingly strong visual perception and long-horizon reasoning capabilities, making VLM-based autonomous game playing feasible. Existing game benchmarks primarily evaluate whether an agent can select appropriate actions from the current visual state across different scenarios and games. However, most of them adopt a step-by-step interaction paradigm where the current visual observation is sent to the agent before each action. In practical deployment, this paradigm introduces two fundamental limitations: the game loop must wait for model inference, making real-time interaction impractical, and repeated VLM…
  - Comment: 21 pages (main paper with appendix), 3 figures, 13 tables
- [ ] **[AutoOntologyBench: A Task-Grounded Benchmark for Agentic Knowledge Engineering](https://arxiv.org/abs/2611.27734v1)**
  <!-- aidb:id=arxiv:2611.27734v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Minye Shao, Chenghao Xiao, Xingyue Zhao, Yang Long
  - Categories: cs.CL
  - Abstract: Foundation-model agents are increasingly extending beyond software engineering (SWE) into autonomous scientific research, where acquiring and integrating domain knowledge remains a critical challenge. Recent industrial advances have increasingly adopted knowledge graphs and ontology-based semantic layers to organize heterogeneous knowledge into reusable representations. We ask: Can autonomous agents construct ontologies that help them solve real tasks, and do they offer measurable benefits over alternative knowledge representations? Existing benchmarks evaluate ontology correctness or agent task success in isolation, leaving the value of autonomously acquired knowledge unresolved. We theref…
- [ ] **[Do Alice and Bob Dream of the Oracle? Wishful Cryptanalysis](https://arxiv.org/abs/2611.27729v1)**
  <!-- aidb:id=arxiv:2611.27729v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Guoxiao Liu, Keting Jia, Hongbo Yu, Zongyue Wang, Tianshuo Cong, Junfeng Fan, Anyu Wang, Xiaoyun Wang
  - Categories: cs.CR
  - Abstract: For two millennia, offense and defense have forged cryptographic security boundaries. Tools automated calculation and search, while humans drove discovery. Foundation models now mark a shift from automated computation to intelligent scientific discovery. Because cryptanalysis rests on exact mathematical definitions and immediately executable truth, it offers a proving ground for autonomous intelligence to move past security reliant on scarce human attention and explore structures beyond human working memory. Unguided models stall between two opposite traps: authority hallucination, where they surrender whenever prior literature declares a route blocked, and reasoning hallucination, where th…
- [ ] **[A Cognitive Agentic AI Framework for Interactive Process Analysis and Optimization](https://arxiv.org/abs/2611.27725v1)**
  <!-- aidb:id=arxiv:2611.27725v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Trung Ngoc Trinha, Roman Tschentscher, Trong Dong Nguyen, Trung Thanh Nguyen, Anna Trubetskaya
  - Categories: cs.MA
  - Abstract: Complex multivariable process analysis and optimization require coordinated access to simulation, structured data, machine learning (ML), optimization, and scientific literature, often across disconnected software tools. We present a Cognitive Agentic AI Framework (CAAF) that enables interactive, iterative process investigation through natural-language prompts within an established flowsheet. Following harness-engineering principles, CAAF assigns task interpretation, planning, knowledge synthesis, and context management to a large language model while delegating numerical calculations to specialized tools. Dedicated providers connect databases, scientific-document retrieval, ML-assisted Bay…
- [ ] **[Chain of Operators: An Inference-Time Harness for In-Context Operator Learning](https://arxiv.org/abs/2606.12318v3)**
  <!-- aidb:id=arxiv:2606.12318v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-10
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Minghui Yang, Chenghan Wu, Ling Guo, Liu Yang
  - Categories: cs.LG, cs.AI
  - Abstract: While scientific foundation models show immense promise in accelerating physical simulations and numerical forecasting, they remain notoriously brittle when encountering out-of-distribution (OOD) scenarios. Adapting these generalist models to complex OOD tasks typically requires expensive parameter fine-tuning. In linguistic AI, this bottleneck is bypassed using "harnesses", which serve as external scaffolding such as reasoning chains and tool use to adapt frozen weights to complex tasks, yet designing an equivalent harness for physical domains remains an open frontier. To bridge this gap, we introduce Chain of Operators (CHOP), a framework that guides a frozen foundation model through comp…
- [ ] **[MetaRigor: From Agentic Automation to Verifiable End-to-End Meta-Analysis Through Scientific Decision Boundaries](https://arxiv.org/abs/2611.27713v1)**
  <!-- aidb:id=arxiv:2611.27713v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yifeng Xie, Chenke Li, Yangshuo Miao, Jingyuan Zheng, Mingxuan Liu, Feiwei Qin, YaQi Wang, Huiyu Zhou, Yifei Chen
  - Categories: cs.AI, cs.SE
  - Abstract: Automated meta-analysis requires not only accurate numerical extraction but also the consistent preservation of result identity across stages, including the associated study, comparison, population, outcome, time point, and analysis conditions. We present MetaRigor, an LLM workflow framework for verifiable end-to-end evidence synthesis. MetaRigor organizes study results as Study x Target units and operationalizes scientific decision boundaries at the task level through Task Contracts, programmatic rules, and source binding. The model performs semantic interpretation that depends on study context, whereas programs execute formalizable rules, computations, validation, and source verification.…
- [ ] **[Object-Centric World Models for Causality-Aware Reinforcement Learning](https://arxiv.org/abs/2511.14262v4)**
  <!-- aidb:id=arxiv:2511.14262v4 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-11-18
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yosuke Nishimoto, Takashi Matsubara
  - Categories: cs.LG, cs.AI
  - Abstract: World models have been developed to support sample-efficient deep reinforcement learning agents. However, it remains challenging for world models to accurately replicate environments that are high-dimensional, non-stationary, and composed of multiple objects with rich interactions since most world models learn holistic representations of all environmental components. By contrast, humans perceive the environment by decomposing it into discrete objects, facilitating efficient decision-making. Motivated by this insight, we propose \emph{Slot Transformer Imagination with CAusality-aware reinforcement learning} (STICA), a unified framework in which object-centric Transformers serve as the world…
  - Comment: Accepted by AAAI-26. Code is available at https://github.com/nishimoto0430/STICA. v4: Fixed the mean score of STICA in Table 1 and the hyperparameters in Table 3. Updated Figure 7
- [ ] **[Embodied-Harness: Towards Recursive Self-Improvement for Robotic Manipulation](https://arxiv.org/abs/2611.27689v1)**
  <!-- aidb:id=arxiv:2611.27689v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zhenxuan Fan, Zhuoya Wang, Yuqian Yuan, Wenqiao Zhang, Juncheng Li, Jun Xiao, Siliang Tang, Yueting Zhuang
  - Categories: cs.RO, cs.AI, cs.CV, cs.MA
  - Abstract: Vision-language model (VLM)-based agents offer a promising approach to robotic manipulation, yet remain limited by inadequate memory organization, uncertain failure attribution, and limited reuse of execution experience. We propose Embodied-Harness, a dual-agent framework that improves manipulation by refining the execution harness without updating model parameters. The Actor interacts with the environment through a robot-control interface, while the Reflector converts execution evidence into reusable operational guidance. Hierarchical Memory Architecture maintains short-term execution context and long-term experiential knowledge to support execution and reflection. Evidence-based Experienc…
- [ ] **[GeoScaffold: From Latent to Realized Geometry in Collaborative Detection](https://arxiv.org/abs/2611.27667v1)**
  <!-- aidb:id=arxiv:2611.27667v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Kang Yang, Yance Fang, Gaochen Cui, Xiaoqiang Jin, Deying Li, Yongcai Wang
  - Categories: cs.CV
  - Abstract: Most collaborative 3D detectors fuse bird's-eye-view (BEV) features from connected vehicles and roadside infrastructure to aggregate complementary observations. Although modern communication, alignment, and fusion pipelines encode rich latent geometry in the fused BEV features, the standard readout pipeline inherited from single-agent detectors, i.e., anchor scoring, box decoding, and non-maximum suppression (NMS), does not fully exploit these geometric cues. We empirically identify and quantify this gap on UrbanIng-V2X. Collaboration improves localization at about two-thirds of positive anchors, yet when NMS resolves two overlapping collaborative boxes of one object, it keeps the better-lo…
  - Comment: 27 pages, 11 figures, 13 tables
- [ ] **[Hierarchical Agentic Mid-Band Agility for Reliable Low-Latency Space-Air-Ground Integrated V2X Networks](https://arxiv.org/abs/2611.27659v1)**
  <!-- aidb:id=arxiv:2611.27659v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Liu Cao, Zisheng Gong, Lyutianyang Zhang, Jinke Ren, Jiguang He, Shuguang Cui
  - Categories: eess.SY
  - Abstract: Upper-mid-band spectrum offers bandwidth opportunities for the integrated networks of ground vehicles, unmanned aerial vehicles (UAVs), and low Earth orbit (LEO) satellites to support 6G wide-area vehicle-to-everything (V2X) connectivity. However, V2X services' latency and reliability are sensitive to the mid-band selection due to frequency-dependent propagation and rain attenuation. This paper investigates environment-aware spectrum agility over candidate frequency range 3 (FR3) bands within 7.125-24.25 GHz, jointly with end-to-end (E2E) multi-path traffic splitting and transmit power control. Each data packet is partitioned into non-overlapping subflows over direct and UAV-assisted paths,…
  - Comment: This work has been submitted to the IEEE for possible publication. 13 pages, 9 figures
- [ ] **[GAAMA: Graph Augmented Associative Memory for Agents](https://arxiv.org/abs/2603.27910v4)**
  <!-- aidb:id=arxiv:2603.27910v4 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-03-29
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Swarna Kamal Paul, Shubhendu Sharma, Nitin Sareen
  - Categories: cs.AI, cs.IR, cs.MA
  - Abstract: AI agents that talk with users across many sessions need long-term memory to stay coherent and personalized. Existing approaches use either flat retrieval-augmented generation (RAG) that ignores how memories connect, or entity-centric knowledge graphs. Entity-centric graphs split each message into separate triples, which loses its context, and in conversations the speakers become hubs linked to almost every message, so propagation through them tells retrieval little. We present GAAMA, a graph-augmented associative memory that organizes conversations around topics. It keeps verbatim episodes, uses an LLM to distill them into atomic facts and topic concepts, and then synthesizes higher-order…
- [ ] **[Characterizing and Detecting Unfaithful Work Reports by Coding Agents](https://arxiv.org/abs/2611.25760v2)**
  <!-- aidb:id=arxiv:2611.25760v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Wenhao Yang, Runzhi He, Minghui Zhou, Pengfei Gao, Dayi Lin, Qingwei Lin, Dongmei Zhang
  - Categories: cs.SE, cs.AI
  - Abstract: Coding agents increasingly carry out long-horizon development tasks, autonomously planning and executing multi-step actions that span files, tools, and sessions. Because developers rarely follow each action, and agents resuming the work depend on records of what was done, the agent's work report often becomes the primary account of what was changed and established. When the report contains false or unsupported claims, it gives recipients false assurance: incomplete work may be accepted without verification, incorrect assumptions about the current state can propagate to later steps and agents, and evaluators that credit stated success may reward the report rather than the work. Yet little is…
- [ ] **[SLA-Aware Task Offloading in the IoT Edge-Cloud Continuum: Class-Weighted Deep Reinforcement Learning Against an Exact Optimum](https://arxiv.org/abs/2611.10638v2)**
  <!-- aidb:id=arxiv:2611.10638v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-07
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Shilpa Golla, Tharun Kumar Korine Palli, Urmila Bandaru
  - Categories: cs.AI, cs.LG, cs.NI
  - Abstract: Deep reinforcement learning (RL) is often used to decide where Internet of Things (IoT) tasks with different latency limits run in the edge-cloud continuum, yet some methods give every missed task the same penalty and few compare their agents with an optimal policy. This benchmark study builds four offloading systems small enough to solve exactly by dynamic programming and measures reward and learner against the optimum. A bonus for a met limit makes each miss cost its penalty plus the bonus, which shifts the class weights of published per-class rewards. A class-blind penalty stays 65% to 118% above the optimal cost even with a perfect learner, while a corrected per-class penalty comes with…
- [ ] **[MoHA: Model-Conditioned Harness Adaptation for Long-Video Agents](https://arxiv.org/abs/2611.27646v1)**
  <!-- aidb:id=arxiv:2611.27646v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jianghan Chao, Wenhui Tan, Hang Su, Qiuyu Tian, Tanxiao Li, Bingzi Zhang, Zequn Liu, Ruihua Song, Yingce Xia
  - Categories: cs.CV
  - Abstract: Long-video understanding increasingly relies on agentic systems that actively acquire evidence rather than process fixed video representations. Their execution harnesses must coordinate language-level planning with video-level observation and evidence acquisition, yet are typically fixed across model stacks. We therefore introduce MoHA, a framework for model-conditioned harness adaptation that adapts a common initial execution harness to the specific planner and observer models it hosts. MoHA treats the harness itself as a model-conditioned optimization object: under the same task distribution and initialization, different planner-observer stacks can benefit from different executable harnes…
  - Comment: 24 pages, 3 figures. Code: https://github.com/roverx12345/MoHA
- [ ] **[MAWAM: A Multi-Agent World-Action Model for Coordinated Manipulation](https://arxiv.org/abs/2611.25105v2)**
  <!-- aidb:id=arxiv:2611.25105v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-18
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Xianzhe Fan, Chi-Pin Huang, Fu-En Yang, Jing Wang, Yecheng Wu, Yu-Cheng Chou, Johan Bjorck, Linxi "Jim" Fan, Jan Kautz, Yu-Chiang Frank Wang, Zhiding Yu, Hengshuang Zhao, Zhiqi Li
  - Categories: cs.RO, cs.AI, cs.CV
  - Abstract: Every move in a robot team changes the world in which its teammates must act. Coordinated manipulation therefore calls for predicting the team's actions together with the physical future they jointly create. We introduce MAWAM, a multi-agent world-action model that jointly generates each robot's future views and executable action chunks in a single sample. Built from a pretrained single-robot world-action backbone, MAWAM jointly denoises all robots' action and future-view tokens through cross-agent attention, while preserving a separate control interface for each robot. MAWAM achieves the highest success on all three real-robot tasks (laundry-bag collection, bath-towel folding, and umbrella…
- [ ] **[Report2Alpha-Bench: Evaluating LLM Agents on End-to-End Quantitative Research](https://arxiv.org/abs/2611.27635v1)**
  <!-- aidb:id=arxiv:2611.27635v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yun Zhang, Hui Yang, Wei Meng
  - Categories: cs.CE
  - Abstract: We evaluate whether LLM agents can independently carry out a several-hour quantitative research project: read a brokerage research report, make a plan, and over 7 rounds of iteration propose hypotheses, write factor code and improve it from backtest feedback, seeing only 2022-2023 market data. Like Terminal-Bench-Science, the task evaluates overall research ability; unlike it, there is no directly checkable unique answer: the model must repeatedly propose hypotheses on very noisy data, revise its understanding from experiments, disentangle multiple factors and design ablations without overfitting in-sample, much like complex real-world decisions with many interacting factors. After the rese…
- [ ] **[Learning Inside Types: Epistemic Typestates for Safe Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2611.27631v1)**
  <!-- aidb:id=arxiv:2611.27631v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Lorenzo Bacchiani, Mario Bravetti, Giovanni Pau, Roberto Girau
  - Categories: cs.AI
  - Abstract: Type disciplines make programs safe by construction: components checked against each other's types compose into programs that cannot go wrong in the ways the types exclude. Types suit reinforcement learning: a type constrains what an agent may choose, not how it chooses, so the guarantee holds for every policy a learner produces. We introduce epistemic typestates, a type discipline for safe multi-agent reinforcement learning. An agent's type is a protocol whose states record its beliefs, the worlds it cannot rule out from its own observations and actions, and permits only actions that are safe in every world of the belief, whatever the others do within their public types. Agents learn insid…
- [ ] **[Benchmarks' Last Exam](https://arxiv.org/abs/2611.27622v1)**
  <!-- aidb:id=arxiv:2611.27622v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: James Zhu, Zekki Cat
  - Categories: cs.AI
  - Abstract: Public benchmarks guide model selection, post-training rewards and claims of progress in artificial intelligence, yet leaderboards report aggregate scores without verifying whether each task's prompt, environment and grader agree on what counts as success. How often that agreement fails in contemporary evaluations, and in which direction confirmed defects move scores, has remained unmeasured across grading designs. Here we synthesize task-level quality reviews of 749 tasks across eight frontier benchmarks and 767 public model evaluations spanning closed-form question answering, document rubrics and agentic execution to assess whether prompts, environments and graders align. Task validity st…
  - Comment: 15 pages, 6 figures, 2 tables. Initial milestone of the Benchmarks' Last Exam initiative; public reports, structured data, and code archived at https://benchmarks-last-exam.com/benchmarks/ and https://github.com/ZekkiCat/Benchmarks-Last-Exam
- [ ] **[Potential emergence in LLM agents: a statistical physics perspective](https://arxiv.org/abs/2611.27618v1)**
  <!-- aidb:id=arxiv:2611.27618v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zhuo-Yang Song, Hua Xing Zhu
  - Categories: cs.LG, cond-mat.stat-mech, cs.AI, cs.CL, nlin.AO
  - Abstract: There has been significant recent interest in understanding the behaviour of LLM agents from the perspective of human preferences or corpus statistics. In this paper we propose agent states as intermediate variables through which post-training can be measured and predicted. From a statistical physics perspective, we study the emergence of a global potential which governs the transition of state in LLM agent reasoning. We introduce a partition function to model the ideal KL-regularised transition distribution and track potential structure, mean reward and state entropy. We demonstrate our approach in two Qwen3.5-9B tasks: safety-test selection and physics-reasoning auditing. We observe that…
  - Comment: 21 pages, 5 figures, 5 tables
- [ ] **[Isonomy: Isolating Every Request from Timing Side Channels at Nearly Full-Sharing Throughput in Multi-Instance LLM Prefill](https://arxiv.org/abs/2611.27596v1)**
  <!-- aidb:id=arxiv:2611.27596v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Bowen Sun, Chaowei Xiao
  - Categories: cs.DC, cs.CR
  - Abstract: Many long prompts share a prefix, and reusing its cached keys and values saves prefill computation. A cache hit, however, makes the first token arrive earlier and can reveal that another request used the same prefix, so providers share the cache only within an account. Under least privilege, even permission to send and pay for requests should not expose other requests' prompts in the same account. This matters because agents send unreviewed requests carrying private data, resellers pool users behind one account, and creden-tials can be stolen. Isonomy therefore isolates each request by default and lets requests opt into explicit sharing groups. Rather than give up reuse, it keeps one cache…
- [ ] **[WEIR: Watershed Exploration and Drift-Aware Prefix Shrinkage for Multi-Turn Agent Reinforcement Learning](https://arxiv.org/abs/2611.27570v1)**
  <!-- aidb:id=arxiv:2611.27570v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Pixel Nomand, Elena Voss, Marcus Hale, Sofia Reyes
  - Categories: cs.LG
  - Abstract: Multi-turn language model agents often receive only a single binary reward at the end of a long interaction trajectory, making it difficult to separate decisive decisions from routine steps or estimate accurate intermediate values. Prefix-tree methods improve sample efficiency by merging trajectories that share action histories, yet two structural flaws remain: naive pooling mixes stale off-policy outcomes into critic targets with fixed weights, and uniform or entropy-driven branching wastes continuations on dead-end states whose outcome is already settled. We introduce WEIR (Watershed Exploration and Intrinsic-Drift Shrinkage), an actor-critic reinforcement learning framework grounded in a…
- [ ] **[Mjolnir: Finding and Reproducing Vulnerabilities in Root-of-Trust Firmware and RTL with Project-Grounded Agents](https://arxiv.org/abs/2611.27567v1)**
  <!-- aidb:id=arxiv:2611.27567v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Collin MacDonald, Carl Lundin, Stephen Herwig, Miguel Osorio, Timothy Trippel
  - Categories: cs.CR
  - Abstract: A root of trust (RoT) anchors secure boot and attestation for the system above it, so a bug in RoT firmware or hardware undermines every layer that trusts it. LLM agents now find real vulnerabilities in general-purpose software, but RoT code presents two challenges. First, many security-relevant bugs depend on project-specific trust boundaries and fault-injection countermeasures rather than generic vulnerability patterns, and may cause no crash. Second, without RoT hardware, agents must exercise RoT inputs through the project's own hardware model, mocks, or RTL testbenches. We present Mjolnir, an agentic pipeline that supplies each project's threat model and design conventions to discovery…
- [ ] **[Trilemma: How Agents choose between Honesty, Confidentiality, and Task Completion](https://arxiv.org/abs/2611.08312v2)**
  <!-- aidb:id=arxiv:2611.08312v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-05
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Johannes Taraz, Abhinav Kumar, Sahar Abdelnabi
  - Categories: cs.MA
  - Abstract: Personal AI agents often act on underspecified instructions and use context such as previous conversations to decide how to proceed. This context may contain private preferences that influence the assigned task or the relation to other people. When asked by a third party to justify its choices, the agent might be conflicted between honesty, confidentiality and task completion. Prior work has studied these largely as separate problems. We study deception and leakage of private information together in a simulated company Slack workspace. There, four employees delegate a sprint staffing to their personal agents. From private messages, two of these agents learn that their employee avoids workin…
- [ ] **[TITAN: DRL-Based Dynamic Scheduling and Resource Allocation for Tactile Internet](https://arxiv.org/abs/2611.27560v1)**
  <!-- aidb:id=arxiv:2611.27560v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Qingrui Fan, Vineet Gokhale, Jayakrishnan Nair, Johannes Cottyn
  - Categories: cs.NI, cs.LG, eess.SP
  - Abstract: Tactile Internet (TI) applications require ultra-reliable, low-latency tactile communication alongside video traffic. However, tactile Quality of Service (QoS) requirements vary with the interaction context, making fixed resource allocation inefficient. In this paper, we propose TITAN (Two-Timescale Integrated Tactile Internet over 5G Access Networks), a dynamic scheduling and resource allocation (SRA) scheme. TITAN receives time-varying tactile QoS profiles from a higher-layer module and adapts SRA to the current QoS profile and network state. A deep reinforcement learning-based agent splits the available network bandwidth between tactile and video streams at a slow timescale, while a fast…
  - Comment: 7 pages, 5 figures. Submitted to IEEE ICC 2027
- [ ] **[Can Language Models See the Circuit in Pixelated RFIC Passives?](https://arxiv.org/abs/2611.27559v1)**
  <!-- aidb:id=arxiv:2611.27559v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jonathan Zhou, Kaushik Sengupta
  - Categories: cs.AI, cs.AR, physics.app-ph
  - Abstract: The emergence of inverse-designed, pixelated passives for microwave and millimeter-wave applications has been a major development in the field of RFIC design. These devices, which appear to be QR-code-like in structure, exist in a generalizable, high-dimensional design space that includes conventional passive topologies. However, these structures are naturally unintuitive for designers, and failures or deviations in performance are difficult to debug. In this work, we ask whether a frontier language model can understand, predict, and edit the responses and layout structure of pixelated passives. The agent, run with all tools disabled, is first asked to read layouts on 18x18 and 27x27 tile g…
  - Comment: 21 pages, 24 figures (5 main, 19 supplementary), 2 tables
- [ ] **[Bringing AI Assistance to the Beznau Nuclear Power Plant: A Hierarchical System of LLM Agents for Reactor Monitoring](https://arxiv.org/abs/2611.27556v1)**
  <!-- aidb:id=arxiv:2611.27556v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Wenqi Zhou, Leonardo Baldo, Edwin Kolbe, Manuel Arias Chao
  - Categories: cs.MA, cs.AI
  - Abstract: Beznau Unit 1 in Switzerland, in operation since 1969, is the most experienced nuclear reactor still running worldwide. Five decades of incremental modernization have left its monitoring systems, alarm logs, variable catalogs, technical specifications and investigation reports in separate silos that were never designed to be queried together. As a result, investigating a core instrumentation anomaly means slow, manual gathering of knowledge scattered across databases, documents, and experienced colleagues. We present a hierarchical multi-agent assistant built on large language models (LLMs) to support these investigations and reduce the need for tedious manual searches in SAP systems. An or…
- [ ] **[Adapting the Process of Adaptation: Darwinian, Lamarckian, and Agent-Directed Evolution in AI](https://arxiv.org/abs/2611.07048v2)**
  <!-- aidb:id=arxiv:2611.07048v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-04
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Andrew W. Lo, Chaoyi Zhao
  - Categories: cs.AI
  - Abstract: Evolution has shaped intelligence for billions of years. Artificial intelligence (AI) now raises a striking possibility: intelligence may begin to direct its own evolution. As AI agents become capable of modifying and evaluating their own behavior, how quickly could they improve, and how can that improvement remain safe? We develop a theoretical framework comparing Darwinian, Lamarckian, and agent-directed evolution following environmental change. Darwinian evolution relies on natural selection, Lamarckian evolution adds inherited learning, and agent-directed evolution allows agents to generate and evaluate behavioral variants and choose how extensively to search. When learning is sufficien…
- [ ] **[Alignment by Socialization: Learning Tradeoffs Under Selection](https://arxiv.org/abs/2611.18531v2)**
  <!-- aidb:id=arxiv:2611.18531v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-13
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Thomas Brennan, Andrew W. Lo, Chaoyi Zhao
  - Categories: cs.AI, q-bio.PE, q-fin.GN
  - Abstract: Artificial intelligence (AI) agents are expected to complete tasks while following rules of conduct, but these objectives can conflict. We study how evolutionary selection shapes an agent's choices between them, and whether experience can make those choices reflect human judgments and withstand subsequent pressures. In our model, copies of an agent face a common uncertain reward state, and only those taking the rewarded action reproduce. We show that long-run growth is maximized when each action is taken as often as the environment rewards it. We compare three policies. A task-only policy thrives in a sandbox rewarding completion alone but fails when conduct matters. A fixed linear policy i…
- [ ] **[Epistemic Social Learning: Latent Behavioral Structure under Endogenous Multi-Agent Interaction](https://arxiv.org/abs/2611.27545v1)**
  <!-- aidb:id=arxiv:2611.27545v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jainendra Shukla, Dhruv Jaiswal, Divyanshi Beniwal, Kiriti Kanjilal
  - Categories: cs.MA, cs.GT
  - Abstract: In multi-agent interaction, a learner's actions shape the observations from which it infers other agents' behavior. A behavioral model may predict these observations well yet support poor adaptation when opponents change. We introduce Epistemic Social Learning (ESL), which couples fast, interaction-specific Bayesian beliefs with slower online learning of population-shared behavioral prototypes. Belief-conditioned decisions influence subsequent observations and, in turn, the representations learned from them. Under explicit regularity and averaging assumptions, we provide a conditional stochastic-approximation characterization of these coupled dynamics. Across twelve synthetic $3\times3$ coo…
  - Comment: Accepted at NeurIPS 2026. 44 pages, 6 figures. Code: https://github.com/jainendra2019/esl
- [ ] **[Alliance Rupture and Repair in Simulating Cognitive Behavioral Therapy Dialogues](https://arxiv.org/abs/2611.27544v1)**
  <!-- aidb:id=arxiv:2611.27544v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jian Chai, Yitian Yang, Siqi Liu, Yi-Chia Wang, Yi-Chieh Lee
  - Categories: cs.CL
  - Abstract: In cognitive behavioral therapy (CBT), routine work can strain the client-counselor working alliance, and the counselor must then notice the rupture, repair it, and adapt the work that follows. Existing CBT simulators model client resistance and follow structured treatment plans, but rarely track alliance state or allow counselors to repair ruptures over multiple turns and revise their plans accordingly. We present ALLY, a simulation framework that brings alliance rupture, repair, and replanning into ongoing CBT dialogue. Each client has a hidden alliance state that governs how openly the client engages. Like a real counselor, the counselor agent sees only the dialogue. It must notice when…
- [ ] **[When Visually Rich Documents Meet Multi-Vector Retrieval for Region-level Retrieval-Augmented Generation](https://arxiv.org/abs/2611.27542v1)**
  <!-- aidb:id=arxiv:2611.27542v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Xu Yuan, Liangbo Ning, Yujuan Ding, Qing Li, Wenqi Fan
  - Categories: cs.CV
  - Abstract: Visually rich documents (VRDs) convey knowledge through textual, visual, and layout information that text-centric Retrieval-Augmented Generation (Text-RAG) struggles to fully exploit. Recent Vision-RAG approaches enable retrieval and generation directly from document images, retaining this multimodal information. However, earlier Vision-RAG methods commonly adopt coarse retrieval representations and full-page visual contexts, which can obscure local evidence and introduce substantial redundancy and computational overhead. To address these challenges, we propose MV-VisRAG, a region-level Vision-RAG framework that uses semantically complete regions for both document representation and visual…
- [ ] **[Where Delay Compensation Belongs in a Decentralized Mean-Field-Game Swarm with a Control-Barrier Safety Filter](https://arxiv.org/abs/2611.27540v1)**
  <!-- aidb:id=arxiv:2611.27540v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jan Mikołajczyk, Igor Rostkowski, Bartosz Ogórkiewicz, Szymon Skierski, Sylwia Opat, Wojciech Rybak, Mikołaj Sczogiel, Radosław Pałys, Jan Gogulski, Bartosz Kościołek, Andrzej Pijanowski, Szymon Kowalski, Marcin Misiewicz
  - Categories: cs.RO, cs.MA, eess.SY
  - Abstract: Large robot teams are often run as a plan-then-execute stack. We study a decentralized instance for drone swarms, a mean-field-game (MFG) routing field with a per-agent control-barrier-function (CBF) safety filter, when communication is limited by a shared TDMA channel. Neighbors are known only through noisy range and bearing measurements exchanged in round-robin slots, so the frame, and with it the age of every estimate, grows with swarm size. In simulation this delay reaches both layers but breaks only the safety layer. Without delay, swarms of up to 100 agents do not collide, even with each measurement's noise held for a whole frame; with it, stale estimates at the CBF cause collisions b…
  - Comment: 9 pages, 3 figures, 2 tables. Submitted to the 8th International Workshop on Multi-Agent Path Finding (WoMAPF) at AAAI-27 (non-archival workshop)
- [ ] **[Fix Where It Fails: Root-Cause-Guided Agentic Harness Optimization for Scene Graph Generation](https://arxiv.org/abs/2611.27529v1)**
  <!-- aidb:id=arxiv:2611.27529v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jee Eun Kim, Donghyeon Choi, Sangjune An, Hae Beom Lee, Kyong Hwan Jin
  - Categories: cs.CV, cs.AI, cs.MA
  - Abstract: Scene graph generation (SGG) aims to detect objects in an image and predict the relationships between them. The standard PredCls, SGCls, and SGDet settings show how much performance drops without ground-truth boxes and labels, but not where or why a model fails. Knowing this would allow fixing a model where it fails, without retraining. We propose RoHa-SGG (Root-cause-guided Harness optimization for SGG), which extends agentic harness optimization to SGG. It optimizes the harness, the inference code around a frozen SGG model. RoHa-SGG has two main LLM agents. A root-cause analysis (RCA) agent finds the components where the model fails and diagnoses why, and a proposer agent searches for a h…
- [ ] **[OmniHarness: Harnessing Generalizable Visual Generation via Symbolic Policy Learning](https://arxiv.org/abs/2609.16057v2)**
  <!-- aidb:id=arxiv:2609.16057v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-13
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Xu Xu, Jinxiu Liu, Zhangbo Qiao, Cheng Song, Jiaxing Lu, Xiangyu Zhang, Yubin Gu, Fangwei Ning, Yan Shi
  - Categories: cs.LG, cs.AI
  - Abstract: Unified multimodal large language models and multi-agent systems have advanced visual generation. However, several limitations remain. (1) Experience acquisition is typically reactive, occurring only in response to downstream tasks. (2) Accumulated knowledge varies in relevance and reliability, making efficient and effective reuse challenging. To address these limitations, we introduce OmniHarness, a framework for generalizable visual generation via symbolic policy learning. Before downstream objectives are specified, self-directed inquiry autonomously generates and executes practice tasks, with selection guided by capability novelty and the current competence frontier. Verified workflows a…
- [ ] **[AutoMaster: Autonomous Post-Training by Making the Same Model a Better Teacher](https://arxiv.org/abs/2611.26510v2)**
  <!-- aidb:id=arxiv:2611.26510v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Guoxin Chen, Shuang Sun, Fanzhe Meng, Xinyu Tang, Ruihua Song, Wayne Xin Zhao
  - Categories: cs.CL
  - Abstract: Task success alone does not specify which behaviors post-training should reinforce. Even successful teacher trajectories can contain unsupported assumptions, unproductive repetition, or superficial verification. We propose Skill-FT (Skill-Guided Fine-Tuning), which uses natural-language skills to suppress undesirable habits and elicit underrepresented effective behaviors during teacher rollouts, then fine-tunes a student model on the resulting trajectories. We introduce AutoMaster, an autonomous post-training system in which an LLM agent develops these interventions through trajectory analysis, skill design, data selection, and feedback from rollouts and evaluation. Across Terminal, Search,…
  - Comment: Website: https://aweai-team.github.io/AutoMaster/ Code: https://github.com/RUCAIBox/AutoMaster Models: https://huggingface.co/collections/RUC-AIBOX/automaster
- [ ] **[Extended Wigner's Friend Scenarios with Agent-like Observers on Quantum Computers](https://arxiv.org/abs/2609.12527v2)**
  <!-- aidb:id=arxiv:2609.12527v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-11
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Joshua Laux, Eric G. Cavalcanti
  - Categories: quant-ph
  - Abstract: The Wigner's friend thought experiment raises the question of whether quantum theory can be applied consistently to systems that include observers. Extended Wigner's Friend Scenarios include spatially separate observers sharing entanglement. In the Local Friendliness (LF) framework, these scenarios lead to experimentally testable inequalities derived from Absoluteness of Observed Events and Local Agency, assumptions weaker than those needed for Bell inequalities. Their violation therefore has stronger implications, but LF tests are more experimentally challenging because they require an observer implemented as a quantum system. Drawing from the literature on artificial intelligence, we impl…
- [ ] **[NavRSI: Recursive Harness Self-Improvement for Vision-and-Language Navigation](https://arxiv.org/abs/2611.27499v1)**
  <!-- aidb:id=arxiv:2611.27499v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Guangzhao Dai, Guoxin Lian, Shuo Wang, Shengbin Yue, Qianru Sun, Xiangbo Shu, Bin Zhu
  - Categories: cs.RO
  - Abstract: Frontier large language models (LLMs) have enabled vision-and-language navigation (VLN) through direct closed-loop perception and action. However, navigation performance depends strongly on the harness governing LLM-environment interactions, while existing harnesses largely rely on manually designed navigation tools, memory, and agent roles. We introduce NavRSI, a harness-centric recursive self-improvement framework that optimizes the navigation behavior of frozen LLMs through closed-loop experience. In each round, NavRSI iteratively collects navigation trajectories and failure diagnostics, employs a designer agent to rewrite the harness, and retains the revisions that prove effective, whil…
- [ ] **[Risk sharing for background risk models with infinite mean](https://arxiv.org/abs/2611.27485v1)**
  <!-- aidb:id=arxiv:2611.27485v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ziting Miao, Yuyu Chen, Han Li
  - Categories: q-fin.RM
  - Abstract: Risk sharing is usually viewed as beneficial for risk-averse agents facing independent risks with finite means, but this situation can be reversed for infinite-mean losses. In this paper, we explore the effects of risk sharing for positively dependent infinite-mean losses using background risk models. Under both linear and conditional mean risk sharing, we show that risk sharing of infinite-mean losses can increase the risk in the sense of usual stochastic order. Our results cover classical multivariate loss distributions, including the Pareto-Clayton and the Fréchet-Gumbel models. For linear risk sharing, we further derive stochastic dominance relations between diversified portfolios, incl…
- [ ] **[From Manufacturing Event Logs to Simulation: Enabling SMEs with Agentic AI for SimPy Simulation Generation](https://arxiv.org/abs/2611.27483v1)**
  <!-- aidb:id=arxiv:2611.27483v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Richard Reider, Lina Döring, Sebastian Lang, Tobias Reggelin, Sebastian Trojahn, Pascal Reusch
  - Categories: cs.AI
  - Abstract: High expertise and cost barriers exclude small and medium-sized enterprises from discrete-event simulation (DES). We introduce GenAI4SimPy, a multi-agent framework powered by Qwen 3.6 (27B), an open-weight large language model, that automates end-to-end DES generation from manufacturing event logs to executable SimPy models through tool-augmented reasoning and human-in-the-loop validation. Evaluated on three execution blocks from a public smart factory dataset, the framework achieved a mean absolute percentage error of 7.9\% and coverage of failure rate for all three blocks and of throughput for two of three. A fidelity paradox was observed: accurate process-level parameters did not ensure…
  - Comment: 12 Pages, 2 figures, Winter Simulation Conference 2026 Glasgow, Scotland
- [ ] **[Communication-constrained multiagent risk estimation: a simulation benchmark for adult sore throat](https://arxiv.org/abs/2611.27468v1)**
  <!-- aidb:id=arxiv:2611.27468v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Anas H. Alzahrani
  - Categories: cs.MA
  - Abstract: Distributed predictive agents may need to approach a shared estimate under limited, unreliable communication. We evaluated classical symmetric pairwise gossip among five agents initialized from frozen calibrated predictions in a synthetic adult sore-throat benchmark. Ninety runs across three fixed generator families supplied 270,000 underlying test encounters, each observed through four missingness views. Complete, ring and star graphs were compared at eight interaction budgets and transaction failure probabilities of 0, 0.2 and 0.5. The coordination extension was designed after inspection of the predictive benchmark and is exploratory. Outcomes were disagreement around the conserved arithm…
  - Comment: 31 pages, 3 main figures, 2 main tables; includes supplementary methods, 7 supplementary tables and 4 supplementary figures. Simulated data; code and fixed inputs included
- [ ] **[ROSWORLD: When Digital Task Competence Meets Physical Execution](https://arxiv.org/abs/2611.27467v1)**
  <!-- aidb:id=arxiv:2611.27467v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Caoyuan Ma, Wendi Liu, Zhimin Zhang, Muyao Niu, Yujie Lu, Zengxi Zhang, Ji Zhao, Shuai Dong, Wenpu Liu, Ziyue Wang, Wenzheng Chang, Taiqiang Wu, Weichu Xie, Yuqi Xu, Haiyuan Wan, Xuehui Wang, Jiaqi Wang, Wenqi Shao, Yinqiang Zheng
  - Categories: cs.RO, cs.AI, cs.CV
  - Abstract: Computer-use agents now solve most desktop tasks through direct software input, but a robot using the same computer must turn GUI knowledge into physical contact with a keyboard and mouse. We introduce ROSWorld, a benchmark that couples a physically simulated robot workstation to a live OSWorld desktop, so that a robot and a desktop agent pursue the same goals under the same official evaluators. The evaluated model receives observations only from the workstation camera views and operates the peripherals through either a single-arm rigid probe or dual-arm dexterous hands. Across five frontier models and 40 tasks in ten applications, models that complete 31-39 tasks on the desktop complete at…
  - Comment: 13 pages, 9 figures, 4 tables
- [ ] **[Poisoning Attacks and Collaborative Defense Framework for LightRAG-Based Construction Regulation Knowledge](https://arxiv.org/abs/2611.27460v1)**
  <!-- aidb:id=arxiv:2611.27460v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yingyan He
  - Categories: cs.CR
  - Abstract: Retrieval-augmented generation (RAG) is widely used in construction, yet the security of building-regulation knowledge bases has received little study. This thesis reports a pre-registered experiment on one fully instrumented LightRAG system built on the UK Approved Documents. Using a 150-item benchmark labeled with safety consequences and tampering directions, it evaluates four attacks (text layer, graph layer, fabricated amendment narrative and a defense-aware adaptive attacker) together with a three-layer retrieval-graph-generation defense in a full factorial design. Text-level poisoning succeeded, with success rising with the budget; graph-level poisoning was less effective, contrary to…
  - Comment: Master's thesis, SWISS UMEF, November 2026. 60 pages, 35 tables, 10 figures
- [ ] **[Binary Decision Process in Pre-Evacuation Behavior](https://arxiv.org/abs/2508.08284v5)**
  <!-- aidb:id=arxiv:2508.08284v5 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-08-01
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Peng N. Wang, Peter B. Luh, Peter Sincak, Laura Pitukova, Xuesong Lu, W. M. Wonham, Timo Korhonen
  - Categories: physics.soc-ph, cs.MA, eess.SY, nlin.AO
  - Abstract: In crowd evacuation the time interval before decisive movement towards a safe place is defined as the pre-evacuation phase, and it has crucial impact on the total time required for safe egress. This process mainly refers to situation awareness and response to an external stressors, e.g., fire alarms. Due to the complexity of human cognitive process, simulation is used to study this important time interval. In this paper a binary decision process is formulated to simulate pre-evacuation time of many evacuees in a given social context. The model combines the classic opinion dynamics (the French-DeGroot model) with binary phase transition to describe how group pre-evacuation time emerges from…
  - Comment: 7 pages
- [ ] **[Learning When to Ask: Advisor-Aware Post-Training for SLM Agents](https://arxiv.org/abs/2611.27443v1)**
  <!-- aidb:id=arxiv:2611.27443v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Aasheesh Singh, Vishal Vaddina
  - Categories: cs.LG, cs.AI
  - Abstract: Small language models (SLMs) are increasingly attractive for cheap, high-throughput agentic deployment, but they remain weak at multi-step reasoning and tool use that long-horizon tasks demand. We study how to post-train an SLM to seek advice from a stronger model and act on that advice itself, following an advisor-executor pattern. Out of the box, this pattern fails across open- and closed-source small-model families: wiring an SLM to an advisor is a harness-design matter that is not enough on its own. A post-training recipe is needed to teach the model when to ask, in a cost-aware fashion, and how to follow advice across steps. Our method, ADAPT (ADvisor-Aware Post-Training), is a multi-s…
  - Comment: Published at the OE-Agent Workshop (Open and Efficient Agentic AI for Resource-Constrained Environments) at ACML 2026 14 pages, 2 figures, 5 tables
- [ ] **[Consensus of Consensus: Decentralized Consensus-Based Optimization](https://arxiv.org/abs/2611.27433v1)**
  <!-- aidb:id=arxiv:2611.27433v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Stefania Bellavia, Massimo Fornasier, Greta Malaspina, Tim Roith
  - Categories: math.OC, math.NA
  - Abstract: We propose and analyze a decentralized variant of Consensus-Based Optimization (CBO) for the global minimization of continuous, possibly non-convex functions accessible only through a stochastic, possibly biased, zeroth-order oracle with bounded mean-squared error. The agents are split among $N$ units of an undirected communication network. Each unit evolves its swarm of $M$ agents towards a local tracking variable, which follows the network average of the local consensus points through one round of neighbour-to-neighbour communication via a doubly stochastic mixing matrix, without any central coordinator. We show that, under an explicit condition linking the drift and diffusion parameters…
- [ ] **[TrojanMaxxing: One-shotting VLM Backdoors with Weight-Space Programming](https://arxiv.org/abs/2611.27425v1)**
  <!-- aidb:id=arxiv:2611.27425v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ahaan Dabholkar, Harshvardhan Patel, Michalis Polychronakis, Saurabh Bagchi
  - Categories: cs.CR, cs.AI, cs.CV
  - Abstract: Recent work shows that large language models (LLMs) can reason directly about the weights of other neural networks. Given only a natural-language objective, an LLM can inspect a model's weights, understand what they compute, and edit them directly without gradient-based optimization. This capability, termed weight-space programming (WSP), has been used to improve model performance on math reasoning, medical QA and other benchmarks. We propose TrojanMaxxing, a novel strategy to backdoor vision-language models (VLMs), by reframing it as a WSP task. We use Claude Opus 5.5 and Mythos 5.2 agents to backdoor VLMs without any optimization or training methods. The agents inspect the model weights,…
  - Comment: 14 pages, 8 figures
- [ ] **[Beyond Future Views: Exploring Future-State World Models for Vision-Language Navigation](https://arxiv.org/abs/2611.27418v1)**
  <!-- aidb:id=arxiv:2611.27418v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Kangyi Wu, Pengna Li, Yucheng Wang, Yance Fang, Xihan Ma, Zhizhong Su, Yang Wu, Ye Deng, Jinjun Wang, Jianyi Liu
  - Categories: cs.RO
  - Abstract: Vision-Language Navigation(VLN) requires an embodied agent to follow language instructions through unseen 3D environments, where the target spaces often lie beyond the current observation. Navigation world models address this challenge by predicting future views either as pixels or latent representations, providing valuable look-ahead information for action decision. Both paradigms define the future primarily through what the agent may observe, raising a fundamental question: is predicting future views the ultimate form to represent the future for VLN? Cognitive studies show that the human hippocampus prospectively represents both future goals and intervening locations along planned routes.…
- [ ] **[STARK: Moving towards Personalized Agents That Truly Learn and Remember](https://arxiv.org/abs/2611.25705v2)**
  <!-- aidb:id=arxiv:2611.25705v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Aryan Jain, Abhishek Jha, Anish Nediyanchath, Promod Yenigalla
  - Categories: cs.CL, cs.AI, cs.IR
  - Abstract: Long-term memory is essential for personalized agentic systems that interact with users over long time periods, yet current architectures only capture what happened while leaving the reasoning of why it happened to be derived later by underlying LLMs. These events can, however, convey not only what a user experienced but also how that experience shaped their behavioral patterns. We introduce STARK, a dual-graph memory architecture which treats these events not just as nodes but also as edges between behavioral insights. STARK maintains an Episodic Graph which records interactions as temporally, causally, and semantically linked episodes; and an Insight Graph which represents LLM-extracted b…
  - Comment: Accepted at IAAI-2027 (Emerging Applications Track)
- [ ] **[Neural variational Skyrmions as a topological benchmark: emergent symmetry, precision energies and KAN--MLP comparison](https://arxiv.org/abs/2611.27411v1)**
  <!-- aidb:id=arxiv:2611.27411v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Koji Hashimoto, Masaki Murata, Gakuto Ogiwara
  - Categories: hep-th, cs.LG, nucl-th, physics.comp-ph
  - Abstract: We propose the three-dimensional Skyrme model as a topological benchmark for neural variational methods and construct fully three-dimensional Skyrmions with baryon number $B=1,\ldots,4$ without imposing a symmetry ansatz, with high precision. For $B=2,3,4$, the relaxation of these Skyrmions starts from $B$ unit-charge lumps with random positions and orientations, which carry no symmetry information. The known toroidal, tetrahedral, and cubic Skyrmions nevertheless emerge spontaneously. The resulting variational energies for $B=1,\ldots,4$ lie slightly below the published reference values. The neural method highlights the high accuracy for retaining the topological charge, differing from $B$…
  - Comment: 32 pages, 6 figures, 12 tables. Code and data: https://doi.org/10.5281/zenodo.24390286
- [ ] **[Detecting Word-Substitution Poisoning of a RAG Knowledge Base with Relative Entropy and Runtime Verification](https://arxiv.org/abs/2611.27410v1)**
  <!-- aidb:id=arxiv:2611.27410v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ali Yousefi, Nikos Komninos, Hafizul Asad
  - Categories: cs.CR, cs.AI
  - Abstract: A retrieval-augmented generation (RAG) system answers questions using passages it retrieves from a knowledge base, so users must trust that knowledge base. We study an attacker who quietly edits existing passages by swapping words for synonyms (PWWS, TextFooler) in a cybersecurity RAG system built from MITRE ATT&CK and CAPEC. Using a reviewed 44-question benchmark, repeated paired runs and a control corpus in which only the layout changes, we find that poisoning lowers judged answer correctness from 0.714 to 0.555. The damage comes mostly from lost evidence and refusals, not from false statements. To find the edited passages, we use relative entropy. Comparing a whole passage with normal te…
- [ ] **[Combatting adversarial distillation](https://openai.com/index/combatting-adversarial-distillation)**
  <!-- aidb:id=url:7ad44f990f0c53ef2e2a -->
  - Feed: OpenAI research and engineering
  - Published: 2026-11-20
  - Topics: research, engineering
  - Abstract: OpenAI’s layered approach to adversarial distillation combines model training, safeguards, detection, and enforcement to protect against capability extraction.
- [ ] **[Evidence sufficiency assessment enables cost-effective review allocation in on-premise clinical AI agents](https://arxiv.org/abs/2611.27390v1)**
  <!-- aidb:id=arxiv:2611.27390v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yiwen Qiu, Che Sun, Shu Shen, Wentao Wang
  - Categories: cs.AI
  - Abstract: On-premise clinical AI agents must auto-accept high-confidence diagnoses, deferring others to clinician review, yet token probabilities and self-reported confidence miss errors, while more reliable five-run consistency incurs fivefold compute. We propose training-free decision-point evidence sufficiency assessment and a three-tier sequential triage protocol. Masking reasoning and diagnosis, the same 4B model scores sufficiency from objective evidence via prior-debiased probabilities over five ordered levels. Calibration freezes a nominal top-50% threshold, selecting single-run, five-run consistency, or full-deferral tiers by whether the one-sided 95% Wilson lower confidence bound of pass ra…
- [ ] **[What Stays in the Picture? From Redundant Instructions to Dependency-Aware Image Editing](https://arxiv.org/abs/2611.27388v1)**
  <!-- aidb:id=arxiv:2611.27388v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zi-Jun Wang, Yu Lin, Zhilin Zhao
  - Categories: cs.CV
  - Abstract: We introduce complex redundant-instruction image editing, where a single request specifies multiple objects, their attributes, and spatial relations while revising or canceling earlier editing requirements. Direct editing can fail to recover this intent, while splitting the request into successive steps can preserve obsolete edits and visual errors. Our key insight is to resolve the revision history into a final editing target that jointly guides planning and verification, so that obsolete requests do not become visual edits. Based on this insight, CRIE-Agent learns to consolidate revisions into object-level final intent and executes the retained objects in reference-first blocks, establish…
- [ ] **[VMSA: Video Memory Skill Agent for Long Video Understanding](https://arxiv.org/abs/2611.27381v1)**
  <!-- aidb:id=arxiv:2611.27381v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Changin Choi, Jungwon Park, Jungmin Ko, Jimyeong Kim, Wonjong Rhee
  - Categories: cs.CV, cs.AI
  - Abstract: Long-video question answering requires retrieving and integrating relevant evidence from videos spanning hours or even days. Recent agentic approaches organize video information into external memories and iteratively retrieve evidence to answer questions. However, effective retrieval and reasoning remain challenging, as agents must determine what information to search for, which memory sources to access, and how to connect evidence across distant temporal intervals. To address these challenges, we propose Video Memory Skill Agent (VMSA), a framework that jointly designs structured video memories and memory skills for long-video understanding. VMSA constructs three complementary memory compo…
- [ ] **[Composable Soft-Prompt Distillation of RL Experts: Toward Continual Post-Training](https://arxiv.org/abs/2611.27376v1)**
  <!-- aidb:id=arxiv:2611.27376v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zhen Zhang, Changyi Yang, Xuehai He, Chengzhi Liu, Yutong Yin, Ziyue Liu, Zhuoran Yin, Yangmin Li, Zhihan Liu, Jisen Li, Mingyu Jin, Chuhan Li, Zhaotian Weng, Ruoyu He, Wenyao Gao, Jiaxin Deng, Chenwei Wu, Hui Shen, Wenhao Chai, Chenyang Zhao, Zhuofan Ying, Kieran Liu, Andrew Chen, Pony Ma, Zhaoran…
  - Categories: cs.LG, cs.CL
  - Abstract: RL post-training typically produces domain experts that must then be consolidated into one model, and as new experts keep arriving, this consolidation becomes a continual process. Weight merging and multi-teacher on-policy distillation (MOPD) must re-consolidate the whole model whenever an expert is added, and can erode capabilities outside the target domains. We propose Composable Soft-Prompt Distillation (CSPD), which keeps the pre-RL model frozen, distills each RL expert independently into a soft prompt, and composes experts by concatenating their prompts without joint training. A single soft prompt suffices to distill an RL expert, recovering at least 90% of the teacher's gain in 22 of…
- [ ] **[Testing for Coordination Failures in Cooperative Multi-Agent Reinforcement Learning](https://arxiv.org/abs/2611.27368v1)**
  <!-- aidb:id=arxiv:2611.27368v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Dennis Gross, Jørn Eirik Betten, Helge Spieker
  - Categories: cs.MA, cs.AI, cs.SE
  - Abstract: Deep parallel cooperative multi-agent reinforcement learning (CMARL)} trains multiple agents that all act at every time step to optimize a common objective. Like single-agent RL, CMARL can produce unsafe behaviors that violate implicit safety requirements not captured by the reward, and these behaviors are hard to explain. However, testing CMARL policies for safety has received less attention than the safety testing of single-agent RL policies. In this paper, we propose DisQ, a test case selection method that identifies failure-revealing states in value-based CMARL by exploiting a signal specific to trained Q-learning agents. The signal is the Q-value gap, an explainable metric that flags a…
  - Comment: STVR
- [ ] **[KV-Control: Parameter-Efficient K/V Injection for Trajectory-Controlled Text-to-Motion](https://arxiv.org/abs/2606.05624v2)**
  <!-- aidb:id=arxiv:2606.05624v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-04
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Tengjiao Sun, Pengcheng Fang, Xiaoyu Zhan, Yanwen Guo, Dongjie Fu, Xiaohao Cai, Hansung Kim
  - Categories: cs.CV, cs.GR
  - Abstract: Text-conditioned 3D human motion models now synthesize plausible motions from prompts, but practical animation and embodied-agent workflows rarely stop at text: a character may need to follow a sketched root path, hit an end-effector target, or satisfy a multi-joint trajectory while still preserving the gait, style, and intent described by language. This exposes a control trade-off. A trajectory controller should be precise without overwriting the pretrained text-conditioned motion prior, yet existing solutions either duplicate large portions of the generator to regain per-layer control access or move much of the cost to test-time optimization. We introduce KV-Control, a compact attention-s…
- [ ] **[Breaking the Long Horizon: Short-Horizon Process Supervision for Long-Form Generation in LLMs](https://arxiv.org/abs/2611.27348v1)**
  <!-- aidb:id=arxiv:2611.27348v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Heyang Xu, HanWen Hao, Qianren Mao, Zhuo Liu, Qili Zhang, Sheng Yang, Jianxin Li
  - Categories: cs.CL
  - Abstract: Long-form generation is increasingly important for agentic LLM systems, yet current reinforcement learning methods typically optimize an entire document with a single outcome-level reward. This delayed and coarse-grained supervision makes it difficult to localize errors and assign credit across semantically distinct parts of the output. To address this, we propose a short-horizon framework that reformulates long-form generation through semantic decomposition into segment-level decisions. Each segment is generated with prefix-conditioned context, allowing cross-segment coherence to be preserved while keeping supervision local. The generated segments are then scored with rubric-based rewards…
  - Comment: Submitted to AAAI 2027. 17 pages, 8 figures
- [ ] **[Dual-Agent DRL based Cooperative Beamforming and Trajectory Optimization for UAV-ISAC Networks](https://arxiv.org/abs/2611.27346v1)**
  <!-- aidb:id=arxiv:2611.27346v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Kaijian Yang, Feng Wang, Guojun Han, Xin Wang, Vincent K. N. Lau
  - Categories: cs.IT, eess.SP
  - Abstract: This paper considers a low-altitude unmanned aerial vehicle (UAV) network, where multiple ground base stations (BSs) provide integrated sensing and communication (ISAC) services for multiple communication UAVs (C-UAVs) and sensing UAVs (S-UAVs). With the objective of maximizing the average sum rate of C-UAVs over the entire flight episode, we jointly optimize the multi-BS multi-UAV ISAC beamforming and trajectory design, subject to the BS transmit power budget and the sensing signal-to-interference-plus-noise ratio (SINR) constraints of S-UAVs, as well as the flight mission and collision avoidance constraints of C-UAVs and S-UAVs. Based on the multi-agent deep reinforcement learning (MADRL)…
  - DOI: 10.1109/JIOT.2026.3754786
  - Comment: 16 pages, 10 figures, accepted by IEEE Internet of Things Journal
- [ ] **[ThunderSync: Lossless Acceleration of Agentic Reinforcement Learning](https://arxiv.org/abs/2610.05935v2)**
  <!-- aidb:id=arxiv:2610.05935v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-05
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Seil Kang, Hangoo Kang, Tarun Suresh, Youngeun Kim, Shreyas Pimpalgaonkar, Seong Jae Hwang, Azalia Mirhoseini
  - Categories: cs.LG, cs.AI
  - Abstract: Language models are moving beyond generating answers to pursuing long-horizon goals in interactive environments. Post-training these agents requires long, heterogeneous trajectories, and synchronous systems leave learner engines idle until rollout and verification finish. To squeeze out these pipeline bubbles, asynchronous training overlaps rollout and learning across updates, but comes at the cost of policy staleness. We introduce ThunderSync, which starts gradient computation as soon as all required inputs are fixed, without policy staleness. For group relative policy optimization (GRPO), ThunderSync computes each trajectory's score gradient as soon as the reward for that trajectory arriv…
- [ ] **[RynnUnify: Towards Unified Embodied Brain](https://arxiv.org/abs/2610.32965v2)**
  <!-- aidb:id=arxiv:2610.32965v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-23
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Minghao Zhu, Bohan Hou, Kun Xiang, Zixuan Wang, Yinzhou Tang, Yifei Yang, Zhikai Wang, Tianyi Zhang, Kehan Li, Haoyu Zhao, Siteng Huang, Leigang Qu, Sicong Leng, Dongchi Huang, Xiao Lin, Ronghao Dang, Mingxiu Chen, Shijian Lu, Yue Wang, Xiaodan Liang, Zhenyu Zeng, Deli Zhao, Chengju Liu, Jianfei Ya…
  - Categories: cs.RO
  - Abstract: We introduce RynnUnify, a 16B unified embodied model that combines strong embodied understanding with long-horizon visual planning through interleaved video--language reasoning. With capabilities spanning spatial reasoning, physical prediction, and grounding, RynnUnify connects an understanding of the physical world with visual anticipation of how it evolves across successive subtasks. Building on these capabilities, we further develop an agentic extension through reinforcement learning to selectively use video predictions for reasoning about unobserved states and interaction outcomes. We also develop a world-action extension of the full RynnUnify model, translating its understanding and pr…
- [ ] **[Why Tabular Foundation Models Excel on Relational Data They Have Never Seen](https://arxiv.org/abs/2611.02936v3)**
  <!-- aidb:id=arxiv:2611.02936v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-02
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Linjie Xu, Yiqun Hu, Jixiang He, David Wipf
  - Categories: cs.AI, cs.DB, cs.LG
  - Abstract: Given a relational database (RDB) storing heterogeneous tabular information, how can we predict missing (or future) values in some target column of interest? As candidate targets are numerous in enterprise settings, it is preferable to avoid learning a new model from scratch each time there is a new prediction task. Frozen foundation models (FMs) based on in-context learning (ICL) and RDB-specific pre-training provide a viable solution, but the ideal design still remains largely unresolved. Perhaps unexpectedly, preliminary evidence has recently shown that existing single-table FMs (aka TFMs), when combined with suitable parameter-free relational encoders, can be quite competitive in practi…
- [ ] **[Zing-1.0: A Playable World System Built on Controllable Rendering](https://arxiv.org/abs/2611.27336v1)**
  <!-- aidb:id=arxiv:2611.27336v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Wenbo Zhang, Guoli Zhang, Xuewen Yu, Xueliang Yang, Jiangqiao Yan, Teng Xia, Xinmiao Wu, Zeyang Tian, Haoze Sun, Jinghui Niu, Hongli Ning, Zhiyuan Liu, Xinna Liu, Weimin Liu, Jialin Liu, Tianpeng Li, Kejun Li, Jun Li, Jiawen Li, Yirong He, Haoyuan Guo, Bosheng Gong, Junhao Gao, Xiaoxiao Fu, Xuezhi…
  - Categories: cs.CV
  - Abstract: We present Zing-1.0, a Playable World System built on Controllable Rendering. An executable engine resolves player actions under the world's rules and produces proxy video from the updated state. A streaming video model synthesizes the player's view from this proxy, and the runtime delivers it to inform subsequent actions. (1) Principle and system. We formulate Controllable Rendering and define the interfaces among world construction, world execution, observation synthesis, and the interaction runtime. To our knowledge, this is the first implementation-independent specification of a Playable World System. (2) AI-native engine. WorldKit provides structured authoring tools and reusable charac…
  - Comment: 34 pages, 17 figures. Authors listed in reverse alphabetical order by surname
- [ ] **[Embodied Interaction Policy: A Unified Model for Full-Duplex Human-Robot Interaction](https://arxiv.org/abs/2611.27327v1)**
  <!-- aidb:id=arxiv:2611.27327v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Youqiang Gui, Yunfei Liu, Lijian Lin, Ye Zhu, Jianan Wang, Cheng Peng, Yu Li
  - Categories: cs.RO
  - Abstract: Real-time human-robot social interaction requires continuous coordination between speech and physical behavior. Existing systems often separate interaction agents from motion generation, complicating coordination as conversational states change. We propose \textbf{Embodied Interaction Policy (EIP)}, a unified streaming framework that couples an Audio-Interaction expert with a motion expert through layer-wise joint attention. This allows motion generation to directly access the evolving interaction context. A chunk-wise causal mask prevents access to future context, while a vocal token encodes speaking state and the semantic emotion of the response. We construct \textbf{Embodied Interaction…
  - Comment: 24 pages, 8 figures, 11 tables. Project page: https://youqiang-gui.github.io/EIP/
- [ ] **[SKILL.PNG: Learning Agent Skills in Pixel Space](https://arxiv.org/abs/2611.26296v2)**
  <!-- aidb:id=arxiv:2611.26296v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Maximilian Seeth, Chengzhi Martin Hu, Marie Kempkes, Paul Röttger, Leo Schwinn
  - Categories: cs.LG, cs.CV
  - Abstract: AI agents are commonly specialized for new tasks and domains using skills, i.e. natural language instructions placed in their context. However, the discrete nature of textual skills prevents continuous optimization. Gradient-based approaches such as finetuning, on the other hand, are typically model-specific, preventing skill transfer across different agents. Since many agents today are built on vision-language models (VLMs), we can address these limitations by introducing Skill$.$png: a method for obtaining skill-like image inputs whose pixels are optimized with gradient descent through the vision encoder of a frozen VLM. Image skills are compatible with any VLM, and a single image can be…
- [ ] **[AutoDFT: A Closed-Loop Multi-Agent Framework for Autonomous DFT Calculations](https://arxiv.org/abs/2605.26179v3)**
  <!-- aidb:id=arxiv:2605.26179v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-05-25
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Penghui Yang, Zhonghan Zhang, Yue Li, Xinrun Wang, Yanchen Deng, Yuhao Lu, Bijun Tang, Zheng Liu, Bo An
  - Categories: cond-mat.mtrl-sci, cs.AI, cs.CE
  - Abstract: Density functional theory (DFT) serves as the basis for computational discovery in materials science and chemistry, yet each calculation demands extensive human effort: adjusting algorithms when convergence stalls, revising plans when unexpected physics emerges, and inserting steps as intermediate results reshape the problem. Existing LLM-based agents automate only the initial planning stage, producing a full execution plan upfront and leaving all subsequent adaptation to hand-crafted rules. As a result, these workflows remain fragile, do not generalize well beyond pre-planned scenarios, and often require expert intervention when failures or unexpected intermediate results require changes t…
  - Comment: Accepted by KDD 2027
- [ ] **[From Relevance to Utility: Rubric Alignment in Yuanbao Search](https://arxiv.org/abs/2611.22503v2)**
  <!-- aidb:id=arxiv:2611.22503v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-17
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Yu Lu, Lixin Zou, Yangqi Chen, Hui Xu, Qiaolin Xia, Hao Wang, Qianwen Ma, Reed Li, Shuang Zeng, Haijin Liang, Haibo Shi
  - Categories: cs.IR
  - Abstract: Agentic search demands that a search engine move beyond per document relevance ranking to assemble document sets optimized for downstream LLM reasoning. Prior work addresses this either by improving individual pipeline stages in isolation or by applying RL based selection on top of relevance trained upstream modules, leaving the full stack unaligned to utility for reasoning. We propose rubric aligned search, a framework that unifies the traditional search pipeline under a single supervision surface. For each query, we derive a rubric from coarse to fine, specifying weighted positive criteria that the document set must satisfy and negative criteria that it must avoid. From this rubric we der…
  - Comment: 10 pages, 5 figures, 5 tables, accepted at KDD 2027
- [ ] **[$γ$-Scape: An Agent-Centric World for Mobile Embodied Intelligence](https://arxiv.org/abs/2611.27306v1)**
  <!-- aidb:id=arxiv:2611.27306v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Xiaotao Zhang, Lin Qian, Hao Zhang, Xuanrui Cui, Yuehao Huang, Yunzi Wu, Yucheng Deng, Jiankun Dong, Hujun Yin, Xinhai Li, Chenjia Bai, Xuelong Li
  - Categories: cs.AI
  - Abstract: Recent embodied agents construct and adapt robot behavior through executable programs, tool use, and interaction feedback. Studying these systems in mobile manipulation calls for physical worlds that connect agent-directed execution with its physical consequences and reusable interaction experience. We introduce $γ$-Scape, an agent-centric simulation and benchmark platform for mobile embodied intelligence. Agents compose motion tools and learned skills to carry out complete tasks that combine navigation and manipulation in a persistent physical world. BenchForge grounds structured objectives in physical task instances with instructions, reference programs, and goal evaluators, defining task…
- [ ] **[Pros4D: Modeling Evolving 4D Worlds in Latent Space for Dynamic Spatial Reasoning](https://arxiv.org/abs/2611.19803v3)**
  <!-- aidb:id=arxiv:2611.19803v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-15
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Rongxin Gao, Dongxuan Liu, Chu Li, Chengyang Ji, Jialing Huang, Runyu Chen, Kairun Wen, Chenxin Li, Jingrui Ye, Haosong Zhen, Xinghao Ding, Yue Huang, Yuzhi Huang, Xiaotong Tu, Jingyan Jiang
  - Categories: cs.CV
  - Abstract: Dynamic spatial reasoning from monocular video enables vision-language models (VLMs) to understand how 3D environments evolve over time, supporting physical world understanding and embodied intelligence. Existing efforts primarily address observed-dynamics understanding, whereas agents in dynamic environments also require future-dynamics prediction beyond the observation boundary. Moreover, external geometric processing and textual descriptions can increase inference complexity or lose information when representing continuous dynamics. These limitations motivate a shared internal state that preserves observed dynamics and remains predictive beyond the input video. Accordingly, we present Pr…
  - Comment: Project page: https://pros4d.github.io/
- [ ] **[ManipScope: A Diagnostic Benchmark for Instruction Following and Generalization in Robotic Manipulation](https://arxiv.org/abs/2611.27305v1)**
  <!-- aidb:id=arxiv:2611.27305v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jiacheng Li, Yaping Li, Congsheng Xu, Qingchen Liu, Haonan Wang, Zhijie Deng, Jiahu Qin
  - Categories: cs.RO
  - Abstract: Completing a manipulation task does not establish that a robot follows the requested goal rather than a familiar routine. ManipScope is an evaluation-only diagnostic benchmark for robotic instruction following under changed task requirements. Built on RoboTwin 2.0's simulation resources, it specifies 48 held-out scenes across six task families with explicit source-task links; policies are trained on unmodified RoboTwin 2.0 demonstrations, and no demonstrations of the scenes are provided, so success requires reusing skills under a changed request rather than fitting supplied examples. Beyond task success, ManipScope provides a chain of diagnostics in which each step tests one explanation of…
  - Comment: 49 pages, including references and appendices
- [ ] **[Bounds on the Entropy Production in Stochastic Resetting with Harmonic Traps](https://arxiv.org/abs/2605.28445v2)**
  <!-- aidb:id=arxiv:2605.28445v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-05-27
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Oded Farago
  - Categories: cond-mat.stat-mech
  - Abstract: We study the entropy production associated with stochastic resetting of a Brownian particle in an optical trap, where resetting is implemented by increasing the trap stiffness to restore a localized distribution. We interpret the dynamics as a thermodynamic cycle consisting of thermal expansion during diffusion and compression performed by an external resetting agent. Within this framework, we distinguish between the irreversibility of the resetting cycle and the additional entropy production associated with its physical implementation. We establish a lower bound based on the Kullback-Leibler (KL) divergence between forward and reversed trajectory ensembles. For a harmonic trap, this diverg…
  - Comment: 9 pages. 2 figures. Substantially revised version with a new title and a fundamentally different theoretical approach to entropy production in stochastic resetting
- [ ] **[HookEvo: A Framework for Coordinated Plugin Evolution on Hook-Enabled Agent Runtimes](https://arxiv.org/abs/2611.27294v1)**
  <!-- aidb:id=arxiv:2611.27294v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Shengze Huang, Yanyu Mao, Xiaofei Yu, Baoshen Guo, Xiaorui Wang, Zhiwen Wu, Sheng Wu, Fukang Wen, Chengxu Wu, Linhao Li, Kailai Sun, Baotong Mi
  - Categories: cs.AI, cs.SE
  - Abstract: Repairing failures in tool-using agents can require coordinated changes to how the harness interprets tool receipts, assembles context, and checks actions. We introduce HookEvo, a framework that uses an existing agent runtime's lifecycle hooks to evolve task-specific harnesses. We instantiate HookEvo on DeepSeek Harness. In each round, a separate improver diagnoses failures from execution traces and proposes a candidate. HookEvo evaluates the candidate against the current harness on matched tasks and carries the retained version into the next round. A single candidate can jointly edit executable plugin handlers and the state they share within a task, allowing a tool receipt to inform contex…
- [ ] **[Belief-State Management Meets Rubric Rewards for Agentic Forecasting](https://arxiv.org/abs/2611.27286v1)**
  <!-- aidb:id=arxiv:2611.27286v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jingyi Chai, Yun Liao, Hao Lu, Kemeng Zhang, Bingyang Zheng, Yujie Ge, Xiangrui Liu, Linfeng Zhang, Siheng Chen
  - Categories: cs.AI, cs.CL
  - Abstract: Current large language model (LLM) agents still struggle to forecast real-world events. This stems from two primary limitations: i) standard ReAct harness accumulates reasoning and evidence within one growing context, and ii) outcome-based rewards in forecasting lead to a slow and noisy signal that cannot distinguish sound reasoning from lucky guesses. To address these, we introduce a forecasting training framework including harness design and post-training. For the harness side, we propose Proactive Belief-State Management (PBM), equipping agents with a fold tool to compress lengthy context into compact belief states and reset the context for subsequent exploration. For the training side,…
- [ ] **[SIR-Agent: Skill-Augmented Image Restoration Agent with Recursive Self-Improvement](https://arxiv.org/abs/2611.27285v1)**
  <!-- aidb:id=arxiv:2611.27285v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yijian Wang, Qingsen Yan, Weiyu Zhou, Mingde Zhang, Axi Niu, Haokui Zhang, Jiantao Zhou
  - Categories: cs.CV
  - Abstract: Agents for Image Restoration (IR) aim to leverage Multimodal Large Language Models (MLLMs) to autonomously perceive image degradation and invoke IR tools. However, existing IR agents typically rely on fine-tuning MLLM parameters to adapt to new IR tasks, leading to catastrophic forgetting of IR knowledge. To address this limitation, we propose a skill-augmented IR agent, dubbed SIR-Agent, that maintains IR knowledge in a scalable skill library and uses Recursive Self-Improvement (RSI) to facilitate efficient skill-library evolution. Specifically, we design a Chain Feedback-driven Skill Revision (CFSR) to evolve the skill library. The CFSR analyzes restoration chains to identify and revise w…
- [ ] **[MemT-1.0: Towards Memory-Native Evolution](https://arxiv.org/abs/2610.26825v4)**
  <!-- aidb:id=arxiv:2610.26825v4 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Zhiyu Li, Zeyu Zhang, Linyun Liu, Yiwei Bu, Chenyang Xi, Xichong Zhang, Yi Yu, Yu Yu, Zhichen Liu, Yuxiao Yi, Chunyu Li, Haoran Liu, Zhenkai Ding, Le Zhou, Juncheng Zhang, Boyu Chen, Zehao Lin, Guorui Li, Renyu Fu, Ji Li, Youyang Xia, Jiajun Shen, Harvey Li, Jinsong Zhou, Helan Hu, Tong Shen, Tianx…
  - Categories: cs.CL, cs.LG
  - Abstract: Memory-native evolution requires making memory an intrinsic capability of foundation models, enabling them to continuously accumulate and utilize information. To this end, we introduce MemT-1.0, a new architecture of memory foundation models that internalize memory as part of model computation. Building on Metis, MemT-1.0 employs Gated DeltaNet-2 with a stable token-level memory update mechanism within each turn. We further introduce Mixture-of-Storage to scale native memory capacity. Following a deliberate backbone preparation, we develop a two-stage training pipeline consisting of continued pre-training and post-training, supported by 34B tokens of training data and efficient training and…
  - Comment: 66 pages, 14 figures, 16 tables
- [ ] **[Training Reasoning Models in Simulation to Natively Use Real Robots](https://arxiv.org/abs/2611.18562v2)**
  <!-- aidb:id=arxiv:2611.18562v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-13
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Jiaming Tang, Zhuoyang Zhang, Junxian Guo, Fangzhou Zhao, Yilong Zhao, Zekai Li, Xingyang Li, Yuyang Zhao, Song Bian, Zhijian Liu, Song Han
  - Categories: cs.RO, cs.LG
  - Abstract: Robot-use agents (RUAs) have emerged as a promising approach to general-purpose robot control. However, strong performance has so far been achieved only by frontier proprietary models such as GPT-6 Astra and Claude Fable 5.2, whereas open-weight models remain substantially less capable. We show that an open-weight 27B reasoning model can be trained to use real robots natively through reinforcement learning, entirely in simulation and without demonstrations. Like a computer-use agent (CUA), the model observes the environment, reasons in a chain of thought, and generates the next end-effector pose, without any harness. We build a Post-training Engine for Agentic Robotics (PEAR) and use it to…
- [ ] **[Do Companies Deliver on Their IPO Claims?](https://arxiv.org/abs/2611.27273v1)**
  <!-- aidb:id=arxiv:2611.27273v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Vidhyakshaya Kannan, Shiv Banafar, Michael Galarnyk, Sagnik Nandi, Soumeya Kannan, Shauray Arora, Abanoub Abdelmalak, Sudheer Chava
  - Categories: cs.CL
  - Abstract: Initial public offering (IPO) filings describe what a company does and what it intends to become. Yet whether individual forward-looking claims are subsequently realized is difficult to assess. We introduce Vision Follow-Through (VFT), a benchmark and agentic pipeline that separates claim extraction, category assignment, verifiability, and evidence-grounded follow-through assessment. \vftclaims{} contains 5,066 human-annotated claim spans from 50 IPO filings, while \vftverify{} adds verifiability tiers, follow-through outcomes, and cited later evidence for 1,000 claims. Across language models, classifying human-annotated claims is substantially easier than extracting claims from full filing…
- [ ] **[Can Coding Agents Write and Transpile Unit Tests](https://arxiv.org/abs/2611.21797v2)**
  <!-- aidb:id=arxiv:2611.21797v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-16
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Gil Pasternak, AJ Langley, Tom Yotam, Ellie Kitanidis
  - Categories: cs.SE, cs.AI
  - Abstract: Coding assistants built on Large Language Models (LLMs) have become a staple of modern software development, increasingly trusted to execute workflows and modernize code end-to-end. Much of this trust rests on passing tests, which are often written by the coding agents themselves. In this work, we examine the ability of these agents to both write reliable tests and translate them between programming languages. We benchmark three popular coding agents, each evaluated with a native frontier model and high reasoning effort. Verifying across a broad suite of metrics, we find that coding agents far exceed human written suites on traditional measures of coverage. This advantage, however, is uneve…
- [ ] **[Why Does CLAUDE.md Keep Growing? Catastrophic Remembering in Agentic Coding](https://arxiv.org/abs/2608.11095v2)**
  <!-- aidb:id=arxiv:2608.11095v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-11
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Kushal Chakrabarti
  - Categories: cs.AI, cs.LG, cs.SE
  - Abstract: Agentic prompts like CLAUDE.md grow without bound in real repositories, stopping only when history ends or someone rewrites the file wholesale. We trace this to imperfect recall: appending an instruction is always cheap, but once an instruction's latent reasoning is gone, deleting it without risking a regression costs O(2^|D|) in a prompt of |D| instructions. Successive edits destroy that latent reasoning, additions outrun deletions and prompts grow until agents become non-functional -- catastrophic remembering. First, we characterize this phenomenon across 247,694 instruction lifetimes in 1,867 repositories: agentic prompts grow nearly monotonically, more than tripling over their lifetime…
- [ ] **[Co-Design Gym: A Unified Benchmark for Embodiment-Policy Co-optimization](https://arxiv.org/abs/2610.02366v2)**
  <!-- aidb:id=arxiv:2610.02366v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-01
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Aviraj Newatia, Yordan Tsvetkov, Leonard Pleiss, Andrew Spielberg, Rika Antonova
  - Categories: cs.LG, cs.RO
  - Abstract: Finding an optimal behaviour policy within a given environment is a widely studied problem in domains as diverse as games, robotics, energy infrastructure, communication networks, and multi-agent systems. Numerous benchmarks have been developed to support such research, but the vast majority assume that the agent's embodiment (design) is fixed, focusing instead on policy learning alone. Lifting this assumption gives rise to a broader class of problems in which optimizing embodiment and policy separately is highly suboptimal. An agent's embodiment strongly shapes which control policies can be discovered, while the optimal embodiment is in turn defined by the policies it admits. To help the r…
  - Comment: Aviraj Newatia and Yordan Tsvetkov contributed equally
- [ ] **[MSRyzen: An Agentic Platform for Unified Proteomics Analysis and Evidence-Centric Visualization](https://arxiv.org/abs/2611.27246v1)**
  <!-- aidb:id=arxiv:2611.27246v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yucheng Liao, Jubao Cheng, Zexu Xiao, Tao Yi, Jiaxiang Ding, Weijie Zhang
  - Categories: cs.CE, cs.SE, stat.AP
  - Abstract: Mass spectrometry (MS)-based proteomics is essential for comprehensive protein characterization, yet it relies on multistep computational workflows that typically demand tedious manual parameter tuning and complex software integration. Here, we present MSRyzen, an agent-driven framework that provides automated parameter optimization and extensible tool integration across bottom-up and top-down proteomics workflows. MSRyzen translates natural-language prompts into directed acyclic workflow graphs, optimizes analytical parameters guided by quantitative metrics and user-defined objectives, and incorporates new third-party software through standardized callable interfaces. Across four public to…
- [ ] **[Generalizing Test-time Compute-optimal Scaling as an Optimizable Graph](https://arxiv.org/abs/2511.00086v2)**
  <!-- aidb:id=arxiv:2511.00086v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-10-29
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Fali Wang, Jihai Chen, Shuhua Yang, Runxue Bao, Tianxiang Zhao, Zhiwei Zhang, Xianfeng Tang, Hui Liu, Qi He, Suhang Wang
  - Categories: cs.LG, cs.AI, cs.CL
  - Abstract: Test-Time Scaling (TTS) improves large language models (LLMs) by allocating additional computation during inference, typically through parallel, sequential, or hybrid scaling. However, prior studies often assume fixed collaboration architectures (e.g., topologies) and single-model usage, overlooking that optimal architectures and model combinations can vary across tasks. Therefore, we study the novel problem of searching for compute-optimal model combinations and architectures in TTS under a fixed budget. We formalize it as a multi-LLM collaboration graph, where nodes encode roles and LLM model assignments, and edges capture information flow. This problem is challenging because (i) the comb…
  - Comment: Accepted by NeurIPS 2026
- [ ] **[FUSE: A Modular Framework for Evaluating Dangerous Capabilities of LLMs](https://arxiv.org/abs/2609.02168v2)**
  <!-- aidb:id=arxiv:2609.02168v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-02
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zhengyi Jin, Ru Zhang, Xinbo Liu, Xiao Chen, Jiaxuan Lin, Jia Huang, Jianyi Liu, Zhen Yang
  - Categories: cs.AI
  - Abstract: Dangerous capabilities of large language models (LLMs) cannot yet be compared across models: knowledge, refusal, and harm benchmarks each cover one step of a misuse path, on different models, protocols, and scales, so regulators cannot tell which model poses greater risk. We present FUSE, a modular framework that defines dangerous capability as a model's ability to advance a black-box adversary along a misuse path, and measures three stages of that path under one protocol: hazardous knowledge, estimated by item response theory; defense under multi-turn adversarial induction by a red-team agent; and the actionability of content produced once the model complies (harm). The stages form a fixed…
- [ ] **[u4lib: An AI-Ready Computational Framework for U(4) Symmetry Algebra, Wigner Coupling, and Racah Recoupling Coefficients](https://arxiv.org/abs/2611.27235v1)**
  <!-- aidb:id=arxiv:2611.27235v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Phong Dang, Daniel Langr, Tomas Dytrych, Michela Negro
  - Categories: nucl-th, physics.comp-ph
  - Abstract: Wigner's supermultiplet symmetry treats nucleon spin and isospin within a common U(4)/SU(4) description. The C++ library u4lib supplies the coupling coefficients and algebraic operations needed for calculations in this scheme. Users can construct irreducible representations (irreps), obtain dimensions and Casimir invariants, conjugate states, enumerate the canonical Gelfand-Tsetlin and physical $\mathrm{SU_S(2)}\otimes\mathrm{SU_T(2)}$ bases with inner multiplicities, and decompose tensor products. Matrix-element routines cover the canonical U(4) generators and the physical spin $\mathbf{S}$, isospin $\mathbf{T}$, and Gamow-Teller-type tensor $\mathbf{U}$. Wigner coupling and Racah recoupli…
  - Comment: 16 pages, 1 figure, 3 tables. Source code available at https://github.com/Deep-SANE/u4lib. Companion to the u3lib manual, arXiv:2611.26558
- [ ] **[Bel: Step-Level Policy Improvement of Visual Agents Without Training](https://arxiv.org/abs/2611.27222v1)**
  <!-- aidb:id=arxiv:2611.27222v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jiajun Fan, Ziwen Wang, Zhaoyu Zhu, Changyi Yang, Neil He, Chaoran Cheng, Ge Liu
  - Categories: cs.AI
  - Abstract: A visual agent acts on what it sees: it taps and types on a screen, or points on a camera image to show a robot where to act. One wrong step can fail its task, yet the right action is often among its own samples, passed over by its greedy decode. Choosing it is a visual judgment, since an action is best judged where it acts, not by its text or coordinates alone: as text, a tap is two numbers; drawn on the screen, it is the Post button of an empty draft. We find that this is decisive: given the screenshot and a tap's coordinates, a decision model chooses among GUI-R1-3B's samples significantly worse on average than when the tap is drawn where it lands. Bel turns this finding into a method th…
- [ ] **[NavTTT: Adaptive Parametric Memory via Hierarchical Test-Time Training for Vision-and-Language Navigation](https://arxiv.org/abs/2611.27219v1)**
  <!-- aidb:id=arxiv:2611.27219v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Xiaoyu Luo, Chengxing Lin, Jiaxin Huang, Jiale Liu, Jingyu Guo, Sirui Chen, Aolin Li, Shaoli Huang, Cheng-zhong Xu, Hui Kong
  - Categories: cs.RO, cs.AI
  - Abstract: Vision-and-language navigation (VLN) demands that agents accumulate and reason over streaming visual observations throughout long navigation episodes. Existing approaches struggle to maintain long-term history, constrained by the finite context capacity of transformer architectures. To solve the problem, fast-weight test-time training (TTT) provides a mechanism for encoding streaming observations into an evolving parameter state. However, existing TTT does not distinguish informative observations from repetitive visual content, allowing redundant tokens to interfere with the retention of information needed for subsequent decisions. We propose Navigation-Conditioned Test-Time Training (NavTT…
  - Comment: Project page: https://gamepeopleplay.github.io/NavTTT/
- [ ] **[Correct Precedents Induce Policy Violations in On-Device LLM Agents](https://arxiv.org/abs/2611.27216v1)**
  <!-- aidb:id=arxiv:2611.27216v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Chong Tian, Yu Wang, Steve Liu, Qirong Ho, Xiuying Chen
  - Categories: cs.CL, cs.AI, cs.CR
  - Abstract: Local-cloud agent systems pair a cloud model with a small on-device agent that acts on private data, often as the last check before an irreversible action. We identify, for the first time, a failure in which such an agent is led into a violation by its own correct decisions within a session. After it correctly releases an item whose restriction was lifted, it becomes more likely to release the next item that is still restricted. Because the trigger is a correct decision, a history with no faulty step can still end in a violation. We call this failure correct-precedent generalization and find it in 13 open-weight models from nine developers. A single correct precedent can cut the safe rate o…
  - Comment: 22 pages, 9 figures, 22 tables
- [ ] **[Exploration Structure in LLM Agents for Multi-File Change Localization](https://arxiv.org/abs/2606.11976v2)**
  <!-- aidb:id=arxiv:2606.11976v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-10
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Akeela Darryl Fattha, Kia Ying Chua, Lingxiao Jiang, Laura Wynter
  - Categories: cs.SE, cs.AI
  - Abstract: Fixing an issue starts with finding the files to change, and most benchmark issues touch several. LLM agents for this task increasingly add structure, such as specialized tools, multiple agents, or code summaries. We ask which of this structure matters when the model is small. We build a coordinator agent with repository tools that limit their output and a reusable registry of subsystem-scoped domain agents. We compare six configurations, each adding structure to the previous one. They are the model alone, a single agent with a Python REPL, a coordinator with only the REPL, the previous structure plus repository tools, then plus the registry map, and finally plus consultation of the domain…
- [ ] **[Explicit Style Extraction for Personalized Long-Form Text Generation](https://arxiv.org/abs/2611.27211v1)**
  <!-- aidb:id=arxiv:2611.27211v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jenitha Reddy Patel, Sameeksha Kini, Amulya Rayasam, Anisa Dye, Abhinav Sharma, Sai Karthik Navuluru, Bo Ni, Li Li, Junda Wu, Tong Yu, Nedim Lipka, Xiaolei Huang, Tyler Derr, Yue Zhao, Zhengzhong Tu, Yu Wang, Hongjie Chen, Thien Huu Nguyen, Nesreen K. Ahmed, Franck Dernoncourt, Ryan A. Rossi
  - Categories: cs.CL, cs.AI, cs.IR
  - Abstract: Personalized long-form generation asks a language model to write new text the way a specific user would. The standard recipe, retrieval-augmented generation, places a few of the user's past texts in the prompt but leaves the model to decide what to take from them. We introduce StylePrism, a taxonomy of 28 stylistic aspects in seven categories, and SP-Refine, an inference-time method that makes style extraction an explicit step: the model first fills StylePrism with the user's patterns, quoted evidence, and habits to avoid, then drafts from the user's samples and revises the draft twice against this profile, guided by its own style scores. On the three long-form tasks of LongLaMP with three…
  - Comment: 21 pages, 8 figures, 11 tables
- [ ] **[The Rise of Agents and the Human Labor Market](https://arxiv.org/abs/2611.27210v1)**
  <!-- aidb:id=arxiv:2611.27210v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Nicola Borri, Anton Cheremukhin, Yukun Liu, Aleh Tsyvinski
  - Categories: econ.GN, q-fin.GN
  - Abstract: We provide the first economy-wide and cross-AI model evidence on the effects of agentic AI on labor demand. We combine proprietary OpenRouter data covering about two quadrillion tokens of realized AI consumption (2 percent of global AI token consumption) across more than 400 AI models, including 1.1 quadrillion agentic tokens, with the full text of 34.8 million U.S. job postings for public firms from Lightcast. We compute our measure of firm-level exposure to aggregate agentic AI consumption (agentic beta) using the comovement of U.S. public firms' stock returns with realized weekly aggregate agentic AI token consumption. We find that a one-standard-deviation increase in a firm's exposure t…
- [ ] **[RoughCut-Bench: A Benchmark for Automatic Video Rough-Cut with Large Vision-Language Models](https://arxiv.org/abs/2611.24098v2)**
  <!-- aidb:id=arxiv:2611.24098v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-18
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Ruisi Zhao, You Li, Sihan Chen, Aosong Cheng, Chixiang Ma, Sen Pei, Zhen Yang, Hehe Fan, Dongliang He, Yi Yang
  - Categories: cs.CV
  - Abstract: Video rough-cut is a core stage in media production workflows, organizing raw media materials into an initial video cut. Despite recent advances in large vision-language models (LVLMs) for video-related tasks, automatic rough-cut remains underexplored, without a comprehensive benchmark for evaluation or mature workflows for producing executable cut plans. To address the evaluation gap, we introduce RoughCut-Bench, which covers two practical settings: (1) a visually driven setting over video cases, covering highlight detection and selection, source-video ordering, and adherence to user requirements when provided; and (2) a speech-driven setting over automatic speech recognition (ASR) transcr…
  - Comment: Accepted to KDD 2027. Project page is at https://whalesong-zrs.github.io/RoughCut-Bench-Project-Page. This revision clarifies the speech-driven evaluation protocol, including count aggregation across ten runs, and corrects numerical errors in the result tables
- [ ] **[EDAGoat: An EDA-Aware Agent for Project-Level GPU Optimization](https://arxiv.org/abs/2611.27196v1)**
  <!-- aidb:id=arxiv:2611.27196v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Chengxi Li, Liang Xiao, Yutao Wang, Wenhao Lin, Xinzhuang Xiong, Han Zhao, Evangeline Young
  - Categories: cs.AI, cs.SE
  - Abstract: GPU acceleration has transformed electronic design automation (EDA), yet further improving expert-engineered GPU tools still demands substantial manual effort. Automating this work calls for coding agents that can trace bottlenecks across host and device code while preserving correctness and design quality. We introduce EDAGoat, to our knowledge the first EDA-aware GPU optimization agent for this task. Its optimization enhancement (OE) mode guides edits with four cross-project GPU optimization patterns. Its mandatory validation (MV) mode requires the agent to test the edited program against the EDA constraints its changes could affect. Our benchmark covers five GPU EDA projects across four…
  - Comment: 7 pages, 2 figures, 3 tables
- [ ] **[See, Remember, Explore: A Benchmark and Baselines for Streaming Spatial Reasoning](https://arxiv.org/abs/2603.23864v2)**
  <!-- aidb:id=arxiv:2603.23864v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-03-25
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yuxi Wei, Wei Huang, Qirui Chen, Lu Hou, Xiaojuan Qi
  - Categories: cs.CV
  - Abstract: Spatial understanding is fundamental for embodied agents, yet most spatial VLMs and benchmarks remain offline-evaluating post-hoc QA over pre-recorded inputs and overlooking two crucial deployment-critical requirements: long-horizon streaming inference and active perception when the current view is insufficient. To address this gap, we introduce S3-Bench, a benchmark suite for streaming spatial question answering with active exploration, where queries are temporally grounded to specific timestamps and must be answered using only observations available up to that moment. S3-Bench adopts a dual-domain design, combining a scalable simulator with controllable trajectories and exploration action…
  - Comment: Superseded by arXiv:2610.17640 (MemAct), a substantially revised and extended version of this work. The two entries describe the same work, not independent contributions
- [ ] **[RegimeCouncil: Paired-Evidence Routing For Memory Conflict Governance In LLM Agents](https://arxiv.org/abs/2611.22113v2)**
  <!-- aidb:id=arxiv:2611.22113v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-17
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Qingcan Kang, Mingyang Liu, Shixiong Kai, Tao Zhong, Mingxuan Yuan
  - Categories: cs.AI
  - Abstract: Alongside memory storage and retrieval, a fundamental challenge in long-term LLM agent systems is how the agent should act when stored memories conflict with an evolving world. Facts often go stale without explicit deletion, so the conflict surfaces before the store is refreshed: delayed feedback shows that acting on one outdated record hurt, but not whether suppression should stay on that fact (a local policy) or extend to other stored facts (a global policy). Existing systems hard-code one of these scopes at design time. We formulate this online choice, under hidden validity and delayed feedback, as memory conflict governance, and propose RegimeCouncil, a lightweight router that keeps bot…
- [ ] **[Agentic programs: an emerging form of scientific software in computational materials science](https://arxiv.org/abs/2609.00795v2)**
  <!-- aidb:id=arxiv:2609.00795v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-01
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yunsung Lim, Haekwan Jeon, Jaesun Kim, Jisu Kim, Seungwu Han
  - Categories: cond-mat.mtrl-sci, cs.AI
  - Abstract: Computational materials science has traditionally delegated algorithmic tasks to computers while leaving scientific judgments to humans. In this Perspective, we argue that agent harnesses built on large language models (LLMs) enable an emerging form of scientific software, agentic programs, integrating deterministic algorithms with bounded LLM-based judgment, task-specific verification, episodic maturation, and complete delegation. We illustrate these characteristics through DeMARS, which constructs atomistic models from experimentally measured disordered crystal structures.
  - Comment: 10 pages, 4 figures, Supplementary information included as ancillary file
- [ ] **[Tripwire: Robot Agents that Program Their Own Interrupts under Human Disturbance](https://arxiv.org/abs/2611.27182v1)**
  <!-- aidb:id=arxiv:2611.27182v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Sunli Chen, Yun Zong, Qinhong Zhou, Xiaowen Qiu, Jiaben Chen, Zeyuan Yang, Chuang Gan
  - Categories: cs.RO, cs.CV
  - Abstract: Agent harnesses are turn-based: the agent acts, waits for the result, then reasons. When the action invokes a pretrained robot policy, such as a vision-language-action (VLA) or world action model (WAM), the policy may react continuously to observations, but the agent cannot revisit its decision until the call returns. Meanwhile, a person may step into the robot's path or move the object it is about to grasp. Invoking the agent more often narrows this blind interval, but a reasoning model takes seconds per decision and most control steps need no new one. We propose TRIP, a training-free, event-driven harness in which the agent programs its own interrupts. With each call, the agent writes a t…
- [ ] **["More Than You Expect!": Leakage-Abuse Attacks on Encrypted Vector Search](https://arxiv.org/abs/2611.27174v1)**
  <!-- aidb:id=arxiv:2611.27174v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yang Zhang, Ruiqi He, Xiaoqian Sun, Siyi Lv, Zheli Liu
  - Categories: cs.CR
  - Abstract: Vector databases support semantic search and retrieval-augmented generation, but embeddings, queries, and record labels may contain sensitive information. Although encrypted vector search protects these contents, some schemes expose records retrieved together across queries. We identify semantic neighborhood leakage, whereby co-retrieval relationships derived from access patterns reveal semantic categories of encrypted records and queries. We present SAGE (Semantic Access-pattern Graph Exploitation), a passive, persistent leakage-abuse attack that infers record labels and query categories from access patterns. SAGE builds a weighted co-retrieval graph and offers two variants requiring diffe…
  - Comment: 18 pages, 7 figures
- [ ] **[Mem-X: A Memory-Dependent Cross-Episode Benchmark for Vision-and-Language Navigation](https://arxiv.org/abs/2611.27166v1)**
  <!-- aidb:id=arxiv:2611.27166v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zhikang Shi, Yuk Tung Samuel Fang, Hongyu Ding, Zixuan Chen, Yujin Wang, Junhui Guo, You Wu, Jieqi Shi, Jing Huo, Yang Gao
  - Categories: cs.CV, cs.RO
  - Abstract: Long-term memory enables embodied agents to reuse past observations across tasks. However, existing cross-episode vision-and-language navigation (VLN) benchmarks often leave it unclear whether successful navigation relies on historical memory or current exploration. We introduce Mem-X, a benchmark designed to evaluate memory-dependent cross-episode VLN. Mem-X organizes episodes into sessions in which subsequent instructions refer to objects or routes encountered in earlier episodes. Its three levels evaluate historical-object recall, in-memory localization and episodic indexing, and off-memory relocalization and historical-route reproduction. For the latter two levels, agents receive episod…
  - Comment: 9 pages, 3 figures. Submitted to IEEE International Conference on Robotics and Automation (ICRA 2027)
- [ ] **[From Acting to Learning: Experience Selection toward Continually Learning Agents](https://arxiv.org/abs/2611.27159v1)**
  <!-- aidb:id=arxiv:2611.27159v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yaoyuan Yan, Haoxiang Jie, Zhiyou Heng, Kailin Wang, Yumiao Li, Lifeng Liu, Anwan Yan
  - Categories: cs.AI, cs.RO
  - Abstract: Successful agent interactions provide training data, but success alone does not determine which records a student should learn from. We examine experience selection for a 4B language agent as a component of continual agent learning. Nine selectors are compared across two fixed experience pools, eight initialization seeds, and two sampling seeds, yielding 288 trained students. Each student is evaluated on 128 development task groups with a common executor. With equal global selection freedom, 256 distinct contents, and 768 training presentations, optimizer-aware gradient selection reaches 81.45\% and 73.19\% success in the two pools. Its gains over global random selection are 8.25 and 5.96 p…
- [ ] **[Co-Evolving Behavioral Agents and Detectors for Adaptive Information Operations](https://arxiv.org/abs/2611.27156v1)**
  <!-- aidb:id=arxiv:2611.27156v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Lin Tian, Marian-Andrei Rizoiu
  - Categories: cs.CL, cs.AI
  - Abstract: Detectors of state-sponsored information operations (IOs) are trained on campaigns that platforms have already taken down. They lose much of their accuracy on an actor they have not seen, even though no operator in the archived data is trying to avoid them. A real operator wants two things, to reach an audience and to avoid being caught. We present IO-AI, a framework that gives simulated agents these two capabilities, engagement and evasion, and tests what each one does to detection. The agents are built from the posting behavior of real campaigns and choose the emotion, type, and timing of each post. An agent and a detector then train against each other in turn. We rank the trained agents…
  - Comment: 12 pages, 5 figures, 7 tables
- [ ] **[ScrapMem: A Bio-Inspired Framework for On-Device Personalized Agent Memory via Optical Forgetting](https://arxiv.org/abs/2605.03804v3)**
  <!-- aidb:id=arxiv:2605.03804v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-05-05
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jiale Chang, Yuxiang Ren
  - Categories: cs.AI
  - Abstract: Long-term personalized memory for LLM agents is challenging on resource-limited edge devices because multimodal histories grow continually and are costly to store. To address this challenge, we propose ScrapMem, a bio-inspired framework that consolidates each day's heterogeneous records into a unified "Scrapbook Page." ScrapMem introduces Optical Forgetting, an optical compression mechanism that progressively reduces the resolution and JPEG quality of older pages, lowering storage costs while keeping recent evidence at higher fidelity. To preserve semantic consistency and support structured retrieval, we construct an Episodic Memory Graph (EM-Graph) that organizes semantic nodes into causal…
  - Comment: 12 pages. Accepted to KDD 2027 (Research Track). Code: https://github.com/changjiale444/ScrapMem
- [ ] **[Mathematical modeling to study combination strategies for neural stem cell therapy in glioblastoma](https://arxiv.org/abs/2611.01374v2)**
  <!-- aidb:id=arxiv:2611.01374v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-01
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Ashley Harrison, Austin Hansen, Anthony E. Bishay, Greg Grigoryan, Vikram Adhikarla, Russell C. Rockne, Margarita Gutova, Heyrim Cho
  - Categories: q-bio.OT
  - Abstract: Neural stem cells (NSCs) are a promising treatment platform due to their ability to cross the restrictive blood-brain barrier and migrate toward damaged regions of the brain. These properties can be leveraged to target brain tumors, as NSCs can infiltrate tumor lesions and deliver therapeutic agents such as drugs, oncolytic viruses, and genetic materials. Despite the advantages of NSCs, translational challenges remain, including patient-specific chemotactic signaling and immune responses, variability in migration and localization at tumor sites, and optimization of delivery strategies. In this work, we focus on intranasal delivery of NSCs and combination strategies for the treatment of brai…
  - Comment: 20 pages, 6 figures
- [ ] **[AscendGYM: A Cost-Aware Kernel Optimization Benchmark for Real-World Workloads on Ascend NPUs](https://arxiv.org/abs/2611.17621v2)**
  <!-- aidb:id=arxiv:2611.17621v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-13
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: SLAI AI Training Platform Team, Bingwei Zhang, Jing Li, Amir Abdullin, Sihang Chen, Xin Chen, Liangjun Feng, Yingmeng Gao, Tao Guo, Junjie Huang, Dongfang Li, Zhanglian Lin, Jiajun Liu, Zekun Liu, Zhengxuan Lu, Xiaodong Luo, Jian Meng, Ivan Nosov, Linyuan Qiu, Weijian Sun, Wanrui Yan, Zhicheng Zhou…
  - Categories: cs.AI, cs.DC, cs.LG
  - Abstract: Kernel optimization is essential for efficient large language model (LLM) training and inference on Ascend NPUs. Existing Ascend kernel benchmarks primarily focus on kernel generation, with less emphasis on the ability of agents to optimize existing implementations under input configurations drawn from real workloads. To address this requirement, we introduce AscendGYM, a benchmark whose initial suite comprises 48 kernels across three difficulty levels. Each kernel is paired with test cases whose data types and tensor shapes are collected from real-world training and inference tasks. Consequently, performance improvements on AscendGYM map directly to the corresponding workloads. In terms of…
  - Comment: 20 pages, 12 figures, 2 tables. Technical Report. Code available at https://github.com/SLAI-AITP/AscendGYM
- [ ] **[Do Senior Agents Do Their Job? Measuring Role Integrity in How LLM Agents Use Subordinate Material](https://arxiv.org/abs/2611.27139v1)**
  <!-- aidb:id=arxiv:2611.27139v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jinxiang Xie, Xinyi Zhang, Changjiang Jiang, Kexu Liu, Qi Yang, Yuxin Su
  - Categories: cs.CL, cs.AI
  - Abstract: Multi-agent LLM systems increasingly divide long tasks among subagents whose reports a senior agent turns into the final answer. Such a division of labor pays off only if each agent, and above all the senior agent, carries out the duties of its role. Current evaluations, however, mostly score the final answer, and a fluent, well-cited answer cannot show whether the senior agent weighed its subagents' reports or merely aggregated them. To assess whether a senior agent meets its assigned responsibilities, we define role integrity as the preservation of an agent's functional responsibilities when it acts on its subordinates' material. To measure it, we introduce RI-Bench, a behavioral benchmar…
- [ ] **[Double counting in LLM evidence fusion: exact posteriors separate rule compliance from posterior gain](https://arxiv.org/abs/2611.27138v1)**
  <!-- aidb:id=arxiv:2611.27138v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Tengfei Shao, Asma Rezaei, Ali Reza Kamali
  - Categories: cs.AI, cs.CL
  - Abstract: Language models fuse reports in retrieval, multi-agent consensus and agent memory, where treating shared-source reports as independent can double count evidence. A common remedy is an instruction to count each source once. Its value depends on the receiver's raw baseline. Pricing it needs an exact reference. We build the graded-dependence exact reference: binary worlds with single-report reliability 0.65 and four dependence levels, whose disclosed parameters give every world an exact posterior and every rule a target risk. The paired gain protocol scores raw and instructed answers of four configurations on 2,976 worlds. Agreement and gain separate in both directions. At $δ$ = 0, claude-opus…
  - Comment: 57 pages (30 main text, 27 supplementary material), 4 figures
- [ ] **[LingSante MedGuard Technical Report](https://arxiv.org/abs/2611.25509v2)**
  <!-- aidb:id=arxiv:2611.25509v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: LingSante MedGuard Team
  - Categories: cs.CR
  - Abstract: As medical AI is increasingly used for patient consultation and clinical decision support, identifying harmful, non-compliant, or ethically problematic responses is essential for responsible deployment. Assessing these risks requires checking clinical claims against relevant evidence, verifying calculations, and applying medical requirements under their intended conditions. We introduce LingSante MedGuard, a capability-enhanced guardrail that integrates supervision from a medical guardrail teacher model and six specialized medical capability experts into a unified model. The guardrail teacher supervises risk decisions and explanations across medical safety, compliance, and ethics, while the…
  - Comment: 52 pages, 15 figures. Dataset: https://github.com/inclusionAI/LingSante-MedGuard
- [ ] **[Towards Embodied Air-Ground Cooperative Object Search: Benchmark, Dataset and Agentic Method](https://arxiv.org/abs/2609.08402v3)**
  <!-- aidb:id=arxiv:2609.08402v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-08
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Boao Yu, Zimo Chen, Junreng Rao, Yue Hu, Zhengqiu Zhu, Yong Zhao, Jianzhe Gao, Pengfei Zhu, Rusheng Ju
  - Categories: cs.CV, cs.AI
  - Abstract: Urban object search, locating a specific object from a single reference image without route or direction instructions and confirming the instance up close, is a fundamental capability for embodied agents. Existing urban embodied benchmarks evaluate one segment of this chain: navigation ends at a coordinate, and detection and question answering stop at an answer. We present AGOS-Bench, the first benchmark for urban cooperative object search by an air-ground team, integrating aerial discovery and ground-level instance verification in one closed loop. Nine metrics assess search, cooperation, and verification, and they distinguish "found but unconfirmed" from "never found". AGOS-Dataset instant…
  - Comment: 22 pages, 6 figures, 20 tables; includes appendices. v3: corrected author list and abstract metadata; manuscript content unchanged from v2
- [ ] **[No-Box Vulnerability Analysis: Description-only Detection of Indirect Prompt Injection Vulnerabilities in MCP Servers](https://arxiv.org/abs/2609.10854v3)**
  <!-- aidb:id=arxiv:2609.10854v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-09
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zehua Zhang, Jie Hu, Pratham Hegde, Aditya Maheshbhai Gabani, Souradip Nath, Yibo Liu, Siyu Liu, Hongkai Chen, Hulin Wang, Zhuoer Lyu, Chang Zhu, Divij Handa, Yan Shoshitaishvili, Tiffany Bao, Ruoyu Wang, Adam Doupé
  - Categories: cs.CR, cs.AI
  - Abstract: When auditing remotely hosted services or commercially gated software for vulnerabilities, third-party analysts may lack both direct system access and the ability to interact with the running system. We call this a no-box setting, in which analysts have access only to functionality metadata that may describe the intended inputs, behaviors, and outputs of the system. Such descriptions constrain the possible implementations of a system, enabling analysts to hypothesize potential implementations and their underlying vulnerabilities. These hypotheses can subsequently guide validation when system access becomes available. To demonstrate the feasibility of conducting vulnerability analysis under…
- [ ] **[OpenRing: Deadlock-Free Execution of Any Planner on AGV Floors with One-Way Lanes](https://arxiv.org/abs/2611.27127v1)**
  <!-- aidb:id=arxiv:2611.27127v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zhihao Lin, Anh-Tu Nguyen, Hui Zhang, Yoshinobu Kawahara
  - Categories: cs.RO, cs.MA
  - Abstract: Lifelong multi-agent path finding replans routes for automated guided vehicles, but deviations can invalidate a plan. With one-way lanes, a late vehicle or lost planner can close a ring of full segments. We separate how fast the floor runs from whether it keeps running. In OpenRing a planner proposes routes and an order, a local guard commits only moves and route changes that cannot close such a ring, and the order binds for a bounded time. Despite arbitrary proposals or planner loss, no ring closes. With two-place segments, traffic can continue under disturbances; progress is guaranteed once they end, and all vehicles exit if entries also stop. Among rules that reroute only on a proposal,…
- [ ] **[CoEvoBench: Can LLMs Drive Recursive Co-Evolution of Agentic Systems?](https://arxiv.org/abs/2611.27116v1)**
  <!-- aidb:id=arxiv:2611.27116v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Chuan Xiao, Baojie Wang, Haizhao Fan, Hongzhe Du, Xander Xu
  - Categories: cs.AI
  - Abstract: The performance of an LLM agent depends on both its model and its harness, the code that mediates its interaction with tools and environments. Can LLM researchers drive this co-evolution as a recursive improvement process, deciding round after round which component to change when each change alters the value of the other? Existing benchmarks evaluate post-training or data research with the harness out of scope, or harness optimization with the model fixed, leaving this joint decision unmeasured. We introduce CoEvoBench, a benchmark that evaluates LLMs as researchers co-evolving the model and harness of a target agent across five agentic domains. Researchers start from a common base model an…
  - Comment: 28 pages, 6 figures. Code: https://github.com/AlibabaResearch/CoEvoBench
- [ ] **[FreeOcc: Decoupling Ego-Motion for Efficient 4D Occupancy Forecasting via Continuous Flow Matching](https://arxiv.org/abs/2611.08128v2)**
  <!-- aidb:id=arxiv:2611.08128v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-05
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Zeping Zhang, Zhuoya Zhao, Samy Metari, Robert Laganière
  - Categories: cs.CV
  - Abstract: Current 4D occupancy world models use heavy cross-attention or deep recurrence to disentangle ego-motion from scene dynamics. This requires significant computational capacity. However, this effort is largely redundant since the ego-vehicle's intended future motion is provided by the downstream motion planner. We present FreeOcc, a lightweight continuous-time world model that introduces explicit $SE(2)$ geometric decoupling into a conditional flow-matching framework. By mathematically factoring out self-motion, we create a purely dynamic feature space. This space supports attention-free temporal fusion and allows physics-constrained ODEs to operate strictly on residual agent kinematics. To m…
- [ ] **[Markdown Is Not a Firewall: four coding agents, one rules file, four boundaries](https://arxiv.org/abs/2611.27112v1)**
  <!-- aidb:id=arxiv:2611.27112v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Sandeep Dhuri
  - Categories: cs.SE, cs.CR
  - Abstract: Teams put a one-page rules file in a repository and call it a control on coding agents. A registered study found agents rarely look up a repository's contribution rules. I asked the security question: what does a rules file do at a boundary, against a gate? I tested one 278-word rules file, with hypotheses and analysis code deposited first. Claude Code, Codex CLI, Gemini CLI and OpenCode with DeepSeek worked through 20 small repositories with hidden tests, 12 for three of them. Three agents met four boundaries I built: a refused endpoint, a destructive shortcut, a planted instruction and a planted package. Permission prompts, each vendor's own control layer, were off by design. A gate in fr…
  - Comment: 22 pages, 7 figures. Pre-registration: doi.org/10.5281/zenodo.23608308. Results dataset: doi.org/10.5281/zenodo.24238904
- [ ] **[RemoteEvolver: Expanding Earth Observation Capabilities through Agent Harness Evolution](https://arxiv.org/abs/2611.27110v1)**
  <!-- aidb:id=arxiv:2611.27110v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Shengxiang Xu, Liang Yao, Shuyi Chen, Yishu Wang, Shimin Di, Fan Liu, Bishun Yao, Hanghui Guo, Xinyu Liu, Chengye Liang, Yuyu Luo, Min-Ling Zhang
  - Categories: cs.CV
  - Abstract: We are interested in developing a continually self-improving remote sensing agentic system. It should identify and address its capability gaps, retaining the resulting improvements to enhance performance on subsequent tasks. However, existing systems typically rely on fixed toolsets and confine their experience accumulation to re-orchestrating predefined capabilities, constraining both capability expansion and the transfer of improvements across tasks. As the infrastructure for agentic systems, the harness manages tools and workflow knowledge as editable, persistent resources outside the base model. These resources can therefore be updated and reused across tasks without additional post-tra…
- [ ] **[Flying over The Uncertain Nature (FORTUNE): Intelligent and Humanistic 3D Path Planning for Low-Altitude Collaboration](https://arxiv.org/abs/2608.03408v2)**
  <!-- aidb:id=arxiv:2608.03408v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-04
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Wenbo Zhu, Wenhan Jia, Minghui Liwang, Yiguang Hong
  - Categories: cs.RO, cs.DC
  - Abstract: Low-altitude intelligent agents are driving demand for timely, socially responsible collaborative sensing in dynamic urban environments. Yet jointly handling heterogeneous spatio-temporal sensing demands, real-time uncertainty, and human-centered constraints in a unified multi-uncrewed aerial vehicle (UAV) framework remains challenging. We study 3D multi-UAV path planning and joint task assignment under heterogeneous spatio-temporal uncertainty of ground points of interest (PoIs). Unlike studies assuming static, known PoIs, we formulate a unified model capturing persistent (Type-I), temporally predictable (Type-II), and emergent unpredictable (Type-III) demands. Following the low-altitude-f…
- [ ] **[Omo: Giving Continuing AI-Agent Work a Place to Return To](https://arxiv.org/abs/2611.27107v1)**
  <!-- aidb:id=arxiv:2611.27107v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Kaviru Hapuarachchi, Harrison Edwards
  - Categories: cs.SE, cs.HC, cs.MA
  - Abstract: AI coding agents now keep working while the people who started them are away. Coming back is the hard part: a session list tells you which agent is where, but not what it was asked to do, what it changed, or what to tell it next. We present Omo, which gives each piece of continuing agent work a persistent place to return to. We built the idea twice. Omo Space is an open-source Minecraft mod in which rooms and screens that people build are live terminals on their own machine. Omo Theia brings the same rooms and desks into a customizable IDE, one step away from the editor and the Git patch. Both keep agent sessions running on the host after the view is closed. We describe the two systems, fou…
  - Comment: 4 pages, 1 composite figure (5 panels)
- [ ] **[PsyAgent: Constructing Human-like Agents Based on Psychological Modeling and Contextual Interaction](https://arxiv.org/abs/2601.06158v3)**
  <!-- aidb:id=arxiv:2601.06158v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-01-06
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zibin Meng, Kani Chen
  - Categories: cs.AI
  - Abstract: Human-like agents must express stable dispositions while adapting to roles, relationships, and norms. We present PsyAgent, a schema-first framework that operationalizes the trait-context interface by coupling a Big Five trait prior with explicit social-structural conditioning. PsyAgent comprises (i) Individual Structure (IS), a machine-usable trait-grounded profile, and (ii) Multi-Scenario Contexting (MSC), a curated library of role-relationship-norm frames spanning eight everyday arenas. At inference, fixed structured prompts couple the active MSC frame with the IS profile, encouraging behavior that is stable yet context-sensitive. To demonstrate learnability beyond prompt engineering, we…
  - DOI: 10.18653/2026.emnlp-main.25
  - Comment: 35 pages, 22 figures. Published in EMNLP 2026 (Main Conference). Updated to match the published version
- [ ] **[Epistemic Guard: Out-of-Process MCP Receipt Proxying, Post-Turn Prose Supervision, and Provenance-Gated Memory for Tool-Using Autonomous Agents](https://arxiv.org/abs/2611.27095v1)**
  <!-- aidb:id=arxiv:2611.27095v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Sean Maxwell
  - Categories: cs.SE, cs.AI, cs.CR
  - Abstract: Language-model agents using the Model Context Protocol (MCP) face three runtime verification gaps: (i) action fabrication, where post-tool prose narrates side effects that failed, timed out, or never ran; (ii) provenance collapse, where unverified model prose or web text enters durable memory alongside executed tool outputs; and (iii) syndicated echo amplification, where mirrored web pages satisfy multi-source corroboration from one origin. Existing MCP firewalls inspect wire calls before execution, while LLM-judge guardrails require multi-gigabyte VRAM without binding prose to receipts. We present epistemic-guard (v0.5.2), an open-source Python library and out-of-process stdio MCP receipt…
  - Comment: 8 pages, 3 tables; open-source code and osaudit-verified manifests at https://github.com/AlienatedAliens/epistemic-guard (v0.5.2)
- [ ] **[Separating Automation Gains from Agent Contributions in AI-Assisted Model Validation](https://arxiv.org/abs/2611.27094v1)**
  <!-- aidb:id=arxiv:2611.27094v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: M. Ahmadi Achachlouei
  - Categories: cs.CL, cs.AI, cs.SE
  - Abstract: LLM agents are being proposed for bank model validation, yet evaluations that compare agent-assisted work with manual practice credit the agent with gains that come from digitized evidence and deterministic tests. We propose a staged architecture in which an LLM-free controlled workflow (P1) is both the fallback and the control arm for individually authorized agent tasks (P2), and an attribution protocol that credits an agent only for faults P1 does not already report. The protocol charges decoy false alarms, unnecessary actions and endorsed developer assertions, counts invalid outputs as misses, folds newly automatable findings back into P1 with discovery credit, and fixes safety bounds an…
  - Comment: 5 pages, 1 figure, 3 tables. Synthetic evaluation pack and reproducibility code included as ancillary material
- [ ] **[Exercised, Rarely Recovered: What Public Reports Say About Recovery in 50 AI Agent Harnesses and Runtimes](https://arxiv.org/abs/2611.27090v1)**
  <!-- aidb:id=arxiv:2611.27090v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Kaviru Hapuarachchi
  - Categories: cs.SE, cs.AI, cs.MA
  - Abstract: When an AI coding agent deletes the wrong files or a long agent run crashes, users fall back on recovery mechanisms: resume from a checkpoint, undo, ask for approval, read the log. Research runtimes promise stronger guarantees, such as saga-style compensation and transactional rollback. We ask what public evidence shows about whether either kind works in real use. Under a protocol frozen before data collection, we graded 12 persistent agent runtimes, 26 coding-agent harnesses and 12 research runtimes on eight recovery mechanisms, from not found to exercised in a real run, with two blind coding passes, adjudication and re-verification against archived sources. Recovery is exercised almost ev…
  - Comment: 5 pages, 2 figures. Replication dataset: doi:10.5281/zenodo.24122560
- [ ] **[Unsatz: Evaluating Scientific Discovery Without a Given Ansatz](https://arxiv.org/abs/2611.03713v2)**
  <!-- aidb:id=arxiv:2611.03713v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-31
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Ethan Ji, Wei Wang, Yizhou Sun
  - Categories: cs.AI, cs.LG
  - Abstract: Before a scientist fits any parameter, they must decide what the model contains: which quantities exist, which are hidden, how they interact, and how they are measured. Physicists call such a trial form an ansatz. Benchmarks for automated equation discovery mostly supply it, by fixing the variables, a library of candidate terms, or a law to be modified. We introduce Unsatz, a benchmark in which an LLM agent must construct the ansatz itself. Each task is a simulated system, generated from a private seed as a program in a small modeling language: ordinary, delay, or partial differential equations, discrete maps, static and causal models, or stochastic processes, possibly with latent states, d…
- [ ] **[Weight-space programming and mechanistic interpretability for model editing in particle physics](https://arxiv.org/abs/2611.27079v1)**
  <!-- aidb:id=arxiv:2611.27079v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Raphaël Bonnet-Guerrini, Johann Ioannou-Nikolaides, Troels Petersen
  - Categories: hep-ph, cs.AI, cs.LG, hep-ex
  - Abstract: We demonstrate that weight-space programming and edits guided by sparse autoencoders can remove unwanted aspects of a particle-physics foundation model through direct edits to its weights. In a foundation model trained on jets, we observe that adding a single soft neutral particle causes large changes in jet classification, violating infrared safety. We locate the responsible attention heads with mechanistic analysis and trace the flaw's origin to pretraining on datasets with different reconstruction thresholds. We then propose two targeted approaches to repair the flaw: by removing three latent directions identified with sparse autoencoders, and by letting language-model agents edit the we…
- [ ] **[Decision Models Are General-Purpose Process Reward Models](https://arxiv.org/abs/2611.27068v1)**
  <!-- aidb:id=arxiv:2611.27068v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jiajun Fan, Qinglong Zheng, Ziwen Wang, Bangji Yang, Neil He, Ruihan Guo, Chaoran Cheng, Ge Liu
  - Categories: cs.AI
  - Abstract: Reinforcement learning (RL) from verifiable outcomes gives a language agent one reward per episode: every step is credited alike, and nothing about the task is learned when all rollouts fail. The last mile, step-level credit, usually requires step labels, a learned critic, costly LLM judges or hand-written rules. We introduce DM-PRM, which turns a general-purpose decision model -- one answering yes/no questions with probabilities -- into a general-purpose process reward model (PRM), zero-shot: no step labels, no fine-tuning, no critic. DM-PRM asks one question per step and adds the standardised answers to the advantage. It plugs into any policy-gradient method; one model, with one question…
- [ ] **[Protecting Private Values in Tool-Using LLM Agents via Recoverable Context Projection](https://arxiv.org/abs/2609.15011v2)**
  <!-- aidb:id=arxiv:2609.15011v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-14
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yu Li, Qikun Cai, Tao Huang, Chen Hou
  - Categories: cs.AI
  - Abstract: Memory-augmented and tool-using agents may expose exact private values when a remote LLM processes retrieved memory, tool actions, and observations. One-way masking limits initial exposure but removes values needed for trusted execution and may allow them to reappear in later observations. We propose Trustworthy Virtual Memory (TVM), a closed-loop runtime that exposes only projected context to the remote model, resolves exact values locally for trusted execution, and reprojects subsequent observations. We study whole-field and structure-preserving span-level projection, using a trusted local model to predict protected spans without access to the evaluation manifest. Experiments show that sp…
  - Comment: 5 pages, 2 figures
- [ ] **[A Survey on Long-Term Memory Security in LLM Agents: Attacks, Defenses, and Governance Across the Memory Lifecycle](https://arxiv.org/abs/2604.16548v6)**
  <!-- aidb:id=arxiv:2604.16548v6 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-04-17
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Zehao Lin, Xixuan Hao, Renyu Fu, Shaobo Cui, Kai Chen, Chunyu Li, Zhiyu Li, Feiyu Xiong
  - Categories: cs.CR, cs.AI, cs.CL
  - Abstract: The emergence of writable, cross-session persistent memory in LLM agents introduces a qualitatively different threat landscape from conventional input-centric security concerns, characterized by three properties: persistence, statefulness, and propagation. To systematically characterize this landscape, we propose a Memory Lifecycle Framework that organizes attacks, defenses, and their cross-phase dependencies along two axes: six lifecycle phases (Write, Store, Retrieve, Execute, Share & Propagate, Forget & Rollback) and four security objectives (Integrity, Confidentiality, Availability, Governance). This analysis in turn exposes the need for explicit security requirements at the system leve…
  - Comment: 22 pages, 3 figures, 4 tables. Expanded version of the EMNLP 2026 paper. Adds evidence on persistent representations, skill memory, authorization changes, and recovery. Table 4 compares lifecycle security claims and their evaluation conditions
- [ ] **[Actions Speak Louder than Words: Stateful Privacy Sniffing of LLM Agents via Behavioral Covert Channels in Web Interactions](https://arxiv.org/abs/2611.27046v1)**
  <!-- aidb:id=arxiv:2611.27046v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ruichao Liang, Wenzhong Deng, Jing Chen, Yuqing Li, Kaixuan Li, Cong Wu, Yang Liu
  - Categories: cs.AI
  - Abstract: LLM agents increasingly rely on Web interaction, issuing searches, following links, and reading pages, to complete complex user tasks. Since each action is driven by the agent's private context, including the user's prompt, dialogue history, memory, and connected data, it also opens a new privacy exposure surface. Prior attacks either passively analyze network traffic, which yields only coarse correlations, or hijack the agent through indirect prompt injection, which must place sensitive content in an outgoing field and is blocked by content-level defenses. Whether an attacker can actively recover fine-grained private context without any explicit transmission thus remains insufficiently und…
- [ ] **[RoboColiseum: Co-evolution of Simulation, Evaluation, and Models](https://arxiv.org/abs/2611.27042v1)**
  <!-- aidb:id=arxiv:2611.27042v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Chenghao Yin, Da Huang, Di Yang, Jichao Wang, Junhui Wu, Nanshu Zhao, Tong Ran, Zhijun Li, Gang Zhao, Linting Guo, Rui Feng, Sheng Zhang, Tianyu Jiang, Wenjun Sun, Yongxin Su, Zhaobo Liu, Zheyuan Xing, Sukai Wang, Yue Zhou, Qihan Jiang, Jianhua Jiang, Chuang Men, Yuxiang Yan, Daizhen Lv, Kunyu Yu,…
  - Categories: cs.RO
  - Abstract: Simulation-based evaluation of embodied models requires calibrated interactions, diverse tasks, and explicit execution constraints. We present RoboColiseum, a platform combining system identification, composable physics and rendering, and multidimensional benchmarking. Recorded-command replay characterizes robot dynamics and object interactions, while a shared interface connects rigid and deformable simulation to rendering. Across 22 paired real--simulation robot--task configurations, task scores have a reported Pearson correlation of 0.9686. Eight evaluation tracks span instruction following, spatial reasoning, general manipulation, robustness, dexterous manipulation, precision manipulatio…
  - Comment: 11 pages, 8 figures. The first eight authors contributed equally. Maoqing Yao and Qian Wang are the corresponding authors
- [ ] **[Subverting Tool Arguments: Defense-Evading Metadata Poisoning in LLM Agents](https://arxiv.org/abs/2611.27041v1)**
  <!-- aidb:id=arxiv:2611.27041v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Shih-Chieh Dai, Xinyu Sun, Haichuan Zhang, Zhiyuan Zhong, Guanhong Tao
  - Categories: cs.CR
  - Abstract: Conventional indirect prompt injection (IPI) attacks hijack an LLM agent's workflow through malicious instructions embedded in retrieved external content. The growing adoption of the Model Context Protocol (MCP) exposes another attack surface: tool descriptions supplied by third-party MCP servers. Attackers can manipulate this metadata to induce malicious argument generation during tool calls. The challenge is to ensure that the modified descriptions still appear benign to both LLMs and users. Existing IPI attacks, however, struggle to achieve both high attack success and low detectability in this setting. To address this challenge, we propose GRAFT, an LLM-based optimization method for cra…
- [ ] **[Mobility-Aware Task Offloading in Mobile Edge Computing-Empowered Space-Air-Ground Integrated Internet-of-Things Networks](https://arxiv.org/abs/2611.14102v2)**
  <!-- aidb:id=arxiv:2611.14102v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-10
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Minghao Sun, Jinghuai Xiong, Xiaoli Chu, Di Yuan, Zitian Zhang
  - Categories: cs.NI
  - Abstract: Mobile edge computing (MEC)-empowered spaceair-ground integrated Internet-of-Things (IoT) networks (SAGIINs) provide a promising solution for computation-intensive tasks generated by mobile IoT devices (IDs). However, task offloading in SAGIINs is challenging due to time-varying IDto-unmanned aerial vehicle (UAV) channels, intermittent LEO satellite service availability, and the coupling among UAV trajectory, communication, computation, and energy decisions. This paper investigates an energy-efficient task offloading and UAV trajectory planning problem in an MEC-empowered SAGIIN, where one UAV acts as both an aerial relay and an MEC server, and multiple LEO satellites provide supplementary…
- [ ] **[Mind the Delta: Early Pruning of RTL Variants for Agentic Hardware Optimization](https://arxiv.org/abs/2611.27035v1)**
  <!-- aidb:id=arxiv:2611.27035v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Siyang Cai, Cangyuan Li, Haoyu Gao, Kun Wang, Mochen Li, Yilin Zhong, Ke Xu, Yinhe Han, Ying Wang
  - Categories: cs.AR
  - Abstract: Autonomous coding agents powered by large language models (LLMs) now write diverse microarchitectural variants of existing register-transfer level (RTL) designs at high throughput, shifting the primary bottleneck of agentic RTL optimization onto logic synthesis. Commercial toolchains take hours per variant, creating an acute compute asymmetry between proposing and evaluating variants. Existing fast evaluators falter in this regime. Subtle RTL edits trigger nonlinear synthesis shifts that learned predictors and coding agents cannot resolve, while synthesis proxies at reduced effort either alter the optimization trajectory or retain most of its runtime. Selecting a variant, however, does not…
- [ ] **[ReactDrive: Self-Reactive Driving World Model](https://arxiv.org/abs/2611.27024v1)**
  <!-- aidb:id=arxiv:2611.27024v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yifan Wang, Xiaoqi Wang, Cho-Ying Wu, Wenbin He, Chenyu You, Liu Ren
  - Categories: cs.CV
  - Abstract: The world evolves through the dynamics of its constituent entities and their interactions, with changes in one entity influencing the behavior of others. To simulate this evolution under different actions, interactive world models need to capture the resulting agent responses as part of the world's own dynamics. In autonomous driving, errors in modeling these responses can misrepresent maneuver safety and undermine the reliability of generated videos used for policy evaluation and learning. To formalize this intrinsic requirement for driving world model, we define self-reactivity as the capability to model agent responses from observed history and a specified ego action, and generate visual…
- [ ] **[From Reflection to Co-Evolution: Self-Evolving Agents with Locally Verified Memory](https://arxiv.org/abs/2611.10382v3)**
  <!-- aidb:id=arxiv:2611.10382v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-07
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Xinxiang Yin, Xinglang Zhang, Haodong Chen, Zhiqing Cui, Weidong Tang, Yuxuan Wang, Junrui Wang, Jingyi Zhang, Jianfeng Zhang, Jian Qian
  - Categories: cs.CV
  - Abstract: LLM agents have made impressive progress in coding and mathematical reasoning, motivating growing interest in learning from long-horizon interaction. Memory supports this process, but plausible lessons can be redundant or reinforce inappropriate actions. Can a memory's source decision provide a practical test for whether to retain it? We localize consequential trajectory steps, extract candidate memories, and replay each source decision with and without its candidate under the same context. This reveals two properties: most candidates barely shift the probed distribution, and both successful and failed source actions can be reinforced or suppressed. These observations motivate Anchor, which…
  - Comment: 31 pages, 9 figures, 6 tables
- [ ] **[Safe Personal RSI: Evaluating and Repairing Personal-Agent Updates](https://arxiv.org/abs/2611.23651v2)**
  <!-- aidb:id=arxiv:2611.23651v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-18
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Jiapeng Pei, Yuhang Yao, Sitan Liu, Hanxin Chen, Hao Li, Guogeng Li, Jiapei Liu, Ruijie Chen, Hongshan Lin, Shangding Gu, Yang Mo, Tianyu Shi
  - Categories: cs.SE, cs.AI, cs.CL
  - Abstract: Kicker is a personal health assistant. Changes to an assistant's reusable instructions can improve task handling while changing what it discloses, which requests it follows, and how it reports actions. We study Safe Personal RSI, an update-evaluation component developed for Kicker. We restrict recursive self-improvement (RSI) to prompt updates, with model weights and runtime code fixed. The procedure tests proposed and current instructions, repeats failing cases, temporarily undoes changes to guide repairs, and checks safety and task performance before adoption. If no version passes, the current instructions stay in use. Our executable benchmark contains 29 email, calendar, health, and mark…
  - Comment: Typo fixed. Add more to appendix
- [ ] **[Declarative Skills for AI Agents in Knowledge-Grounded Tool-Use Workflows](https://arxiv.org/abs/2606.06923v2)**
  <!-- aidb:id=arxiv:2606.06923v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-05
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: M. Danish Lim, I. Danial Bin Sharudin, Wen Han Chen, Cedric Lim, Laura Wynter
  - Categories: cs.AI, cs.SE
  - Abstract: We study how orchestration affects tool-using large language model (LLM) agents in customer-service workflows over an unstructured knowledge base, comparing a declarative agent that reads natural-language skill files, an imperative agent built on a state machine, and an unscaffolded baseline. The three are formalized as policy classes within one decentralized partially observable Markov decision process and evaluated on a complete design of five models, two retrieval regimes, and three agents, with paired tests. Averaged over all conditions, orchestration does not improve task success. The effect, however, depends on the quality of the agent's observation channel. Under perfect retrieval, s…
- [ ] **[Physics-Guided Recursive Self-Improvement of Amortized Bayesian Inference Across Physics](https://arxiv.org/abs/2611.27006v1)**
  <!-- aidb:id=arxiv:2611.27006v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Bo Liang, Mingtao Chen, Minghui Du, Ziren Luo, Guohua Wang, Peng Xu, Zhichao Hu, Maxm Pan
  - Categories: physics.comp-ph, astro-ph.CO, astro-ph.EP, astro-ph.IM
  - Abstract: Across physics, from the orbits of imaged exoplanets and the matter inside neutron stars to thin films at synchrotrons and cortical neurons, conservation laws, interference, and compensating currents compress the posteriors of precise data into tiny, curved regions where Markov chains need minutes to days. We introduce PhyRSI (physics-guided recursive self-improvement), in which an AI agent coupled to the simulator writes and revises an amortized Bayesian inference algorithm for each field, scored by the importance weights of the exact likelihood because the true posterior is unknown. It evolves coordinates, symmetries, and factorizations matched to the physics: orbital elements at the best…
  - Comment: 7 pages, 2 figures, 2 tables
- [ ] **[Moonshine Conjecture Formalized](https://arxiv.org/abs/2611.27001v1)**
  <!-- aidb:id=arxiv:2611.27001v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Jin-Cheng Guu
  - Categories: math.QA, cs.LO, math-ph
  - Abstract: The celebrated and intimidating Moonshine Conjecture has now been formalized in Lean. This achievement might suggest that, once a sufficiently large library compiles, the principal mathematical work is complete. This paper tells a less optimistic story. During our formalization project, we repeatedly encountered two problems that a formally checked proof alone does not settle: (1) whether the formal statements actually express the mathematics we humans expect, and (2) how that meaning survives as the repositories and their dependencies evolve. We argue that there is no magic pill that turns a large agent-produced library into mathematics a community can trust. Even after the proofs are chec…
  - Comment: 7 pages, 0 figures. A case study in Lean formalization, semantic trust, and repository versioning
- [ ] **[DEBATE: A Large-Scale Benchmark for Evaluating Opinion Dynamics in Role-Playing LLM Agents](https://arxiv.org/abs/2510.25110v8)**
  <!-- aidb:id=arxiv:2510.25110v8 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-10-29
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Yun-Shiuan Chuang, Ruixuan Tu, Chengtao Dai, You Li, Smit Vasani, Binwei Yao, Michael Henry Tessler, Sijia Yang, Dhavan Shah, Robert Hawkins, Junjie Hu, Timothy T. Rogers
  - Categories: cs.CL
  - Abstract: Modeling opinion change through social interactions is important for understanding polarization, misinformation, and societal conflict. Recent work simulates opinion dynamics with role-playing LLM agents (RPLAs), but multi-agent simulations often display unnatural group behavior (e.g., premature convergence) and lack empirical benchmarks for assessing alignment with real human group interactions. We introduce DEBATE, a benchmark for evaluating the authenticity of opinion dynamics in multi-agent RPLA simulations. Its three-round design makes each participant's public interaction history complete and traceable. DEBATE contains multi-round public messages and private Likert-scale beliefs from…
  - Comment: Accepted at the 40th Conference on Neural Information Processing Systems (NeurIPS 2026), Track on Evaluations and Datasets
- [ ] **[From Letter-of-Credit Requirements to Executable Specifications: Evaluating Verification Accuracy and Completeness](https://arxiv.org/abs/2611.26988v1)**
  <!-- aidb:id=arxiv:2611.26988v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ji Sub Choi, Whan Choi, Seo Yeon Gu, Suhyun Kim, Inyong Yun
  - Categories: cs.AI, cs.CL
  - Abstract: In letter-of-credit (LC) document examination, a correct final decision does not show that every requirement was examined. We therefore evaluate examination requirement by requirement and make each requirement executable. A language model converts the bill of lading (BL) and commercial invoice (IV) requirements of a credit into atomic conditions and logical structures, and a deterministic verifier retrieves the named evidence and computes each outcome, so every check can be compared with a gold encoding and traced to logged evidence. Because LC records are confidential, our on-premises 9B parser is fine-tuned only on synthetic pairs built from templates and human-reviewed public document va…
  - Comment: Accepted at the 3rd Workshop on LLMs and Generative AI for Finance (AI4F) at ACM ICAIF 2026 (non-archival). 10 pages, 4 figures, 7 tables. Code: https://github.com/Ji-S/LC-Spec-Synth
- [ ] **[Privacy Protection in Self-Evolving Personal Agents: Persistent Memory and Cross-Carrier Transfer](https://arxiv.org/abs/2611.26983v1)**
  <!-- aidb:id=arxiv:2611.26983v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zibin Lin, Taotao Wang, Shengli Zhang
  - Categories: cs.CR, cs.AI
  - Abstract: Personal agents carry private experience into later decisions through persistent memory. This thematic survey compares memory admission, maintenance, release, and withdrawal by protected change, observer, and validation setting. Direct evidence in the screened corpus comes from controlled memory workflows. Three worked scenarios follow one private fact through booking, feedback-driven learning, and withdrawal. We show when prompt revision and memory reads compose, when skills inherit a private head's bound, and why reader non-use does not establish cleanup of learned state. Diagnostic experiments measure the utility costs of wider label protection and broad memory deletion, and test how mis…
- [ ] **[Agentic Coding in the Wild: Characterizing GitHub Copilot Traces at Production Scale](https://arxiv.org/abs/2608.00101v2)**
  <!-- aidb:id=arxiv:2608.00101v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-07-30
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Banruo Liu, Haoran Qiu, Íñigo Goiri, Rodrigo Fonseca, Ricardo Bianchini, Esha Choukse
  - Categories: cs.AI, cs.LG
  - Abstract: AI coding agents (e.g., GitHub Copilot, Claude Code, Codex) interleave multi-step LLM inference with tool execution, creating a workload different from chatbots. We present the first production-scale characterization of coding agents using sampled GitHub Copilot traces from June-July 2026, comprising 7.4M users, 819M conversations, 5.7B LLM calls, and 946T tokens. Our analysis reveals distinctive workload properties with unique systems implications: e.g., sparse user-initiated turns unfold into autonomous agent loops with nearly 1:1 coupling between LLM calls and tool execution; parallel LLM calls are rare but exist in turns that trigger subagents; KV cache hit rates average 90% within a tu…
- [ ] **[Contexture: Runtime Context Eviction for High-Throughput Agent Serving](https://arxiv.org/abs/2611.26980v1)**
  <!-- aidb:id=arxiv:2611.26980v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Colin Hong, Bryan Shan, Wei Siong Pang, Chengzhi Lu, Xu Guo, Nitin Shivaraman, Tao Luo, Esha Choukse, Kisson Lin, Dmitrii Ustiugov
  - Categories: cs.DC, cs.AI, cs.MA, cs.OS
  - Abstract: LLM agents such as Hermes, OpenClaw, and Codex repeatedly resend growing execution histories, increasing shared GPU key-value (KV) cache demand in high-bandwidth memory (HBM). We show that shared KV capacity limits agent-serving throughput. Existing context-reduction methods lack global cache-state visibility, while runtime KV managers lack tool-execution information. Tracing tokens to their originating tool operations reveals that later operations supersede earlier outputs and associated turns, identifying 64% of recorded final-history tokens as removal candidates. We present Contexture, a harness- and model-agnostic architecture for runtime context eviction. Contexture separates the harne…
  - Comment: 14 pages, 15 figures
- [ ] **[Keep the Process, Change the Supplier: Runtime Governance for Tool-Using AI Agents](https://arxiv.org/abs/2611.26966v1)**
  <!-- aidb:id=arxiv:2611.26966v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Deepak Waghmare, Shaad Sufi
  - Categories: cs.AI
  - Abstract: Tool-using AI agents propose actions whose authorization and external effects cannot be inferred from generated text alone. We study an execution boundary that separates agent proposals from business-controlled authority, context disclosure, and supplier selection. The Open Process Control Plane (OPCP) mediates capability calls and records uncertain outcomes when a supplier may have acted without returning an acceptable reply. We evaluate this runtime with scripted requests and synthetic suppliers: 2,400 fault episodes across four policies, 60 process-termination/restart episodes, 19,000 timed calls across 19 configurations, five targeted mutations over 43 fixtures, and 160 substitution rec…
- [ ] **[Idempotency Is Not Recovery: A Fault-Injection Study of Language-Model Agent Tool Actions](https://arxiv.org/abs/2611.23353v2)**
  <!-- aidb:id=arxiv:2611.23353v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-17
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Song Xu
  - Categories: cs.SE, cs.AI
  - Abstract: When a language-model agent's tool call is interrupted, the action may already have changed an external system without confirmation. Retrying risks duplication; assuming success may conceal an action that never occurred. We study these failure modes in a controlled agent runtime combining authorization, an action ledger, target-side idempotency, reconciliation, and evidence sealing. We inject ten single-host fault classes and compare four configurations and three ablations using a target-side oracle separate from the runtime ledger. On each of Windows and Linux, 7,513 trials used 96 captured model responses from 24 constructed cases. In 200 known original crash and replay pairs, the full co…
  - Comment: 12 pages, 1 figure. Added submission notice on first page. Earlier single-author preprint; a later revision with additional authors was submitted to IEEE Transactions on Reliability. Aggregate data: https://doi.org/10.5281/zenodo.24369921
- [ ] **[RAG Makes Guardrails Brittle? Investigating Robustness of Guardrails under RAG-style Contexts](https://arxiv.org/abs/2510.05310v2)**
  <!-- aidb:id=arxiv:2510.05310v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-10-06
  - Updated: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Yining She, Daniel W. Peterson, Marianne Menglin Liu, Vikas Upadhyay, Mohammad Hossein Chaghazardi, Eunsuk Kang, Dan Roth
  - Categories: cs.CL, cs.AI
  - Abstract: With the increasing adoption of large language models (LLMs), ensuring the safety of LLM systems has become a pressing concern. External LLM-based guardrail models have emerged as a popular solution to screen unsafe inputs and outputs, but they are themselves fine-tuned or prompt-engineered LLMs vulnerable to data distribution shifts. In this paper, taking Retrieval Augmentation Generation (RAG) as a case study, we investigate how robust LLM-based guardrails are against additional information embedded in the context. Through a systematic evaluation of 3 Llama Guards and 2 GPT-oss models, we find that inserting benign retrieved documents flips the judgments of input and output guardrails in…
- [ ] **[Tracking and Limiting Unsupported Claim Propagation in Multi-Agent LLM Systems: A Provenance-Aware Framework](https://arxiv.org/abs/2611.26957v1)**
  <!-- aidb:id=arxiv:2611.26957v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Zijia Cao, Hanqing Dou
  - Categories: cs.MA, cs.AI
  - Abstract: This research examines how unsupported claims change as they move through multi-agent pipelines. It also examines whether preserving provenance can reduce these changes. We test both homogeneous and heterogeneous pipelines. Homogeneous pipelines use the same model across agents, while heterogeneous pipelines use different models. We compare the baseline with a provenance-aware framework. The framework passes each claim with its support status, source, evidence and transmission history. No new evidence is introduced during transmission. We measure changes in claim meaning, unsupported detail accretion, semantic drift, and provenance preservation. These metrics show whether the framework limi…
- [ ] **[CodeReviewBench: An Automated Benchmark for Evaluating the Software Factory](https://arxiv.org/abs/2611.26942v1)**
  <!-- aidb:id=arxiv:2611.26942v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ashley Zhang, Narmeen Fatimah Oozeer, Aleksandr Zverianskii, Daniel Ng, Tasana Pejovic, Antía García, Jacob Clyne, Ravpreet Setia, Akshay Utture, Etan Jacob Ginsberg, Shriyash Kaustubh Upadhyay, Fazl Barez
  - Categories: cs.AI, cs.SE
  - Abstract: As AI agents ship more code with minimal human oversight, code review becomes the critical quality-control checkpoint -- but one without a reliable, objective verifier: review quality is nuanced and ultimately a judgment call by the PR author. Existing benchmarks are structurally misaligned with this: annotators are third-party reviewers, like the bots they evaluate, not the PR authors who actually decide what to fix. They also rely on small, static issue sets that require full re-evaluation as tools update, limiting how frequently progress can be tracked. We introduce CodeReviewBench, built on a fundamentally different signal: revealed developer preferences -- if a developer acts on a bot'…
- [ ] **[Looking Right Is Not Being Right: Evaluating the Geometry of Agent-Built 3D Scenes](https://arxiv.org/abs/2611.26937v1)**
  <!-- aidb:id=arxiv:2611.26937v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Ziyang Long, Yen-Liang Lin, Shifan Zhu, Allen Tu, Meher Gitika Karumuri, Chenqi Li, Srikumar Sastry, Sarosij Bose, Mellon M. Zhang, Hsin-Jung Yang
  - Categories: cs.CV
  - Abstract: Vision-language agents can reconstruct rooms from video as editable 3D scenes, but convincing renders do not establish geometric accuracy. We introduce a scan-referenced evaluation and use controlled experiments to study reconstruction accuracy, the role of geometric inputs, and agents' ability to verify and correct their scenes. Our geometric score measures surface, depth, and furniture placement agreement with laser scans of 30 real rooms on a 0-100 scale. The strongest tested agent, GPT-6 Astra, scores 51.4 from video alone, while a dense reconstruction from the same video scores 75.9. Given the point cloud used for that reconstruction, Astra produces an editable scene that scores within…
  - Comment: 11 pages, 6 figures. Project: https://github.com/Albertlongzi/looking-right-being-right
- [ ] **[SecretAgent: A Multi-Agent Framework for Privacy Protection against Vision Language Models](https://arxiv.org/abs/2611.26936v1)**
  <!-- aidb:id=arxiv:2611.26936v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Minda Zhao, Yue Zhang, Mengyu Wang
  - Categories: cs.CV, cs.AI, cs.CR, cs.LG, cs.MA
  - Abstract: Vision-language models (VLMs) can infer private information from shared images, including locations, personally identifiable information (PII), and personal attributes such as age and sex, even from medical images. Adversarial perturbations can protect such information against black-box VLMs, but existing methods overlook image quality and introduce visible artifacts into the images they protect. We present SecretAgent, the first general multi-agent framework that protects image privacy against VLMs while preserving visual fidelity. LLM agents iteratively locate the visual evidence that reveals private information and adapt an invisible perturbation to the target VLM's answers and to an app…
- [ ] **[AhaBench: Do Agents Turn Experience into Reusable Insights? A Long-Horizon Benchmark for Continual Learning](https://arxiv.org/abs/2609.05435v3)**
  <!-- aidb:id=arxiv:2609.05435v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-30
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Zerui Cheng, Jiawei Xu, Huacan Chai, Jiayang Sun, Pramod Viswanath, Maxm Pan
  - Categories: cs.LG, cs.CL
  - Abstract: Solving a task, even from a worked example, does not make an agent any better at the next one. As agents move from single tasks to long collaborations with people, turning experience into reusable insight becomes the capability that separates a tool from a collaborator that improves over time. AhaBench is a benchmark for this kind of continual learning. It simulates three patterns of long human-AI collaboration and holds a later test fixed while varying the experience before it: in Aha-Puzzle, the agent questions a partner who knows the answer to a new mystery after solving earlier ones; in Aha-Euler, a person teaches a computation and the agent applies it to new inputs; in Aha-Vending, the…
  - Comment: 35 pages, 8 figures
- [ ] **[Task-Specific Agent Memory For Continual Learning](https://arxiv.org/abs/2609.29144v2)**
  <!-- aidb:id=arxiv:2609.29144v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-24
  - Updated: 2026-11-20
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Yezhou Cheng, Runjia Du, Zeming Liu, Qibai Chen, Hang Lyu, Yankai Zeng, Yilan Wei, Bojun Lin
  - Categories: cs.AI
  - Abstract: Language-model agents can learn continually by storing useful instructions in memory and reusing them as new tasks arrive, without changing model weights. This requires both learning from new feedback and retaining earlier gains. However, an instruction learned from one task family can hurt other families when the agent uses the same memory for every task. We introduce task-specific agent memory: proposed skills are checked with execution tests, stored by task family, and retrieved for tasks in that family. We evaluate this design on a 12-round code-repair benchmark with recurring task families, tracking performance throughout learning. Holding proposals, acceptance decisions, and task comp…
- [ ] **[The Illusion of Evaluation: Challenges in Agentic Product Evaluation Practice](https://arxiv.org/abs/2611.26923v1)**
  <!-- aidb:id=arxiv:2611.26923v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Abhinav Palia, Andrew Gully, Drew Brooks
  - Categories: cs.CY
  - Abstract: Agentic products introduce risks that extend beyond those of their underlying models, arising from their tools, permissions, data access, safeguards, and operating conditions. Existing evaluation instruments provide useful evidence about model behavior and agents in defined harnesses, but their results do not necessarily transfer to deployed products or cover risks created by product configurations and interactions. Identifying and measuring such risks is especially difficult before deployment, when failure pathways, exposure, and outcome distributions may be poorly understood. This raises a fundamental question: what can evaluation evidence establish about the safety of a particular produc…
- [ ] **[Multi-Tier Edge Triage: Optimizing Latency for Safe Clinical Agents](https://arxiv.org/abs/2611.26914v1)**
  <!-- aidb:id=arxiv:2611.26914v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-20
  - Topics: agents, rag, research
  - Authors: Joshua Broyde, Sarita A. Joshi
  - Categories: cs.LG
  - Abstract: Deploying generative AI agents in enterprise clinical workflows requires enforcing multi-dimensional safety and compliance policies--preventing HIPAA Protected Health Information (PHI) exposure, maintaining clinical scope-of-practice boundaries, ensuring patient-appropriate reading comprehension, and preserving brand integrity--under interactive latency constraints. Synchronous outbound calls to cloud Large Language Model (LLM) judges add substantial network and decoding overhead onto the critical response path. We present Multi-Tier Edge Triage, a safety screening architecture that co-locates a compact Tier-1 sequence classifier on the clinical agent's host server, resolving clear queries…
  - Comment: 16 pages, 7 figures, 8 tables
- [ ] **[Welcome Inkling 2 Mini, Cutting-edge Performance for your Local Setup](https://huggingface.co/blog/inkling2mini)**
  <!-- aidb:id=url:824c03b970f1dc58cad6 -->
  - Feed: Hugging Face and community engineering
  - Published: 2026-11-20
  - Topics: engineering, research
- [ ] **[Introducing harness adapters: adapt your favorite model to your harness to improve performance and cost](https://huggingface.co/blog/harness-adapters-at-scale)**
  <!-- aidb:id=url:701a571706ec6c00de8b -->
  - Feed: Hugging Face and community engineering
  - Published: 2026-11-20
  - Topics: engineering, research
- [ ] **[Hebbia sees improvements in financial research with GPT-6 Astra](https://openai.com/business/customer-stories/hebbia)**
  <!-- aidb:id=url:8145fefb47ff1ca9fa55 -->
  - Feed: OpenAI research and engineering
  - Published: 2026-11-20
  - Topics: research, engineering
  - Abstract: Hebbia tested GPT-6 Astra for financial research. Its prerelease evaluations found gains in source coverage, citation relevance, and presentation quality.
- [ ] **[Can AI help scientists identify promising drug candidates?](https://openai.com/index/introducing-medchembench)**
  <!-- aidb:id=url:c1a2af93db54bfcf7c21 -->
  - Feed: OpenAI research and engineering
  - Published: 2026-11-20
  - Topics: research, engineering
  - Categories: Research
  - Abstract: MedChemBench evaluates how well AI models interpret molecular structures, reason from experimental evidence, and select compounds in early drug discovery.
- [ ] **[Self-Evolving Beyond Human-Crafted Experience for EDA Scripting](https://arxiv.org/abs/2611.26912v1)**
  <!-- aidb:id=arxiv:2611.26912v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Yang Liu, Shengbo Tong, Xiyuan Chen, Shiwei Hou, Sen Yuan, Hao Wang, Yanfeng Li, Hongwen Li, Yiming Zhu, Zhuolun He, Wenjian Yu
  - Categories: cs.AI
  - Abstract: The growing complexity of electronic systems demands efficient design flows, yet EDA scripting remains a bottleneck: proprietary APIs are sparsely documented, and errors often appear as silent failures or cryptic exceptions. Hand-crafted knowledge helps but is difficult to maintain as toolchains evolve. We present ZhuLong-SE (Self-Evolution), an execution-grounded LLM agent that learns reusable knowledge from prior task traces. Building on ZhuLong, it enhances the task-level harness with API retrieval, documentation responses, isolated sandbox execution, and static checking, then adds governed cross-task self-evolution. Beyond solving individual tasks, ZhuLong-SE distills past execution tra…
  - Comment: Submitted to DATE 2027. 7 pages, 3 figures, 5 tables
- [ ] **[InfantConnect: integrating developmental brain atlases and electrophysiological network analysis](https://arxiv.org/abs/2611.26911v1)**
  <!-- aidb:id=arxiv:2611.26911v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Alessandro Crimi, Paweł Gryboś
  - Categories: cs.CE
  - Abstract: The brains of infants change considerably during the first two years. Hence, developmental neuroimaging requires computational tools that account for age-related anatomy while supporting the analysis of electrophysiological data. For instance, cortical surfaces, electrode montages, tractography atlases, and electroencephalography (EEG) analysis utilities are commonly distributed across separate resources and software environments. Here we propose an open Python framework that brings these components into a shared three-dimensional workspace and supplements interactive visualization with command-line tools for EEG quality control, preprocessing, source-related visualization, and effective-co…
- [ ] **[Improving Consistency in Retrieval-Augmented Systems with Group Similarity Rewards](https://arxiv.org/abs/2510.04392v2)**
  <!-- aidb:id=arxiv:2510.04392v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-10-05
  - Updated: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Faisal Hamman, Chenyang Zhu, Anoop Kumar, Xujun Peng, Sanghamitra Dutta, Daben Liu, Alfy Samuel
  - Categories: cs.CL, cs.AI, cs.CY, cs.LG
  - Abstract: Retrieval-Augmented Generation (RAG) systems are increasingly deployed in high-stakes domains where users expect outputs to be consistent across semantically equivalent queries. However, existing systems often exhibit significant inconsistencies due to variability in both the retriever and generator, undermining trust and reliability. In this work, we focus on information consistency, i.e., the requirement that generated outputs convey the same core content across semantically equivalent inputs. We introduce a principled evaluation framework that decomposes RAG consistency into retriever-level, generator-level, and end-to-end components, enabling systematic identification of inconsistency s…
  - Comment: NeurIPS 2026 Main Conference
- [ ] **[AstronautBench: Measuring Agent Self-Improvement Across Episodes Through Knowledge, Evidence, and Progress](https://arxiv.org/abs/2611.26910v1)**
  <!-- aidb:id=arxiv:2611.26910v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Congyuan Yu, Runping Tian
  - Categories: cs.AI, cs.CL
  - Abstract: LLM agents are expected to improve themselves from their own experience across episodes, with fixed weights. Self-improvement in an embodied world cannot be read from one measure. Existing benchmarks measure task progress, world-knowledge question answering (QA), and episodic memory, but a correct answer does not show that the agent ever observed the evidence for it, and progress does not show what the agent learned. We introduce AstronautBench, which measures one agent's self-improvement through three views on the same run: what it knows, whether its own evidence supports that knowledge, and how far it gets in the world. It is built on the game Outer Wilds, where each episode is a 22-minut…
  - Comment: 11 pages, 3 figures, 6 tables
- [ ] **[AI-Assisted Decision Support for Formula 1 Pit-Stop Strategy: Deep Reinforcement Learning and Mathematical Programming](https://arxiv.org/abs/2611.26909v1)**
  <!-- aidb:id=arxiv:2611.26909v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Felipe Méndez, Charles Thraves
  - Categories: math.OC, cs.AI
  - Abstract: Pit-stop strategy in Formula 1 is a sequential decision problem under uncertainty, in which strategists decide at each lap whether to pit and which tire compound to fit. We develop a data-driven simulator, calibrated with historical race data, that captures tire degradation, drivers' recent performance, overtaking, yellow flag events, and rivals' pit-stop decisions. We train agents with five Deep Reinforcement Learning (DRL) algorithms and compare them with a Quadratic Mixed-Integer Programming (QMIP) formulation that is optimal in deterministic single-driver settings. Without uncertainty or competition, all DRL methods except TRPO achieve near-optimal performance. With a full grid of compe…
  - Comment: 54 pages (main text and appendices). Code, data and trained models: https://doi.org/10.5281/zenodo.24361704
- [ ] **[Budget-Aware Predict-and-Verify Theorem Proving with Heterogeneous LLM Solvers](https://arxiv.org/abs/2611.26906v1)**
  <!-- aidb:id=arxiv:2611.26906v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Wei Jiang, Ziran Liu, Wei Wang
  - Categories: cs.AI, cs.LG, cs.LO
  - Abstract: Large language model (LLM) theorem solvers differ in both proving capability and inference cost. Applying an expensive solver to every subgoal wastes computation when cheaper models are sufficient, while always starting from the cheapest solver wastes attempts on subgoals that require stronger models. We present BudgetPV, an agentic budget-aware predict-and-verify system that allocates computation across unresolved subgoals and heterogeneous LLM solvers. BudgetPV uses a cross-solver predictor to guide solver selection for each subgoal and revises the allocation as verification feedback becomes available. The allocation problem changes as proving progresses. Early decisions mainly determine…
  - Comment: 16 pages, 9 tables, 1 figure
- [ ] **[Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](https://arxiv.org/abs/2605.11229v2)**
  <!-- aidb:id=arxiv:2605.11229v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-05-11
  - Updated: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Neil Fendley, Zhengyu Liu, Aonan Guan, Jiacheng Zhong, Yinzhi Cao
  - Categories: cs.CR, cs.AI, cs.SE
  - Abstract: Automation platforms such as GitHub Actions and n8n are increasingly adopting so-called agentic workflows, which integrate Large Language Model (LLM) agents for tasks such as code review and data synchronization. While bringing convenience for developers, this integration exposes a new risk: An adversary may control and craft certain inputs, such as GitHub issue comments, to manipulate the LLM agent for unwanted actions, such as credential exfiltration and arbitrary command execution. To our knowledge, no prior academic work has studied such a risk in agentic workflows. In this paper, we design the first detection and exploitation framework, called JAW, to hijack agentic workflows hosted on…
  - DOI: 10.1145/3830454.3846775
- [ ] **[Perceive Once, Escalate on Demand: Handing Off Visual KV Memory from Small to Large VLMs](https://arxiv.org/abs/2611.26902v1)**
  <!-- aidb:id=arxiv:2611.26902v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Qiang Zhou, Jianing Deng, Siyan Dong, Jingxian Chen, Han-Yi Lin, Jingtong Hu
  - Categories: cs.CV, cs.AI, cs.CL, cs.LG, cs.RO
  - Abstract: An embodied agent cannot afford a large vision-language model (VLM) at every step of a long video, so a cascade runs a small VLM continuously and escalates only uncertain decisions to a large one. Each escalation, however, forces the large model to re-encode a history the small model has already perceived, and this dominates its cost. We present Baton, which hands the large model the small model's visual memory, its key-value (KV) cache over the history. Baton rests on one finding: the large model needs a usable memory, not a faithful copy of its own. A map trained to reproduce the large model's cache matches it most closely, yet brings no gain over the small model alone. Baton instead dist…
  - Comment: 10 pages, 6 figures
- [ ] **[ReDence: A Hybrid Agentic and System One Model Framework for Rapid, Evidence-Grounded Detection of Social Engineering Scams](https://arxiv.org/abs/2610.30963v2)**
  <!-- aidb:id=arxiv:2610.30963v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-22
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Jaishnoor Kaur, Josef Horáček, Ian Waskom, Sayak Saha Roy
  - Categories: cs.CR, cs.LG
  - Abstract: Detecting online social engineering (SE) scams often requires examining website workflows, verifying claims against external sources, and connecting evidence across multiple pages. Existing detectors provide limited support for these tasks and rarely produce actionable evidence to support their decisions, leaving analysts to manually investigate flagged websites, which inevitably delays detection and subsequent takedown of these attacks. To address this gap, we present ReDence, a hybrid framework for automated, evidence-grounded scam investigation, detection, and reporting across diverse SE scam categories. ReDence combines two locally deployed, fine-tuned models: a multimodal agentic Inves…
- [ ] **[ProbeAgent: Principled Diagnosis of Agent Failures in Verifiable Environments](https://arxiv.org/abs/2611.26897v1)**
  <!-- aidb:id=arxiv:2611.26897v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Yue Huang, Yuchen Ma, Shuhang Lin, Yuyang Wu, Zixuan Weng, Zixiang Xu, Xiangqi Wang, Yuexing Hao, Yujun Zhou, Yue Zhao, Olexandr Isayev, Stefan Feuerriegel, Xiangliang Zhang
  - Categories: cs.CL, cs.AI
  - Abstract: Improving agents requires discovering where they fail and understanding why. An agent acts over multiple steps in a changing environment, so diagnosing its failures requires more than inspecting the final response of a large language model (LLM). The same unsuccessful outcome can arise from task difficulty or from an error the agent repeats across tasks. We introduce ProbeAgent, an automated framework that discovers agent failures, tests their proposed causes, and identifies shared failure modes. Starting from benchmark tasks, ProbeAgent builds executable tests and validates them using reference solutions, automated checks, and review of the task requirements. For each failed trajectory, it…
- [ ] **[Permitted but Unauthorized: Affordance-Induced Delegated-Scope Violations in Multi-Agent LLM Systems](https://arxiv.org/abs/2611.04086v2)**
  <!-- aidb:id=arxiv:2611.04086v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-02
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Shravya Kanchi
  - Categories: cs.CR
  - Abstract: Multi-agent LLM systems place several agents on shared infrastructure, where each agent holds permissions far broader than the task it is delegated -- so every agent is routinely permitted to act on a peer's resources it was never assigned. We ask: under competitive pressure, what determines whether an agent crosses from its delegated scope into a peer's resources, and can such crossings be enforced away? We study this across eight LLMs in two simulated environments -- a CI/CD release pipeline and a security-operations incident queue -- using a deterministic, no-model-in-the-loop detector over hash-chained, replay-verified logs. In a controlled 2x2x2 factorial over competitive incentive, ca…
  - Comment: v2: adds real-world incident motivation (with primary sources) to the introduction and a full related-work section situating the work among concurrent agent-authorization research; minor consistency edits. Results unchanged from v1. 11 pages, 7 figures, 5 tables. Code and data: https://github.com/s…
- [ ] **[Codetta: High-Capacity, Keyless, and Undetectable Multi-Agent Collusion](https://arxiv.org/abs/2609.28900v3)**
  <!-- aidb:id=arxiv:2609.28900v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-24
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Qi Pang, Virginia Smith, Wenting Zheng
  - Categories: cs.CR, cs.MA
  - Abstract: Multi-agent systems built on large language models (LLMs) are increasingly deployed in high-stakes settings such as finance, healthcare, and software engineering, where agents coordinate through natural-language messages. The same channels, however, let colluding agents exfiltrate confidential information or coordinate unauthorized actions, and steganography can hide such communication inside outputs that look ordinary to an auditor reading the transcript. Existing provably undetectable LLM steganography protocols are not suited to realistic deployments. High-capacity schemes assume a symmetric setting where the receiver can reproduce the sender's output distribution, the state-of-the-art p…
- [ ] **[Efficient Inference for Inverse Reinforcement Learning and Dynamic Discrete Choice Models](https://arxiv.org/abs/2512.24407v3)**
  <!-- aidb:id=arxiv:2512.24407v3 -->
  - Feed: arXiv: agents and RAG
  - Published: 2025-12-30
  - Updated: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Lars van der Laan, Aurélien Bibaut, Nathan Kallus
  - Categories: cs.LG, math.ST
  - Abstract: In many sequential decision-making problems, researchers observe actions but not the rewards that drive behavior, yet wish to evaluate counterfactual policies. Flexible inverse reinforcement learning (IRL) methods accommodate rich reward representations but typically lack valid inference, whereas classical dynamic discrete choice (DDC) methods provide inference under restrictive parametric structure. We develop a semiparametric framework for debiased inverse reinforcement learning in maximum-entropy IRL and Gumbel-shock DDC models. We show that the log behavior policy acts as a pseudo-reward, identifying policy-value differences without point identifying the reward and, under a normalizatio…
  - Comment: 117 pages, including supplementary appendix. Revised theory and added empirical applications to medical care and fertility decisions
- [ ] **[CredLeakBench: Evaluating Credential Leakage and Recovery in LLM Agents](https://arxiv.org/abs/2610.08871v2)**
  <!-- aidb:id=arxiv:2610.08871v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-06
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Rafid Ahmed, Joseph Fioresi, Mubarak Shah, Yuzhang Shang
  - Categories: cs.CR, cs.AI
  - Abstract: Language model agents are increasingly deployed to automate everyday digital chores from managing emails and social media to handling banking and bills allowing users to step away from supervision. However, this capability also exposes sensitive information to phishing. Safe execution requires distinguishing malicious requests from genuine ones without simply refusing to act. Despite its practical importance, this problem remains underexplored and it is unclear whether current agents or existing defenses can achieve it. To study this problem, we first propose CredLeak-Bench, a comprehensive benchmark designed to evaluate how effectively and securely agents automate human workflows when conf…
- [ ] **[Explain Your Code: AI-Based Examination at Class Scale](https://arxiv.org/abs/2611.26836v1)**
  <!-- aidb:id=arxiv:2611.26836v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: David Sarne, Shachar Sagi, Yossi Ben-Zion
  - Categories: cs.HC, cs.CY
  - Abstract: Generative AI has weakened the link between working code and a student's understanding of it. Oral examination, the traditional test of that understanding, does not scale to large courses. We report the full-course deployment of a three-agent AI system that examines students on their own code. The first, the examiner, asks three questions anchored to specific lines of the submission, adapting difficulty to each answer, in a 16-minute text dialogue. The other two grade: a code reviewer that never sees the examination and a grader without direct access to the code. Authorship is assessed separately and is advisory. The system examined 247 students in an operating systems course (three exercis…
- [ ] **[A Scalable Decentralized Event-Triggered Topology-Switching Protocol for Verifiable Safe Control in Multi-Agent Systems](https://arxiv.org/abs/2611.21513v2)**
  <!-- aidb:id=arxiv:2611.21513v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-16
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Amber He Wei, Shiyu Cheng, Andrew Clark, Bruno Sinopoli
  - Categories: eess.SY, math.OC
  - Abstract: This paper develops a decentralized event-triggered topology-switching protocol that allows agents to disconnect from the communication network while preserving state safety and excluding Zeno behavior. We establish a robust barrier function condition that guarantees safety as long as the estimation error remains within a prescribed threshold. Each agent uses locally computable certificates to determine when to connect and disconnect from the network. The certificate construction improves scalability by reducing the complexity of topology-dependent computations from $O(2^N)$ to $O(N)$, where $N$ is the number of agents. We formally prove that the protocol ensures the estimation error does n…
- [ ] **[Bridging Learned Visual Perception and Symbolic Belief-Space Planning via Probabilistic Grounding](https://arxiv.org/abs/2609.16884v2)**
  <!-- aidb:id=arxiv:2609.16884v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-09-15
  - Updated: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Guy Azran, Michael Navat, Sarah Keren
  - Categories: cs.AI, cs.RO
  - Abstract: In partially observable settings, agents must act without full knowledge of the world state and rely on uncertain state-estimation pipelines. Obtaining grounded and verifiable symbolic plans under such uncertainty remains a key challenge. Recent work has integrated Vision-Language Models (VLMs) to bridge perception and symbolic reasoning, following two main paradigms. The first, VLM-as-planner, maps images directly to action sequences, and the second, VLM-as-grounder, grounds observations into symbolic predicates used as the initial state by off-the-shelf planners. Both approaches ignore uncertainty in the planning process, compromising robustness. We introduce a third paradigm, VLM-as-prob…
  - Comment: Proceedings of the 3rd International Conference on Neuro-Symbolic Systems (NeuS), 2026
- [ ] **[AgentArk: Distilling Multi-Agent Intelligence into a Single LLM Agent](https://arxiv.org/abs/2602.03955v4)**
  <!-- aidb:id=arxiv:2602.03955v4 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-02-03
  - Updated: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Yinyi Luo, Yiqiao Jin, Weichen Yu, Mengqi Zhang, Srijan Kumar, Xiaoxiao Li, Weijie Xu, Xin Chen, Jindong Wang
  - Categories: cs.AI, cs.MA
  - Abstract: While large language model (LLM) multi-agent systems achieve superior reasoning performance through iterative debate, practical deployment is limited by their high computational cost and error propagation. This paper proposes AgentArk, a novel framework to distill multi-agent dynamics into the weights of a single model, effectively transforming explicit test-time interactions into implicit model capabilities. This equips a single agent with the intelligence of multi-agent systems while remaining computationally efficient. Specifically, we investigate three hierarchical distillation strategies across various models, tasks, scaling, and scenarios: reasoning-enhanced fine-tuning; trajectory-ba…
  - Comment: Accepted by NeurIPS 2026
- [ ] **[MedicalRSI: Medical Recursive Self-Improving Agents via Clinical Model-Harness Co-Evolution](https://arxiv.org/abs/2611.26806v1)**
  <!-- aidb:id=arxiv:2611.26806v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Ziqing Wang, Hamid Palangi, Lili Zhao, Kaize Ding
  - Categories: cs.CL, cs.AI
  - Abstract: Medical agents built on large language models (LLMs) have advanced rapidly, yet most stay fixed once deployed and do not keep using their experience to improve later attempts. As a result, the same kind of error can recur across patients. To address this, existing self-improvement methods update an agent's weights or its medical harness from its own experience, but their improving strategy stays fixed and never learns which changes actually help, which caps how much the agent can improve. Recursive self-improvement (RSI) instead improves both the agent and its improving strategy. However, achieving RSI for medical agents is challenging, because clinical workflows rarely come with a referenc…
- [ ] **[Incentive Compatible Mechanisms for Sequential Fair Resource Allocation with Private Demands](https://arxiv.org/abs/2611.26800v1)**
  <!-- aidb:id=arxiv:2611.26800v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Ramtin Salamat, Sean R. Sinclair, Seyed M. R. Iravani
  - Categories: cs.GT, math.OC
  - Abstract: We study a strategic variant of the canonical online fair allocation problem, where a planner must sequentially allocate a divisible resource to agents with privately known demands. At each stage, the planner announces an allocation rule, the agent reports their demand, and the planner allocates resources according to the rule and the reported demand. Unlike the standard model, we allow agents to strategically misreport their needs, as can arise in nonprofit settings where demand is self-reported and monetary transfers are unavailable. We characterize the structure of incentive-compatible (IC) allocation rules in this model, and use this to identify conditions under which the optimal mechan…
  - Comment: 26 pages, 4 figures
- [ ] **[ChatAtom: A Multi-Agent LLM System for Molecular Dynamics Simulation and Visualization](https://arxiv.org/abs/2611.26782v1)**
  <!-- aidb:id=arxiv:2611.26782v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Trupti Mohanty, Ming Du, Mitchell A. Wood, Brad L. Boyce, Remi Dingreville, Mathew J. Cherukara
  - Categories: cs.AI
  - Abstract: Molecular dynamics (MD) simulation resolves atomic-scale motion and predicts the structural, mechanical, and dynamic properties of materials, making it cen- tral to materials design and discovery. Yet an MD study requires an expert-driven workflow: designing the simulation, writing reliable input scripts, executing them, and analyzing the results with separate tools. Here we present ChatAtom, a multi-agent large language model system that translates a natural-language request into a complete MD workflow without the user writing input scripts or analysis code. Each agent has a defined responsibility within the workflow. An orchestrator plans the study; the LAMMPS and OVITO agents each use a…
- [ ] **[What Helps Language-Model Agents Review Violent Video? A Controlled Comparison with a Human Evidence Reference](https://arxiv.org/abs/2611.26776v1)**
  <!-- aidb:id=arxiv:2611.26776v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Mohammed El Amine Mokhtari, Matei Mancas, Virginie Vandenbulcke
  - Categories: cs.CL, cs.AI, cs.CV, cs.MM
  - Abstract: Systems that flag violent video for a human operator can now be built from language models without training, by combining perception models and letting a language model decide. We ask how the observations of the perception models should reach the decision, and which evidence matters. On the XD-Violence test set (799 clips) we fix one set of perception agents (video description, object detection, sound tagging, speech recognition and speech tagging) and one reasoning model, and compare three interfaces: messages between agents, a typed evidence graph explored with tools, and flat text read in one pass; and a single audio-visual model given the raw clip. Two annotators provide a human referen…
  - Comment: 17 pages, 1 figure, 12 tables. Code: https://github.com/amine0110/evidence-graph-agents ; project page: https://amine0110.github.io/evidence-graph-agents/
- [ ] **[Self-verifiable LLM-driven science and why it needs human researchers](https://arxiv.org/abs/2611.26754v1)**
  <!-- aidb:id=arxiv:2611.26754v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Michael G. Medvedev, Nikolai V. Krivoshchapov, Stepan N. Ostarkov
  - Categories: physics.chem-ph, cs.AI
  - Abstract: Language models are now used throughout all sciences - for reading literature, extracting numbers from tables and spectra, analyzing data, drafting conclusions - and their answers arrive in the same polished confident tone whether they are right or wrong, so a result has to be re-derived by a human researcher before it can be relied on. The cost of that re-checking, not the ability to generate results, is what currently limits AI-assisted research. In the field of mathematics, this problem is solved by proof assistants like Lean 4 and Coq that let any formal statement and its proof be written down and checked - a perfect match for LLMs, which are now actively used to search for proofs with…
  - Comment: Code: https://github.com/OstarkovSN/verifiable-cyber-science Full agent traces: https://ostarkovsn.github.io/verifiable-cyber-science/traces/
- [ ] **[Auditing Reward Hackability in Code RL Training Environments](https://arxiv.org/abs/2606.16062v2)**
  <!-- aidb:id=arxiv:2606.16062v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-06-14
  - Updated: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Shreshth Rajan
  - Categories: cs.AI, cs.LG
  - Abstract: Code RL rewards a policy for passing a task's tests, so a test suite that accepts a wrong patch trains the wrong behavior. We measure how often open code RL environments accept wrong patches and how reliably hackable tasks can be detected and repaired, checking each claim by execution against the task's gold patch. First, 22.4% of 49 SWE-bench Verified tasks accept a Docker-verified patch that behaves differently from the gold patch, and 57.8% against a stronger attacker. The gold-patch check is necessary: an attacker not shown the gold patch returns it for 31% of its passing "exploits". Second, across 134 public SWE-bench submissions, models pass hackable tasks 28.6 pp more often than task…
  - Comment: 15 pages, 2 figures, 8 tables. v2: every claim re-checked by execution against the gold patch; SWE-bench Verified hackability corrected from 28.6% to 22.4%; adds audits of two public SWE training sets (SWE-smith, R2E-Gym)
- [ ] **[Fully Automated Discovery of Phase Diagrams Using Agentic Large Language Models](https://arxiv.org/abs/2611.26749v1)**
  <!-- aidb:id=arxiv:2611.26749v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Robert Amelung, Maximilian Nägele, Florian Marquardt
  - Categories: cond-mat.stat-mech
  - Abstract: Classifying phases of matter and mapping out phase diagrams are central problems in physics. Recently, machine learning techniques have emerged as promising tools for phase classification, ranging from supervised learning to various unsupervised methods. However, these techniques provide limited qualitative insight into the discovered phases, typically work only for specific system classes, and do not by themselves efficiently map out the phase diagram. Autonomously constructing the phase diagram of a general system purely from measurements, without prior knowledge of the system, while also yielding qualitative understanding of the phases, remains an open task. In this work, we introduce Ph…
  - Comment: 13 pages, 6 figures
- [ ] **[SkillPrivus: Uncovering PRIVacy of USe Harms in Agentic Skills](https://arxiv.org/abs/2611.26747v1)**
  <!-- aidb:id=arxiv:2611.26747v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Mariana Fernandez-Espinosa, Ivoline Ngong, Keerthiram Murugesan, Karthikeyan Natesan Ramamurthy
  - Categories: cs.CL
  - Abstract: Agent skills extend AI assistants through installable instructions and code that can access users' files, accounts, and data. Even when performing their advertised tasks, skills may infer sensitive attributes, retain unnecessary information, or disclose data to unexpected recipients. We study these potential privacy-of-use harms through SkillPrivus, a static audit framework that analyzes skills before installation without executing them. SkillPrivus extracts data operations from code and natural-language instructions, grounds them in source evidence, and adapts Contextual Integrity to assess their appropriateness. Applied to 726 real skills from public marketplaces, 563 of which handle pers…
- [ ] **[A Metamaterial Agentic Swarm: Coordinated Search for Discrete Mechanical Design](https://arxiv.org/abs/2611.26743v1)**
  <!-- aidb:id=arxiv:2611.26743v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Achuth Chandrasekhar, Alexander Zhao, Amir Barati Farimani
  - Categories: cs.CE
  - Abstract: Designing discrete metamaterial assemblies is challenging because local unit-cell choices collectively determine the global elastic response. We present Metamaterial Agentic Swarm, an island-based portfolio of forty specialized numerical search agents for unit-cell selection in a pixel-resolved mechanical cloak. Five cooperating islands each contain eight agents responsible for global sampling, spatial proposals, mutation, learning, recombination, diversity, neighborhood exploration, and polishing. Islands maintain separate parents while exchanging evaluated assignments through an elite archive and recombination. The objective is the relative exterior displacement mismatch on a supplied obs…
- [ ] **[MetaShare: Failure-Aware Collective Self-Improvement for Open-Ended Agents](https://arxiv.org/abs/2610.21887v2)**
  <!-- aidb:id=arxiv:2610.21887v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-10-15
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Vishal Bhutani, Prasang Gupta, Sumanth Chundru, Kevin Paul
  - Categories: cs.MA
  - Abstract: Humans often learn fastest not by repeating success, but by remembering which failures not to repeat. Open-ended self-improving agents can share experience across lineages, as in GEA, or edit their own improvement mechanisms, as in DGM-Hyperagents, yet failed improvement attempts are rarely retained as reusable cross-branch knowledge, and search can collapse onto redundant strategies. We introduce MetaShare, a failure-aware framework that records successful and unsuccessful agent modifications together with signed performance deltas. Before each generation, MetaShare retrieves diverse high-performing strategies alongside high-confidence failures from other lineages, letting agents reuse eff…
  - Comment: 30 pages, 4 figures. Accepted at the NeurIPS 2026 Meta-Agents Workshop. v2: corrected Polyglot 60-task results and implementation details
- [ ] **[MLE Agents: Autonomous ML Engineering in Large-scale Recommendation Systems](https://arxiv.org/abs/2611.23910v2)**
  <!-- aidb:id=arxiv:2611.23910v2 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-18
  - Updated: 2026-11-19
  - Signal: новая версия уже известной arXiv-статьи
  - Topics: agents, rag, research
  - Authors: Matthew Li, Albert Jiongqian Liang, Dilip Raj
  - Categories: cs.AI
  - Abstract: The typical workflow for improving large-scale ranking and recommendation models is slow and tedious: an engineer forms a hypothesis, implements it as a code change, trains a model, and evaluates it both offline and online, often relying on their own intuition and experience along the way. Autonomous LLM agents promise to speed this up by running the loop on their own, but it is still unclear whether they can do this in industry-scale systems rather than on benchmarks or small proxy tasks. We build human-on-the-loop machine learning engineer (MLE) agents that propose, implement, train, and evaluate model changes on large-scale search rankers. Engineers retain control over objective design,…
  - Comment: NeurIPS 2026 AutoMLR Workshop (oral)
- [ ] **[TOUMAII: A 4.5M-Pair Tool-Calling Preference Dataset and Its Source-Agnostic Generator](https://arxiv.org/abs/2611.26722v1)**
  <!-- aidb:id=arxiv:2611.26722v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Moritz Pötzsch, Andrea Gentilini, Lisa Rossgoderer, Tom Osterfeld, Kesava Prasad Sanjivi Arul, Swanand Ravindra Kadhe
  - Categories: cs.AI, cs.CL
  - Abstract: To autonomously execute multi-step tasks, enterprise agents must reliably interact with tools, call APIs, or query databases, making tool-calling a fundamental capability of AI models. Supervised fine-tuning (SFT) optimises for producing the correct call, but never contrasts it with a plausible incorrect one. In an environment where even a minor formatting error can invalidate a call and an incorrect decision can derail the interaction, direct preference optimisation (DPO) targets exactly this contrast. DPO, therefore, requires preference pairs rather than plain demonstrations. For tool-calling, such data, especially in realistic multi-turn settings, remains extremely scarce. To address thi…
  - Comment: Accepted to the 2nd Workshop on Agentic AI Benchmarks and Applications for Enterprise Tasks (AABA4ET) at NeurIPS 2026. 27 pages, including 5 pages of main text, references, and appendices; 17 figures and 7 tables. Code: https://github.com/tum-ai/toumaii-gen. Datasets: https://huggingface.co/collect…
- [ ] **[Coherence by Construction: Synthesizing CTI Knowledge Graphs and the Formal Limits of Coherence Validation](https://arxiv.org/abs/2611.26717v1)**
  <!-- aidb:id=arxiv:2611.26717v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Tanzimul Alam Fahim, Mohammad Arif Hossain
  - Categories: cs.AI
  - Abstract: Synthesizing relational training data such as knowledge graphs with a large language model typically emits structured objects one at a time, which keeps each object valid but leaves the relationships between them ungrounded. We study an alternative paradigm, generation by simulation: rather than describing a relational artifact, we simulate a process that produces it and take the artifact to be its causal record. Language-model agents propose intent and a deterministic referee resolves outcomes against an explicit world model, so a relation is emitted only when the event it represents occurs, making coherence a property of construction. We instantiate the paradigm for cyber threat intellige…
  - Comment: 21 pages, 5 figures. Includes supplementary material (Sections S-I through S-X)
- [ ] **[Federated KPI Aggregation with Local Privacy Constraints and Coordinated OLAP Roll-Ups](https://arxiv.org/abs/2611.26709v1)**
  <!-- aidb:id=arxiv:2611.26709v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Felix Härer
  - Categories: cs.DB, cs.MA
  - Abstract: Cross-organizational KPI analysis can require aggregated results from independently administered data warehouses without centralizing detailed records. To limit disclosure from small local groups, a site can require a minimum number of contributing records before releasing a KPI value for a group. If each site applies this rule independently, different local contributions may be suppressed and the combined KPI can become incomplete. This paper investigates whether OLAP granularity can be coordinated before local query results are released so that all sites satisfy their local minimum-cohort rules and contribute at the same analytical level. The proposed method selects the least-generalized…
  - Comment: Presented at 2026 13th International Conference on Soft Computing & Machine Intelligence (ISCMI 2026), November 2026. Accepted for publication in the conference proceedings. Official publication forthcoming
- [ ] **[Agent-guided construction of Feynman integral bases](https://arxiv.org/abs/2611.26688v1)**
  <!-- aidb:id=arxiv:2611.26688v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Pau Petit Rosas, William J. Torres Bobadilla
  - Categories: hep-ph, hep-th
  - Abstract: Finding bases of Feynman integrals whose differential equations are suitable for phenomenology is a remarkably verifiable task. We exploit this to design two \emph{skills} with which Claude Opus~5.5 produces novel results autonomously, working for several days. For a two-loop five-point family (with two masses and 18 elliptic sectors) and a two-loop superfamily for the radiative jet function with a K3 sector, the agent finds bases whose differential equations are free of poles in the dimensional regulator $\varepsilon$ and at most quadratic in it, and takes the jet-function one to $\varepsilon$-factorized form.
- [ ] **[How developers split roles among them and a coding agent and what "collaboration" means](https://arxiv.org/abs/2611.26668v1)**
  <!-- aidb:id=arxiv:2611.26668v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Linus Ververs, Helya Dadkhah, Lutz Prechelt
  - Categories: cs.SE
  - Abstract: Background: Coding agents such as Claude Code become more and more competent, so that their role in the development process can grow. Objective: How do developers characterize the role-split between them and their agent? How would they ideally want to collaborate with their agent? Methods: We perform a 3-step, mixed-methods study. We apply qualitative open coding to 2025 early adopters' blog articles; perform a quantitative survey of 2026 practitioners; develop and apply a method for coding-agent-supported open coding of survey freetext responses. Results: The 2025 practitioners have the agent work in supporting roles only. Accountability was firmly human. In 2026, both are fundamentally st…
  - Comment: 32 pages (plus 27 pages of appendices), 4 figures, 10 tables
- [ ] **[Adding One More Agent: How AI Team Size and Formation Shape Productivity and Diversity in Human-AI Brainstorming Teams](https://arxiv.org/abs/2611.26663v1)**
  <!-- aidb:id=arxiv:2611.26663v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-11-19
  - Topics: agents, rag, research
  - Authors: Rong-Ching Chang, Hao-Chuan Wang
  - Categories: cs.AI, cs.CL
  - Abstract: Generative AI has improved individual productivity, but whether adding a plurality of AI partners helps or hurts remains open. We crossed AI partnership (one versus two) with behavioral formation (calibrated to average human behavior versus customized by the participant) in a brainstorming experiment ($N$=168) with human-human dyads as reference. Two-AI rooms posted more ideas to the shared board, but human-authored ideas dropped substantially. With one AI partner, formation mattered: humans paired with an average-calibrated AI posted more than any other condition. With two, this effect vanished. Humans continued talking but converted fewer ideas into board posts. AI social talk predicted m…

## Suppressed duplicates

937 уже встречавшихся записей сохранены в `manifest.json`, но не требуют повторного triage.

## После triage

Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.
