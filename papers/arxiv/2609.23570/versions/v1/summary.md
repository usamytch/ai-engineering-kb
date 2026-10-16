# VibeMemBench: Evaluating Memory Systems for Coding Agents on Real Repository Coding Tasks

## Executive summary

VibeMemBench is a carefully controlled benchmark for asking whether persistent memory improves executable repository work, rather than merely recalling stored facts. It selects targets for which a target-aware historical experience helped a reference solver, freezes that experience, transfers it to held-out solvers, and separately tests four existing memory systems on the same histories. The strongest conclusion is a gap between available and delivered experience: verified records produce small directional gains for most transfer solvers and reduce steps for all, whereas almost every system–solver retrieval pairing fails to beat memory-off. However, all transfer confidence intervals cross zero, the benchmark is deliberately outcome-selected, and proprietary frontier solvers are absent. The evidence therefore supports using the benchmark as a diagnostic and design testbed, not treating its aggregate uplift as an unbiased deployment estimate. Its most actionable findings are that uniform injection can harm already-capable solvers, record form matters more than simple ranking expansion, and raw transcript volume appears more damaging than instruction semantics alone.

## Problem

**Statement.** Existing repository benchmarks measure executable code changes without isolating persistent memory, while memory benchmarks measure recall without establishing whether retrieved experience improves repository repair.

**Why it matters.** A memory system may retrieve plausible or relevant text yet fail to improve—and may even degrade—the only downstream outcome that ultimately matters: whether the modified repository passes its declared executable tests.

**Scope.** The paper evaluates persistent-memory interventions on repository-level bug fixes, features, interface changes, configuration work, and related tasks. It studies frozen verified-experience transfer and pre-trajectory retrieval, not online closed-loop memory during a target-solving trajectory.

## Method

The authors construct VibeMemBench with the four-stage SIEVE pipeline. Source instances are validated by executing their gold patches; prior tasks from the same repository are screened using patch structure and an LLM judgment; selected history trajectories are executed and distilled into target-aware records; and targets are retained only when some candidate record improves a reference solver over memory-off. Evaluation then pairs memory-on and memory-off runs while fixing the task, seed, agent, prompt, tools, sandbox, budget, task order, and aggregation. One layer transfers each frozen selected record to held-out solvers. A second layer lets Mem0, SimpleMem, MemoryOS, and A-MEM ingest eligible histories and inject their top-ranked record. Executable test resolution is primary; solver tokens and agent steps are secondary. Target-level bootstrap intervals retain all seeds of each target.

### Key components

- SIEVE source validation, same-repository patch-pattern screening, history execution and target-aware experience distillation, followed by retention based on positive reference uplift.
- A frozen verified record containing a bug class, root cause, fix pattern, and reusable lesson, constructed without access to the target gold patch, test patch, or test outcome.
- A matched intervention contract in which only declared persistence and retrieval may differ between memory-off and memory-on conditions.
- Two evaluation layers: direct transfer of frozen verified experience, and retrieval from full eligible history by four existing memory systems.
- Diagnostic analyses covering headroom, first-broken-stage attribution, record-form mechanisms, same-record cross-solver contrasts, stripping, retrieval-budget dose, and counterfactual substitution.

### Assumptions

- Passing the declared executable predicate is an adequate measure of target resolution.
- The fixed reference agent and shortlist are sufficient to certify the existence of at least one useful historical experience, although not the globally best one.
- Paired runs under the same declared configuration isolate the memory intervention apart from stochastic seed variation.
- Pre-trajectory top-ranked retrieval is a meaningful evaluation of existing memory systems, even though it does not model online closed-loop memory.
- Target-level bootstrap resampling with seeds kept intact is the appropriate uncertainty unit.

## Main claims

- **The benchmark isolates persistent memory as a matched intervention while judging downstream success through executable tests rather than a gold retrieval label.**
  - Evidence: [b00008-66f011475f] “Both runs share the task, agent, tools, sandbox, and budget. Only the declared memory condition changes.”; [b00008-66f011475f] “Executable tests measure whether the supplied experience improves task resolution rather than whether it matches a gold retrieval label.”
- **SIEVE controls direct target leakage and constructs records from historical evidence, while reserving target patches and outcomes from record construction and solver context.**
  - Evidence: [b00037-38f86f51ae] “The target gold patch enters only this offline screen, the target test patch remains evaluator only”; [b00038-4c78d35d77] “The distillation never sees the target gold patch, test patch, or test outcome.”
- **The paper distinguishes experience availability from a memory system’s ability to construct and retrieve useful solver context.**
  - Evidence: [b00087-8e0360dea2] “The benchmark separates two questions, whether the frozen verified experience helps a solver once it reaches the context, and whether existing memory systems turn the same history into useful context.”
- **The diagnostic attributes the main retrieval failure to the supplied record’s form, but the fine boundary between ranking and form is not robust across raters.**
  - Evidence: [b00077-5a1253c7a1] “the combined share of the two stages located in the supplied record stays dominant for every rater at 61.9 to 81.4 percent.”; [b00077-5a1253c7a1] “The form degradation share in Table 4 therefore follows the written anchor rule rather than rater consensus.”
- **The usefulness of the same record depends materially on solver headroom, making uniform injection an unsafe default.**
  - Evidence: [b00070-47b534e5b6] “In every contrast the solver with the weaker memory-off result gains, while the stronger loses.”; [b00065-fa61ce0bb5] “Below the ceiling, existing memory systems help too little, and uniform top-1 injection is not a neutral default.”

## Results

- **Frozen verified experience increased observed resolution for four of five held-out solvers, with changes ranging from 1.1 to 4.5 percentage points; deepseek-v4-pro was unchanged. Yet every bootstrap interval crossed zero, so these are directional rather than statistically separated effects.**
  - Context: This is the strongest controlled evidence that selected historical experience can transfer beyond the reference solver, but it does not establish a reliable nonzero average effect at the benchmark’s sample size.
  - Evidence: [b00062-d06eb83b18] “The frozen verified experience raises Resolved on four of the five transfer solvers and leaves deepseek-v4-pro unchanged”; [b00062-d06eb83b18] “All five bootstrap intervals cross zero, so at 111 targets the observed gains of 1.1 to 4.5 points remain directional evidence rather than effects separable from zero.”
- **Existing systems underperformed broadly: eleven of twelve solver–system pairings stayed at or below memory-off. The only positive point estimate was MemoryOS on glm-5 at 2.0 points, and its interval still crossed zero; glm-5 with Mem0 was the sole pairing whose interval lay entirely below zero.**
  - Context: The contrast between frozen-record transfer and system retrieval supports an availability-to-use gap. It also shows that shorter trajectories are not sufficient evidence of helpful memory.
  - Evidence: [b00064-0a47f99005] “Eleven of the twelve solver and system pairings stay at or below the matched memory-off baseline, no system interval lies above zero, and the glm-5 and Mem0 interval lies entirely below it.”; [b00064-0a47f99005] “The single exception, MemoryOS on glm-5, gains 2.0 points and still trails the frozen verified experience.”
- **Failure attribution assigned 160 of 231 failing pairings, or 69.3%, to form degradation; coverage misses accounted for 37, ranking misses for 3, and use failures for 31.**
  - Context: Under the paper’s written anchor rule, retrieval usually reached related history but rendered it poorly. This attribution is mechanistically useful, though its fine categories are sensitive to how anchors are interpreted.
  - Evidence: [b00078-28355098b1] “Coverage miss source history never entered the system store 37 16.0% Ranking miss stored, but the injected record shares no anchor with it 3 1.3%”; [b00078-28355098b1] “Form degradation relevant history reached, but the fix pattern dropped or buried in raw transcript 160 69.3%”; [b00078-28355098b1] “Use failure record matches the reference on anchor and repair principle, yet the run fails 31 13.4% All failing pairings 231 100%”
- **The strip ablation did not support instruction semantics as the causal mechanism: deleting flagged lines recovered 0.60 resolved seeds per pairing, while deleting an equal number of unflagged lines recovered 0.48. The authors conclude that transcript volume, rather than instruction content, explains the comparable recovery.**
  - Context: This is a consequential negative ablation: lexical instruction-pollution markers identify bulky records but do not isolate the harmful semantic component.
  - Evidence: [b00206-f25b5e1f59] “The strip arm gains 0.60 resolved seeds per pairing and the random arm gains 0.48, so removing an equal count of unflagged lines recovers a comparable amount.”; [b00206-f25b5e1f59] “The harm operates through transcript volume rather than instruction semantics.”
- **A wider Mem0 retrieval budget did not recover performance: every budget from one to five records remained below the 67.1% memory-off baseline, and the best observed budget resolved 65.5%.**
  - Context: This argues against top-one retrieval capacity as the principal cause, at least for the tested deepseek-v4-pro–Mem0 configuration. It does not establish that larger budgets or other retrieval systems can never help.
  - Evidence: [b00210-8fef23e65b] “Budget k Resolved Δ^ (pp) 95% CI 0 67.1% — — 1 62.8% −4.28 [−9.91,+1.35] 2 61.7% −5.41 [−11.26,+0.23]”; [b00210-8fef23e65b] “3 64.4% −2.70 [−8.78,+3.38] 4 65.5% −1.58 [−7.21,+4.05] 5 63.7% −3.38 [−9.46,+2.48]”; [b00212-938eda56fb] “No budget reaches the memory-off baseline.”

## Experimental evaluation

### Datasets

- VibeMemBench: outcome-selected repository coding targets derived from SWE-rebench V2, paired with completed trajectories from the same repositories.
  - Evidence: [b00032-2cafc18d24] “The 111 targets span 90 repositories after deduplication by history directory and draw on 3,634 completed history trajectories.”
- The task mix is broader than bug repair, covering feature, interface, configuration, test-infrastructure, and other repository work.
  - Evidence: [b00031-2fdfc9320e] “Bug fixes account for under a third of the labels, and feature, interface, configuration, and test infrastructure work covers the rest.”
- The targets cover nine programming languages but are concentrated in Python and other mainstream languages, limiting how aggregate scores represent the smaller language groups.
  - Evidence: [b00030-e1d36ca8f6] “The left chart in Figure 3 reports the language distribution across nine languages.”; [b00030-e1d36ca8f6] “The distribution concentrates on Python and three mainstream languages, so an aggregate score chiefly reflects these languages.”

### Baselines

- Matched memory-off runs using the same target, seed, model, prompt, tools, sandbox, context budget, resource limits, task order, and aggregation.
  - Evidence: [b00046-e545f5841a] “Let A denote the fixed agent configuration, including the model, prompt, tools, sandbox image, context budget, resource limits, task order, and aggregation rule”
- Frozen verified experience selected in the reference setting and transferred unchanged to held-out solvers.
  - Evidence: [b00049-218dba61e9] “The first layer transfers the frozen verified experience that the deepseek-v4-flash reference setting identifies for each retained target.”
- A fixed irrelevant-memory control containing everyday sentences and no software content, run on only three solvers.
  - Evidence: [b00169-51e0ef7451] “injects one fixed distractor passage in place of the frozen verified experience.”; [b00169-51e0ef7451] “contains no software content.”
- Four evaluated memory systems: Mem0, SimpleMem, MemoryOS, and A-MEM.
  - Evidence: [b00050-bfc19974d4] “Mem0, SimpleMem, MemoryOS, and A-MEM”; [b00050-bfc19974d4] “a declared target query selects one top-ranked experience, which the protocol injects into MiniSWEAgent.”

### Metrics

- Resolved: the share of target-seed runs passing the declared executable predicate; paired memory effect is memory-on minus memory-off.
  - Evidence: [b00055-701dba348f] “We report Resolved, the share of target-seed runs whose declared test predicate passes”; [b00055-701dba348f] “the paired memory effect is Δ^=p^on−p^off.”
- Target-level percentile bootstrap confidence intervals, resampling targets while retaining their seeds together.
  - Evidence: [b00055-701dba348f] “the reported intervals resample the 111 targets with their four seeds intact 10,000 times and give percentile bounds for Δ^.”
- Mean solver input tokens, output tokens, and agent steps per run; these exclude latency and memory-side resource consumption.
  - Evidence: [b00056-90f02757fb] “Both measure solver use and interaction length, not latency, and the protocol does not record memory-side token consumption.”

### Ablations

- Irrelevant-memory control tests whether injected text alone explains transfer gains, while keeping placement and other settings fixed.
  - Evidence: [b00169-51e0ef7451] “separates the effect of relevant experience from the effect of injected text.”
- Instruction-pollution strip ablation compares removal of flagged lines with removal of an equal number of randomly selected unflagged lines.
  - Evidence: [b00203-e2c955bc1a] “The strip arm deletes every line that triggers the lexical pollution marker and reinjects the remainder.”; [b00203-e2c955bc1a] “The random arm deletes an equal number of unflagged lines at a fixed seed, which controls for length.”
- Retrieval-budget dose curve varies the number of injected Mem0 records while holding the store, query, ranker, truncation, task order, and seeds fixed.
  - Evidence: [b00208-30de0d268e] “It varies only the number of injected records k from one to five and holds the Mem0 store, retrieval query, ranker, truncation, task order, and seeds at the main-experiment values.”
- Counterfactual substitution replaces each failing system record outcome with the frozen verified experience outcome for the same target and solver; it is explicitly a recovery bound, not a repaired-system prediction.
  - Evidence: [b00237-ace445301d] “the substitution replaces the four-seed system outcome with the frozen verified experience outcome of the same target and solver”; [b00240-eafddf26d6] “it is not a prediction for a repaired system, since frozen injection changes more than record form.”

### Negative results

- No frozen-transfer confidence interval excludes zero.
  - Evidence: [b00062-d06eb83b18] “All five bootstrap intervals cross zero”
- The irrelevant-memory control produced no gain on any tested solver.
  - Evidence: [b00172-baa4fd63c1] “No solver gains, so injected text alone reproduces none of the frozen verified experience gains.”
- Almost all existing memory-system pairings failed to exceed memory-off, and one pairing was detectably worse under its reported interval.
  - Evidence: [b00064-0a47f99005] “Eleven of the twelve solver and system pairings stay at or below the matched memory-off baseline”; [b00064-0a47f99005] “the glm-5 and Mem0 interval lies entirely below it.”
- Removing flagged instruction lines did not outperform the length-matched random deletion according to the predeclared causal criterion.
  - Evidence: [b00206-f25b5e1f59] “The predeclared criterion for a causal form effect requires the strip arm to recover and the random arm not to, so the effect is not established.”
- Expanding retrieval did not restore the memory-off baseline and yielded a non-monotone curve.
  - Evidence: [b00212-938eda56fb] “No budget reaches the memory-off baseline.”; [b00212-938eda56fb] “The curve is also non-monotone, so added records do not trace a recovery toward the baseline.”


## Limitations

- Targets are selected using an oracle-assisted comparison of target and history gold patches plus positive reference uplift. The resulting benchmark measures downstream value where useful transferable history is known to exist, not its prevalence in deployment.
  - Evidence: [b00089-3ea3cda95e] “The offline patch-pattern screen compares target and history gold patches, and the 111 targets have positive deepseek-v4-flash reference uplift by design.”; [b00089-3ea3cda95e] “not an estimate of how often a deployed agent finds such a pair.”
- Reference uplift is selected through an argmax over noisy seed-level outcomes, creating optimism in the selection audit even though held-out transfer does not reselect records.
  - Evidence: [b00044-18a08e2280] “the seed-level argmax lets seed noise inflate it.”; [b00044-18a08e2280] “the transfer estimates inherit the selected population but not the argmax optimism.”
- The solver pool excludes proprietary Claude and GPT frontier families, so claimed solver generality is untested for them.
  - Evidence: [b00091-9fa474bab6] “The solver pool omits proprietary frontier models such as the Claude and GPT families for reasons of inference budget”
- Existing-system evaluation retrieves before the target trajectory and therefore does not evaluate online closed-loop memory.
  - Evidence: [b00050-bfc19974d4] “it is not online closed-loop memory, because retrieval occurs before the target solver trajectory rather than during it.”
- Resource accounting covers solver tokens and steps but omits memory-system token consumption, latency, wall-clock time, and price, preventing a full efficiency comparison.
  - Evidence: [b00056-90f02757fb] “the protocol does not record memory-side token consumption.”; [b00056-90f02757fb] “Wall-clock time and API price vary with provider and pricing policy, so they do not enter the comparison across systems.”
- The irrelevant-memory control is not token-matched to the frozen record, leaving context-length effects incompletely controlled.
  - Evidence: [b00173-5c7c13d591] “The distractor passage is not matched to the frozen record in token count”
- Fine-grained failure attribution is sensitive to the written anchor rule, with only modest agreement between scripted and judged labels.
  - Evidence: [b00167-f3115bf694] “Primary-stage agreement is 56.3 and 44.2 percent with Cohen’s kappa 0.32 and 0.24”; [b00167-f3115bf694] “the residual disagreement reflects the looseness of the ranking and form boundary”

## Reproducibility

**Status:** partial

The reporting contract is unusually detailed and repeatedly states what the release contains, including executable predicates, environments, manifests, provenance, and recomputable diagnostics. However, the supplied material does not expose the release itself or an immutable artifact reference, so artifact completeness and end-to-end rerunnability cannot be verified here. Reproducibility is therefore partial rather than strong.

**Available artifacts**

- The paper states that the release preserves target provenance, test commands, environments, and execution results.
- The release manifest is described as recording construction variants, prompts, chronology, model revisions, retrieval configuration, target queries, and condition fields.
- Task histories, executable predicates, intervention protocol, injected text, retrieval events, trajectory paths, and declared agent steps are described as released or logged.
- Failure-attribution labels are described as deterministically recomputable; judge labels and disagreement cases are said to enter the release.

**Missing pieces**

- The supplied blocks do not provide an artifact URL, repository URL, immutable release identifier, or installation instructions.
- The supplied blocks do not include the actual manifests, container hashes, source code, prompts, or raw run files needed to verify reproducibility claims directly.
- Memory-side token consumption, latency, wall-clock time, and API cost are not recorded.
- Exact provider snapshots and continued availability of evaluated model endpoints cannot be established from the supplied document alone.

## AIDB assessment

- Novelty: High conceptual novelty in evaluation design: the work combines executable repository outcomes with a matched memory toggle and explicitly separates availability of useful history from construction and retrieval by memory systems. Outcome-based selection is also an unusual way to guarantee that every retained target contains demonstrably useful prior experience, though it narrows external validity.
- Usefulness: High for researchers and engineers designing coding-agent memory. The benchmark offers controlled baselines, negative results, diagnostics, and concrete design implications: gate injection by headroom, compress raw transcripts around repair spans, preserve target-anchored constraints, and do not assume more retrieved records will solve form degradation. It is less suitable for estimating real-world average memory uplift because targets are selected for positive reference uplift.
- Confidence: medium
- Recommended action: adopt
- Rationale: Adopt VibeMemBench as a diagnostic evaluation suite, contingent on verifying the released artifacts and reproducing a subset of runs. Do not adopt its aggregate transfer scores as deployment forecasts. The controlled design and consequential negative results are decision-relevant, but all principal transfer intervals cross zero, target selection is intentionally favorable to useful memory, and the tested systems and solver families are limited.

## Uncertainties

- **Whether the small transfer gains would become statistically distinguishable with more independently sampled targets.** — The central positive finding currently supports directionality, not a stable nonzero average effect; scaling the benchmark could either confirm useful transfer or show that observed gains are mostly noise.
  - Evidence: [b00062-d06eb83b18] “All five bootstrap intervals cross zero, so at 111 targets the observed gains of 1.1 to 4.5 points remain directional evidence rather than effects separable from zero.”
- **Whether headroom-aware gating can improve aggregate resolution without requiring knowledge unavailable before solving.** — Headroom is the paper’s strongest operational predictor, but deployment must estimate it prospectively rather than observe the memory-off outcome after running the task.
  - Evidence: [b00088-192c1e9b69] “Injection should be gated on expected solver headroom rather than applied uniformly.”; [b00189-989b12c398] “A rule that predicts the sign from memory-off count alone is correct on 56.5 percent of the 641 pairings that change Resolved”
- **Whether compressing transcripts to repair-bearing spans would close the availability-to-use gap in an actual memory pipeline.** — The strip and substitution studies diagnose volume and estimate recoverable outcomes, but neither evaluates an end-to-end learned compressor that must identify the correct repair span without access to the frozen record.
  - Evidence: [b00085-5747edab32] “This bound marks what one verified record recovers, not a prediction for a repaired system, because frozen injection changes more than record form.”
- **How well results generalize to online memory, other retrieval interfaces, proprietary frontier solvers, and repositories outside the selected SWE-rebench V2 population.** — These omitted settings may change both headroom and a solver’s susceptibility to irrelevant or overlong records.
  - Evidence: [b00050-bfc19974d4] “it is not online closed-loop memory”; [b00091-9fa474bab6] “the solver-agnostic protocol stays untested for them.”

## Open questions

- Can solver headroom be estimated before executing a full memory-off trajectory accurately enough to gate retrieval safely?
- Does a target-anchored repair schema trained specifically on coding trajectories outperform raw transcript and dialogue-fact schemas under the same token budget?
- Would a token-matched irrelevant control alter the interpretation of the frozen-record transfer gains?
- How stable are the findings across new repositories, chronological releases, online retrieval during solving, and proprietary frontier solvers?
- Can confidence-calibrated abstention from memory injection preserve below-ceiling gains while avoiding ceiling losses?

## Proposed AIDB experiments

- **Hypothesis:** A prospective headroom gate can retain most gains on difficult targets while reducing harm on targets the solver already resolves reliably.
  - Baseline: Uniform top-ranked injection and memory-off, evaluated on the same target–seed pairs. Train or calibrate the gate without using each evaluation target’s realized memory-off outcome.
  - Primary metric: Paired change in Resolved versus memory-off, accompanied by the share of injected targets, ceiling-target losses, below-ceiling gains, and target-level bootstrap intervals.
  - Stop condition: Stop if the gated condition fails to improve the uniform-injection point estimate and fails to reduce ceiling losses, or if its interval excludes the prespecified minimum useful gain on the unfavorable side.
- **Hypothesis:** Target-anchored extraction that emits root cause, repair action, constraints, and code anchors will outperform raw transcripts and dialogue-fact records under equal context allocation.
  - Baseline: MemoryOS or A-MEM raw-transcript records, Mem0 or SimpleMem atomic records, and a token-matched irrelevant-text control, all using the same retrieved source history.
  - Primary metric: Paired Resolved difference under a fixed token budget; secondary diagnostics are form-degradation rate, retained repair-field rate, solver tokens, and steps.
  - Stop condition: Stop if the structured extractor does not beat both memory-system families on paired Resolved or if any apparent gain disappears against the token-matched control.
- **Hypothesis:** Online, confidence-triggered retrieval during the solver trajectory is more useful than pre-trajectory top-ranked injection because it can condition records on the solver’s observed state and avoid unnecessary context.
  - Baseline: The paper’s pre-trajectory top-ranked condition, memory-off, and frozen verified experience under matched total context and resource budgets.
  - Primary metric: Paired Resolved difference, with memory-side and solver-side tokens, latency, retrieval count, and ceiling-target harm recorded separately.
  - Stop condition: Stop if online retrieval does not exceed pre-trajectory retrieval in Resolved or if additional memory-side cost exceeds a prespecified budget without a compensating success gain.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:10:43.258214+00:00`
- Document SHA-256: `1b7c02f027016cb9206a494cc299f4faf3e2129a6597225c941740888438896a`
- Metadata SHA-256: `a83c571cb1a747c579a23fcb7c5a5cebf987d4af8b73d4beba9f8c4ff9ff9d3f`
- Blocks: 242
- Deterministic repair attempts: 1
