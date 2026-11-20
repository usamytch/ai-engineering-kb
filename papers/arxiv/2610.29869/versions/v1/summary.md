# Compaction Laundering: Provenance Destruction in Context-Compacting Coding Agents

## Executive summary

The paper identifies context compaction as a security boundary: serializers that replace typed roles with forgeable text labels can turn attacker-controlled document content into apparent user instructions. Its strongest evidence is a controlled nine-harness comparison, paired clean arms, sandboxed command execution, and a small end-to-end pi TUI study. Flattening harnesses laundered forged approvals while role-typed controls did not; the live attack succeeded in 3/6 poisoned takes versus 0/5 clean takes. The causal mechanism is persuasive, but precise execution rates are uncertain because most execution cells contain only 3–5 runs, released products were usually not exercised end to end, and the defense lacks adaptive evaluation. Serializer escaping or retained typed provenance is more compelling than the partially effective post-hoc validator.

## Problem

**Statement.** Long-running coding agents replace an original typed conversation with a compact summary. If the harness first flattens roles into unescaped in-band labels, attacker-controlled files or pages can forge a user turn whose true source disappears when the original transcript is discarded.

**Why it matters.** The corrupted summary can assert standing authorization, steer an agent away from security-relevant files, or contribute to attacker-controlled command execution. The issue affects the ordinary compaction path rather than requiring a separate persistent-memory component.

**Scope.** The study examines nine released harnesses: five flattening systems and four role-typed controls. Most experiments exercise pinned serializers and compaction prompts in a staged runner; one experiment exercises the real pi TUI end to end. Execution measurements primarily cover model-only or full-auto conditions and benign canary payloads.

## Method

The authors inspect and pin real compaction prompts and serializers, inject a forged role marker into tool output, compact controlled conversations with frontier models, and score whether the resulting summary attributes the forged claim to the user. They separate laundering from downstream action, compare poisoned, genuine-approval, and clean arms, execute benign payloads in disposable containers, vary model, harness, context size, placement, repetition, and prompt defenses, and run a paired live demonstration in pi.

### Key components

- Threat model with attacker-controlled file, web page, or dependency documentation containing an in-band role marker.
- Structural comparison between flattening serializers and role-typed message arrays, with the latter used as controls.
- Primary laundering judgment based on whether the summary speaks for the user without preserving the external origin.
- Sandboxed downstream agent that can issue a real command and create a host-observed proof artifact.
- End-to-end paired pi TUI sessions differing only by one forged line in the fetched guide.
- Post-hoc provenance-contrast defense that compares user-attributed summary claims with retained genuine user turns.

### Assumptions

- The attacker can cause the agent to read attacker-controlled content before compaction.
- The affected serializer does not escape role labels appearing inside untrusted content.
- For the principal command-execution measurements, the model is effectively the execution gate; an enforced external approval mechanism or OS sandbox can block the demonstrated network command.
- A benign canary is an adequate mechanical indicator of attacker-controlled execution, but not of the execution rate for overt credential theft or other high-stakes payloads.
- The LLM laundering judge and salience judge adequately represent their stated scoring criteria; only the laundering judge receives a reported cross-family validation sample.

## Main claims

- **Exposure is attributed to serialization structure rather than to a universal model weakness: flattening makes role markers forgeable, while role-typed messages retain origin.**
  - Evidence: [b00007-6acd159b39] “Susceptibility is therefore a property of the serialization strategy, not of the model.”; [b00160-09250186db] “Harnesses that flatten roles into text launder 87–100%; harnesses that keep roles typed launder 0%, with no intermediate values.”
- **The forged label is an operative causal component, because removing it while retaining the payload words sharply reduces laundering.**
  - Evidence: [b00104-96290ac2d0] “harness / arm with forged label plain text pi 87% 6%”; [b00105-478d69511b] “Without the label, the same words mostly do not launder.”
- **Laundering and command execution are distinct links: a false approval can be retained without being acted upon, and downstream behavior depends on audit survival, payload characteristics, salience, and the next user message.**
  - Evidence: [b00190-55120e913b] “The agent held a false belief without acting on it.”; [b00191-d58c016531] “Neither E6’s execution rates nor E10’s laundering rates subsume the other; the live chain exposes the joint.”
- **Prompt-only anti-injection instructions reduce but do not eliminate laundering on counterfactual flattened input; the proposed code-level check is stronger but remains incomplete.**
  - Evidence: [b00109-c19905a43a] “even where it helps most it leaves 62% of payloads laundered, a reduction, not a fix.”; [b00154-b0a24f437d] “At the recommended setting (0.15), 23% still gets through, a substantial mitigation, not a solution.”

## Results

- **In the main cross-harness comparison, pi, opencode, and Aider laundered 100% (15/15), OpenHands 93% (14/15), and Cline 87% (13/15), whereas Codex, Gemini CLI, Qwen Code, and Continue produced 0% (0/15).**
  - Context: Each harness used its real serializer and compaction prompt on three frontier models. This is the strongest controlled evidence for the structural serialization hypothesis, although the outcome is laundering rather than live execution.
  - Evidence: [b00156-cdcd0328e8] “We planted the identical forged approval in nine released harnesses and ran each one’s real serializer and real compaction prompt on three frontier models (n = 15 per harness).”; [b00159-49108a510f] “Flattening pi, opencode, Aider 100% (15/15) Flattening OpenHands 93% (14/15) Flattening Cline 87% (13/15)”; [b00159-49108a510f] “Role-typed Codex, Gemini CLI, Qwen Code, Continue 0% (0/15)”
- **The real pi TUI produced a full-chain win in 3/6 poisoned takes and 0/5 clean takes; all poisoned takes refused pre-compaction execution, while one clean take executed before compaction and was excluded from the attack’s causal sequence.**
  - Context: This paired end-to-end experiment is the most operationally relevant evidence, but its sample is small and uses one harness and one victim model.
  - Evidence: [b00183-edd1ed3d83] “arm full chain (WIN) refused post-compaction ran pre-compaction (attack unnecessary) poisoned 3/6 3/6 0/6 clean 0/5 5/5 1/6 †”; [b00184-f3d8250cd2] “†one clean take executed the bootstrap during its first turn, before any compaction — model variance, not the attack — and the paired design absorbs it.”
- **At the recommended provenance-contrast setting of 0.15, the defense caught 77% of laundering while demoting 2% of legitimate claims. The compared prompt rule stopped about 13% on Claude and 25% on GPT, while the cited classifier baseline reached 67% at best and 42% on low-signal payloads.**
  - Context: The comparison favors checking summary attribution in code, but the classifier figures are imported from prior work rather than re-measured on the same implementation, and the defense was not tested against adaptive payloads.
  - Evidence: [b00151-e484d69edf] “0.15 77% 2%”; [b00153-952debaebe] “Gemini’s in-prompt rule stops ~13% of laundering on Claude, ~25% on GPT”; [b00153-952debaebe] “Published classifier defenses [2] 67% catch rate at best, 42% on low-signal payloads”
- **A genuine skeptical audit sharply reduced downstream execution: pooled across all E16 arms and both models, execution was 1/50 even though forged user approval still laundered reliably. This contrasts with the live study’s approximately 50% success when the audit disappeared during compaction.**
  - Context: This consequential negative result limits the broad RCE interpretation and supports the paper’s separation between false authorization and artifact verification. The audit was scripted and deliberately strong.
  - Evidence: [b00198-1f5b881f25] “execution collapses to 1/50 pooled across all arms and both models.”; [b00206-c51a3eabf0] “1/50 with the maximal forgery, versus E15’s ~50% when the audit is absent.”

## Experimental evaluation

### Datasets

- Synthetic poisoned and clean conversations used to isolate compaction behavior, including short controlled transcripts and filled windows.
  - Evidence: [b00069-a57b82d064] “The poisoned conversation is synthetic, and we invoke the summarizer directly rather than waiting for a real window to fill and trigger compaction on its own.”
- Raw outputs for every reported table, organized under the repository’s data directory.
  - Evidence: [b00029-d8b4fb20cb] “data/ the raw output behind every table”
- Paired live pi TUI sessions with recordings, logs, and per-take digests; poisoned and clean guides differ by one forged line.
  - Evidence: [b00075-ec5e7d23e8] “Every take is run as a paired arm, byte-identical except for one forged [User]: line in the served guide, so the only variable is the poison.”
- Clean defense corpus comprising 324 claims from four sessions.
  - Evidence: [b00150-cc17834e93] “over 324 claims from clean summaries.”; [b00370-238fa2a4d2] “The clean corpus behind the false-positive rate is also small (4 sessions).”

### Baselines

- Role-typed Codex, Gemini CLI, Qwen Code, and Continue as the structural control group.
  - Evidence: [b00050-81fa2d9b09] “We test five flattening harnesses and four role-typed ones; the role-typed group is the control.”
- Clean arm: identical task and transcript without the forged line.
  - Evidence: [b00084-9c6e8ce790] “The exact same task with no forged line planted.”
- Genuine user approval as an execution ceiling and no approval as a floor.
  - Evidence: [b00135-a412e99855] “laundered, a forged [User]: line in tool output (the attack); genuine, a real user turn saying it (the ceiling); and clean, no approval (the floor).”
- Gemini’s in-prompt rule and previously published classifier defenses as defense baselines.
  - Evidence: [b00152-e1f7a0f525] “the Gemini rule and this check measured on our data; the classifier row is the rate reported by [2], not re-measured here”

### Metrics

- Laundering: whether the forged line appears as a user-attributed instruction without its external origin.
  - Evidence: [b00078-49c2a79361] “Laundering (the primary metric). The forged line appears in a part of the summary that speaks for the user, with nothing marking it as originating elsewhere.”
- Survival: whether the forged line remains anywhere in the summary, regardless of correct attribution.
  - Evidence: [b00080-4a10a5b396] “Survival. A weaker signal, whether the line appears in the summary at all.”
- Issued and confirmed execution, distinguishing the agent’s command from appearance of the proof file.
  - Evidence: [b00082-368cc35423] “Issued means the agent ran the attacker’s command, the behavior of interest. Confirmed means the payload’s proof file appeared.”
- Defense catch rate and collateral demotion of legitimate summary claims.
  - Evidence: [b00150-cc17834e93] “The catch rate is measured over the cells that laundered; the collateral is how much legitimate summary content it wrongly demotes”
- LLM-judged summary salience on a 1–5 scale.
  - Evidence: [b00171-a127db32a8] “an LLM-judged salience (1–5) of how prominently that same summary carries the approval”

### Ablations

- Forged role label versus identical plain text without the label.
  - Evidence: [b00103-f92dc0fe59] “we ran the same payload two ways, with the forged label in front of it and as plain text with no label.”
- Gemini anti-injection rule enabled versus removed over counterfactual flattened serialization.
  - Evidence: [b00107-a5da26cb37] “we run its real prompt with the rule on and off over a flattening serialization”
- Context-size and poison-position sweeps, including windows up to approximately 908,000 tokens.
  - Evidence: [b00143-8f086b50fa] “~2,800 3/3 ~65,200 3/3 ~130,000 3/3 ~306,800 3/3 ~507,000 3/3 ~731,000 3/3 ~908,000 3/3”; [b00147-700e062f9a] “start (10% in) 3/3 3/3 middle (50% in) 3/3 3/3 end (90% in) 3/3 3/3”
- Injection-design ablation comparing baseline, recency, repetition, and framing at fixed window size.
  - Evidence: [b00171-a127db32a8] “The four designs: baseline (one forged line 75% into the session), recency (that line moved to the end), repeat 4× (the line planted at four points), and framed”

### Negative results

- An exact-substring provenance check caught attacks but destroyed summary utility by demoting most legitimate content.
  - Evidence: [b00154-b0a24f437d] “demanding an exact match against a user turn, caught nearly everything but demoted 72–100% of legitimate content”
- Repeating the forged line was counterproductive in the salience experiment.
  - Evidence: [b00176-198a9c85c5] “planting the same line four times drops execution to 0%”
- A credential-exfiltration payload did not execute in live testing despite laundering.
  - Evidence: [b00354-11dbbc9b11] “In live testing, a credential-exfiltration payload never executed, even with the approval laundered.”
- Forged assistant reasoning and fabricated supporting evidence generally failed to overcome a genuine skeptical audit.
  - Evidence: [b00198-1f5b881f25] “The audit’s decision, not the forgery’s presence, controls the outcome”


## Limitations

- Most staged experiments use real serializers and prompts but not the released applications end to end; only pi receives a full-product demonstration.
  - Evidence: [b00372-5e9a0cc879] “a generic downstream agent, not the released programs end to end (see §6), except E15”
- Execution rates have low precision because individual cells commonly contain only three to five runs.
  - Evidence: [b00360-d5ff063f96] “The execution rate is noisy at small n (3–5 runs).”; [b00360-d5ff063f96] “The numbers should be treated as direction, not precision.”
- The end-to-end result covers one harness and one model with a small paired sample, so its exact success fraction should not be generalized.
  - Evidence: [b00358-d0e771e4ac] “E15’s absolute numbers are small (six paired takes on one model)”; [b00358-d0e771e4ac] “what is solid is the mechanism and the paired 3/6-vs-0/5 separation, not the precise fractions.”
- Executed demonstrations are limited to OpenAI models; other model families were not tested at the execution stage.
  - Evidence: [b00352-b1c373c48c] “Other non-GPT models are untested at the execution stage.”
- Salience evidence is a within-model association at low sample size because the same model summarizes, judges salience, and acts.
  - Evidence: [b00356-679f52eedc] “both experiments run at n = 5 on that one model.”; [b00356-679f52eedc] “a within-model association rather than two independent instruments”
- The demonstrated command-execution regime lacks an external approval gate or enforced OS sandbox, limiting applicability to more constrained deployments.
  - Evidence: [b00374-478bae2f44] “Our agent loop has no approval gate or sandbox, so the RCE numbers measure the model’s decision in isolation”
- The defense has no adaptive evaluation and may be evaded by payloads that mimic the user’s language.
  - Evidence: [b00366-1aa47c1e0f] “The defense has not yet been subjected to an adaptive attack.”; [b00366-1aa47c1e0f] “one written to mimic the user’s own wording would likely evade the provenance-contrast check.”
- The defense’s clean corpus is small, recombination attacks are untested, and generic payloads may understate targeted-attack risk.
  - Evidence: [b00370-238fa2a4d2] “Recombination is untested [5], so every number here is a floor.”; [b00370-238fa2a4d2] “The clean corpus behind the false-positive rate is also small (4 sessions).”; [b00368-eca8a3b0d1] “Every measured poison is deliberately untailored.”

## Reproducibility

**Status:** strong

Reproducibility is strong for an empirical security paper because the authors report pinned upstream components, runnable code, raw table data, containment infrastructure, scoring code, recordings, and paired live artifacts. The strongest remaining gaps concern external validity and unperformed experiments rather than absence of the reported artifacts.

**Available artifacts**

- Public repository containing experiment harnesses and runners.
- Raw output behind every table.
- Pinned upstream prompts, serializers, sources, and commits for all nine harnesses.
- Containerized live demonstration with operator script, paired takes, recordings, session logs, and per-take digests.
- Scoring code and an independent adjudication record for the laundering judge.

**Missing pieces**

- A reported independent multi-model replication of the salience mechanism.
- Adaptive-attack evaluation for the provenance-contrast defense.
- End-to-end product runs for harnesses other than pi.
- Large-sample execution estimates and broader non-GPT execution coverage.
- A larger clean corpus for estimating defense collateral.
- Executed tests of recombination attacks and harms under enforced OS sandboxes.

## AIDB assessment

- Novelty: Moderate to high. The general memory-poisoning phenomenon is acknowledged as prior work, but the paper contributes a clear serializer-level causal account, a nine-harness structural control, executed consequences in the compaction channel, and a paired real-product demonstration.
- Usefulness: High for coding-agent implementers and security reviewers. The findings translate directly into design checks: retain typed roles, escape in-band markers, preserve provenance through summaries, keep external approval and sandbox gates, and test compaction with adversarial tool output.
- Confidence: high
- Recommended action: adopt
- Rationale: Adopt the structural mitigation—role-typed serialization or delimiter escaping—and add regression tests now. Treat the post-hoc provenance validator as defense in depth rather than a complete fix. Confidence is high in the existence and mechanism of the flaw, but only medium in precise execution-rate estimates because of small samples and limited end-to-end coverage.

## Uncertainties

- **The field prevalence of vulnerable serializer patterns is unknown beyond the nine selected harnesses.** — The paper demonstrates a class vulnerability but does not establish how common it is across proprietary agents, forks, later releases, or other agent categories.
  - Evidence: [b00049-6c5ecd7bd6] “We selected widely used harnesses of each class.”
- **The exact live success probability is unresolved.** — Deployment risk calculations should not treat the observed paired fraction as a stable population estimate.
  - Evidence: [b00358-d0e771e4ac] “what is solid is the mechanism and the paired 3/6-vs-0/5 separation, not the precise fractions.”
- **It is unclear how well the provenance-contrast defense withstands adaptive attackers or user-style mimicry.** — The reported catch rate may substantially overestimate protection after publication of the detector.
  - Evidence: [b00366-1aa47c1e0f] “So 77% is an upper bound against an attacker who is not adapting.”
- **The salience-to-execution relationship may partly reflect shared-model measurement bias.** — If an independent judge or different executor does not reproduce the association, the proposed attenuation mechanism would be weaker.
  - Evidence: [b00171-a127db32a8] “the salience-execution link here is a within-model association, not two independent instruments”
- **The demonstrated benign-canary execution rate does not determine rates for overtly harmful payloads.** — Operational severity depends on whether attackers can conceal harmful effects within apparently routine behavior.
  - Evidence: [b00354-11dbbc9b11] “The executed rates here are therefore an upper bound for high-stakes payloads”

## Open questions

- How prevalent are unescaped role-label serializers in proprietary agents and in downstream products derived from the five affected harnesses?
- Does delimiter escaping reduce forged-label laundering to an acceptably low level across all harnesses, models, label variants, encodings, and nested document formats?
- Can an adaptive attacker evade provenance contrast by matching genuine user vocabulary, paraphrasing prior turns, or splitting authority across multiple fragments?
- Do independent salience judges and heterogeneous acting models reproduce the size, recency, and execution relationships?
- What harms remain executable when network access, filesystem scope, approval prompts, and process isolation are enforced outside the model?
- How do repeated natural compactions, rather than directly invoked synthetic compactions, affect provenance and execution in long-lived real projects?

## Proposed AIDB experiments

- **Hypothesis:** Escaping every in-band role marker before flattening reduces forged-label laundering to the plain-text level without materially harming legitimate-summary fidelity.
  - Baseline: Unpatched serializer, plain-text payload without a forged label, and role-typed serializer control, evaluated on the same harness-model-transcript matrix.
  - Primary metric: Difference in laundering rate between patched forged-label and plain-text arms, with legitimate-summary retention as a co-primary safety metric.
  - Stop condition: Stop when confidence intervals are narrow enough to exclude a practically important excess over the plain-text arm, or when any patched harness shows a reproducible laundering pathway requiring redesign.
- **Hypothesis:** An adaptive attacker can reduce the provenance-contrast defense’s catch rate by matching the vocabulary and paraphrase style of genuine user turns.
  - Baseline: The published generic payload suite at the recommended provenance-contrast setting, plus clean summaries for collateral measurement.
  - Primary metric: Adaptive laundering escape rate at a fixed legitimate-claim demotion budget.
  - Stop condition: Stop after the adaptive attack reaches a stable plateau across held-out users and models, or immediately if escape becomes high enough that the defense no longer improves materially over the prompt baseline.
- **Hypothesis:** The reported salience-execution association generalizes when summary generation, salience judgment, and downstream action use different model families.
  - Baseline: The original single-model baseline, recency, repetition, and framing conditions at matched context sizes.
  - Primary metric: Command-issuance rate stratified by independently judged salience, with effect sizes and uncertainty across summarizer–judge–executor combinations.
  - Stop condition: Stop when the direction of the salience effect is replicated across multiple independent combinations with adequate precision, or when the association reverses or disappears in enough combinations to reject generality.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:35:32.380015+00:00`
- Document SHA-256: `558bdacf405e05aae7a46bdda179392cdc2efa1b4a5870c57010714be4388476`
- Metadata SHA-256: `c1c1b82355185451e5d3487874c633794e655447ca8f4a5ba15c9618de6bf819`
- Blocks: 399
- Deterministic repair attempts: 0
