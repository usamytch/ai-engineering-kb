# PACE: Keeping the Right Tokens in the KV Cache Is Not Enough for Long-Horizon LLM Agents

## Executive summary

PACE addresses two distinct failures in budgeted KV caches: needed tokens can be evicted, or retained yet difficult to use because their rotary-position distance is large. It combines planner-directed retention with exact, bounded-position renumbering. Controlled Qwen3-8B results are strong: PACE substantially outperforms standard eviction and either component alone, and retains quality through very long synthetic coding sessions. The mechanism evidence is persuasive but narrow: one synthetic task family, mostly oracle plans, two small models, one GPU type, small cells, and no matched full-cache control at the headline length. The paper is valuable and merits replication before production adoption, especially under noisy plans, realistic workloads, concurrency, and time-sensitive tasks where collapsed gaps may alter semantics.

## Problem

**Statement.** Budgeted KV-cache systems optimize whether future-needed tokens remain resident, but the paper tests whether near-perfect residency is sufficient when retained tokens remain far from the query in rotary-position space.

**Why it matters.** Long-running agents can accumulate histories whose full KV state exceeds accelerator memory. If residency alone does not ensure usable context, eviction evaluations and agent-serving designs can appear successful while late-step correctness still deteriorates.

**Scope.** The work targets planned agent workloads in which future dependencies can be stated. It does not claim to provide an unrestricted long-context window or reliable recall of arbitrary, unplanned historical details.

## Method

PACE modifies an inference engine’s KV-cache manager. A planner supplies dependencies over earlier message spans; a foresight bonus makes future-referenced spans outrank unreferenced tokens, prioritizing the soonest use. Separately, retained tokens are periodically renumbered in logical order and cached keys are re-rotated so their physical positions remain bounded. Persistent sessions carry eviction state between turns, while optional memory tiers can restore planned spans that were evicted. A reference-key store prevents rounding error from compounding across repeated renumbering.

### Key components

- Plan-aware retention converts a dependency blueprint into span-level future references and adds a dominant bonus to cumulative-attention scores.
- Bounded positions collapse gaps left by eviction, preserve retained-token order, and exactly re-rotate cached keys to their new physical positions.
- Persistent sessions append only new messages and preserve cache state and prior eviction decisions across agent steps.
- Tiered rehydration restores planner-requested spans from host memory, local storage, or a remote cache.
- A reference store derives later key positions from a stable copy to prevent repeated bf16 rounding from accumulating.

### Assumptions

- The planner can identify which earlier spans later steps will need.
- The protected spans generally fit the token budget; otherwise restoration or prioritization is required.
- Collapsing positional gaps preserves the semantics relevant to the evaluated task.
- A fixed foresight bonus remains above the cumulative-attention scores of unprotected tokens over the tested session lengths.
- The synthetic coding benchmark’s dependency and recall structure is informative about broader planned-agent workloads.

## Main claims

- **Retaining needed tokens is necessary but not sufficient: correctness also depends on their rotary-position distance from the query.**
  - Evidence: [b00026-491af0dd9f] “This paper asks whether ρt≈1 suffices, and shows that it does not: at ρt≥0.99, accuracy still falls with Δt”; [b00073-7087da1392] “Retention only keeps 99.6% of the needed tokens at every gap, yet its accuracy falls from 93% to 64%.”
- **PACE jointly controls retention and physical rotary distance by combining planner foresight with order-preserving key renumbering.**
  - Evidence: [b00008-e56a3ae324] “Plan-aware retention turns the dependency graph an agent planner already produces into a per-span foresight bonus”; [b00035-a5202057e4] “the resident row of each layer is renumbered to p′∈{0,…,R−1} in logical order, every kept key is re-rotated from p to its new position p′”
- **The two main components address different failure modes and both are required for the strongest Qwen3-8B result.**
  - Evidence: [b00067-786492a920] “With positions only, the needed tokens are close to the query but often gone”; [b00067-786492a920] “With retention only, the tokens are resident (residency 1.000 at every probe) but 30–80K positions away”; [b00067-786492a920] “Only when the tokens are both kept and close does the model use them reliably.”
- **PACE is intended for planned workflows, not arbitrary recall over an entire history.**
  - Evidence: [b00010-077fc8e3e0] “PACE targets agent workloads whose planner can state what later steps depend on”; [b00010-077fc8e3e0] “full-context serving remains preferable for unplanned recall of arbitrary details from an entire history.”

## Results

- **In the pre-registered Qwen3-8B headline comparison, PACE passed 145/150 hidden checks (97%) and 28/30 probes completely, versus H2O at 63/150 (42%) and 7/30. Each single-component arm reached 94/150 (63%), while PACE recalled 100% of session facts.**
  - Context: Ten fresh 100K-token sessions, three probes per session, with a 2,048-token KV budget. This is the strongest controlled factorial comparison, although the 8K position limit had first been selected from an earlier distance sweep and was then tested on fresh seeds.
  - Evidence: [b00064-f0f275d570] “Qwen3-8B, 100K-token sessions, B=2,048, ten fresh sessions, three probes each”; [b00065-883c4b2eba] “H2​O – – 63/150 (42%) 7/30 83%”; [b00065-883c4b2eba] “positions only – ✓ 94/150 (63%) 10/30 86%”; [b00065-883c4b2eba] “retention only ✓ – 94/150 (63%) 12/30 96%”; [b00065-883c4b2eba] “PACE ✓ ✓ 145/150 (97%) 28/30 100%”
- **The distance intervention supports the proposed mechanism: retention-only accuracy declined from 93% at a 2K logical gap to 64% at 90K despite residency of 0.992–0.996, whereas PACE with an 8K bound scored 97–100% and kept observed rotary gaps between 2.7K and 6.5K.**
  - Context: Five 100K-token sessions per distance used the same seeds while moving only the definitions. This is stronger than the pooled distance analysis because session length is fixed, though only five sessions were used per point.
  - Evidence: [b00069-da152a971d] “five sessions per D, same seeds at every D”; [b00069-da152a971d] “Residency is 0.992​–​0.996 for every PACE-family arm at every D.”; [b00070-78619f2565] “2K 44% 93% 100% 𝟗𝟕% 2.9K 2.7K”; [b00070-78619f2565] “90K 52% 64% 93% 𝟏𝟎𝟎% 23.9K 6.5K”
- **Quality persisted at extreme length on one GPU: at 1M tokens PACE passed 74/75 checks (99%) and recalled 125/125 facts; at 2M it passed 75/75 and recalled 125/125. Positions-only fell from 33% checks and 74% recall to 13% and 50%.**
  - Context: Five fresh Qwen3-8B sessions at each length placed definitions roughly 90% of the session before probes. These evaluations were pre-registered, but compare only bounded-position arms at the longest lengths and remain within the same synthetic task family.
  - Evidence: [b00093-19e031cb0a] “PACE passes 74 of 75 checks (99%), fully passes 14 of 15 probes, and recalls all 125 session facts”; [b00093-19e031cb0a] “Positions only passes 33% and recalls 74%”; [b00094-b9e19cc531] “PACE passes all 75 checks, fully passes all 15 probes, and recalls all 125 facts.”; [b00094-b9e19cc531] “Positions only falls from 33% at 1M to 13% (10/75), fully passes no probe, and recalls 50%”
- **The resident state remained bounded while execution overhead was measurable: PACE used 0.30 GB for the 2,048-token KV budget plus at most 0.30 GB for reference keys, versus a 147 GB full cache at 1M, and took 1,047 s versus 963 s (+9%) over ten 100K-token sessions.**
  - Context: Memory values are computed from model dimensions. Timing uses the same eager decode path but does not characterize concurrent serving or absolute production throughput.
  - Evidence: [b00089-4f7a08fd4b] “PACE took 1,047​ s against H2​O’s 963​ s (+9%)”; [b00089-4f7a08fd4b] “2,048 tokens, 0.30​ GB for Qwen3-8B”; [b00089-4f7a08fd4b] “the reference store (at most 0.30​ GB)”; [b00089-4f7a08fd4b] “the full cache would need 14.7​ GB at 100K tokens and 147​ GB at 1M.”
- **Generalization to the second model was mixed but informative: Mistral’s no-eviction control passed 40% of checks; PACE stayed near that ceiling, but its pre-declared 90K comparison against retention-only was not significant (46% versus 36%, p=0.75).**
  - Context: This negative result limits the claim that bounded positions improve test-pass accuracy across models. The authors attribute limited separation partly to Mistral’s coding ceiling, while recall provides a less ceiling-constrained signal.
  - Evidence: [b00083-cb451f29bf] “it recalls 99% of facts but passes only 40% of checks”; [b00084-e34383527b] “The pre-declared paired test of PACE against retention only at D=90​K is not significant (46% vs. 36% on p1+p2; 6 better, 4 worse; p=0.75”

## Experimental evaluation

### Datasets

- A synthetic, execution-scored long-horizon coding-session benchmark. Randomized definitions are followed by Python standard-library filler and three late code probes; all arms within a run receive identical sessions.
  - Evidence: [b00051-108b07d03b] “We therefore built an execution-scored session benchmark in which recall of early definitions is the only path to a correct late answer.”; [b00052-ffaad91fd4] “All arms of a run see identical sessions.”
- Distance-layout sessions hold total length fixed while moving definitions relative to terminal probes, enabling a controlled distance intervention.
  - Evidence: [b00056-f31bd4029c] “the session length is fixed at 100K tokens and the definitions are placed D tokens before the three probes at the end, so only the gap varies.”

### Baselines

- H2O: cumulative-attention heavy-hitter retention plus recent tokens, using positions as written where feasible.
  - Evidence: [b00020-b3da54f750] “H2​O [31] keeps the tokens with the largest cumulative attention received, plus a recent window”
- SnapKV: current-query attention ranking under the same overall budget.
  - Evidence: [b00020-b3da54f750] “SnapKV [12] ranks tokens by the attention of the last few prompt tokens”
- StreamingLLM-style sink-plus-recent cache for sessions beyond the native positional range.
  - Evidence: [b00090-b04b4014c7] “a StreamingLLM-style baseline that spends the budget on sink and recent tokens with in-cache positions”
- No-eviction controls establish model-specific task ceilings, but the Qwen3-8B control is shorter than the headline sessions.
  - Evidence: [b00055-92895afe26] “A control run with no eviction (an 8K-token session within an 8K budget) scores 100% on Qwen3-8B”; [b00083-cb451f29bf] “A no-eviction control first establishes the model’s own ceiling”

### Metrics

- Hidden unit-test checks and complete-probe pass rates, obtained by executing generated code.
  - Evidence: [b00055-92895afe26] “Each probe’s code is executed against hidden unit tests in a subprocess”
- Session-fact recall, used with execution scores to distinguish forgetting from coding errors.
  - Evidence: [b00055-92895afe26] “a recall metric checks whether the answer contains each session fact”; [b00055-92895afe26] “failed with all facts recalled (a coding error), or failed with facts missing (forgetting)”
- Needed-token residency and reconstructed rotary gap at each probe.
  - Evidence: [b00069-da152a971d] “the rotary gap is the mean distance, in the positions the model sees, from the query to the definitions”; [b00064-f0f275d570] “Residency: fraction of needed tokens resident at the probes.”
- Paired statistical tests on identical sessions, plus full-pass and interaction tests.
  - Evidence: [b00060-fe73939b6e] “Comparisons between arms are paired on identical sessions and use a two-sided sign test; full-pass rates use Fisher’s exact test”

### Ablations

- Retention only: planner foresight with positions as written, isolating the effect of bounded positions.
  - Evidence: [b00054-72db17bc39] “retention only H2​O + foresight bonus as written (YaRN) ablation: no bounded positions”
- Positions only: bounded positions with H2O retention, isolating planner foresight.
  - Evidence: [b00054-72db17bc39] “positions only H2​O bounded, L=8​K ablation: no foresight”
- A larger position limit tests whether merely staying inside the model range is sufficient.
  - Evidence: [b00054-72db17bc39] “PACE (L=40​K) H2​O + foresight bonus bounded at the model’s range limit ablation”
- Rehydration is directly tested by flagging an already-evicted definition, including a remote-only restore condition.
  - Evidence: [b00088-2190f61bd0] “rehydration restores it and recall is 5/5 against 1/5 without rehydration”; [b00088-2190f61bd0] “all restores came from the remote tier and recall stayed 5/5.”

### Negative results

- At the recommended position bound, the factorial interaction was not statistically significant; the evidence supports necessity of both components, not super-additivity.
  - Evidence: [b00068-2867bc4513] “the interaction, +8.3 points (CI [−8.0,+23.8], p=0.32), is not significant”; [b00068-2867bc4513] “not that they are super-additive at the recommended setting.”
- The Mistral comparison between PACE and retention-only at the longest tested gap was not significant.
  - Evidence: [b00084-e34383527b] “46% vs. 36% on p1+p2; 6 better, 4 worse; p=0.75”
- Naive repeated re-rotation accumulated enough numerical error to degrade stressed accuracy; the reference-store implementation was required to recover it.
  - Evidence: [b00188-3d00636bb4] “the stressed arm scored 63/75 (84%; 4 probes worse, none better)”; [b00188-3d00636bb4] “the reference-store implementation passes 75/75 checks (0 worse)”
- Per-turn latency increased late in very long sessions despite a fixed resident set, and the source was not isolated.
  - Evidence: [b00094-b9e19cc531] “the median filler turn rose from about 0.9​ s at the start of each session to 1.7​–​3.2​ s at the end”; [b00094-b9e19cc531] “we have not yet isolated it.”


## Limitations

- External validity is limited by a single synthetic coding task family; other agent workloads may have different retention and distance requirements.
  - Evidence: [b00102-2464b27ee5] “The benchmark is a synthetic coding session with randomized specifications.”; [b00102-2464b27ee5] “other agent workloads (tool traces, multi-document research, multi-agent hand-offs) may weigh retention and distance differently.”
- Evidence covers only two small models and one GPU type; the statistically established bounded-position advantage is confined to Qwen3-8B.
  - Evidence: [b00104-c562fef2d6] “Two models at 7–8B, one GPU type.”; [b00104-c562fef2d6] “Larger models, which may use distant context better, are untested.”
- Most experiments use an oracle dependency graph, and sensitivity to worse planner errors is unknown.
  - Evidence: [b00108-ea99cf465b] “Mostly an oracle planner.”; [b00108-ea99cf465b] “How accuracy degrades with planner errors beyond that is not yet characterized.”
- The fixed foresight bonus may cease to dominate attention scores at longer sessions and the proposed relative bonus is unevaluated.
  - Evidence: [b00110-263c50e054] “Extrapolated, it reaches the floor at about 5M tokens”; [b00110-263c50e054] “Longer sessions need a relative bonus, scaled to the current unprotected maximum at each eviction; we have not yet evaluated it.”
- Renumbering destroys original temporal distances between retained tokens, potentially harming tasks whose semantics depend on elapsed distance.
  - Evidence: [b00112-865f244f6a] “Renumbering preserves order but not distance between kept tokens.”; [b00112-865f244f6a] “tasks that depend on how long ago something happened could be affected.”
- Rehydration evidence comes mainly from a scripted late-flag test and was disabled in the longest evaluations.
  - Evidence: [b00114-5b07f98541] “it is disabled in the 300K, 1M and 2M runs; its benefit is shown in a scripted late-flag test.”
- Serving evaluation omits concurrency and absolute production throughput, while unexplained per-turn work grows with session length.
  - Evidence: [b00116-38ba9e577e] “we report relative overhead, not absolute serving throughput, and do not evaluate concurrent sessions.”; [b00116-38ba9e577e] “The source, outside the bounded attention path, is not yet isolated.”
- There is no matched full-cache Qwen3-8B reference at the headline length.
  - Evidence: [b00118-5a5df61d03] “We do not report the same model with its full cache at 100K tokens on this hardware; the no-eviction control is an 8K-token session.”
- Filler topic and construction affect behavior, and the headline and later long-session studies use different filler regimes.
  - Evidence: [b00120-c1aaf4c564] “Filler content matters.”; [b00120-c1aaf4c564] “The 100K experiments also span two filler regimes (recurring vs. non-repeating files)”
- Cells contain few sessions, making secondary patterns unstable despite strong headline significance.
  - Evidence: [b00122-618bf3ea65] “Five to ten sessions per configuration, three probes each.”

## Reproducibility

**Status:** partial

The procedural description is unusually detailed and includes templates, controls, integrity safeguards, factorial ablations, pre-registration statements, and hardware. However, the supplied material does not itself expose the implementation or raw artifacts needed to independently reproduce reported tables, so reproducibility is partial rather than strong.

**Available artifacts**

- The complete session templates and sampled-value ranges are included in the supplied document.
- The paper specifies model versions, GPU and host memory, cache budget, engine path, decoding mode, position limits, statistical tests, seeds per configuration, integrity checks, and several pre-registration boundaries.
- The implementation is stated to be a configuration-controlled subclass in an open-source inference engine.
- Result files are stated to fingerprint instruction templates, and merge tooling rejects incompatible runs.

**Missing pieces**

- No repository snapshot, commit identifier, installation instructions, environment lockfile, runnable benchmark package, raw result files, pre-registration records, or exact reproduction commands are supplied in the document blocks.
- The paper does not provide a matched full-cache 100K-token Qwen3-8B run.
- Exact concurrent-serving and production-throughput reproduction procedures are absent.

## AIDB assessment

- Novelty: High conceptual novelty within the supplied paper: it separates residency from retrievability inside a KV-evicting multi-turn server and treats rotary distance as a second controlled cache objective. The engineering combination of planner foresight, bounded exact re-rotation, persistence, and non-compounding reference keys is also distinctive.
- Usefulness: Potentially high for planned coding and tool agents under strict accelerator-memory budgets. The strongest immediate value is diagnostic: cache evaluations should measure both needed-token residency and physical positional distance. Production usefulness remains contingent on realistic planner errors, diverse workloads, concurrent serving, and temporal-semantics tests.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled Qwen3-8B comparisons, fresh-seed headline run, distance intervention, factorial ablations, integrity protocol, and very-long-session results make the central finding credible enough to influence evaluation design. Adoption is premature because external validity is narrow, planner robustness is under-characterized, the second-model component comparison is inconclusive, concurrency is untested, and executable artifacts are not supplied here.

## Uncertainties

- **Whether the measured rotary-distance effect persists on larger or stronger models.** — If stronger models use distant retained context reliably, bounded positions may yield less benefit relative to planner retention alone.
  - Evidence: [b00104-c562fef2d6] “Larger models, which may use distant context better, are untested.”
- **How performance changes under realistic false-positive and false-negative dependency graphs.** — Planner quality determines which spans receive protection or restoration; systematic misses could erase PACE’s advantage or waste the fixed budget.
  - Evidence: [b00081-fb690020a2] “Foresight is only as good as the plan.”; [b00108-ea99cf465b] “How accuracy degrades with planner errors beyond that is not yet characterized.”
- **Whether positional gap collapse harms tasks that encode time, delay, or original spacing.** — The intervention deliberately changes model-visible distances, so success on order-dependent coding recall does not establish semantic safety elsewhere.
  - Evidence: [b00040-57b8e62e36] “This is a deliberate change of what the model observes”; [b00112-865f244f6a] “tasks that depend on how long ago something happened could be affected.”
- **What causes late-session latency growth outside the bounded attention path.** — Unexplained work that scales with total session length may weaken the claimed operational benefit even when KV memory remains bounded.
  - Evidence: [b00094-b9e19cc531] “the growth comes from per-turn work that scales with the session elsewhere in the serving path; we have not yet isolated it.”
- **How PACE behaves when planned protected spans exceed the resident budget frequently.** — The main benchmark rarely exercises rehydration, so end-to-end quality and latency under sustained oversubscription remain unclear.
  - Evidence: [b00058-c03fc2a31b] “it was rarely triggered, because in these sessions the protected set fits the budget”; [b00114-5b07f98541] “its benefit is shown in a scripted late-flag test.”

## Open questions

- Does bounded-position renumbering improve real repository-scale coding, tool-use, research, and multi-agent workflows when dependencies and distractors arise naturally?
- What planner precision and recall thresholds preserve an advantage over retention-only and retrieval-based alternatives?
- Can the foresight bonus be made relative and stable beyond the tested length without introducing cache-score oscillations?
- Which serving-path component causes per-turn latency to grow despite a fixed resident set?
- How does PACE perform under many concurrent persistent sessions, tier pressure, and frequent remote restoration?
- Can original temporal-distance information be retained explicitly for tasks where elapsed time or spacing is semantically meaningful?

## Proposed AIDB experiments

- **Hypothesis:** PACE retains a statistically meaningful advantage over retention-only on natural planned-agent workloads when dependencies come from an imperfect production planner.
  - Baseline: Retention-only using the same planner, cache budget, persistent-session implementation, model, tasks, and generated trajectories; include H2O as a secondary reference.
  - Primary metric: Paired end-to-end task success, stratified by planner edge precision and recall, with needed-span residency and rotary gap recorded at every dependent step.
  - Stop condition: Stop and reject the hypothesis if the pre-registered confidence interval for PACE minus retention-only includes zero or if benefit disappears in a majority of workload families.
- **Hypothesis:** Bounded renumbering does not degrade tasks whose answers depend on original temporal or positional distances.
  - Baseline: The same retained-token set with positions as written, plus a full-context control where hardware permits.
  - Primary metric: Accuracy on pre-registered temporal-order, elapsed-distance, recency, and timestamp-grounded queries, reported alongside ordinary recall and likelihood.
  - Stop condition: Stop deployment-oriented validation if bounded positions produce a statistically significant accuracy loss or exceed a pre-declared non-inferiority margin on any safety-critical temporal category.
- **Hypothesis:** PACE’s bounded KV state translates into useful production throughput under concurrency despite long-session latency growth and tier restoration.
  - Baseline: H2O, retention-only, and a retrieval-driven bounded-cache system under matched models, budgets, session traces, concurrency, and hardware.
  - Primary metric: Completed agent steps per second at fixed quality, with p50/p95/p99 latency, GPU and host memory, restoration frequency, and remote-tier bytes measured.
  - Stop condition: Stop if PACE fails to improve quality-adjusted throughput or violates pre-declared tail-latency and memory limits at any target concurrency level.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:46:47.430147+00:00`
- Document SHA-256: `ce97b31ba35a7c197b5b78cee0e1630e24e8ed1e6a8f632a6545c73b39e0db15`
- Metadata SHA-256: `716498707606930345eaf74c7a4e08566d4b71086e463d1315368fc6f31a5507`
- Blocks: 188
- Deterministic repair attempts: 0
