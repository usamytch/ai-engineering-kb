# Memory Tax: Dissecting the Net Value of Agent Memory

## Executive summary

The paper asks whether constructed agent memory adds value beyond retrieval from raw history. Across three conversational-memory benchmarks and three backbones, its controlled tables show that most tested memory systems lose to a two-round hybrid RAG reference, although isolated gains remain. It frames these gains and losses as “memory benefit” and “memory tax,” then diagnoses construction loss, reduced accessibility, and cross-backbone fragility. The central warning is persuasive and practically useful, but generality is constrained by sampled, mostly static English benchmarks, modified baseline configurations, incomplete numerical support for several diagnostic figures, and code/results that are promised rather than supplied.

## Problem

**Statement.** Dedicated memory systems alter raw interaction history through extraction, compression, organization, or learned policies, but their marginal value is unclear when direct retrieval from that same history is not used as a strong control.

**Why it matters.** Without a retrieval control, gains attributable merely to finding raw evidence can be mistaken for gains from constructing memory. This matters because memory construction and maintenance add computation and can discard, obscure, fragment, or distort evidence.

**Scope.** The main study covers personal-agent conversational memory, then tests whether the benefit–tax framing transfers to experiential memory and long-horizon world-model memory. It does not establish universal conclusions for all memory forms or live deployments.

## Method

The authors treat chunk-based RAG over raw history as the reference and compare each memory system with it at aggregate and per-query levels. A query solved only by memory contributes to memory benefit; a query solved by RAG but lost by memory contributes to memory tax. Main experiments standardize QA models, judge, embedding model, and retrieval exposure where possible. Diagnostic analyses separate construction faithfulness, retrieval accessibility, and robustness to construction/QA backbone changes. Additional experiments cover benchmark headroom, experiential memory, and video world-model memory.

### Key components

- Evaluate flat-store, hierarchical/lifecycle, graph-based, and trained-policy memories against one-round and two-round hybrid RAG.
- Run main systems with Qwen3.5-4B, Qwen3.6-27B, and GPT-5.6 Luna (low), sharing Qwen3-Embedding-0.6B and generally a common reranker.
- Align heterogeneous retrieval configurations using Retrieval Scope: the fraction of retrievable-store tokens exposed from retrieval through answering.
- Measure answer quality with a Qwen3.6-27B LLM judge and separately track token cost, wall-clock time, LLM calls, and memory-store size.
- Trace benchmark gold turns into memory units, compare oracle raw evidence with oracle memory evidence, annotate information loss, replay iterative retrieval, and inspect similarity drift.
- Construct memories and answer them with different backbones to assess sensitivity beyond raw-history RAG.
- Test transfer of the framing on agent-task experience libraries and video world-model memory carriers.

### Assumptions

- Naive hybrid RAG is an appropriate operational reference for the net value of constructed memory, not a memory-free lower bound in an absolute conceptual sense.
- Judge accuracy is an adequate proxy for task correctness; the reported human-agreement check supports but does not eliminate judge bias.
- Retrieval Scope makes access opportunities more comparable, although it does not equalize exact inference-token budgets.
- Changes made to official memory configurations do not materially disadvantage those systems; the authors provide selected validations, but not a full factorial retuning of every method.
- Per-query correctness differences against RAG meaningfully operationalize benefit and tax, even though both quantities depend on the chosen RAG implementation.

## Main claims

- **The paper defines the net value of constructed memory relative to naive RAG and decomposes it into query-level gains and losses called memory benefit and memory tax.**
  - Evidence: [b00033-e795bf84a9] “Memory does solve some queries RAG misses, benefiting from additional organization or processing, while losing others that RAG already solves”; [b00033-e795bf84a9] “These quantities are reference-dependent, and throughout this work are defined relative to the naive RAG.”
- **Memory tax can arise during construction because restructuring and compression may remove or distort evidence, and after construction because preserved evidence can become harder to retrieve.**
  - Evidence: [b00038-65c93477cf] “Memory operations like restructuring and compression may discard or distort evidence before retrieval begins”; [b00042-e8b50baa00] “Some systems (MAGMA, LightMem) achieve gold-mem scores close to gold-raw-turn scores, yet far above their original, suggesting the preserved evidence may become harder to access.”
- **Many evaluated memory mechanisms add fragility when the construction or QA backbone changes.**
  - Evidence: [b00049-47f0c3abec] “changing the QA backbone causes larger performance variation than naive RAG for many systems”; [b00049-47f0c3abec] “many memory mechanisms can introduce additional fragility beyond the raw-history retrieval”
- **The benefit–tax pattern is not confined to conversational memory; the authors report analogous mixed outcomes in experiential and world-model settings.**
  - Evidence: [b00061-b835ed74b4] “memory tax also emerges in experiential memory, but its magnitude depends strongly on the task settings.”; [b00064-3e5ceb7e38] “latent- or cache-based memories do not consistently outperform this simpler alternative.”

## Results

- **Across the main comparison, two-round RAG scored 72.2, 81.4, and 90.0 on LongMemEval-s across the three backbones. Every listed memory method was below it in those columns; deficits ranged from −1.2 to −40.4 points.**
  - Context: This is the strongest controlled evidence for negative net value in the retrieval-friendly main benchmark. It does not imply that every memory method loses on every benchmark: the same table contains a few positive cells on PersonaMem-v2 and MINT-Eval.
  - Evidence: [b00017-48d0d2de18] “RAG (2rd) 72.2 81.4 90.0 36.2 48.7 48.4 26.1 33.1 34.5”; [b00017-48d0d2de18] “OpenViking 31.8 (−40.4) 58.8 (−22.6) 63.0 (−27.0)”; [b00017-48d0d2de18] “Mem-T 71.0 (−1.2) 75.0 (−6.4) 78.0 (−12.0)”
- **The main table also shows consequential exceptions: MemOS exceeded two-round RAG on PersonaMem-v2 by +1.0 and +1.5 with two Qwen backbones, while PlugMem and Mem-T exceeded it on MINT-Eval with GPT-5.6 Luna by +3.3 and +3.9.**
  - Context: These exceptions support the paper’s dual-edged account: memory is not uniformly harmful, and aggregate comparisons conceal query- and task-dependent benefit.
  - Evidence: [b00017-48d0d2de18] “MemOS 62.0 (−10.2) 76.6 (−4.8) 78.0 (−12.0) 37.2 (+1.0) 50.2 (+1.5)”; [b00017-48d0d2de18] “PlugMem 68.0 (−4.2) 75.8 (−5.6) 70.0 (−20.0) 35.0 (−1.2) 45.2 (−3.5) 39.8 (−8.6) 21.5 (−4.7) 33.3 (+0.1) 37.8 (+3.3)”; [b00017-48d0d2de18] “Mem-T 71.0 (−1.2) 75.0 (−6.4) 78.0 (−12.0) 32.1 (−4.1) 42.1 (−6.6) 41.0 (−7.4) 27.0 (+0.9) 30.4 (−2.7) 38.4 (+3.9)”
- **Human annotation found sharply different preservation behavior: MAGMA had 93.6% no loss and 0.0% no memory unit, whereas OpenViking had 39.4% no loss and 38.0% no memory unit.**
  - Context: This supplies direct evidence that construction loss varies substantially by system. However, the annotation pools sampled facts across three benchmarks, and the supplied table does not expose uncertainty intervals or per-benchmark breakdowns.
  - Evidence: [b00035-313653a178] “OpenViking 39.4 9.6 13.0 38.0”; [b00035-313653a178] “MAGMA 93.6 6.2 0.2 0.0”; [b00303-e32ba8b7c0] “we sample 500 raw turns from the corpus of three benchmarks and trace each to its corresponding memory unit(s)”
- **In experiential memory, gains depended on domain: Memp scored 76.1 versus naive RAG’s 73.1 on ALFWorld, but on AppWorld naive RAG scored 22.6 while Memp and ReasoningBank each scored 14.3. G-Memory reached 78.0 versus 69.0 for naive RAG on τ2-Bench.**
  - Context: The transfer experiment supports task dependence rather than a universal ranking. Token use also differs greatly, so score-only conclusions should be paired with the table’s resource columns.
  - Evidence: [b00331-c0f8bf12f1] “Naive RAG 73.1 234.8 22.7 38.4 36.8 8.8 45.3 9.6”; [b00331-c0f8bf12f1] “Memp 76.1 237.7 23.4 44.5 37.6 7.8 47.9 6.4”; [b00331-c0f8bf12f1] “Naive RAG 21.6 5.2 1† 22.6 339.6 20.0 69.0 394.5 14.3”; [b00331-c0f8bf12f1] “ReasoningBank 14.9 13.7 1† 14.3 383.7 22.1 51.0 381.8 15.0”; [b00331-c0f8bf12f1] “Memp 20.3 8.9 1† 14.3 317.1 20.9 62.0 396.2 14.6”; [b00331-c0f8bf12f1] “G-Memory 20.3 62.9 1† 22.6 388.7 21.0 78.0 424.3 13.8”
- **For world-model memory, naive-frame I3DM led all listed methods on Context-as-Memory with PSNR 19.8, SSIM .560, and 1 − LPIPS .704. On MemoBench it led PSNR and 1 − LPIPS at 14.4 and .476, while MagicWorld had the highest SSIM at .433 versus I3DM’s .430.**
  - Context: This supports the narrower claim that latent and cache memories do not consistently dominate direct past-frame retrieval. It is not a clean component ablation because the compared systems differ beyond memory carrier.
  - Evidence: [b00362-655ce32a35] “Method Mem Carrier PSNR ↑ SSIM ↑ 1 - LPIPS ↑”; [b00362-655ce32a35] “C-as-M-eval I3DM naive frames 19.8 .560 .704”; [b00362-655ce32a35] “MemoBench I3DM naive frames 14.4 .430 .476”; [b00362-655ce32a35] “MagicWorld visual latents 13.9 .433 .412”

## Experimental evaluation

### Datasets

- Main conversational-memory benchmarks: LongMemEval-s, PersonaMem-v2, and MINT-Eval. PersonaMem-v2 uses a stratified subset, as does MINT-Eval; the Luna evaluation also subsets LongMemEval-s.
  - Evidence: [b00022-763c147d34] “We evaluate on LongMemEval-s (Wu et al., 2025), PersonaMem-v2 (Jiang et al., 2025b), and MINT-Eval (Lee et al., 2026).”; [b00084-32e5c0a418] “20% of PersonaMem-v2, 10% of MINT-Eval, and 20% LongMemEval-s questions for GPT-5.6 Luna”
- Experiential-memory benchmarks span embodied tasks, web navigation, coding, and tool use: ALFWorld, WebShop, Mind2Web, BigCodeBench, AppWorld, and τ2-Bench.
  - Evidence: [b00060-7360836ecf] “covering embodied tasks (ALFWorld), web (WebShop, Mind2Web), coding (BigCodeBench) and tool use (AppWorld, τ2-Bench)”
- World-model evaluation uses Context-as-Memory and MemoBench; the supplied appendix states that only a subset of MemoBench is tested.
  - Evidence: [b00356-252538e279] “We use 60 samples from it.”; [b00357-9c5e12a085] “We test 25% of it, i.e., 90 samples.”

### Baselines

- Main memory systems: A-Mem, SimpleMem, MemOS, MemoryOS, LightMem, OpenViking, HippoRAG2, PlugMem, MAGMA, Mem-T, and Memory-R2; controls include No Context, Full Context, Gold Context, and one- and two-round RAG.
  - Evidence: [b00023-998cec78cb] “We use RAG over the raw corpus as the main memory-free baseline, with both single-round (1rd) and two-round (2rd) variants.”; [b00023-998cec78cb] “We also include several vanilla references, including No Context, Gold Context, etc.”
- Experiential-memory controls are a ReAct agent without memory and naive RAG over similar prior task trajectories; memory methods are Memp, ReasoningBank, G-Memory, and SkillPro.
  - Evidence: [b00060-7360836ecf] “We compare Memp (Fang et al., 2026b), ReasoningBank (Ouyang et al., 2026), G-Memory (Zhang et al., 2025a) and SkillPro (Mi et al., 2026)”; [b00060-7360836ecf] “against a ReAct agent without memory and a naive RAG baseline”
- World-model baselines compare naive frames, raw or learned key-value caches, visual latents, and memory tokens.
  - Evidence: [b00360-e34cf055d5] “I3DM (Li et al., 2026) retrieves the past frames most relevant to the current viewpoint”; [b00360-e34cf055d5] “HyDRA (Chen et al., 2026d) summarizes the history into a small set of memory tokens”

### Metrics

- Main performance metric: judge accuracy from a Qwen3.6-27B LLM judge; MCQ outputs are exactly parsed where possible.
  - Evidence: [b00201-02bad39f6c] “We score answers with an LLM-as-Judge backed by Qwen3.6-27B”; [b00201-02bad39f6c] “For MCQ, we match the parsed option exactly and send unparsable responses to the judge.”
- Reported system costs include total LLM tokens, normalized end-to-end time, number of LLM calls, and memory-store size.
  - Evidence: [b00024-59507577c7] “Alongside accuracy we report several cost metrics including token cost, end-to-end wall-clock time, number of LLM calls, and memory storage size.”
- Experiential tasks use each benchmark’s official metric; world models use PSNR, SSIM, and one minus LPIPS, with higher values preferred.
  - Evidence: [b00352-8606c5faca] “We follow each benchmark’s official metric: success rate for ALFWorld, task score for WebShop, step success rate for Mind2Web, pass@1 for BigCodeBench”; [b00356-252538e279] “report PSNR, SSIM and 1 − LPIPS, all higher is better.”

### Ablations

- RAG component ablations vary chunking, lexical versus dense versus hybrid retrieval, embedding model, and reranker while holding other settings fixed.
  - Evidence: [b00227-f7b3b3ac0e] “Ablations of the RAG baseline on chunking method, retrieval method, embedding model and reranker.”; [b00229-2347a495f4] “We vary one component at a time while keeping the rest at the default”
- Configuration-offset checks compare adjusted and repository-default retrieval depth and examine system-specific modifications for selected memories.
  - Evidence: [b00266-4d38099aef] “In most cases, we increase top-k beyond the repository defaults, which generally improves performance.”; [b00268-7549a217a7] “Beyond the shared settings and the retrieval scope, a few systems need individual changes:”
- Oracle-memory versus oracle-raw replay removes retrieval failure to separate construction loss from accessibility loss.
  - Evidence: [b00041-85c0c4d021] “Gold memory units remove retrieval failures, so the remaining memory tax reflects the losses introduced in memory construction”

### Negative results

- Most dedicated memories do not consistently beat the strong RAG reference in the main evaluation.
  - Evidence: [b00029-49cb9cdd22] “Overall, many memory systems fail to beat RAG in many cases”
- Simple retrieval remains competitive across RAG design variations, weakening the explanation that one lucky configuration created the result.
  - Evidence: [b00251-70ac739753] “naive RAG remains strong under a range of configurations”; [b00251-70ac739753] “Most variants stay within a few points of the default across settings.”
- Additional memory processing does not consistently improve experiential tool-use tasks or video consistency.
  - Evidence: [b00061-b835ed74b4] “for tool-use, several memory methods fall behind it”; [b00064-3e5ceb7e38] “latent- or cache-based memories do not consistently outperform this simpler alternative.”


## Limitations

- The evaluated memory methods are representative rather than exhaustive, and stronger system-specific tuning could change rankings.
  - Evidence: [b00084-32e5c0a418] “our baseline selection is representative rather than exhaustive.”; [b00084-32e5c0a418] “further system-specific tuning may yield better performance.”
- The main evidence is dominated by static, offline, English-language benchmarks, leaving multilingual and continuously updated deployments underexplored.
  - Evidence: [b00084-32e5c0a418] “Our benchmarks are primarily static, offline, and English-language”; [b00084-32e5c0a418] “leaving long-lived deployments with interleaved queries and multilingual interactions underexplored.”
- Cost constraints cause benchmark subsampling and exclude stronger frontier models, reducing precision and external validity.
  - Evidence: [b00084-32e5c0a418] “Our evaluation is limited by computational and API-calling cost.”; [b00084-32e5c0a418] “We do not include stronger frontier models beyond GPT-5.6 Luna (low)”
- Retrieval Scope is a useful normalization but does not equalize exact token budgets, and some systems receive exceptions because their stores contain few large units.
  - Evidence: [b00265-4e8426793c] “RS is not intended to equalize exact inference token budgets across systems”; [b00216-1a55b2e9c1] “The RS requirement has some exceptions.”
- Gold-memory mapping partly depends on model selection and is imperfect in spot checks, introducing measurement error into faithfulness and accessibility analyses.
  - Evidence: [b00295-f287ae7898] “the remaining systems require this LLM-based filtering.”; [b00298-0e8f4076c4] “Human spot check of LLM-selected gold memory units (%), labeled as correct, extraneous (irrelevant units are selected), or missing”
- The supplied world-model comparison changes whole systems, not only memory carriers, so causal attribution specifically to representation is limited.
  - Evidence: [b00360-e34cf055d5] “WorldKV (Yi et al., 2026) keeps the key-value cache of past frames as world memory, and retrieves and compresses the cached entries”; [b00360-e34cf055d5] “FramePack (Zhang et al., 2026e) packs the history into a fixed-length context of visual latents”

## Reproducibility

**Status:** partial

The paper is unusually detailed about operational choices and baseline adjustments, making conceptual reproduction plausible. Exact reproduction remains incomplete because the promised code/results are not part of the supplied record, some decisive analyses are figure-only, and uncertainty across stochastic or sampling variation is not quantified.

**Available artifacts**

- Detailed benchmark composition and sampling descriptions.
- Naive RAG chunking, hybrid retrieval, reranking, and second-round procedure.
- Backbone, embedding, reranker, decoding, and hardware settings.
- Definitions of accuracy, cost metrics, Retrieval Scope, oracle evidence, and iterative retrieval replay.
- Tables of principal scores, selected costs, configuration checks, and prompt-template locations.

**Missing pieces**

- The metadata promises future release of code and results, but no released artifact is supplied here.
- Several central diagnostic conclusions depend on figures whose underlying numerical values are absent from the supplied text blocks.
- The supplied prompt section names prompt tables but does not include the actual prompt contents.
- No random seeds, run-to-run variance, confidence intervals, or significance tests are stated in the supplied blocks.
- Complete executable environments, dependency versions, endpoint versions, and all processed evaluation subsets are not supplied.

## AIDB assessment

- Novelty: The main conceptual contribution is not a new memory architecture but an evaluation lens: measure constructed memory’s marginal value against direct retrieval and decompose per-query differences into benefit and tax. The faithfulness–accessibility–robustness diagnosis makes that lens more actionable.
- Usefulness: High for reviewers and system builders. It supplies a strong warning against reporting memory performance without a well-specified RAG control, encourages cost-aware evaluation, and identifies concrete failure channels. Adoption should be as an evaluation protocol and design heuristic, not as proof that memory construction is generally undesirable.
- Confidence: medium
- Recommended action: read
- Rationale: The central controlled comparisons are broad and practically consequential, and the paper includes useful baseline and configuration checks. Confidence stops short of high because benchmark subsampling, English offline tasks, configuration modifications, reference dependence, missing variance estimates, and incomplete released artifacts limit generalization and exact verification.

## Uncertainties

- **How much of the reported tax is specific to this relatively strong hybrid-and-reranked RAG reference?** — Benefit and tax are explicitly reference-dependent. A different retrieval budget, latency constraint, index, or online update regime could change both their magnitude and sign.
  - Evidence: [b00033-e795bf84a9] “These quantities are reference-dependent”; [b00189-b3cf478859] “BM25 and dense retrieval (Qwen3-Embedding-0.6B) independently return their top-k chunks.”
- **Whether score differences are statistically reliable is unresolved because the supplied material reports point estimates without confidence intervals or repeated-run variance.** — Several positive exceptions are small, and sampled benchmarks may amplify sampling noise. The absence of uncertainty estimates prevents a firm separation of stable effects from evaluation noise.
  - Evidence: [b00022-763c147d34] “Due to cost constraints, we evaluate 20% of PersonaMem-v2 and 10% of MINT-Eval.”; [b00016-0eaf1192b9] “Scores are judge accuracy (%).”
- **The effect of baseline-specific modifications is only partly isolated.** — Shared settings improve control but may remove capabilities tightly coupled to a system’s intended operation; selected offset checks do not establish optimality for every system.
  - Evidence: [b00263-d93c23a59d] “we standardize several evaluation components across baselines”; [b00268-7549a217a7] “a few systems need individual changes:”
- **The proposed recovery and recursive-memory design implications lack numerical evidence in the supplied blocks.** — The text claims consistent improvements, but without the referenced table values their effect size, cost, and robustness cannot be independently assessed from this record.
  - Evidence: [b00072-aaea8b93e3] “Results in Table show consistent improvements and reduction of memory tax across several memory systems.”; [b00073-a9153b50fb] “Results in Table also validate its effectiveness.”

## Open questions

- Do memory systems retain a net advantage under live, interleaved write–query workloads where raw-history indexing and retrieval must also be continuously maintained?
- How do benefit and tax vary by question type after controlling jointly for retrieval exposure, online latency, total tokens, and offline construction cost?
- Would system-specific tuning under a fixed compute budget reverse any of the principal rankings?
- How stable are the findings across repeated runs, alternative judges, human evaluation, and independently sampled benchmark subsets?
- Can a single controlled world-model architecture vary only the memory carrier while holding generator, training data, compute, and retrieval policy fixed?
- Does preserving source pointers eliminate construction loss without erasing the compression, privacy, and forgetting advantages that motivate structured memory?

## Proposed AIDB experiments

- **Hypothesis:** A hybrid memory with source-history fallback reduces query-level memory tax without eliminating memory benefit.
  - Baseline: Each memory system in its standard configuration, two-round raw-history RAG, and a token-budget-matched union that retrieves memory units and source chunks but does not jointly rerank them.
  - Primary metric: Paired per-query net value against two-round RAG, reported with memory-benefit rate, memory-tax rate, judge accuracy, total tokens, and online latency.
  - Stop condition: Stop after prespecified paired confidence intervals show either a reduction in tax with no loss of net accuracy under the same online token budget, or no practically meaningful improvement for all tested systems.
- **Hypothesis:** Observed memory tax grows mainly from construction loss on some systems and retrieval accessibility loss on others.
  - Baseline: Normal retrieval, oracle memory units, oracle raw turns, and source-linked memory units under identical QA prompts and backbones.
  - Primary metric: Accuracy gap from oracle raw turns to oracle memory units for construction loss, plus the gap from oracle memory units to normal retrieval for accessibility loss.
  - Stop condition: Stop when repeated samples yield stable system-level gap estimates with prespecified confidence widths, or when annotation disagreement prevents reliable separation of the two channels.
- **Hypothesis:** The ranking between constructed memory and raw-history RAG changes under realistic interleaved queries and multilingual updates.
  - Baseline: Best main-table memory systems versus one- and two-round RAG, all with identical cumulative storage, online token, and latency budgets.
  - Primary metric: Time-weighted task accuracy minus total operational cost, stratified by language, query type, history age, and update frequency.
  - Stop condition: Stop after the preregistered deployment horizon if rankings stabilize across strata, or earlier if one approach is dominated on both accuracy and cost in every consecutive evaluation window.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-11-20T08:53:05.103994+00:00`
- Document SHA-256: `53f6ca08485f6f243cf82e93db22264aec8ad5323bdcfc142841893d71e72e8b`
- Metadata SHA-256: `05251324f371399f614ed3c4cc362b814c12cd5b7bdb6a54b39af5b30c04ccb0`
- Blocks: 418
- Deterministic repair attempts: 0
