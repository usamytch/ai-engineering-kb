# Who Remembers What? Multi-Granularity Memory Extraction for Multi-User, Multi-Agent Interaction

## Executive summary

MixUA routes distilled trajectory lessons into Pair, User, Agent, or Global memory, using isolated reusable/protected streams and optional store review. CrossLearnBench evaluates utility, preference retention, and synthetic privacy leakage across heterogeneous users and agents. Controlled scheduled experiments favor reviewed MixUA over no memory and single-scope stores; random assignment also shows transfer to previously unseen tasks. Scope removal and masking support distinct roles for Global and User memory, while targeted probes motivate Agent and Pair scopes. The evidence is extensive but costly, model-dependent, largely synthetic, and weak at population scale: scaling uses one seed, utility loses its edge over Global-only at the largest tested population, and real consent, deletion, adversarial contributors, and hierarchical audiences are untested.

## Problem

**Statement.** Shared experiential memory for heterogeneous agents must decide both where a lesson is useful and where it is safe to disclose; indiscriminate pooling can misroute user-specific knowledge or expose private information.

**Why it matters.** Cross-user learning can broaden the benefit of a discovered lesson, but deployment requires personalization and confidentiality to survive sharing rather than treating utility and privacy as separate afterthoughts.

**Scope.** The paper studies independent synthetic users paired with fixed LLM-harness configurations. It addresses learned audience routing across four Cartesian scopes, not organizational hierarchies, arbitrary groups, real-user governance, or base-model retraining.

## Method

MixUA converts graded user-agent trajectories into structured, scoped memory. A splitter separates reusable from protected evidence; isolated writers create situation-conditioned lessons with provenance; protected entries are restricted to Pair or User memory. A periodic review can re-scope and merge entries. At inference, each pair sees its own Pair memory, its user's User memory, its agent's Agent memory, and Global memory, retrieved by situation–prompt embedding similarity under separate character budgets or exposed as searchable files.

### Key components

- Four authorized-audience scopes: Pair, User, Agent, and Global, defined by whether access is specific or open along user and agent axes.
- A formal safety/usefulness constraint requiring an entry's authorized audience to remain within both its generalization scope and disclosure boundary.
- Dual-stream writing with isolated reusable and protected writers; scope labels derive from the stream rather than trusting the writer to self-label privacy.
- Structured entries containing a situation, lesson, scope, and provenance over originating tasks, pairs, rounds, and outcomes.
- Optional round-level store review that re-scopes entries with the full store in view and merges entries within destinations.
- Per-scope retrieval by cosine similarity between embedded situations and task prompts, with a file-based retrieval variant.
- CrossLearnBench, which wraps established tasks with synthetic preferences and planted private facts while retaining source task environments, instructions, and verifiers.

### Assumptions

- Users are independent principals; every private fact belongs to exactly one user.
- Agents are treated as independent, fixed LLM-harness configurations.
- The reusable/protected splitter and privacy judge can adequately recognize sensitive or identifying content.
- A four-scope lattice is sufficient for the tested audience patterns.
- Synthetic preferences and planted private files are useful proxies for personalization and privacy behavior in deployment.
- Provider and harness defaults are acceptable experimental settings despite unseeded model sampling.

## Main claims

- **The paper frames cross-learning as per-entry audience selection constrained jointly by usefulness and disclosure safety.**
  - Evidence: [b00022-2371cdd607] “Each entry has an authorized audience Aud⁡(e)⊆𝒰×𝒜, the set of user-agent pairs permitted to access it.”; [b00023-1ed28bc80c] “Aud⁡(e)⊆𝒢⁡(e)∩𝒟⁡(e), (1)”
- **The four scopes provide different access paths rather than merely four semantic labels.**
  - Evidence: [b00026-61abb690e4] “Pair ({u}×{a}) is read only by the user-agent pair itself, User ({u}×𝒜) by the user with any agent, Agent (𝒰×{a}) by the agent with any user, and Global (𝒰×𝒜) by everyone.”
- **Privacy isolation is architectural: protected evidence is handled by an isolated writer and cannot be written into cross-user scopes.**
  - Evidence: [b00031-f4ea7d0833] “we split each trajectory into a reusable and a protected stream and send them to two isolated writers”; [b00031-f4ea7d0833] “a protected entry can land only in its owner’s User or Pair memory.”
- **The benchmark jointly tests task utility and user-layer behavior that ordinary task verifiers omit.**
  - Evidence: [b00038-4992d29839] “CrossLearnBench has two layers. (1) Tasks from established benchmarks test agents’ task success, and (2) a user layer tests what memory retains and leaks”
- **The experimental design includes both online evolution and frozen-store tests, allowing transfer during learning to be distinguished from post-training memory use.**
  - Evidence: [b00128-23a6715483] “The held-out stage complements the evolution stage rather than replacing it.”; [b00128-23a6715483] “The held-out stage then freezes each store after round 3”

## Results

- **In scheduled assignment, reviewed LLM MixUA achieved a reported pass rate of 89.8±1.3 and a gain of +16.3±1.1 percentage points over no memory, versus 85.5±1.6 and +11.5±0.6 for Global-only. Its cross-pair gain was +13.9, and its evolution and held-out preference retention were 89 and 90.**
  - Context: This is the strongest main controlled comparison, averaged over three runs. It supports the value of multi-scope routing over a single broadcast store, although MixUA also consumed more delivered memory and writing cost.
  - Evidence: [b00046-2b9b88f24b] “Global only 85.5±1.6 +11.5±0.6∗∗ +8.9∗∗ 11 10”; [b00046-2b9b88f24b] “MixUA (LLM) + review 89.8±1.3 +16.3±1.1∗∗ +13.9∗∗ 89 90”
- **Under random assignment, MixUA passed 82.3% versus 70.5% without memory, a +11.4-point gain. On 526 first attempts among 821 attempts, its gain was +10.1, compared with +5.5 for Global-only.**
  - Context: This comparison is consequential because first-attempt tasks lack a task-specific lesson from an earlier pair, so improvement must transfer from other tasks. The two random-assignment seeds were pooled.
  - Evidence: [b00153-70112059dc] “No memory 70.5 – – – – 11 12 n/a 10 18.2 0 0.41”; [b00153-70112059dc] “Global only 79.1 +8.5∗∗ +5.5∗∗ +15.9∗∗ +13.0∗∗”; [b00153-70112059dc] “MixUA (LLM) + review 82.3 +11.4∗∗ +10.1∗∗ +12.5∗∗ +15.1∗∗”; [b00153-70112059dc] “n=821 n=526 n=112 n=179”
- **Scope removal showed complementary roles: removing Global reduced overall gain from 15.3 to 9.0 and cross-pair gain from 13.0 to 4.6, while removing User reduced preference retention from 90% to 81%. Targeted probes found that removing Pair increased work-context leakage from 22% to 95%, and removing Agent reduced crowded-store pass rate from 89% to 40%.**
  - Context: The broad ablation most strongly supports Global and User. Pair and Agent changed aggregate results less, so the paper introduced constructed scope probes to expose their intended failure modes; those probes are informative but narrower and more synthetic than the main benchmark.
  - Evidence: [b00071-d9d4d7982a] “removing Global causes the largest drop, cutting Δ from 15.3 to 9.0 points and Δcross from 13.0 to 4.6.”; [b00071-d9d4d7982a] “removing User causes the largest drop (90% to 81%).”; [b00071-d9d4d7982a] “Without Agent, crowd pass falls from 89% to 40%”; [b00071-d9d4d7982a] “without Pair, leak rises from 22% to 95%.”
- **The strongest planted-private-fact evidence reports 0 findings among 268215 probes at 100 users, while smaller MixUA scaling runs found 2/9753 and 3/57913. However, preference leakage remained 3.0% at 100 users, and privacy evaluation used synthetic personas rather than real records.**
  - Context: The exact-match fact probes indicate very low observed forbidden-scope leakage, but zero observed findings is not proof of zero risk. Preference leakage is a separate privacy measure and is materially higher.
  - Evidence: [b00158-20e192d6ce] “MixUA (LLM) + review 80.3 +8.9∗∗ +8.0∗∗ 89 89 3.8 2/9753”; [b00158-20e192d6ce] “MixUA (LLM) + review 81.8 +10.9∗∗ +8.4∗∗ 82 74 3.5 3/57913”; [b00158-20e192d6ce] “MixUA (LLM) + review 78.1 +5.8∗∗ +4.4 78 45 3.0 0/268215”; [b00158-20e192d6ce] “100 No memory 72.0”; [b00086-43a914dc3e] “All users and personal facts in this study are synthetic”
- **Scale is a notable negative result: with 100 users, MixUA reached a 78.1 pass rate and +5.8 gain, below Global-only at 79.4 and +7.3; first-attempt gain was +4.4 for MixUA versus +6.2 for Global-only. The scaling experiment used one seed per size.**
  - Context: This weakens the claim that learned four-scope routing already scales better than broadcast memory. Preference retention still favored MixUA, so the result is a utility–personalization trade-off rather than a uniform failure.
  - Evidence: [b00158-20e192d6ce] “Global only 79.4 +7.3∗∗ +6.2∗∗ 11 11 0.1 0/92160”; [b00158-20e192d6ce] “MixUA (LLM) + review 78.1 +5.8∗∗ +4.4 78 45 3.0 0/268215”; [b00158-20e192d6ce] “100 No memory 72.0”; [b00159-9f54f54493] “one seed per size”

## Experimental evaluation

### Datasets

- CrossLearnBench draws tasks from AutoCodeBench, FeatureBench, SpreadsheetBench (verified), SWT-Bench (verified), USACO, Terminal-Bench 2.0, and VMax Tasks.
  - Evidence: [b00040-2e34f9b5ee] “We source tasks from seven established datasets”; [b00040-2e34f9b5ee] “AutoCodeBench (Zhou et al., 2026a), FeatureBench (Zhou et al., 2026b), SpreadsheetBench (verified)”; [b00040-2e34f9b5ee] “SWT-Bench (verified) (Mündler et al., 2024), USACO (Shi et al., 2024), Terminal-Bench 2.0”; [b00040-2e34f9b5ee] “and VMax Tasks (VMax AI, 2026).”
- Scheduled evaluation uses evolution and disjoint held-out tasks; random evaluation samples from a larger task pool.
  - Evidence: [b00185-c7d40d01cc] “Total 178 20 513 140”; [b00187-95a5e12d7f] “Held-out task ids are disjoint from evolution ids.”; [b00054-f8416f5172] “each round draws 60 tasks from a 546-task pool”

### Baselines

- No memory and four scope-pinned stores: Pair-only, User-only, Agent-only, and Global-only.
  - Evidence: [b00050-7b28c87912] “We compare no memory, four single-scope stores (Global-only, User-only, Agent-only, and Pair-only)”
- MixUA variants use either an LLM or agentic writer, each with and without periodic store review.
  - Evidence: [b00050-7b28c87912] “MixUA with an LLM or a Codex agent as memory writer, each with and without store review”
- Additional controls vary retrieval budget, replace prompt retrieval with searchable files, mask visible scopes, shuffle owners, or restate preferences.
  - Evidence: [b00052-63d050ee3e] “masking which memory is visible (none, each scope alone, all scopes, a shuffled user’s scopes, or the preferences restated as a ceiling).”; [b00046-2b9b88f24b] “10k char retrieval limit 85.3±1.4”; [b00046-2b9b88f24b] “file-based memory 87.2±2.3”

### Metrics

- Utility: pass rate under each source benchmark's verifier; paired gains are reported in percentage points.
  - Evidence: [b00056-f7379e35fc] “utility, the pass rate under each source benchmark’s verifier”; [b00056-f7379e35fc] “Gains are in percentage points (pp)”
- Personalization: the rate of satisfied document-preference checks after the initial statement is withdrawn.
  - Evidence: [b00056-f7379e35fc] “preference retention, the rate of satisfied document checks after the round-1 statement is withdrawn”
- Privacy: forbidden-scope planted-fact findings and cross-user preference findings; exposure is separately tracked by whether planted files are opened.
  - Evidence: [b00056-f7379e35fc] “the share of memory probes finding a planted private fact in a forbidden scope or a user’s preference in another user’s memory”; [b00042-cca67989d4] “We then measure exposure, how often the agent opens a planted file, and leakage”
- Secondary measures include context size, turns, cost, efficiency, significance, and held-out transfer.
  - Evidence: [b00056-f7379e35fc] “Table 9 adds context size, cost, and efficiency.”; [b00056-f7379e35fc] “exact McNemar significance marked ∗ p<0.05 and ∗∗ p<0.01.”

### Ablations

- Remove one scope at a time while allowing remaining scopes to encode conditional substitutes.
  - Evidence: [b00071-d9d4d7982a] “we test scope combinations by removing one scope at a time from MixUA (LLM)”; [b00071-d9d4d7982a] “the remaining scopes can still record what the missing scope would have held.”
- Mask scopes on frozen held-out stores to locate task knowledge and preferences.
  - Evidence: [b00073-3eaf68a0ee] “show the agent one scope, all scopes, or a shuffled user’s memory”
- Vary retrieval budget and compare embedding retrieval with file-based memory.
  - Evidence: [b00075-799cdd0be0] “Varying the retrieval budget rules this out”; [b00075-799cdd0be0] “Replacing retrieval with searchable files”
- Compare LLM and agentic writers, with and without store review.
  - Evidence: [b00198-190bbbdadf] “MixUA (LLM) all four LLM off MixUA (LLM) + review all four LLM LLM”; [b00198-190bbbdadf] “MixUA (agentic) all four agentic off MixUA (agentic) + review all four agentic agentic”

### Negative results

- At the largest user-scaling condition, MixUA did not outperform Global-only on utility or first-attempt gain.
  - Evidence: [b00158-20e192d6ce] “Global only 79.4 +7.3∗∗ +6.2∗∗”; [b00158-20e192d6ce] “MixUA (LLM) + review 78.1 +5.8∗∗ +4.4”
- Removing Agent or Pair changed aggregate benchmark measures relatively little, requiring targeted probes to establish their value.
  - Evidence: [b00071-d9d4d7982a] “we find that removing Agent or Pair changes relatively little.”
- File-based memory used more turns and retained fewer preferences than standard retrieval.
  - Evidence: [b00075-799cdd0be0] “agents take more turns (17.0 versus 13.9) and retain fewer preferences (75% versus 90%).”
- Some agent–condition combinations regressed, including Agent-only for the strongest no-memory agent.
  - Evidence: [b00134-3677d050de] “Claude Code-Opus-5 92.1 +0.7 +3.3 -1.3 +4.0 +3.3∗∗”


## Limitations

- The four scopes cannot express teams, departments, organizational hierarchies, shared projects, or secrets jointly owned by a group.
  - Evidence: [b00080-3efbfdb760] “Knowledge owned by a team is neither pair-level private nor global, which our privacy boundary rule cannot express.”
- Audience selection is restricted to one or all on each axis, forcing subset-valid lessons into scopes that are too narrow or too broad.
  - Evidence: [b00082-fbd487c862] “a lesson valid for a subset, such as one team or the agents built on one model, must sit either at User or Agent, where it reaches too few, or at Global, where it reaches too many.”
- Population scale is limited and review assumes the store can be read as a whole; both context competition and writing cost may become prohibitive.
  - Evidence: [b00084-5075331281] “our study has 5, 20, or 100 synthetic users, seven agents, and at most 546 tasks over eight rounds.”; [b00084-5075331281] “At global scale the store grows without bound”; [b00084-5075331281] “a review that reads the whole store no longer fits in one pass.”
- All users, facts, and preferences are synthetic, limiting ecological validity for real privacy behavior and user needs.
  - Evidence: [b00086-43a914dc3e] “All users and personal facts in this study are synthetic”; [b00084-5075331281] “real users bring richer needs and preference requirements.”
- Consent, inspection, deletion, and defenses against intentionally misleading contributors are required for deployment but not evaluated.
  - Evidence: [b00086-43a914dc3e] “a way for users to inspect and delete what was learned from them, and defenses against contributors who write misleading lessons on purpose”; [b00086-43a914dc3e] “we do not evaluate these mechanisms.”
- Observed low leakage does not establish deployment safety, particularly because the probes cover planted targets under a specified boundary contract.
  - Evidence: [b00086-43a914dc3e] “Low leakage in our probes does not justify deploying shared memory without access control and privacy review.”
- Model stochasticity is not seeded, and scaling results use only one seed, weakening precision for scale-dependent comparisons.
  - Evidence: [b00209-d6f0c8fcee] “user scaling seed 1”; [b00209-d6f0c8fcee] “model sampling is not seeded.”
- The system is expensive: memory-side processing dominates reported study cost, while table cost columns omit several memory components.
  - Evidence: [b00213-3efd07ef99] “The memory side accounts for 79% ($55.4k)”; [b00213-3efd07ef99] “The cost columns of the result tables count only the writer on the memory side.”

## Reproducibility

**Status:** partial

The paper provides unusually detailed experimental settings, task IDs, commits, models, budgets, metric definitions, and summarized prompts. This supports reconstruction in principle, but the supplied document does not identify executable artifacts or raw outputs, and runtime prompts are condensed. Dependence on proprietary, nondeterministic models and provider defaults further limits exact reproduction; therefore the appropriate status is partial rather than strong.

**Available artifacts**

- Exact source dataset registry names and pinned repository commits are listed.
- Evolution and held-out task identifiers are enumerated.
- Harness versions, model identifiers, turn caps, timeouts, host/container limits, retrieval budgets, seeds, and run structure are stated.
- Prompt roles and rules for the splitter, writer, review, and privacy judge are summarized.
- Metric definitions, paired-comparison procedure, privacy boundary contract, and preference pools are supplied.

**Missing pieces**

- No released implementation, benchmark repository, generated user/persona files, raw trajectories, evolved memory stores, or analysis artifacts are identified in the supplied blocks.
- The five key prompts are explicitly condensed rather than reproduced verbatim as rendered at runtime.
- Provider defaults govern sampling and reasoning, and model sampling is unseeded, so exact behavioral reproduction is not guaranteed.
- The supplied material does not state API snapshots, provider-side retry logs, or a fully auditable bill.
- Pew terms prevent release of the full survey data used to select user privacy labels.

## AIDB assessment

- Novelty: High at the systems formulation level: the paper treats audience selection as a learned two-axis routing problem and integrates utility, personalization, and privacy evaluation in one heterogeneous user-agent benchmark. The strongest novelty is the explicit Pair/User/Agent/Global lattice plus protected-stream enforcement, not a new base-memory representation.
- Usefulness: Promising for platforms or teams sharing heterogeneous agent experience. The controlled comparisons and diagnostic ablations make it useful as a design reference. Adoption should wait for real-user governance, hierarchical/group scopes, adversarial testing, released artifacts, and evidence that utility survives larger populations without losing to a simpler Global-only store.
- Confidence: medium
- Recommended action: read
- Rationale: The paper contains strong, multifaceted experiments and unusually candid negative scale evidence. The main scheduled and random-task results support further evaluation, but the largest scaling result, synthetic privacy setup, proprietary model dependence, high memory-side cost, and absent executable artifacts prevent an adopt recommendation.

## Uncertainties

- **Whether utility advantages over Global-only persist as user count and store size increase.** — The largest tested population reverses the utility ordering, so the central multi-scope advantage may be budget- or scale-sensitive.
  - Evidence: [b00158-20e192d6ce] “Global only 79.4 +7.3∗∗ +6.2∗∗”; [b00158-20e192d6ce] “MixUA (LLM) + review 78.1 +5.8∗∗ +4.4”
- **How well synthetic exact-target privacy probes predict leakage of real, paraphrased, inferable, or correlated personal information.** — A deployment may leak information without reproducing a planted sentence, and real users may define sensitivity contextually.
  - Evidence: [b00207-96c0666f10] “Privacy probes are checked by exact substring match and, on a seeded 20% sample, by the LLM judge.”; [b00086-43a914dc3e] “All users and personal facts in this study are synthetic”
- **How much of the result depends on the specific proprietary splitter, writer, review, judge, and embedding models.** — The architecture may not retain its privacy–utility profile with weaker, open, or differently calibrated components.
  - Evidence: [b00196-2782213385] “The splitter, the LLM writer, and the store review call Claude Opus 5, and the privacy judge calls Claude Sonnet 5”; [b00194-40d9af6ab0] “Titan Text Embeddings v2”
- **Whether whole-store review remains feasible or accurate once entries exceed the review model's input and merging regime.** — Review improves several metrics but its current implementation assumes bounded global visibility.
  - Evidence: [b00207-96c0666f10] “Stage 1 reads the whole store within a 900k-token input budget”; [b00084-5075331281] “a review that reads the whole store no longer fits in one pass.”
- **Whether targeted Agent and Pair benefits occur frequently enough in natural workloads to justify their complexity.** — Aggregate ablations show small changes, while their strongest evidence comes from deliberately constructed probes.
  - Evidence: [b00071-d9d4d7982a] “removing Agent or Pair changes relatively little.”; [b00071-d9d4d7982a] “We therefore build these situations as scope probes”

## Open questions

- Can hierarchical or dynamically discovered group scopes preserve auditability without making privacy classification and retrieval intractable?
- Would MixUA outperform a capacity-matched Global-only system under larger stores, equal total context, and multiple seeds?
- How does performance change with open-weight splitters, writers, judges, and embeddings?
- Can consent, provenance inspection, correction, deletion, and unlearning be implemented and empirically verified end to end?
- How robust is scoped memory to malicious contributors, poisoned lessons, prompt injection in trajectories, and colluding users or agents?
- Can privacy evaluation cover semantic inference, linkage across entries, indirect identifiers, and adaptive attackers rather than primarily planted-string recovery?
- What retrieval or review mechanism prevents old preferences and minority-user knowledge from being crowded out as the population grows?

## Proposed AIDB experiments

- **Hypothesis:** At larger populations, a hierarchical retrieval and sharded-review variant preserves MixUA's personalization while recovering a statistically reliable utility advantage over capacity-matched Global-only memory.
  - Baseline: Global-only and original reviewed MixUA, matched on total delivered characters, writer calls, task sequence, and total memory-side cost across several independent seeds.
  - Primary metric: Paired utility gain over no memory on first-attempt tasks, reported jointly with preference retention, forbidden-scope fact leakage, and memory-side cost.
  - Stop condition: Stop expansion if the confidence interval for the MixUA variant minus Global-only utility excludes the prespecified minimum useful gain on two successive population sizes, or if privacy leakage exceeds the prespecified deployment threshold.
- **Hypothesis:** Semantic and adaptive privacy attacks reveal materially more forbidden information than exact planted-string probes, and provenance-aware filtering reduces that gap without erasing utility gains.
  - Baseline: The paper's dual-stream MixUA and an otherwise identical system without provenance-aware filtering, evaluated against exact-match probes, paraphrase probes, linkage questions, and adaptive red-team prompts.
  - Primary metric: Forbidden-information attack success rate, stratified by direct reproduction, paraphrase, inference, and cross-entry linkage, with paired pass-rate change as a safety constraint.
  - Stop condition: Stop if filtering fails to reduce attack success by the prespecified relative margin or lowers paired task utility beyond the prespecified non-inferiority bound.
- **Hypothesis:** Agent and Pair scopes provide measurable value on naturally occurring heterogeneous workloads, not only constructed scope probes.
  - Baseline: Full MixUA versus matched variants without Agent and without Pair, with missing-scope lessons conditionally encoded in the remaining scopes as in the paper's strict ablation.
  - Primary metric: Frequency-weighted reduction in misapplied agent lessons and cross-agent user-context spillover, together with overall pass rate and preference retention.
  - Stop condition: Stop after the preregistered workload size if neither removed scope produces a statistically reliable degradation on its natural failure metric and the aggregate utility difference remains within the equivalence margin.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T09:05:33.744654+00:00`
- Document SHA-256: `9183c5a7afaccd41d8b0fbf52aaee29f171626fdf971220080e95732acf25f84`
- Metadata SHA-256: `c45748cca95708345224ee7ebb640e11cceaabc14fa7750b923965c8f811c56d`
- Blocks: 258
- Deterministic repair attempts: 0
