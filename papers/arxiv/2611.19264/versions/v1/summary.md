# Read Boundaries in Agent Memory: Consistency, Completeness, and Repair

## Executive summary

The paper shows that protecting only an initial database operation is insufficient when an agent-memory recall performs later enrichment or materialization. Across controlled and open-arrival tests, whole-call locking and optimistic epoch validation prevent mixed-version Cognee evidence; a shared PostgreSQL snapshot fixes Hindsight’s cross-connection mismatch. Epoch trades shorter update tails for longer recall tails, while a persistent DIRTY state converts uncertain post-failure content into explicit refusal until recovery. The evidence is unusually careful about completeness, canonical publication, queues, and failed updates. Adoption should remain conditional: tests use one changing source, deterministic representations, one owner process, selected fault sites, and no downstream answer-quality evaluation.

## Problem

**Statement.** A memory service may assemble one response through multiple reads or stores. If an update occurs between those reads, the returned assertion and its cited source may belong to different revisions; an update failure can also leave derived and canonical state published differently.

**Why it matters.** Contradictory evidence undermines citation and audit, while locally coherent derived content after failure may still disagree with the canonical record. A repair must therefore distinguish compatibility, completeness, freshness, availability, and recovery rather than report only successful retrieval.

**Scope.** The study examines complete-recall protection in Hindsight and Cognee, including enrichment and lazy-result materialization, normal incremental and full-rebuild updates, selected update failures, service refusal, and recovery. It does not evaluate downstream model quality or establish behavior for multiple owner processes.

## Method

For Hindsight, the wrapper exports one read-only PostgreSQL Repeatable Read snapshot and imports it into every participating connection before its first query, keeping the exporter open through recall completion. For Cognee, the study compares ordinary recall, unconditional whole-call repetition, a writer-preference read/write lock held through materialization, and optimistic generation validation. Epoch readers accept a fully materialized response only when the generation remains the same, healthy, and even; failed or uncertain protected mutations leave the scope DIRTY until a successful later operation reopens it. Controlled interleavings, open-arrival workloads, and injected failures are evaluated with direct source bindings and backend receipts used for checking rather than response construction.

### Key components

- A compatibility predicate asks whether every current-state evidence item can be explained by one dependency-consistent source state; unresolved or empty evidence is labeled UNKNOWN.
- Cognee completeness requires passage, summary, city and employer graph assertions, and city and employer fact text. Usability additionally requires timely and compatible delivery.
- Gate holds shared read permission through awaited search and full materialization, while a writer holds exclusive permission through update and completion checks.
- Epoch records a healthy READY generation, performs and materializes the native recall, then validates that the same generation remains healthy; crossed reads are discarded and retried within the original deadline.
- Failure handling preserves a DIRTY state after failed or uncertain admitted mutations and explicitly refuses recall until successful recovery establishes a newer READY generation.

### Assumptions

- The evidence checker’s captured receipts and source relationships are sufficient to classify compatibility within the tested source scope.
- All relevant writers and background publication work participate in the selected protection scope, which has one owner process.
- The six-role representation contract is an appropriate completeness target for the evaluated Cognee workload, but it is not a proxy for answer quality.
- The tested stores safely tolerate the read/write overlap permitted by Epoch, while separate lifecycle guards protect resource lifetime.

## Main claims

- **The required protection boundary spans the recall’s first read through enrichment and materialization; connection-local transactions or locks released at entry do not cover later reads.**
  - Evidence: [b00007-42b939a9b6] “A transaction on one connection does not cover enrichment on another; a lock released at request entry leaves later graph reads exposed.”; [b00007-42b939a9b6] “Protection must span the recall’s first read through materialization of every lazy result.”
- **The proposed repairs preserve native evidence rather than constructing corrected responses: snapshots share one database view, Gate excludes writes across the whole call, and Epoch validates a completed read against service health and generation.**
  - Evidence: [b00008-6362626cec] “We protect complete recalls without changing the service’s returned evidence.”; [b00008-6362626cec] “Gate excludes writes through materialization; Epoch validates the completed read against a healthy generation.”
- **Compatibility, completeness, freshness, waiting, and failure service are distinct properties; a complete and locally compatible return can still disagree with canonical publication.**
  - Evidence: [b00026-51510c8ef8] “Criterion Question Measurement Compatibility Do the source revisions agree?”; [b00022-71c1f4d346] “A locally compatible and complete return can differ from that canonical record.”
- **After a protected update fails or has uncertain completion, the system deliberately refuses reads until a successful newer operation restores READY.**
  - Evidence: [b00046-9c31f4d98b] “Both protected policies keep the scope DIRTY after an admitted mutation fails or its completion is uncertain.”; [b00046-9c31f4d98b] “A successful recovery in a newer generation restores READY”

## Results

- **In open-arrival default-update workloads, ordinary recall produced 199 conflicting responses among 12,010 scheduled recalls for spaced writes and 284 among 12,010 for bursts; Gate and Epoch each delivered complete, compatible responses for all 24,020 scheduled recalls.**
  - Context: This is the strongest natural-load correctness comparison. It shows that incremental publication can preserve role coverage while still mixing revisions, whereas both whole-call protection strategies eliminate delivered incompatibility in the tested workloads.
  - Evidence: [b00071-660db71d7f] “199 of 12,010 scheduled recalls with spaced writes (1.66%) and 284 of 12,010 with bursts (2.36%).”; [b00073-bd32cda4c3] “Gate and Epoch each provide complete, compatible responses for all 24,020 scheduled default-update recalls.”
- **Unconditional repetition did not repair the controlled incremental-publication anomaly: in all twenty default read-first histories, the unprotected response and the delivered second response both conflicted.**
  - Context: This consequential negative result rules out a superficially simple retry policy. The repeated call had no checker, backoff, or fallback, so it could cross the same publication window again.
  - Evidence: [b00066-c9742f509a] “In all twenty default read-first histories, both the unprotected response and the delivered second response conflict”; [b00039-80894d8d57] “DOUBLE READ repeats the whole recall and delivers the second result, without a checker, backoff, or fallback.”
- **Under default bursts, Epoch’s mean run recall-p95 was 1,475 ms versus 1,185 ms for Gate, a 290 ms increase with 95% CI [48, 562]; its mean run update-p95 was 109 ms lower with interval [−168, −64].**
  - Context: Epoch shifts waiting away from an active reader body and toward readers that wait for stability or repeat invalidated work. The quantile contrast does not isolate how much each mechanism contributes.
  - Evidence: [b00078-15ecc12b35] “Mean run recall-p95 is 1,475 ms for Epoch and 1,185 ms for Gate: a paired increase of 290 ms, 95% CI [48, 562].”; [b00078-15ecc12b35] “Mean run update-p95 is lower by 109 ms [−168, −64].”
- **After incremental failure, unprotected and Double read each delivered fifty conflicting probes at P1 and fifty locally complete, compatible probes at P2 whose basis differed from canonical Data; Gate and Epoch refused every fault-stage probe. The first default retry restored all five usable probes in every one of the 80 fault runs through native full-rebuild fallback.**
  - Context: The result separates mixed revisions from coherent-but-unpublished derived state. Refusal protects publication-aware admission but sacrifices availability until a successful operation reopens service.
  - Evidence: [b00088-5c7c715ba0] “Unprotected and Double read each deliver fifty conflicting P1 probes.”; [b00088-5c7c715ba0] “At P2, each delivers fifty locally complete, compatible probes whose source basis differs from canonical Data”; [b00088-5c7c715ba0] “Gate and Epoch refuse every fault-stage probe.”; [b00089-166010c2e2] “The first default retry restores canonical v1 and all five usable probes in every fault run.”; [b00089-166010c2e2] “All 80 retries take the native full-rebuild fallback”
- **For Hindsight, sharing one PostgreSQL snapshot removed the controlled mismatch in all ten pairs, but median native-read p95 rose from 19.09 to 28.97 ms. The joint cost screen failed because the one-client recall-rate ratio was 0.790 against a 0.80 threshold.**
  - Context: The controlled correctness evidence is strong, while the natural workload had too few conflicts to estimate incident-frequency reduction. The throughput measurement concerns one-client completion rather than concurrent capacity.
  - Evidence: [b00092-a3fcfa68b2] “Sharing one PostgreSQL snapshot removes the Hindsight mismatch in all ten controlled pairs”; [b00093-f3350d6b68] “median native-read p95 rises from 19.09 to 28.97 ms (1.52-fold)”; [b00093-f3350d6b68] “the one-client recall-rate ratio is 0.790, below the 0.80 screen.”; [b00093-f3350d6b68] “the joint screen is therefore unmet.”

## Experimental evaluation

### Datasets

- Cognee main study: fresh-store runs using one changing source, deterministic extraction, and fixed low-dimensional embeddings; controlled schedules, open arrivals, and full-rebuild failure conditions are included.
  - Evidence: [b00049-c94e23415a] “The main Cognee evaluation comprises 600 fresh-store runs”; [b00049-c94e23415a] “Each uses one changing source with deterministic extraction and eight-dimensional embeddings.”
- Separate Cognee incremental-failure study covering two injected publication sites, controls, protected and unprotected policies, staged probes, and sequential recovery interventions.
  - Evidence: [b00056-815ff21d94] “At P1, a one-shot ordinary exception follows acknowledged new graph/vector writes”; [b00056-815ff21d94] “At P2, it follows that withdrawal and precedes canonical Data publication”; [b00056-815ff21d94] “Each site, condition, and policy has ten histories, giving 160 runs.”
- Hindsight controlled-pair, natural-workload, and no-write cost measurements over a PostgreSQL-backed installation with a connection pool.
  - Evidence: [b00059-3b104d194e] “Ten controlled pairs use four schedules in counts 3/3/2/2”; [b00059-3b104d194e] “Twenty natural workloads per condition each complete fifteen writes and at least sixty recalls”; [b00060-0fb2fbf3e2] “Snapshot cost is measured on five no-write pairs”

### Baselines

- Unprotected native recall: collects whichever evidence is visible during one call.
  - Evidence: [b00041-9919e69091] “Unprotected Collects visible evidence One call”
- Double read: repeats the whole recall and returns the second result without checking, backoff, or fallback.
  - Evidence: [b00039-80894d8d57] “DOUBLE READ repeats the whole recall and delivers the second result, without a checker, backoff, or fallback.”
- Gate: a writer-preference read/write lock providing whole-call reader/writer exclusion.
  - Evidence: [b00042-17e587d1d3] “GATE uses a writer-preference read/write lock.”; [b00042-17e587d1d3] “A reader holds permission through the awaited search and materialization”
- Epoch: optimistic validation against a stable healthy generation, with bounded retries and no fallback to Gate.
  - Evidence: [b00043-7573c26191] “It accepts only the same healthy even generation.”; [b00043-7573c26191] “At most eight attempts fit within the original request deadline.”

### Metrics

- Source compatibility C1 over nonempty evidence with resolved bindings; other returns are UNKNOWN.
  - Evidence: [b00022-71c1f4d346] “We evaluate C1 on nonempty evidence with resolved bindings; other returns are marked UNKNOWN.”
- Completeness through six role-presence flags and usable-by-deadline service requiring timely, compatible, complete delivery.
  - Evidence: [b00024-c5fa001f66] “Cognee’s completeness contract requires six roles”; [b00024-c5fa001f66] “A request is usable by deadline when it returns on time, has compatible source bindings, and contains all six.”
- Freshness lag, queue/gate/read/update duration, partial delivery, refusal, recovery probes, request-level service rates, and delivered-conflict rates.
  - Evidence: [b00026-51510c8ef8] “Freshness How old is the source basis? Lag against observed successful-update heads”; [b00026-51510c8ef8] “Waiting Where is time spent? Queue, gate, read, and update durations”; [b00028-c0fb0a086f] “Service rates count every scheduled request”; [b00028-c0fb0a086f] “Delivered-conflict rates instead use only classifiable delivered responses”
- Descriptive paired uncertainty intervals produced by clustered resampling of histories or workload runs.
  - Evidence: [b00062-621d6b5982] “Confidence intervals (CIs) are descriptive 95% percentile intervals from 10,000 paired cluster resamples”

### Ablations

- Four Cognee read policies are crossed with default incremental updates and explicit full rebuilds.
  - Evidence: [b00051-819454fcfe] “20 histories × 2 entrance orders × 2 update modes × 4 policies”
- Controlled read-first and write-first interleavings target distinct publication stages rather than estimating their natural frequency.
  - Evidence: [b00052-9e29c6f6d6] “Controlled read-first (AR) executions pause after the old passage is retrieved”; [b00052-9e29c6f6d6] “Write-first (AW) executions pause after an acknowledged mutation”
- Open-arrival write timing varies between spaced updates and a compact burst while preserving shared recall-arrival lists and concurrency limits.
  - Evidence: [b00053-99bbfba909] “Two write profiles differ only in update timing”; [b00053-99bbfba909] “Policies share arrival lists, four active recall slots, 64 pending slots, one FIFO writer, and ten warmups.”
- Failure experiments compare injected faults with controls at a full-rebuild deletion site and two incremental-publication sites, followed by default retry and explicit rebuild.
  - Evidence: [b00055-db76aab7c4] “Failure runs inject one exception after the first completed nonempty vector deletion in a full rebuild.”; [b00057-3552494607] “after a same-input default retry (S1), and after a subsequent explicit full rebuild (S2).”

### Negative results

- Double read fails to remove controlled incremental-publication conflicts.
  - Evidence: [b00066-c9742f509a] “Double read still returns conflicting evidence during default incremental publication.”
- Under full rebuild, the second Double read can become compatible yet remain incomplete because fact roles are absent.
  - Evidence: [b00069-db3209506d] “Under full rebuild, Double read’s second call becomes compatible but lacks fact roles.”
- The Hindsight snapshot passed its latency screen but missed the client-rate screen, so the predeclared joint screen was not satisfied.
  - Evidence: [b00093-f3350d6b68] “The latency condition passes and the client-rate condition does not; the joint screen is therefore unmet.”
- For spaced updates, the recall-tail contrast between Epoch and Gate was inconclusive under both update modes.
  - Evidence: [b00079-0524997aa2] “the 95% CI of the recall-tail difference between Epoch and Gate includes zero under both update modes.”
- An explicit rebuild after successful default-retry recovery added no observed content benefit.
  - Evidence: [b00089-166010c2e2] “It adds no observed content benefit after successful R1.”


## Limitations

- The workload uses fixed software versions, deterministic representations, and a single changing source, limiting semantic and deployment diversity.
  - Evidence: [b00106-d537ede13b] “The experiments use fixed versions, deterministic extraction and embeddings, and a single changing source.”
- Controlled repetitions demonstrate possible executions but cannot be interpreted as independent tasks or estimates of real incident frequency.
  - Evidence: [b00106-d537ede13b] “Controlled schedules establish possible executions; their repetitions are not independent semantic tasks or incident-rate samples.”
- Fault injection covers selected publication sites with ordinary exceptions, not crashes, cancellation breadth, or arbitrary corruption.
  - Evidence: [b00106-d537ede13b] “Fault coverage comprises the full-rebuild deletion site and two incremental publication sites, using ordinary exceptions rather than process crashes.”
- Representation completeness is not downstream answer quality, and the paper does not evaluate model behavior.
  - Evidence: [b00106-d537ede13b] “Six-role coverage is a service contract rather than downstream answer quality.”; [b00106-d537ede13b] “We did not test its serial single-connection Repeatable Read alternative, exhaustive cancellation/import failure, multi-owner safety, or downstream model behavior.”
- Neither protected policy repairs already-inconsistent content or guarantees freshness through later consumption.
  - Evidence: [b00106-d537ede13b] “Neither policy repairs pre-existing inconsistency or guarantees freshness until later consumption.”
- Update-tail estimates rest on few writes, and one congestion episode has an unmeasured cause on a memory-constrained desktop snapshot.
  - Evidence: [b00106-d537ede13b] “update-run tail estimates use three or four writes.”; [b00106-d537ede13b] “the cause of an early congestion episode is unmeasured.”
- The implementation scope has one owner process; extension to multiple workers needs shared generation and health state, full writer participation, and safe resource lifetimes.
  - Evidence: [b00104-70544949f0] “Our scope has one owner process.”; [b00104-70544949f0] “Extending either policy to several workers requires shared generation and health state, participation by every writer and background publisher, and safe backend-resource lifetimes.”

## Reproducibility

**Status:** partial

Reproducibility is stronger for the Cognee experiments because the environment, schedules, policies, fault sites, accounting rules, and statistical procedure are unusually explicit, and code plus data are declared available. It remains partial because the artifact was not inspected here, Hindsight cost-environment details are missing, and no independent reproduction is reported.

**Available artifacts**

- The paper states that code and data are publicly available in a named repository.
- Cognee software, dependency versions, host operating system, CPU count, memory, workload schedules, deadlines, failure sites, resampling count, and one resampling seed are reported.
- Referenced Hindsight and Cognee revisions are identified in the supplied references.

**Missing pieces**

- Hindsight’s exact contemporaneous hardware is unavailable.
- Hindsight’s Python and asyncpg microversions are unavailable.
- The supplied blocks do not report an independent artifact reproduction or cross-host replication.
- The natural-language statement of artifact availability does not establish artifact completeness, executability, or archival permanence.

## AIDB assessment

- Novelty: The main novelty is systems-level localization of the read boundary in existing agent-memory services, combined with empirical separation of evidence compatibility, role completeness, canonical publication agreement, availability, and recovery admission. The mechanisms themselves adapt established snapshot, lock, and sequence-counter ideas; the contribution is their end-to-end placement and evaluation across heterogeneous recall stages.
- Usefulness: High for designers of memory, retrieval, and provenance services whose responses span multiple connections or stores. The paper provides actionable contracts and exposes why naive repetition and local consistency checks are insufficient. Production selection between Gate and Epoch still requires workload-specific latency, concurrency, crash, and multi-worker testing.
- Confidence: high
- Recommended action: read
- Rationale: The controlled comparisons, exhaustive request accounting, separate failure study, and explicit negative results support the central claim within the tested scope. AIDB should treat it as strong evidence for whole-recall protection and publication-aware recovery, but not as sufficient evidence to adopt a particular policy across production systems because the workload, ownership model, fault model, and semantic evaluation are narrow.

## Uncertainties

- **The real-world incidence of mixed-version responses is unresolved.** — Controlled schedules prove reachability, while the Hindsight natural workload produced too few events for a stable frequency comparison. Deployment benefit depends on actual update timing, recall concurrency, and publication duration.
  - Evidence: [b00092-a3fcfa68b2] “Natural workloads yield too few events to compare frequency”; [b00106-d537ede13b] “their repetitions are not independent semantic tasks or incident-rate samples.”
- **Epoch’s production advantage over Gate is workload-dependent and its measured tail differences do not reveal individual causal components.** — Epoch improves the measured writer tail during one burst condition but lengthens the reader tail and performs discarded work; capacity and queue interactions may change with host and workload.
  - Evidence: [b00078-15ecc12b35] “quantile differences do not identify its individual causes.”; [b00080-0ce74c2364] “This small discard count does not measure prevented errors.”
- **It is unknown whether the policies remain safe and effective with multiple processes, nonparticipating publishers, or store implementations that cannot tolerate overlap.** — These conditions are common in scaled services and violate assumptions behind process-local generation state and lifecycle protection.
  - Evidence: [b00104-70544949f0] “A shared lock alone would not supply all three.”; [b00104-70544949f0] “Epoch additionally depends on the stores tolerating the read/write overlap it validates.”
- **The impact of coherent-but-canonically-unpublished evidence on end-user answers is not measured.** — A strict refusal may be preferable for audit-sensitive callers but unnecessarily reduce availability for callers that can consume explicit degraded-state metadata.
  - Evidence: [b00100-51fde8a331] “A DEGRADED interface could expose available content together with missing roles or publication status if callers can interpret those distinctions.”; [b00106-d537ede13b] “Six-role coverage is a service contract rather than downstream answer quality.”

## Open questions

- How do Gate, Epoch, and shared snapshots behave under realistic multi-source updates, heterogeneous document sizes, nondeterministic extraction, and production embedding dimensions?
- Can generation and health metadata be made safe across multiple workers and every background publisher without introducing a new single point of failure?
- Would build-then-swap provide a better availability and latency envelope once storage duplication and old-generation reclamation are included?
- Which caller classes should receive strict DIRTY refusal, and which can safely consume a typed DEGRADED response with publication status and missing-role metadata?
- How robust are recovery guarantees under process crashes, cancellation races, snapshot-import failures, and failures during the recovery operation itself?
- Do evidence-consistency repairs measurably improve citation correctness, answer quality, or audit outcomes in downstream agent tasks?

## Proposed AIDB experiments

- **Hypothesis:** A shared, durable generation protocol preserves the zero-delivered-conflict property of Epoch across multiple worker processes and background publishers without materially reducing usable service.
  - Baseline: Single-owner Epoch and multi-worker unprotected recall under identical multi-source update and recall traces.
  - Primary metric: Usable-by-deadline fraction, accompanied by delivered-conflict fraction and recovery time after worker termination.
  - Stop condition: Stop adoption if any protected response has incompatible source bindings, if a worker crash permits READY while publication is incomplete, or if usable-by-deadline service is worse than the single-owner baseline by more than a predeclared margin.
- **Hypothesis:** Build-then-swap reduces recall-tail inflation and DIRTY refusal time relative to Gate and Epoch while retaining compatible, complete evidence.
  - Baseline: Gate and Epoch under the same spaced, burst, and injected-failure schedules.
  - Primary metric: Usable-by-deadline fraction across all scheduled recalls, with storage amplification and update-p95 as required secondary constraints.
  - Stop condition: Stop if any mixed-generation response is delivered, old-generation resources are reclaimed before all readers finish, or the predeclared storage or update-tail budget is exceeded.
- **Hypothesis:** A typed DEGRADED response after failed publication improves task availability without misleading callers when canonical disagreement and missing roles are explicit.
  - Baseline: Strict DIRTY refusal and unprotected native delivery after the same injected failures.
  - Primary metric: Downstream source-attribution accuracy on audit tasks, reported jointly with completed-task fraction.
  - Stop condition: Stop if DEGRADED responses reduce attribution accuracy relative to strict refusal, conceal canonical disagreement, or fail to improve completed-task fraction by the predeclared minimum.

## Provenance

- Schema: `paper-summary-v1`
- Profile: `deep`
- Provider: `codex-exec:configured-default`
- Generated: `2026-11-20T08:10:10.284531+00:00`
- Document SHA-256: `b2e927227c8d7084e254a5ebb0c296f331954f93a9c08d201f5be2f20f77cd25`
- Metadata SHA-256: `d29bef76544ecd96f7a291a72066027334537a79ac99fd81c8a8e0d99b351011`
- Blocks: 129
- Deterministic repair attempts: 0
