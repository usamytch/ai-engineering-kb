# Retrieved but Not Delivered: Multimodal Memory Delivery for Long-Term Agents

## Executive summary

The paper isolates “delivery,” the post-retrieval transformation of stored multimodal records into prompt content. Its strongest evidence is a paired MemLens decomposition: with gold messages fixed, retaining pixels improves accuracy far more than replacing ordinary retrieval with oracle retrieval. DeliverMem preserves pixels, adds readable image identities and temporal annotations, and pairs these with region-aware retrieval. It leads published memory-agent baselines on MemLens and DMV-Bench, but effects are sharply task- and backbone-dependent. The controls are unusually careful; nevertheless, only image memory is tested, some headline comparisons use published rather than paired runs, and the promised code and outputs were not yet available in the supplied record.

## Problem

**Statement.** Multimodal memory research usually optimizes storage and retrieval but does not isolate the interface that determines which parts of a retrieved record, and in which modality and structure, reach the answering model.

**Why it matters.** A record may be retrieved successfully while decisive visual information is withheld or made hard to address. Such failures can be misdiagnosed as retrieval or reasoning failures, directing optimization toward the wrong stage.

**Scope.** The paper studies image-based long-term agent memory on MemLens and DMV-Bench. It separates delivery from retrieval, evaluates original-modality preservation, item identity, temporal position and image-message binding, and adds one region-aware retrieval adapter. It does not experimentally establish transfer to audio, video or other modalities.

## Method

The authors formalize answering as a model conditioned on a delivered transformation of retrieved records. They estimate delivery and retrieval effects from paired conditions sharing questions, answering model, prompt template and judge. DeliverMem then modifies outgoing context without training: it retains original images, stamps each image with a readable tag referenced by the prompt, and attaches a timestamp or append ordinal. A separate retrieval adapter encodes each image globally and over an overlapping regional grid, scoring it by region MaxSim. Delivery components are evaluated against controls intended to preserve the delivered set, order and budget while changing one property.

### Key components

- D1, original-modality preservation: retrieved records retain their pixels rather than being reduced to textual proxies.
- D2, addressability: a short identifier is rendered into each delivered image and named in the accompanying prompt.
- D3, temporal position: each item receives the finest available store index, using dates on MemLens and append ordinals on DMV-Bench.
- R1, region multi-vector retrieval: whole-image and overlapping regional SigLIP 2 representations are combined using MaxSim.
- Paired controls include withheld, decoy, phase-randomized and spatially scrambled images; constant, shuffled, absent and text-only tags; permuted or absent dates; and shuffled image-message binding.

### Assumptions

- The benchmark judge is an adequate accuracy measure for MemLens; exact page selection is the appropriate success criterion for DMV-Bench.
- The oracle condition—gold messages padded or truncated to the fixed delivery budget—meaningfully represents retrieval at ceiling for that budget.
- Paired question-level sign tests on MemLens and chain-level permutation tests on DMV-Bench capture the relevant dependence structure.
- The chosen delivery budgets and prompt interface are representative enough to support conclusions about post-retrieval delivery.
- The original media and timestamps remain available in storage; D1–D3 cannot retrofit systems that discarded them during ingestion.

## Main claims

- **Delivery is a distinct accuracy-relevant stage between retrieval and answer generation because it determines which information in retrieved records is usable by the answering model.**
  - Evidence: [b00008-b557ad4078] “Retrieval decides which memories are accessible. Delivery decides which information in them is usable by the answering model.”
- **DeliverMem can retrofit a memory stack that retains original media and timestamps without training components or changing stored records.**
  - Evidence: [b00041-ce8e6bea42] “Because (D1)–(D3) train nothing and touch only the outgoing delivered context, they retrofit any stack that keeps the original media and their timestamps.”; [b00013-805e49247a] “Nothing is trained and no stored record is modified”
- **A delivery intervention can help only when the relevant information survives storage, is retrieved, is needed by the question and is not already conveyed by the context.**
  - Evidence: [b00009-3f97d6fc19] “a delivery decision helps where (i) the information survives storage and reaches the model, (ii) the question needs the property the decision supplies, and (iii) the delivered context does not already carry it”
- **The deployed system combines delivery changes with a retrieval-side adapter because delivery cannot recover an item that retrieval never returned.**
  - Evidence: [b00042-cea1c3c6ff] “Delivery cannot supply a fourth property: it cannot expose an item that retrieval never returned.”; [b00042-cea1c3c6ff] “A retrieval-side adapter, (R1), is paired with the interface to cover that gap.”

## Results

- **On MemLens’s non-refusal subset, fixing the retrieved set to gold messages and retaining pixels yielded 43.93 accuracy versus 30.06 with pixels withheld, a +13.87 delivery effect. Replacing ordinary retrieval with gold retrieval while retaining pixels yielded only +2.31 and was not statistically distinguishable from zero; the paired delivery contrast was significant.**
  - Context: This is the paper’s central controlled decomposition. It supports a larger delivery opportunity under this exact benchmark, budget, judge and backbone, but not a universal ranking of stages.
  - Evidence: [b00031-37e0b31ba0] “Gold messages (R⋆) 43.93 30.06 +13.87 31/7, 1.2×10−4”; [b00031-37e0b31ba0] “ΔR +2.31 +2.89 interaction −0.58 W/L, p 17/13, 0.58”
- **Across three Qwen3-VL backbones, delivery remained larger than retrieval: +13.87 versus +2.31, +15.61 versus +9.83, and +17.92 versus +11.56. The delivery-to-retrieval ratio narrowed from 6.00× to 1.59× and 1.55×, while the between-term gap was significant only on the smallest backbone.**
  - Context: The direction replicates across tested backbones, but the comparative advantage narrows and the larger-backbone differences lack significance at the reported sample size.
  - Evidence: [b00257-9e1696f02e] “8B dense Delivery +13.87 31/7 1.2×10−4 Retrieval +2.31 17/13 0.58”; [b00257-9e1696f02e] “30B-A3B Delivery +15.61 36/9 6.6×10−5 (MoE) Retrieval +9.83 21/4 9.1×10−4”; [b00257-9e1696f02e] “32B dense Delivery +17.92 32/1 7.9×10−9 Retrieval +11.56 26/6 5.4×10−4”; [b00257-9e1696f02e] “Ratio delivery : retrieval 8B 6.00× 30B-A3B 1.59× 32B 1.55×”; [b00038-dd994fa66e] “The gap between the two terms is significant at 8B (p=0.0078) and keeps its sign on the larger two without reaching significance at n=173 (p=0.18 and 0.14”
- **DeliverMem outperformed the best published MemLens memory agent at every released context length: scores were 51.28, 44.10, 42.05 and 38.97, with margins of +18.46, +12.82, +10.77 and +8.20. The reported full-context-to-delivered input ratios were 10.0×, 19.2×, 36.6× and 72.9×.**
  - Context: These are benchmark-level comparisons against the best published agent at each length, not uniformly same-batch paired reproductions. Refusal questions materially contribute to the largest headline margin.
  - Evidence: [b00055-8e682ee374] “DeliverMem 51.28 44.10 42.05 38.97 Margin over the best published agent +18.46 +12.82 +10.77 +8.20”; [b00055-8e682ee374] “Input ratio, full context to delivered 10.0× 19.2× 36.6× 72.9×”; [b00058-fb6b94e2ff] “Of the 36 questions behind the 32K margin, 19 are refusal questions”
- **On DMV-Bench, DeliverMem exceeded the published DualMem scores in all reported settings on both backbones, with margins ranging from +7.0 to +16.7 on Qwen2.5-VL-7B and from +10.6 to +23.5 on Gemini 2.5 Flash. Same-batch comparisons were also positive, but attribution differed: on Gemini at the heaviest setting, region retrieval had a +22.16 main effect while delivery had +0.46 and was non-significant.**
  - Context: This demonstrates system-level strength but also limits the broad delivery claim: the DMV-Bench gain can be primarily retrieval-driven and depends on the backbone’s failure mode.
  - Evidence: [b00057-afc6ec4b73] “Qwen2.5-VL-7B Gemini 2.5 Flash”; [b00057-afc6ec4b73] “Δ over previous best +7.0 +11.9 +14.3 +16.7 +10.6 +15.0 +18.2 +23.5”; [b00266-77756177a9] “The main effects are +22.16 for (R1), with all six chains agreeing in sign at the permutation floor p=0.031, and +0.46 for delivery at p=0.156.”
- **Component effects were specific rather than uniformly beneficial. Original image content contributed +11.56 on MemLens; accurate temporal position gained +13.92 on temporal questions; addressability gained +11.85 against a constant-tag control on DMV-Bench but only +0.51 on MemLens. The assembled tag-and-date change also harmed some question types.**
  - Context: The matched controls strengthen causal interpretation for individual interface properties, while the heterogeneous and adverse effects argue against treating every component as universally useful.
  - Evidence: [b00065-763cb925a0] “(D1) original modality pixel phase randomised MemLens question (173) +11.56 28/8, 0.0012”; [b00065-763cb925a0] “(D2) addressability∗ tags made identical DMV chain (10) +11.85 10 of 10, 0.002”; [b00065-763cb925a0] “(D2) addressability∗ tags made identical MemLens question (195) +0.51 4/3, 1.00”; [b00065-763cb925a0] “(D3) temporal position date values permuted MemLens question (194) +13.92 31/4, 3.5×10−6”; [b00286-6318e4ee43] “four lost on knowledge update (−13.79), two lost on information extraction (−3.28)”

## Experimental evaluation

### Datasets

- MemLens: a public benchmark of long multimodal conversations and evidence-supported questions at four released context lengths. The main evaluation uses its canonical question subset and separately analyzes the released question pool for per-type effects.
  - Evidence: [b00027-dfe140d0c0] “MemLens (Ren et al., 2026) pairs a long multimodal conversation with questions whose answers are supported by a small number of messages scattered through it, across four released context lengths.”; [b00027-dfe140d0c0] “We use the canonical 195-question subset”
- DMV-Bench: a public interactive visual-memory benchmark in which an agent must return to the product photograph containing a small visual cue absent from page text.
  - Evidence: [b00025-4adc287229] “one product photograph carries a small object that appears nowhere in the page text, and sessions later the agent must return to the product that carried it.”

### Baselines

- MemLens published memory agents: M2A, M3C, M3-Agent, Memory-T1, MemOS, Mem0 and MemAgent-7B; the strongest system varies across context lengths. Direct long-context LVLMs are reported separately as cost–accuracy references.
  - Evidence: [b00155-5da0271b68] “Every one of the seven published memory agents runs on a backbone of 8B parameters or fewer”; [b00159-e4c837a57f] “These models take the whole conversation as input, at more than ten times the inference cost”
- DMV-Bench baselines include NoMemory, TextOnly, Caption, benchmark reimplementations of WorldMM, MMA and M2A, and DualMem as the strongest published comparator.
  - Evidence: [b00056-006966abd5] “The upper block is the benchmark’s own pool, with NoMemory, TextOnly and Caption as its baselines and the -lite rows as its re-implementations of published systems.”; [b00153-066291bb6f] “DualMem is the strongest published system in all eight DMV-Bench cells”

### Metrics

- MemLens accuracy is determined by the benchmark’s Qwen3-VL-family judge; SubEM is used in supporting analyses and configuration selection.
  - Evidence: [b00027-dfe140d0c0] “an 8B backbone and the benchmark’s own 235B judge, both from the Qwen3-VL family”; [b00201-482e1cc202] “with SubEM as the objective”
- DMV-Bench uses exact task success: whether the agent opens the correct product page.
  - Evidence: [b00025-4adc287229] “Scoring is exact, with no judge model.”; [b00087-060d88aaa9] “DMV-Bench is scored exactly, by whether the agent opens the correct product page.”
- MemLens paired comparisons use an exact two-sided sign test; DMV-Bench paired runs use exact cluster permutation over independent chains.
  - Evidence: [b00029-913407ddd3] “We use an exact two-sided sign test on discordant pairs.”; [b00060-7d21945334] “The test is an exact cluster permutation (Good, 2005) over all 2m sign assignments for m chains”

### Ablations

- Pixel delivery is compared with pixels withheld under both oracle and ordinary retrieval, producing a factorial separation of delivery, retrieval and their interaction.
  - Evidence: [b00030-9ea12c3da7] “Rows vary what is retrieved and columns whether the retrieved items keep their pixels”
- Counterfactual images separate content from mere image-token presence using spatial scrambling, decoy photographs and phase randomization.
  - Evidence: [b00226-77156a6c34] “Each counterfactual condition delivers an identical set of image slots and differs only in what the pixels carry.”
- Addressability controls shuffle tag-to-item mappings, make tags identical, remove tags, or move tags from pixels to text.
  - Evidence: [b00065-763cb925a0] “(D2) addressability tag in text, pixels intact DMV chain (10) +7.89 9 of 10, 0.0039”
- Temporal specificity is tested against value-preserving date permutations and against no date; image-message binding is tested by permuting only their pairing.
  - Evidence: [b00178-ceee2c23cb] “The binding control fixes the stamps, dates, text, order and image set and permutes only which image follows which message.”; [b00283-21ae48c661] “accurate dates improve on no date by 8.76 points on the 194 temporal questions”
- Delivery budget is swept on MemLens while other headline experiments fix the selected-message count.
  - Evidence: [b00274-60620b966f] “Sweeping it (benchmark judge, 32K) gives 40.00 at K=3, 46.67 at K=5, 51.28 at K=10 and 51.28 at K=20.”

### Negative results

- A real but irrelevant photograph performed identically to no photograph, indicating that image tokens or visual-pathway activation alone did not explain the gain.
  - Evidence: [b00229-efe793b669] “A real but wrong photograph scores exactly what no photograph scores, +0.00 with 6 questions moving each way and p=1.00.”
- Perfect retrieval was non-significant in the central MemLens decomposition despite much greater gold-message coverage.
  - Evidence: [b00035-03bf8254ba] “Five times the evidence coverage buys only +2.31.”; [b00031-37e0b31ba0] “W/L, p 17/13, 0.58”
- Addressability was null on MemLens under the constant-tag comparison.
  - Evidence: [b00070-72c38d39f5] “On MemLens that contrast is half a point”
- Region retrieval was null on MemLens despite being strongly useful on DMV-Bench.
  - Evidence: [b00074-0b5005febe] “null on MemLens, where replacing the default index with the region index moves the same condition by −1.03 (4/6, p=0.75”
- Delivery was null on Gemini 2.5 Flash in DMV-Bench’s factorial decomposition.
  - Evidence: [b00266-77756177a9] “delivery alone by +0.31”; [b00266-77756177a9] “+0.46 for delivery at p=0.156”
- Increasing the MemLens delivery budget beyond the selected operating point produced no additional judged accuracy.
  - Evidence: [b00274-60620b966f] “going from ten to twenty changes the judge score by exactly zero.”


## Limitations

- The experiments cover only images; claims about audio, video or modality-general delivery remain conceptual extrapolations.
  - Evidence: [b00077-b1ff07073e] “Every measurement is on the image modality”; [b00180-5fed334982] “Every number in this paper is measured with images as the original modality.”
- The study does not measure delivery granularity—crop, whole frame or both—so it cannot determine the best media unit to deliver.
  - Evidence: [b00077-b1ff07073e] “Delivery granularity, whether to send a crop, the whole frame, or both, is a degree of freedom we do not measure.”
- Some per-type analyses use the full released question pool rather than the canonical evaluation subset because important categories are small in the latter.
  - Evidence: [b00077-b1ff07073e] “Per-type effects are measured on the full 789 released questions, since the 195-question evaluation subset contains only 29 knowledge-update questions”
- Several headline comparisons use transcribed published scores, for which paired significance tests are unavailable; same-batch reproductions use a different opponent run and estimate.
  - Evidence: [b00060-7d21945334] “a published figure admits no paired test.”; [b00060-7d21945334] “The margins below differ from Table 3’s because both the estimate and the opponent’s run differ.”
- Run-to-run variation creates small discrepancies across tables, and some contrasts combine conditions from separate runs or batches.
  - Evidence: [b00302-cdc942c7d3] “Across runs only paired differences compare, and a condition scored in two runs agrees with itself to about one question.”
- The method exposes more raw imagery to the answering model, increasing privacy exposure relative to caption-only delivery.
  - Evidence: [b00084-1882c3534c] “a memory system built this way places more raw imagery in front of the answering model than a captioning system does.”
- DeliverMem requires retained original media and cannot compensate for records discarded during ingestion or never retrieved.
  - Evidence: [b00041-ce8e6bea42] “they retrofit any stack that keeps the original media and their timestamps.”; [b00042-cea1c3c6ff] “it cannot expose an item that retrieval never returned.”

## Reproducibility

**Status:** partial

The experimental design is documented in substantial detail and many contrasts could be audited from the promised outputs. However, the wording is future tense—code “will be released”—and those artifacts are absent from the supplied material. End-to-end reproduction also depends on external benchmark harnesses and hosted APIs, so the current evidence supports only partial reproducibility.

**Available artifacts**

- A project-page URL is provided in the supplied abstract.
- The paper states that prompts and condition definitions are documented in the appendices.
- Runtime environment, model interfaces, encoders, benchmark harness requirements and statistical tests are specified.
- The authors promise per-question scores, per-probe outcomes and traces sufficient to recompute paired contrasts.

**Missing pieces**

- The supplied record does not include the promised released code.
- The supplied record does not include per-question or per-probe outputs, agent traces, configuration files or executable scripts.
- Benchmark data and harnesses are explicitly not redistributed.
- Hosted model APIs and judge versions may not remain stable or independently accessible.
- No license information is supplied in the metadata.

## AIDB assessment

- Novelty: High conceptual novelty within the supplied literature framing: the paper turns prompt assembly after retrieval into an independently measurable multimodal-memory stage and uses matched controls to distinguish content, identity, time and binding from rendering confounds.
- Usefulness: High for builders of multimodal memory agents that preserve original media. The interface changes are training-free and the diagnostic decomposition can identify whether retrieval, presentation or item selection is limiting performance. Utility is narrower for text-only stores, privacy-constrained deployments and modalities not evaluated here.
- Confidence: medium
- Recommended action: read
- Rationale: The central paired decomposition and component controls are strong enough to merit close reading and replication. Adoption should wait for released artifacts and validation on independent benchmarks, backbones, modalities and privacy-aware deployments. The strongest qualification is heterogeneity: delivery dominates MemLens under the reported protocol, but DMV-Bench on one backbone is overwhelmingly retrieval-limited, and assembled components can harm some question types.

## Uncertainties

- **It is unclear whether delivery remains the larger bottleneck on independently constructed benchmarks rather than the two evaluated suites.** — Benchmark structure determines whether evidence is already retrieved, whether questions require pixels, and whether tags or dates supply missing information. These factors directly govern the measured effect.
  - Evidence: [b00074-0b5005febe] “whether a component transfers does not follow from the stage it acts on.”
- **The relative importance of delivery and retrieval may depend strongly on the answering backbone rather than generalize at the benchmark level.** — A deployment could optimize the wrong stage if conclusions from one backbone are transferred directly to another.
  - Evidence: [b00267-3d54633a6c] “Which stage pays depends on what the backbone fails at rather than on the benchmark alone.”
- **The causal interpretation of some cross-run contrasts may be sensitive to model or judge nondeterminism.** — Small component effects and differences of a few questions could change sign or significance when conditions are not scored in one batch.
  - Evidence: [b00302-cdc942c7d3] “a condition scored in two runs agrees with itself to about one question.”
- **The balance among accuracy, inference cost, retrieval-index cost and privacy risk is unresolved for real deployments.** — The reported input-token savings omit offline indexing work, while retaining and re-showing raw images expands model access to personal media.
  - Evidence: [b00276-1bbe35e915] “The ratio counts only what reaches the answering model, leaving out the offline work behind it”; [b00084-1882c3534c] “Where the stored media are personal, that widens what the model sees”

## Open questions

- Do the delivery effects replicate with independently implemented prompts, retrievers and judges rather than the authors’ pipeline?
- How should an agent choose between a crop, a full frame and both when evidence has region annotations?
- Can content-preserving delivery work for audio and video while controlling duration, temporal alignment and cross-modal binding?
- Would a privacy-filtered or selectively redacted delivery policy retain the accuracy gains of raw-pixel delivery?
- Why does the assembled configuration harm knowledge-update and some information-extraction questions, and can routing avoid those losses without relying on benchmark-provided question types?
- How stable are the results under repeated API calls, alternative judge models and non-Qwen open backbones?

## Proposed AIDB experiments

- **Hypothesis:** Original-modality delivery improves accuracy only when the requested fact is visually grounded, and does not improve matched text-supported questions.
  - Baseline: For a new benchmark with paired visually supported and text-supported questions over the same retrieved records, compare gold-set delivery with original images against identical delivery with pixels withheld and against phase-randomized images.
  - Primary metric: Paired accuracy difference and the interaction between delivery condition and evidence type, with confidence intervals and multiplicity-corrected tests.
  - Stop condition: Stop after the preregistered sample provides enough discordant pairs for the target power; reject broad transfer if the interaction is absent or the visual subset fails to improve over both controls.
- **Hypothesis:** Adaptive component routing preserves DeliverMem’s useful effects while eliminating losses on question types that do not need tags, dates or region retrieval.
  - Baseline: Compare the fixed DeliverMem configuration with a no-component baseline and a router trained only on a disjoint development split without benchmark-provided question labels.
  - Primary metric: Held-out macro accuracy across question types, accompanied by worst-type accuracy and the fraction of queries using each component.
  - Stop condition: Stop if the router fails to exceed the fixed configuration on macro accuracy or reduces any preregistered question type beyond the allowed non-inferiority margin.
- **Hypothesis:** Privacy-filtered visual delivery retains most of the original-pixel benefit while exposing less sensitive image content.
  - Baseline: Compare raw-pixel delivery, caption-only delivery, and automatically redacted or cropped delivery under an identical oracle retrieved set and prompt structure.
  - Primary metric: Accuracy versus a preregistered privacy-exposure score based on retained sensitive regions, reported as a Pareto frontier.
  - Stop condition: Stop if no filtered condition improves accuracy over caption-only delivery while meeting the privacy threshold, or if it cannot retain the preregistered fraction of raw-pixel accuracy gain.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-10-16T14:31:51.406672+00:00`
- Document SHA-256: `bb0636b9b821f7d4634574bfe096eca7b73564763f15974a149cb12b51835ac9`
- Metadata SHA-256: `92c8161ad7f9dece3aa9075681fb9de6902529651a810575ebecb0ca05cf559d`
- Blocks: 318
- Deterministic repair attempts: 0
