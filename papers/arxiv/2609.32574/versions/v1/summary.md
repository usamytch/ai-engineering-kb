# CUE-Mem: Benchmarking Long-Term User Memory via Implicit Cues in Multimodal Conversations

## Executive summary

CUE-Mem is a synthetic Chinese text-image-audio benchmark for memories implied by recurring peripheral objects and ambient sounds. Its controlled experiments convincingly expose three distinct bottlenecks: cue preservation during textualization, retrieval amid noisy histories, and evidence integration by the answer model. Detailed captions and separated background audio substantially improve implicit-memory accuracy, but increase token cost and can weaken refusal behavior. Native multimodal access helps one backbone and harms another; multimodal indexing raises recall while sharply reducing precision. The benchmark is useful for diagnosing memory pipelines, but its synthetic users, unpaired evidence conditions, multiple-choice format, narrow language coverage, and incomplete full-scale repeated runs limit claims about deployment behavior.

## Problem

**Statement.** Long-term assistants must recover user information that was never directly stated but is repeatedly implied by peripheral visual objects or non-speech sounds. Existing evaluations emphasize textual or foregrounded evidence and do not adequately isolate this failure mode.

**Why it matters.** A system that misses such evidence cannot personalize reliably, while a system that converts weak incidental cues into durable claims may over-infer sensitive facts. The paper therefore treats both successful memory use and refusal under insufficient evidence as necessary capabilities.

**Scope.** The study evaluates synthetic Chinese multi-session histories containing text, images, and voice messages. Implicit evidence is restricted to recurring peripheral visual objects and ambient non-speech audio; unstated information inferred from text alone is excluded.

## Method

The authors generate structured synthetic profiles, assign attributes to explicit or implicit evidence plans, distribute recurring cues across dated sessions, synthesize dialogue and media, and apply automatic plus human quality control. They then construct four-way questions for entity recall, longitudinal pattern aggregation, personalized recommendation, and refusal. Experiments compare textualized memory systems, caption and audio-textualization variants, and a controlled native-multimodal RAG matrix that independently varies index modality and evidence-use modality.

### Key components

- Operational evidence taxonomy: explicit targets are stated or foregrounded; implicit targets are unstated and carried by peripheral imagery or ambient non-speech sound.
- Three-stage construction: profile and event scripts, multimodal dialogue synthesis, then automatic and human review.
- Four tasks separate fact recovery, cross-session aggregation, application to recommendations, and calibrated refusal.
- Textualized evaluation compares full history, retrieval-based and structured memory systems against no-context and oracle-evidence controls.
- Cue-preservation interventions vary image-caption granularity and audio representation among speech-only, mixed-waveform hinting, and separate speech/background descriptions.
- Native evaluation crosses text versus multimodal indexing with text versus original-media evidence use, helping distinguish retrieval from evidence-integration failures.

### Assumptions

- Repeated synthetic cues constitute valid longitudinal evidence for a stable profile attribute.
- Multiple-choice accuracy is an adequate controlled proxy for memory recovery, aggregation, application, and refusal.
- Automatic similarity thresholds and unanimous human review sufficiently control leakage, recognizability, identity consistency, and answer support.
- Aggregate explicit and implicit conditions are comparable enough for EI-Gap analysis even though examples are not one-to-one counterparts.
- Oracle source text is a useful ceiling for question answerability after the target information has been cleanly preserved.

## Main claims

- **CUE-Mem specifically operationalizes implicit multimodal memory as recurring, unstated background evidence rather than ordinary semantic inference from explicit text.**
  - Evidence: [b00148-11b9ae12b7] “Implicit: the target is never stated and must instead be inferred from a peripheral visual object or an ambient, non-speech sound.”; [b00150-175d75e205] ““implicit” does not mean that the answer requires ordinary semantic inference from an explicit sentence.”
- **The benchmark spans four complementary memory capabilities and includes both explicit and implicit instances.**
  - Evidence: [b00053-d3ea0554fa] “CUE-Mem evaluates long-term user memory through four multiple-choice tasks: Entity Recall, Long Pattern, Personalized Recommendation, and Answer Refusal”; [b00053-d3ea0554fa] “Each task includes explicit and implicit instances.”
- **The main technical conclusion is that implicit-memory failure is distributed across preservation, retrieval, and evidence use rather than attributable to question answerability alone.**
  - Evidence: [b00102-079d1562b0] “Cue-aware textualization narrows this gap at growing token cost.”; [b00102-079d1562b0] “Native multimodal access preserves missing information, but gains depend on the backbone”; [b00102-079d1562b0] “multimodal indexing adds noise.”
- **The dataset underwent substantial automatic and human filtering, with agreement reported for three review dimensions.**
  - Evidence: [b00046-8731129ee3] “Together, these checks remove 42.80% of the initial samples.”; [b00048-6179b13a0d] “The average Fleiss’ κ across the three dimensions is 0.73.”; [b00048-6179b13a0d] “Human review removes an additional 22.10% of the remaining samples.”

## Results

- **Textualized systems remain far below clean oracle evidence: the best implicit Memory Avg. is 38.5 for Qwen3.6-35B-A3B and 41.9 for GPT-5.4-mini, versus 80.8 and 78.4 with Oracle Evidence.**
  - Context: This is the strongest evidence that answerability is not the sole bottleneck. Human readers of the full textualized histories score similarly on explicit and implicit samples, although that human comparison does not isolate retrieval from other human advantages.
  - Evidence: [b00086-069a8f538b] “The best implicit Memory Avg. reaches only 38.5 with Qwen3.6-35B-A3B and 41.9 with GPT-5.4-mini, compared with 80.8 and 78.4 for Oracle Evidence.”; [b00086-069a8f538b] “Humans reading full textualized histories achieve 83.2 and 82.8 on explicit and implicit samples”
- **Cue-aware textualization improves implicit memory without closing the gap: Detailed image captions move implicit Memory Avg. from 26.9 to 46.4 and EI-Gap from 35.9 to 27.1 points; audio splitting moves implicit Memory Avg. from 40.1 to 51.0 and EI-Gap from 29.4 to 19.4 points.**
  - Context: The controlled representation changes support a preservation bottleneck for peripheral image details and background sounds. The gains vary by task, so improved encoding is necessary but not sufficient.
  - Evidence: [b00093-083472e2f0] “Detailed image captions raise implicit Memory Avg. from 26.9 to 46.4 and reduce the EI-Gap from 35.9 to 27.1 points.”; [b00093-083472e2f0] “Audio splitting similarly raises implicit Memory Avg. from 40.1 to 51.0 and reduces the gap from 29.4 to 19.4 points.”
- **The image-preservation gain has a steep efficiency cost: retrieved input rises from 1.9k to 7.0k tokens per QA, while implicit accuracy rises from 53.3 to 62.2 and explicit accuracy from 70.9 to 72.4.**
  - Context: The asymmetry favors richer captions for implicit evidence, but the cost increase and smaller explicit gain argue for selective cue retention rather than uniformly verbose captioning.
  - Evidence: [b00095-b859dc136c] “increase retrieved input from 1.9k tokens per QA with Medium captions to 7.0k.”; [b00095-b859dc136c] “implicit accuracy rises from 53.3 to 62.2, while explicit accuracy increases only from 70.9 to 72.4.”
- **Native multimodal evidence use is backbone-dependent: with a fixed index it improves Qwen implicit Memory Avg. by 2.2 or 7.4 points, but reduces MiniCPM performance by 8.4 or 5.1 points.**
  - Context: This controlled index/use comparison rejects a general claim that restoring raw media automatically fixes textualization loss. The answer backbone must still interpret and integrate the localized evidence.
  - Evidence: [b00099-03960baf96] “MM-Use improves Qwen’s implicit Memory Avg. by 2.2 points with Text-Index and 7.4 points with MM-Index.”; [b00099-03960baf96] “For MiniCPM, it reduces performance by 8.4 and 5.1 points, respectively.”
- **Multimodal indexing recovers more implicit clues but introduces substantial noise: implicit Recall@25 is 29.7 versus 23.1, whereas implicit Precision@10 is 8.6 versus 16.2 for the text index.**
  - Context: This provides a retrieval-level mechanism for why multimodal indexing does not consistently improve end-task accuracy. The index surfaces weak cues but also expands distractor exposure.
  - Evidence: [b00353-51062cdfcc] “Its largest implicit-recall advantage is at k=25 (29.7 versus 23.1).”; [b00353-51062cdfcc] “implicit Precision@10 is 8.6 for the multimodal index versus 16.2 for the text index.”

## Experimental evaluation

### Datasets

- CUE-Mem: synthetic Chinese multi-session text-image-audio conversations for 20 users, containing 648 sessions, 5,798 turns, 496 images, 2,228 audio clips, and 2,674 QA pairs.
  - Evidence: [b00067-0274031f07] “CUE-Mem contains 20 synthetic users, 648 sessions, and 5,798 dialogue turns, including 496 images and 2,228 audio clips.”; [b00067-0274031f07] “The benchmark contains 2,674 QA pairs: 1,401 explicit and 1,273 implicit.”
- Profile seeds come from ALOE or PersonaHub; ambient-sound categories are derived from ESC-50 and FSD50K.
  - Evidence: [b00032-966bd71b56] “We initialize each synthetic user with a persona seed from ALOE (Wu et al. 2025) or PersonaHub (Ge et al. 2024).”; [b00034-bbb9667752] “we construct an ambient-sound seed pool from ESC-50 (Piczak 2015) and FSD50K (Fonseca et al. 2021).”

### Baselines

- No Context, Oracle Evidence, Full Memory, NaiveRAG, Generative Agents, Reflexion, MemGPT, A-Mem, MemoryOS, and human full-history/oracle conditions.
  - Evidence: [b00080-40a4f511d3] “Systems include Full Memory, NaiveRAG (Lewis et al. 2020), Generative Agents (Park et al. 2023), Reflexion (Shinn et al. 2023), MemGPT (Packer et al. 2023), A-Mem (Xu et al. 2025b), and MemoryOS (Kang et al. 2025).”; [b00078-618abef58e] “No Context omits the history, whereas Oracle Evidence supplies the source text prompts used to synthesize multimodal clues.”
- Textualized answer backbones are Qwen3.6-35B-A3B and GPT-5.4-mini; native multimodal backbones are Qwen3-Omni-30B-A3B-Instruct and MiniCPM-o-4.5.
  - Evidence: [b00082-64c3ccbe5b] “We use Qwen3.6-35B-A3B (Yang et al. 2025) and GPT-5.4-mini (Singh et al. 2025) for textualized memory”; [b00082-64c3ccbe5b] “Qwen3-Omni-30B-A3B-Instruct (Xu et al. 2025a) and MiniCPM-o-4.5 (Cui et al. 2026) for native multimodal memory”

### Metrics

- Accuracy by explicitness and task; EI-Gap is explicit accuracy minus implicit accuracy. Memory Avg. macro-averages Entity Recall, Long Pattern, and Personalized Recommendation, with Answer Refusal reported separately.
  - Evidence: [b00078-618abef58e] “We report accuracy under explicit and implicit evidence settings and define EI-Gap as Accexplicit−Accimplicit”; [b00078-618abef58e] “Memory Avg. averages Entity Recall, Long Pattern, and Personalized Recommendation; Answer Refusal measures calibration under insufficient evidence and is reported separately.”
- Retrieval evaluation reports Recall@k and Precision@k; statistical analysis uses percentage-point risk differences, bootstrap intervals, and Holm-adjusted p-values.
  - Evidence: [b00353-51062cdfcc] “Table 16 gives the complete Recall@k and Precision@k breakdown behind the RQ3 retrieval analysis.”; [b00322-b56d30d29a] “We report risk differences in percentage points as effect sizes, two-sided bootstrap-tail p-values, and Holm-adjusted p-values”

### Ablations

- Image textualization compares Brief, Medium, and Detailed captions that progressively preserve peripheral content.
  - Evidence: [b00092-292a5bb8e7] “GPT-5.4 generates Brief, Medium, and Detailed captions through prompts that increasingly emphasize peripheral details.”
- Audio textualization compares ASR, mixed-waveform Hint, and Split speech/background representations.
  - Evidence: [b00092-292a5bb8e7] “For audio, ASR uses Qwen3-ASR-1.7B (Shi et al. 2026); Hint uses Gemini 3.1 Pro to caption mixed speech and background audio; Split separates them”
- Native RAG uses a controlled matrix crossing Text-Index or MM-Index with Text-Use or MM-Use.
  - Evidence: [b00098-eb66027580] “We test native multimodal access during indexing and evidence use in our RAG-based system”; [b00307-f67ce71dcb] “Text-Index embeds one textualized dialogue round, including available image and audio captions.”; [b00307-f67ce71dcb] “MM-Use instead restores the original images and audio associated with the retrieved turn”

### Negative results

- Better cue preservation can harm refusal calibration: detailed image captions reduce implicit Answer Refusal by 16.9 points.
  - Evidence: [b00094-68f9043a72] “Meanwhile, implicit Answer Refusal drops by 16.9 points for images.”
- Native multimodal evidence use is not universally beneficial and reduces MiniCPM performance under both tested indices.
  - Evidence: [b00099-03960baf96] “For MiniCPM, it reduces performance by 8.4 and 5.1 points, respectively.”
- Multimodal indexing lowers implicit Memory Avg. for both native backbones under the tested settings.
  - Evidence: [b00101-c64ee7b7d6] “Holding evidence use fixed, MM-Index lowers implicit Memory Avg. for both backbones.”
- Cue recurrence was not causally ablated; no matched one-versus-many-occurrence evaluation was performed.
  - Evidence: [b00365-06ffdaa02a] “Recurrence count and temporal spacing were not independently randomized”; [b00365-06ffdaa02a] “no matched evaluation was run in which the same question was answered after one versus several occurrences.”


## Limitations

- The synthetic, deliberately stable histories may contain generation artifacts and do not test preference drift, contradictions, corrections, or long-term forgetting.
  - Evidence: [b00403-231abe18f8] “Its profiles, dialogues, images, and speech may contain generation artifacts, overly coherent personalities, or repeated visual and acoustic patterns”; [b00403-231abe18f8] “CUE-Mem does not evaluate preference drift, contradictory disclosures, corrections, or forgetting over longer interaction.”
- Coverage is narrow: 20 synthetic users, Chinese conversations, and only text, shared images, and voice messages with environmental audio.
  - Evidence: [b00405-93ed1cdb85] “CUE-Mem contains 20 synthetic users and Chinese multi-session conversations covering the six profile domains used in construction.”; [b00405-93ed1cdb85] “Its multimodal scope is text, shared images, and voice messages with environmental audio.”
- Explicit and implicit cues are not perceptually matched or paired counterfactuals, so EI-Gap is an aggregate condition difference rather than a clean per-example causal effect.
  - Evidence: [b00407-d81f408569] “These are modality-specific constructions, not perceptually matched difficulty levels.”; [b00407-d81f408569] “Explicit– implicit comparisons should therefore be interpreted at the aggregate condition level rather than as paired counterfactual effects.”
- Four-way multiple choice does not measure open-ended memory formation, revision, explanation, or abstention in conversation.
  - Evidence: [b00409-ccac906543] “All four tasks use four-way single-answer questions.”; [b00409-ccac906543] “does not measure how systems form, revise, explain, or abstain from memories in open-ended conversation.”
- The design space is not exhaustive: results depend on selected backbones, memory implementations, textualizers, embedding model, and retrieval cutoffs.
  - Evidence: [b00409-ccac906543] “Performance also depends on the evaluated answer backbones, seven memory systems, captioning granularities, audio textualizations, embedding model, and retrieval cutoffs.”; [b00409-ccac906543] “neither exhausts possible native multimodal memory designs.”
- Implicit-memory capability raises privacy and consent risks because incidental background information may be retained or profiled without active disclosure.
  - Evidence: [b00396-03ef7f2333] “Recurrence does not by itself make such an inference accurate or consented to.”; [b00396-03ef7f2333] “strong benchmark performance should not be treated as permission to retain or profile background information from real interactions.”

## Reproducibility

**Status:** partial

The package description is unusually detailed and includes checked-in configurations and end-to-end stages, but exact replication is blocked by missing caption-generation provenance, absent ASR decoding parameters, proprietary model-service dependencies, and incomplete repeated-run provenance. The reported robustness audit covers only a fixed subset rather than every full-scale configuration.

**Available artifacts**

- The metadata identifies an open-source repository and a dataset location.
- Programs are described for construction, synthesis, textualization, QA generation, clue verification, evaluation, retrieval analysis, token analysis, statistics, and table/figure generation.
- Experiment configurations record models, memory systems, textualization conditions, seeds, and expected input/output structure.
- Checkpointing and resume support are described for expensive stages.

**Missing pieces**

- The transferred full RQ1–RQ3 result trees contain only one identified artifact per configuration, not three complete independent runs.
- Distinct prompts and generation logs for Brief, Medium, and Detailed image captions are absent.
- The Qwen3-ASR decoding command and parameters are absent.
- Per-reason filtering counts were not preserved in the transferred snapshot.
- Reproduction requires machine-specific paths, API credentials, and access to corresponding model services.

## AIDB assessment

- Novelty: High as a benchmark contribution: it isolates recurring peripheral visual and acoustic cues, includes ambient audio, separates preservation, retrieval, and evidence-use interventions, and jointly evaluates memory use and refusal.
- Usefulness: High for diagnosing multimodal memory pipelines and testing selective cue retention. Lower for estimating real-world user benefit because histories are synthetic, questions are multiple choice, users are few, and the ethical acceptability of retaining incidental cues is outside benchmark accuracy.
- Confidence: high
- Recommended action: adopt
- Rationale: Adopt as a targeted diagnostic benchmark, not as a standalone deployment-readiness measure. The controlled comparisons, oracle conditions, retrieval metrics, human checks, and explicit negative results support actionable diagnosis. Any adoption should preserve separate reporting by task, evidence type, modality, token cost, and refusal behavior; a single aggregate score would conceal the principal trade-offs.

## Uncertainties

- **Whether the explicit–implicit gap reflects implicitness itself, unmatched perceptual difficulty, or differences in the independently constructed question sets.** — The paper supports an aggregate benchmark gap but not a per-example causal effect of converting the same memory from explicit to implicit evidence.
  - Evidence: [b00011-eb0beb8522] “The two conditions enable aggregate comparison, but individual examples are not constructed as one-to-one counterparts.”; [b00407-d81f408569] “These are modality-specific constructions, not perceptually matched difficulty levels.”
- **How stable the main results are across complete repeated full-scale runs.** — Most transferred configurations have one result artifact; the three-run audit is limited to fixed profiles, so system rankings and smaller effects may be less stable than the headline trends.
  - Evidence: [b00271-7fcc853b90] “the transferred RQ1–RQ3 result trees contain one result artifact per configuration rather than three independently identified runs.”; [b00409-ccac906543] “the repeated-run significance analysis uses a fixed five-profile sample”
- **Whether performance transfers to natural histories, other languages, cultures, cue distributions, or media types.** — Synthetic regularity and narrow coverage may make both cue recognition and distractor structure unlike deployment data.
  - Evidence: [b00405-93ed1cdb85] “Results therefore should not be assumed to transfer to other languages, cultural settings, cue distributions, or broader media settings without additional evaluation.”
- **Whether increasing recurrence causally improves memory accuracy.** — Recurrence is central to the benchmark definition, but its count and spacing are construction controls rather than randomized interventions.
  - Evidence: [b00365-06ffdaa02a] “These statistics characterize a construction control, not an accuracy ablation.”; [b00365-06ffdaa02a] “We therefore do not claim that the observed counts causally improve detection or aggregation.”
- **How often each diagnosed failure mode occurs.** — Selected examples localize plausible mechanisms but cannot establish their prevalence or relative importance across the benchmark.
  - Evidence: [b00382-96a615bf28] “We do not report frequencies for these categories because the cases below were selected for diagnosis rather than drawn as a frequency-estimation sample.”

## Open questions

- Can a matched counterfactual dataset express the same target memory with controlled explicit and implicit evidence while equalizing perceptual salience and question wording?
- Can selective captioning or event-triggered retention recover peripheral cues without the token growth and refusal degradation of uniformly detailed captions?
- Would temporal or entity-aware multimodal consolidation outperform independent item retrieval while maintaining precision?
- How do results change with natural, consented user histories containing drift, corrections, contradictions, and genuinely ambiguous cues?
- Can confidence calibration distinguish repeated but weak evidence from unsupported inference in open-ended responses?
- Do full-dataset repeated runs preserve the reported system ordering and backbone-dependent native-access effects?

## Proposed AIDB experiments

- **Hypothesis:** Selective cue extraction conditioned on recurrence and uncertainty matches uniformly Detailed captions on implicit-memory accuracy while reducing input cost and preserving refusal calibration.
  - Baseline: Uniform Detailed captions and the paper’s Medium-caption textualized RAG configuration.
  - Primary metric: Implicit Memory Avg. jointly reported with retrieved tokens per question and implicit Answer Refusal accuracy.
  - Stop condition: Stop if the selective method does not reach the Detailed-caption implicit Memory Avg., fails to reduce retrieved tokens by at least 30%, or lowers implicit Answer Refusal accuracy relative to Medium captions.
- **Hypothesis:** Entity- and event-linked multimodal consolidation improves implicit retrieval precision without sacrificing the recall advantage of multimodal indexing.
  - Baseline: The paper’s unified MM-Index with the same embedding backbone, query construction, and retrieval cutoff.
  - Primary metric: Implicit retrieval F1 at the fixed cutoff, with downstream implicit Memory Avg. as a required secondary check.
  - Stop condition: Stop if retrieval F1 does not improve on a held-out split or if downstream implicit Memory Avg. decreases under either native answer backbone.
- **Hypothesis:** Increasing independently spaced cue recurrence improves Long Pattern accuracy only up to a saturation point and may increase unsupported inference.
  - Baseline: Matched histories containing one target occurrence, with identical questions, distractors, total history length, and non-target content.
  - Primary metric: Long Pattern accuracy as a function of one, two, three, and five occurrences, accompanied by Answer Refusal false-claim rate.
  - Stop condition: Stop after confidence intervals show no practically meaningful gain across two successive recurrence levels, or if gains are accompanied by a larger increase in false claims on matched refusal items.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-10-16T14:20:12.931491+00:00`
- Document SHA-256: `093b9683f9c88fba9c1106cfb82238519e456d61be3e04664d00e9e0750970cd`
- Metadata SHA-256: `38fd3d845c73debfe414f2e5eb8dacb0b37e702da0127fa23185b2afcaf42f17`
- Blocks: 409
- Deterministic repair attempts: 0
