# Remember, Verify, or Ask? Evaluating Memory Decisions at Reuse Time

## Executive summary

The paper introduces MCB, a benchmark for deciding whether interaction-derived information should be persisted, used ephemerally, externally verified, or clarified with the user at reuse time. Its strongest evidence is an independently adjudicated held-out set plus controlled prompt and label-versus-tool comparisons. Prompting materially helps some models, but clarification remains difficult. Tool-selection behavior can diverge sharply from label decisions, although unmatched prompts prevent causal attribution to interface alone. The work is valuable as a diagnostic benchmark, not evidence that any memory backend or end-to-end agent is safe or useful.

## Problem

**Statement.** Given interaction history, a candidate memory update, and a later reuse context, determine whether the candidate warrants durable persistence, current-context use only, an external check, or clarification from the user.

**Why it matters.** A mistaken durable update can silently affect future behavior, while world facts, user intent, scope, and referents require different authorities. A memory system therefore needs a decision boundary before treating interaction-derived information as durable.

**Scope.** The study evaluates reuse-time action selection under a conservative policy. It does not evaluate candidate extraction, acquisition-time filtering, actual writes, external checks, user answers, retrieval, or downstream task utility.

## Method

MCB frames memory handling as four-way classification over persist, ephemeral, verify, and clarify. The primary benchmark is split into development and held-out portions; a rule-authored evidence-flip contrast set tests controlled sensitivity, and a small WildChat-derived extension provides a descriptive naturalistic check. Four checkpoints are evaluated with bare definitions, an archived policy prompt, few-shot examples, and a structured tool-selection condition. Held-out labels are independently audited, and analyses include action-level metrics, bootstrap intervals, exact paired tests, and exploratory class-recall comparisons.

### Key components

- Each scenario supplies acquisition context, a candidate update, and a visible later reuse context.
- The four actions distinguish durable commitment, local use, world-authoritative verification, and user-authoritative clarification.
- Two non-authors label the held-out primary and contrast sets independently; a blind third annotator resolves disagreements.
- MCB-Act replaces labels with one structured call among memory_write, use_now, check_source, and ask_user.
- Prompt conditions comprise bare definitions, the original five-rule policy, and four development demonstrations.
- The evidence-flip extension changes evidence within paired, rule-authored scenarios; the naturalistic extension uses screened public user turns and a standardized later context.

### Assumptions

- The annotation policy intentionally prefers weaker commitment when persistence remains uncertain.
- Reuse context is known when the model decides; findings do not transfer automatically to acquisition-time gating.
- User intent, preferences, and referents are user-authoritative, whereas changing facts, versions, and schedules are externally authoritative.
- The benchmark labels operationalize a stated conservative policy, not universal ground truth.
- Bootstrap intervals characterize uncertainty over evaluated items, not repeated stochastic model sampling.

## Main claims

- **MCB evaluates a four-way reuse-time commitment decision rather than retrieval or storage execution.**
  - Evidence: [b00006-da941a33c0] “an agent selects one of four actions: persist, ephemeral use, verify against an external source, or clarify with the user.”; [b00024-82a88aaa82] “MCB records action selection; storage writes, source checks, user answers, and backend-specific transitions are not executed.”
- **The held-out annotations have substantial independent auditing rather than relying only on author labels.**
  - Evidence: [b00055-90942348b6] “Two non-authors independently labeled the 70 held-out primary and 70 contrast items while blinded to author labels, categories, rationales, model outputs, and each other.”; [b00055-90942348b6] “Agreement across all 140 items was 0.971 (κ=0.962)”; [b00055-90942348b6] “Majority adjudication changed eight primary labels and no contrast labels.”
- **The benchmark separates uncertainty requiring a world source from uncertainty requiring the user.**
  - Evidence: [b00006-da941a33c0] “An external source establishes changing world facts, while the user establishes intent, scope, and ambiguous reference.”
- **The released artifact is intended to make the reported analyses auditable from frozen inputs and outputs.**
  - Evidence: [b00142-1a3c489900] “supplies the benchmark and executable reproduction code.”; [b00143-3ff3961575] “Model access is not needed.”; [b00143-3ff3961575] “This validates the frozen data and regenerates the primary baselines, class metrics, recall comparisons, and descriptive naturalistic analysis.”

## Results

- **Verification recall exceeded clarification recall in every original label condition, but only three exploratory comparisons survived multiplicity correction, and none involved Claude.**
  - Context: This supports a recurring pattern on the authored held-out set, not a general model property: class content and difficulty differ, and the tests were added after review.
  - Evidence: [b00080-874e6a8997] “Verification recall exceeds clarification recall in all 12 original label conditions”; [b00080-874e6a8997] “only Qwen bare (pH=.004), Qwen policy (pH<.001), and Gemma policy (pH=.012) remain significant.”; [b00080-874e6a8997] “No Claude comparison passes this correction.”
- **Prompt effects were model-dependent: Haiku policy improved accuracy by +.229 and Qwen few-shot by +.214, with corrected p-values of .003 and .002; several other apparent gains were not significant.**
  - Context: The archived policy is incomplete relative to the annotation guide, so these comparisons do not test a fully aligned policy.
  - Evidence: [b00086-bbae96ae29] “Haiku policy is significant relative to bare (Δ=+.229, Holm-adjusted pH=.003)”; [b00086-bbae96ae29] “Qwen few-shot remains significant (Δ=+.214, pH=.002).”; [b00086-bbae96ae29] “Gemma’s policy and few-shot gains, +.100 and +.086, are also not significant (pH=.898 for each).”
- **Label and tool-selection settings produced large behavioral shifts: agreement ranged from .229 to .571, while Sonnet, Qwen, and Gemma accuracy fell significantly in the tool condition.**
  - Context: The comparison is consequential but confounded because role framing, wording, and policy content differ across modes; it cannot isolate output format.
  - Evidence: [b00092-67fe0d56b5] “Haiku −.114 [−.214,−.014] .057 .571 Sonnet −.286 [−.414,−.143] <.001 .571”; [b00092-67fe0d56b5] “Qwen −.214 [−.386,−.029] .047 .229 Gemma −.471 [−.614,−.329] <.001 .243”; [b00063-00005a985f] “this comparison does not isolate output format as a causal factor.”
- **Gemma’s tool-selection run exposed a severe persistence failure: it selected memory_write 41 times, never selected ask_user, lost .471 accuracy, and reached .486 erroneous persistence.**
  - Context: All calls passed minimum structural checks, showing that syntactically valid tool output is not evidence of correct operation choice.
  - Evidence: [b00090-051199b83d] “it calls memory_write 41 times, use_now 28 times, check_source once, and ask_user zero times.”; [b00090-051199b83d] “Its accuracy falls by .471 (pH<.001), OM rises to .486”; [b00090-051199b83d] “Valid syntax and minimum argument checks do not establish correct operation choice.”
- **The naturalistic check did not provide external validation: no evaluated local condition exceeded the .583 majority-ephemeral accuracy, and every one of the 16 local conditions missed both clarification cases.**
  - Context: The extension is small, class-imbalanced, uses a standardized counterfactual reuse context, excludes Claude, and reports descriptive results only.
  - Evidence: [b00096-b6154db877] “The majority-ephemeral reference reaches .583 accuracy but only .184 macro-F1. No local condition exceeds its accuracy.”; [b00097-d45efcb09a] “Only two items require clarification. All 16 local conditions miss both.”; [b00097-d45efcb09a] “Even 0/2 has a 95% Wilson interval of approximately [0,.658].”

## Experimental evaluation

### Datasets

- MCB primary benchmark: authored English scenarios, deterministically split into development and held-out sets within category.
  - Evidence: [b00054-1215e26c35] “The 140 primary items are deterministically split 70/70 by sorted identifier within category.”
- Evidence-flip contrast extension: paired, rule-authored scenarios used only for controlled sensitivity analysis.
  - Evidence: [b00054-1215e26c35] “A separate 70-item contrast extension contains 35 evidence-flip pairs and is used only as a controlled sensitivity analysis.”
- Naturalistic extension: screened English user turns from a frozen WildChat revision, producing an independently adjudicated descriptive set rather than a longitudinal memory log.
  - Evidence: [b00059-feafa1b9b5] “Forty English user turns pass automated privacy/safety screens and a pre-annotation quality review.”; [b00060-d34ef84e71] “Majority vote excludes four unsupported candidates and retains 36”; [b00059-feafa1b9b5] “this is a source-grounded naturalistic check, not a longitudinal memory log.”

### Baselines

- Always-Persist reference.
  - Evidence: [b00072-e10d18fa9f] “Reference systems are Always-Persist, a fixed temporal/scope keyword heuristic, Majority Action, and a category-majority oracle.”
- Fixed temporal/scope keyword heuristic receiving the same scenario text as models.
  - Evidence: [b00072-e10d18fa9f] “The fixed keyword rules receive the same scenario text as models and do not inspect test labels.”
- Majority Action distribution diagnostic.
  - Evidence: [b00072-e10d18fa9f] “Majority Action uses the evaluated split’s most frequent gold action”
- Category-majority oracle using hidden category identities and test labels; explicitly not a deployable or fair competitor.
  - Evidence: [b00072-e10d18fa9f] “the oracle uses both test gold labels and category IDs hidden from models.”; [b00075-0f95569f1e] “prevents interpreting it as a fair trained competitor.”

### Metrics

- Accuracy, per-action precision, recall, F1, and macro-F1.
  - Evidence: [b00066-4b2c9d954e] “Accuracy measures the proportion of correct decisions.”; [b00066-4b2c9d954e] “F1 combines precision and recall, and macro-F1 weights all four actions equally.”
- Over-memory measures erroneous persistence over all items; under-memory measures missed gold-persist cases, with different denominators.
  - Evidence: [b00066-4b2c9d954e] “Over-memory (OM) is erroneous persistence divided by all items.”; [b00066-4b2c9d954e] “Under-memory (UM) is the proportion of gold-persist items missed”
- Uncertainty and paired inference use bootstrap intervals, exact two-sided McNemar tests, and Holm correction; verify-versus-clarify recall uses exploratory two-sided Fisher tests.
  - Evidence: [b00067-5def1ab8f5] “2,000 bootstrap resamples quantify uncertainty due to the evaluated items.”; [b00067-5def1ab8f5] “Exact two-sided McNemar tests count items on which one run alone is correct.”; [b00068-d5f671127c] “a two-sided Fisher test compares correct/incorrect counts on 18 verify and 12 clarify items.”

### Ablations

- Bare definitions versus the original policy prompt versus four-shot prompting.
  - Evidence: [b00062-09a7483129] “Bare provides definitions only; policy adds the original five rules; few-shot adds four development examples.”
- Bare label output versus structured tool selection.
  - Evidence: [b00089-30b19cfdba] “Table 7 compares each bare label run to its tool-selection run.”
- Controlled Qwen evaluation combining primary and evidence-flip items.
  - Evidence: [b00094-4f290b24d8] “On the combined 140 Qwen items, bare, policy, and few-shot accuracy is .614, .757, and .843.”

### Negative results

- The corrected recall comparison yields no significant Claude verification-versus-clarification difference.
  - Evidence: [b00080-874e6a8997] “No Claude comparison passes this correction.”
- Several prompt gains do not survive correction.
  - Evidence: [b00086-bbae96ae29] “Haiku’s few-shot gain is not significant after correction (pH=.070).”; [b00086-bbae96ae29] “Gemma’s policy and few-shot gains, +.100 and +.086, are also not significant (pH=.898 for each).”
- Policy-associated reductions in erroneous persistence for Qwen and Gemma are not significant after the expanded correction.
  - Evidence: [b00087-099585079d] “these changes are not significant (pH=.051 and .273).”
- The naturalistic extension supplies no condition beating the majority-ephemeral accuracy and no successful clarification decision.
  - Evidence: [b00096-b6154db877] “No local condition exceeds its accuracy.”; [b00097-d45efcb09a] “All 16 local conditions miss both.”


## Limitations

- The primary evidence comes from a small authored English set with unequal action counts and strong category/action structure, limiting generalization and making class-recall comparisons vulnerable to content and difficulty differences.
  - Evidence: [b00108-9858668e25] “The primary test has 70 authored English items, including 12 clarify and 18 verify cases”; [b00108-9858668e25] “The category oracle’s .800 accuracy reveals strong category/action structure.”; [b00108-9858668e25] “Class content and difficulty differ”
- The original policy omits important clarification rules, while label and tool prompts differ beyond output format; therefore neither full-policy effectiveness nor a causal interface effect is established.
  - Evidence: [b00109-d478ffe239] “The original policy omits conflict, second-hand preference, and expired-scope clarification rules”; [b00109-d478ffe239] “no act-plus-policy comparison isolates these factors.”
- The naturalistic extension is too small and imbalanced for stable clarification estimates, excludes Claude, and is not a longitudinal deployment study.
  - Evidence: [b00110-4d1a62ceaf] “The naturalistic extension has 36 items, only two requiring clarification, and no Claude evaluation.”; [b00110-4d1a62ceaf] “It is neither a longitudinal deployment study nor a statistically stable clarification evaluation.”
- Only one serving configuration per checkpoint and one quantized local-model version are tested, so robustness across sampling, serving systems, quantization, and scale is unknown.
  - Evidence: [b00111-cc89b8cfa9] “We use one serving configuration per checkpoint and one quantized version per local model.”; [b00111-cc89b8cfa9] “comparisons with dense models do not isolate scale.”
- The benchmark stops at decision selection and does not measure memory writes, verification, dialogue resolution, retrieval, task utility, or the costs induced by conservative intervention.
  - Evidence: [b00111-cc89b8cfa9] “without extracting candidates, executing writes or checks, obtaining user answers, or measuring retrieval and task utility.”; [b00025-7a2945ab78] “We do not measure these costs or establish that the preference is optimal.”
- The naturalistic data retain residual privacy risk, and real verification or clarification can create disclosure and user-burden costs absent from benchmark scores.
  - Evidence: [b00113-d584604401] “automated de-identification cannot guarantee zero residual privacy risk.”; [b00113-d584604401] “a clarification policy can burden users, and a verification policy can expose sensitive queries to external services.”

## Reproducibility

**Status:** strong

Reproducibility of the frozen numerical analyses is strong: the archive reportedly contains data, annotations, prompts, predictions, metadata, tests, and a script that regenerates the analyses without model access. Reproduction of live model behavior and extensions beyond the archived prompts is only partial because there is no claimed public repository, the aligned policy is unevaluated, and backend execution is outside scope.

**Available artifacts**

- Supplementary archive named NORA2026_camera_ready_supplement.zip.
- All primary, contrast, and adjudicated naturalistic items.
- Frozen non-author annotation decisions and annotator packets.
- Archived prompts and checkpoint metadata.
- Item-level predictions, raw outputs, parsed actions, and tests.
- Executable reproduction script reproduce_camera_ready.py.
- Complete guide-aligned policy implementation in src/aligned_policy.py, explicitly unevaluated.

**Missing pieces**

- No public repository URL is claimed in the paper.
- Fresh model inference for hosted checkpoints may depend on external access and serving behavior.
- The complete guide-aligned label and tool policies have no reported runs.
- No repeated-seed or repeated-serving robustness study is reported.
- No executable end-to-end memory backend, source-check, or user-clarification evaluation is reported.

## AIDB assessment

- Novelty: The paper’s distinctive contribution is a four-action decision boundary that separates durable persistence, ephemeral use, externally authoritative verification, and user-authoritative clarification, then tests both labels and structured memory operations. The independently adjudicated evidence-flip and naturalistic extensions strengthen the benchmark design, although the core scenarios remain authored and structurally predictable.
- Usefulness: Useful as an auditable diagnostic suite for memory-gate policies and especially for detecting erroneous persistence or label/tool inconsistencies. It should not be treated as a deployment-readiness test because it does not execute memory systems, measure downstream utility, or establish privacy and interaction costs.
- Confidence: high
- Recommended action: read
- Rationale: The benchmark targets a practically important, under-measured failure boundary and reports unusually candid negative results and validity constraints. The frozen artifact appears suitable for replication and internal policy testing. Adoption as a definitive benchmark should wait for matched label/tool prompts, evaluation of the complete policy, larger naturalistic clarification samples, and end-to-end outcome measurements.

## Uncertainties

- **Whether the verification-over-clarification pattern persists on larger, independently sourced, difficulty-matched data.** — The central behavioral pattern may reflect class composition, authored templates, or prompt coverage rather than a stable model tendency.
  - Evidence: [b00068-d5f671127c] “Class difficulty and prompt construction differ”; [b00080-874e6a8997] “it does not establish a general cross-model tendency to prefer verification.”
- **Whether tool-selection degradation is caused by output interface, missing policy rules, tool semantics, or role framing.** — Without isolating the causal factor, the results cannot prescribe whether systems should change interfaces, prompts, or training.
  - Evidence: [b00063-00005a985f] “Its role framing and wording also differ from label mode”; [b00109-d478ffe239] “no act-plus-policy comparison isolates these factors.”
- **Whether improved benchmark decisions produce safer or more useful downstream memory behavior.** — A classification gain may not reduce harmful writes, improve retrieval, or help users once checks, questions, and storage transitions are executed.
  - Evidence: [b00102-bcca8c669a] “We have not compared those implementations or tested the effects on retrieval and downstream utility.”
- **Whether the conservative preference for weaker commitment has acceptable application-specific costs.** — Unnecessary questions and external checks can burden users, delay tasks, or disclose sensitive information.
  - Evidence: [b00025-7a2945ab78] “This is an assumed cost preference”; [b00113-d584604401] “a clarification policy can burden users”

## Open questions

- How do fully guide-aligned label and tool prompts compare when decision rules, examples, wording, and role framing are matched?
- Does the verification-versus-clarification gap survive on larger naturalistic samples with balanced actions and matched item difficulty?
- How should application-specific costs of erroneous persistence, missed persistence, unnecessary questions, and external verification be calibrated?
- Do MCB improvements translate into fewer harmful writes and better downstream retrieval or task outcomes in real memory backends?
- How robust are the findings across repeated serving, decoding settings, quantization levels, languages, domains, and model families?

## Proposed AIDB experiments

- **Hypothesis:** With identical complete decision rules, examples, and role framing, label and tool outputs will show substantially higher agreement than the archived unmatched settings without increasing erroneous persistence.
  - Baseline: For each checkpoint, compare the archived bare-label and original tool runs against matched complete-policy label and act-plus-policy runs on the same adjudicated primary and contrast items.
  - Primary metric: Paired label–tool agreement, with accuracy and over-memory as co-reported safety metrics.
  - Stop condition: Stop after all preregistered checkpoints complete deterministic parsing and paired tests; reject the hypothesis if agreement does not improve or if over-memory worsens under the matched tool condition.
- **Hypothesis:** Verification recall will no longer consistently exceed clarification recall after balancing classes and matching scenario difficulty, authority cues, lexical traps, and ambiguity strength.
  - Baseline: The original held-out verify and clarify subsets, evaluated with the same checkpoints and a fully guide-aligned prompt.
  - Primary metric: Within-model difference between verify recall and clarify recall, with multiplicity-corrected paired or stratified inference on a newly adjudicated balanced set.
  - Stop condition: Stop at the preregistered sample size or earlier only for annotation-quality failure; reject the hypothesis if the corrected recall gap remains consistently positive across model families.
- **Hypothesis:** A reuse-time gate using the complete policy reduces harmful durable writes while preserving downstream task utility compared with unconditional persistence and the archived policy.
  - Baseline: Always-Persist, the archived policy gate, and a matched complete-policy gate connected to the same memory backend and retrieval pipeline.
  - Primary metric: Rate of harmful durable updates measured on subsequent tasks, jointly reported with downstream task success and user-intervention burden.
  - Stop condition: Stop after the preregistered longitudinal task set; reject the hypothesis if harmful writes do not decrease, or if task success or intervention burden crosses predefined non-inferiority limits.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:27:23.949279+00:00`
- Document SHA-256: `9d98294df5a3b3aeb3bd8e9128c562df03527e495dd743feec6b09d647e8e044`
- Metadata SHA-256: `16eb4e17e69b3407959f3d14d77437439dd8c7f401f5715364d2469eeeb3c4f5`
- Blocks: 166
- Deterministic repair attempts: 0
