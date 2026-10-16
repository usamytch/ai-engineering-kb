# Beyond Retrieval Failure: Understanding Why LLMs Miss Evidence in Multi-Hop RAG

## Executive summary

The paper introduces ExecutionRAG, a training-free requirement register for keeping unresolved sub-questions and their evidence explicit during multi-hop retrieval. Its strongest contribution is diagnostic: with the retriever, corpus, and generator held fixed, recovered gold passages demonstrate that some apparent retrieval failures arose from search guidance rather than evidence access. The controlled MuSiQue analysis shows a large reduction in missing-evidence failures, but only a modest improvement in total answer accuracy because premature resolution and abstention grow. The evidence supports the bottleneck-shift thesis, although asymmetric failure labeling, incomplete gold-paragraph matching, stochastic generation, and absent released code or run artifacts limit causal precision and reproducibility.

## Problem

**Statement.** Standard evaluation labels a wrong answer with an unretrieved required passage as a retrieval failure, although the passage may either be unreachable by the fixed retriever or reachable but never requested because the search drifted away from an unresolved sub-question.

**Why it matters.** Conflating access failure with search drift can direct research toward better indexes or embeddings when the actual defect is loss of intermediate requirements. It also hides a later-stage problem: retrieved evidence may still be judged insufficiently or synthesized incorrectly.

**Scope.** The study addresses multi-hop question answering with iterative RAG. The core controlled failure analysis is on MuSiQue; answer-level evaluation additionally covers HotpotQA and 2WikiMultiHopQA, using GPT-4o-mini and two embedding backbones.

## Method

ExecutionRAG adds an explicit requirement register without changing the retriever, corpus, tool interface, or generator. A seed retrieval grounds an initial list of concrete sub-questions. Each entry stores a status, evidence note, and supporting passages. Iterative retrieval selects an open item, composes a query from the original question, that item, and its evidence note, then updates only affected entries. The system answers when no item remains open or emits a bounded answer when its budget is exhausted. Deterministic bookkeeping prevents silent deletion of open requirements and preserves accumulated evidence.

### Key components

- Seed-grounded initialization from the question and an initial semantic retrieval.
- Four-state requirements: pending, active, resolved, and retired.
- Item-directed query construction using the global question, active requirement, and current evidence note.
- Iterative register updates after retrieval, with explicit resolution and retirement events.
- Progress-delta injection rather than replaying the entire register after every step.
- Deterministic preservation of requirements and append-only supporting evidence.
- A stopping rule tied to register clearance, plus budget-aware forced answering.
- Controlled attribution through a matched A-RAG comparison with the same generator, tools, corpora, and retriever.

### Assumptions

- MuSiQue supporting paragraphs approximate the minimal evidence required for a correct answer.
- A recovered gold passage under a fixed retriever and corpus certifies reachability for that passage, but failure to recover it does not certify unreachability.
- The matched A-RAG condition isolates the requirement register closely enough to attribute observed differences primarily to search guidance and bookkeeping.
- Contain-Match and the LLM judge together provide useful, though imperfect, answer-quality measurements.
- A 40-character fingerprint correctly maps matched supporting paragraphs to corpus chunks; unmatched paragraphs remain outside evidence-recall measurement.
- The language model's register-resolution decision is observable but not necessarily correct.

## Main claims

- **The paper separates apparent retrieval failure into unreachable evidence and reachable evidence that the agent never requested; recovery under fixed retrieval certifies the latter for an individual passage.**
  - Evidence: [b00024-d38de586bf] “If an intervention leaves R and 𝒦 untouched and the needed passage is nonetheless retrieved, then a query returning it existed, so that failure was unasked. Recovering evidence certifies reachability; failing to recover it proves nothing.”
- **ExecutionRAG is a training-free intervention that changes search guidance while leaving evidence access and generator parameters unchanged.**
  - Evidence: [b00016-80bf422f2e] “We introduce ExecutionRAG, a training-free requirement register that provides the controlled intervention. It tracks unresolved sub-questions and their supporting passages while leaving the retriever, corpus, and generation-model parameters unchanged.”
- **The register makes requirement-resolution decisions explicit and therefore permits post-hoc comparison against gold evidence for premature resolution.**
  - Evidence: [b00036-47f58f3879] “Recording this decision as an event, rather than leaving it implicit in free-form reasoning, allows us to compare it with gold evidence and determine whether it was premature.”
- **The central empirical claim is a bottleneck shift: better search guidance recovers evidence, while evidence verification and answer commitment become more prominent residual problems.**
  - Evidence: [b00094-3ec11840a5] “This redistribution is the central result: once search guidance recovers more required evidence, evidence verification and answer commitment become the dominant sources of the remaining error.”
- **Seed grounding and iterative register updates both contribute to performance.**
  - Evidence: [b00122-7ae81a1aba] “Both seed grounding and iterative updates contribute to the observed gain.”

## Results

- **On MuSiQue with all-MiniLM-L6-v2, missing-evidence failures fall from 382 for A-RAG to 234 for ExecutionRAG, corresponding to 69.3% of 551 baseline failures versus 43.9% of 533 ExecutionRAG failures.**
  - Context: This is the matched, fixed-retriever comparison underlying the paper's search-drift diagnosis.
  - Evidence: [b00093-e5f84baeeb] “With all-MiniLM-L6-v2, the count decreases from 382 for A-RAG to 234 for ExecutionRAG; these values represent 69.3% of 551 baseline failures and 43.9% of 533 ExecutionRAG failures.”
- **With Qwen3-Embedding-0.6B on MuSiQue, missing-evidence failures decrease from 383 to 274, or from 66.4% of 577 failures to 47.9% of 572 failures.**
  - Context: The reduction persists under the alternative embedding backbone, supporting robustness to retriever choice within the tested configurations.
  - Evidence: [b00093-e5f84baeeb] “With Qwen3-Embedding-0.6B, the count decreases from 383 to 274, or from 66.4% of 577 failures to 47.9% of 572 failures.”
- **Evidence recovery does not translate proportionally into total-error reduction: reasoning errors rise from 9% to 26% with MiniLM and from 8% to 21% with Qwen, abstentions rise from 7% to 13% and from 12% to 17%, and MuSiQue LLM-Evaluation Accuracy rises from 44.9 to 50.2 against A-RAG.**
  - Context: The error redistribution supports the paper's bottleneck-shift interpretation, but part of the apparent increase in reasoning errors may come from improved observability in ExecutionRAG.
  - Evidence: [b00094-3ec11840a5] “Reasoning errors after retrieval increase from 9% to 26% with MiniLM and from 8% to 21% with Qwen”; [b00094-3ec11840a5] “Abstentions also increase, from 7% to 13% and from 12% to 17%, respectively.”; [b00094-3ec11840a5] “Against A-RAG, LLM-Evaluation Accuracy on MuSiQue rises from 44.9 to 50.2”
- **Under Qwen3-Embedding-0.6B, ExecutionRAG obtains LLM-Evaluation Accuracy of 80.0, 68.3, and 42.8 on HotpotQA, 2Wiki, and MuSiQue, versus 76.4, 55.2, and 42.3 for A-RAG; the reported gains are +13.1 on 2Wiki and +0.5 on MuSiQue.**
  - Context: The largest answer-level improvement is concentrated on 2Wiki, while the MuSiQue improvement under this backbone is small.
  - Evidence: [b00104-e8faa65514] “ExecutionRAG outperforms A-RAG on all three benchmarks: 80.0, 68.3, and 42.8 LLM-Evaluation Accuracy on HotpotQA, 2Wiki, and MuSiQue, respectively, compared with 76.4, 55.2, and 42.3 for A-RAG. The largest gain remains on 2Wiki (+13.1), while MuSiQue shows a smaller positive gain (+0.5).”
- **In the default MuSiQue ablation, full ExecutionRAG reaches 50.2 LLM-Acc; removing seed-grounded initialization lowers it to 48.7, and removing iterative progress-register updates lowers it to 48.3.**
  - Context: The component study indicates that both initialization from seed evidence and repeated state updates matter, although it does not isolate every bookkeeping feature.
  - Evidence: [b00122-7ae81a1aba] “Building the register from the question alone rather than from seed evidence lowers LLM-Acc from 50.2 to 48.7, indicating that grounding requirements in retrievable evidence is beneficial. Removing iterative updates and constructing the register only once lowers LLM-Acc further to 48.3.”
- **The register increases retrieval cost on MuSiQue and HotpotQA but not retrieved-token volume on 2Wiki: 7,161 versus 5,015 tokens per MuSiQue question, 3,373 versus 2,860 on HotpotQA, and 3,966 versus 3,992 on 2Wiki.**
  - Context: This weakens a pure 'more retrieved text' explanation for the large 2Wiki gain, while showing a material efficiency cost on the other datasets.
  - Evidence: [b00118-09440b4077] “On MuSiQue, it reads 7,161 retrieved tokens per question, compared with 5,015 for A-RAG; on HotpotQA, it reads 3,373 compared with 2,860. On 2Wiki, token use is comparable at 3,966 and 3,992, respectively.”

## Experimental evaluation

### Datasets

- HotpotQA: a full 1,000-question sample from the official validation set, using the HippoRAG retrieval corpus.
  - Evidence: [b00222-8f69a2a4f3] “We follow the HippoRAG evaluation protocol, using the same retrieval corpora and the same 1,000-question splits sampled from the official validation sets of HotpotQA, 2WikiMultiHopQA, and MuSiQue.”
- 2WikiMultiHopQA: a full 1,000-question sample from the official validation set, using the HippoRAG retrieval corpus.
  - Evidence: [b00222-8f69a2a4f3] “We follow the HippoRAG evaluation protocol, using the same retrieval corpora and the same 1,000-question splits sampled from the official validation sets of HotpotQA, 2WikiMultiHopQA, and MuSiQue.”
- MuSiQue: a full 1,000-question sample from the official validation set; also the dataset used for the detailed failure analysis and ablations.
  - Evidence: [b00088-c9060ddbd6] “All main results use the full 1,000-question evaluation sets. The ablation study is conducted on the full 1,000-question MuSiQue evaluation set.”

### Baselines

- Direct inference: GPT-4o-mini without retrieval.
  - Evidence: [b00084-23029e8629] “(1) Direct inference: GPT-4o-mini without retrieval;”
- Vanilla RAG: top-k retrieval, CoT-augmented retrieval, and IRCoT.
  - Evidence: [b00084-23029e8629] “(2) Vanilla RAG: top-k retrieval with k∈{3,5,10}, CoT-augmented retrieval, and IRCoT (Trivedi et al., 2023);”
- Structured and agentic RAG: KGP, G-Retriever, RAPTOR, LightRAG, HippoRAG, HippoRAG 2, GFM-RAG, LinearRAG, LAG, and A-RAG.
  - Evidence: [b00084-23029e8629] “(3) Structured and agentic RAG: KGP (Wang et al., 2024), G-Retriever (He et al., 2024), RAPTOR (Sarthi et al., 2024b), LightRAG (Guo et al., 2025), HippoRAG and HippoRAG 2 (Gutiérrez et al., 2024; Gutiérrez et al., 2025a), GFM-RAG (Luo et al., 2025), LinearRAG (Zhuang et al., 2025), LAG (Xiao et al., 2025), and A-RAG (Du et al., 2026).”
- A-RAG is the matched baseline: it shares the generator, retrieval tools, and corpora, and differs by lacking the requirement register.
  - Evidence: [b00110-0c0ede00e0] “A-RAG is the matched baseline for the failure analysis. It uses the same generation model, retrieval tools, and corpora as ExecutionRAG; the requirement register is the added component.”

### Metrics

- Contain-Match Accuracy: checks whether the gold answer occurs as a substring of the prediction.
  - Evidence: [b00086-bdc868fab7] “Contain-Match Accuracy, which checks whether the gold answer appears as a substring of the prediction”
- LLM-Evaluation Accuracy: an LLM judge assesses semantic equivalence.
  - Evidence: [b00086-bdc868fab7] “LLM-Evaluation Accuracy, which uses an LLM judge to assess semantic equivalence.”
- Missing-evidence failure count and within-method share among wrong answers.
  - Evidence: [b00090-9c8acc2792] “We measure the controlled reduction described in Section 2.2 by assigning each wrong answer on MuSiQue a single cause using the gold supporting paragraphs.”
- Exclusive error categories in priority order: judge error, gave up, reasoning error, and missing evidence.
  - Evidence: [b00092-3f4ca32ed3] “Each wrong answer receives exactly one cause, assigned by a fixed priority order so the categories cannot overlap: judge error”; [b00092-3f4ca32ed3] “gave up (the answer explicitly abstains), reasoning error”; [b00092-3f4ca32ed3] “and missing evidence (a supporting passage was never retrieved and no premature resolution occurred).”
- Hop-level evidence recall based on fingerprint-matched gold supporting paragraphs.
  - Evidence: [b00260-172a01576f] “We map each supporting paragraph to its corresponding corpus chunk using 40-character fingerprint matching (paragraph-level recall: 87.9%), and compute hop-level evidence recall as the fraction of supporting paragraphs for which at least one matching chunk was retrieved.”
- Efficiency: average retrieved tokens and average API cost per question.
  - Evidence: [b00249-611f2bb207] “Tokens: average retrieved tokens per question; Cost: average API cost per question (USD).”

### Ablations

- Register initialization without seed evidence: build requirements from the question alone.
  - Evidence: [b00122-7ae81a1aba] “Building the register from the question alone rather than from seed evidence lowers LLM-Acc from 50.2 to 48.7”
- No iterative progress register: construct the register once and omit subsequent updates.
  - Evidence: [b00122-7ae81a1aba] “Removing iterative updates and constructing the register only once lowers LLM-Acc further to 48.3.”

### Negative results

- Recovered evidence does not yield a proportional reduction in total errors; reasoning errors and abstentions increase.
  - Evidence: [b00094-3ec11840a5] “Recovering this evidence does not reduce total error proportionally.”
- On HotpotQA, Contain-Match is essentially tied with A-RAG rather than improved.
  - Evidence: [b00108-a784564e37] “On HotpotQA, it reaches 77.0, which is essentially tied with A-RAG (77.3).”
- The register does not remove the difficulty of long evidence chains.
  - Evidence: [b00112-c7b6877feb] “The register improves overall accuracy but does not remove the difficulty of long evidence chains.”
- ExecutionRAG still has its highest residual missing-evidence rate on four-hop questions.
  - Evidence: [b00098-d0a7f172ff] “Residual failures caused by missing evidence for ExecutionRAG remain highest on four-hop questions, which contain longer and more weakly connected evidence chains.”


## Limitations

- Failure attribution is asymmetric: premature resolution is explicitly observable for ExecutionRAG but has no analogous event in A-RAG, so baseline reasoning errors may be undercounted and labeled as missing evidence.
  - Evidence: [b00097-e885121a69] “A-RAG has no analogous event; when it answers from incomplete evidence, the error is generally assigned to the missing passage instead. The comparison may thus undercount premature answers by the baseline.”
- The experiment can certify reachability only for recovered passages; unrecovered passages cannot be classified as unreachable.
  - Evidence: [b00024-d38de586bf] “Recovering evidence certifies reachability; failing to recover it proves nothing.”
- Aggregate reductions do not identify exactly which baseline failures were converted because the systems may fail on different questions.
  - Evidence: [b00025-78757d9304] “a reduction in the frequency of missing-evidence failures does not by itself identify which baseline failures were converted, because the two systems can fail on different questions.”
- Gold supporting paragraphs are incompletely mapped to corpus chunks, with paragraph-level fingerprint recall of 87.9%.
  - Evidence: [b00260-172a01576f] “using 40-character fingerprint matching (paragraph-level recall: 87.9%)”
- The register does not provide a reliable verifier and cannot make genuinely difficult passages retrievable.
  - Evidence: [b00098-d0a7f172ff] “The register guides search but does not provide a reliable evidence verifier: the language model still decides whether a requirement has been resolved, and this decision can be incorrect. It also cannot make genuinely difficult passages retrievable.”
- The method increases token and API cost on some datasets.
  - Evidence: [b00118-09440b4077] “The register increases the cost of some searches.”
- The system remains dependent on the retriever, language model, and source documents, and may produce overconfident answers from incomplete evidence.
  - Evidence: [b00330-a73eb99641] “the method still depends on the underlying retriever and LLM, so biases or errors in source documents may propagate. The framework could be misused in automated decision-making systems without human oversight, producing overconfident answers based on incomplete evidence.”
- The principal controlled failure analysis is confined to MuSiQue rather than repeated across all three benchmarks.
  - Evidence: [b00258-079c41b5e9] “we conduct a systematic error analysis on MuSiQue (n=1,000) and compare against the strongest agentic baseline, A-RAG.”

## Reproducibility

**Status:** partial

The paper supplies unusually strong procedural detail and full prompts, so an informed reimplementation is possible. Exact reproduction is not supported by the supplied material because code, data manifests, run artifacts, model snapshots, and stochastic-run controls are absent or unspecified.

**Available artifacts**

- Detailed method equations and state-transition rules.
- Extended configuration details for GPT-4o-mini, retrieval tools, embedding models, budgets, caching, and progress injection.
- Prompt templates for the agent, register initialization, register update, state injection, and forced final answer.
- Dataset split size, corpus protocol, matched baseline, accuracy tables, efficiency tables, ablations, and failure-analysis tables.

**Missing pieces**

- No source-code or executable repository artifact is identified in the supplied document.
- No released retrieval indices, sampled question identifiers, predictions, traces, register logs, or error annotations are identified.
- No exact GPT-4o-mini model snapshot or service version is stated.
- The tool-using agent uses default sampling settings, but no random seeds, repeated-run variance, or confidence intervals are reported.
- The identity and prompt/configuration of the LLM evaluation judge are not specified in the supplied blocks.
- The exact fingerprint-matching implementation and handling of unmatched gold paragraphs are not fully specified.

## AIDB assessment

- Novelty: The main novelty is not a new retriever but a controlled diagnostic framing: a requirement register is used as an intervention to separate reachable-but-unasked evidence from genuine access limitations, while exposing explicit resolution events for failure analysis. Related work already tracks gaps and sufficiency, so the strongest novelty lies in the fixed-retrieval measurement design and bottleneck-shift analysis.
- Usefulness: High for researchers designing or evaluating agentic multi-hop RAG. The paper provides a practical state representation, detailed prompts, matched comparisons, cost measurements, and a failure taxonomy that can distinguish search guidance from post-retrieval verification. Operational usefulness is tempered by increased cost, premature resolution, abstention, and incomplete reproducibility artifacts.
- Confidence: medium
- Recommended action: read
- Rationale: The controlled matched comparison and detailed failure analysis make the paper decision-relevant, especially for teams interpreting retrieval recall or building long-horizon RAG agents. Adoption should wait for independent replication with released traces, symmetric error annotation, repeated runs, and a stronger evidence verifier.

## Uncertainties

- **The MiniLM failure-analysis pass counts 533 ExecutionRAG failures, whereas the main-table accuracy of 50.2% on 1,000 questions implies 498. Appendix E acknowledges the discrepancy but does not reconcile the underlying predictions.** — The failure decomposition and main-table accuracy should not be treated as one identical set of scored predictions; paired traces are needed before attributing the precise change in total errors.
  - Evidence: [b00270-453dd61b6d] “The totals themselves come from this failure-analysis pass, and for ExecutionRAG under all-MiniLM-L6-v2 the total is slightly larger than the failure count implied by that method’s main-table accuracy”
- **How much of the measured shift from missing evidence to reasoning error is a true behavioral change rather than an artifact of asymmetric observability?** — If A-RAG premature resolutions are systematically hidden inside the missing-evidence category, the headline redistribution overstates the causal movement between failure types.
  - Evidence: [b00097-e885121a69] “Part of this increase reflects observability rather than a change in the model’s reasoning alone.”
- **What fraction of residual missing evidence is genuinely unreachable rather than still unasked?** — The experiment establishes a recoverable component but cannot determine the remaining retriever-coverage ceiling.
  - Evidence: [b00093-e5f84baeeb] “They do not imply that every residual missing passage is unreachable”
- **How sensitive are the results to stochastic model behavior and exact GPT-4o-mini versions?** — Structured register calls are deterministic in temperature, but the agent loop uses default sampling; without repeated runs, variance could affect accuracy, search paths, and failure counts.
  - Evidence: [b00216-e67a5e60d9] “Structured JSON calls for seed analysis and register updates use temperature = 0.0 to reduce output variance, while the tool-using agent loop uses the model’s default sampling settings.”
- **How much does incomplete paragraph-to-chunk matching bias missing-evidence counts and hop-level evidence recall?** — Unmatched supporting paragraphs may make evidence coverage or failure attribution incomplete, and the direction of the bias is not quantified.
  - Evidence: [b00092-3f4ca32ed3] “we match each supporting paragraph to its corpus chunk by a 40-character fingerprint (87.9% of paragraphs match)”
- **Does the diagnostic reduction generalize beyond MuSiQue to the other evaluated benchmarks?** — Answer accuracy generalizes across datasets, but the detailed gold-evidence failure decomposition is only reported for MuSiQue.
  - Evidence: [b00090-9c8acc2792] “We measure the controlled reduction described in Section 2.2 by assigning each wrong answer on MuSiQue a single cause using the gold supporting paragraphs.”
- **Is the gain caused specifically by persistent requirement state, or partly by extra LLM calls, prompting, and control logic?** — The matched baseline controls retriever, corpus, and generator backbone, but the register adds computation and multiple intertwined mechanisms; the two reported ablations do not isolate all components.
  - Evidence: [b00110-0c0ede00e0] “The register adds bookkeeping calls, but these calls alone do not explain the gain”

## Open questions

- Would a verifier trained on explicit resolution events improve answer accuracy without changing retrieved evidence?
- Can A-RAG and ExecutionRAG be evaluated with a symmetric, trace-level premature-resolution annotation protocol?
- What are the mean and variance across repeated stochastic runs and model snapshots?
- How do results change when all gold supporting paragraphs are mapped manually or with a higher-recall alignment method?
- Does the missing-evidence reduction replicate on HotpotQA and 2WikiMultiHopQA with benchmark-specific gold evidence annotations?
- Which register feature matters most independently: seed grounding, persistent state, progress deltas, retirement, append-only evidence, or the stopping rule?
- Can a shorter or cheaper register preserve the evidence-recovery gain while reducing token and API overhead?
- How robust is the register when seed retrieval grounds the wrong entity or omits a necessary requirement?

## Proposed AIDB experiments

- **Hypothesis:** Adding an independent evidence-sufficiency verifier at each active-to-resolved transition will reduce premature resolutions and improve final answer accuracy without materially changing evidence recall.
  - Baseline: Full ExecutionRAG with the language model alone deciding whether requirements are resolved.
  - Primary metric: LLM-Evaluation Accuracy, paired with the rate of false-resolution errors among wrong answers.
  - Stop condition: Stop if the verifier fails to improve LLM-Evaluation Accuracy across repeated runs or if its confidence interval includes no improvement while evidence recall remains unchanged.
- **Hypothesis:** A symmetric post-hoc annotation of both A-RAG and ExecutionRAG traces will reduce the apparent difference in reasoning-error share but preserve a significant reduction in missing-evidence failures.
  - Baseline: The paper's priority-based annotation scheme with ExecutionRAG-only false-resolution events.
  - Primary metric: Paired difference between systems in missing-evidence failure rate under symmetric trace annotation.
  - Stop condition: Stop if inter-annotator agreement is inadequate for reliable categorization or if the reduction is not robust to adjudication.
- **Hypothesis:** The controlled missing-evidence reduction generalizes to HotpotQA and 2WikiMultiHopQA when gold supporting passages are aligned to the retrieval corpus.
  - Baseline: Matched A-RAG using the same generator, tools, corpora, embedding model, and budgets.
  - Primary metric: Wrong answers with at least one unretrieved required passage, reported as count and within-method percentage.
  - Stop condition: Stop if corpus alignment cannot reach a pre-registered recall threshold or if neither benchmark shows a reduction across both embedding backbones.
- **Hypothesis:** Persistent requirement state, rather than additional token consumption, accounts for most of the answer-level gain.
  - Baseline: A compute-matched A-RAG variant given the same LLM-call budget, retrieval-loop budget, and retrieved-token budget as ExecutionRAG but no persistent register.
  - Primary metric: LLM-Evaluation Accuracy at matched retrieved-token and API-cost budgets.
  - Stop condition: Stop if compute matching eliminates the accuracy advantage or if budget matching cannot be achieved without changing retrieval access.
- **Hypothesis:** Improved gold-paragraph alignment will change absolute failure counts but preserve the relative reduction in missing-evidence failures.
  - Baseline: The existing 40-character fingerprint mapping.
  - Primary metric: Difference in the A-RAG-to-ExecutionRAG missing-evidence reduction under manual or higher-recall alignment versus fingerprint alignment.
  - Stop condition: Stop when the confidence interval for the difference excludes the pre-registered materiality threshold or the enhanced alignment reaches the target recall.
- **Hypothesis:** A compressed register retaining only open requirements and passage identifiers will recover most of the accuracy benefit at lower cost.
  - Baseline: Full ExecutionRAG with evidence notes and progress deltas.
  - Primary metric: LLM-Evaluation Accuracy per average API cost per question.
  - Stop condition: Stop if accuracy drops beyond a pre-registered non-inferiority margin or cost fails to decrease materially.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `reviewed-candidate`
- Generated: `2026-10-16T14:31:47.294361+00:00`
- Document SHA-256: `7b2f78a6ae566235f337ad0a07b24686f119ebf468773989eb90fef9f1843747`
- Metadata SHA-256: `41fa88c84e13cf9d0cb1e0a7e57b4378420a0c48c97e63f9385cede877c8093e`
- Blocks: 330
- Deterministic repair attempts: 0
