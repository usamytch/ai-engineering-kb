# Cited but Unused: Parametric Provenance in Retrieval-Augmented Generation

## Executive summary

The paper distinguishes citation support from causal provenance and introduces counterfactual value substitution to construct behavioral labels. On ASQA, measured parametric provenance varies materially by model, substitution distance, and demonstrations; title/question leakage had previously inflated rates. Support-based NLI is ineffective, while token-level context contrast ranks cases substantially better but still fails as a deployable flagger at low base rates. The study is unusually candid about negative results and artifacts, but generalization is limited by numeric-value coverage, discarded cases, small non-ASQA samples, open models no larger than 14B, and a detector that captures prior knowledge more readily than actual use.

## Problem

**Statement.** RAG citations can corroborate a claim without truthfully identifying the source that caused it. The paper studies claims whose cited passages agree with the output even though the disputed value came from parametric memory.

**Why it matters.** A supported but post-rationalized citation can appear verifiable while directing the reader to evidence without confirmatory power. This makes ordinary entailment-based citation checks structurally incapable of establishing provenance.

**Scope.** The empirical scope covers five Qwen2.5-Instruct sizes and Llama-3.1-8B-Instruct, primarily on ASQA, with smaller ELI5 and QAMPARI evaluations. It targets editable numeric values and behavioral provenance under counterfactual passage edits, not the causal provenance of an entire claim or unrestricted text.

## Method

The protocol finds a value shared by an answer and its retrieved passages, replaces it throughout passage bodies and titles with a false variant, regenerates the answer, and labels the disputed value contextual if the model follows the replacement or parametric if it repeats the original. Cases containing both or neither value, and cases where the value appears in the question, are excluded. Detection methods are then evaluated against these constructed labels without regeneration.

### Key components

- Counterfactual value substitution supplies operational ground truth through an intervention rather than an inference about hidden model state.
- The corrected protocol edits passage titles as well as bodies and excludes values surviving in the question.
- Generation uses ALCE-style completion prompts, greedy decoding, and seeded counterfactual selection.
- Prevalence is compared across model scale, family, datasets, substitution distances, retrieval depths, and demonstration counts.
- Detection compares support-based NLI, sentence-level contrast, passage-deletion attribution, token-level context contrast, and related likelihood or entropy signals.
- Utility is evaluated separately from ranking quality by asking whether flagging improves provenance honesty at realistic base rates.

### Assumptions

- Repeating the original value after all contextual occurrences are replaced operationally indicates reliance on memorization; following the replacement indicates contextual dependence.
- String containment reliably identifies the disputed values except for acknowledged parsing and token-boundary failures.
- Discarded cases are not assumed equivalent to decided cases; the paper explicitly identifies possible selection bias.
- The experimental labels concern the provenance of the disputed value, not necessarily the provenance of every part of the claim.
- Greedy decoding makes generation deterministic conditional on model and prompt, but counterfactual-value choice remains a source of variation that is not replicated across seeds.

## Main claims

- **Citation correctness and citation faithfulness are distinct: a passage may entail a claim without having causally influenced it, which makes support-only verification insufficient for provenance.**
  - Evidence: [b00038-429bcf1fd6] “A post-rationalised citation is correct but not faithful; this is exactly the circumstance that support-based verification cannot detect”
- **The authors construct behavioral provenance labels by replacing a shared value in all passage surfaces and observing whether regeneration follows the replacement or preserves the original.**
  - Evidence: [b00041-303fc9e089] “If the model reports v′ then it used the context; if it reports v it instead relied on memorisation”; [b00041-303fc9e089] “replacing it throughout the passages including their titles with a false variant v′”
- **Parametric claims receive citations about as readily as contextual claims in models that reliably follow the citation format.**
  - Evidence: [b00072-341368169f] “between 89% and 100% of parametric claims carry a citation”; [b00072-341368169f] “A model answering from memory hence cites as readily as one answering from the passages.”
- **The strongest tested signal reflects the model’s prior knowledge more directly than its actual choice to use memory rather than context.**
  - Evidence: [b00104-46e9f2c8df] “The signal measures what the model knows rather than what it used”; [b00104-46e9f2c8df] “Knowing is not deciding: of those 220 claims, 191 followed the edited passage anyway.”

## Results

- **On ASQA at the default substitution setting, measured parametric provenance ranged from 1.2% for Qwen2.5-0.5B to 13.3% for Qwen2.5-14B, while Llama-3.1-8B reached 15.7%. Within Qwen, the reported size trend was Kendall’s τ=0.80, but the middle-sized intervals were less distinct.**
  - Context: This is the headline prevalence comparison. It supports an association with scale within one family while also showing a strong family effect; it does not justify extrapolation beyond the tested models.
  - Evidence: [b00048-ce1fd52abc] “Qwen2.5-0.5B 0.5 1.2 [0.6, 2.6]”; [b00048-ce1fd52abc] “Qwen2.5-14B 14.8 13.3 [10.4, 16.9]”; [b00048-ce1fd52abc] “Llama-3.1-8B 8.0 15.7 [12.6, 19.4]”; [b00050-a1e18d1085] “with Kendall’s τ=0.80”; [b00050-a1e18d1085] “the trend between 3B, 7B and 14B less distinct”
- **Substitution distance materially changed prevalence: the near setting yielded 4.6% on Qwen2.5-7B and 8.5% on Qwen2.5-14B, whereas the far setting yielded 16.3% and 17.6%. The authors therefore interpret the quantity partly as resistance to contradicting evidence rather than provenance in the abstract.**
  - Context: This is a major construct-validity qualification. Extreme counterfactuals may reward reasonable rejection of implausible evidence, so default-setting rates are conditional on intervention design.
  - Evidence: [b00054-458bfd6895] “Near 4.6 [3.0, 6.8] 8.5 [6.3, 11.3]”; [b00054-458bfd6895] “Far 16.3 [12.9, 20.3] 17.6 [14.2, 21.5]”; [b00223-70ced6f30e] “better described as resistance to contradicting evidence than as provenance in the abstract”
- **Support-based verification did not separate provenance reliably. On cited Qwen2.5-7B claims, AUROC was 0.532 with interval [0.415, 0.646]; despite the asserted value occurring in 0 of 35 cited parametric passages versus 96.5% of cited contextual passages, mean entailment was higher for parametric claims, 0.329 against 0.214.**
  - Context: This controlled cited-passage comparison is the strongest evidence for the paper’s structural critique of entailment-based verification: even explicit contradiction at the disputed value was not converted into a useful provenance ranking.
  - Evidence: [b00080-03bed36fad] “AUROC 0.532, interval [0.415, 0.646]”; [b00080-03bed36fad] “0 of 35 cases, against 96.5% of cited contextual claims”; [b00080-03bed36fad] “mean entailment is higher for parametric claims, 0.329 against 0.214”
- **Token-level context contrast was the strongest tested family, with mean AUROC about 0.79, compared with 0.70 for ConSens, 0.67 for sentence-level likelihood, and 0.59 to 0.67 for passage-level attribution. Removing oracle knowledge of the disputed span reduced Qwen2.5-7B AUROC from 0.760 to 0.668.**
  - Context: Fine localization improves ranking, but the deployment-oriented scan shows that oracle span selection contributes materially. The paper treats the oracle scores as an upper bound rather than deployable performance.
  - Evidence: [b00084-a5a2932f0c] “Measuring the context contrast at the disputed token gives a mean AUROC of 0.79.”; [b00084-a5a2932f0c] “0.70 for ConSens and 0.67 for the sentence-level likelihood”; [b00084-a5a2932f0c] “Passage-level attribution, which is what leave-one-out and the necessity and sufficiency rewards compute, gives 0.59 to 0.67.”; [b00101-76159bd3a4] “lowers AUROC from 0.760 to 0.668”
- **Ranking quality did not translate into useful symmetric-cost flagging: no tested model improved honesty, precision peaked at 0.45 below the 0.5 break-even point, and the authors dismissed the ELI5 gain of +0.022 as noise. Under asymmetric costs, the largest reported reduction was 46% only at a 5:1 ratio and a 35% budget.**
  - Context: This consequential negative result separates detector AUROC from operational value. Deployment would require explicit cost asymmetry and a large review budget, not merely a moderately strong ranker.
  - Evidence: [b00111-d2371b5ee7] “flagging does not pay on any of the six models: honesty falls at every budget”; [b00111-d2371b5ee7] “precision peaks at 0.45, below the break-even point of 0.5”; [b00111-d2371b5ee7] “a gain of +0.022 on ELI5, resting on three correct flags and one incorrect, which we regard as noise”; [b00111-d2371b5ee7] “a 46% cost reduction on Qwen2.5-14B, and only at a 5:1 ratio and a 35% budget”

## Experimental evaluation

### Datasets

- ASQA is the primary dataset, paired with GTR top-5 retrieval and 800 questions per condition.
  - Evidence: [b00044-d4df2c1774] “Our primary reference dataset is ASQA (Stelmakh et al., 2022) with GTR (Ni et al., 2022) top-5 retrieval, 800 questions per condition.”
- ELI5 with BM25 retrieval and QAMPARI were evaluated on Qwen2.5-7B to probe long-form questions, entity lists, and retrieval variation, but editable-value coverage and positive counts were low.
  - Evidence: [b00044-d4df2c1774] “We also assess ELI5 (Fan et al., 2019) with BM25 retrieval and QAMPARI (Amouyal et al., 2023) using Qwen2.5-7B”; [b00129-9d011ab90e] “ELI5 and QAMPARI yield four and three parametric cases, too few for detection statistics.”

### Baselines

- The primary support baseline is a DeBERTa NLI cross-encoder using maximum entailment over every retrieved passage, deliberately avoiding a citation-selection penalty.
  - Evidence: [b00046-f430d29958] “The support-based baseline is a DeBERTa (He et al., 2021) cross-encoder trained for NLI.”; [b00046-f430d29958] “taking for each claim the maximum entailment over all retrieved passages”
- The attribution comparison includes localized token contrast, context-free Jensen–Shannon divergence, sentence-level likelihood, ConSens, sufficiency, leave-one-out maximum and sum, necessity, NLI entailment, and TrustMargin.
  - Evidence: [b00082-3e4c522999] “Localised (ours)”; [b00082-3e4c522999] “JSD, no context”; [b00082-3e4c522999] “ConSens”; [b00082-3e4c522999] “Sufficiency”; [b00082-3e4c522999] “LOO max”; [b00082-3e4c522999] “LOO sum”; [b00082-3e4c522999] “Necessity”; [b00082-3e4c522999] “NLI entailment”; [b00082-3e4c522999] “TrustMargin”
- Most comparison entries are reimplementations of each method’s computed quantity, not executions of the published systems; ContextCite is the stated exception.
  - Evidence: [b00135-b852168cf9] “Our comparison table uses reimplementations of the quantity each method computes rather than the published systems.”; [b00135-b852168cf9] “The exception is ContextCite, which we run as published on Qwen2.5-7B”

### Metrics

- Prevalence rates use Wilson confidence intervals.
  - Evidence: [b00046-f430d29958] “Confidence intervals for rates are Wilson intervals”
- Detection is evaluated primarily by AUROC; intervals and paired method comparisons use claim-level bootstrap resampling.
  - Evidence: [b00046-f430d29958] “AUROC intervals and paired comparisons use a bootstrap over claims with 2000 resamples”
- Label validation reports percentage agreement and Cohen’s κ, including agreement with majority vote and pairwise annotator reliability.
  - Evidence: [b00069-411169cc3c] “82.8% for the majority vote (κ=0.658)”; [b00069-411169cc3c] “Pairwise agreement between the annotators themselves”
- End-to-end utility is assessed through provenance honesty, precision at a flagging budget, and cost reduction under asymmetric error costs.
  - Evidence: [b00106-333baa8641] “Define provenance honesty as the fraction of claims presented truthfully in regard to their origin.”; [b00111-d2371b5ee7] “Under asymmetric costs the largest gain is a 46% cost reduction”

### Ablations

- Counterfactual distance was varied across near, default, and far settings; measured prevalence increased with distance on both tested models.
  - Evidence: [b00057-2293261fda] “The rate rises at every increment on both models”
- Retrieval depth from one to ten passages did not materially change prevalence.
  - Evidence: [b00225-1d5a52c93a] “All four intervals overlap and the extremes do not differ (p=0.47).”
- Increasing demonstrations raised measured prevalence and was the prompt choice identified as materially affecting the protocol.
  - Evidence: [b00227-a7248f9a3f] “The rate rises from 5.4% with no demonstrations to 8.2% with two and 12.6% with four”; [b00227-a7248f9a3f] “This is the one prompt choice that materially affects the measurement”
- Localizing scores to the disputed token was compared with sentence-level scoring, and scanning all numeric candidates tested performance without oracle span knowledge.
  - Evidence: [b00092-f910fe8358] “Localisation improves detection on every model”; [b00218-532933b253] “Localisation therefore survives candidate selection at a measurable price.”

### Negative results

- Four tested entailment verifiers failed to provide useful provenance separation.
  - Evidence: [b00211-274d5f22ac] “No verifier separates provenance at a level that would be useful.”
- ContextCite was indistinguishable from chance on Qwen2.5-7B.
  - Evidence: [b00089-bb51a05380] “it reaches AUROC 0.507, with a bootstrap interval of [0.413, 0.605] that contains the chance value 0.5”
- Three additional black-box hypotheses were tested and discarded: competing-value intervention, frequency correction, and unsupervised mixture estimation.
  - Evidence: [b00251-277fb2c6da] “Three further hypotheses were tested and discarded.”; [b00253-f323f5a1ab] “correcting for it costs performance (0.803 to 0.727).”; [b00254-6b231f89dd] “even 150 labels leave 0.042 absolute error”
- The detector did not improve provenance honesty under symmetric costs.
  - Evidence: [b00197-bd36fa149e] “flagging yields no honesty gain under symmetric costs”


## Limitations

- The evaluated open-weight models span only 0.5B to 14B; closed frontier models are inaccessible to the required token-level scoring, so larger-model extrapolation is untested.
  - Evidence: [b00123-87484c3f9f] “the largest we measure is 14B and the extrapolation is not tested”; [b00123-87484c3f9f] “closed frontier models do not expose”
- Between 19% and 24% of records are discarded as undetermined, creating possible selection bias that the protocol cannot internally diagnose.
  - Evidence: [b00125-f3662c91b6] “Between 19% and 24% of records are discarded as undetermined”; [b00125-f3662c91b6] “If those cases differ systematically from the decided ones, the rates are biased.”
- Coverage is restricted to numeric values shared by answer and passages, reaching roughly 70% on ASQA but much less on ELI5 and QAMPARI; unmeasured claims may behave differently.
  - Evidence: [b00127-494bf46822] “roughly 70% of ASQA answers but only 16.5% and 21.8% of ELI5 and QAMPARI”; [b00127-494bf46822] “Claims without such a value are not measured”
- Non-ASQA detection evidence is underpowered because ELI5 and QAMPARI contain very few parametric cases.
  - Evidence: [b00129-9d011ab90e] “ELI5 and QAMPARI yield four and three parametric cases, too few for detection statistics.”
- The behavioral intervention can label a model parametric even if it used the passage but resisted the edit, and it labels only the disputed value rather than the whole claim.
  - Evidence: [b00131-caee89bc39] “A model might use a passage yet still resist an edit, which our protocol would label parametric.”; [b00131-caee89bc39] “The label therefore reflects the provenance of the disputed value rather than of the whole claim.”
- Blind validation covers only one model and achieves substantial rather than strong majority agreement.
  - Evidence: [b00133-41edde6434] “The blind round covers 120 items from one model, Qwen2.5-14B.”; [b00133-41edde6434] “κ=0.658 for the majority is substantial rather than strong”
- String-based extraction and replacement can match substrings, split formatted numbers, or create impossible dates; a typed-value parser was not used.
  - Evidence: [b00137-8613b55359] “the target value is found and replaced by string operations rather than by parsing”; [b00137-8613b55359] “A parser over typed values would remove all three.”
- Most published attribution systems were not run directly, and internal-state methods could contain information absent from output distributions.
  - Evidence: [b00135-b852168cf9] “methods that read attention or hidden states (Qi et al., 2024; Wu et al., 2025) are cited but not run”; [b00135-b852168cf9] “could carry information the output distribution does not”

## Reproducibility

**Status:** strong

Reproducibility is strong on the paper’s own account because code, configurations, outputs, environment metadata, and traceability are explicitly provided, and the computational requirement is modest. Confidence is reduced by the absence of multi-seed counterfactual replication and by baseline reimplementation. The paper also notes that two analyses run in different environments can differ in the third decimal, so exact numerical matching should use the recorded run metadata.

**Available artifacts**

- Public code repository is stated to contain code, configurations, and per-run outputs.
- Each run records a configuration hash, git commit, package and CUDA versions, and GPU model.
- The paper specifies model families and sizes, precision, prompt style, decoding mode, datasets, retrieval methods, sample counts, confidence procedures, and generation hardware/software.
- Counterfactual selection is seeded and recorded for individual runs.

**Missing pieces**

- Runs were not repeated under different counterfactual-value seeds, so reported intervals do not capture variation across substitution choices.
- The supplied blocks do not state exact model checkpoint identifiers or dataset/retrieval snapshot versions.
- Published implementations were not run for most attribution baselines.
- No reproduction results from an independent environment are supplied.

## AIDB assessment

- Novelty: The central novelty is not merely applying entity substitution, but using corrected, intervention-constructed labels to separate causal provenance from corroborative support across several model sizes and then connecting those labels to detector utility. The explicit discovery and correction of title/question leakage materially strengthens the methodological contribution.
- Usefulness: High for evaluation design and reviewer practice: it demonstrates that citation entailment cannot establish source use, supplies an auditable counterfactual protocol, exposes sensitivity to intervention distance and demonstrations, and reports when promising AUROC fails operationally. Immediate production use is low because the detector is not deployable and the protocol covers only a subset of claims.
- Confidence: medium
- Recommended action: read
- Rationale: The paper deserves close reading because its strongest contribution is a validity correction to common citation evaluation, supported by controlled comparisons and unusually informative negative results. Adoption of the detector would be premature: prevalence is intervention-dependent, broad claim coverage is absent, many records are undecidable, and the signal confounds knowing with using.

## Uncertainties

- **How much measured prevalence reflects provenance failure versus rational resistance to implausible counterfactual evidence remains unresolved.** — If intervention plausibility changes the target construct, a single headline rate cannot be treated as an intrinsic model property or safely compared across protocols.
  - Evidence: [b00223-70ced6f30e] “Part of what we measure is how implausible the substituted value is”; [b00223-70ced6f30e] “The two coincide only where the substituted value is plausible enough”
- **The behavior of discarded cases is unknown.** — Systematic differences between decided and undetermined records could bias both prevalence estimates and detector evaluation.
  - Evidence: [b00125-f3662c91b6] “The protocol provides no label for them, so we cannot check this from within it.”
- **Label reliability may differ across the five models not included in blind validation.** — Model-specific response styles, conflict statements, and citation adherence could change the relationship between automatic labels and human judgments.
  - Evidence: [b00133-41edde6434] “Whether the labels are equally reliable on the other five is untested”
- **It is unknown whether black-box signals can distinguish prior knowledge from actual use when both context and memory support the same value.** — This is the central barrier to a detector that works under ordinary, non-conflicting retrieval rather than under label-generating interventions.
  - Evidence: [b00139-420c4addbc] “We did not test whether a signal distinguishing knowledge from use exists within black-box access”; [b00139-420c4addbc] “the central open question this work leaves”
- **The reported scale trend may not extend beyond the tested open-weight range or across model families.** — Deployment risk assessments for frontier systems cannot be inferred from the measured family without direct tests.
  - Evidence: [b00123-87484c3f9f] “the extrapolation is not tested”; [b00051-32e0657b82] “Family is at least as significant as size”

## Open questions

- Can a behavioral or black-box intervention distinguish what a model knew from what it causally used when memory and retrieved context agree?
- Do provenance rates and detector behavior generalize to nonnumeric entities, relations, quotations, and multi-hop claims?
- How should counterfactual values be sampled so that edits remain plausible while still producing identifiable interventions?
- What explains undetermined cases, and can they receive reliable provenance labels without introducing human-intent inference?
- Do hidden-state or attention-based methods outperform output-distribution signals on the same corrected labels?
- How stable are prevalence estimates across counterfactual seeds, retrieval snapshots, prompt templates, languages, and independently reproduced environments?
- Can a calibrated policy achieve useful precision under low base rates without an impractically large review budget or extreme cost asymmetry?

## Proposed AIDB experiments

- **Hypothesis:** Typed, plausibility-constrained substitutions reduce protocol artifacts and lower sensitivity to substitution distance while preserving the ordering between model conditions.
  - Baseline: The paper’s string-based near/default/far substitution protocol with title replacement and question exclusion.
  - Primary metric: Difference in parametric-provenance rate across substitution distances, accompanied by the fraction of malformed, substring, or semantically implausible edits and human plausibility agreement.
  - Stop condition: Stop if typed substitution does not reduce edit defects and does not narrow cross-distance rate variation on a preregistered held-out sample, or if label coverage falls enough to make confidence intervals wider than the baseline.
- **Hypothesis:** A detector using internal activations can distinguish knowledge from use better than output-distribution contrast, especially among claims the model can already answer without context.
  - Baseline: Localized change-in-entropy or change-in-log-probability scoring, evaluated both overall and on the prior-knowledge subset.
  - Primary metric: Paired AUROC and precision at the symmetric-cost break-even operating point on corrected counterfactual labels, with the prior-knowledge subset designated primary.
  - Stop condition: Stop if the internal-state detector fails to improve paired AUROC on the prior-knowledge subset and fails to cross break-even precision on two independently seeded test sets.
- **Hypothesis:** Multi-seed counterfactual evaluation reveals non-negligible intervention-choice variance that is missing from claim-only confidence intervals.
  - Baseline: One seeded counterfactual per claim with Wilson intervals and claim-level bootstrap, matching the reported design.
  - Primary metric: Variance component attributable to counterfactual choice and the resulting change in confidence intervals for prevalence and detector AUROC.
  - Stop condition: Stop once interval estimates stabilize under sequential seeds, or conclude the original design is adequate if counterfactual-choice variance remains below a preregistered negligible-effect threshold across all tested models.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:32:18.017555+00:00`
- Document SHA-256: `90d63faf5518cfe64e747ddc6f917111e30a3dc213d6ad189b4f4b8983ee04ea`
- Metadata SHA-256: `9c88999eb72df2a7ea2df08fa3c221e233c0145a75f81c914280bd50aa782faa`
- Blocks: 261
- Deterministic repair attempts: 0
