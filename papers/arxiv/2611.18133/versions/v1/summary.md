# Forget the Lineage: Forward-Secure, Lineage-Complete Cryptographic Erasure for LLM-Agent Memory

## Executive summary

The paper identifies a real erasure gap: deleting an input or its key leaves model-written descendants, vectors, storage residue, and backups. LinEra derives object and vector-shard keys along a recorded lineage graph; puncturing one object’s PPRF point makes its closure unreadable after later storage-and-key compromise. Controlled replays show zero recovered canaries under the sound lineage rule, while logical, per-object, epoch, and attributed alternatives leak. The central trade-off is severe: broad writer contexts create large erasure closures and sharply reduce facts-only utility. Four-turn writing and re-derivation mitigate this in the tested workloads. The formal model and artifacts are unusually strong, but deployment validity depends on complete prompt capture, protected pre-forget state, and assumptions excluding weights, contemporaneous RAM, side channels, and prior exports.

## Problem

**Statement.** LLM-agent memory contains model-generated facts, summaries, embeddings, and later derivatives. Erasing only the user-designated source does not erase these descendants or copies retained in database pages, vector indexes, and backups.

**Why it matters.** The adversary considered may later obtain all storage ever written and the store’s current secret state. Ordinary deletion and object-local encryption therefore fail when readable descendants retain information from a forgotten source.

**Scope.** The work addresses confidentiality of external agent memory and its lineage closure. It does not claim machine unlearning, protection of model weights, contemporaneous RAM, process side channels, or erasure of copies exported before the request.

## Method

LinEra represents sources and derived memories as a lineage DAG. The sound rule records every plaintext object visible in the writer’s context as a parent. Source and object-specific key material comes from a GGM puncturable PRF; derived keys combine parent keys and the object’s own PRF value through HKDF. Contents use authenticated encryption, parent tags are bound as associated data, and vector shards derive keys from all members. Forgetting punctures the selected tag, making the object and every descendant key unrecoverable without locating descendants. Re-derivation and small-context writing are proposed to recover utility and limit closure size.

### Key components

- LC-FS security game exposing all historical ciphertexts, the clear lineage graph, and the current secret state after adaptive forgetting.
- Context-confinement lemma connecting prompt-visible inputs to the closure that may depend on a source.
- PPRF-rooted key graph with HKDF derivation along parent edges and object-local puncture points.
- AEAD binding of ciphertexts to tags and parent lists, plus lineage-dependent encrypted vector shards.
- Crash-consistent state replacement, background rotation/compaction, and a mem0 adapter that captures retrieved memories and recent messages.
- Empirical evaluation of leakage channels, forgetting radius, retrieval and answer utility, re-derivation, writer context, model family, and system cost.

### Assumptions

- Sources are modeled as independent random variables for the context-confinement lemma; repeated information in another source is not erased by forgetting one source.
- The lineage hook sees every plaintext object supplied to the writer; memory accessed outside the framework can escape the recorded closure.
- The pre-forget secret state is unavailable to the adversary, while all historical storage and the current state may be obtained later.
- The main proof models the generator components and HKDF as independent random oracles and assumes one-time IND-CPA security for AEAD; the standard-model result uses additional PRG, block-keyed-PRF, key-separation, and AEAD assumptions.
- Security concerns stored external memory, not knowledge already present in model weights, copies made before forgetting, RAM at the request moment, or runtime side channels.

## Main claims

- **Under the sound lineage rule, every object whose content can depend on a forgotten source lies inside that source’s lineage closure, subject to the stated independence and writer-model assumptions.**
  - Evidence: [b00046-34c6ca87a4] “Then, for every source s, the joint content of all objects outside 𝖢𝗅⁡({s}) is a function of the other sources, θ and the writer randomness; hence it is independent of the content of s.”
- **LinEra’s construction makes a single puncture disable decryption of the selected object’s full descendant closure without first finding those descendants.**
  - Evidence: [b00077-e8dea860a0] “After 𝖯𝗎𝗇𝖼𝗍𝗎𝗋𝖾⁡(S,ts), no descendant of s can be decrypted, and the store never has to find them.”
- **The paper proves LC-FS confidentiality and lineage integrity under its cryptographic models, with a standard-model variant that incurs polynomial loss.**
  - Evidence: [b00099-581330af02] “Theorem 1 (LinEra is LC-FS secure).”; [b00104-ee59420cc0] “The random oracles can be removed.”; [b00104-ee59420cc0] “the loss is polynomial (a factor C′​N​ℓ, Theorem 3).”; [b00106-a7f181ac62] “Without the secret state, an adversary that modifies the storage cannot make Get(t) return a content other than the one stored for t”

## Results

- **In the main LoCoMo replay, logical deletion exposed all 35 forgotten canaries through some channel; per-object and epoch encryption exposed 22 of 35; the attributed LinEra rule exposed 3; the sound rule exposed 0, while erasing 526 objects.**
  - Context: This is the strongest same-memory controlled comparison: every scheme replayed identical model-written texts, changing only lineage and cryptography. It shows that encryption limited to the requested object removes storage residue but not model-generated descendants.
  - Evidence: [b00129-ecd7bacecc] “Logical deletion + soft-deleted HNSW 14 35 26 22 35 35”; [b00129-ecd7bacecc] “Per-object keys (no lineage) 14 0 8 22 22 35 Epoch keys 14 0 8 22 22 35”; [b00129-ecd7bacecc] “LinEra, attributed rule 0 0 0 3 3 56 LinEra, sound rule 0 0 0 0 0 526”
- **With the larger writer across all ten LoCoMo conversations, logical deletion leaked 70 of 71 canaries and per-object or epoch keys leaked 67, whereas the sound rule leaked none in either session or four-turn writing.**
  - Context: The extension covers the full LoCoMo set and a larger model. It supports robustness across model size and writing strategy, though it remains an evaluation with open models and planted canaries.
  - Evidence: [b00160-e0585ed191] “on all ten LoCoMo conversations (272 sessions, 5,953 turns, 71 canaries from the same templates and seed)”; [b00162-af3649059b] “Logical deletion leaks 70 of them through some channel, and per-object and epoch keys 67, entirely through the model’s copies”; [b00162-af3649059b] “The sound rule leaks none in either setting.”
- **Writer fan-in governed the erasure radius: for the larger writer, forgetting 1% of turns erased 73.0% of session-written memories, versus 3.8% with four-turn windows; at a 10% forget rate, the windowed radius was 32.7%.**
  - Context: This is both a validity threat and a system-design result. Sound lineage can destroy most derived memory when summaries repeatedly ingest broad context, while bounded windows sharply localize erasure.
  - Evidence: [b00164-0273d0f89c] “forgetting 1% of the turns erases 73.0% of the derived memories, against 77.2% predicted by the fan-in law.”; [b00164-0273d0f89c] “Four-turn windows bring the fan-in down to 3.8 and the radius to 3.8% (predicted 3.8%), and to 32.7% at 10%.”
- **The sound rule substantially reduced facts-only answer utility for session summaries, but re-derivation restored it: on 1,323 LoCoMo questions, F1 moved from 27.8 without forgetting to 13.8 after forgetting 1%, then to 27.9 after re-derivation; at 10%, it moved to 2.0 and then 27.3.**
  - Context: The comparison isolates utility after excluding questions whose evidence was intentionally forgotten. Restoration required rewriting affected sessions, so the recovered quality is accompanied by model-call latency and cost.
  - Evidence: [b00166-46536e1f34] “Over 1,323 LoCoMo questions (bootstrap standard deviation about 0.9 points), the session writer reaches F1 27.8 without forgetting.”; [b00166-46536e1f34] “The sound rule drops it to 13.8 at 1%”; [b00166-46536e1f34] “Re-derivation restores it: F1 27.9 at 1% (169 sessions, 19 minutes) and 27.3 at 10% (272 sessions, 27 minutes).”; [b00166-46536e1f34] “and to 2.0 at 10%, where none does.”
- **Four-turn writing improved the tested quality–erasure trade-off: F1 was 31.8 without forgetting, 30.7 after forgetting 1%, and 26.6 after forgetting 10%; re-derivation returned it to 31.8 and 31.9.**
  - Context: This controlled design variant suggests that sound erasure need not impose a large answer penalty when writer context is deliberately bounded. It also increases the number of short writer calls and may not transfer to tasks requiring broad synthesis.
  - Evidence: [b00166-46536e1f34] “the windowed writer answers better even without forgetting (31.8), keeps 30.7 at 1% and 26.6 at 10% under the sound rule”; [b00166-46536e1f34] “and returns to 31.8 and 31.9 after re-deriving 57 and 498 short windows.”

## Experimental evaluation

### Datasets

- LoCoMo long-conversation benchmark, evaluated in a main subset and an extended full-conversation campaign with planted canary turns.
  - Evidence: [b00121-d5d00fd36c] “We replay LoCoMo [40], a benchmark of very long two-person conversations.”; [b00160-e0585ed191] “on all ten LoCoMo conversations (272 sessions, 5,953 turns, 71 canaries from the same templates and seed)”
- LongMemEval-S, first as a seeded subset and later as a larger set of histories spanning four question types.
  - Evidence: [b00150-018b34cc36] “We repeated phases A and B on a seeded subset of LongMemEval-S [41]”; [b00160-e0585ed191] “on 100 LongMemEval-S histories (25 questions of each of the four types).”

### Baselines

- Logical deletion with plaintext rows and a soft-deleting HNSW index.
  - Evidence: [b00114-1086892a98] “logical deletion (plaintext rows and an HNSW index [33] from hnswlib with soft deletion, as offered by hnswlib)”
- Per-object GGM keys without lineage, modeled after object-local cryptographic deletion.
  - Evidence: [b00114-1086892a98] “per-object keys (a GGM key per object, no lineage, in the spirit of Holepunch [5])”
- Epoch encryption in which forgetting re-encrypts remaining objects and destroys the old epoch key.
  - Evidence: [b00114-1086892a98] “epoch keys (one key per epoch of five sessions; a forget re-encrypts the rest of the epoch and destroys the old key”
- LinEra with embedding-based attributed lineage, used as a weaker utility-oriented alternative to the sound rule.
  - Evidence: [b00042-1a9319842c] “in our experiments, the three context objects whose embeddings are closest to d.”

### Metrics

- Four post-forgetting leakage channels: readable exact secrets, exact secrets in raw file bytes, identification from vectors against decoys, and topic-bearing readable descendants.
  - Evidence: [b00127-8410d086c2] “tries four channels: (i) records it can read or decrypt that contain the exact number or word;”; [b00127-8410d086c2] “(ii) the exact secret anywhere in the raw bytes of the files”; [b00127-8410d086c2] “(iii) the vectors it can read or decrypt”; [b00127-8410d086c2] “(iv) a readable descendant of the canary turn (ground truth: the model saw it) that mentions the canary’s topic.”
- Forgetting radius: the share of derived memories erased after randomly forgetting source turns, averaged over repeated seeds.
  - Evidence: [b00132-57dac1b425] “Radius: share of derived memories erased when a random fraction of turns is forgotten (mean of 3 seeds).”
- Retrieval utility measured by whether a top-10 result comes from an evidence session.
  - Evidence: [b00139-42623a1783] “share of retained questions for which a top-10 hit comes from an evidence session (mean of 3 seeds).”
- Answer quality measured with token F1, accompanied by unknown-answer rates and re-summarization counts.
  - Evidence: [b00143-7681b1c579] “Answer quality from the surviving memory (token F1, %), share of “unknown” answers (%) and number of sessions re-summarised.”
- System measurements include write, read, search, forget, secret-state size, rotation, database size, and closure size.
  - Evidence: [b00177-7c66088121] “Write includes the vector index; search is a warm top-10 scan over all shards; forget includes the closure, the puncture, the atomic state write and the shard rebuilds”

### Ablations

- Sound lineage versus attributed top-context lineage isolates the security–utility effect of complete prompt capture.
  - Evidence: [b00125-e5ba2902e5] “LinEra with the attributed and the sound rule”
- Session summaries are compared with windows ranging from two to sixteen turns, testing the proposed fan-in mechanism without fitting its prediction.
  - Evidence: [b00152-2bd394b160] “Table 5 and Fig. 2 vary the window from 2 to 16 turns on conversations 0 and 1.”; [b00152-2bd394b160] “The fan-in law holds at every size, with no fitted parameter.”
- Re-derivation is compared with leaving the post-forgetting memory depleted.
  - Evidence: [b00146-e05cccf42b] “Re-derivation removes the loss”
- Facts-only and hybrid stores test whether retaining encrypted raw turns buffers retrieval loss.
  - Evidence: [b00138-b44e1a4b67] “We use two views of the store: facts-only, where the agent retrieves derived memories only (as mem0 does), and hybrid, where the encrypted raw turns are also retrievable.”
- A second model family and a larger writer test whether findings persist beyond the main writer configuration.
  - Evidence: [b00119-756990c6cc] “we repeat the main runs on two conversations with Llama-3.2-3B-Instruct [37] (4 bits).”; [b00119-756990c6cc] “replays everything with a larger writer, Qwen2.5-7B-Instruct in 16-bit precision”

### Negative results

- Logical deletion failed completely against storage residue in the main canary test.
  - Evidence: [b00130-7f2800cb27] “Logical deletion loses everything: the deleted turns stay in free SQLite pages (35 of 35)”
- Per-object and epoch encryption removed residue but left model-generated copies readable.
  - Evidence: [b00130-7f2800cb27] “Encryption with per-object or epoch keys removes these storage residues, but not the model’s copies”
- Attributed lineage preserved more utility but missed genuine influence and leaked topics.
  - Evidence: [b00130-7f2800cb27] “the attribution function missed the canary turn when the model folded it into a summary.”
- Sound lineage with broad session contexts caused a collapse in facts-only retrieval after a small forget rate.
  - Evidence: [b00142-863cd16e07] “The sound rule makes the facts-only store collapse, from 63.2% to 18.9% at 1%”
- The implementation’s warm exhaustive vector scan is identified as the dominant scaling cost rather than a production-ready search design.
  - Evidence: [b00179-7681388af7] “The warm search scan over all shards (326 ms at 106) is the main cost and would use an approximate index per shard in production.”


## Limitations

- The empirical study is limited to open models no larger than 7B parameters; frontier-model copying behavior is untested.
  - Evidence: [b00189-89202c13c8] “Our LLM experiments use open models of at most 7B parameters”; [b00189-89202c13c8] “Frontier models may copy secrets verbatim more or less often”
- Answer outputs vary with inference engine and hardware, so the authors restrict comparisons to conditions computed within the same table and machine.
  - Evidence: [b00189-89202c13c8] “rerunning the same quantised model on another CPU changed a few answers”; [b00189-89202c13c8] “we compare conditions only within a table computed on one machine.”
- The lineage graph, object sizes, and creation times remain visible and may leak structural metadata.
  - Evidence: [b00110-6623fb5826] “The lineage graph, object sizes and creation times are in clear”
- Complete security depends on capturing the entire writer prompt; external tools or uninstrumented memory access bypass lineage recording.
  - Evidence: [b00189-89202c13c8] “Lineage capture assumes that the hook sees the whole prompt; tools that read memory outside the framework would bypass it.”
- The threat model excludes model weights, RAM at forgetting time, process side channels, and copies exported before the request.
  - Evidence: [b00051-7f7587d5f3] “RAM content at the very moment of forgetting, side channels on the running process and the model weights are out of scope.”; [b00110-6623fb5826] “The scheme also does not protect the model weights, RAM at the time of forgetting, or copies made before the request”
- The standard-model construction requires key separation that the measured implementation does not use; the implementation is covered by the random-oracle theorem instead.
  - Evidence: [b00281-564a0dc412] “This costs one HKDF call per object; our implementation and measurements use ko directly, which the random-oracle theorem covers.”
- Small-context writing increases the number of model calls and has only been tested on the supplied conversational-memory settings; broad synthesis tasks may behave differently.
  - Evidence: [b00136-ee5840b3d4] “214 short calls instead of 38 long ones”

## Reproducibility

**Status:** strong

Reproducibility is strong for a paper artifact: code, call logs, model digests, generators, scripts, seed, and an archival identifier are stated. The strongest results can in principle be replayed without regenerating all model outputs because schemes share logged texts. Confidence should remain below independent-replication level because the analysis supplied here does not execute the artifacts, datasets are external, hardware-sensitive answers are acknowledged, and the proposed production search path is not benchmarked.

**Available artifacts**

- Public LinEra implementation and baseline implementations.
- Canary generator and logs of every LLM call, including prompts, outputs, and model-file digests.
- Scripts claimed to produce every reported number and table.
- Archived Zenodo release and mirrored repository.
- Declared random seed and detailed model, quantization, inference-engine, hardware, embedding, and dataset settings.
- Test suite covering puncturing, serialization, closure erasure, post-forget theft, compaction, lineage tampering, deep key derivation, shards, backups, and the mem0 adapter.

**Missing pieces**

- The supplied blocks do not report an independent reproduction by unaffiliated researchers.
- The datasets are not redistributed; scripts depend on downloading them from their original sources.
- The paper does not provide repeated end-to-end LLM generation across multiple random seeds; repeated seeds are stated for selected forgetting-radius measurements.
- The production approximate vector index suggested for scaling is not evaluated.

## AIDB assessment

- Novelty: High within the paper’s framing: the key contribution is not puncturable deletion alone, but cryptographic key dependence over a model-generated derivation DAG plus a lineage rule connecting prompt exposure to the closure that must be erased. The paper also combines formal confidentiality, lineage integrity, vector handling, crash consistency, and an agent-memory integration.
- Usefulness: High for architects of privacy-sensitive agent memory. It supplies a concrete threat model, a deployable storage abstraction, clear failure cases for common deletion designs, and an actionable design rule: bound writer fan-in and re-derive after forgetting. Adoption requires reliable whole-prompt instrumentation and acceptance of visible lineage metadata.
- Confidence: medium
- Recommended action: read
- Rationale: The paper merits close reading and prototype evaluation: it offers unusually coherent formal and empirical evidence, controlled same-text comparisons, multiple writer configurations, and strong artifact claims. Immediate adoption would be premature because the central guarantee is conditional on complete lineage capture and protected pre-forget state, the implementation differs from the standard-model variant, production vector search is unevaluated, and no independent reproduction is supplied.

## Uncertainties

- **Whether the zero-leakage empirical result generalizes to frontier models, multimodal memories, tool-heavy agents, and non-conversational workflows.** — The cryptographic guarantee is writer-independent only when lineage is sound, but operational leakage and erasure radius depend on what the writer copies and how much context it consumes.
  - Evidence: [b00189-89202c13c8] “Frontier models may copy secrets verbatim more or less often, which changes how much the baselines leak but not the guarantee of LinEra.”
- **Whether a production agent can ensure complete lineage capture across every retrieval path, plugin, cache, tool result, and side store.** — A missed plaintext dependency falls outside the cryptographic closure and defeats the semantic claim even if the encryption layer works correctly.
  - Evidence: [b00189-89202c13c8] “tools that read memory outside the framework would bypass it.”
- **How much sensitive structural information can be inferred from the clear lineage graph, sizes, and timing metadata.** — The scheme hides content but explicitly leaves relationship and activity metadata visible; the paper does not quantify attacks on that metadata.
  - Evidence: [b00110-6623fb5826] “After forgetting, the adversary therefore learns that some object with k children existed, but not its content.”; [b00110-6623fb5826] “Hiding the graph would require encrypting it under a key that is itself forward-secure; we leave this to future work.”
- **Whether the standard-model key-separated variant preserves the measured performance and operational behavior.** — The evaluated implementation uses object keys directly, whereas the stronger proof variant adds derivation work and a different key-use discipline.
  - Evidence: [b00281-564a0dc412] “In the standard model we use the usual separation: the AEAD key of o is HKDF⁡(ko,"lf/enc")”; [b00281-564a0dc412] “This costs one HKDF call per object”
- **Whether re-derivation can accidentally recreate semantically equivalent forgotten information from correlated surviving sources.** — The formal argument excludes dependence on the forgotten source under source independence, but repeated or correlated information in other sources remains available by design.
  - Evidence: [b00049-9765b933e8] “information about s that other sources also carry (if Alice repeats her code in another message, forgetting one message does not forget the code)”

## Open questions

- Can lineage structure, object size, and timing be hidden while preserving forward-secure derivation and efficient retrieval?
- How should storage-level erasure compose with machine unlearning when information has entered model weights or adaptation state?
- Can whole-prompt lineage capture be enforced and audited across tools, caches, retrieval services, multimodal inputs, and third-party agent components?
- Does small-context writing retain its utility advantage on tasks requiring cross-session synthesis, long-horizon planning, or conflict resolution?
- What is the end-to-end cost of the key-separated standard-model variant with a production approximate vector index and hardware-backed secret state?

## Proposed AIDB experiments

- **Hypothesis:** An instrumented whole-agent deployment can detect every plaintext dependency used by memory writers, including tool and cache paths, with no unrecorded derived-memory influence.
  - Baseline: The paper’s mem0 wrapper, which captures store retrievals and recent messages visible to the extractor.
  - Primary metric: Fraction of derived objects whose observed information-flow dependencies are all present in their recorded parent sets, measured by controlled taint injection across retrieval, tool, cache, and side-store paths.
  - Stop condition: Reject deployment readiness if any controlled taint influences a derived object without its source being recorded as an ancestor; otherwise continue until every supported integration path has been exercised repeatedly without a miss.
- **Hypothesis:** Key separation and per-shard approximate indexing preserve LinEra’s erasure behavior while reducing search latency without materially increasing write or forget cost.
  - Baseline: The measured implementation using object keys directly and a warm exhaustive scan over encrypted shards.
  - Primary metric: Post-forget leakage success, search recall at fixed latency, and end-to-end write, search, forget, compaction, and state-storage cost across increasing object counts.
  - Stop condition: Stop if any forgotten closure becomes decryptable, stale shards reveal vectors, search recall falls below the chosen service threshold, or latency fails to improve over exhaustive scanning at production scale.
- **Hypothesis:** Bounded-context writing retains its lower erasure radius without sacrificing quality on workloads that require cross-session synthesis.
  - Baseline: Session-level summaries with retrieved prior summaries, compared against fixed small windows and a hierarchical bounded-fan-in writer.
  - Primary metric: Answer token F1 or task-specific exact accuracy on surviving-evidence questions, jointly reported with leakage count, forgetting radius, model calls, and re-derivation cost.
  - Stop condition: Reject the bounded-context design if it leaks any sound-lineage canary or if its quality confidence interval is materially below the session baseline at the predeclared forget rates; accept only if radius reduction and quality preservation both replicate across model families and task types.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:55:46.689798+00:00`
- Document SHA-256: `278bc1dee85105fc36cfdd0459efd608a97b8fe01f3a2c96700c83e451b050eb`
- Metadata SHA-256: `96494c86decc7dbde3b1154f5cd5ef8ffa725d6007a82280cd224bf342f0488c`
- Blocks: 292
- Deterministic repair attempts: 0
