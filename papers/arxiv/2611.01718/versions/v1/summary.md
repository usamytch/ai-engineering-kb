# Delivered, Not Used: Evaluating Agent Memory at Its Point of Use

## Executive summary

MemUse is a trajectory-based framework for distinguishing memory delivery, novelty, attributable use, and observed consequences. Across SWE-bench Verified runs, final resolve rates did not distinguish four memory configurations from no memory, while delivery-level analysis exposed large differences in relevance, use, benefit, harm, repetition, and token efficiency. The strongest insight is diagnostic rather than causal: beneficial use can occur in failed episodes and harmful use in successful ones. Evidence-access checks and explicit uncertainty are strengths, but the conclusions depend on one agent, one task sequence, one judge, observational attribution, and a corpus with identified benchmark overlap. Human agreement was not measured. MemUse is promising for audits and system design, but should not yet be treated as a validated causal utility measure.

## Problem

**Statement.** End-task success, retrieval quality, and cost cannot determine whether a delivered memory changed an agent’s behavior or what consequences followed. The paper asks how to evaluate individual, dynamically delivered memories from recorded execution alone while separating information already visible to the agent from information supplied by memory.

**Why it matters.** A delivered entry consumes finite context even when it is irrelevant, redundant, ignored, or harmful. Outcome-only evaluation can hide useful local progress inside failed tasks, harmful detours inside successful tasks, and null aggregate effects produced by very different mechanisms.

**Scope.** The empirical scope is repository-level software engineering with mini-SWE-agent on SWE-bench Verified, comparing four configurations of three memory systems. MemUse evaluates realized behavior in recorded trajectories; it does not estimate counterfactual effects on task success.

## Method

MemUse reconstructs each memory delivery at its consuming model call, removes the target delivery to form the prior context, and follows eligible actions through an entry-specific credit window. Identical repeated deliveries that remain visible are grouped into injection spans. An agentic judge assigns relevance, accuracy, novelty, influence, and observed effect to each entry. Programmatic checks enforce structural validity and required evidence reads; deterministic rules then produce span triage labels and entry-share profiles. A memory graph links verdicts to item histories, while delivered-text estimates and recorded call costs represent resource use.

### Key components

- A memory bridge annotates creation, update, search, and delivery operations; a pass-through recorder captures model requests, responses, tool observations, usage, and context rewrites.
- Exposure matching distinguishes full, clipped, and unknown exposure; the prior context contains what remained visible at first consumption after removing the target delivery.
- Injection spans collapse identical restatements while retaining their delivered-text cost; per-entry credit windows allocate later actions among successive deliveries of the same item.
- The judge separates information quality from influence and consequence, with explicit null or undetermined values when evidence cannot support a decision.
- Coverage checks require complete reads appropriate to each judgment, including full credit windows for non-use and the remaining trajectory for determined effects.
- Fixed aggregation reports span triage, entry-share profiles, benefit and harm yields, episode coverage, token efficiency, memory histories, and recorded monetary cost.

### Assumptions

- Recorded model-boundary inputs and annotations faithfully represent what the agent saw.
- A specific action can be observationally attributed when memory-specific content is absent from prior sources and appears in an action within the credit window.
- Recorded checks and downstream use are adequate evidence of local benefit or harm, although they do not establish a counterfactual task-success effect.
- Equal weighting of profiled spans is an appropriate summary despite differing entry counts and delivery forms.
- The supplied gold patch may inform relevance and accuracy without determining influence or observed effect.

## Main claims

- **The paper presents MemUse as a reference-free framework that jointly assesses use and observed effects of individual memory deliveries without requiring a dedicated benchmark, reference trajectory, task label, or additional execution.**
  - Evidence: [b00009-6c8036bd71] “MemUse is the first reference-free framework to jointly assess the use and observed effects of individual memory deliveries without a dedicated memory benchmark, reference solution, task label, or additional execution.”
- **MemUse explicitly separates information quality, attributable action, and observed consequence rather than equating delivery or action consistency with memory use.**
  - Evidence: [b00031-4d0fed2cdf] “Information comprises its relevance, accuracy, and novelty; use is its influence on actions; and consequence is the observed effect of that use.”; [b00057-8360f9b71f] “An action matching such advice therefore requires evidence linking a specific detail of the action to the entry.”
- **The framework’s verdicts describe observed behavior, not the counterfactual effect of memory on task success.**
  - Evidence: [b00031-4d0fed2cdf] “The verdict describes observed behavior in the recorded episode, not a counterfactual effect on task success.”
- **Programmatic validation establishes evidence access and coverage but leaves semantic interpretation to the model judge.**
  - Evidence: [b00070-5cace9f926] “The checks certify evidence access and coverage, and the judge interprets the evidence.”

## Results

- **Final outcomes did not separate the systems: resolve rates ranged from 72.65% to 73.35% versus 72.95% without memory; every 95% interval contained zero, and the maximum difference was 0.40 percentage points.**
  - Context: This is the controlled memory-versus-no-memory comparison over paired task runs. It supports a null outcome-level conclusion, not equivalence: the reported intervals permit both small gains and small losses.
  - Evidence: [b00098-f77cf085bf] “Resolve rates range from 72.65% to 73.35%, against 72.95% without memory, and every 95% interval for the difference from the baseline contains zero.”; [b00098-f77cf085bf] “These differences of at most 0.40 percentage points are smaller than the spread across the baseline’s own runs”
- **Delivery-level profiles differed sharply: MemGovern had 15.08% relevance and 50.50 beneficial entries per million delivered tokens, Mem0 had 1.42–1.43% relevance and 3.08–4.92 token efficiency across the other configurations, while TencentDB reached 28.48% relevance but its always-relevant persona contributed 18.0 percentage points.**
  - Context: These comparisons show that similar task outcomes can conceal different memory composition and efficiency. TencentDB’s headline relevance is sensitive to recurring persona content, so it should not be read as task-specific retrieval quality alone.
  - Evidence: [b00099-95759eaacc] “MemGovern’s mean relevance share of 15.08% is more than ten times Mem0’s 1.42–1.43%.”; [b00099-95759eaacc] “TencentDB’s relevance share is the highest at 28.48%, but the spans that carry its always-relevant persona block contribute 18.0 of these percentage points.”; [b00099-95759eaacc] “MemGovern’s token efficiency of 50.50 beneficial entries per million delivered tokens is more than ten times the 3.08–4.92 of the other configurations.”
- **Most memory failed before productive action: 71.5–98.6% of entries per span were irrelevant on average, 51.3–79.7% of relevant entries remained unused, and only 0.40–4.08% of entries were acted on.**
  - Context: Unused means no action, selection, or reference within the applicable credit window. The paper reports that redundancy explains only part of non-use, so filtering and actionability are distinct bottlenecks.
  - Evidence: [b00101-4cc1295c5f] “First, 71.5–98.6% of a span’s entries were irrelevant on average.”; [b00101-4cc1295c5f] “Second, 51.3–79.7% of the relevant entries remained unused”; [b00101-4cc1295c5f] “the agent acted on only 0.40–4.08% of a span’s entries on average”
- **Observed memory effects and terminal outcomes often diverged: 89 of 383 episodes with beneficial use failed (23.2%), while 5 of 16 episodes with harmful use passed (31.3%).**
  - Context: This is the central evidence that final success is an inadequate proxy for realized memory effects. Because effect labels are observational judge assessments, these counts diagnose trajectory-local contributions rather than causal changes in success probability.
  - Evidence: [b00104-f0965906dc] “89 of 383 with beneficial use failed (23.2%), while 5 of 16 with harmful use passed (31.3%).”
- **Repeated and broad delivery consumed most text while concentrated full content supplied most benefit: TencentDB restated 88.4% of deliveries and Mem0 78.2%; full cards supplied 96.4% of MemGovern benefit with 12.5% of tokens, task recall supplied 75.8% of Mem0 benefit with 13.0%, and full skills supplied 86.0% of TencentDB benefit with 2.0%.**
  - Context: This result points to deduplication and staged retrieval as concrete design opportunities. Preview and index content may still have instrumental value through selection, so token removal should preserve access pathways.
  - Evidence: [b00111-a8fe9b581a] “TencentDB restates 88.4% of its deliveries and Mem0 78.2%”; [b00110-e2a1dc30e0] “Full cards account for 96.4% of MemGovern’s beneficial entries but 12.5% of its delivered tokens.”; [b00110-e2a1dc30e0] “Mem0’s task recall supplies 75.8% of its beneficial entries with 13.0% of its tokens”; [b00110-e2a1dc30e0] “full skills supply 86.0% of TencentDB’s beneficial entries with 2.0% of its tokens.”

## Experimental evaluation

### Datasets

- All SWE-bench Verified tasks, ordered to approximate ongoing development across Python repositories; memory persists between sequential tasks.
  - Evidence: [b00090-c37b219a38] “We use all 500 tasks of SWE-bench Verified (Jimenez et al., 2024), drawn from 12 Python repositories”; [b00090-c37b219a38] “Every run, with or without memory, executes the same sequence one task at a time.”

### Baselines

- No-memory mini-SWE-agent with the same agent model and task sequence, repeated alongside each memory configuration.
  - Evidence: [b00094-ea7e0a6ceb] “Each memory configuration and a no-memory baseline run the sequence four times with the same agent model”; [b00097-76896870dd] “No memory 73.0±1.5 — 0.0045 —”
- Memory configurations: MemGovern, Mem0 with local scopes, Mem0 with local plus global scope, and TencentDB Agent Memory.
  - Evidence: [b00092-d73db40fde] “We evaluate three systems in four configurations, which together cover the host-scheduled and agent-directed delivery routes.”

### Metrics

- SWE-bench resolve rate, paired percentage-point difference from no memory, bootstrap interval, per-episode monetary cost, and cost increase.
  - Evidence: [b00096-9b1f799fdc] “Resolve rates are mean ± sample standard deviation across four runs. Differences from the no-memory baseline are in percentage points, with 95% confidence intervals from a paired bootstrap over tasks.”
- Memory-profile shares: relevance, corroboration, information gain, acted-on use, benefit, harm, plus uncertainty shares.
  - Evidence: [b00078-45853d527d] “Six axes describe information quality, use, and consequence.”; [b00079-ac7c5a3b52] “Four uncertainty shares use the same denominator.”
- Benefit and harm yields, beneficial entries per delivered-token volume, and episode-level coverage.
  - Evidence: [b00082-ec82e5db38] “Benefit and harm yields give the number of beneficial and harmful entries per 100 profiled spans.”; [b00082-ec82e5db38] “Token efficiency gives the number of beneficial entries per million estimated tokens of delivered memory text.”

### Ablations

- —

### Negative results

- No memory configuration showed a statistically resolved task-success difference from the no-memory baseline.
  - Evidence: [b00098-f77cf085bf] “every 95% interval for the difference from the baseline contains zero.”
- The Mem0 local-plus-global configuration did not exercise its global scope, leaving the two Mem0 profiles nearly identical rather than testing global-memory value.
  - Evidence: [b00099-95759eaacc] “The agent never requested the global scope, so both used repository and episode scopes.”
- Most final outcome gains and losses lacked a corresponding acted-on memory entry, limiting outcome differences as evidence of memory influence.
  - Evidence: [b00107-5690a8fd6d] “Most of these episodes contained no acted-on entry (64 of 71 gains and 80 of 87 losses).”


## Limitations

- Human agreement with the judge was not measured. Coverage checks prove that required evidence was read, not that relevance, attribution, or effect judgments are semantically correct.
  - Evidence: [b00260-2ceda319d7] “These checks establish access to the required evidence. Agreement with human judgments has not been measured in this evaluation.”; [b00262-aa5dce7811] “They do not validate prose-only citations or semantic correctness.”
- The study is narrow: one coding benchmark, one agent implementation and model, one fixed task order, and one judge configuration. Generalization to other agents, domains, judges, and task orders is untested.
  - Evidence: [b00290-06d5dc2695] “The experiments use one fixed task sequence, four runs per configuration, and a common judge protocol.”; [b00295-7012197940] “The agent is mini-SWE-agent 2.4.6 with gpt-6-luna with medium reasoning effort”; [b00304-5c404fa270] “All runs use DeepSeek-V4.1-Flash-1017 through Chat Completions, with temperature zero and medium thinking.”
- The attribution is observational and does not establish how the same episode would have unfolded without a delivery.
  - Evidence: [b00031-4d0fed2cdf] “The verdict describes observed behavior in the recorded episode, not a counterfactual effect on task success.”
- Bootstrap intervals condition on recorded memory histories and do not model dependence between sequential tasks induced by evolving memory.
  - Evidence: [b00309-98d7b8eb80] “Independent task resampling does not model dependence between tasks induced by evolving memory histories, which are not rerun.”
- MemGovern contains identified overlap with benchmark development histories, potentially inflating relevance or efficiency and also preserving superseded harmful guidance; full-corpus prevalence is unknown.
  - Evidence: [b00353-7b757fa636] “MemGovern’s reported relevance and token efficiency therefore include guidance from the benchmark problems’ own development histories.”; [b00353-7b757fa636] “This targeted review establishes specific overlaps; their prevalence across the full corpus remains unmeasured.”
- Delivered-token volume is estimated from characters rather than isolated model token counters, and monetary accounting omits unreported service work and hosting charges.
  - Evidence: [b00288-c05af1a1f0] “Because token counters belong to whole model calls, delivery volume uses the auxiliary estimate T^S=⌊CS/4⌋.”; [b00286-c854c361aa] “The accounting covers observed model calls and excludes unreported service work and hosting charges.”

## Reproducibility

**Status:** partial

Methodological specification is unusually detailed, including exact routing, validation, aggregation, and execution policies. However, the supplied paper does not identify downloadable implementation or trajectory artifacts, so independent reproduction cannot be classified as strong.

**Available artifacts**

- Detailed operational definitions for exposure, spans, credit windows, signals, aggregation, and costs.
- Named agent, memory-system, and judge versions or configurations.
- Task ordering, execution limits, bootstrap procedure, judge budgets, and resource-use totals.
- Saved reports are stated to retain resolved settings, prompt hashes, conversations, validation attempts, and rollbacks.

**Missing pieces**

- No repository, code release, data archive, prompt package, trajectory bundle, or executable reproduction instructions are identified in the supplied document.
- Exact pinned server revision and full MemGovern corpus are not supplied in the blocks.
- Provider rates, infrastructure details, and complete run manifests needed to reproduce monetary cost are not supplied.
- No human-labeled validation set or inter-rater agreement results are provided.

## AIDB assessment

- Novelty: High conceptual novelty in evaluating delivered memory at its point of use and separating availability, novelty, influence, and consequence from terminal success. The contribution is best understood as an auditable observational diagnostic, not causal credit assignment.
- Usefulness: High for auditing agent-memory pipelines, identifying irrelevant or repeated delivery, locating harmful recurring items, and comparing benefit against delivered-text cost. Deployment decisions should retain outcome tests and human validation because judge correctness and causal utility are unresolved.
- Confidence: medium
- Recommended action: read
- Rationale: The paper offers a rigorous, actionable framework and reveals consequential patterns hidden by outcome metrics. Confidence is moderated by unmeasured human agreement, observational attribution, benchmark overlap, a single experimental stack, and incomplete artifact availability.

## Uncertainties

- **The semantic accuracy and calibration of the agentic judge are unknown.** — Core relevance, influence, benefit, and harm counts may change under human review or a different judge even when evidence coverage is complete.
  - Evidence: [b00260-2ceda319d7] “Agreement with human judgments has not been measured in this evaluation.”
- **A substantial fraction of acted-on entries had effects that remained undetermined.** — Comparisons of benefit and harm condition on incomplete consequence attribution, particularly for TencentDB, and low all-entry uncertainty shares can obscure this conditional uncertainty.
  - Evidence: [b00318-bfa46bf15a] “213 of 714 acted-on entries, or 29.8%, have undetermined effects.”
- **The prevalence of benchmark-source overlap in the full MemGovern corpus is unknown.** — Unmeasured overlap could affect both beneficial and harmful delivery profiles and weaken fair cross-system comparison.
  - Evidence: [b00353-7b757fa636] “This targeted review establishes specific overlaps; their prevalence across the full corpus remains unmeasured.”
- **The global-memory option in one Mem0 configuration was never used.** — The experiment cannot determine whether cross-repository global recall would improve or degrade utility, despite naming a separate global configuration.
  - Evidence: [b00300-53ac16d6e0] “Mem0 (L+G) also permits an explicitly requested global scope, but none of its 3,997 searches used that scope.”

## Open questions

- How closely do MemUse judgments agree with expert human annotations at the entry, span, and episode levels?
- Do the profile rankings persist across different agent models, judge models, task domains, and randomized task orders?
- How much of MemGovern’s apparent efficiency remains after removing every item derived from benchmark-problem histories?
- Can interventions that remove repeated or irrelevant entries preserve beneficial selection pathways while improving task success and cost?
- Which unresolved effects can be converted into determined effects through better recording or targeted counterfactual reruns?

## Proposed AIDB experiments

- **Hypothesis:** Human reviewers will substantially agree with MemUse on relevance and influence, but agreement will be lower for improved versus harmed observed effects.
  - Baseline: The paper’s accepted agentic-judge labels on a stratified sample covering every memory system, usage label, and uncertainty category.
  - Primary metric: Human–judge agreement and class-wise F1 for relevance, influence, and observed effect, with adjudicated expert labels as reference.
  - Stop condition: Stop adoption as a quantitative benchmark if any consequential effect class has F1 below a pre-registered threshold or if system rankings reverse under adjudicated labels.
- **Hypothesis:** Suppressing restatements and filtering low-relevance entries will reduce delivered-text cost without reducing beneficial-entry coverage or resolve rate.
  - Baseline: Each original memory configuration with its reported delivery policy and unchanged agent.
  - Primary metric: Beneficial episodes per million delivered tokens, jointly reported with resolve-rate difference and harmful-episode coverage.
  - Stop condition: Stop if the intervention’s resolve-rate interval crosses the pre-registered harm margin, harmful coverage rises, or beneficial-episode coverage falls beyond the non-inferiority margin.
- **Hypothesis:** MemGovern’s relative token efficiency will decrease after removing all cards linked to benchmark-problem development histories, while its qualitative advantage over Mem0 may or may not persist.
  - Baseline: The original fixed MemGovern corpus and retrieval policy on the identical task protocol.
  - Primary metric: Difference in beneficial entries per million delivered tokens after corpus decontamination, with relevance, harm, and resolve rate as safeguards.
  - Stop condition: Stop once the complete corpus audit is finished and confidence intervals can distinguish retention or loss of the pre-registered efficiency advantage.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:59:42.491059+00:00`
- Document SHA-256: `b06665b67af02067de8103bda32b86b219f370d5487a5e453e81a47f4f40c66e`
- Metadata SHA-256: `10d2e1c5c263ef324d07d2c1ef00d7e55f0e9216a5e06f8f4cb676bbc976deb2`
- Blocks: 361
- Deterministic repair attempts: 0
