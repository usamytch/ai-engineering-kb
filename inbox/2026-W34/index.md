# Weekly discovery — 2026-W34

> Это очередь решений, а не склад статей. Полные HTML/PDF/TeX скачиваются только для `[n]` и `[r]`.
>
> `[d]` drop · `[w]` watch · `[n]` deep note · `[r]` deep review · `[x]` обработано.

Сгенерировано: 2026-08-19T17:46:48+00:00

## Кандидаты

- [ ] **[v0.22.0](https://github.com/openai/openai-agents-python/releases/tag/v0.22.0)**
  <!-- aidb:id=url:52d7fe5e2f70c9ee2258 -->
  - Feed: OpenAI Agents SDK releases
  - Published: 2026-08-19
  - Topics: agents, sdk
  - Authors: seratch
- [ ] **[Multi-Agent AI System for Radiology Report Structuring and Quality Assurance with Independent Radiologist Evaluation](https://arxiv.org/abs/2608.18072v1)**
  <!-- aidb:id=arxiv:2608.18072v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Iryna Hartsock, Cesar Lam, Christopher Otteni, Aliya Qayyum, Robert Gatenby, Cyrillo Araujo, Ghulam Rasool
  - Categories: cs.CL
  - Abstract: Purpose: To develop and evaluate a locally deployed multi-agent AI system for radiology report structuring and quality assurance. Materials and Methods: This retrospective study included 638 radiology reports from CT examinations of the chest, abdomen, and pelvis dictated by 15 board-certified radiologists in 2023 and 2024. A multi-agent AI pipeline was developed to perform report structuring and quality assurance (QA). The system structured the report into standardized anatomical sections at the sentence level using regex rules and local large language models. It also detected mismatches between the Findings and Impression sections, or within sections; gender-anatomy conflicts; and undocum…
  - Comment: 14 pages, 2 figures, 4 tables
- [ ] **[Planning Against Learning in Rank-1 Games](https://arxiv.org/abs/2608.18067v1)**
  <!-- aidb:id=arxiv:2608.18067v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: William Overman
  - Categories: cs.GT
  - Abstract: Learning algorithms are often used to make decisions in repeated multi-agent environments. When another player understands how a learner adapts from past experience, that player can plan strategically across rounds to influence the learner's future behavior. Recent work shows that optimizing against Replicator Dynamics, the continuous-time analogue of Multiplicative Weights Update, is tractable in zero-sum games but can be hard in unrestricted general-sum games. We study the first structured class beyond zero sum: bimatrix games satisfying $\text{rank}(A+B)=1$, for which Nash equilibria can be computed in polynomial time. Our main result shows that this equilibrium tractability does not ext…
- [ ] **[On the Fragility of Self-Improving Agents: Variance, Task Order, and Underspecification](https://arxiv.org/abs/2608.18066v1)**
  <!-- aidb:id=arxiv:2608.18066v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Qinyuan Ye, Yu Li, Yada Pruksachatkun, Jiaxin Zhang, Chien-Sheng Wu
  - Categories: cs.AI, cs.CL, cs.LG
  - Abstract: Memory-based self-improving agents--those that learn from an online stream of tasks and improve over time by maintaining a textual memory bank--have shown great promise in recent literature. However, the reliability aspects of these methods have been critically overlooked. In this work, we conduct a comprehensive re-evaluation of two memory-based methods, broadening the scope of evaluation along two axes: (1) including multiple runs to quantify variance, and (2) randomly shuffling the tasks to investigate the effect of task order. Through these experiments, we make two observations that expose the fragility of current methods: First, agent evaluation is inherently noisy in complex environme…
  - Comment: Code: https://github.com/SalesforceAIResearch/self-improve-fragility Data: https://huggingface.co/datasets/Salesforce/self-improve-fragility
- [ ] **[Delegation Asymmetry in Agentic Recommender Systems: Measuring Two-Sided Receptivity in Online Dating](https://arxiv.org/abs/2608.18058v1)**
  <!-- aidb:id=arxiv:2608.18058v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Daria Leshchikova, Valentina V. Kuskova, Dmitry Zaytsev, Valerii Klimov
  - Categories: cs.AI
  - Abstract: Autonomous LLM agents that converse on a user's behalf are an emerging design pattern in matching platforms, yet their viability depends on a condition rarely examined: users must accept not only delegating conversation to an agent, but also receiving agent-mediated communication from others. We study this condition using two large-scale surveys of active users of a major dating platform (N=2,894 on generative profile features; N=2,617 on autonomous conversational agents, fielded in two languages). We develop a latent-variable measurement model of agent receptivity based on graded response models with latent regression, and show via model comparison that willingness to send and willingness…
- [ ] **[StagedWorkspace: A Versioned Workspace for Knowledge-Work Agents](https://arxiv.org/abs/2608.18050v1)**
  <!-- aidb:id=arxiv:2608.18050v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Yining Hua, Hongbin Na, Yifan Zhou, Akshay Kalose, Cyrus Ayubcha, Levi Lian
  - Categories: cs.AI
  - Abstract: AI agents increasingly perform knowledge work (i.e., produce and modify persistent digital artifacts such as code repositories, documents, spreadsheets, slides, reports), yet the parsed views they search, the native files they edit, the changes they review, and the artifacts they submit can refer to different versions of the same work product. We formulate this as a workspace-state contract: every view should be explicitly tied to a version of the evolving workspace state. Coding agents partly address this need through repository contracts for search, diffs, and tests, whereas an analogous contract is less explicit for PDFs, spreadsheets, slides, notebooks, and mixed-format project folders.…
  - Comment: Under Review
- [ ] **[Language Has Two Parameters: Narrative-Induced Semantic Plasticity and Phase-Sensitive Interpretation](https://arxiv.org/abs/2608.18041v1)**
  <!-- aidb:id=arxiv:2608.18041v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Hollis Robbins
  - Categories: cs.CL
  - Abstract: Language has two parameters. Count how often words occur together and you estimate amplitude, the strength of association. Word embeddings and attention weights refine that count, which sums every writer in the corpus together. This paper claims a second parameter, phase, which signed weights learned from a corpus do not supply. Phase exists only between meanings: it determines how coactivated meanings combine, and it can reverse what a meaning contributes while that meaning stays fully present. A speaker can set phase in the signal through linguistic form; encounters install phase relations and history distributes them. Population averaging deletes history-indexed phase: agent-deindexed co…
  - Comment: 23 pages; 0 figuresCC
- [ ] **[Deep Academic Survey: Stateful Agentic Closed-Loop Paradigm for Academic Survey Automation](https://arxiv.org/abs/2608.18034v1)**
  <!-- aidb:id=arxiv:2608.18034v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Zhikai Xu, Zhucun Xue, Teng Hu, Yabiao Wang, Yong Liu, Jiangning Zhang
  - Categories: cs.CV
  - Abstract: Academic surveys play a central role in organizing rapidly expanding scholarly literature, yet their construction requires extensive paper analysis, coherent knowledge organization, fine-grained citation support, and reliable manuscript assembly. Existing Deep Research and automated survey generation systems address parts of this process, but typically do not coordinate paper understanding, literature organization, evidence-grounded drafting, and manuscript validation through a shared, revisable state. We introduce DAS, a stateful agentic framework for generating publication-oriented academic surveys. Its key idea is to separate reusable paper analysis from topic-specific manuscript constru…
  - Comment: Project page: https://zhikaixu24.github.io/projects/DAS/ | Code: https://github.com/ZhikaiXu24/DAS | Data: https://huggingface.co/datasets/ZhikaiXu24/DAS-2M
- [ ] **[Policy-Invariant Reward Shaping from LLM Feedback: A Framework for Hybrid RL Agents](https://arxiv.org/abs/2608.18008v1)**
  <!-- aidb:id=arxiv:2608.18008v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Christophe D. Hounwanou, John Emeka Eze, Yaé U. Gaba
  - Categories: cs.LG, cs.AI
  - Abstract: Combining large language models with reinforcement learning is increasingly explored, yet the theoretical status of LLM-derived reward signals is often left implicit. We formalize the hybrid LLM-planner and RL-controller architecture as a Goal-Augmented Markov Decision Process and show that when the LLM per-state progress score is used as a bounded potential function, the resulting shaping term preserves the optimal policy set even when the LLM scores are inaccurate. This guarantee is stronger than what general LLM-as-reward approaches provide. We verify the result numerically on a small MDP under four potential configurations, including an adversarial one scaled to twenty times the base re…
  - Comment: 14 pages
- [ ] **[aDSL: Agentic 3D Creation via Joint Agent-Program Design](https://arxiv.org/abs/2608.17975v1)**
  <!-- aidb:id=arxiv:2608.17975v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Rui-Huan Wang, Si-Tong Wei, Jia-Qi He, Heng-Yi Wei, Baoquan Chen, Peng-Shuai Wang
  - Categories: cs.GR, cs.CV
  - Abstract: Programmatic representations provide a compelling paradigm for 3D content creation, enabling fine-grained edits, interpretability, and explicit structural control. Yet, agentic workflows that rely on large language models (LLMs) to author 3D programs remain brittle, often failing to translate high-level intent into consistent low-level geometry. We attribute this fragility to a mismatch between existing programmatic interfaces and the reasoning strengths of LLMs, which favor semantic structure and spatial relations over fragile numeric choices. In this paper, we jointly design an Agent-centric Domain-Specific Language (aDSL) and a role-specialized multi-agent system to close this gap. aDSL…
- [ ] **[Quo Vadis? Scientific Discovery in the Age of Artificial Intelligence](https://arxiv.org/abs/2608.17970v1)**
  <!-- aidb:id=arxiv:2608.17970v1 -->
  - Feed: arXiv: agents and RAG
  - Published: 2026-08-18
  - Topics: agents, rag, research
  - Authors: Petr O. Jedlicka
  - Categories: cs.CY
  - Abstract: This paper examines the growing role of AI in scientific discovery. It first surveys the rapid rise of AI capabilities, especially in reasoning, abstraction, planning, and long-horizon task execution, before turning to scientometric evidence of AI's diffusion across the sciences. It then proposes a typology of AI systems used in research, ranging from specialized scientific AI through scientific AI assistants and agents to hybrid experimental systems that combine computation and physical experimentation. On this basis, it offers a selective overview of recent achievements in mathematics and computer science, physics, chemistry, the life sciences, and the behavioural and social sciences. It…
  - DOI: 10.46938/tv.2026.728
  - Comment: To be published in Theory of Science
- [ ] **[v1.39.0](https://github.com/google/adk-python/releases/tag/v1.39.0)**
  <!-- aidb:id=url:dc009bcabb091ae6098c -->
  - Feed: Google ADK Python releases
  - Published: 2026-08-17
  - Topics: agents, sdk
  - Authors: wuliang229
- [ ] **[v2.7.1](https://github.com/google/adk-python/releases/tag/v2.7.1)**
  <!-- aidb:id=url:7ac2ce458271723bdedb -->
  - Feed: Google ADK Python releases
  - Published: 2026-08-17
  - Topics: agents, sdk
  - Authors: GWeale
- [ ] **[v0.21.1](https://github.com/openai/openai-agents-python/releases/tag/v0.21.1)**
  <!-- aidb:id=url:4d3f8d8c8b307f670217 -->
  - Feed: OpenAI Agents SDK releases
  - Published: 2026-08-16
  - Topics: agents, sdk
  - Authors: seratch
- [ ] **[v0.21.0](https://github.com/openai/openai-agents-python/releases/tag/v0.21.0)**
  <!-- aidb:id=url:ba7442a9a2dcb32b5d26 -->
  - Feed: OpenAI Agents SDK releases
  - Published: 2026-08-15
  - Topics: agents, sdk
  - Authors: seratch
- [ ] **[v2.7.0](https://github.com/google/adk-python/releases/tag/v2.7.0)**
  <!-- aidb:id=url:3023bb5371ab7054d5db -->
  - Feed: Google ADK Python releases
  - Published: 2026-08-13
  - Topics: agents, sdk
  - Authors: GWeale

## После triage

Запустить `make week-process`: выбранные arXiv `[n]`/`[r]` пройдут full-text ingest, extraction, deep summary и evidence checks. Перенос в основную KB остаётся ручным решением.
