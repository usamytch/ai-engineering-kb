# Beyond Memory Construction: Rethinking Memory Access for LLM-based Conversational Agents

## Executive summary

Threader replaces LLM-based rewriting of conversational memory with structure-aware access over preserved raw interactions. It combines incremental topic segmentation, separate user, assistant, and full-interaction representations, and two-stage multi-signal retrieval. The reported answer-accuracy, evidence-recall, and efficiency results are strong across LongMemEval and PersonaMem, with extensive ablations. However, the evidence remains benchmark-centered: segmentation supervision and LongMemEval judging depend on GPT-4.1-mini, abstraction-heavy tasks expose weaknesses, extremely large memories are untested, and important execution details are not present in the supplied blocks.

## Problem

**Statement.** LLM-based memory systems commonly rewrite raw dialogue into compact units, but the paper argues that this construction step loses evidence, becomes unstable as sessions grow longer and more entangled, and amplifies computational cost.

**Why it matters.** Long-term conversational agents must locate sparse, temporally distant, and evolving user evidence. Information discarded during memory writing cannot necessarily be recovered by later retrieval, while repeated LLM calls constrain scalability.

**Scope.** The work targets persistent token-level factual memory for long-horizon human–assistant dialogue. It does not establish performance for experiential memory, active-task working memory, embodied agents, tool traces, or truly lifelong memory stores.

## Method

Threader retains raw interactions as memory. A lightweight online classifier creates contiguous topic-coherent segments; each segment receives user-only, assistant-only, and full-interaction representations. Retrieval unions dense and BM25 candidates, applies localized message-level dense scoring, lexical fusion, and cross-encoder reranking, and finally returns complete segments to preserve discourse and temporal context.

### Key components

- Incremental binary CONTINUE/SEGMENT classification over the current segment and each incoming turn, implemented with a lightweight BERT encoder.
- Training supervision combines hard session boundaries with GPT-4.1-mini annotations of intra-session topic changes.
- Three shared-encoder views represent user-only text, assistant-only text, and the full interaction.
- The first retrieval stage unions candidates from dense multi-view retrieval and BM25.
- The second stage combines message-level dense evidence matching, lexical matching, and cross-encoder reranking.
- Complete segments rather than isolated messages are supplied to response generation.

### Assumptions

- Raw dialogue can serve as durable factual memory without construction-time semantic rewriting.
- Topic-coherent boundaries are useful retrieval units and can be predicted online from accumulated local context and the next turn.
- User, assistant, and full-interaction views provide complementary retrieval evidence.
- Preserving complete segments supplies sufficient context for query-time synthesis by the response model.
- Boundary supervision derived from LongMemEval transfers adequately to other conversational distributions.

## Main claims

- **The central design shift is from construction-time abstraction to structure-aware access over raw interactions.**
  - Evidence: [b00007-581589eaa9] “instead of transferring interactions into memory during construction, we treat raw interactions as first-class memory with efficient query-time access.”
- **Threader jointly uses incremental segmentation, multi-view representation, and multi-signal retrieval.**
  - Evidence: [b00020-2ea69ba40f] “Accordingly, Threader consists of three components. (1) Incremental Topic-Coherent Segmentation”; [b00020-2ea69ba40f] “(2) Multi-View Segment Representation”; [b00020-2ea69ba40f] “(3) Multi-Signal Evidence Retrieval combines dense, lexical, and reranking signals”
- **The segmentation procedure is fully online and does not revisit past context.**
  - Evidence: [b00026-bc4ca96bb0] “This formulation enables fully online segmentation without revisiting past context.”
- **Multi-view encoding is intended to prevent dominant assistant content from obscuring weaker user evidence.**
  - Evidence: [b00034-472346ca0a] “dominant assistant-side content can overshadow weak but critical user-side signals”; [b00035-058039da1c] “This design decouples evidence into complementary representations”
- **Message-level scoring localizes evidence, while whole-segment retrieval preserves coherent context.**
  - Evidence: [b00051-9a7acb0a73] “fine-grained scoring is used to identify evidence within segments, while segment-level retrieval ensures that retrieved content remains structurally and temporally consistent for generation.”
- **Rewrite-based memory construction becomes lossy and unstable as sessions become longer and denser.**
  - Evidence: [b00223-ce7f44a0e9] “both Mem0 and MemU construct fewer and less informative memory entries, indicating that the memory writing process becomes increasingly lossy.”; [b00223-ce7f44a0e9] “QA correctness fluctuates across different concatenation settings, suggesting that rewrite-based memory construction is unstable under long and high-entropy sessions.”
- **The authors report improvements in answer accuracy and evidence recall alongside reduced construction and query-time cost.**
  - Evidence: [b00082-35f6b4382f] “Threader not only improves answer accuracy and evidence recall, but also substantially reduces both construction and query-time cost.”

## Results

- **On LongMemEval, Threader’s overall scores were 80.60 and 90.60 under the two reported response settings, with relative improvements of 3.33% and 6.84%.**
  - Context: Main evaluation using segment retrieval and LLM-as-a-Judge.
  - Evidence: [b00061-d1dcdf7194] “Threader 94.29 (↑1.55%) 98.21 (↑3.77%) 63.33 (↓36.67%) 67.67 (↑1.12%) 83.33 (↑1.56%) 81.20 (↑6.94%) 80.60 (↑3.33%)”; [b00061-d1dcdf7194] “Threader 98.57 (↑2.99%) 98.21 (→0.00%) 96.67 (↓3.33%) 79.70 (↑0.95%) 93.59 (↑5.80%) 90.98 (↑11.02%) 90.60 (↑6.84%)”
- **On PersonaMem, Threader’s overall scores were 63.16 and 69.95 under the two reported response settings, with relative gains of 4.50% and 7.29%.**
  - Context: Main evaluation using segment retrieval and exact match.
  - Evidence: [b00063-f170b1a5e2] “Threader 78.95 (↑25.00%) 72.73 (↑5.27%) 69.77 (↑2.27%) 52.94 (↓25.00%) 72.73 (↓6.49%) 37.63 (↓5.40%) 58.27 (↑5.18%) 63.16 (↑4.50%)”; [b00063-f170b1a5e2] “Threader 84.21 (↑17.07%) 70.91 (↓2.50%) 80.62 (↑8.33%) 70.59 (→0.00%) 79.80 (↓8.14%) 45.16 (↓6.67%) 63.31 (↓5.38%) 69.95 (↑7.29%)”
- **Reported LongMemEval gains include Temporal-Reasoning improvements of 6.94% and 11.02%, plus a Knowledge-Update improvement of 5.80%.**
  - Context: Category-level results on sparse and temporally distant evidence.
  - Evidence: [b00059-732701fc2c] “Threader improves Temporal-Reasoning by 6.94% with GPT-5-nano and 11.02% with GPT-5-mini, and improves Knowledge-Update by 5.80% with GPT-5-mini.”
- **Threader underperformed category leaders on several tasks, with reported decreases including 36.67%, 3.33%, 25.00%, 6.49%, 5.40%, 2.50%, 8.14%, 6.67%, and 5.38%.**
  - Context: Category-specific negative results despite the strongest overall scores.
  - Evidence: [b00061-d1dcdf7194] “63.33 (↓36.67%)”; [b00061-d1dcdf7194] “96.67 (↓3.33%)”; [b00063-f170b1a5e2] “52.94 (↓25.00%) 72.73 (↓6.49%) 37.63 (↓5.40%)”; [b00063-f170b1a5e2] “70.91 (↓2.50%)”; [b00063-f170b1a5e2] “79.80 (↓8.14%) 45.16 (↓6.67%) 63.31 (↓5.38%)”
- **For construction per 100K input tokens, Threader reported 18.33 seconds, 0 LLM calls, 0 input tokens, and 0 output tokens; query latency was 8.66 seconds with the remaining reported retrieval-side values also 0.**
  - Context: The cost table separates offline memory construction from online query serving.
  - Evidence: [b00079-ad85d5e6c1] “We report construction cost per 100K input tokens and query-time cost per query”; [b00080-4ec1e71b63] “Threader 18.33 0 0 0 0 8.66 0 0 0 0”
- **Threader was slower than Self-RAG in construction, 18.33s versus 13.18s, while Mem0 had lower query latency at 8.38s.**
  - Context: Explicit efficiency cases in which Threader was not the best method.
  - Evidence: [b00078-82acfba1f5] “It is only slightly slower than Self-RAG (18.33s vs. 13.18s)”; [b00078-82acfba1f5] “Although Mem0 is slightly faster (8.38s)”
- **In the LongMemEval ablation, full Threader reached 90.60 ACC, 93.40 Full-R, and 96.50 Mean-R; removing segmentation reduced ACC to 87.00, fixed chunks produced ACC values from 79.80 to 86.40, and message-unit retrieval produced 85.80.**
  - Context: Component and retrieval-granularity ablation.
  - Evidence: [b00070-23363993df] “Threader 82.60 82.55 90.26 90.60 93.40 96.50 w/o Seg. 82.00 – – 87.00 – – Chunk-500 82.40 – – 85.60 – – Chunk-1K 74.20 – – 86.40 – – Chunk-2K 63.60 – – 79.80”; [b00070-23363993df] “Segment Unit 82.60 82.55 90.26 90.60 93.40 96.50 Message Unit 82.00 – – 85.80 – –”
- **On PersonaMem, Threader achieved 69.95 ACC; fixed-size alternatives included 67.40, removing BM25 gave 65.87, removing reranking gave 66.04, removing message-level embeddings gave 65.70, and message-unit retrieval gave 67.06.**
  - Context: Cross-dataset ablation of segmentation, retrieval signals, and retrieval granularity.
  - Evidence: [b00318-0b54e9b5eb] “Threader 69.95 Chunk-300. 65.70 Chunk-500 67.40 Chunk-700 63.67 Chunk-1K 59.76”; [b00319-aa7f756b4a] “Threader 69.95 w/o Emb. 67.40 w/o BM25 65.87 w/o Rerank. 66.04”; [b00319-aa7f756b4a] “w/o Msg.-Emb. 65.70 Retrieval granularity ablation Segment Unit 69.95 Message Unit 67.06”
- **With Qwen-family models, Threader reported 87.00 overall accuracy on LongMemEval and 82.00 on PersonaMem, with relative improvements of 8.21% and 2.98%.**
  - Context: Cross-backbone robustness test changing both memory-writing and response models.
  - Evidence: [b00302-a58af80f10] “On LongMemEval, Threader achieves an overall accuracy of 87.00, outperforming the strongest baseline, EverMemOS, by 8.21% relative improvement.”; [b00302-a58af80f10] “On PersonaMem, Threader also obtains the best overall score of 82.00, outperforming the strongest baseline, A-Mem, by 2.98% relative improvement.”
- **Keeping memory and retrieved evidence fixed while changing the response model increased Threader’s pooled accuracy from 60.69 to 75.95; the reported task scores included 100.00 and 65.59.**
  - Context: Controlled response-model comparison on abstraction-related questions.
  - Evidence: [b00346-b72b1e4d51] “Threader GPT-5-mini 96.67 45.16 63.31 60.69 Threader GPT-5.6-sol 100.00 65.59 77.70 75.95”; [b00342-f37599159d] “keep each method’s memory bank, retrieved evidence, and response prompt unchanged”

## Experimental evaluation

### Datasets

- LongMemEval contains 500 QA instances and tests single-session recall, preferences, multi-session reasoning, knowledge updates, and temporal reasoning; its average session length is approximately 2,160 tokens.
  - Evidence: [b00165-233460e062] “LongMemEval contains 500 QA instances, with an average session length of approximately 2,160 tokens.”; [b00165-233460e062] “single-session user information recall, single-session assistant information recall, preference recall, multi-session reasoning, knowledge update, and temporal reasoning.”
- PersonaMem contains 589 QA instances across 37 samples, with sessions averaging 26,165.38 tokens and seven question types.
  - Evidence: [b00158-7f74364485] “PersonaMem 589 37 1 26,165.38 174.65 149.82”; [b00182-7416a2568a] “PersonaMem contains 589 QA instances and covers seven question types.”
- The motivation study samples 60 LongMemEval instances and constructs original, 2×, 4×, and 8× session-concatenation settings while retaining QA pairs, evidence annotations, and total dialogue content.
  - Evidence: [b00222-7f585b0440] “sampling 60 instances, with 10 instances from each question type.”; [b00222-7f585b0440] “keep the original QA pairs, evidence annotations, and total dialogue content unchanged”; [b00222-7f585b0440] “the original data, 2×, 4×, and 8× session concatenation.”

### Baselines

- The memory baselines are Mem0, MemU, A-Mem, MemOS, and EverMemOS.
  - Evidence: [b00055-779676f35d] “The memory baselines include Mem0 (Chhikara et al., 2025), MemU, A-Mem (Xu et al., 2025), MemOS (Li et al., 2025), and EverMemOS (Hu et al., 2026)”
- The agentic-RAG baselines are Self-RAG and HippoRAG2.
  - Evidence: [b00055-779676f35d] “The agentic RAG baselines include Self-RAG (Asai et al., 2024) and HippoRAG2 (Gutiérrez et al., 2025)”
- Self-RAG uses a LangGraph-based reimplementation rather than its original specially fine-tuned release.
  - Evidence: [b00201-f2b6c12626] “we instead use a LangGraph-based re-implementation of its retrieve-generate-reflect workflow”

### Metrics

- LongMemEval correctness uses GPT-4.1-mini with a four-way judge protocol; only predictions labeled correct count as correct.
  - Evidence: [b00298-0012bc8665] “we use GPT-4.1-mini as the judge model and adopt a stricter four-way protocol: correct, partially_correct, incorrect, and insufficient.”; [b00298-0012bc8665] “Only predictions labeled as correct are counted as correct”
- PersonaMem uses exact match.
  - Evidence: [b00054-52d76ad1ef] “PersonaMem using exact match.”
- Retrieval evaluation reports Full-R for complete evidence coverage and Mean-R for average evidence recall.
  - Evidence: [b00067-8fe8feccc7] “Full-R denotes the fraction of queries with complete evidence coverage, and Mean-R denotes average evidence recall.”
- Segmenter evaluation covers exact-match F1, window-tolerant F1, boundary over-segmentation ratio, purity, and coverage.
  - Evidence: [b00257-1ad7696051] “Exact-match F1 measures agreement between predicted and reference boundaries.”; [b00259-b770e3efd2] “Window-tolerant F1 (W-F1) allows a boundary offset of one turn.”; [b00263-2c2913cbd4] “Boundary Over-segmentation Ratio (BOR) measures the number of predicted boundaries relative to the reference”; [b00266-636c7219ff] “Purity measures how well each predicted segment is contained within a reference segment”; [b00269-5ca2558b3e] “Coverage measures how well each reference segment is preserved within a predicted segment”
- Efficiency evaluation includes runtime or latency, LLM calls, input and output token use, and monetary cost.
  - Evidence: [b00079-ad85d5e6c1] “covering runtime/latency (s), LLM calls, input and output token consumption, and monetary cost ($).”

### Ablations

- Learned topic-coherent segmentation is compared with disabled segmentation and fixed-size chunking.
  - Evidence: [b00072-ecae96e44c] “Disabling segmentation or replacing topic-coherent segmentation with fixed-size chunking consistently degrades performance”
- Multi-view representation is compared with user-only, assistant-only, and full-interaction representations.
  - Evidence: [b00067-8fe8feccc7] “Emb.-User, Emb.-Asst., and Emb.-Full correspond to using only user, assistant, or full interaction views, respectively.”
- Dense embeddings, BM25, reranking, their combinations, and message-level embedding refinement are ablated.
  - Evidence: [b00069-861348277e] “w/o Emb. 79.00 79.15 87.40 84.60 86.17 92.19 w/o BM25 81.60 80.43 88.21 88.20 91.49 94.81 w/o Rerank. 78.40 77.23 86.43 88.20 91.49 95.08”; [b00069-861348277e] “w/o Msg.-Emb. 81.80 81.28 88.72 89.20 93.19 96.29”
- Complete-segment retrieval is compared with independent message retrieval.
  - Evidence: [b00071-6ceecba340] “segment-level in Threader vs. message-level”
- Segmenter analyses vary encoder family, threshold, training-data size, class distribution, and supervision mixture.
  - Evidence: [b00246-7b1c26718f] “We compare the base-size variants of BERT (Devlin et al., 2019), RoBERTa (Liu et al., 2019), and ModernBERT (Warner et al., 2025)”; [b00276-5c3cc0da58] “the effects of training data size, class distribution, and supervision mixture.”
- Retrieval analyses vary the retrieved-segment budget and fusion weights.
  - Evidence: [b00075-338afa6208] “the number of retrieved segments K”; [b00328-d9ea16f6e5] “The analyses below characterize sensitivity to variations in these weights.”

### Negative results

- Threader is less advantageous for preference aggregation and preference evolution, exposing a trade-off between evidence preservation and abstraction.
  - Evidence: [b00064-e6f73465f0] “Threader is less advantageous on tasks such as Single-Session-Preference (LongMemEval) and tracking-full-preference-evolution (PersonaMem)”; [b00064-e6f73465f0] “This suggests a complementary trade-off between evidence preservation and abstraction.”
- Increasing the retrieval budget eventually introduces irrelevant context and causes accuracy to fluctuate.
  - Evidence: [b00075-338afa6208] “after K becomes sufficiently large, additional segments introduce more irrelevant or weakly related context, and the accuracy no longer increases steadily but starts to fluctuate.”
- Additional segmenter training data beyond the original setting produced little benefit.
  - Evidence: [b00281-131f215baf] “Increasing the training size beyond the original setting yields little additional benefit”
- Hard-only supervision under-segments, whereas soft-only supervision over-segments.
  - Evidence: [b00292-421e77c053] “hard-only supervision produces conservative boundary predictions, resulting in low F1 and substantial under-segmentation.”; [b00292-421e77c053] “soft-only supervision leads to pronounced over-segmentation.”
- MemOS is omitted from the cost comparison because its interface prevents reliable attribution.
  - Evidence: [b00079-ad85d5e6c1] “MemOS is omitted due to its black-box interface, which prevents reliable cost attribution.”


## Limitations

- Segmentation mistakes can propagate to retrieval, particularly when related evidence is divided across boundaries.
  - Evidence: [b00144-5fce8d0a30] “segmentation errors may propagate to downstream retrieval.”; [b00144-5fce8d0a30] “if semantically related evidence is split across segment boundaries, it may reduce recall.”
- Storage and retrieval behavior for extremely large or lifelong histories is not established.
  - Evidence: [b00145-baa01ba18f] “scaling to extremely large or lifelong interaction histories may introduce additional storage and retrieval challenges.”
- The raw-evidence approach has limited built-in abstraction for distant dependencies and cross-segment synthesis.
  - Evidence: [b00146-a90dcd5033] “some tasks may benefit from higher-level abstraction or long-range reasoning that integrates information across distant segments.”
- Inputs exceeding the encoder window use default truncation, creating a possible evidence-loss path within long segments.
  - Evidence: [b00217-1e88d50a53] “Inputs exceeding the encoder context window are handled by the model’s default truncation behavior.”
- The validated scope is factual conversational memory; experiential and action-oriented memory remains future work.
  - Evidence: [b00148-af1e151351] “we will broaden the current factual-memory framework toward more general agent memory scenarios, especially experiential memory for action-oriented agents.”
- Memory inspection, editing, deletion, selective forgetting, access control, and retention policies are proposed rather than evaluated system capabilities.
  - Evidence: [b00148-af1e151351] “Important directions include user-facing mechanisms for memory inspection, editing, deletion, and selective forgetting, as well as privacy-preserving storage, access control, retention policies”
- LongMemEval judging and fine-grained segmentation annotations both depend on GPT-4.1-mini, without human-agreement evidence in the supplied blocks.
  - Evidence: [b00086-468119ff0e] “GPT-4.1-mini was used to annotate fine-grained intra-session topic boundaries for segmenter training and evaluation.”; [b00086-468119ff0e] “GPT-4.1-mini was also used as an LLM-as-a-Judge to evaluate answer correctness on LongMemEval”
- The main evaluation contains two benchmarks, and LoCoMo is excluded because its format and session length differ from the target setting.
  - Evidence: [b00199-ba51fb20f3] “we do not include it in our main evaluation because it differs from our target setting in both session length and interaction format.”

## Reproducibility

**Status:** partial

The paper provides substantial experimental detail, including model choices, segmenter optimization settings, retrieval weights, and extensive ablations. Reproducibility remains partial because the referenced executable artifacts and prompt contents are not contained in the supplied blocks, the repository state is not pinned, and stochastic or API-based evaluation lacks seeds, repeated-run statistics, and full environment details.

**Available artifacts**

- The paper states that code is available in a public Threader repository.
- The supplied blocks describe the algorithmic framework and name the embedding, reranking, construction, response, and judge models.
- Segmenter training settings include optimizer, epochs, batch size, learning rate, precision, and GPU.
- Dataset statistics, result tables, cost measurements, ablations, threshold selection, and retrieval weights are reported.
- The paper states that pseudocode, prompts, baseline details, training procedures, and hyperparameters appear in appendices.

**Missing pieces**

- The supplied blocks do not contain the actual pseudocode or response and judge prompt text.
- No repository commit hash, release tag, dependency lockfile, package versions, or container image is stated.
- Random seeds, repeated-run counts, variance, confidence intervals, and significance tests are not stated.
- The exact hardware and measurement protocol for the full cost and latency table are not stated.
- API model snapshots, pricing date, decoding settings, concurrency, and caching conditions are not stated.
- Human validation or inter-rater agreement for generated boundary labels and judge decisions is not reported.
- Repository availability and completeness cannot be verified from the supplied document alone.

## AIDB assessment

- Novelty: The principal novelty is an architectural reframing: preserve raw dialogue as first-class memory and spend computation on lightweight structural indexing and query-time multi-signal access rather than LLM rewriting of every interaction. The individual retrieval ingredients are established, but their evidence-preserving integration and explicit construction-versus-access trade-off form a meaningful systems contribution.
- Usefulness: Potentially high for persistent conversational-memory systems where evidence fidelity, auditability, and construction cost matter. The reported cost profile, cross-backbone results, and ablations make the approach operationally interesting. Adoption should remain conditional for preference synthesis, governance-sensitive use, encoder-overflow cases, and memory scales beyond the evaluated benchmarks.
- Confidence: medium
- Recommended action: read
- Rationale: The paper reports strong benchmark results, direct efficiency measurements, explicit negative results, and broad ablations across two dialogue-memory benchmarks and several response settings. Confidence is not high because evaluation remains narrow, one benchmark relies on an LLM judge, segmentation supervision partly comes from the same model family, baseline implementations are not uniformly original, and no repeated-run uncertainty or lifelong-scale experiment is reported.

## Uncertainties

- **The stability of the reported gains across random seeds, API revisions, and repeated generations is unknown.** — Central measurements depend on stochastic proprietary models, while the supplied blocks report point estimates without dispersion or significance tests.
  - Evidence: [b00056-6cfe228208] “Our main setting uses GPT-4.1-mini for memory construction and GPT-5-mini for response generation”; [b00298-0012bc8665] “we use GPT-4.1-mini as the judge model”
- **The validity of GPT-4.1-mini boundary annotations and judge decisions relative to human judgments is unresolved.** — Annotation noise could affect both segmentation training and reported LongMemEval accuracy.
  - Evidence: [b00086-468119ff0e] “GPT-4.1-mini was used to annotate fine-grained intra-session topic boundaries”; [b00086-468119ff0e] “GPT-4.1-mini was also used as an LLM-as-a-Judge”
- **The effect of using LongMemEval-derived dialogue for segmenter training, threshold calibration, and retrieval-weight calibration is not fully resolved.** — Repeated use of one benchmark distribution may favor that benchmark even when QA labels are excluded from calibration.
  - Evidence: [b00241-b3bd54f884] “We construct segmentation supervision from the dialogue histories of abstention instances in LongMemEval.”; [b00251-8e9a87df3e] “This subset also serves to calibrate the boundary decision threshold.”; [b00328-d9ea16f6e5] “We calibrate the segmentation threshold and retrieval weights on the same 50-instance LongMemEval subset”
- **The practical effect of default encoder truncation is not quantified.** — A system designed to preserve evidence may still discard it when a segment exceeds the encoder window.
  - Evidence: [b00217-1e88d50a53] “Inputs exceeding the encoder context window are handled by the model’s default truncation behavior.”
- **The portability of the cost comparison across hardware, pricing, concurrency, caching, and serving conditions is unknown.** — Latency and monetary advantages may change under different deployment environments.
  - Evidence: [b00079-ad85d5e6c1] “We report construction cost per 100K input tokens and query-time cost per query”
- **The cross-backbone experiment changes memory-writing and response models simultaneously.** — It cannot isolate whether score changes arise from memory construction, response reasoning, or their interaction.
  - Evidence: [b00300-da9ceb6087] “This setting changes both the memory-writing model and the response generator, and therefore should be interpreted as a cross-backbone robustness test rather than a component-wise ablation.”

## Open questions

- How does Threader perform on genuinely lifelong histories with persistent updates, deletions, and storage constraints?
- What is human agreement with the GPT-4.1-mini boundary annotations and LongMemEval judge decisions?
- How much evidence is lost through encoder truncation, and would longer-context encoders preserve the latency advantage?
- Do the gains persist across repeated runs and fixed, versioned model snapshots?
- How does Threader compare with hybrid systems that preserve raw evidence while maintaining lightweight preference summaries?
- What are the index growth rate, memory footprint, update throughput, and deletion cost under sustained use?
- Can provenance, privacy controls, selective forgetting, and user-visible correction be added without harming retrieval fidelity?
- How well does the approach transfer to multilingual conversations and distributions beyond the two evaluated benchmarks?

## Proposed AIDB experiments

- **Hypothesis:** Threader’s advantage remains statistically reliable across repeated stochastic runs and fixed model snapshots.
  - Baseline: Re-run Threader and the strongest competing methods with identical prompts, model snapshots, and retrieval budgets.
  - Primary metric: Mean overall answer-accuracy difference with a bootstrap confidence interval for each benchmark.
  - Stop condition: Stop if the confidence interval for Threader’s gain includes zero on either benchmark or when the preregistered run budget is exhausted.
- **Hypothesis:** A hybrid raw-evidence and lightweight-summary memory improves abstraction-heavy tasks without reducing evidence recall.
  - Baseline: Full Threader using raw segments only.
  - Primary metric: Pooled accuracy on preference and personalized-generation categories, with Full-R as a non-inferiority guardrail.
  - Stop condition: Stop if pooled accuracy does not improve or Full-R exceeds the preregistered allowable decline.
- **Hypothesis:** Replacing default truncation with long-context or hierarchical encoding improves retrieval for oversized segments while retaining acceptable latency.
  - Baseline: Current encoders using default truncation.
  - Primary metric: Mean-R on queries whose gold evidence lies beyond the original encoder window.
  - Stop condition: Stop if Mean-R does not improve or query latency exceeds the preregistered deployment budget.
- **Hypothesis:** Threader maintains retrieval quality and manageable resource growth at lifelong-memory scale.
  - Baseline: Current Threader at benchmark scale and fixed-size chunking with the same encoder and reranker.
  - Primary metric: Full-R as indexed history grows, accompanied by index size and tail query latency.
  - Stop condition: Stop when Full-R falls below the preregistered quality threshold or latency or storage exceeds its capacity budget.
- **Hypothesis:** Human-reviewed supervision and evaluation preserve the reported ranking of methods.
  - Baseline: Current GPT-4.1-mini boundary annotations and judge labels.
  - Primary metric: Human–model agreement and the change in Threader’s accuracy margin over the strongest baseline after adjudication.
  - Stop condition: Stop if agreement falls below the preregistered threshold or human adjudication reverses the overall ranking.
- **Hypothesis:** The learned segmenter transfers beyond the evaluated benchmarks without dataset-specific calibration.
  - Baseline: Fixed-size chunking and the existing LongMemEval-trained segmenter.
  - Primary metric: Answer accuracy and Mean-R on an independently sourced human–assistant dialogue benchmark.
  - Stop condition: Stop if the transferred segmenter fails to outperform the strongest fixed-size baseline on both primary measures.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-10-16T14:31:48.129078+00:00`
- Document SHA-256: `39831818a7f8f9290f4d134d0f685702d99aed27fd934d42467b579cff626b92`
- Metadata SHA-256: `660edec7137a81ba0dba71024e4245b0fff5ae0e3c7159b450f97608a0d3e9fd`
- Blocks: 347
- Deterministic repair attempts: 0
