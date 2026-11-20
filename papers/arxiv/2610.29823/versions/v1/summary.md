# MemoryTax: The Bitter Lesson of Agent Memory

## Executive summary

MemoryTax tests whether prebuilt agent memory remains useful when capable models can search raw conversation history. Across seven methods and three models on one LoCoMo conversation, Mem0 improves over full context only for the weakest model, while its build costs exceed a complete full-context rollout. Writer–reader swaps show that stronger readers cannot fully repair information omitted by weaker memory writers. Pi with Claude Opus 5.5 reaches the reported cost–accuracy frontier, but most of its apparent accuracy lead over full context comes from unequal access to photo captions. The paper is decision-relevant but exploratory: one conversation, one accepted run per cell, a model judge, one erroneous key, defaults-only memory settings, and retry selection prevent broad or variance-aware conclusions.

## Problem

**Statement.** The paper asks whether systems that extract facts or graphs before questions arrive still help when a sufficiently capable model can instead inspect and search the uncompressed raw history.

**Why it matters.** Designed memory introduces extraction loss, retrieval choices, build cost, and operational complexity. Establishing when those costs buy accuracy—and when raw-record search is preferable—directly affects architecture and model-selection decisions for long-lived agents.

**Scope.** The empirical scope is one LoCoMo conversation whose history fits every tested context window. It compares full context, BM25, Mem0, Zep, Pi, Codex, and Claude Code under three models; it does not establish behavior across conversations, repeated stochastic runs, histories exceeding context windows, or tuned memory systems.

## Method

The study forms a factorial comparison of seven methods and three models. Full context exposes the entire raw history; BM25 retrieves nearby raw turns; Mem0 retrieves extracted facts; Zep retrieves temporal-graph edges; and three coding-agent harnesses receive one JSON conversation file and decide what to inspect with their tools. Each cell builds any required store and answers the question set. A GPT-4o-mini judge scores answers, while model-call list prices, calls, and tokens characterize resource use. Additional analyses exchange memory writers and readers and stratify questions by whether their evidence appears in a photo-sharing turn.

### Key components

- Evaluation input: LoCoMo conv-26, containing conversational sessions and several question types; adversarial questions are excluded.
- Memory representations: unmodified history, lexical retrieval over turns, extracted facts, a temporal graph, and agent-directed inspection of the raw file.
- Model conditions: GPT-4o-mini, GPT-6 Luna, and Claude Opus 5.5; the latter two use high reasoning effort.
- Agent isolation: each question starts in a fresh container and fresh session, with network access restricted to the model endpoint.
- Accounting: a rollout includes store construction and all questions; judge cost is excluded, cached input is included in token accounting, and embeddings affect cost but not token totals.
- Validity probes: cross-model writer–reader swaps test extraction ceilings, while the photo-evidence split partially diagnoses unequal input access.

### Assumptions

- The GPT-4o-mini judge and its lenient rubric are sufficiently aligned with substantive correctness for comparisons to be meaningful.
- Provider list prices and caching behavior are an appropriate proxy for deployer cost.
- A single accepted rollout represents each method–model cell despite stochasticity and permitted retries.
- Conv-26 is informative about the broader task because its per-method accuracies reportedly track the full LoCoMo set, although that supporting comparison is not shown in the supplied blocks.
- Default Mem0 and Zep configurations are representative enough to evaluate the designed-memory approach, rather than only those configurations.

## Main claims

- **The paper claims that designed agent memory mainly compensates for a weak model: Mem0 improves on full context under GPT-4o-mini but ceases to help under the stronger tested models.**
  - Evidence: [b00028-e5712a4c20] “With GPT-4o-mini, Mem0 scores highest. It scores 78%, against 74% for both full context and BM25; Zep scores 43%.”; [b00029-fcd0247b5c] “With the two stronger models, the patch stops helping.”
- **The paper claims that lossy memory construction imposes a writer-defined ceiling that cannot be removed merely by substituting a stronger reader.**
  - Evidence: [b00033-aae4b5aaed] “The model that writes the store limits every reader.”; [b00035-c3a88861e1] “A stronger reader does not recover what the writer left out.”
- **The paper claims that, for the strongest model, Pi occupies the best observed cost–accuracy position, while acknowledging that unequal photo-caption access explains most of its accuracy advantage over full context.**
  - Evidence: [b00037-079d71c4db] “Pi with Claude Opus 5.5 is the top of the frontier in Figure 1.”; [b00039-9cb16b66dd] “Photo captions account for most of Pi’s lead over full context.”

## Results

- **Under GPT-4o-mini, Mem0 achieves 78% correctness, compared with 74% for both full context and BM25 and 43% for Zep. The observed advantage over full context is therefore confined to four percentage points in this single rollout.**
  - Context: This is the paper’s strongest direct evidence that precomputed memory can help a weaker model, but the study reports no replication or uncertainty interval.
  - Evidence: [b00028-e5712a4c20] “It scores 78%, against 74% for both full context and BM25; Zep scores 43%.”
- **Mem0’s construction cost alone exceeds a complete full-context rollout for every model tested: $0.56 versus $0.43, $0.45 versus $0.29, and $25.88 versus $17.84. The estimated break-even points are 372, 545, and 596 questions, while the evaluated history receives 152 questions.**
  - Context: This controlled accounting is the clearest support for the proposed “memory tax.” It applies to the stated list prices, caching assumptions, dataset, and implementation defaults rather than proving a universal cost relationship.
  - Evidence: [b00031-337bdecc4c] “$0.56 against $0.43 with GPT-4o-mini, $0.45 against $0.29 with GPT-6 Luna and $25.88 against $17.84 with Claude Opus 5.5”; [b00031-337bdecc4c] “the build would pay for itself after 372, 545 and 596 questions on the same history; LoCoMo asks 152.”
- **The writer–reader experiment reveals substantial extraction dependence. On Zep’s GPT-4o-mini graph, the three readers score 43%, 43%, and 45%; on the Claude Opus 5.5 graph they score 66%, 71%, and 87%. Mem0 shows the same ordering with narrower gaps: 78%, 83%, and 84% from the weaker writer’s store versus 89%, 91%, and 95% from the stronger writer’s store.**
  - Context: Because retrieval invokes no language model, swapping readers isolates some effect of store construction. It supports a writer ceiling within these two systems, though it does not separate omitted information from other writer-dependent representation or retrieval effects.
  - Evidence: [b00035-c3a88861e1] “On Zep’s GPT-4o-mini graph, GPT-4o-mini, GPT-6 Luna and Claude Opus 5.5 score 43%, 43% and 45%; on the graph Claude Opus 5.5 wrote, 66%, 71% and 87%.”; [b00035-c3a88861e1] “78%, 83% and 84% from GPT-4o-mini’s store, 89%, 91% and 95% from Claude Opus 5.5’s.”
- **With Claude Opus 5.5, Pi scores 99% at $6.95 per rollout, while full context scores 95% at $17.84. However, after restricting evaluation to the 88 questions without photo evidence, Pi scores 100% and full context scores 99%, reducing the matched-evidence difference to one answer.**
  - Context: Pi is the strongest observed operating point, but the headline accuracy comparison is confounded because agents can read captions withheld from memory methods. The restricted split is more diagnostic of search versus full-context reading, yet it remains post-stratified and small.
  - Evidence: [b00037-079d71c4db] “Pi with Claude Opus 5.5 is the top of the frontier in Figure 1. No other cell scores higher: Pi scores 99% for $6.95 a rollout, while full context with the same model scores 95% for $17.84.”; [b00039-9cb16b66dd] “On the 88 questions without photo evidence, Pi scores 100%, and full context, Mem0, Codex and Claude Code 99% each (Table 4).”; [b00013-63201f86f3] “Where the two read the same text they differ by one answer;”

## Experimental evaluation

### Datasets

- LoCoMo conv-26: one conversation with 419 turns in 19 sessions and 152 single-hop, multi-hop, temporal, and open-domain questions. Adversarial questions are excluded.
  - Evidence: [b00018-5420c025d1] “LoCoMo conv-26 [9]: 419 turns in 19 sessions and 152 single-hop, multi-hop, temporal and open-domain questions.”; [b00018-5420c025d1] “LoCoMo’s adversarial questions are left out, as in Mem0’s evaluation [1].”

### Baselines

- Full context: the model receives all raw history.
  - Evidence: [b00020-139e4d6bd6] “Full context raw history all of it”
- BM25: raw turns are stored and the model sees the top-8 turns with a ±2-turn neighborhood.
  - Evidence: [b00020-139e4d6bd6] “BM25 raw turns top-8 turns, ±2”
- Mem0 and Zep: extracted-fact and temporal-graph memory baselines, respectively, using default extraction and retrieval.
  - Evidence: [b00020-139e4d6bd6] “Mem0 extracted facts top-200 facts Zep temporal graph top-20 edges”; [b00021-a55e071894] “both with default extraction and retrieval [1, 2].”
- Coding-agent harnesses: Pi, Codex, and Claude Code search a raw-history JSON file using their available tools.
  - Evidence: [b00020-139e4d6bd6] “Pi, Codex, Claude Code raw history, one JSON file what its tools read”

### Metrics

- Correct-answer rate, assigned by GPT-4o-mini using Mem0’s judge rubric; empty answers are incorrect.
  - Evidence: [b00026-5048be7104] “GPT-4o-mini grades every answer with Mem0’s 2025 judge rubric [1]; empty answers count as wrong.”
- Rollout cost: list price of all language-model and embedding calls, excluding the judge.
  - Evidence: [b00026-5048be7104] “Cost is the list price of every model call, LLM and embedding (text-embedding-3-small), with the judge excluded.”
- Operational consumption: language-model calls and input/output tokens, including cached input but excluding embeddings from token counts.
  - Evidence: [b00026-5048be7104] “Tokens are those calls’ input and output tokens, cached input included; embeddings are not counted.”

### Ablations

- Writer–reader cross-over: each model answers using retrievals from stores written by each other model, testing whether reader strength can compensate for memory construction.
  - Evidence: [b00033-aae4b5aaed] “each model answers from the retrievals of the others’ stores”
- Photo-evidence stratification: performance is split between questions whose evidence occurs in photo-sharing turns and all remaining questions.
  - Evidence: [b00080-7e01c503b0] “the 64 questions with evidence in a turn that shares a photo, whose caption only the agents could read, and on the other 88.”

### Negative results

- With GPT-6 Luna, Mem0 trails full context rather than improving it; with Claude Opus 5.5, it only ties full context.
  - Evidence: [b00029-fcd0247b5c] “With GPT-6 Luna, full context scores 92%, BM25 82%, Mem0 80% and Zep 51%”; [b00029-fcd0247b5c] “With Claude Opus 5.5, Mem0 and full context both score 95% and Zep 87%”
- Neither Mem0 nor Zep appears on the reported cost–accuracy frontier.
  - Evidence: [b00031-337bdecc4c] “Mem0 and Zep are never on the frontier of Figure 1”
- Weak models do not reliably operate coding-agent tools: Codex opens the conversation for only three questions in four, and Claude Code almost never does.
  - Evidence: [b00028-e5712a4c20] “Codex opens the conversation file for three questions in four and Claude Code almost never”


## Limitations

- The experiment uses one of LoCoMo’s conversations and one run per cell, so small differences have unknown variance and may reverse under replication.
  - Evidence: [b00043-cdc532bf1f] “One conversation of LoCoMo’s ten, and one run per cell. Differences of a few questions may not hold in a second run.”
- Grading depends on a lenient GPT-4o-mini judge, and the benchmark contains at least one incorrect answer key.
  - Evidence: [b00045-c1a61e0a28] “A GPT-4o-mini judge with a lenient rubric, and at least one wrong answer key.”
- Agents and memory methods receive unequal evidence because only agents can read photo captions, confounding their aggregate comparison.
  - Evidence: [b00047-690e14098a] “The agents could read photo captions that the memory methods were not given (Section 5).”
- Every evaluated history fits the model context windows, leaving behavior on genuinely overlength histories unresolved.
  - Evidence: [b00049-32c7d00630] “The history fits in every model’s context window, so full context is always an option.”; [b00049-32c7d00630] “Results may differ on other benchmarks such as LongMemEval [14] and on histories that do not fit.”
- Mem0 and Zep use defaults rather than tuned configurations, and cost conclusions depend on list prices and provider caching.
  - Evidence: [b00051-8f71434005] “Mem0 and Zep run with their default extraction and retrieval, and other settings may do better.”; [b00051-8f71434005] “Costs are list prices and depend on each provider’s caching.”
- Failed or answerless agent trials are rerun and only accepted trials are counted, but retry incidence and rejected-trial costs are not reported; this may bias reliability and cost estimates.
  - Evidence: [b00085-3ee3c68d69] “A trial that fails or ends without an answer is run again, and only the accepted trial is counted.”

## Reproducibility

**Status:** partial

The protocols are unusually concrete for a short study and the aggregate tables permit consistency checks, but independent reproduction remains incomplete without code, full prompts, raw outputs, retry records, and immutable environment and pricing specifications. The one-run design also prevents reproduction from distinguishing implementation mismatch from ordinary sampling variation.

**Available artifacts**

- A named interactive version is identified in the paper.
- Method and software versions are reported for Mem0, Zep, Pi, Codex, Claude Code, and Harbor.
- The supplied blocks describe retrieval sizes, agent isolation, reasoning effort, time and turn limits, judging, and cost accounting.
- Full aggregate result tables and the writer–reader and photo-evidence splits are supplied.

**Missing pieces**

- Executable experiment code or an archived repository is not identified in the supplied blocks.
- The actual prompt bodies are absent from the supplied document blocks; only prompt section labels are present.
- Per-question predictions, judge decisions, model-call logs, and raw cost traces are not supplied.
- Randomness controls, seeds, run-to-run variance, retry counts, rejected trials, and their resource consumption are not reported.
- Exact container images, dependency lockfiles, proxy configuration, and provider price snapshot are not supplied.
- A machine-readable manifest connecting each result to the precise input, model endpoint, and accepted trial is not supplied.

## AIDB assessment

- Novelty: The main contribution is not a new memory algorithm but an integrated cost–accuracy comparison that places precomputed memory, retrieval, full context, and tool-using coding agents under multiple reader strengths. The writer–reader cross-over and explicit build-cost amortization are particularly useful diagnostic framings.
- Usefulness: High as a hypothesis-generating systems study and as a warning against adopting extracted memory without measuring build amortization, information loss, and model strength. Low-to-moderate as direct deployment evidence because the benchmark, run count, input parity, tuning coverage, and retry accounting are too narrow for universal architectural guidance.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled comparisons reveal actionable failure modes: memory construction can dominate cost, lossy stores constrain later readers, and harness choice materially changes outcomes. Nevertheless, the headline agent advantage is partly attributable to unequal evidence, while single-run results and accepted-trial selection leave both accuracy and cost uncertainty unquantified. AIDB should treat the conclusions as strong experimental hypotheses, not settled general laws.

## Uncertainties

- **It is unresolved whether model-directed search is intrinsically more accurate than reading the same complete record.** — This is central to choosing an agent harness over full context. The aggregate comparison cannot answer it because the agent receives photo captions that full context does not.
  - Evidence: [b00039-9cb16b66dd] “Whether searching the record answers more than reading all of it, this study does not settle.”
- **The stability of small accuracy differences is unknown because each cell has only one run.** — Several conclusions depend on only a few questions, so stochastic variation could change rankings or frontier membership.
  - Evidence: [b00043-cdc532bf1f] “Differences of a few questions may not hold in a second run.”
- **The generality of the claimed memory ceiling beyond Mem0 and Zep defaults is untested.** — Alternative extraction, chunking, reranking, or query-time reconstruction might preserve more evidence and reduce writer dependence.
  - Evidence: [b00051-8f71434005] “other settings may do better.”
- **Reported agent economics exclude failed or answerless attempts that were replaced by accepted trials.** — A production system pays for failures as well as successful retries; omitting them can overstate reliability and understate expected cost.
  - Evidence: [b00085-3ee3c68d69] “only the accepted trial is counted.”

## Open questions

- Do Pi and full context retain their ranking when both receive exactly the same text, including all photo captions?
- How large are accuracy, cost, call-count, and latency variances across repeated runs for every cell?
- How do the methods behave when histories exceed the model context window and full context is no longer feasible?
- Does tuning extraction, retrieval depth, reranking, or memory-writing models move Mem0 or Zep onto the cost–accuracy frontier?
- How frequently were agent trials rerun, why did they fail, and what are reliability and cost when all attempts are counted?
- Does the writer ceiling persist for verbatim chunk stores or hybrid stores that retain links back to raw evidence?
- How sensitive are conclusions to human adjudication, alternative model judges, and correction of erroneous answer keys?

## Proposed AIDB experiments

- **Hypothesis:** When evidence access is exactly matched, Pi with the strongest tested model remains cheaper than full context but has no practically meaningful correctness advantage.
  - Baseline: Full context and Pi using the identical official conversation file, including captions, identical answer rules, and corrected answer keys; run both repeatedly on the full question set.
  - Primary metric: Paired difference in human-adjudicated correctness, reported with a confidence interval, alongside total cost including every failed and retried attempt.
  - Stop condition: Stop when the confidence interval is narrow enough to determine whether the correctness difference crosses a prespecified one-answer equivalence margin and the cost ranking is stable across repetitions.
- **Hypothesis:** Precomputed extracted memory loses its advantage as reader capability rises because writer omissions dominate, whereas verbatim retrieval degrades less under writer–reader mismatch.
  - Baseline: Mem0 and Zep defaults versus BM25 and a verbatim semantic-retrieval store, crossed over weak and strong writers and readers on all available benchmark conversations.
  - Primary metric: Correctness loss relative to full context for each writer–reader pair, with omitted supporting evidence manually classified for errors.
  - Stop condition: Stop after repeated runs show either a consistent interaction between writer strength and representation type or a confidence interval excluding a practically meaningful interaction.
- **Hypothesis:** Designed memory becomes cost-effective only beyond a workload-dependent query threshold, and that threshold changes under tuned retrieval and full retry accounting.
  - Baseline: Full context, BM25, tuned Mem0, tuned Zep, and Pi on histories both within and beyond context limits, with identical evidence and all build, query, failure, and retry costs included.
  - Primary metric: Expected total cost at matched human-adjudicated correctness as a function of cumulative questions per history.
  - Stop condition: Stop once each method’s break-even region is bounded tightly enough to support an architecture choice, or once a method is dominated in both cost and correctness throughout the tested workload range.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:04.044240+00:00`
- Document SHA-256: `a6078401254157bb907ee7066eb404f56479a8ff3a05a138036abb594ab7b945`
- Metadata SHA-256: `73c81e873540ed7ae1c73c574ef61162d97fee0d4af7ba0676e262bf6b62beca`
- Blocks: 91
- Deterministic repair attempts: 0
