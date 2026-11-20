# Can LLM Agents Organize Their Own Memory?

## Executive summary

SoMem lets an LLM organize persistent memory as editable linked Markdown while immutable source records retain evidence and deterministic code rebuilds temporal, relational, and recent views. With a shared Reader, it leads the reported overall results on three conversational-memory benchmarks. The strongest controlled ablation shows that removing Source hurts much more than removing Topic, supporting the combination of summaries and original records. Cross-model reuse is promising, but the evidence remains benchmark-centric, judge-dependent, costly, and mostly based on single saved runs; semantic correctness is not guaranteed by runtime validation.

## Problem

**Statement.** Deployed LLM agents must preserve new information outside fixed model weights, but fixed schemas and isolated records make it difficult to revise groupings while retaining the original evidence and consistent retrieval structures.

**Why it matters.** Long-running interactions introduce updates, relationships, and temporal qualifications. Compact summaries risk omitting context, whereas complete histories preserve detail but force the agent to locate the relevant exchanges.

**Scope.** The paper studies persistent memory construction and question-time access over conversational histories. It does not establish sustained personalization, autonomous task execution, or semantic correctness under continuing real-world updates.

## Method

SoMem archives interactions as immutable Source records. A Writer creates and revises linked Topic documents, promotes a bounded subset into Core, and attaches event times and Source references to statement spans. Before accepting an edit, the runtime validates structure, paths, references, links, temporal values, Source immutability, and Core capacity. Deterministic code then rebuilds Graph, Timeline, Recent, and the file inventory. At query time, a Reader starts with Core, Recent, an inventory, and an optional question date, then iteratively searches, lists, and reads Topic, derived views, and original Source evidence without a fixed retrieval order.

### Key components

- Source preserves original interaction records and remains directly inspectable.
- Topic is the agent-edited semantic layer: documents, headings, paragraphs, cross-document links, event-time annotations, and evidence references may be reorganized as information accumulates.
- Core is a size-bounded Topic file placed in every query’s initial context for persistent preferences, standing requirements, and frequently needed background.
- Graph derives directed links and backlinks from paragraph references; Timeline derives time-indexed entries from event annotations; Recent derives the most recently created memory units.
- Staged validation rejects malformed updates without replacing the prior memory state, then rebuilds all access views from accepted content.
- The Reader chooses between exact-text, BM25, and embedding search and can follow documents, links, dates, and Source references through multiple tool rounds.

### Assumptions

- The Writer can produce useful semantic organization even though validation checks only structural and referential properties, not factual correctness or completeness.
- Paragraph-level units, explicit event annotations, and document links are adequate primitives for the evaluated conversational-memory tasks.
- The selected Writer and Reader prompts, tool limits, and model configurations represent meaningful implementations of each compared memory method.
- LLM-judge scores are treated as useful proxies for answer correctness despite the absence of systematic human calibration.

## Main claims

- **The central design separates model-controlled semantic organization from runtime-controlled evidence and access consistency.**
  - Evidence: [b00009-89022ce633] “the model controls semantic organization and the runtime maintains evidence and access consistency.”; [b00031-4d784d82b1] “These operations construct the views without requiring the model to write each representation separately.”
- **Accepted memory edits retain resolvable evidence links and trigger reconstruction of derived views, while rejected edits preserve the previous state.**
  - Evidence: [b00134-74da119785] “Accepted edits are normalized, relative links affected by moves are repaired, and Graph, Timeline, Recent, and the file inventory are rebuilt”; [b00134-74da119785] “a rejected edit leaves the previous state unchanged.”
- **Question answering is iterative and agent-directed rather than a single prescribed retrieval step.**
  - Evidence: [b00044-3b671abcd8] “These operations can be combined according to the question, without a prescribed retrieval sequence.”; [b00138-80641c8f8e] “the agent can enter through a Topic document, a Timeline date, or a search hit, and then follow links and source references as needed.”
- **The resulting workspace is intended to be reusable by Readers other than the Writer that constructed it.**
  - Evidence: [b00081-727e5d65b3] “other Readers can use the same documents and evidence references without rebuilding memory.”

## Results

- **With the shared GPT-6 Luna Reader, SoMem achieved 88.96 overall LoCoMo accuracy versus 86.30 for E-mem, the next-highest listed memory method, while Full Context reached 84.22.**
  - Context: This is the full 1,540-question primary comparison. The shared Reader improves comparability, although each method retains its own organization and retrieval pipeline.
  - Evidence: [b00060-e89cc0d9c5] “Table 2: LoCoMo LJ accuracy (%) on all 1,540 category 1–4 questions.”; [b00061-0325db2bb6] “Full Context 94.17 80.85 45.83 72.59 84.22”; [b00061-0325db2bb6] “E-mem 92.75 85.11 58.33 78.82 86.30 SoMem 94.53 83.33 59.38 88.16 88.96”; [b00062-433c1ce5ab] “all other rows use GPT-6 Luna.”
- **On BEAM-100K, SoMem reported a 54.02 overall nugget score and 61.50 pass rate; the strongest other listed nugget score was Full Context at 50.92, while the strongest other pass rate was A-Mem at 55.75.**
  - Context: The comparison covers 400 questions and uses capability-specific rubric scoring. SoMem is not uniformly best by capability: its reported abstention score is 23.75, below several alternatives.
  - Evidence: [b00064-5aa1d06076] “Table 3: BEAM-100K results (%) on 400 questions.”; [b00065-1c8d47c3e4] “Full Context 82.86 50.25 41.25 50.00 25.63 36.95 56.25 84.38 49.14 32.50 50.92 55.25”; [b00065-1c8d47c3e4] “A-Mem 76.82 54.30 41.25 46.25 23.44 39.78 66.88 86.25 40.11 30.00 50.51 55.75”; [b00065-1c8d47c3e4] “SoMem 73.70 51.53 53.75 48.75 36.56 46.84 73.75 85.62 45.94 23.75 54.02 61.50”
- **On LongMemEval-S, SoMem reached 76.50 overall accuracy versus 74.50 for LightMem, but it was weaker on knowledge update: 77.56 versus 91.67 for LightMem.**
  - Context: This full 500-question result supports the overall advantage while also exposing a consequential category-level weakness that the aggregate score conceals.
  - Evidence: [b00067-b920b2d208] “Table 4: LongMemEval-S LJ accuracy (%) on all 500 questions.”; [b00068-f1f4a84382] “LightMem 91.67 75.56 25.00 86.67 92.86 71.80 74.50”; [b00068-f1f4a84382] “SoMem 77.56 58.65 99.11 73.33 98.57 73.31 76.50”
- **The controlled LoCoMo ablation found that removing Source changed accuracy by −8.64 percentage points with a 95% interval of [−11.67,−6.11], while removing Topic changed it by −2.92 with [−4.96,−0.88]. Removing Core produced +0.00 with [−1.16,+1.09].**
  - Context: All conditions reused frozen memory and changed query-time access only. The result supports Source and Topic as complementary access components, but does not show how construction quality changes when a component is absent.
  - Evidence: [b00165-f397e8a7f1] “Condition Δ (pp) W→R R→W 95% CI (pp)”; [b00154-ac356c01d1] “All conditions reuse the same memory without reconstruction and change only query-time component access.”; [b00165-f397e8a7f1] “w/o Topic −2.92 65 110 [−4.96,−0.88] w/o Core +0.00 52 52 [−1.16,+1.09]”; [b00165-f397e8a7f1] “w/o Source −8.64 28 161 [−11.67,−6.11]”
- **Cross-model reuse worked across the reported LoCoMo matrix: memory written by GPT-5.6 Luna yielded overall scores from 92.34 to 93.25 across four Readers, and the paper reports that this Writer’s memory had the highest accuracy averaged across Readers for every task category.**
  - Context: This supports interoperability of the document workspace within the tested model set. It does not isolate reuse from model- and prompt-specific configuration effects.
  - Evidence: [b00080-bb6a7ab64b] “GPT-5.6 Luna GPT-5.6 Luna 95.36 91.49 72.92 90.97 92.34”; [b00080-bb6a7ab64b] “Qwen 3.8 Flash 95.01 93.97 73.96 93.77 93.25”; [b00079-4ece1ca60b] “Each Writer’s frozen memory is reused by all Readers.”; [b00081-727e5d65b3] “its accuracy averaged across Readers is highest for every task category.”

## Experimental evaluation

### Datasets

- LoCoMo: four question-answering types; the full evaluation has 1,540 questions, with a fixed 100-question Reader-effort subset.
  - Evidence: [b00054-07b23bc8cb] “LoCoMo 4 QA types 1,540 / 100”
- LongMemEval-S: six question-answering types and 500 full-set questions.
  - Evidence: [b00054-07b23bc8cb] “LongMemEval-S 6 QA types 500 / –”
- BEAM-100K: ten memory capabilities, with 400 full-set questions and a 200-question Reader-effort subset.
  - Evidence: [b00054-07b23bc8cb] “BEAM-100K 10 capabilities 400 / 200”

### Baselines

- Primary memory baselines are A-Mem, Mem0, MemoryOS, Nemori, LightMem, and E-mem.
  - Evidence: [b00058-1dcfdbc950] “A-Mem (Xu et al., 2025), Mem0 (Chhikara et al., 2025), MemoryOS (Kang et al., 2025), Nemori (Ma et al., 2026), LightMem (Fang et al., 2026), and E-mem (Wang et al., 2026a).”
- Full Context answers from the untruncated original history with the same Reader and no retrieval tools.
  - Evidence: [b00058-1dcfdbc950] “Full Context uses the same Reader and answers directly from the complete original history, without truncation or retrieval tools.”
- A supplementary access comparison includes one-shot BM25 and Dense retrieval plus local adaptations of E-mem and LightMem.
  - Evidence: [b00171-5f436a2c2d] “BM25 and Dense retrieve Source evidence once; E-mem reconstructs routed episodic evidence; and LightMem retrieves extracted facts.”

### Metrics

- LoCoMo and LongMemEval-S use GPT-4o-mini LLM-judge accuracy; overall accuracy is the proportion of correctly answered questions.
  - Evidence: [b00056-95c984b528] “We report LLM-judge (LJ) accuracy by question type and overall.”; [b00056-95c984b528] “Overall accuracy is the proportion of correctly answered questions across the evaluation set.”
- BEAM-100K uses criterion scores of 0, 0.5, or 1, averaged within questions and over questions as a nugget score; pass rate uses a score of at least 0.5.
  - Evidence: [b00056-95c984b528] “each rubric criterion receives a score of 0, 0.5, or 1”; [b00056-95c984b528] “counting questions with a score of at least 0.5 as passes.”
- Scaling analyses measure answer score and mean cumulative Reader input and output tokens per question, excluding construction and evaluation.
  - Evidence: [b00085-360720353d] “We measure actual usage as the mean cumulative input and output tokens across Reader calls per question, excluding memory construction and evaluation.”

### Ablations

- Full LoCoMo query-time removals test Topic, Core, Source, Recent, Timeline, and Graph against the same frozen memory and fixed Reader.
  - Evidence: [b00072-02cfd99015] “We freeze memory and fix the Reader (GPT-6 Luna without reasoning effort) and query settings, changing only query-time access”; [b00074-2d3fa0126d] “w/o Topic 92.51 76.95 57.29 85.67 86.04 w/o Core 93.10 86.52 58.33 89.41 88.96 w/o Source 83.35 82.98 52.08 78.50 80.32”
- Paired uncertainty is estimated by conversation-level percentile bootstrap on saved answers, conditional on those runs.
  - Evidence: [b00163-8ac6d936ce] “We compute paired percentile bootstrap intervals by resampling conversations to preserve dependence among questions from the same history.”; [b00166-9965179847] “They describe sampling uncertainty for the saved runs, not repeated-run variability; no multiple-comparison correction is applied.”

### Negative results

- Removing Core left overall LoCoMo accuracy unchanged, and removal of individual derived views had intervals including zero; these components’ overall effects remain within sampling uncertainty.
  - Evidence: [b00076-361f29765c] “removing Core leaves overall accuracy unchanged”; [b00076-361f29765c] “The effects of the derived views and Core on overall accuracy remain within sampling uncertainty.”
- Greater reasoning effort sometimes plateaued or reversed; the highest tested setting was not consistently best.
  - Evidence: [b00088-e234f2a026] “The gains nevertheless exhibit saturation and occasional reversals.”; [b00088-e234f2a026] “others plateau or decline at the highest tested setting.”
- SoMem’s LongMemEval-S knowledge-update result trails several alternatives despite its best aggregate result.
  - Evidence: [b00068-f1f4a84382] “Mem0 91.03 60.90 76.79 73.33 91.43 62.41 72.80”; [b00068-f1f4a84382] “SoMem 77.56 58.65 99.11 73.33 98.57 73.31 76.50”
- The system’s full LoCoMo reference cost is substantially higher than the reported costs of several baselines.
  - Evidence: [b00197-7251888132] “SoMem reaches 88.96% LJ accuracy at a total reference cost of $229.73, compared with $6.75 for Mem0 (80.32%), $6.46 for LightMem (77.99%), and $35.19 for A-Mem (60.06%)”


## Limitations

- External validity is narrow: the experiments mainly test question answering over stored conversation histories, not sustained personalization or long-term task execution.
  - Evidence: [b00098-fde1680f49] “they do not fully cover sustained personalization or task execution during long-term interaction.”
- Evaluation depends on an LLM judge without systematic human calibration, creating an unresolved measurement-validity risk.
  - Evidence: [b00098-fde1680f49] “Evaluation relies on LLM judges without systematic human calibration and may be affected by judge biases.”
- The ablations remove query-time access from frozen memory rather than rebuilding memory without each component, and each condition is a single run.
  - Evidence: [b00099-140adb8094] “Component ablations restrict access to frozen memories rather than testing how memory would be reconstructed or reorganized after removing a component; each condition is a single run”
- Reasoning-effort labels are not equivalent compute budgets across providers, weakening direct cross-model scaling comparisons.
  - Evidence: [b00099-140adb8094] “their labels do not represent equivalent compute budgets; cross-model comparisons reflect performance under the respective configurations.”
- Structural validation cannot establish that organized memories are factually correct or complete.
  - Evidence: [b00100-3c765d81d8] “The runtime checks evidence references and structural consistency but cannot guarantee the semantic correctness or completeness of memory content.”
- Construction, maintenance, and multi-round reading introduce material overhead, and deployment requires controls not evaluated here.
  - Evidence: [b00100-3c765d81d8] “Memory construction, maintenance, and multi-round reading incur additional overhead”; [b00100-3c765d81d8] “Practical deployment additionally requires access controls, retention policies, and isolated tool execution for the stored conversations.”

## Reproducibility

**Status:** partial

The disclosed code URL and unusually detailed protocol, limits, ablation controls, bootstrap seed, and resource accounting support partial reproduction. Confidence remains below strong because proprietary model behavior may drift, important prompts and environments are absent from the supplied text, and most reported comparisons rely on single saved runs evaluated by one uncalibrated judge.

**Available artifacts**

- The abstract supplies a public code repository URL.
- The paper specifies datasets, full-set and subset sizes, baseline families, shared primary Writer and Reader, judge model, temperature, retrieval interfaces, and query-turn limits.
- Appendices report ablation controls, paired-bootstrap sampling details and seed, token accounting, model calls, latency, and reference costs.

**Missing pieces**

- The supplied blocks do not state exact prompts for memory construction and answering, despite mentioning a LoCoMo judge prompt figure.
- No dependency lockfile, software environment, hardware specification, API snapshot, or model version identifiers beyond model names are stated in the supplied blocks.
- No repeated-run variance is reported for primary comparisons or ablations.
- No human evaluation or judge-calibration data are supplied.
- The supplied blocks do not give per-method construction parameters and costs in a complete machine-readable table.

## AIDB assessment

- Novelty: The distinctive contribution is the combination of agent-editable ordinary documents, immutable evidence records, resolvable statement-level provenance, and deterministic reconstruction of multiple access views after validated edits. Related work already includes model-controlled memory, topic documents, hierarchical organization, graphs, and iterative retrieval, so novelty lies primarily in this division of responsibilities and consistency mechanism rather than in any single primitive.
- Usefulness: High for teams designing inspectable persistent-agent memory: the method exposes evidence, supports revision, allows iterative inspection, and decouples stored memory from the answering model. Practical adoption should be gated by cost, semantic-integrity tests, privacy controls, and evaluation on real update-heavy workflows.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled shared-Reader comparisons and paired ablations make the paper decision-relevant, especially the strong Source-removal effect and reusable workspace. Adoption is premature because judge calibration, repeated-run stability, construction ablations, semantic error behavior, and production safety are unresolved, while reported cost is high relative to several baselines.

## Uncertainties

- **It is unclear how often the Writer creates incorrect, incomplete, duplicated, or misleading Topic content during long update sequences.** — The runtime validates references and structure, but downstream retrieval may confidently use semantically flawed summaries.
  - Evidence: [b00134-74da119785] “factual interpretation remains the responsibility of the model.”; [b00100-3c765d81d8] “Detecting and correcting omissions or errors during continued updates therefore remains an important direction for further study.”
- **The stability of headline gains across repeated construction, retrieval, and judging runs is unknown.** — Single-run agent trajectories and judge outputs may vary, while the reported bootstrap intervals condition on saved runs rather than measuring run-to-run variability.
  - Evidence: [b00099-140adb8094] “each condition is a single run”; [b00166-9965179847] “They describe sampling uncertainty for the saved runs, not repeated-run variability”
- **The independent contribution of history length is not established by the BEAM-1M supplement.** — The longer-history experiment changes Reader configuration, preventing a controlled conclusion about scaling with history length.
  - Evidence: [b00182-9ac1282d65] “Its Reader configuration differs from the primary BEAM-100K comparison, so it documents performance at this scale rather than isolating the effect of history length.”
- **The degree to which LLM-judge preferences alter method rankings is unresolved.** — A large difference between reported BEAM-1M judge outcomes indicates that absolute conclusions may be judge-sensitive.
  - Evidence: [b00180-12fda692cb] “GPT-4o-mini 69.29 63.24 GPT-6 Sol 84.14 73.86”; [b00098-fde1680f49] “may be affected by judge biases.”

## Open questions

- How does SoMem compare with baselines under repeated Writer, Reader, and judge runs with confidence intervals over the complete pipeline?
- Does evidence-linked organization improve sustained personalization and task completion, not just retrospective question answering?
- How frequently do Topic summaries omit, distort, duplicate, or incorrectly reconcile Source evidence after months of incremental updates?
- What policy should decide when to reorganize, split topics, promote content to Core, or trigger the optional repair probe?
- Can equivalent or better accuracy be achieved with bounded cost, latency, and tool calls under production constraints?
- How should access control, retention, deletion, and provenance repair propagate across Topic, Core, Graph, Timeline, Recent, and Source?
- Would calibrated human evaluation preserve the reported rankings and category-level conclusions?

## Proposed AIDB experiments

- **Hypothesis:** The advantage of Source plus Topic over either layer alone persists across independent memory constructions and Reader trajectories, not merely within one frozen saved run.
  - Baseline: Full SoMem versus systems reconstructed from scratch without Topic and without Source, using identical Writer, Reader, prompts, budgets, and question sets.
  - Primary metric: Mean paired change in human-verified answer accuracy across independent end-to-end runs, with intervals that include construction, retrieval, and judging variability.
  - Stop condition: Stop when the interval for each removal is narrow enough to distinguish a practically meaningful accuracy loss, or when a prespecified run budget is exhausted without such separation.
- **Hypothesis:** A semantic audit-and-repair stage reduces unsupported or incomplete Topic statements during long incremental update streams without erasing valid historical qualifications.
  - Baseline: Validated SoMem updates using structural and referential checks only.
  - Primary metric: Human-adjudicated rate of unsupported, contradicted, duplicated, or materially incomplete Topic statements after staged update sequences.
  - Stop condition: Stop if the repair system fails to reduce the aggregate semantic-error rate, increases loss of valid facts beyond a prespecified tolerance, or exceeds the allowed maintenance budget.
- **Hypothesis:** A budget-aware Reader can retain most of SoMem’s answer quality while materially reducing cumulative tokens, calls, latency, and monetary cost.
  - Baseline: The paper’s fixed query-turn configurations for the same frozen memories and Readers.
  - Primary metric: Answer quality at matched cumulative Reader-token and latency budgets, summarized as the quality–cost Pareto frontier.
  - Stop condition: Stop when no tested policy improves the frontier over the fixed configuration on held-out conversations, or when further tuning yields no prespecified minimum gain.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:09.829602+00:00`
- Document SHA-256: `9981dc5162a69643b00cd36ad99f4123dbed003a2b8fbdcdb7e3d250e12e0073`
- Metadata SHA-256: `32358b4eabeac4144f9304c7d0670ca03f8e5197090b8bc4415e5121f53e5f98`
- Blocks: 197
- Deterministic repair attempts: 0
