# Memorizing Who, Knowing How: Benchmarking Personal and Procedural Memory for Persistent Assistants

## Executive summary

PraxisMemBench evaluates evolving personal facts, reusable procedures, and their associations across synthetic persistent-assistant trajectories. Separate personal and procedural stores lose the relations needed for user-conditioned action; relation-related failures become more prevalent later in a trajectory. PraxisMem learns joint memory using location-aware GRPO and residual-routed on-policy self-distillation. It outperforms the tested non-oracle systems, with controlled ablations supporting placement-aware rewards and selective routing. The evidence includes detailed diagnostics and judge auditing, but comes from fictional personas, mock applications, one complete run per method, model-based grading, and privileged supervision tied to an authored memory organization. Headline success is memory-conditioned, not strict end-to-end task completion; baselines are harness adaptations, not evaluations of entire products.

## Problem

**Statement.** Persistent assistants must remember both who the user is and how to act, including changing associations that determine which procedure is applicable. Existing evaluations tend to isolate factual personal memory or procedural execution and therefore do not adequately test their interaction over long-running, stateful use.

**Why it matters.** A system may retrieve individually plausible facts and procedures yet still perform the wrong action if it loses their operative relation, uses stale personal state, or fails to reorganize memory after repeated updates. This is consequential for personalized actions across communication, finance, travel, health, and other stateful domains.

**Scope.** The paper studies memory maintenance and use in synthetic, persistent harness trajectories covering Tool, Artifact, and Memory QA sessions. It evaluates Scheduled and Autonomous access, but does not establish behavior with real users, real accounts, or unconstrained production applications.

## Method

PraxisMemBench constructs temporally ordered persona trajectories from canonical personal memory, procedural memory, association structure, and application state. Accepted sessions disclose or change memory, instantiate measurable downstream dependencies, and update the canonical state only after independent validation. Evaluation is free-running: realized memory and application state carry forward without repair. PraxisMem uses a structured Markdown store and trains one memory-manager policy for Update and Retrieval. During training, canonical joint states provide privileged targets. Location-aware GRPO rewards semantic coverage and correct placement, while dynamic residual-routed OPSD activates only for criteria missed by all rollouts and only at chunks where the defect persists. Deployment does not receive the privileged state.

### Key components

- PraxisMemBench: separate training and held-out test pools, persistent trajectories, three task families, and both Scheduled and Autonomous memory access.
- Canonical sequential construction: personal events, procedures, application state, fixtures, reference executions, and gold checks evolve session by session.
- Free-running evaluation: memory and application errors propagate to later sessions rather than being reset to canonical state.
- Structured memory: USER.md, MEMORY.md, dated event files, domain-specific SKILL.md files, and a raw interaction archive.
- Location-aware GRPO: state matching rewards both required content and its intended organizational location, with penalties for redundant or misplaced units.
- Dynamic residual-routed OPSD: a privileged self-teacher observes current-versus-target discrepancies, with criterion-level and chunk-level gates limiting token supervision.
- Mixed grading: deterministic checks for tool and artifact outcomes, plus LLM judging for semantic memory requirements and Memory QA.

### Assumptions

- Canonical authored memory states are treated as useful privileged supervision, although the paper acknowledges that they are one valid organization rather than uniquely correct.
- Correct placement under the selected Markdown schema is assumed to be a meaningful proxy for long-term maintainability and joint recoverability.
- Synthetic personas, generated changes, mock applications, and offline tools are assumed to preserve the central difficulty of persistent personal assistance.
- The fixed task agent, user simulator, judge, budgets, and harness configurations are assumed to permit meaningful comparisons among memory methods.
- Session-level pooled success is treated as the primary diagnostic of memory-conditioned performance, distinct from strict end-to-end success.

## Main claims

- **The benchmark explicitly couples personal and procedural memory in persistent executable trajectories, with later tasks omitting historical conditions that the memory system must recover.**
  - Evidence: [b00026-47017e4921] “Crucially, in later dependent sessions, these details are omitted from the public request”; [b00034-0cf90fed82] “303 of 360 executable tasks require joint memory”
- **Maintaining personal and procedural memory as independent stores is insufficient when the procedure must be conditioned on current personal context.**
  - Evidence: [b00079-33345fce2c] “DualMem performs progressively worse from personal-only (84.7%) and procedural-only (84.5%) tasks to Coordinated tasks (80.1%)”; [b00079-33345fce2c] “and drops further on Interdependent tasks (77.9%).”
- **Persistent interaction changes the dominant failure mode from missing access toward broken or competing personal–procedural relations.**
  - Evidence: [b00085-7413a15769] “Access failures fall from 40.2% in early sessions to 27.1% in late sessions”; [b00085-7413a15769] “relation-related failures rise from 59.8% to 72.9%”
- **PraxisMem learns both memory content and its organization by combining placement-sensitive reinforcement learning with selectively routed privileged distillation.**
  - Evidence: [b00038-f5be51249b] “location-aware GRPO learns what information should be maintained and where it should be organized”; [b00038-f5be51249b] “dynamic residual-routed OPSD identifies when unresolved defects persist along the update trajectory”

## Results

- **PraxisMem obtains 40.78% overall Session SR, versus 20.60% for Claude Code native memory; this is nearly a twofold score, but the absolute success rate remains below half of eligible sessions.**
  - Context: Overall pooled Scheduled-setting result. The paper’s overall Session SR is memory-conditioned rather than strict end-to-end success, and the complete test split was run once per method.
  - Evidence: [b00398-4a9addc57a] “Claude Code 16.99 449.18K 6.72K 140.76 0.190 – 20.60”; [b00398-4a9addc57a] “PraxisMem (Ours) 7.47 248.87K 5.16K 88.91 0.108 0.122 40.78”; [b00304-9b8e09f9da] “Session SR is a diagnostic, memory-conditioned measure and does not correspond to Strict E2E Session SR”
- **Separate-store DualMem declines from 84.7% on personal-only and 84.5% on procedural-only tasks to 80.1% on Coordinated and 77.9% on Interdependent tasks.**
  - Context: Controlled diagnostic using Combined Completion over Tool Step SR and Artifact Assertion. This supports the relation-maintenance hypothesis more directly than the aggregate leaderboard, although it does not isolate every difference between DualMem and a learned unified manager.
  - Evidence: [b00079-33345fce2c] “personal-only (84.7%) and procedural-only (84.5%) tasks to Coordinated tasks (80.1%)”; [b00079-33345fce2c] “and drops further on Interdependent tasks (77.9%).”
- **In audited failures, relation-related errors rise from 59.8% in early sessions to 72.9% in late sessions, while access failures fall from 40.2% to 27.1%.**
  - Context: Failure audit for MemOS, Hermes, and PraxisMem. The trend supports a continual-organization problem but is not shown to generalize to every baseline or real deployment.
  - Evidence: [b00085-7413a15769] “Access failures fall from 40.2% in early sessions to 27.1% in late sessions”; [b00085-7413a15769] “relation-related failures rise from 59.8% to 72.9%”
- **On eight fixed trajectories, the progressive ablation improves Combined Completion from 66.2% to 83.4%, Interdependent Completion from 54.9% to 82.1%, and Avg SR from 23.5% to 43.1%.**
  - Context: The variants share training data, base model, store format, and protocol. The monotonic progression supports the placement and routing mechanisms, but the subset is small and selected as the first eight trajectories rather than through repeated random subsets.
  - Evidence: [b00088-fcc41b8326] “Combined Completion increases from 66.2% under content-only GRPO to 83.4% with full PraxisMem”; [b00088-fcc41b8326] “Interdependent Completion rises more substantially from 54.9% to 82.1%”; [b00088-fcc41b8326] “Avg SR similarly improves from 23.5% to 43.1%.”
- **Autonomous access remains substantially harder: PraxisMem leads non-oracle methods with Tool, Memory QA, and Artifact Session SR of 23.00%, 22.22%, and 31.64%, while advanced systems invoke retrieval in only 57.3% of sessions on average.**
  - Context: Requests are less specified and the task agent must decide whether, when, and how to query memory. This exposes a major remaining bottleneck not solved by better memory organization alone.
  - Evidence: [b00359-f8f7d73f62] “The advanced memory systems have an average retrieval-call rate of 57.3%.”; [b00359-f8f7d73f62] “PraxisMem attains the strongest non-oracle Session SR for Tool, Memory QA, and Artifact tasks at 23.00%, 22.22%, and 31.64%”

## Experimental evaluation

### Datasets

- PraxisMemBench contains separate training and test splits, each with 20 users and 500 sessions across 20 MCP-accessible domains; the two splits cover 40 domains in total and the test setting contains 2,185 memory dependencies.
  - Evidence: [b00034-0cf90fed82] “each with 20 users and 500 sessions spanning 20 MCP-accessible application domains (40 in total)”; [b00034-0cf90fed82] “covering 2,185 memory dependencies.”
- Each trajectory contains 25 temporally ordered sessions, with observed histories averaging an estimated 663.6K tokens across selected harness runs.
  - Evidence: [b00283-a74556167f] “PraxisMemBench uses 25 temporally ordered sessions per trajectory.”; [b00283-a74556167f] “averages an estimated 663.6K tokens per trajectory (606.7K–742.7K).”
- The data are synthetic: personas are fictional, interaction trajectories are generated, and tools execute in isolated benchmark applications.
  - Evidence: [b00094-b73970de7e] “constructed from fictional personas and synthetic interaction trajectories”; [b00094-b73970de7e] “All tool interactions are executed in isolated benchmark applications”

### Baselines

- Diagnostic controls: Oracle Memory, Long Context, and DualMem.
  - Evidence: [b00071-9ad864fb41] “Diagnostic controls include Oracle Memory, Long Context, and DualMem”
- Retrieval and harness-native baselines: BM25, embedding RAG, OpenClaw, Hermes, and Claude Code.
  - Evidence: [b00071-9ad864fb41] “Retrieval baselines include BM25 and embedding RAG. Harness-style baselines include OpenClaw, Hermes, and Claude Code.”
- Advanced and learned systems: Mem0, Zep, A-Mem, ReMe, MemOS, Memory-R2, and PraxisMem.
  - Evidence: [b00071-9ad864fb41] “Advanced memory systems include Mem0, Zep, A-Mem, ReMe, MemOS, Memory-R2, and PraxisMem”

### Metrics

- Tool tasks report personal-memory, procedural-memory, Tool Step SR, and Session SR; Artifact tasks use personal-memory, procedural-memory, Artifact Assert, and Session SR.
  - Evidence: [b00032-0a23aa4616] “Tool and Artifact tasks report personal-memory, procedural-memory, and execution-level scores (Tool Step SR or Artifact Assert)”
- Memory QA reports Precision, Recall, F1, and Session SR.
  - Evidence: [b00032-0a23aa4616] “Memory QA isolates retrieval quality through Precision, Recall, and F1. All three families additionally report Session SR.”
- Correct-location Recall and location-aware F-state diagnose whether required content is stored in the intended organization.
  - Evidence: [b00339-d2dfd61cdf] “Correct-location Recall measures whether required information is maintained at the intended memory location”; [b00339-d2dfd61cdf] “location-aware F-state jointly reflects memory-state correctness and placement quality.”
- Semantic judge reliability is assessed with quadratic weighted Cohen’s κ against adjudicated expert annotations.
  - Evidence: [b00309-fac396d4af] “We compute quadratic weighted Cohen’s κ (QWK) on their independent ratings and adjudicate disagreements”

### Ablations

- Four progressive variants compare content-only GRPO, a location-aware reward, criterion-routed OPSD, and full criterion-by-chunk PraxisMem.
  - Evidence: [b00080-f7f37795e7] “Content-only GRPO 66.2 54.9 23.5 + Location-aware reward 73.6 66.5 29.0”; [b00080-f7f37795e7] “+ Criterion-routed OPSD 76.9 72.1 32.7 PraxisMem (criterion×chunk) 83.4 82.1 43.1”
- The ablation uses eight fixed test trajectories, with all variants sharing training data, base model, store format, and evaluation protocol.
  - Evidence: [b00337-1003f5e624] “uses the first eight trajectories in the fixed test-set order.”; [b00337-1003f5e624] “All variants share the same training data, base model, memory-store format, and evaluation protocol.”
- Backbone sensitivity is tested with three task LLMs while holding the memory method and other evaluation components fixed.
  - Evidence: [b00386-bcb2ac2663] “with three task LLMs: Qwen3.7-Plus, GLM-5.2, and DeepSeek-V4-Pro.”; [b00386-bcb2ac2663] “All other settings, including the memory method, user simulator, judge, verifier, and trajectory subset, remain unchanged.”

### Negative results

- Even gold memory does not solve executable tasks: Oracle Tool Session SR is 83.90% and Artifact Session SR is 77.42%, demonstrating substantial post-retrieval grounding and execution error.
  - Evidence: [b00353-d78ad0937d] “Tool Session SR rises from 83.90% to 94.10%”; [b00353-d78ad0937d] “Artifact Session SR increases from 77.42% to 95.65%.”
- Long-range evidence degrades for several systems: relative to evidence within one week, later-bucket means fall by 30.0 points for Long Context, 17.9 for Embedding RAG, and 15.3 for MemOS.
  - Evidence: [b00084-6f1bb4943a] “drops by 30.0 points for Long Context, 17.9 for Embedding RAG, and 15.3 for MemOS.”
- Autonomous requests sharply reduce complete-session success even when step completion remains much higher.
  - Evidence: [b00358-bc4cb92064] “Hermes falls from 26.34% to 10.42% Tool Session SR”; [b00358-bc4cb92064] “Hermes and MemOS still reach 62.58% and 62.80% Tool Step SR, yet complete few sessions.”
- PraxisMem still exhibits asymmetric update failures in which personal context is stored but associated procedural rules remain only in raw evidence.
  - Evidence: [b00383-505546709a] “Personal context from the source session is stored in USER.md and events/2026-09-07.md”; [b00383-505546709a] “two disclosed procedural rules remain only in raw/”


## Limitations

- External validity is limited because the benchmark uses fictional personas, synthetic trajectories, and isolated mock applications rather than real users and production systems.
  - Evidence: [b00094-b73970de7e] “constructed from fictional personas and synthetic interaction trajectories”; [b00094-b73970de7e] “no real accounts, payments, communications, or other external actions are involved.”
- Synthetic personas and generated events may encode cultural, demographic, or behavioral biases and are not claimed to represent real populations.
  - Evidence: [b00094-b73970de7e] “may inherit cultural, demographic, or behavioral biases”; [b00094-b73970de7e] “should not be interpreted as representative of real users.”
- Reported full-test comparisons lack repeated-run uncertainty: the authors report one complete-test-split inference run per method.
  - Evidence: [b00321-a038efd7c6] “We report one complete-test-split inference run per method.”
- Semantic evaluation remains model-dependent. GLM-5 agreement with adjudicated experts is below human–human agreement, especially leaving room for rubric sensitivity.
  - Evidence: [b00310-1ec6787f78] “the two expert annotators reach an overall QWK of 0.934. GLM-5 reaches 0.793”; [b00310-1ec6787f78] “partial coverage of memory-bearing open-text arguments leaves more room for rubric interpretation.”
- The main Session SR is not strict end-to-end success, so headline values should not be read as the rate of fully correct task execution.
  - Evidence: [b00304-9b8e09f9da] “does not correspond to Strict E2E Session SR, which additionally requires all successful task execution and outcomes.”
- The strongest controlled training ablation covers only the first eight fixed test trajectories, limiting statistical confidence and sensitivity to trajectory selection.
  - Evidence: [b00337-1003f5e624] “uses the first eight trajectories in the fixed test-set order.”
- Training targets embody one selected Markdown organization rather than a uniquely correct memory state, which may couple gains to the authored schema and placement contract.
  - Evidence: [b00330-0b717d8829] “This reference is one valid organization under our chosen schema, rather than a benchmark-provided or uniquely correct memory state.”

## Reproducibility

**Status:** partial

Documentation is strong and unusually specific, including versions, budgets, training settings, prompts, and validation procedures. Reproducibility is nevertheless partial because the essential executable artifacts and checkpoint are described as future releases, and stochastic uncertainty is not quantified.

**Available artifacts**

- Detailed benchmark construction, evaluation, implementation, training, and prompt descriptions are stated to be included in the paper and appendices.
- Model and harness versions, budgets, inference settings, hardware, training configuration, prompts, grading procedures, and judge audit are reported in the supplied document.
- The authors state an intention to release fixed splits, fixtures, SOPs, gold annotations, verifiers, construction and evaluation code, baseline configurations, prompts, training code, and a checkpoint.

**Missing pieces**

- The supplied material provides a release promise, not evidence that the benchmark, code, checkpoint, fixtures, and annotations are already publicly available.
- No repeated full-test runs, confidence intervals, or random-seed variance are reported.
- The visible blocks do not establish independent replication by an external group.

## AIDB assessment

- Novelty: High conceptual and benchmark novelty: the paper makes evolving personal–procedural associations, not merely separate memory types, the object of persistent evaluation. The residual-routed, location-aware training formulation is also a substantive method contribution.
- Usefulness: High for researchers building persistent agents, memory managers, harness evaluations, or long-horizon personalization. The benchmark’s free-running state, diagnostic task families, relation-failure taxonomy, autonomous setting, and cost reporting provide several useful evaluation lenses. Production conclusions should remain provisional until tested with real users and less authored memory organizations.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled ablation, broad baseline suite, chronological evaluation, failure audit, judge audit, and implementation detail make this a strong research artifact. Confidence stops short of high because headline comparisons use one full run, the benchmark is synthetic, the primary success metric is not strict end-to-end completion, and promised release artifacts are not shown as currently available.

## Uncertainties

- **It is unclear how much of PraxisMem’s gain transfers to memory representations whose valid organization differs substantially from the authored Markdown placement contract.** — The method claims to learn maintainable organization rather than merely fit one schema; cross-representation evidence would distinguish the general principle from schema-specific supervision.
  - Evidence: [b00142-6995346a09] “The Markdown schema is one implementation of this structured state”; [b00330-0b717d8829] “This reference is one valid organization under our chosen schema”
- **The variance of method rankings and effect sizes across stochastic runs is unknown.** — A single full-test run cannot reveal whether score differences are stable under sampling, simulator variation, or memory-update randomness.
  - Evidence: [b00321-a038efd7c6] “We report one complete-test-split inference run per method.”
- **The extent to which synthetic user changes and authored SOP dependencies match real longitudinal assistance is unresolved.** — Real users disclose information irregularly, contradict themselves, request deletion, and impose privacy constraints that may alter both memory maintenance and retrieval behavior.
  - Evidence: [b00094-b73970de7e] “Synthetic personas and LLM-generated events may inherit cultural, demographic, or behavioral biases”; [b00094-b73970de7e] “should not be interpreted as representative of real users.”
- **Headline Session SR may overstate practical task reliability if readers conflate it with complete end-to-end execution.** — Deployment decisions require strict success, safety, and correct external effects, whereas the reported metric is explicitly memory-conditioned.
  - Evidence: [b00304-9b8e09f9da] “Session SR is a diagnostic, memory-conditioned measure”; [b00304-9b8e09f9da] “does not correspond to Strict E2E Session SR”

## Open questions

- Will PraxisMem retain its advantage when trained and evaluated with alternative memory schemas, including graphs, databases, or unstructured stores?
- How stable are the results across random seeds, repeated simulator trajectories, alternative judges, and independently sampled ablation subsets?
- What are the strict end-to-end success, safety, and irreversible-error rates for every method?
- Can autonomous memory invocation be trained jointly with maintenance and retrieval, rather than delegated to the task agent?
- How does the system handle user-requested correction, forgetting, consent revocation, access control, or conflicting multi-user information?
- Do the benchmark and method generalize to genuine longitudinal user interactions without synthetic persona scaffolding?
- Are the promised splits, fixtures, code, configurations, training checkpoint, and annotations released under terms permitting independent replication?

## Proposed AIDB experiments

- **Hypothesis:** PraxisMem’s advantage persists across memory representations and is not primarily caused by fitting the authored Markdown placement contract.
  - Baseline: Train matched content-only GRPO and PraxisMem variants on Markdown, a normalized relational schema, and an unstructured document store, using identical data, base model, budgets, and task agent.
  - Primary metric: Mean overall strict end-to-end Session SR across representations, supplemented by Interdependent Completion and representation-specific correct-organization recall.
  - Stop condition: Reject the generalization hypothesis if PraxisMem’s improvement over content-only GRPO is absent in at least two non-Markdown representations or reverses under any matched representation.
- **Hypothesis:** Jointly training autonomous memory invocation and query formulation closes a material part of the gap between Scheduled and Autonomous evaluation.
  - Baseline: Current PraxisMem with task-agent-controlled memory calls under the Autonomous setting.
  - Primary metric: Autonomous pooled Session SR, with retrieval-call recall on memory-dependent sessions and unnecessary-call rate on memory-independent sessions.
  - Stop condition: Stop if three independent runs show no improvement in pooled Session SR or if gains require a higher unnecessary-call rate without improving strict end-to-end success.
- **Hypothesis:** PraxisMem’s reported ranking is robust to run-to-run variation and judge choice.
  - Baseline: Re-run PraxisMem, Claude Code, Hermes, MemOS, Memory-R2, and the strongest retrieval baseline under the same complete test split.
  - Primary metric: Bootstrap confidence intervals for pooled Session SR and the probability that PraxisMem ranks first across multiple seeds and at least two independently audited semantic judges.
  - Stop condition: Conclude the ranking is not robust if confidence intervals overlap broadly with the strongest competitor or PraxisMem fails to rank first in more than one quarter of replicated evaluations.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-10-16T14:31:50.579990+00:00`
- Document SHA-256: `c83b2380d1a582f051ad43222b49afedacd5a9a91f4cf62408669503b32c9f01`
- Metadata SHA-256: `8a68e7f2e20f38f83894904b10a0f1768b03a4db14cb19e0befa35f1f825038e`
- Blocks: 411
- Deterministic repair attempts: 0
