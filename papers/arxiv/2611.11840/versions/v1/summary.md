# Correct Answers from Insufficient Histories: A Controlled Study of Agent Memory Evaluation

## Executive summary

The paper diagnoses a validity failure in agent-memory evaluation: agreement with a complete-history reference can look correct even when the visible context does not determine the answer. It introduces executable sufficiency and insufficiency certificates, then tests two hosted readers, compact packing, and an LLM judge on synthetic device logs. Both readers frequently answer insufficient inputs and sometimes match hidden references; compact CSV yields no conclusive appropriateness gain. A deterministic program solves the certified grammar, while the highly accurate judge still makes support errors. The protocol is valuable and unusually auditable, but evidence is restricted to short synthetic histories, fixed English queries, shared certification logic, and unpinned hosted models.

## Problem

**Statement.** Agent-memory evaluations often score an answer against a reference computed from the complete history without separately asking whether the history actually shown to the reader uniquely determines that answer.

**Why it matters.** This can reward unsupported guessing as successful memory behavior and can mislabel a truncated but already sufficient history as unanswerable, confounding evidence access, reasoning, and abstention.

**Scope.** The paper studies controlled reading and evaluation over executable synthetic device logs with repeated reports, rejected actions, state transitions, and temporal cutoffs. It does not establish prevalence in deployed memory systems, natural-language evidence assessment, or superiority of a memory architecture.

## Method

The authors define sufficiency relative to public task guarantees: all legal histories compatible with the exact packed context must yield the same executable answer. Insufficiency is certified by two legal histories that repack to byte-identical contexts but have different answers. Chronological sufficiency is certified using a complete-log marker, a complete record after the cutoff, or an already visible first accepted route. Inputs without either certificate remain unclassified. Reader outputs are scored separately for complete-history reference agreement and context appropriateness.

### Key components

- An executable device-log environment with duplicate reports, accepted or rejected actions, three evidence labels, and four fixed query operators.
- Answer validation using environment snapshots, Python replay, and SQL deduplication and temporal queries.
- Exact repacking of insufficiency witnesses, requiring identical packed UTF-8 bytes and different executable answers.
- Qwen3-32B confirmation and fixed-input DeepSeek-V4-Flash replication on identical visible inputs.
- History-clustered bootstrap intervals and paired format contrasts restricted to jointly certified questions.
- A held-out evaluator audit with constructed controls, deterministic programs, an LLM judge, and a program-first hybrid.

### Assumptions

- The declared event grammar and public semantics correctly formalize the controlled task.
- Chronological prefixes begin at the start of the log and are ordered by event time.
- A concrete answer is appropriate only when uniquely determined; applications favoring guesses need another objective and explicit error costs.
- Unclassified inputs are unresolved rather than presumed insufficient.
- Program agreement checks implementation consistency within declared semantics, not unrestricted natural-language truth.

## Main claims

- **Reference agreement and evidence sufficiency are distinct measurement axes; a correct-looking answer may be unsupported by the visible history.**
  - Evidence: [b00005-a2e3788a5a] “A model can agree with the hidden reference after a decisive tool outcome has been removed.”; [b00044-8fd509eb3c] “The reference score remains useful, but answers a different measurement question.”
- **The paper provides constructive, auditable insufficiency certificates rather than treating truncation or failed search as proof of insufficiency.**
  - Evidence: [b00036-5efb563b5e] “The resulting contexts must be byte-identical.”; [b00031-e5c4082237] “Unclassified does not mean insufficient.”
- **The evidence-sensitive answering contract fails in both hosted reader configurations tested.**
  - Evidence: [b00095-a6fe21b123] “Both readers frequently supply concrete values when compatible histories force different answers; some match the original reference.”; [b00076-bdc4a5c36f] “The diagnosis persists under explicit instructions against guessing.”
- **The study is an evaluation diagnosis, not a new retrieval or memory architecture and not a demonstration of natural-domain transfer.**
  - Evidence: [b00011-0cb128496d] “Our contribution is an executable, auditable evaluation protocol and a controlled empirical diagnosis, rather than a new retrieval or memory architecture.”; [b00101-463da1b580] “Transfer to independent tasks, longer histories, and natural language remains open.”

## Results

- **On certified insufficient raw prefixes, Qwen produced concrete answers on 196/203 cases, abstained on 7/203, and matched the hidden reference on 87/203. DeepSeek produced concrete answers on 182/203, abstained on 21/203, and matched the hidden reference on 85/203.**
  - Context: This fixed-input replication supports the central diagnosis: reference hits remain common even though compatible legal histories yield different answers.
  - Evidence: [b00074-d24f01c720] “Insufficient: concrete 196/203 182/203 Insufficient: abstains 7/203 21/203 Insufficient: ref. hit 87/203 85/203”
- **The paired compact-CSV appropriateness effect was +3.16 percentage points with CI [0.00,6.57] for Qwen and +2.46 percentage points with [−1.84,6.94] for DeepSeek; neither lower endpoint was strictly positive.**
  - Context: The primary format comparison is inconclusive. It is conditional on questions certified in both arms and does not establish equivalence or an all-question effect.
  - Evidence: [b00072-aca250d387] “CSV minus raw appropriateness is +3.16 pp, CI [0.00,6.57], for Qwen and +2.46 pp, [−1.84,6.94], for DeepSeek.”; [b00072-aca250d387] “Neither lower endpoint is strictly positive. These inconclusive results do not establish equivalence.”
- **The low-effort LLM judge was jointly correct on 1,908/1,920 cases (99.38%) but falsely supported two concrete answers under decisive missing outcomes and produced two truncated outputs.**
  - Context: Aggregate evaluator accuracy concealed support-axis errors, so the judge did not pass the full prespecified reliability gate.
  - Evidence: [b00090-c0a085463c] “The low configuration is jointly correct on 1,908/1,920 cases (99.38%; history-clustered CI [98.91,99.74]).”; [b00090-c0a085463c] “It falsely treats two concrete answers under decisive missing outcomes as context-appropriate; two other outputs truncate.”
- **A cutoff-aware deterministic program was appropriate on all 307, 307, and 298 certified partial-arm cases using zero model calls; the extended evaluator program matched the hybrid’s observed 1,920/1,920 score.**
  - Context: The fixed executable grammar does not require an LLM, and the hybrid has no observed advantage over the strongest simple baseline. The solver shares rules with the certifier, so it is a consistency check rather than independent validation.
  - Evidence: [b00081-b6ccbf9789] “It is appropriate on all 307, 307, and 298 certified cases, using zero model calls.”; [b00091-530ac29211] “The extended program uses zero API calls and matches the hybrid’s observed 1,920/1,920 score.”

## Experimental evaluation

### Datasets

- Synthetic outcome-masking and unordered-packing development histories with controlled missing outcomes and multiple context budgets.
  - Evidence: [b00047-2775221ce9] “Masking and unordered packing use 40 exposed histories; the judge uses 120 reserved histories from that generator.”
- Chronological confirmation histories from an independent random stream, reused as fixed inputs for the second reader.
  - Evidence: [b00047-2775221ce9] “Qwen’s chronological study uses a new generator, 16 development histories, and 80 confirmation histories from an independent random stream.”; [b00047-2775221ce9] “DeepSeek reuses those 80 histories after Qwen’s results are observed.”
- Held-out constructed judge controls derived from reserved histories, with scalar and two-axis evidence candidates.
  - Evidence: [b00084-977a99b9e1] “The judge study uses the 120 reserved histories from the outcome-masking generator.”; [b00084-977a99b9e1] “It selects one query per history, balanced across the four operators, and constructs 16 candidates per selected query.”
- An exploratory natural-trajectory pilot excluded from controlled confirmation because it does not validate the executable certificates.
  - Evidence: [b00168-3127d82a2f] “It does not provide an external validation set for the executable evidence certificates.”

### Baselines

- END-only deterministic program that abstains on partial prefixes and executes queries on complete logs.
  - Evidence: [b00081-b6ccbf9789] “An END-only program abstains on every partial prefix and runs the executable query on full logs.”
- Cutoff-aware deterministic program using public cutoff and first-route conditions.
  - Evidence: [b00081-b6ccbf9789] “A cutoff-aware program also uses the public cutoff and first-route conditions.”
- Finite and extended evaluator programs, reference-only scoring, an LLM judge, and program-first hybrid routing.
  - Evidence: [b00086-1edfafb383] “We compare a finite program, an extended program supporting the declared extra format, reference-only scoring, the model judge, and a program-first hybrid.”

### Metrics

- Reference agreement against the executable complete-history answer.
  - Evidence: [b00041-d0f4366ea6] “Reference agreement is R=𝕀[a=y], even on insufficient contexts.”
- Certified context appropriateness, including reference hits and abstention behavior by evidence status.
  - Evidence: [b00043-2d5502fac4] “We report the certified denominator, reference hits on insufficient inputs, abstention on insufficient inputs, and incorrect abstention on sufficient inputs.”
- All-input appropriateness identification bounds accounting for unresolved inputs.
  - Evidence: [b00043-2d5502fac4] “This is an identification bound, not a confidence interval.”
- History-clustered percentile bootstrap intervals for paired contrasts.
  - Evidence: [b00057-f0a452e57b] “We resample whole histories with replacement, retaining all questions and paired conditions, for 10,000 bootstrap replicates.”

### Ablations

- Decisive versus irrelevant outcome masking with neutral padding.
  - Evidence: [b00062-ca7e3f3a41] “Two possible outcome assignments change the answer in the decisive arm; the irrelevant arm preserves a unique answer.”
- Raw, whole-record raw, and compact CSV prefixes under fixed context budgets, plus full-source controls.
  - Evidence: [b00052-f9f18f8ccc] “Raw-prefix and CSV-prefix policies truncate to a context-token budget and may cut a record.”; [b00052-f9f18f8ccc] “Whole-record raw prefixes stop before the next record would exceed that budget.”
- Second-reader replication changing only the model field in frozen request payloads.
  - Evidence: [b00054-7b9d40ea57] “DeepSeek’s replication changes only the model field of Qwen’s frozen request payloads, preserving messages, seed, and strict answer schema.”
- Paired judge configurations comparing low reasoning with a weaker configuration while also changing output limits.
  - Evidence: [b00085-7f88c22b16] “Thus the comparison changes both reasoning setting and output budget; it is not an isolated causal test of reasoning effort.”

### Negative results

- Neither hosted reader established a positive compact-CSV appropriateness effect under the prespecified criterion.
  - Evidence: [b00072-aca250d387] “Neither lower endpoint is strictly positive.”
- DeepSeek did not establish Qwen’s positive full-source CSV contrast.
  - Evidence: [b00079-b7b294b546] “Thus a positive full-source CSV contrast is not established in both configurations.”
- The LLM judge failed the full reliability gate despite high aggregate correctness.
  - Evidence: [b00090-c0a085463c] “The full prespecified reliability gate is not passed, despite the high aggregate score and zero false accepts on the separate scalar controls.”
- The exploratory natural-trajectory path does not validate architecture improvement or the main claims.
  - Evidence: [b00168-3127d82a2f] “The pilot neither estimates full AMA-Bench performance nor validates an architecture improvement.”


## Limitations

- External validity is narrow: short synthetic device histories, fixed English templates, and explicit semantics do not represent ambiguous natural conversations or long-horizon memory.
  - Evidence: [b00105-e3de34c15f] “The histories are short and synthetic.”; [b00105-e3de34c15f] “Our legal-world certificates do not resolve these issues, and these experiments do not measure long-horizon memory scaling.”
- Only two hosted reader configurations are tested; server weights cannot be pinned, temperature zero does not ensure determinism, and responses are sampled once.
  - Evidence: [b00106-a1a25d6d02] “Temperature zero does not ensure determinism, and server weights cannot be pinned.”; [b00106-a1a25d6d02] “Successful contents are sampled once; reader variability and model-family-wide failure rates are not estimated.”
- Certification is conservative and representation-dependent; the paired format estimate excludes unresolved cases and does not identify the all-question effect.
  - Evidence: [b00107-1423b4890a] “Coverage varies by representation.”; [b00107-1423b4890a] “The main paired estimate is conditional on certification in both arms and does not identify the effect on all questions.”
- The deterministic solver and certifier share rules, so agreement cannot detect a shared specification error.
  - Evidence: [b00107-1423b4890a] “Their agreement cannot exclude an error in the shared specification.”
- Interventions remain confounded: masking differs in duplicate multiplicity, while format comparisons jointly change syntax and token length.
  - Evidence: [b00108-78b35e0db1] “The masking arms differ in duplicate multiplicity for 47 queries. Format comparisons change syntax and token length together.”
- There is no independent human adjudication, and the confirmation cannot rule out small effects.
  - Evidence: [b00109-9c7d6fe075] “The chronological confirmation contains 80 histories and cannot rule out small effects.”; [b00109-9c7d6fe075] “No human answer or evidence adjudication was performed.”

## Reproducibility

**Status:** partial

The internal audit trail is unusually detailed and supports reconstruction of retained results, but independent reproduction is limited by the absent public artifact and non-pinnable hosted models. Program-generated components appear substantially reproducible once released; exact model-response replication remains weak.

**Available artifacts**

- Generation and scoring scripts, public prompts, ground-truth files, witnesses, request hashes, sanitized receipts, fee estimates, and offline replay checks are retained locally.
- Seeds, software versions, tokenizer hash, request counts, transport attempts, API usage, and cost accounting are documented.
- Network-disabled replay reportedly reproduces scored rows and the summary byte-for-byte.

**Missing pieces**

- The retained materials were not publicly released with the paper.
- Hosted model weight snapshots cannot be independently pinned.
- Some historical software versions were not recorded.
- A fresh hosted API run is not guaranteed to return identical contents.
- AMA-Bench source histories are excluded from the intended release.

## AIDB assessment

- Novelty: Moderate to high as an evaluation contribution. The paper does not claim the general sufficiency distinction, but operationalizes it with byte-identical compatible-world witnesses, public temporal certificates, conservative unresolved labels, and separate evaluator calibration.
- Usefulness: High for designing or auditing agent-memory and history-QA evaluations. The protocol exposes when reference accuracy conflates evidence access with unsupported answering and supplies strong deterministic baselines. Immediate applicability is greatest in executable or tightly specified domains.
- Confidence: high
- Recommended action: adopt
- Rationale: Adopt the separation of reference agreement, certified sufficiency, and context appropriateness, and require executable baselines where semantics permit. Treat the reported reader rates and format effects as bounded diagnostics rather than portable estimates. The careful negative results, replication, and validity boundaries make the paper decision-useful despite narrow external validity.

## Uncertainties

- **How often unsupported reference matches occur in deployed memory systems or natural conversational histories is unknown.** — The practical prevalence determines how urgently existing benchmarks and production evaluations need redesign.
  - Evidence: [b00095-a6fe21b123] “The evidence-sensitive contract fails in two hosted configurations, without estimating prevalence in deployed memory systems.”
- **The causal mechanism behind any CSV effect is unresolved.** — Packing changes several properties together, so the current comparison cannot reliably guide format engineering.
  - Evidence: [b00097-2882641a64] “Compaction changes record coverage, the cutoff frontier, partial-tail certifiability, and readability.”
- **Unclassified inputs may include further sufficient or insufficient cases that the conservative certifier cannot resolve.** — Representation-dependent certification changes the analysis population and limits interpretation of paired effects.
  - Evidence: [b00039-40cc0f4ac8] “These conditions are sufficient rather than necessary; a partial field can sometimes establish more than our parser certifies.”
- **Dependence on hosted-service drift and one-shot response sampling is unresolved.** — The replication strengthens the diagnosis across configurations but does not estimate within-model variability or stable family-wide rates.
  - Evidence: [b00106-a1a25d6d02] “reader variability and model-family-wide failure rates are not estimated.”

## Open questions

- Can same-context certificates be extended to natural trajectories with independently validated evidence labels and ambiguous language?
- How much do current memory benchmarks overstate capability when hidden-reference agreement is separated from visible-context support?
- Can certification coverage improve for partial records without assumptions unavailable to the reader?
- Which intervention—record coverage, syntax, tokenization, completeness markers, or instructions—actually changes context-appropriate behavior?
- Do repeated hosted runs, additional model families, and longer histories preserve the observed tendency to answer insufficient contexts?
- How should appropriateness be generalized when applications assign explicit utilities to abstention and different error types?

## Proposed AIDB experiments

- **Hypothesis:** Evidence-sensitive scoring will materially lower apparent performance relative to hidden-reference accuracy on independently sampled natural agent trajectories.
  - Baseline: The same systems scored only by complete-history reference agreement, plus a deterministic executable subset where tool semantics permit certification.
  - Primary metric: Paired difference between reference agreement and context appropriateness on independently human-adjudicated sufficient, insufficient, and unresolved cases.
  - Stop condition: Stop and withhold a prevalence claim if blinded adjudicators miss the prespecified agreement threshold or the certifiable subset cannot achieve the prespecified interval width.
- **Hypothesis:** With visible records and byte content fixed, CSV syntax alone will not improve context appropriateness; observed gains primarily arise from complete-record coverage.
  - Baseline: Raw serialization with the same records, completeness marker, partial-tail status, and model-native token budget.
  - Primary metric: History-clustered paired difference in certified context appropriateness between syntax-only conditions, with certification status fixed per question.
  - Stop condition: Stop when the interval satisfies a prespecified equivalence margin or when record and byte matching fails for any compared pair.
- **Hypothesis:** Explicit evidence-state prediction before answer generation will reduce concrete answers on insufficient contexts without materially increasing abstention on sufficient contexts.
  - Baseline: The paper’s direct-answer prompt with the same model, visible bytes, decoding configuration, and output budget.
  - Primary metric: Change in insufficient-context concrete-answer rate, jointly constrained by change in sufficient-context correct-answer rate.
  - Stop condition: Reject the intervention if the insufficient concrete-answer rate does not improve beyond the prespecified margin or sufficient correct answering breaches its non-inferiority margin.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:25:51.862855+00:00`
- Document SHA-256: `fbeb28b0ca6cca940f1f76b55d663b2c9648d876a156ffcaef043f1cdc6d5447`
- Metadata SHA-256: `4407d3978a1d94a3009a652822771dc0d23d51f8aa153fdcd02f92a9e4a35974`
- Blocks: 177
- Deterministic repair attempts: 0
