# Prune the Summary, Not the History: Source-Judged Compaction for Long-Horizon Agents

## Executive summary

Structured summaries mix environment-grounded observations with plans and interpretations authored by the compressor, yet downstream agents receive both as memory. Source-Judged Compaction (SJC) addresses this with a training-free post-processing gate: retrieve evidence, score each summary entry’s provenance using Jev, and delete unsupported entries without rewriting retained content. Across AppWorld and OfficeBench with two agent/compressor models, SJC consistently improves cross-run reliability relative to the host prompting compressor, while accuracy is less uniform. The strongest comparison freezes agent policy and interface and changes only context representation. Crucially, provenance is not correctness: a sourced but wrong conclusion can survive, and a useful unsupported plan can be deleted. Limited supported-entry recall and evaluation of only one compressor, short windows, and single-instruction tasks make this a replication candidate, not a general reliability guarantee.

## Problem

**Statement.** Recurrent compaction turns a generated summary into persistent working memory. Because compaction prompts request decisions and future work as well as observations, the checkpoint may contain compressor-generated reasoning that has no source in environment outputs. After older history is replaced, the agent cannot distinguish that reasoning from established state and may execute it as fact.

**Why it matters.** The failure mode affects execution rather than merely summary fidelity: an unsupported or contradicted entry can redirect later actions, and the same kind of unsupported reasoning is regenerated at successive boundaries. A remedy must therefore operate at every compaction event while preserving compatibility with fixed or API-only agents and compressors.

**Scope.** The paper studies structured natural-language checkpoints produced by an unchanged host compressor. Its operator may only delete complete entries, not add or rewrite them. Empirical scope is AppWorld and OfficeBench, two agent/compressor models, one OpenClaw-derived host compressor, and deliberately small context windows that force within-task compaction.

## Method

At each compression boundary, the host compressor first generates its ordinary structured checkpoint. SJC parses the checkpoint into entries while retaining section headings. For each entry, BM25 retrieves passages from environment outputs in the compressed span and retained interaction; passages are expanded and pooled. Jev-1.13 receives all entries, the pooled evidence, the task instruction, retained interaction, and previous committed summary, and returns a probability that each entry contains information originating in an environment output or previous summary. Entries meeting a fixed source-score threshold are rendered unchanged into the committed checkpoint; other entries are deleted. The filtered checkpoint becomes both the agent’s context and the prior summary at the next boundary.

### Key components

- A structured-summary parser that treats each bullet under the host compressor’s section headings as one removable unit.
- Per-entry BM25 retrieval over environment outputs, followed by pooling of the retrieved passages into a compact judge evidence set.
- Jev-1.13 as a non-generative probabilistic source judge, invoked once per compaction in the normal case.
- A fixed provenance threshold that retains or removes complete entries without modifying retained text.
- Recurrent application at every boundary, so newly generated unsupported reasoning is filtered before becoming persistent memory.

### Assumptions

- Environment outputs and the previous committed checkpoint are treated as admissible sources; the fixed task prompt is context for judging but is deliberately not counted as a source.
- The task instruction remains visible after compaction, making it acceptable in the evaluated single-instruction setting to delete entries that only restate or interpret it.
- Structured summaries can be reliably decomposed into independently removable entries without destroying essential relationships between entries.
- Evidence retrieval exposes enough relevant environment material for the source judge to make useful provenance decisions.
- Removing unsupported content improves execution often enough to outweigh deletion of correct or helpful unsupported reasoning.

## Main claims

- **Compaction summaries are not neutral records: commonly used prompts explicitly request decisions and plans, and substantial portions of forward-looking sections lack an environment or prior-summary source.**
  - Evidence: [b00028-313a551b03] “Of these, 21 ask the compressor for decisions or next steps: 18 request the decisions made and 17 request the remaining work”; [b00029-0ca01ef832] “67.7% of open TODOs and 86.1% of pending user asks have no source.”
- **Unsupported reasoning is produced repeatedly rather than merely propagated from an earlier checkpoint, motivating a gate at every compaction boundary.**
  - Evidence: [b00030-3d72c70e1d] “only 20.5% of unsupported reasoning entries reappear in the following summary, and 5.3% three summaries later.”; [b00030-3d72c70e1d] “The compressor writes unsupported reasoning anew at each boundary, so removing it once is not enough.”
- **SJC is a training-free, drop-in deletion layer: it leaves the agent and host compressor unchanged, preserves retained entries verbatim, and adds a source-judgment request rather than another summary-generation call.**
  - Evidence: [b00008-f671ffddd9] “Entries without such a source are removed as complete units, while retained entries remain identical to the compressor’s output.”; [b00008-f671ffddd9] “SJC requires no modification to the agent, the compressor prompt, or the runtime, and adds no summary-generation call.”; [b00049-0e1d303f77] “SJC thus adds one judge request per boundary, however many entries there are.”
- **The paper’s controlled protocol attempts to isolate context representation as the manipulated variable while keeping the downstream agent configuration and environment fixed.**
  - Evidence: [b00169-97758edc37] “Only the context representation supplied to the agent changes.”; [b00170-5b2115fa26] “Replacement contexts are inserted at the same continuation point”; [b00171-ac8ed2eaf5] “we freeze all prompt templates before evaluation and record hashes of the rendered prompts used in each run.”

## Results

- **In the failure attribution study, 29 of 35 analyzed failed runs executed a specific summary entry; among those entries, 22 were unsupported, 3 contradicted an environment output, and only 4 were supported.**
  - Context: This is the paper’s strongest mechanistic evidence, but it is observational attribution on the AppWorld training split rather than a randomized intervention. The authors excluded a scenario whose reference solution was inconsistent with its environment data, and they warn that per-run observations are clustered by scenario.
  - Evidence: [b00036-a7d2f8bdef] “In 29 of the 35 failed runs, the failing action carries out a specific summary entry;”; [b00036-a7d2f8bdef] “22 of these entries are supported by no output and 3 contradict one; only 4 are supported.”; [b00163-8b6c74441c] “a single scenario accounts for 9 of them, so per-run counts are not independent”
- **Relative to Prompting, SJC increased Pass3 in all four benchmark–model settings: by 8.9% and 7.1% on AppWorld and by 5.3% and 2.1% on OfficeBench. Accuracy improved by 1.1%–5.3% in three settings but declined by 1.0% in the remaining setting.**
  - Context: Pass3 is the fraction of tasks solved in all three independent runs and is the primary evidence for improved cross-run reliability. Reported differences are absolute. The accuracy decline shows that better all-run consistency does not guarantee a higher mean success rate.
  - Evidence: [b00076-4d5acbb372] “Pass3 rises over Prompting by 8.9% and 7.1% on AppWorld (GPT-5.6 Luna and MiniMax-M3) and by 5.3% and 2.1% on OfficeBench.”; [b00076-4d5acbb372] “Accuracy rises by 1.1%–5.3% in three settings; on OfficeBench with MiniMax-M3 it falls by 1.0%.”
- **The largest reported subset gain occurs on difficult or multi-application work: on OfficeBench 3-APP tasks with GPT-5.6 Luna, Pass3 rises from 41.9% to 54.8% and accuracy from 59.1% to 64.5%. Across twelve subset groups, Pass3 improves in ten, is unchanged in one, and decreases in one.**
  - Context: This pattern supports the stated hypothesis that provenance filtering matters most where compaction causes greater degradation, but subset multiplicity and only three runs limit certainty about the stability of each subgroup difference.
  - Evidence: [b00077-20a78366cc] “On OfficeBench 3-APP tasks with GPT-5.6 Luna, Pass3 rises from 41.9% to 54.8% and accuracy from 59.1% to 64.5%.”; [b00077-20a78366cc] “Across the twelve benchmark–model–subset groups, Pass3 improves in ten, is unchanged in one, and decreases in one”
- **SJC reduced cumulative agent-and-compressor tokens relative to Prompting by −8.0% and −2.9% on AppWorld and by −1.3% and −7.0% on OfficeBench; pruning removed 13%–21% of entries and shortened summaries by 14%–27%.**
  - Context: These counts exclude Jev calls from cumulative LLM tokens. The separate judge cost is reported as below $0.002 per task, so the efficiency claim is best interpreted as no increase in agent/compressor token use plus a small external judging charge.
  - Evidence: [b00081-86f92ccab1] “Cumulative agent and compressor tokens change by −8.0% and −2.9% on AppWorld and by −1.3% and −7.0% on OfficeBench relative to Prompting.”; [b00081-86f92ccab1] “pruning removes 13%–21% of entries and shortens each summary by 14%–27%.”; [b00080-2b4be4716b] “its judge costs under $0.002 per task”
- **The source judge distinguishes annotated provenance with AUROC 0.905, but at the operating threshold it recovers only 64.2% of supported entries. Provenance itself is nearly unrelated to correctness: 92.2% of supported and 90.6% of unsupported entries are correct, with correctness-ranking AUROC 0.444.**
  - Context: This is a consequential qualification, not merely a judge benchmark. SJC deliberately targets source attribution rather than truth or utility, so it can retain sourced errors and delete correct, useful plans.
  - Evidence: [b00026-067e96d788] “Jev separates the two with an AUROC of 0.905”; [b00198-9ae878aae9] “it recovers 64.2% of all supported entries.”; [b00198-9ae878aae9] “92.2% of supported and 90.6% of unsupported entries are correct”; [b00198-9ae878aae9] “AUROC 0.444”

## Experimental evaluation

### Datasets

- AppWorld: stateful API-use tasks across simulated applications and users; experiments use the 168-task test-normal split. The summary-composition and failure analyses separately use the training split.
  - Evidence: [b00065-efe5b6bc0a] “AppWorld (Trivedi et al., 2024) contains stateful API-use tasks across simulated applications and users; we use its 168-task test-normal split.”; [b00026-067e96d788] “on the training split of AppWorld (Trivedi et al., 2024) (90 tasks, three runs, GPT-5.6 Luna).”
- OfficeBench: multi-application document, spreadsheet, and email workflows; the selected test set contains 95 tasks divided into single-, two-, and three-application groups.
  - Evidence: [b00065-efe5b6bc0a] “OfficeBench covers multi-application office workflows involving documents, spreadsheets, and email”; [b00195-e8e3fd495c] “95 tasks: 42 single-application, 22 two-application, and 31 three-application tasks.”

### Baselines

- No Compression, a full-history reference used for behavior preservation and token-cost comparison.
  - Evidence: [b00173-20be7dd5a5] “The agent receives the complete, uncompressed interaction history.”
- FIFO, a recency-based sliding window that discards complete oldest turns until the budget is met.
  - Evidence: [b00176-f211596af2] “complete turns are discarded from the front, oldest first, until the history fits.”
- LLMLingua and LLMLingua-2, task-agnostic token-pruning baselines using learned importance or token classification.
  - Evidence: [b00071-3afa2c7105] “LLMLingua (Jiang et al., 2023) and (3) LLMLingua-2 (Pan et al., 2024) perform token-level pruning using learned importance models”
- Fast-Jev, which uses the same judge family to select raw tool interactions rather than post-process a natural-language summary.
  - Evidence: [b00071-3afa2c7105] “Fast-Jev (Tran, 2026) uses Jev to select raw tool calls and outputs for retention, without producing a summary”
- Prompting, the original OpenClaw structured compaction prompt and direct host baseline for Prompting + SJC.
  - Evidence: [b00071-3afa2c7105] “Prompting uses the original OpenClaw structured compaction prompt”; [b00071-3afa2c7105] “Prompting + SJC, uses the same Jev model to prune unsupported entries from the summaries produced by Prompting.”

### Metrics

- Acc.: mean task success rate over three independent runs.
  - Evidence: [b00067-0766d23be4] “Acc. denotes the mean task success rate”
- Pass3: fraction of tasks solved in all three runs, intended to measure cross-run reliability.
  - Evidence: [b00067-0766d23be4] “Pass3 denotes the fraction of tasks solved in all three runs and measures cross-run reliability.”
- Efficiency measures: mean interaction steps, peak input length in thousands of tokens, cumulative agent/compressor tokens, and separately reported Jev API cost.
  - Evidence: [b00067-0766d23be4] “We also report the mean number of interaction Steps and the peak input length (Peak), measured in thousands of tokens.”; [b00067-0766d23be4] “we report cumulative agent and compressor tokens, including all inputs and outputs, and report the API cost of Jev separately.”

### Ablations

- Judge substitution: replacing Jev with the compressor as a binary self-judge wins on one setting but falls below Prompting in the other three; repeatability testing favors Jev.
  - Evidence: [b00092-97a1b01cc0] “Replacing Jev with the compressor itself gives the best Pass3 on AppWorld with GPT-5.6 Luna but falls below Prompting in the other three settings”; [b00092-97a1b01cc0] “the self-judge changes its answer on 8.6% of entries and Jev on 2.1%.”
- Threshold sensitivity: source scores are reported as bimodal, and changing the retention threshold across the tested interval has limited effect on the pruned fraction.
  - Evidence: [b00090-f5f59bb448] “Moving τ from 0.3 to 0.7 therefore changes the pruned fraction by at most 10.2% in any setting.”; [b00090-f5f59bb448] “We use τ=0.5 throughout.”
- Raw-history placement control: Fast-Jev uses the same judge but underperforms Prompting in most settings, suggesting that the judgment question and placement at summary-entry level matter.
  - Evidence: [b00075-e84f8227a4] “Fast-Jev uses the same judge model to select raw history and falls below Prompting in three of four settings”

### Negative results

- Mean accuracy declines in the OfficeBench/MiniMax-M3 setting even though Pass3 improves.
  - Evidence: [b00076-4d5acbb372] “on OfficeBench with MiniMax-M3 it falls by 1.0%.”
- One OfficeBench subset shows lower Pass3 after SJC.
  - Evidence: [b00077-20a78366cc] “decreases in one (OfficeBench 1-APP with MiniMax-M3, 90.5% to 88.1%)”
- Using the compressor as the source judge is unreliable across settings rather than a generally adequate replacement for Jev.
  - Evidence: [b00092-97a1b01cc0] “falls below Prompting in the other three settings”
- Compaction is not always cheaper than full history: one AppWorld configuration uses more tokens because it adds interaction steps.
  - Evidence: [b00083-860e59f8e9] “On AppWorld with GPT-5.6 Luna it uses 6.9% more, because compaction adds 5.8 steps per task”
- The case study does not establish deterministic causation: the same unsupported entry appears in a successful Prompting run.
  - Evidence: [b00097-88174580bb] “the third Prompting run carries the same entry and still succeeds.”


## Limitations

- Provenance filtering is not correctness checking. A sourced entry can draw a wrong conclusion and survive, while a correct or useful compressor-generated plan can be removed.
  - Evidence: [b00105-0be7fe0536] “SJC filters by provenance, not correctness, and the two are largely independent”; [b00105-0be7fe0536] “An entry that cites a real observation but draws a wrong conclusion from it has a source and is kept”; [b00105-0be7fe0536] “Conversely, SJC removes entries that are correct and sometimes entries that help.”
- The operating threshold has low recall for supported entries, creating a material risk of deleting valid state. The paper documents a model-dependent task failure caused by such pruning.
  - Evidence: [b00105-0be7fe0536] “At our threshold the judge errs toward pruning and recovers 64.2% of supported entries.”; [b00105-0be7fe0536] “MiniMax-M3 does not and fails in two of three runs.”
- External validity is narrow: only two benchmarks, two agent models, one host compressor, and artificially small compaction windows are evaluated.
  - Evidence: [b00106-28c32865d2] “Our evaluation covers two benchmarks, two agent models, and one host compressor, with compaction triggered at small context windows”
- The evaluated tasks keep one instruction visible. Multi-turn conversations, where earlier user messages must themselves be recognized as sources, are not tested.
  - Evidence: [b00106-28c32865d2] “In multi-turn settings, earlier user messages are themselves a source and would need to be treated as one; we have not evaluated that case.”
- SJC depends on a proprietary external API judge whose outputs are not fully deterministic, constraining portability and exact replication.
  - Evidence: [b00106-28c32865d2] “SJC also depends on an external judge model accessed through an API, whose scores are not fully deterministic”
- Failure attribution relies on LLM annotators and author adjudication; despite strong reported agreement, it is not independent human annotation.
  - Evidence: [b00106-28c32865d2] “the failure analysis in Section 3 relies on annotations produced by LLM annotators under a written protocol.”; [b00162-a09dcdf9a5] “The authors resolved the 14 runs with any disagreement.”

## Reproducibility

**Status:** partial

Reproducibility is partial. The methodological description is unusually concrete and the paper points to code, fixed upstream commits, and explicit judge/retrieval settings. However, the decisive judge and both agent models are API services, run-to-run sampling is intentional, and essential raw outputs and exact execution manifests are not established in the supplied material. Independent replication should therefore be feasible in design but may not reproduce exact task outcomes or costs.

**Available artifacts**

- The metadata states that code is available at https://github.com/GuanghuiMin/sjc.
- The paper specifies agent/compressor models, APIs, reasoning effort, output and step limits, context windows, compression scope, retrieval passage/chunk settings, evidence pooling, judge version, source question, threshold, and fallback behavior.
- The OpenClaw safeguard baseline is tied to a specific commit, and the LLMLingua implementation is tied to a release and commit.
- The evaluation uses three independent sampled runs per configuration and reports dataset splits and task counts.

**Missing pieces**

- No archived artifact or immutable release identifier is supplied for the SJC repository itself.
- No exact model snapshots, API seeds, decoding parameters beyond reasoning effort, or complete environment version manifest are present in the supplied blocks.
- The external Jev API is nondeterministic, and no local judge weights or replayable response cache are stated.
- The supplied blocks do not provide raw trajectories, per-task outcomes, full prompt hashes, annotations, evaluation scripts, or statistical significance tests for the main comparisons.
- The appendices describe configuration but do not state hardware, wall-clock latency, or a complete command sequence for reproducing every table.

## AIDB assessment

- Novelty: The novel contribution is a narrowly targeted provenance gate applied after structured summary generation, rather than another compressor, agent-training method, or raw-history selector. Its distinctive design choice is to preserve the host summary interface and delete only complete unsupported entries at every recurrent boundary.
- Usefulness: High potential usefulness for deployed agents whose model and compressor cannot be retrained, especially where summary checkpoints are structured and costly failures arise from compressor-authored future actions. Adoption should remain experimental because useful unsupported plans can be removed, multi-turn provenance is unresolved, and the external judge is a dependency.
- Confidence: medium
- Recommended action: watch
- Rationale: The controlled comparisons consistently favor SJC on Pass3 and the mechanism is supported by detailed failure tracing, while efficiency overhead is small. Confidence stops short of high because the main result uses only three runs per configuration, subgroup results include reversals, accuracy is not uniformly improved, the judge’s supported-entry recall is limited, and generalization beyond one compressor and single-instruction benchmarks is untested. AIDB should watch and reproduce the method before adopting it as a default compaction policy.

## Uncertainties

- **It is unclear whether the gains generalize to other structured compressors, schemas, agent models, or naturally large context windows.** — A drop-in claim is operationally valuable only if the parser, retrieval, and provenance criterion remain effective outside the single host compressor and forced-small-window regime.
  - Evidence: [b00106-28c32865d2] “two benchmarks, two agent models, and one host compressor”; [b00188-4342edd923] “We set these windows well below the models’ limits so that compaction occurs within each task.”
- **The causal contribution of deleting unsupported entries is not fully isolated from stochastic trajectories and shorter summaries.** — A single unsupported entry can coexist with success, and pruning also changes context length; more paired or replay-based interventions are needed to distinguish mechanism from correlated execution changes.
  - Evidence: [b00097-88174580bb] “The unsupported entry raises the chance of the error rather than determining it”; [b00081-86f92ccab1] “shortens each summary by 14%–27%.”
- **The practical tradeoff between false pruning and retained harmful entries is not fully characterized per model, task type, or summary section.** — The judge recovers a limited portion of supported entries, while provenance does not predict correctness. A globally fixed threshold may therefore conceal materially different utility tradeoffs.
  - Evidence: [b00198-9ae878aae9] “it recovers 64.2% of all supported entries.”; [b00198-9ae878aae9] “Provenance does not predict correctness”
- **Statistical uncertainty for the main benchmark differences is unresolved in the supplied text.** — Three sampled runs produce point estimates and across-run variability, but no confidence intervals or paired significance analysis is supplied for the reported improvements.
  - Evidence: [b00067-0766d23be4] “we evaluate each method over three independent runs.”; [b00059-9db5f91ad9] “Acc.: mean task success, with the across-run standard deviation as a subscript.”

## Open questions

- How does SJC perform with naturally occurring compaction thresholds near each model’s actual context limit rather than deliberately small windows?
- Can provenance be expanded to include earlier user turns, files, retrieved documents, or trusted agent actions without allowing unsupported plans to become self-validating memory?
- Would a utility-aware policy that combines provenance, contradiction detection, and estimated downstream value outperform source-only deletion?
- How sensitive are results to retrieval failures, entry segmentation errors, different summary schemas, and alternative judge providers?
- Do paired per-task analyses or trajectory replay confirm that the deleted entries, rather than incidental sampling differences or reduced summary length, cause the reliability gains?
- Can an open, locally reproducible judge match Jev’s calibration and repeatability without adding a proprietary API dependency?

## Proposed AIDB experiments

- **Hypothesis:** SJC’s Pass3 advantage persists under realistic context windows and with at least two additional structured host compressors, rather than depending on forced-frequent compaction or the OpenClaw schema.
  - Baseline: For every benchmark–model–compressor combination, compare the unmodified host compressor with the identical compressor plus SJC; include No Compression as a reference and preserve the same agent policy, seeds, and continuation points.
  - Primary metric: Paired per-task difference in Pass3, supplemented by mean task success, number of compactions, cumulative tokens, and judge cost.
  - Stop condition: Stop and reject broad drop-in generalization if the paired Pass3 improvement is non-positive for at least half of the added host-compressor settings or if the confidence interval includes a practically material decline in either benchmark.
- **Hypothesis:** Extending the admissible source set to earlier user messages prevents harmful deletion in multi-turn tasks without materially increasing retention of unsupported compressor reasoning.
  - Baseline: Compare source-only SJC as specified in the paper, SJC with earlier user turns treated as sources, and the unmodified prompting compressor on a multi-turn benchmark with annotated provenance.
  - Primary metric: Task success stratified by whether required information appears only in an earlier user turn, together with supported-entry recall and unsupported-entry precision.
  - Stop condition: Stop if adding user-turn provenance fails to improve success on earlier-turn-dependent tasks or reduces unsupported-entry precision enough to erase the overall Pass3 benefit.
- **Hypothesis:** A hybrid gate that retains sourced entries and separately rejects contradictions will reduce the supported-error failure class without increasing deletion of useful supported state.
  - Baseline: Compare original SJC, original Prompting, and SJC plus a contradiction detector using the same retrieved evidence and frozen agent/compressor trajectories.
  - Primary metric: Paired task success on cases containing supported-but-wrong entries, with false-deletion rate on annotated supported-and-correct entries as the safety metric.
  - Stop condition: Stop if the hybrid does not reduce failures attributable to supported erroneous entries or if its false-deletion rate exceeds that of original SJC by a pre-registered tolerance.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-10-16T14:31:48.924454+00:00`
- Document SHA-256: `76a5b319de328f56ac5f00d83a842080373712e14faca7dfa71f8e898dd55258`
- Metadata SHA-256: `1ae55a3baa104d14795ccc51210d12f98d232ff6a18bd6592aefe00ba4f112fc`
- Blocks: 200
- Deterministic repair attempts: 0
