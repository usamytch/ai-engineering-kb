# Surfacing Disagreement Beats Resolving It: A Gated Ablation Study of Provenance-Weighted Memory for Multi-Agent Debate

## Executive summary

The paper tests whether shared memory should collapse contradictory facts before multi-agent debate or expose the ranked conflict set to agents. Its controlled ablation supports surfacing: in the reachable-conflict regime it substantially improves F1 and reduces successful poisoning at similar token cost. The initial protocol concealed much of the effect because its retrieval cap made most planted contradictions unreachable; the authors disclose and remeasure this confound. Write-time trust gating and router provenance features become harmful when conflicts are reachable. Evidence is unusually transparent, but generalization remains constrained by one model family, two corpora, synthetic attacks, a single judge, and memories that fit within the full context window.

## Problem

**Statement.** Shared-memory systems commonly reconcile competing facts and return one winner before debate begins. The paper asks whether, with debate, budget, and retrieved evidence held fixed, storage should instead preserve a ranked set of contradictory claims and delegate adjudication to the agents.

**Why it matters.** Premature reconciliation can erase useful disagreement and creates an attack surface when an adversarial writer controls the signal used for tie-breaking. The question is consequential because debate already supplies explicit reasoning machinery that could compare the claims.

**Scope.** The study concerns a multi-agent question-answering pipeline with shared episodic and graph memory, provenance-labelled contradiction injection, fixed-budget retrieval, three agents, two debate rounds, and one judge. It evaluates five switchable memory mechanisms across LoCoMo and a reduced HotpotQA document port under the stated write-adversary model.

## Method

DebateGraph provides a common read/write/snapshot contract across four retrieval modes. Dialogue turns or document sentences become episodes; an LLM extracts provenance-linked triples into a bi-temporal store. At query time, vector, graph, or hybrid retrieval operates under a hard context budget. A resolver groups retrieved edges sharing a subject and relation but asserting distinct objects, ranks them by validity, trust, and cross-writer support, then either passes only the winner or the complete ranked conflict set. Each ablation changes one switch while downstream debate and judging remain fixed. Effects are evaluated with paired item-level comparisons, bootstrap confidence intervals, Wilcoxon tests, and exact McNemar tests for attack discordance.

### Key components

- A provenance-preserving edge representation with writer, validity interval, trust, source type, support, and links back to source episodes.
- Four retrieval modes—vector, one-hop, multi-hop, and hybrid—behind a shared interface and a fixed prompt budget.
- A write trust-gate based on groundedness, graph compatibility, relation compatibility, writer credibility, and a contradiction penalty.
- A conflict resolver that detects distinct objects for a shared subject–relation key and compares collapse against surface.
- DebateMem-Conflict, which injects later, type-consistent contradictory objects under a non-debating writer.
- Pre-declared phase gates and single-mechanism ablations, followed by a disclosed retrieval-reachability correction.

### Assumptions

- Only retrieved edges can form a conflict set; therefore mechanism exposure depends on retrieval reachability.
- Corpus transcript facts are treated as ground truth and bypass write admission.
- Single-valued relations define eligible contradictions; simultaneous assertions are treated as elaborations rather than conflicts.
- The adversary can write and choose timestamps but cannot modify stored edges, inspect agent state, or alter prompts.
- All agents in a round receive the same retrieved context, and one judge converts the debate into the scored answer.
- The primary establishment rule is a paired bootstrap confidence interval excluding zero; subgroup analyses are pre-specified around poisoned and actually discriminating items.

## Main claims

- **The paper claims that surfacing the whole ranked conflict set, rather than collapsing it to one stored winner, improves final-answer accuracy and poisoning robustness when contradictions are reachable.**
  - Evidence: [b00054-cd35f66baf] “surfacing raises F1 from 0.116 to 0.456 (Δ=+0.340, CI [+0.267,+0.414], Wilcoxon p<10−4)”; [b00054-cd35f66baf] “cuts attacks from 22 to 7 of 122”
- **The authors claim that the surfacing effect is not confined to one retrieval substrate and directionally transfers from conversational memory to document memory.**
  - Evidence: [b00049-0cd7920c78] “Two independent substrates, same direction, both CIs excluding zero.”; [b00057-1b731cef98] “We claim a directional replication of the accuracy effect on a second corpus”
- **The paper claims that the write trust-gate is structurally mis-specified for attacks composed from already-known entities and can harm accuracy once conflicts reach retrieval.**
  - Evidence: [b00045-54ec66f33f] “100% of poison objects are entities already in the graph, against 53% of gold objects.”; [b00047-f2efa71d35] “enabling the gate costs 0.075 F1 (CI [−0.133,−0.018], Wilcoxon p=0.039)”
- **The authors explicitly do not claim state-of-the-art performance; full context remains the strongest accuracy baseline on the studied corpus.**
  - Evidence: [b00009-cc763efa5e] “The contribution is not a new state of the art”; [b00062-feab1ead36] “On this corpus that is the right baseline and we do not beat it.”
- **The paper claims that mechanism evaluation must separately verify whether the mechanism was able to act, because the original retrieval cap strongly attenuated the measured effect.**
  - Evidence: [b00074-b08e8549fd] “Our pre-declared retrieval cap left three quarters of planted contradictions unretrievable”; [b00074-b08e8549fd] “A mechanism can only be measured where it is able to act”

## Results

- **In the reachable-conflict graph comparison, surfacing increased F1 from 0.116 to 0.456, a +0.340 change with 95% CI [+0.267,+0.414] and Wilcoxon p<10−4; successful attacks fell from 22 to 7 of 122, with exact McNemar p=0.0003.**
  - Context: This is the strongest controlled comparison: collapse and surface use the same retrieval pipeline and prompt budget, while every poisonable item is attacked at the higher candidate-edge cap. It establishes both accuracy and attack-success endpoints in this regime.
  - Evidence: [b00054-cd35f66baf] “surfacing raises F1 from 0.116 to 0.456 (Δ=+0.340, CI [+0.267,+0.414], Wilcoxon p<10−4)”; [b00051-454a3a1a2a] “∗ denotes a 95% bootstrap CI excluding zero.”; [b00054-cd35f66baf] “cuts attacks from 22 to 7 of 122”; [b00054-cd35f66baf] “McNemar exact p=0.0003”
- **The declared cap of 40 exposed only 12/51 poisoned items to a retrieved contradiction; reachability rose to 27/51 and 40/51 at larger caps. Accordingly, the graph surfacing contrast grew from +0.043 at cap 40 to +0.340 at cap 200.**
  - Context: This is both a validity threat and a useful diagnostic result. The cap ordered graph candidates without question relevance, so many identical prompts were tied by construction rather than demonstrating absence of treatment effect.
  - Evidence: [b00051-454a3a1a2a] “Every conflict-dependent contrast, at the pre-declared cap of 40 and again at 200, same paired procedure.”; [b00050-f862da9460] “rises 12/51→27/51→40/51 at caps of 40,100,200.”; [b00052-5ba9c0f47b] “surfacing, graph backend +0.043∗ +0.340∗ helps”
- **With contradictions reachable, enabling the write trust-gate cost 0.075 F1, with CI [−0.133,−0.018] and p=0.039, while attacks moved from 7 to 9 of 122. Its log showed 123 invalidations but only 3 rejections.**
  - Context: The gate was intended to reject poisoned writes, but most measured action came from supersession invalidation. This makes the negative result mechanistically informative rather than merely a failed threshold.
  - Evidence: [b00047-f2efa71d35] “enabling the gate costs 0.075 F1 (CI [−0.133,−0.018], Wilcoxon p=0.039)”; [b00047-f2efa71d35] “moves attacks the wrong way, 7→9 of 122.”; [b00047-f2efa71d35] “it fires 123 invalidations against 3 rejections.”
- **On HotpotQA’s discriminating subset, surface minus collapse was +0.111 with CI [+0.010,+0.232], whereas the all-item effect was +0.032 with CI [-0.005,+0.077]. Attack success changed from 3 to 2 of 67 with McNemar p=1.00.**
  - Context: This supports directional cross-corpus replication only for the pre-specified subset where a conflict actually entered context. It does not establish a full-sample accuracy effect or an attack-success reduction.
  - Evidence: [b00134-0937ddcb28] “ΔF1, all items +0.043∗ [+0.010, +0.082] +0.032 [-0.005, +0.077]”; [b00134-0937ddcb28] “ΔF1, discriminating +0.329∗ [+0.115, +0.572] +0.111∗ [+0.010, +0.232]”; [b00134-0937ddcb28] “attacks 5→3 of 51 3→2 of 67 McNemar exact p 0.63 1.00”
- **Full context achieved F1 0.503 on the multihop-temporal slice at 147,702 tokens per query, compared with vector retrieval at 0.304 and 6,405 tokens and graph retrieval at 0.154 and 11,199 tokens. Raising graph recall from 0.30 to 0.76 moved F1 only from 0.154 to 0.155.**
  - Context: The proposed memory configuration does not beat the full-context accuracy ceiling. The graph deficit persists after relieving candidate truncation, suggesting that triple presentation—not only evidence coverage—limits performance in this setup.
  - Evidence: [b00118-24f1d52c4e] “multihop-temp. full-context 0.503 0.20 147,702 0.0034 1.00 0.0 vector 0.304 0.10 6,405”; [b00118-24f1d52c4e] “graph (k-hop) 0.154 0.08 11,199 0.0137 0.30 15.8”; [b00043-d2d7b9d6e2] “recall rises 0.30→0.76 while F1 moves 0.154→0.155”

## Experimental evaluation

### Datasets

- LoCoMo conversational memory: multihop-temporal and single-hop slices, with stratified question sets and extracted episodes and edges.
  - Evidence: [b00032-5973d957b3] “LoCoMo (Maharana et al., 2024): 10 conversations, 5,878 episodes, 9,769 edges”; [b00032-5973d957b3] “n=100 stratified items each.”
- HotpotQA-distractor document-memory port, sampled from bridge questions; time is represented by a synthetic ingestion clock, so the replication tests a reduced mechanism.
  - Evidence: [b00131-17a98d246a] “5,918 bridge questions are available; we sample n=100 with a fixed seed.”; [b00132-ad5ffbcf3f] “the replication validates a reduced form of the mechanism.”
- DebateMem-Conflict, a deterministic synthetic contradiction-injection set restricted to questions whose answer is expressible as a single-valued edge object.
  - Evidence: [b00033-1d9a4185c2] “122 of 603 items (20.2%) qualify.”; [b00033-1d9a4185c2] “we synthesise a contradicting edge on the same (h,r)”

### Baselines

- Full-context input, which omits no LoCoMo content and acts as the accuracy and high-cost ceiling.
  - Evidence: [b00042-4faaa1f61a] “Full context recovers essentially all gold evidence at a 32K budget and omits nothing”
- Always-vector retrieval, described in the ablation table as a Mem0-style baseline.
  - Evidence: [b00140-99914c6a36] “vector-only (Mem0-style) 0.374 — — 0.098 0.47”
- Always-graph retrieval, described as a Zep/G-Memory-style baseline.
  - Evidence: [b00140-99914c6a36] “graph-only (Zep/G-Memory-style) 0.131 — — 0.039 0.26”
- Trust-only retrieval, heuristic routing, and contextual-bandit routing under several cost weights.
  - Evidence: [b00137-27be2b07bc] “heuristic router 0.321 7,584 0.0423 0.059”; [b00137-27be2b07bc] “bandit λ=4 0.384 6,718 0.0572 0.078”
- Cross-framework execution inside AutoGen, used to test transfer of ordering rather than superiority.
  - Evidence: [b00148-1d04604e46] “We therefore claim transfer of the memory abstraction and its behavioural signature, and explicitly not a gain”

### Metrics

- Token-level final-answer F1 and exact match.
  - Evidence: [b00017-aecbf1254d] “scored by token-F1 against gold.”; [b00118-24f1d52c4e] “Slice Backend F1 EM tokens/q acc/1K ev. rec. omit”
- Attack success rate and exact McNemar tests on discordant paired outcomes.
  - Evidence: [b00036-dd7a09f712] “exact McNemar on attack-success discordance.”
- Token cost per query and accuracy per thousand tokens.
  - Evidence: [b00137-27be2b07bc] “Policy F1 tokens/q acc/1K ASR mode selection”
- Gold-evidence recall, omitted blocks, conflict-resolution F1, latency, and conflict reachability.
  - Evidence: [b00117-4fd3b0b8e0] ““omit” is blocks dropped at the budget ceiling; “ev. rec.” is gold-evidence recall”; [b00140-99914c6a36] “confl. F1 ASR ev. rec.”
- Paired uncertainty analysis using bootstrap confidence intervals and two-sided Wilcoxon tests.
  - Evidence: [b00036-dd7a09f712] “10,000-resample bootstrap (Efron, 1987) with two-sided Wilcoxon”

### Ablations

- Conflict surface versus collapse, with all downstream debate components fixed.
  - Evidence: [b00025-df515ff9b1] “collapse passes only the top-ranked claim, surface passes the whole ranked set with its provenance.”
- Write trust-gate, including its admission and invalidate-on-supersede behavior.
  - Evidence: [b00028-945849ebf7] “Switch: trust_gate, which governs admission and invalidate-on-supersede”
- Router provenance features, trust-weighted retrieval, and temporal validity in conflict ranking.
  - Evidence: [b00052-5ba9c0f47b] “router provenance features −0.002 −0.096∗ harms trust-weighted retrieval −0.059 −0.065 inert temporal validity in ranking +0.001 −0.004 inert”
- Round-level snapshot isolation versus a lock-protected store.
  - Evidence: [b00144-a9a54d511f] “MVCC and a single lock-protected store produce serial-equivalent accuracy”
- Retrieval substrate and routing policy: vector, graph, heuristic router, and bandit router.
  - Evidence: [b00136-6bad8276e3] “No policy beats always-vector on acc/1K, so the pre-declared gate fails.”

### Negative results

- Graph retrieval failed its pre-declared benefit threshold and substantially underperformed vector retrieval and full context.
  - Evidence: [b00042-4faaa1f61a] “it loses 0.150 F1 (CI [−0.216,−0.085], p<10−4)”
- The original write gate rejected none of the injected poisoned writes; three repairs raised this only slightly.
  - Evidence: [b00045-54ec66f33f] “the gate rejects 0/122 poisoned writes.”; [b00045-54ec66f33f] “together they move rejection to 3/122.”
- At the reachable cap, router provenance features were harmful rather than neutral.
  - Evidence: [b00055-de54fed401] “router’s provenance features (−0.096, CI [−0.149,−0.043], p=0.030).”
- Trust-weighted retrieval, temporal validity, and the full-system write-gate ablation remained inert across both cap regimes.
  - Evidence: [b00052-5ba9c0f47b] “trust-weighted retrieval −0.059 −0.065 inert temporal validity in ranking +0.001 −0.004 inert write gate (full-system ablation) +0.012 +0.004 inert”
- The learned router beat the heuristic but not always-vector on accuracy efficiency; its cost-weight sweep did not yield a meaningful frontier.
  - Evidence: [b00060-f726eecf4a] “but not always-vector (+0.010, CI [−0.013,+0.040], marginally lower acc/1K).”; [b00142-67aa864a3a] “The λ sweep is flat”
- Snapshot isolation preserved serial-equivalent accuracy but was not load-bearing in the tested debate topology.
  - Evidence: [b00144-a9a54d511f] “The mechanism is nonetheless not load-bearing at this debate topology”


## Limitations

- Results rely on one model family, so model-specific behavior cannot be separated from mechanism-level behavior.
  - Evidence: [b00069-228d07913f] “All results use gpt-oss-120b, so we cannot separate model-specific from mechanism-level effects.”
- All LoCoMo memories fit inside the context window; retrieval is a cost choice, not a necessity, and true overflow behavior is untested.
  - Evidence: [b00070-c2bb200959] “Every LoCoMo partition fits in 32K tokens”; [b00070-c2bb200959] “we do not exhibit the regime where memory genuinely overflows”
- The attack benchmark covers only answers represented as single-valued edge objects and uses template-generated contradictions, narrowing question type and linguistic realism.
  - Evidence: [b00071-bbce53b714] “DebateMem-Conflict covers the 20.2% of items whose answers are single-valued edge objects”; [b00071-bbce53b714] “Injections are template-generated for determinism”
- A single judge mediates between debate and the answer metric, leaving judge sensitivity unmeasured.
  - Evidence: [b00071-bbce53b714] “A single judge sits between memory and score.”
- Attack-success reduction lacks statistical establishment at the original cap and on HotpotQA because few attacks land.
  - Evidence: [b00068-8627b8ef6e] “not at cap 40 (5→3 of 51, p=0.63) nor on HotpotQA (3→2 of 67, p=1.00)”
- Some experiments were not rerun in the reachable regime; the authors judge the retrieval cap irrelevant to them rather than verifying that judgment.
  - Evidence: [b00067-2337724b97] “We judge those unaffected rather than having verified it”
- The HotpotQA port substitutes ingestion order for event time, so it does not replicate genuine bi-temporal memory behavior.
  - Evidence: [b00132-ad5ffbcf3f] “the replication validates a reduced form of the mechanism.”
- Only one external multi-agent framework was integrated; the second planned framework was not attempted.
  - Evidence: [b00148-1d04604e46] “We integrated one external framework, not the two we set out to”

## Reproducibility

**Status:** partial

Documentation and logged artifacts are unusually extensive, and full-payload caching should reproduce the reported executions closely. The rating remains partial because this review is restricted to the supplied text: the actual release cannot be inspected, no concrete artifact location appears, and exact environment and execution commands are not shown. Replaying cached outputs is strong result verification but is not equivalent to independently regenerating model behavior.

**Available artifacts**

- The paper states that code, per-query JSONL for all runs, the attack set, gate outputs, significance outputs, and corpus-validation outputs are released.
- Every LLM call is cached on the full request payload for byte-identical replay.
- Core corpora, attack construction, model, sampling parameters, budget, retrieval cap, agent and round counts, and paired statistical procedure are described.
- Scripts are said to recompute tables and rebuild the harness and attack set deterministically.

**Missing pieces**

- The supplied document does not expose a concrete repository URL or artifact identifier, so availability cannot be independently checked from the provided material.
- Exact runnable commands and a complete environment specification are not present in the supplied blocks.
- The main model endpoint and local embedding hardware are described operationally but not with a fully portable infrastructure recipe.
- The stochastic study uses cached calls; the supplied blocks do not demonstrate independent fresh-call replication across random seeds or alternative serving environments.

## AIDB assessment

- Novelty: The central contribution is a clean division-of-labor test: storage either adjudicates a contradiction or exposes it to an existing debate reasoner. The strongest novelty is experimental design and diagnosis rather than a new model architecture—independent mechanism switches, pre-declared gates, explicit reachability instrumentation, and publication of a correction that enlarges both positive and negative effects.
- Usefulness: High for designers of shared agent memory and retrieval evaluations. The evidence argues for retaining provenance-labelled alternatives until a reasoning component sees them, and for instrumenting whether an ablated mechanism actually fires. It also warns that topology-based write plausibility and provenance-heavy routing can be actively harmful. Direct production adoption should remain conditional because the evaluation is narrow and full context still wins on accuracy.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled surface-versus-collapse comparison, paired uncertainty analysis, disclosure of the cap confound, and consequential negative results make the paper decision-relevant. However, a one-model evaluation, synthetic entity-level attacks, one judge, reduced temporal replication, and absence of genuine context overflow limit confidence in broad deployment claims. The work merits close reading and targeted internal replication before adoption.

## Uncertainties

- **It is unclear whether surfacing remains beneficial with other model families, judge models, or debate topologies.** — The mechanism depends on agents recognizing and resolving explicit disagreement; this capability may vary materially across models and orchestration designs.
  - Evidence: [b00069-228d07913f] “the model axis is untested”
- **The benefit under genuinely overflowing long-term memory is unresolved.** — That is the deployment regime where retrieval and storage reconciliation are unavoidable, rather than optional cost optimizations.
  - Evidence: [b00070-c2bb200959] “we do not exhibit the regime where memory genuinely overflows”
- **Robustness to fluent, adaptive, multi-write, or provenance-spoofing adversaries is unknown.** — Template-generated single-edge contradictions may underrepresent realistic attacks that manipulate several related claims or mimic trusted sources.
  - Evidence: [b00071-bbce53b714] “they test contradiction handling rather than fluent adversarial paraphrase.”
- **The causal contribution of each provenance field shown to agents is not isolated.** — The full surfaced representation includes writer, trust, evidence count, and supersession status, but the evidence does not identify which fields help or whether raw contradictory text alone suffices.
  - Evidence: [b00029-540b640527] “the whole ranked set enters the prompt with writer, trust, evidence count and supersession status”
- **The all-sample cross-corpus effect remains unresolved despite a positive discriminating-subset result.** — A practical system must handle the full query distribution, including cases where retrieval fails to surface a conflict.
  - Evidence: [b00057-1b731cef98] “On the full sample the HotpotQA interval contains zero.”

## Open questions

- Does conflict surfacing outperform collapse with multiple independently served model families and multiple judge models?
- Which surfaced fields—alternative claim text, writer identity, trust score, support count, or supersession state—cause the gain?
- How does the mechanism behave when stored memory genuinely exceeds every available context window?
- Can retrieval be optimized directly for conflict reachability without degrading ordinary evidence relevance or increasing prompt cost?
- Does the result survive adaptive attacks involving paraphrases, coordinated writers, provenance spoofing, or several mutually supporting false edges?
- Would a relative candidate-versus-incumbent admission rule avoid the trust-gate failure without suppressing truthful first mentions?

## Proposed AIDB experiments

- **Hypothesis:** Conflict surfacing improves paired answer quality and attack robustness across model families rather than only for the reported model.
  - Baseline: For each of at least two additional independently served model families, compare collapse with surface using identical retrieved sets, prompts, budgets, attacks, and judges; include a judge-swap analysis.
  - Primary metric: Paired token-F1 difference on conflict-reachable items, with attack-success discordance as a co-primary safety endpoint and bootstrap confidence intervals reported per model.
  - Stop condition: Stop and reject model-independent generalization if the confidence interval includes zero for most added model families, if any adequately powered family shows a significant reversal, or if judge swaps change the direction.
- **Hypothesis:** The gain comes primarily from exposing competing claim content, while provenance annotations add smaller or inconsistent value.
  - Baseline: Compare collapse, unlabelled competing claims, claims plus writer, claims plus support count, claims plus trust, claims plus supersession state, and the full surfaced representation under identical retrieval.
  - Primary metric: Paired token-F1 on discriminating items, supplemented by prompt tokens and attack success rate.
  - Stop condition: Stop adding provenance fields when no field yields a confidence interval excluding zero over unlabelled competing claims, or when its accuracy gain is offset by a pre-declared token-cost threshold.
- **Hypothesis:** Surfacing remains beneficial when memory exceeds the model context window and under adaptive, fluent poisoning.
  - Baseline: Construct long-memory partitions that necessarily overflow context; compare collapse and surface under matched retrieval, then repeat with template attacks, fluent paraphrases, coordinated multi-writer attacks, and provenance-spoofing attacks.
  - Primary metric: Paired token-F1 and attack success rate on items where both truthful and poisoned alternatives are demonstrably retrieved into the conflict set.
  - Stop condition: Stop and narrow the claim if surfacing fails to improve F1 with a confidence interval excluding zero in the overflow regime, or if any adaptive attack class eliminates the robustness benefit at matched cost.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:06.986667+00:00`
- Document SHA-256: `34c9c8be93673e6ca76e58b4b46aa7136f8309133cca746d5f14149718736564`
- Metadata SHA-256: `6844046e30095764015a04e0f7742fd892b3df15dcb1c28b188fb70d2bd318da`
- Blocks: 486
- Deterministic repair attempts: 0
