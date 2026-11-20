# HabitusMem: Belief Memory over Evolving User Preferences for LLM Agents

## Executive summary

HabitusMem replaces retrieved history fragments with request-conditioned textual beliefs containing claim, evidence, scope, and status. A Qwen3.5-9B LoRA writer serves frozen Qwen and DeepSeek agents. It is the best evaluated compact memory for PersonaMem-v2 answering and has the highest average reward among memory methods on VitaBench 2.0. Controlled interventions strongly support learned request conditioning as the main answering mechanism; auxiliary tasks help tool use. However, direct-only training beats the full method on answering, plain text can beat it on tool-use consistency, each writer is trained once, and retraction handling remains poor. The method is promising but should be validated across seeds, stronger controls, broader applications, and human-grounded evaluation before adoption.

## Problem

**Statement.** Personalized agents must infer which preferences currently hold, where they apply, and which ones matter to the present decision. Content-oriented memories preserve statements or events but do not explicitly represent evidential support, scope, or whether a preference was superseded or retracted.

**Why it matters.** An agent can otherwise apply stale or context-specific preferences, omit exact transactional constraints, or suffer interference from irrelevant history. These errors affect both personalized answers and tool-executed actions.

**Scope.** The paper studies long-history personalized multiple-choice and generated answering on PersonaMem-v2, plus personalized tool use on VitaBench 2.0, using two frozen locally deployed agent families.

## Method

HabitusMem treats the user as an evolving latent preference state and implements a qualitative approximation to belief-state memory. A trained writer reads a budget-selected raw history plus the current request, emits request-relevant textual records, and passes them to a frozen agent. The decision-theoretic equations motivate the design but are not numerically estimated or optimized through agent rollouts.

### Key components

- Each record has the form claim | evidence | scope | status, separating the asserted preference or constraint from its source, applicability, and current standing.
- The writer is Qwen3.5-9B with one shared LoRA adapter and produces memory in one greedy decoding pass.
- History selection keeps the beginning on PersonaMem-v2 and combines an initial segment with recent interactions on VitaBench 2.0; memory is regenerated whenever history or request changes.
- Training has a teacher-supported cold start and parent-writer stage, followed by a shared four-task mixture: direct writing, state update, request projection, and action projection.
- Question and action suffixes condition selection differently; action projection emphasizes exact products, variants, quantities, addresses, times, and fulfillment constraints.

### Assumptions

- Preferences can be usefully represented as durable but revisable latent dispositions, circumstances, and explicit constraints.
- A textual record can communicate qualitative belief state without calibrated posterior probabilities.
- The current request is both evidence about the user and a specification of the decision for which memory should be selected.
- A frozen downstream agent will generally interpret and obey evidence, scope, and status fields, although the probes show this is not guaranteed.
- Teacher-written and annotation-derived reference memories are adequate supervision even though target preparation checks syntax rather than factual correctness.

## Main claims

- **The proposed representation defines memory as the decision-relevant subset of beliefs about the user, with evidence, scope, and status attached to each claim.**
  - Evidence: [b00010-794f6f32c0] “Memory is thus composed of beliefs about the user rather than of content from the history.”; [b00033-b8fc16f53d] “Each record in HabitusMem has four fields.”
- **HabitusMem is an approximate learned text generator, not an implementation of exact Bayesian inference or direct risk optimization.**
  - Evidence: [b00034-dfce5364cc] “HabitusMem neither estimates numerical posteriors nor optimizes Equation 2 through agent rollouts.”; [b00154-18ba756ae1] “The records therefore express the belief qualitatively, through the stated evidence and status of each claim, and not as posterior probabilities.”
- **The deployed writer is trained through four tasks sharing one adapter, intended to cover belief inference, revision, and decision projection.**
  - Evidence: [b00047-0a7932f372] “We initialize HabitusMem from the parent and train it on four tasks that cover inferring, revising, and selecting beliefs.”; [b00049-04b396c8ac] “All four tasks update one adapter, so that inference, update, and projection share parameters.”
- **The component evidence attributes answering gains primarily to learned use of the current request, while auxiliary supervision is more useful for tool execution.**
  - Evidence: [b00072-2b468ed21e] “The two interventions have nearly the same effect, which shows that the gain comes from the content of the request and not from the suffix format.”; [b00077-2894372ca8] “On tool use, the full mixture improves paired average reward over Direct only by 3.3 points with Qwen and 4.5 points with DeepSeek”

## Results

- **On PersonaMem-v2, HabitusMem is the strongest compact memory in overall accuracy for both agents: 0.537 with Qwen and 0.484 with DeepSeek, reported as 4.8 and 4.6 points above the strongest baseline. It nevertheless remains below full context in overall multiple-choice accuracy.**
  - Context: This is the primary answering result. The method leads more consistently across scenarios than individual content-memory baselines, but the privileged full-history condition scores higher overall.
  - Evidence: [b00061-2d3b4331df] “HabitusMem is the most accurate memory method under both agents, at 0.537 with Qwen and 0.484 with DeepSeek, 4.8 and 4.6 points above the strongest baseline.”; [b00059-96947022eb] “Full context 0.519 0.594 0.573 0.543 0.624 0.585 0.599 0.548 0.565 0.569”; [b00059-96947022eb] “HabitusMem 0.649 0.526 0.529 0.503 0.557 0.522 0.487 0.462 0.532 0.537”
- **On VitaBench 2.0, HabitusMem obtains the highest average reward among memory methods for both agents and the highest all-success among non-privileged conditions: 0.1310 with Qwen and 0.1284 with DeepSeek, versus 0.1297 and 0.1102 for full context.**
  - Context: The advantage is clearest in repeatability across trials, not any-success coverage. The ground-truth profile is privileged and therefore should not be treated as an ordinary deployable baseline.
  - Evidence: [b00062-ebbb346518] “Table 2: Personalized tool-use results on VitaBench 2.0.”; [b00065-9dc81c7a2f] “HabitusMem obtains the highest average reward among memory methods under both agents and the highest all-success of any non-privileged condition”; [b00065-9dc81c7a2f] “0.1310 and 0.1284 against 0.1297 and 0.1102 for full context.”
- **Removing or corrupting request conditioning sharply reduces PersonaMem-v2 performance. Default accuracy of 0.5372 and 0.4842 falls to 0.4004 and 0.3394 without the request; using an unrelated request gives 0.4019 and 0.3376. The paired intervention changes only the request passed to the writer.**
  - Context: This is the strongest controlled mechanism result because the trained writer, selected history, instruction, generation settings, downstream queries, agents, and judge are held fixed.
  - Evidence: [b00166-fb349e77aa] “HabitusMem (default) 0.5372 0.3257 0.4842 0.3824”; [b00166-fb349e77aa] “Without request conditioning 0.4004 0.1345 0.3394 0.1995”; [b00166-fb349e77aa] “With an unrelated request 0.4019 0.1247 0.3376 0.1859”; [b00172-77ef4dcaed] “Both interventions keep the trained adapter, instruction, selected history, and generation settings fixed and change only the request passed to the writer.”
- **Controlled probes expose a major failure on retracted preferences despite explicit status records: the full format yields only 1/10 correct retraction answers with Qwen and 2/10 with DeepSeek. DeepSeek also scores only 2/10 for conditional preferences queried outside their scope.**
  - Context: Manual inspection indicates that revocations were present in memory, so these errors implicate downstream use as well as extraction. The constructed probes are diagnostic rather than benchmark-sampled estimates.
  - Evidence: [b00199-e31efa742f] “Conditional, solo 10/10 2/10 7/10”; [b00199-e31efa742f] “Retracted 1/10 2/10 0/10”; [b00201-e2bf38528a] “the two agents answer one and two of ten retraction probes correctly although the full writer marks the revocation.”

## Experimental evaluation

### Datasets

- PersonaMem-v2, English 32k setting: personalized answering from long histories, with changing and forgotten preferences; the official test split contains 5,000 queries across nine scenarios.
  - Evidence: [b00054-ba59b79f0d] “We evaluate in the English 32k setting, whose test split contains 5,000 queries.”; [b00054-ba59b79f0d] “The test queries span nine task scenarios.”
- VitaBench 2.0: 771 subtasks from 56 users covering delivery, in-store consumption, and online travel, evaluated with four trials per subtask.
  - Evidence: [b00054-ba59b79f0d] “VitaBench 2.0 (Chen et al., 2026) contains 771 subtasks from 56 users”; [b00054-ba59b79f0d] “We run four trials per subtask”
- A constructed diagnostic suite uses 90 probes per writer across ten topics to isolate attribution, scope, and status behavior.
  - Evidence: [b00194-a7397289b2] “We construct 90 probes per writer across ten topics and nine cells”

### Baselines

- Compact systems: RAG, Rewrite, Mem0, A-MEM, and MemListener.
  - Evidence: [b00056-66997be18d] “We compare with five compact memory systems: retrieval-augmented memory (RAG)”; [b00056-66997be18d] “Rewrite (an LLM-rewritten history summary), Mem0 (Chhikara et al., 2025), A-MEM (Xu et al., 2026a), and MemListener”
- Reference conditions: memory-free base LLM, full interaction history, and a privileged annotated ground-truth profile on VitaBench 2.0.
  - Evidence: [b00056-66997be18d] “The base LLM receives no memory, and full context gives the agent direct access to the interaction history.”; [b00056-66997be18d] “a ground-truth profile built from annotated preferences is an additional privileged reference.”
- Two frozen downstream agents are evaluated: Qwen3.5-397B-A17B and DeepSeek-V4-Flash-0731.
  - Evidence: [b00056-66997be18d] “We test personalization with two locally deployed agents, Qwen3.5-397B-A17B and DeepSeek-V4-Flash-0731.”

### Metrics

- PersonaMem-v2 uses multiple-choice personalized QA accuracy as primary metric and an external Qwen3.5-9B generation judge score.
  - Evidence: [b00054-ba59b79f0d] “We report personalized QA accuracy on multiple-choice questions as the primary metric and a generation score assigned by an external Qwen3.5-9B judge.”
- VitaBench reports average reward, any-success over four trials, and all-success over four trials.
  - Evidence: [b00054-ba59b79f0d] “We report average reward (Avg​@​4), success in at least one of four trials (Pass​@​4, any-success), and success in all four (Pass4, all-success).”
- Statistical comparisons use McNemar tests for query correctness and success, and paired bootstrap over task clusters for average reward.
  - Evidence: [b00179-311c50e0d0] “Paired PersonaMem-v2 accuracy comparisons use query-level correctness and McNemar tests.”; [b00179-311c50e0d0] “VitaBench average reward uses paired bootstrap over task clusters”

### Ablations

- Fixed-writer inference interventions remove the request or substitute one unrelated request; both strongly reduce answering accuracy and generation score.
  - Evidence: [b00072-2b468ed21e] “Both keep the trained adapter, instruction, history selection, and generation settings fixed and change only the request passed to the writer.”
- Leave-one-task-out retraining isolates direct writing, state update, request projection, and action projection; direct writing is essential for the deployed raw-history-to-record mapping.
  - Evidence: [b00076-8a995c3767] “Removing direct writing lowers accuracy to 0.387 and 0.348, the level of the untrained writers”; [b00076-8a995c3767] “the removed task is the only difference.”
- Matched controls compare the full mixture with optimization-budget-matched direct-only training and a fully retrained plain-text format.
  - Evidence: [b00178-1df9afc626] “matching the 5,096 steps of the 40,766-row full mixture”; [b00178-1df9afc626] “The plain-text control starts from the base model and repeats the cold-start and four-task stages with the same examples”
- Sensitivity tests vary task weights, input and output budgets, history selection, and prompting.
  - Evidence: [b00183-6232c26131] “We did not run an extensive hyperparameter search”; [b00188-7c708eaf48] “We vary one setting at a time”

### Negative results

- Direct-only training outperforms full HabitusMem on PersonaMem-v2 answering under both agents, so auxiliary tasks do not improve the primary answering result.
  - Evidence: [b00168-23b2fd9a8e] “Direct only 0.553 0.345 0.487 0.401”; [b00168-23b2fd9a8e] “HabitusMem 0.537 0.326 0.484 0.382”
- On VitaBench, the plain-text control has higher all-success than HabitusMem for both agents, including 0.1725 versus 0.1310 with Qwen.
  - Evidence: [b00069-3fc821291e] “Plain text 0.3252 0.4929 0.1725 0.3324 0.5344 0.1362”; [b00069-3fc821291e] “HabitusMem 0.3291 0.5616 0.1310 0.3573 0.5798 0.1284”
- Training-mixture selection has no uniform benefit across agents and metrics; with Qwen it improves any-success but reduces all-success.
  - Evidence: [b00185-b75314d1e6] “selected has higher any-success (0.5642 against 0.4410 and 0.4488) and lower all-success (0.1336 against 0.2153 and 0.2438).”; [b00185-b75314d1e6] “weight selection does not yield a uniform advantage across agents and metrics.”


## Limitations

- A fixed input budget can omit relevant evidence, and reduced input caps cause large performance losses.
  - Evidence: [b00083-d9721ad97e] “its fixed input budget may exclude relevant evidence from long interaction histories.”; [b00188-7c708eaf48] “Reducing the input cap to 2,500 or 5,000 tokens costs 13.7–16.7 accuracy points”
- Belief extraction and downstream application remain imperfect, especially for retractions and exact execution constraints.
  - Evidence: [b00083-d9721ad97e] “belief extraction and application remain imperfect, particularly for retracted preferences and precise execution constraints.”
- External validity is limited because broader applications such as email composition, recommendation, and scheduling were not evaluated.
  - Evidence: [b00083-d9721ad97e] “we have not yet evaluated HabitusMem in broader applications, including email composition, personalized recommendations, and scheduling.”
- Training targets may contain factual errors because preparation enforces syntax but does not validate record content.
  - Evidence: [b00047-0a7932f372] “Target preparation enforces the record syntax but does not check the factual content of the records.”
- Statistical tests omit training-seed variability because each writer was trained only once.
  - Evidence: [b00179-311c50e0d0] “Each writer is trained once, so these tests do not capture variation across training seeds.”

## Reproducibility

**Status:** partial

The methodological specification is unusually detailed and a repository is named, but reproducibility cannot be rated strong from the supplied document alone. Key generated artifacts and software-environment details are not established, and single-run training prevents assessment of optimization variance.

**Available artifacts**

- A code-repository URL is supplied in the document front matter.
- The paper specifies the writer architecture, LoRA targets and hyperparameters, dataset splits, task-mixture sizes, inference selectors, evaluation protocols, statistical tests, and computational cost.
- Exact aggregate tables and detailed component-control protocols are included.

**Missing pieces**

- No evidence in the supplied blocks that released code was executed or that checkpoints, generated memories, evaluation trajectories, teacher outputs, and judge prompts are available.
- No multi-seed training results or uncertainty over writer training.
- The supplied blocks do not establish environment versions, hardware model, random seeds, or an end-to-end reproduction command.

## AIDB assessment

- Novelty: The main conceptual contribution is to represent personalized memory as request-conditioned qualitative beliefs with explicit evidence, scope, and status, rather than as retrieved or summarized historical content. The decision-theoretic framing is a rationale, not an executed probabilistic model.
- Usefulness: High potential for agents that must reconcile evolving preferences and exact task constraints. The request-conditioning intervention is compelling, memory is much shorter than full history, and the method transfers across two agent families. Practical value is tempered by retraction failures, writer latency, and mixed evidence for structured fields and auxiliary tasks.
- Confidence: medium
- Recommended action: read
- Rationale: The paper merits close reading and controlled replication: it has a clear representation, strong paired request-conditioning evidence, broad baselines, and useful negative results. Adoption is premature because structured records do not consistently beat plain text, direct-only training wins on answering, retraction obedience is poor, and training-seed variance is unknown.

## Uncertainties

- **The independent value of evidence, scope, and status fields is not cleanly established on downstream benchmarks.** — The structured record is central to the novelty claim, yet the matched plain-text control sometimes has better tool-use consistency, and the paper reports non-significant DeepSeek tool differences.
  - Evidence: [b00180-86d9fbe6f5] “none of which is statistically significant.”; [b00079-a6ecf8264a] “On PersonaMem-v2, the full format adds 1.3 and 1.9 accuracy points”
- **Some prose values conflict with the main accuracy table for the DeepSeek reference conditions.** — The discrepancy complicates exact interpretation of claimed accuracy-versus-generation tradeoffs and should be resolved from evaluation artifacts.
  - Evidence: [b00061-2d3b4331df] “from 0.446 and 0.263 to 0.569 and 0.522”; [b00059-96947022eb] “Base LLM 0.368 0.230 0.236 0.257 0.274 0.232 0.246 0.265 0.224 0.266”; [b00059-96947022eb] “Full context 0.533 0.512 0.514 0.512 0.553 0.545 0.529 0.516 0.524 0.527”
- **The extent to which gains depend on teacher quality, preference annotations, or benchmark-specific training remains unresolved.** — All training examples come from PersonaMem-v2, while cold-start memories and auxiliary states are teacher-generated; generalization to organically evolving users may differ.
  - Evidence: [b00162-93d9d13bb7] “All examples come from the official training split, and direct writing uses its preference annotations as target supervision.”; [b00045-7fa5339a6e] “belief memories from a frozen DeepSeek-V4-Flash teacher”
- **Automatic judges and simulated users may introduce model-dependent measurement error.** — The generation score, simulated user, trajectory scoring, and some probe checks depend on Qwen3.5-9B; the gift analysis demonstrates that checker and answer-key assumptions can distort conclusions.
  - Evidence: [b00054-ba59b79f0d] “a generation score assigned by an external Qwen3.5-9B judge.”; [b00203-070533617b] “We treat the automatic checks as model-dependent diagnostics cross-checked by manual inspection.”

## Open questions

- Do gains persist across multiple writer-training seeds and independently reproduced evaluation runs?
- Which individual field—evidence, scope, or status—causally improves downstream decisions when content and token budget are strictly matched?
- Can an agent-side instruction or training intervention make retracted and out-of-scope preferences reliably non-operative?
- How does the method perform on naturally collected histories, languages beyond the evaluated English setting, and broader workflows such as email, recommendations, and scheduling?
- Can incremental belief updates match full regeneration while reducing latency without accumulating stale or unsupported beliefs?

## Proposed AIDB experiments

- **Hypothesis:** Explicit evidence, scope, and status fields improve decision quality beyond equivalent plain text when information content and token count are matched.
  - Baseline: Content-matched plain bullets plus separate variants retaining only evidence, only scope, or only status; train every condition with identical data, optimization steps, and multiple seeds.
  - Primary metric: Paired downstream accuracy and all-success on benchmark tasks, supplemented by accuracy on controlled attribution, scope, and retraction probes.
  - Stop condition: Reject the hypothesis if the full schema does not significantly outperform content-matched plain text across both agent families and the relevant field-specific probes.
- **Hypothesis:** Agent-side training or constrained execution can convert correctly written retraction and scope records into reliable behavior.
  - Baseline: The frozen-agent HabitusMem pipeline with the current execution guidance.
  - Primary metric: Correct answers on retracted and conditional-solo controlled probes, with separate measurement of whether the writer recorded the manipulated fact correctly.
  - Stop condition: Stop if downstream correctness fails to improve while writer-record correctness remains unchanged, or if gains reduce ordinary active-preference accuracy.
- **Hypothesis:** HabitusMem generalizes beyond benchmark-specific supervision and remains beneficial under natural history growth and distribution shift.
  - Baseline: Full context, RAG, Rewrite, direct-only belief writing, and content-matched plain text.
  - Primary metric: Human-validated task success and preference-violation rate on held-out real workflows involving email, recommendations, and scheduling.
  - Stop condition: Do not advance to deployment if HabitusMem fails to beat the strongest compact baseline on preference-violation rate across multiple training seeds or exhibits materially worse retraction compliance.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:18:01.142796+00:00`
- Document SHA-256: `c643b778d43b3fd1c8c964bea1555fcd059b419e579c948fad0b36519a778fa9`
- Metadata SHA-256: `5194d4b7b1b155fb9dd4cd70e74bd56e94051101d303c6fdff4511dfd226bd4a`
- Blocks: 207
- Deterministic repair attempts: 1
