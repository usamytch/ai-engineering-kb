# CoReMem: Cost-Internalizing Memory for Successive Coding Tasks with Prospective Valuation

## Executive summary

CoReMem targets agents solving successive tasks in a persistent repository, where memory is written before the next task is known. It prospectively values trajectory segments on the next task, retains compact location and executable-check anchors, and adapts the actor with an outcome-and-step reward plus provenance-gated memory-value credit. On ChainSWE, post-training improves resolution and efficiency across three open-weight actors; for the 27B actor, resolution rises from 21.0% to 25.7% while steps and total cache-aware tokens fall. Controlled ablations support the cost reward and gated credit, but evidence is concentrated in Python, one principal benchmark/harness, small model coverage, and author-run evaluations. Reproducibility is partial because detailed protocols are supplied but the code link is anonymous and several decisive artifacts are absent from the supplied blocks.

## Problem

**Statement.** An agent must decide what information to preserve after one coding task for an unknown later task on the inherited repository, and must learn when using that information reduces work rather than distracting execution.

**Why it matters.** Existing memory systems may improve resolution while increasing overall cost: the paper reports that none of the tested existing forms reduced both steps and total tokens, and each spent more memory-module tokens than it saved.

**Scope.** The work studies sequential coding sessions in a persistent workspace. Each next task inherits earlier edits, while only a memory text—not the preceding trajectory—crosses the session boundary.

## Method

CoReMem first estimates prospective memory value by rerunning the unseen next task from the same inherited repository state with and without candidate memory. It partitions the prior trajectory by role, ablates segments, and converts useful material into compact anchors: repository locations and executable checks. It then post-trains the actor in rollout groups mixing own memory, no memory, and memory from another repository. A reward ranks every successful run above failures while charging steps within successful runs. The mean own-memory versus no-memory reward gap estimates on-policy memory value; that extra value is assigned only to steps whose first-use anchors can be traced to memory, while all steps retain outcome credit.

### Key components

- Prospective segment valuation compares next-task runs from a fixed inherited state and estimates each segment’s contribution by removing it from the full trajectory memory.
- The induced memory template preserves commands and repository content, compresses test output and changes, and drops reasoning narrative and scratch-file manifests.
- Anchors are concrete repository locations or executable checks that the next task can use directly and that also enable traceable attribution.
- Training groups contain no-memory sessions, own-memory sessions, and one misplaced-memory session to discourage indiscriminate memory following.
- The reward prioritizes successful resolution over all step savings, then penalizes step count within successful sessions and credits partial test progress for failures.
- Provenance-gated credit applies the measured memory-value term to memory-driven steps while retaining session-outcome credit on every step.

### Assumptions

- Successive tasks share a repository state, and the next task is unknown when memory is written.
- Repository locations and commands can be extracted reliably enough by string matching to serve as actionable and traceable anchors.
- Paired stochastic rollouts from the same boundary provide a useful estimate of memory value despite sampling variance.
- Steps and cache-aware tokens are adequate operational proxies for effort, although latency and energy are not measured.
- The writer can produce a valid short structured memory, with a corrective retry or separate fallback call when needed.

## Main claims

- **The prospective-value procedure yields a compact memory centered on actionable locations and checks rather than narrative reasoning.**
  - Evidence: [b00045-a14dc73996] “What saves the next task effort is where to look and what to run, not the narrative”; [b00049-4650df60b4] “The memory keeps the whole median step saving of M with 6% of its bytes.”
- **The training objective explicitly separates session outcome credit from an on-policy estimate of memory value and routes the latter to memory-driven steps.**
  - Evidence: [b00060-38c87af02a] “The first is the session’s outcome credit”; [b00060-38c87af02a] “The second is the memory’s value credit”; [b00067-00195a145f] “The gate marks traceable use of the memory, not the step’s own effect on the outcome”
- **The paper analytically argues that uniformly broadcasting memory value cannot specifically encourage memory use, whereas gating creates a directed policy-gradient term.**
  - Evidence: [b00258-05f15b0e5d] “Paid to every step instead, the same value multiplies 𝔼⁡[∇θ​log​πθ​(τ∣m)]=0 and teaches nothing about memory use.”; [b00076-1c9ade79e4] “the second moves how often the actor acts on the memory, up where the memory pays and down where it does not”
- **The authors report that the frozen CoReMem memory reduces steps across all evaluated actor models without reducing resolution.**
  - Evidence: [b00083-6a283b859f] “our memory lowers steps on all six actor models”; [b00083-6a283b859f] “without lowering resolution, which rises on five of them and is unchanged on Opus”

## Results

- **For Qwen3.8-27B-FP8 on ChainSWE, CoReMem raises overall resolve rate from 21.0% without memory to 25.7%, while mean steps fall from 35.1 to 29.2 and total cache-aware tokens per session fall from 32.2K to 28.5K.**
  - Context: This is the strongest central comparison because it jointly improves task success and both reported effort measures. It compares the post-trained actor plus CoReMem against the same actor family without memory on the held-out test split.
  - Evidence: [b00062-fe100f95ef] “No memory 19.1 30.9 (22.8) 23.4 40.5 (30.4) 21.0 35.1 (26.0) 32.2 (24.7)”; [b00062-fe100f95ef] “CoReMem 25.1 26.2 (18.0) 26.5 33.4 (25.0) 25.7+22% 29.2 (20.0)−17% 26.6 (18.5) 1.9 (1.7) 28.5 (20.3)−11%”
- **Across the three post-trained open-weight actors, total tokens fall by 9% to 19%, resolution rises by 22% to 27%, and resolve per total token rises by 38% to 46%, averaging 41%.**
  - Context: This aggregate supports cross-model consistency within the tested open-weight set, but it does not cover the three API-served actors because they were evaluated only with the frozen memory layer.
  - Evidence: [b00085-124bc867a8] “at 9% to 19% fewer total tokens, and raises resolution by 22% to 27%, so resolve per total token rises by 38% to 46%, 41% on average”
- **The memory design yields 1.32 used anchors per 1K characters, versus 0.92 for MemOp, 0.19 for ReasoningBank, and 0.14 for Mem0.**
  - Context: This diagnostic supports the proposed mechanism—dense actionable references—but anchor use is defined by textual occurrence, not a causal intervention on each anchor.
  - Evidence: [b00090-13e625c701] “the next task acts on 1.32 of them per thousand characters against 0.92 for MemOp, 0.19 for ReasoningBank and 0.14 for Mem0”
- **In the 27B ablation, resolve-only RL reduces steps from 32.6 to 30.4; adding the cost-internalizing reward reduces them further to 29.7, while the full method records 29.2.**
  - Context: This comparison isolates evidence that charging steps within successful runs contributes beyond resolution-only training, although the full method is not uniformly best on every model: the reported 9B M1+M2 step count is lower than the full method.
  - Evidence: [b00095-751ae17479] “Resolve-only RL lowers steps on 27B from 32.6 to 30.4”; [b00095-751ae17479] “charging steps inside success (M1+M2) lowers them further, to 29.7 and 63.8, and the full method stays at 29.2 and 72.4.”
- **For the 27B actor, adding provenance-gated value credit reduces the step cost of misplaced memory from 2.1 to +0.3 and increases the memory benefit from +1.7 to +2.3 resolution points.**
  - Context: This is the most direct behavioral ablation for selective memory use. The appendix interval for the +0.3 misplaced-memory effect includes zero, so the evidence supports eliminating a detectable penalty more strongly than proving a positive residual cost.
  - Evidence: [b00097-661f625903] “without the value credit a misplaced memory costs the 27B actor model 2.1 steps, while with it the cost shrinks to +0.3”; [b00097-661f625903] “the memory benefit grows from +1.7 to +2.3 points on 27B.”

## Experimental evaluation

### Datasets

- ChainSWE is the primary benchmark: 100 repository-specific task chains are split by repository into 52 training chains with 97 boundaries and 48 test chains with 96 boundaries.
  - Evidence: [b00217-d5472126ff] “100 chains of successive tasks”; [b00217-d5472126ff] “a training half of 52 chains (97 boundaries) and a test half of 48 chains (96 boundaries), so no repository appears in both.”
- SWE-bench Verified evaluates the adapted actors without memory on all 500 single-task instances.
  - Evidence: [b00236-fc10b52a36] “All 500 instances, one task each, no memory, 3 replays per row.”
- External checks include SWEContextBench, SWE-Bench-CL, and 94 ChainSWE test tasks under the OpenHands harness.
  - Evidence: [b00249-6cc91aa725] “on SWEContextBench with the inherited tree and on SWE-Bench-CL with the tree reset.”; [b00249-6cc91aa725] “Table 6 runs 94 of the 96 next tasks of the test split”

### Baselines

- No memory and full previous-task history.
  - Evidence: [b00221-3fb043c68f] “No memory runs every next task from the inherited tree with its task description alone. Full history injects the most recent part of the transcript”
- Mem0, MemOp, and ReasoningBank, run with their official instructions and memory write/read calls.
  - Evidence: [b00221-3fb043c68f] “Mem0 (Chhikara et al., 2025), MemOp (Guo et al., 2026) and ReasoningBank (Ouyang et al., 2026) run with their official instructions”
- CoReMem without training isolates the memory layer on a frozen actor; resolve-only RL and M1+M2 isolate training components.
  - Evidence: [b00087-3c678244c0] “w/o training runs M1 on the frozen actor model, resolve-only RL trains on the resolution term alone and M1+M2 trains without the value credit”

### Metrics

- Resolve rate, overall and on linked/unlinked boundaries, based on hidden tests passing at session end.
  - Evidence: [b00223-14d2fd038e] “Resolve rate is the share of next tasks whose hidden tests pass on the working tree at the end of the session”
- Steps, defined as assistant turns with one command each.
  - Evidence: [b00223-14d2fd038e] “Steps is the number of assistant turns of a session, each one command.”
- Cache-aware actor, writer, and total tokens per session; resolve per thousand actor or total tokens.
  - Evidence: [b00223-14d2fd038e] “Tokens per session count every call of the session, cache-aware”; [b00223-14d2fd038e] “Resolve per token divides the overall resolve rate by the thousand actor or total tokens per session.”
- API-model list-price cost per session and resolve per dollar.
  - Evidence: [b00223-14d2fd038e] “USD per session prices the same calls at the provider’s list rates”; [b00223-14d2fd038e] “resolve per USD divides the resolve rate by it.”
- Used anchors per memory and per 1K memory characters.
  - Evidence: [b00093-b08880cb5c] “Memory layer Anchors per 1K chars Used anchors per memory Used anchors per 1K chars”

### Ablations

- M1 compares the anchor memory on frozen actors; M2 compares resolution-only training with a reward that charges successful-run steps; M3 removes provenance-gated value credit.
  - Evidence: [b00087-3c678244c0] “We further conduct ablations on the three modules of §3”
- Misplaced-memory arms test whether actors indiscriminately follow structurally valid but repository-inappropriate memory.
  - Evidence: [b00058-78cdd6dd31] “one misplaced-memory session (m~) carries a real memory written for another repository, right in form and wrong in content.”
- Segment ablations separately evaluate reasoning, commands, repository content, test feedback, changes, outcome, scratch files, and compressed variants.
  - Evidence: [b00287-95c4ce1563] “the agent’s reasoning (C1), the commands it issued (C2), the repository content it read (C3), the feedback of its tests (C4), the change it left (C5), its outcome (C6) and its scratch files (C7).”

### Negative results

- No tested existing memory form reduces both steps and total tokens; each spends more memory-module tokens than it saves.
  - Evidence: [b00022-8e1897dcd5] “no existing form reaches the quadrant where steps and total tokens both fall.”; [b00022-8e1897dcd5] “each spends more tokens on its memory than it saves.”
- Reasoning text and the diff body add no measured step savings and increase token cost.
  - Evidence: [b00045-a14dc73996] “removing the reasoning text or the diff body adds no steps and saves tokens”
- A likelihood-ratio provenance alternative is uninformative in the reported pilot.
  - Evidence: [b00274-e89439ea16] “In a pilot of 36 sessions on the 27B actor its AUC is 0.506 for real against the null”
- On the 9B ablation, the full method uses more steps than M1+M2, so provenance gating does not show an effort advantage in that comparison.
  - Evidence: [b00095-751ae17479] “M1+M2) lowers them further, to 29.7 and 63.8, and the full method stays at 29.2 and 72.4.”


## Limitations

- The main experiments use Python repositories in mini-swe-agent; other languages and larger actors remain untested.
  - Evidence: [b00106-b719390b7d] “Our main experiments use Python repositories in the mini-swe-agent harness”; [b00106-b719390b7d] “Other programming languages and larger actor models remain to be tested.”
- Post-training evidence covers only three open-weight actor models; the API-served models test the frozen memory layer, not actor adaptation.
  - Evidence: [b00106-b719390b7d] “post-training covers the three open-weight actor models.”
- Efficiency is measured through steps and cache-aware tokens, without wall-clock latency or energy measurements.
  - Evidence: [b00106-b719390b7d] “We measure effort by steps and cache-aware tokens and do not report wall-clock latency or energy use.”
- The method does not yet address accumulation and refresh over long repository histories.
  - Evidence: [b00106-b719390b7d] “How memory should be accumulated and refreshed over longer repository histories is future work.”
- The provenance gate is a heuristic string matcher with measurable null leakage, so credited steps are not equivalent to causal attribution.
  - Evidence: [b00270-79e6f4fb9d] “Memory-free sessions scored against the memory they would have seen give a leakage null of 1.61% of steps”; [b00067-00195a145f] “The gate marks traceable use of the memory, not the step’s own effect on the outcome”
- Replay counts differ across models, including only one replay for Opus, which weakens precision and comparability across actor families.
  - Evidence: [b00225-3b36b2b030] “12 for the frozen 9B rows, 6 to 7 for 27B, 6 for DeepSeek, 3 for Gemma and Luna and 1 for Opus.”
- One external evaluation adapted writer instructions after observing initial runs, introducing a post-observation design choice.
  - Evidence: [b00250-16f44911a7] “The adapted instructions were written after observing the first runs on the set”

## Reproducibility

**Status:** partial

The paper supplies unusually detailed protocol, optimization, ablation, and accounting information, sufficient to understand the intended implementation. Reproduction remains partial because the blocks do not expose the code artifact, complete prompts/configuration, raw runs, model adapters, or full infrastructure specification.

**Available artifacts**

- Detailed data split and linked-boundary definition.
- Actor models, context windows, step limits, replay counts, and significance procedure.
- Training-group composition, rewards, LoRA settings, optimizer, learning rates, update counts, truncation, and timeouts.
- Segment definitions, anchor matcher rules, memory-template derivation, and reported deployed-template hash prefix.
- An author-reported anonymous code link.

**Missing pieces**

- A stable, inspectable code URL in the supplied material.
- Complete executable configuration files and container/image identifiers.
- Full memory-writing instruction text; the supplied blocks describe the figure but do not contain its verbatim body.
- Raw trajectories, generated memories, replay outputs, bootstrap samples, and trained adapter weights.
- Compute budget, hardware configuration, random seeds beyond the stated ablation bootstrap seed, and total training cost.
- Independent reproduction.

## AIDB assessment

- Novelty: High conceptual novelty within the paper’s framing: it connects next-task counterfactual valuation, compact repository/check anchors, on-policy memory-value estimation, and step-level provenance routing in one cost-aware framework. The strongest novelty is not generic memory compression but measuring value on the unseen next task from inherited state and using the same value notion for both memory design and actor adaptation.
- Usefulness: Potentially high for persistent coding agents where token and interaction costs matter. The frozen memory layer is immediately relevant because it reduces steps across six actors, while post-training shows larger gains for supported open-weight models. Adoption should wait for independent reproduction, multilingual and longer-history tests, latency measurements, and release of operational artifacts.
- Confidence: medium
- Recommended action: read
- Rationale: The central comparisons are strong and unusually cost-aware; controlled component ablations and external checks add credibility. Confidence stops at medium because the principal evidence is author-run, concentrated in Python and one main benchmark/harness, some replay budgets are small, provenance is heuristic, and full reproducibility artifacts are unavailable in the supplied material.

## Uncertainties

- **How much of the post-training gain comes from general efficient-coding adaptation rather than memory-specific behavior?** — The adapted actors improve on SWE-bench Verified even without memory, so the headline post-training gain cannot be attributed entirely to better use of cross-task memory.
  - Evidence: [b00235-162889746b] “one task per instance and no memory, the post-trained actor model resolves 4.5 points more than its untrained counterpart on 27B and 6.4 on 9B”
- **Does anchor occurrence accurately identify meaningful memory use?** — The gate has nonzero leakage, removes many early matches, and explicitly measures provenance rather than causal effect; misclassification could distort both credit assignment and the mechanism analysis.
  - Evidence: [b00270-79e6f4fb9d] “the veto removes about 88% of them”; [b00067-00195a145f] “not the step’s own effect on the outcome”
- **Will the method remain cost-effective as memory accumulates across many tasks rather than one boundary?** — Long-lived repositories require conflict handling, staleness control, refresh, deletion, and bounded retrieval costs, none of which is resolved by the current one-boundary design.
  - Evidence: [b00106-b719390b7d] “How memory should be accumulated and refreshed over longer repository histories is future work.”
- **How robust are claims for API-served actors with low replay counts?** — Stochastic variance may be poorly characterized, especially for the actor evaluated once, limiting confidence in cross-model generalization.
  - Evidence: [b00225-3b36b2b030] “3 for Gemma and Luna and 1 for Opus.”

## Open questions

- Can the memory template and provenance matcher transfer to statically typed, compiled, polyglot, or non-test-centric repositories?
- What is the separate causal contribution of general post-training versus memory-conditioned training when both are evaluated with and without memory under matched checkpoints?
- How should multiple memories be merged, invalidated, refreshed, access-controlled, and redacted over long task chains?
- Do step and token reductions translate into lower wall-clock latency, energy, and monetary cost under realistic parallel tool execution and cache policies?
- Would semantic or execution-level provenance outperform anchor string matching without introducing excessive training cost?
- How sensitive are results to writer quality, memory corruption, repository drift, and adversarial or stale commands?

## Proposed AIDB experiments

- **Hypothesis:** CoReMem’s post-training benefit is specifically larger when valid cross-task memory is present than when no memory is present, beyond general efficient-coding adaptation.
  - Baseline: A factorial comparison using the same base actor and training budget: untrained/no memory, untrained/CoReMem, post-trained/no memory, and post-trained/CoReMem, plus a post-trained shuffled-memory arm.
  - Primary metric: Difference-in-differences for resolve per total cache-aware token, with paired repository-chain confidence intervals; also report resolution and steps separately.
  - Stop condition: Stop after the preregistered number of independent repository chains and replays; reject the memory-specific hypothesis if the interaction confidence interval includes zero or if resolution decreases.
- **Hypothesis:** Provenance-gated credit improves selective memory use more reliably than whole-trajectory credit across model sizes and languages.
  - Baseline: Matched training runs with identical initialization, rollouts, reward, and compute, differing only between gated credit, whole-trajectory credit, and outcome-only credit.
  - Primary metric: Misplaced-memory step cost jointly with valid-memory resolution benefit, evaluated on held-out repositories in at least one non-Python language.
  - Stop condition: Stop after fixed seeds and replay budgets; reject the hypothesis if gating fails to reduce misplaced-memory cost without reducing valid-memory resolution benefit on most preregistered model-language settings.
- **Hypothesis:** A bounded refresh policy preserves CoReMem’s efficiency over long repository histories better than retaining only the latest memory or concatenating all memories.
  - Baseline: Latest-memory-only, unbounded concatenation, fixed-size recency selection, and CoReMem with explicit merge/refresh/invalidation over long task chains.
  - Primary metric: Resolve per total token across chain position, accompanied by wall-clock latency and stale-anchor execution rate.
  - Stop condition: Stop at the preregistered chain length or when all methods exceed the same memory budget; reject the hypothesis if refreshed CoReMem does not improve area under the resolve-per-token-by-position curve or increases stale-anchor use.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:33:30.472618+00:00`
- Document SHA-256: `0ae9c59378c49b66958367b2f82c90085619025a0947540ac072c21226e064b1`
- Metadata SHA-256: `c08b55b16fc1c47e574a60e4ec5b43dc32045b16d9994c4722b309aaf77f0aaa`
- Blocks: 330
- Deterministic repair attempts: 1
