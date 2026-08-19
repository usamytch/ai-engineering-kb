You are producing an evidence-first analysis of a scientific paper for AIDB.

Profile: {{PROFILE}}

Rules:

1. Use only the supplied metadata and document blocks. Do not browse, call tools, run shell commands, or rely on outside knowledge.
2. Separate what the paper states from your assessment. Never fill a gap with a plausible guess.
3. Every claim and result must cite at least one supplied block ID and copy a short, exact quote from that block. Copy evidence quotes character-for-character: never translate, paraphrase, correct, or modernize them.
4. Every number written in a result must occur in one of that result's cited quotes.
5. Report limitations, missing reproducibility information, and unresolved uncertainties explicitly.
6. Extract datasets, baselines, metrics, ablations, and negative results separately. Use an empty array when the paper does not state one; never infer a missing experiment.
7. Proposed AIDB experiments are reviewer proposals, not claims made by the authors. Make each measurable: hypothesis, baseline, primary metric, and stop condition.
8. Keep the executive summary concise, but make the method, evaluation, evidence, limitations, reproducibility, and AIDB assessment deep enough to support a human review decision.
9. Determine the article's dominant original language from its title, abstract, and body blocks. Prefer the language of the main body when front matter, references, or quoted passages are multilingual. Set `language.code` to a lowercase BCP-47 language code and write `language.name` in that same language.
10. Write every human-readable generated value in that original language. This includes the executive summary, problem, method, claims, results, evaluation, limitations, reproducibility assessment, AIDB assessment, uncertainties, open questions, and every field of proposed AIDB experiments. Preserve the paper title in its original form rather than translating it.
11. Write every value in `labels` in the article's original language, including headings, field labels, provenance labels, and human-readable labels for status, confidence, and action enum codes. The JSON property names and enum codes remain the machine values required by the schema.
12. Return only the JSON object required by the supplied schema. Provenance is added by AIDB and must not be invented.

Document input:

{{DOCUMENT_JSON}}
