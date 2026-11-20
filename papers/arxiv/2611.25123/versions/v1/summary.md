# Forget Freely, Grep Later: Lossless, Index-Free Memory for Long-Horizon LLM Agents

## Executive summary

GrepMem combines lossy working-context summaries with an append-only verbatim history searchable by regular expressions. Under a shared Qwen3.5-9B RL setup, it is compelling where exact details disappear from context: after RL it reaches 97.4% on ContextBench KV Store and 95.3% on Log Triage, versus 6.6–20.7% for SUPO and masking. Its average across five tasks is 66.4%, and it improves BCP-Multi over SUPO. The central caveat is task dependence: on AMA-Bench stream its post-RL advantage over SUPO is only 0.9 points, not statistically significant, while token use is 2.3× higher. Evidence is broad but restricted to one model and controlled benchmarks; confidence intervals cover items, not independent training runs. Code, prompts, and checkpoints are promised rather than shown as available.

## Problem

**Statement.** Long-horizon agents exceed bounded context windows and must remove observations before their future relevance is known. Compression may discard exact details, while structured external memory adds representation, extraction, indexing, and retrieval decisions.

**Why it matters.** The failure mode is consequential for research sessions, trajectory analysis, and long streams: an identifier, value, or log event observed early may only become relevant after later work, so successful reasoning requires both bounded active context and recoverable historical evidence.

**Scope.** The paper studies five context-management strategies with Qwen3.5-9B across multi-question research, recorded-agent trajectories, and synthetic long-stream recall. It tests questions known before input and questions revealed afterward, before and after strategy-specific reinforcement learning.

## Method

GrepMem retains SUPO's compaction loop but separates active reasoning state from persistent storage. When the working context approaches its limit, the model produces a summary and resumes from the original prompt plus that summary. Independently, the harness appends messages, tool calls, tool outputs, summaries, and responses to plain text. After the first compaction, the agent may query this history with case-insensitive regular expressions. Retrieval is paginated, includes surrounding lines and source locations, supports counting, and is learned jointly with task actions and summarization through episode-level reinforcement learning.

### Key components

- A bounded working context compacted by model-generated summaries.
- An append-only plain-text log intended to preserve the complete interaction trajectory verbatim.
- The grep_history tool for case-insensitive regular-expression matching, contextual lines, pagination, offsets, and count-only queries.
- Joint GRPO-based optimization of task actions, summaries, and retrieval behavior from a shared episode-level reward, without separate labels for summaries or queries.
- Controlled comparison using the same base model, training mixture, reinforcement-learning recipe, context window, and interaction budgets across strategies.

### Assumptions

- Relevant historical evidence can often be located through explicit lexical patterns such as names, identifiers, dates, numbers, or regular expressions.
- Keeping raw interaction history outside the active prompt is operationally affordable even when repeatedly processing the entire history in-context is not.
- Episode-level reward supplies enough learning signal to improve when and how the agent searches, despite no direct supervision of summaries or grep queries.
- The benchmark graders and gpt-5.6-sol reference judgments adequately represent answer correctness.
- Token usage summed across model calls is an informative cost proxy, although storage, grep execution, privacy controls, and infrastructure costs are not incorporated into the headline trade-off.

## Main claims

- **The authors present GrepMem as lossless and index-free because compaction affects the working context while an append-only raw log remains searchable without embeddings or an additional retrieval model.**
  - Evidence: [b00008-9fb402ee26] “GrepMem extends this loop by automatically appending every message and tool output to a persistent plain-text log.”; [b00008-9fb402ee26] “No embeddings, retrieval index, memory extraction, or additional models are required.”
- **Retrieval is agent-controlled rather than automatically injected: the agent chooses when to search and must formulate a regular expression that lexically matches relevant log text.**
  - Evidence: [b00034-ffaa276c1f] “The agent decides when to invoke it, subject to the interaction budget.”; [b00035-c5d8acec6d] “the agent must formulate search patterns that match relevant text in the history log.”
- **The experimental comparison attempts to isolate context-management strategy by training every strategy with a shared model and reinforcement-learning configuration.**
  - Evidence: [b00043-07f337c3da] “we separately train Qwen3.5-9B (Qwen Team, 2026) with thinking enabled under each context management strategy using the same GRPO-based RL recipe”; [b00043-07f337c3da] “All strategies use a 32,768-token context window and the same interaction budgets.”
- **The authors claim that GrepMem is Pareto-efficient on all evaluated accuracy–token-cost comparisons, but this is only relative to the evaluated strategies and tasks.**
  - Evidence: [b00073-9da0e348fe] “GrepMem lies on the accuracy–token-cost Pareto frontier across all five benchmark settings: no evaluated strategy is both cheaper and more accurate”

## Results

- **After RL, GrepMem obtains 97.4% accuracy on ContextBench KV Store and 95.3% on Log Triage, whereas SUPO and masking span 6.6–20.7%. This is the strongest controlled evidence for the paper's thesis: preserving raw history matters when evaluation demands exact values, individual log entries, or counts that lossy compression can omit.**
  - Context: The questions are revealed only after the stream has been processed, and ContextBench uses exact programmatic grading. The comparison shares the model and RL recipe, making the memory mechanism a meaningful experimental factor, though independent training-run variance is not measured.
  - Evidence: [b00064-873413c0e1] “After RL, GrepMem achieves 97.4% accuracy on KV Store and 95.3% on Log Triage, compared with just 6.6–20.7% for SUPO and Masking.”; [b00052-b3dd500de9] “KV Store requires retrieving exact values, while Log Triage requires finding specific log entries and counting entries that satisfy given conditions.”
- **On BCP-Multi, RL-trained GrepMem reaches 46.9% accuracy, exceeding SUPO by 8.8 percentage points and MemGPT by 7.0 points. The result supports recovery from repeated compaction in multi-question research, where the paper reports 25–27 compactions per episode for SUPO and GrepMem.**
  - Context: All questions are known initially, so this does not isolate surprise future queries. It instead tests whether earlier research findings survive a shared session and repeated summarization while subsequent questions are investigated.
  - Evidence: [b00062-d636de5ad4] “On BCP-Multi, the RL-trained GrepMem achieves 46.9% accuracy, outperforming SUPO by 8.8 percentage points and MemGPT by 7.0 points.”; [b00062-d636de5ad4] “SUPO and GrepMem average 25–27 context compactions per episode”
- **Across five tasks, GrepMem's average accuracy rises by 5.9 percentage points after RL to 66.4%. The improvement is concentrated rather than universal: Log Triage gains 20.3 points and BCP-Multi gains 6.0 points, while AMA-Bench file and stream change by -0.6 and +0.3 points.**
  - Context: This pattern suggests that training retrieval behavior helps exact lookup, counting, and evidence reuse more than causal or state-transition reasoning. Because the intervals reflect items rather than training runs, the attribution to RL remains vulnerable to run and checkpoint variation.
  - Evidence: [b00068-97cdc6493f] “GrepMem gaining 5.9 percentage points to achieve the highest post-RL average accuracy of 66.4%.”; [b00068-97cdc6493f] “The largest improvement occurs on ContextBench Log Triage, where accuracy increases by 20.3 points”; [b00068-97cdc6493f] “On BCP-Multi, accuracy improves by 6.0 points.”; [b00068-97cdc6493f] “AMA-Bench file and stream show almost no improvement after RL (-0.6 and +0.3 points, respectively).”
- **AMA-Bench stream is the consequential negative case. GrepMem's post-RL lead over SUPO is only 0.9 points, is not statistically significant even beyond the context window, and costs 2.3× as many tokens while invoking grep roughly 19 times per trajectory.**
  - Context: The method is therefore not uniformly cost-effective whenever input exceeds context. Its advantage appears tied to whether exact omitted details, rather than summary-preservable causal or state information, determine the answer.
  - Evidence: [b00064-873413c0e1] “GrepMem’s lead over SUPO narrows from 4.1 points before RL to 0.9 points after RL.”; [b00064-873413c0e1] “Even on trajectories exceeding the context window, the gain is not statistically significant.”; [b00073-9da0e348fe] “GrepMem uses 2.3× as many tokens as SUPO for a small improvement in accuracy and calls grep roughly 19 times per trajectory.”

## Experimental evaluation

### Datasets

- BCP-Multi: multi-question research constructed by grouping BrowseComp-Plus questions into disjoint triples; all questions are supplied initially and answered in one shared research episode.
  - Evidence: [b00050-1b7d21c226] “We group three questions into one episode so that findings from earlier searches must remain accessible”; [b00050-1b7d21c226] “All three questions are provided together in the initial prompt”
- AMA-Bench file: recorded trajectories remain outside working context and are exposed to every strategy through the same regular-expression trajectory-search tool.
  - Evidence: [b00050-1b7d21c226] “with the source trajectories kept outside the model’s working context and accessible through grep_trajectory.”; [b00050-1b7d21c226] “We provide all context management strategies with grep_trajectory”
- AMA-Bench stream: recorded trajectories are incrementally streamed; questions are hidden during processing and answered from independent copies of final context and memory state.
  - Evidence: [b00052-b3dd500de9] “AMA-Bench stream evaluates question answering over recorded agent trajectories presented incrementally.”; [b00052-b3dd500de9] “Both settings hide questions during input processing, preventing question-guided retention.”
- ContextBench KV Store and Log Triage: synthetic long streams test exact-value retrieval, log-event lookup, and conditional counting across increasing lengths.
  - Evidence: [b00052-b3dd500de9] “The agent receives these records incrementally, then answers 24 questions about them.”; [b00052-b3dd500de9] “We evaluate input sequences ranging from 33K to 968K tokens across 11 length levels, with four random seeds per level.”
- Training data mix: OpenResearcher single-question and three-question sessions plus synthetic ContextBench-style streams.
  - Evidence: [b00044-53b51a23cb] “Our training set contains 4,000 episodes: 70% single-question OpenResearcher tasks”; [b00044-53b51a23cb] “15% three-question sessions constructed from the OpenResearcher training split, and 15% synthetic ContextBench-style streams”

### Baselines

- ReAct retains complete history until the context limit and cannot continue past a full window.
  - Evidence: [b00041-195bbbdc26] “ReAct (Yao et al., 2023) retains full history until the context limit is reached.”
- Masking replaces older tool observations with placeholders and may additionally remove old reasoning or whole turns when required to fit.
  - Evidence: [b00143-a625e0a334] “the oldest unmasked observations are replaced by the placeholder until the context is below τ/2.”; [b00143-a625e0a334] “We drop entire turns only if the prompt still does not fit within the context window.”
- SUPO summarizes the accumulated interaction and resumes from a compacted context; it is the closest baseline because GrepMem extends this loop.
  - Evidence: [b00041-195bbbdc26] “SUPO (Lu et al., 2026) summarizes and resumes the context.”; [b00008-9fb402ee26] “We build on the summarization loop of SUPO”
- The MemGPT-style baseline combines a working notepad, searchable message history, recursive summaries, and archival memory; this implementation uses substring search and BM25 rather than embeddings.
  - Evidence: [b00041-195bbbdc26] “MemGPT-style memory (Packer et al., 2024) combines a notepad with searchable message history and archival memory.”; [b00145-a8b1442f05] “Archival memory ranks passages with BM25 (Robertson and Zaragoza, 2009) instead of MemGPT’s embeddings”

### Metrics

- Accuracy is reported before and after RL, with exact-value accuracy for ContextBench KV Store and exact-answer accuracy for Log Triage.
  - Evidence: [b00057-0284ce4a2e] “we report exact-value accuracy on KV Store and exact-answer accuracy on Log Triage.”
- Answer grading uses gpt-5.6-sol against references for research and trajectory QA, while ContextBench uses official programmatic graders.
  - Evidence: [b00054-68aa02a3ee] “OpenResearcher, BCP-Multi, and AMA-Bench answers are graded by gpt-5.6-sol (OpenAI, 2026) against references; ContextBench uses its official programmatic graders.”
- Uncertainty is reported through confidence intervals over test items rather than independent training runs.
  - Evidence: [b00054-68aa02a3ee] “We report 95% confidence intervals for accuracy.”; [b00054-68aa02a3ee] “These intervals reflect variation across test items, not across training runs.”
- Efficiency is measured as total prompt and generated tokens across all model calls, including compaction and recall; approximate wall-clock runtime is also presented.
  - Evidence: [b00054-68aa02a3ee] “We report total token cost across all model calls, including summarization and recall”; [b00155-71a5ae724d] “Runtime measurements are approximate because episodes ran concurrently on shared inference and retrieval servers.”

### Ablations

- Before-versus-after-RL evaluation isolates the empirical effect of reinforcement learning within each context-management strategy, though it is not replicated across independent training runs.
  - Evidence: [b00054-68aa02a3ee] “We evaluate the model before and after RL training.”; [b00057-0284ce4a2e] “using Qwen3.5-9B before and after training with the same RL recipe”
- Task comparisons vary whether questions are known before input or revealed afterward, testing guided retention versus unanticipated recall needs.
  - Evidence: [b00048-2469fa8aab] “These tasks are distinguished by whether questions are revealed before or after the relevant input.”
- No direct component ablation removes summaries, disables grep while retaining the log, replaces regex with another retriever, or separates raw-log preservation from retrieval training; such an experiment is not stated in the supplied blocks.
  - Evidence: [b00041-195bbbdc26] “GrepMem augments SUPO with a lossless, append-only history log and an index-free grep interface”

### Negative results

- On AMA-Bench stream, the non-ReAct strategies are close after RL, and GrepMem's gain over SUPO is not statistically significant beyond the context window.
  - Evidence: [b00064-873413c0e1] “all strategies except ReAct differ in accuracy by at most 1.2 percentage points after RL”; [b00064-873413c0e1] “Even on trajectories exceeding the context window, the gain is not statistically significant.”
- RL provides almost no improvement for GrepMem on either AMA-Bench variant.
  - Evidence: [b00068-97cdc6493f] “AMA-Bench file and stream show almost no improvement after RL (-0.6 and +0.3 points, respectively).”
- GrepMem has a poor token-cost trade-off on AMA-Bench stream relative to SUPO.
  - Evidence: [b00073-9da0e348fe] “The notable exception is AMA-Bench stream, where GrepMem uses 2.3× as many tokens as SUPO for a small improvement in accuracy”
- Reported single-checkpoint performance can fluctuate materially, weakening conclusions based on one selected checkpoint.
  - Evidence: [b00165-c398838982] “Single checkpoints fluctuate by several points”; [b00165-c398838982] “GrepMem on ContextBench Log Triage drops from 97.3 to 88.1 between two earlier evaluations.”


## Limitations

- External validity is restricted by controlled benchmarks and a single base model; the paper does not establish behavior across model scales, families, deployment environments, or open-ended agent workloads.
  - Evidence: [b00078-bb54733605] “Our evaluation focuses on controlled benchmarks and a single model, leaving open how GrepMem generalizes to broader agent settings.”
- Regex retrieval depends on lexical cues and may fail when the agent cannot name or pattern-match the relevant evidence, especially for paraphrased, implicit, or semantically related information.
  - Evidence: [b00078-bb54733605] “GrepMem also relies on lexical search, which may be less effective when relevant information cannot be identified through explicit search patterns.”
- Lossless history can retain sensitive information. Real deployment requires access controls, retention policies, deletion mechanisms, and threat analysis that are not evaluated here.
  - Evidence: [b00080-dd226be79b] “GrepMem preserves complete interaction histories, which may contain sensitive information in real-world deployments.”; [b00080-dd226be79b] “appropriate access controls and data retention policies should be applied according to the deployment setting.”
- The benefit is task-dependent; when summaries already preserve sufficient information, retrieval can add avoidable overhead.
  - Evidence: [b00078-bb54733605] “when summaries retain sufficient information, additional retrieval may introduce unnecessary overhead.”
- Statistical intervals quantify item variation rather than training-run variation, and checkpoint scores fluctuate, so optimization stability and reproducibility of RL gains remain incompletely characterized.
  - Evidence: [b00054-68aa02a3ee] “These intervals reflect variation across test items, not across training runs.”; [b00165-c398838982] “Single checkpoints fluctuate by several points”
- The compaction implementation may drop old turns and shorten recent tool outputs to make the summary request fit. The persistent log may preserve those records, but the summary-generation input itself is not always complete.
  - Evidence: [b00140-bf68f8fe85] “drop the oldest turns (always keeping the system prompt, the task and the latest turn), then shorten the latest tool outputs if needed”

## Reproducibility

**Status:** partial

The paper provides unusually substantial procedural detail, including a full training configuration, benchmark construction, harness corrections, and evaluation resampling. That supports informed reimplementation, but not direct reproduction from the supplied material. The artifact commitment is future tense, and the absence of independent RL runs is particularly important because checkpoint performance fluctuates. Reproducibility is therefore partial rather than strong.

**Available artifacts**

- The supplied paper gives prompts and tool-behavior details, including pagination and output limits.
- Training data composition, model, optimizer family, hyperparameters, interaction budgets, hardware, and reward design are reported.
- Evaluation task construction, seeds or seed ranges, sample counts, graders, re-evaluation procedure, and bootstrap method are described.
- The authors state an intention to release code, prompts, and trained checkpoints.

**Missing pieces**

- No released repository, artifact URL, license, or archival identifier is supplied in the provided blocks.
- The stated future release does not establish that code, prompts, or checkpoints are currently available.
- Independent training seeds and across-run variance are not reported.
- Exact end-to-end commands, environment lockfile, dependency versions, and raw per-item predictions are not supplied.
- Some implementation details are referenced through appendices, but the supplied evidence does not establish a complete runnable package.

## AIDB assessment

- Novelty: Moderate to high as a systems baseline: the individual ingredients—summarization, append-only logs, lexical search, and RL tool use—are simple, but their combination cleanly separates lossy active context from lossless historical storage and trains the agent to query its own trajectory. The paper itself acknowledges related raw-history and grep retrieval work, so novelty lies more in the integrated mechanism and controlled five-strategy evaluation than in a new retrieval primitive.
- Usefulness: High for agents whose failures arise from losing exact identifiers, values, citations, or log events. Implementation burden is low relative to embedding or knowledge-graph systems, and the controlled ContextBench and BCP-Multi results justify using GrepMem as a baseline. Usefulness is lower for semantic, causal, or state-abstraction questions, where summaries may suffice and repeated grep calls can waste tokens.
- Confidence: medium
- Recommended action: read
- Rationale: The strongest results are large, interpretable, and obtained under a shared training setup, while the negative AMA-Bench result usefully bounds the claim. However, adoption should wait for released artifacts, independent-run replication, tests across other models, and component ablations. Privacy and deletion requirements also need design work before production use of a complete append-only interaction history.

## Uncertainties

- **It is unclear how much of the gain comes from preserving raw history, exposing grep, learning retrieval with RL, or interactions among all three, because the supplied experiments do not report a factorial component ablation.** — Without separating storage, tool access, and training, implementers cannot know which components are necessary or whether a cheaper untrained or selectively enabled variant would retain most benefits.
  - Evidence: [b00037-5b441ab0eb] “jointly optimizing task actions, context summarization, and memory retrieval through a shared episode-level reward”; [b00041-195bbbdc26] “GrepMem augments SUPO with a lossless, append-only history log and an index-free grep interface”
- **The stability of RL improvements across random initializations is unknown.** — Confidence intervals over evaluation items cannot distinguish a robust training effect from variability caused by a single optimization run or checkpoint choice.
  - Evidence: [b00054-68aa02a3ee] “These intervals reflect variation across test items, not across training runs.”; [b00165-c398838982] “Single checkpoints fluctuate by several points”
- **The method's behavior when relevant evidence lacks obvious lexical anchors is not quantified.** — Many realistic memory queries are paraphrastic or conceptual; regex search may underperform semantic retrieval precisely in those deployments.
  - Evidence: [b00035-c5d8acec6d] “retrieval relies on regular-expression matching rather than semantic similarity”; [b00078-bb54733605] “may be less effective when relevant information cannot be identified through explicit search patterns.”
- **The headline token-cost frontier omits operational properties of ever-growing logs, including storage growth, search latency distributions, access-control overhead, and deletion compliance.** — A method can be token-efficient yet costly or unsafe in persistent production systems, especially when histories contain sensitive data.
  - Evidence: [b00054-68aa02a3ee] “We report total token cost across all model calls, including summarization and recall”; [b00080-dd226be79b] “GrepMem preserves complete interaction histories, which may contain sensitive information in real-world deployments.”

## Open questions

- Does GrepMem retain its advantage across different model families, parameter scales, context windows, languages, and agent tool ecosystems?
- Which component contributes most: the complete log, the grep interface, summary-plus-log complementarity, or RL-trained retrieval behavior?
- Can a learned policy avoid retrieval when summaries are sufficient, reducing the AMA-Bench stream overhead without sacrificing exact recall?
- How does regex retrieval compare with substring search, BM25, embeddings, hybrid lexical-semantic search, and structured memory under equal token, latency, and storage budgets?
- How should append-only history support redaction, user-requested deletion, retention limits, access control, and prompt-injection-resistant retrieval?
- Will the promised code, prompts, checkpoints, and per-item evaluation outputs reproduce the reported results across independent training runs?

## Proposed AIDB experiments

- **Hypothesis:** The complete raw log and grep access provide most of the exact-recall gain, while RL mainly improves query formulation and counting on the hardest log tasks.
  - Baseline: Use the same base model, training data, budgets, and evaluation protocol to compare SUPO; SUPO plus a raw log but no search; GrepMem before RL; GrepMem after RL; and GrepMem after RL with grep disabled at evaluation.
  - Primary metric: Paired accuracy difference on ContextBench KV Store and Log Triage, accompanied by processed tokens, grep calls, and confidence intervals across both evaluation items and at least three independent training runs.
  - Stop condition: Stop after all prespecified runs complete; reject the hypothesis if raw-log grep before RL fails to improve over SUPO or if the after-RL improvement is not consistent across independent runs.
- **Hypothesis:** A selective retrieval policy can preserve GrepMem's exact-recall performance while removing most unnecessary cost on tasks whose summaries already retain the answer.
  - Baseline: Compare always-available GrepMem with SUPO and a gated GrepMem variant trained or prompted to retrieve only when answer uncertainty or an exact-detail requirement crosses a fixed threshold.
  - Primary metric: Accuracy versus total processed tokens on AMA-Bench stream and ContextBench, with retrieval rate and calibration error as secondary metrics.
  - Stop condition: Stop when the gated policy either reduces AMA-Bench stream token use without a statistically significant accuracy loss and preserves ContextBench accuracy, or fails those criteria across all prespecified thresholds.
- **Hypothesis:** Hybrid lexical-semantic retrieval improves questions without explicit lexical anchors while preserving grep's efficiency on exact identifiers.
  - Baseline: Under an identical persistent log and agent policy, compare regex-only GrepMem, BM25-only retrieval, embedding-only retrieval, and a hybrid router on paraphrased long-history queries plus the original benchmarks.
  - Primary metric: Macro-averaged exact or reference-graded accuracy across lexical-anchor and paraphrastic subsets, reported jointly with processed tokens, retrieval latency, and index/storage cost.
  - Stop condition: Stop after the preregistered query set and compute budget are exhausted; reject the hybrid if it does not significantly improve the paraphrastic subset or if its gain is dominated on the accuracy–total-cost frontier.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:28:14.557845+00:00`
- Document SHA-256: `135464820bc29de1dd9376ac750ad8920cda12d11f673fcbf5fc3909d8f24de4`
- Metadata SHA-256: `10c02c95f50909099f1dbeb50e49462624641a27c32b3ec37060538b6c9e53e8`
- Blocks: 173
- Deterministic repair attempts: 0
