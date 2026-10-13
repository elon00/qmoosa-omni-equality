# OEQ Evidence-First Global Integration Blueprint
Version: 1.0 | Date: 2026-10-13 | Status: PROPOSED, NOT IMPLEMENTED | Mainnet: BLOCKED

## Decision record
OEQ is a proposed citizen-centered identity, legal-access, allocation, and auditable economic governance protocol. Adoption of a standard does not imply recognition or endorsement by courts, governments, UN bodies, central banks, or standards organizations. No spending, deployments, or identity enrollment is authorized by this document.

## Prime Directive: evidence over claims
- Do not introduce mock/stub/fake responses, hardcoded success statuses, invented transaction IDs, dummy institutional approvals, prerecorded chain responses, or artificial oracle values into production paths or acceptance reports.
- Never describe statevector quantum computation, agent-based economic models, synthetic datasets, JavaScript arithmetic checks, or a local EVM as real physical quantum hardware, live economic evidence, formal verification, or public-network transactions.
- Separate verification types: STATIC, UNIT, CRYPTO_INTEROP, LOCAL_EVM, FORMAL_PROOF, EXTERNAL_DATA, PUBLIC_TESTNET, INDEPENDENT_AUDIT, MAINNET. None may substitute for another.
- On missing external credentials, unavailable data, failed signature checks, untrusted institutions, stale feed, missing license, contradictory evidence, or unsafe proposal: return BLOCKED and log a redacted reason. Never automatically fall back to mock or demo data.
- Every machine-generated claim needs source URI, source identity, timestamp, license, digest, parser version, verification method, and evidence classification.
- An autonomous agent cannot sign, send legal notices, register humans, move money, change policy, or deploy contracts without explicitly scoped authenticated human approval.
- Do not spend gas, ICP cycles, cloud compute, or buy subscriptions. GitHub branch/PR changes only; hard-stop if tool requires payment.

## 5W1H
WHAT: Standards-compliant system for verifiable citizen credentials, legally reviewed assistance, documented resource evidence, auditable token accounting and democratic governance.
WHY: Reduce administrative opacity and exclusion with inspectable decisions, not guaranteed social or economic outcomes.
WHO: Verified citizens, consent-based issuers, qualified legal professionals, NGOs, researchers, auditors, and opt-in institutional partners.
WHERE: Initially narrow jurisdiction and permitted datasets; expansion only after legal and privacy reviews.
WHEN: Sequential gates, never concurrent mainnet deployment.
HOW: Modular service contracts, verified identity and policy, robust data provenance, reproducible CI, independent review.

## Root risk register (must be addressed before feature work)
P0-01 Bespoke ML-DSA: current custom verify routine fails to establish knowledge of the private key, allowing signature construction from public data. Disable as authentication. Replace with independently maintained standard ML-DSA-65 implementation; FIPS 204 test vectors, invalid signatures, malformed data, swapped keys, interop, constant-time implementation and secret handling review. No self-written replacement.
P0-02 Governance: dynamic_governance currently accepts arbitrary citizen_id strings as voters and computes 60% among submitted votes. Require independently authenticated eligible voter registry/snapshot, authorized proposer, unique nullifier per poll, replay protection, signed votes, explicit quorum, eligibility and snapshot binding, immutable voting window and audit trail. Use integer arithmetic for thresholds.
P0-03 Solidity: current scripts/verify_contracts.js compiles bytecode, but 'invariants' are standalone JS computations, not EVM-executed tests or machine-checked proofs. Rename accurately, add Foundry/EVM deployment lifecycle tests, fuzzing, invariant suites, access-control abuse, rounding, gas scaling, rollback and double enrollment tests. Independent security review before funds.
P0-04 Sybil-resistance: hash uniqueness is NOT unique-person proof. Define issuer trust, enrollment, revocation, appeal, privacy and adversarial threat model. No automatic real-person guarantee.
P0-05 Economics: dynamic Python regime configurations must not be labeled active on-chain if immutable Solidity constants remain unchanged. Write explicit on-chain governance specification and migration strategy. Protect 40/20/40 policy against unauthorized changes.
P0-06 Legal aid: no guaranteed free lawyers, enforceable riders or court rights without partner program, eligible case criteria, local counsel and enforceable funding. Label generated output informational pending legal review.
P0-07 Current API: mandatory OAuth/OIDC or equivalent delegated auth where appropriate, strict policy-based authorization, input bounds, request timeouts and quotas, PII minimization, safe errors, abuse monitoring, legal and data retention review.

## Phase 0: truth baseline and scope (NO integrations before completion)
Deliver: docs/SECURITY_THREAT_MODEL.md, docs/TRUST_BOUNDARIES.md, docs/RELEASE_GATES.md, docs/PRIVACY_IMPACT.md, docs/DATA_PROVENANCE.md, docs/JURISDICTION_MATRIX.md, docs/ARCHITECTURE_DECISIONS.md.
Capture current source commit, workflow SHA, dependencies, external resources. Run existing tests with intact logs; record existing green CI as workflow success only. Open critical findings as issues; no blanket 100% green.
Gate 0: human-approved threat model, known-gap inventory, nonspending proof, and scope boundaries.

## Phase 1: secure base (P0)
1. Cryptography adapter interface: keygen, sign, verify, algorithm/version metadata, secure key storage abstraction, domain-separated challenge, issuer/key revocation. Adopt audited ML-DSA-65 provider; reject ambiguous or legacy custom signer; cross-implementation test vectors.
2. Decentralized identity: W3C Verifiable Credentials Data Model 2.0 issuer/holder/verifier, registered trust lists, credential status, challenge and expiry, privacy selective disclosure if formally supported, DID resolution controls. DID alone does not prove personhood. Evaluate World ID only as optional third-party attestation with privacy/security/legal reviews and alternatives for excluded users.
3. Governance: registry-backed one-person-one-vote eligibility, signed consent, proposal content digest, snapshot height and voter set, quorum based on eligible population, supermajority based on eligible/participating thresholds explicitly defined, nonce, deadline, immutable ballot, timelock, emergency veto/circuit breaker and public audit.
4. Ledger: Foundry pinned toolchain, contract unit tests on local EVM (clearly local), property-based fuzz, actual EVM invariant handlers, access controls, cross-contract registry consistency, accounting conservation, decimal rounding, bounded redistribution gas, reentrancy and timestamp manipulation.
5. API security: minimal privilege, OpenAPI contract validation, authentication, consent withdrawal, rate-limit, resource ceilings for heavy QAOA tasks, no raw entropy/secrets in URL or logs, safe response semantics.
Gate 1: no critical/high exploit findings, independent crypto interoperability, authenticated governance E2E and EVM-executed ledger tests, evidence links.

## Phase 2: legal documentary interoperability (P1)
Akoma Ntoso v1.0/OASIS LegalDocML: create core/legal_parity/akoma_ntoso.py; parse with hardened XML tooling disabling external entities and network retrieval; schema validate official AKN samples; preserve authoritative statute source, jurisdiction, publication date, effective date, amendments and citations. Produce export templates marked 'draft for review'. Do not claim a generated document is a formally filed bill.
Legal advice: lawyer-in-the-loop workflow with sources, uncertainty, jurisdiction and escalation; never auto-file complaints or fabricate citations. Text extraction for user uploads requires consent, virus/file validation, and protected storage.
Gate 2: authentic permitted court/parliament source + XML validation + licensed document provenance + counsel sign-off for jurisdiction-specific notices.

## Phase 3: agent interop (P1)
MCP server api/mcp_server.py: default read-only resources/tools; authentication and capability-scoped tokens; explicit allowlist of upstream registries; no unverified agent-origin claims. Prompt-injection defenses, SSRF protection, tool-call budgets, dual authorization for any external side effect, denylist private case files from open logs.
Vertex AI Agent Builder optional paid/managed integration; never assume free. Prefer a local/offline review-only agent or no agent over violating zero-spend.
Gate 3: authenticated tool requests, malicious document prompt-injection red-team tests, complete tool attribution, no autonomous legal/financial side effects.

## Phase 4: reliable planetary and procurement data (P2)
Copernicus Sentinel / permissible Earth Engine access: ingest real geospatial scenes with location/date, catalog asset ID, cloud-quality flags, spatial resolution, processing lineage, satellite latency, uncertainty, dataset license. Geographic proxy indices cannot be treated as unbiased ground truth of poverty or entitled individual beneficiaries. Mandatory equity impact review; never auto-allocate relief from satellite proxy alone.
OCDS + Neo4j: accept only authorized public procurement records, OCDS schema validation, beneficial ownership data where lawful and explicitly available, entity resolution with uncertainty and source attribution. Graph edges signify evidence of relationship, not legal culpability. No automated adverse action on suspicious association alone.
Gate 4: reproducible ingest from external authentic endpoints, immutable digests, coverage and bias report, consent/license verification, independent spot-checks.

## Phase 5: mathematical rigor and privacy (P2/P3)
Lean 4: proofs for pure accounting and vote threshold propositions; explicitly relate proof assumptions to implementation using tested/refined interfaces. A theorem about a model does not prove an entire deployed contract safe.
STARK/zk proof-of-accounting pilot only once threat model, proving system, verifier soundness, cost and chain compatibility are benchmarked. Avoid unproven 'post-quantum universal privacy' guarantees and claimed throughput. Distinguish ZK privacy from data confidentiality, side channels, metadata leakage.
QAOA: existing Qiskit statevector computations are simulation, never count as physical quantum execution. Under strict no-simulation policy, disable statevector path from production acceptance and rely on real non-quantum mathematical optimization and genuine data, or integrate authenticated quantum hardware only with an authorized budget (currently forbidden).
AI Economist: simulation-based research only. Under user's zero-simulation directive do not enable it and never call simulation empirical proof.
Gate 5: Lean checks against exact assumptions, code-traceability, independent verifier tests, observed actual hardware/data for any claim of physical computation.

## Phase 6: institutional adoption and public-network readiness (P3)
For each jurisdiction: legal counsel, data protection review, procurement/identity permissions, domain experts, partner agreements, accessibility, language review, appeals/grievance process, public financial reporting, and transparent eligibility decisions. Neither OASIS nor W3C compliance implies parliamentary/UN recognition.
Testnet: only with separate explicit user authorization after ALL offline critical gates; public endpoint, chain ID, verified bytecode, contract addresses, signed transactions, events, independent explorer proofs, custody rules and rollback strategy.
Mainnet: separate user approval after documented testnet lifecycle, professional external audit, code freeze, emergency controls, incident tabletop, treasury governance, operational availability and cost approval. No deployments/cycles/transactions in this blueprint PR.

## Architecture contract
[Authentic external data + signed provenance] -> [validated ingest, quarantine on failure] -> [policy/legal/identity adapters] -> [auditable deterministic core accounting + optimization] -> [authenticated citizen UI and read-only agents] -> [independent evidence store and observability] -> [gated future on-chain adapter].
No direct raw agent instructions to treasury or smart contracts. No state transition if trust verification fails.

## Proposed repository layout
core/identity/{credential_verifier.py,trust_registry.py,revocation.py,governance_auth.py}
core/legal_parity/{akoma_ntoso.py,authority_registry.py,review_queue.py}
core/data/{provenance.py,copernicus_adapter.py,ocds_adapter.py,license_policy.py}
core/proofs/{accounting_spec.py,governance_spec.py}
api/{mcp_server.py,security.py}
contracts/test/{Identity.t.sol,LedgerInvariant.t.sol,Governance.t.sol}
proofs/{Accounting.lean,VoteThreshold.lean}
docs/{SECURITY_THREAT_MODEL.md,DATA_PROVENANCE.md,JURISDICTION_MATRIX.md,PRIVACY_IMPACT.md,RELEASE_GATES.md}
scripts/{verify_crypto_interop.py,verify_external_sources.py,release_gate.py}
evidence/<commit-sha>/ (generated by CI as signed artifact, not committed private data)

## Acceptance contract (every integration)
For each module publish 5W1H, risk/owner, dependency/license, independent upstream source, fixture prohibition, test steps, real integration evidence, failure-mode test, reproducible command, security findings, cost declaration and rollback.
Status enum: NOT_IMPLEMENTED, IMPLEMENTED_UNVERIFIED, VERIFIED_LOCAL, VERIFIED_EXTERNAL, VERIFIED_TESTNET, BLOCKED. GREEN only for the exact gate whose proof exists.
Mandatory CI: lint/type, Python tests, pip-audit, npm audit with lockfiles, secrets scanning, SAST, contract compilation, Foundry EVM tests, crypto interop, XML/schema tests, threat-model traceability, evidence provenance. Network-required real-data checks must FAIL/BLOCK if unavailable; do not falsely pass or silently skip.

## Strict instructions for Antigravity
1. Work on new branches and reviewable PRs only; never directly push main.
2. Inspect all affected files, related tests, official specs, contracts and current dependency versions before modifying.
3. Start with P0 vulnerabilities; do not add unrelated technology until resolved.
4. Never use pseudo-ML-DSA, homemade signature schemes or unsupported PQ claims.
5. Never assert EVM invariants are proven by JavaScript arithmetic; execute deployed bytecode in a clearly labeled local EVM and additionally obtain formal verification if claiming formal proofs.
6. No dummy API tokens, synthetic identity proof, fabricated country recognition or grant availability; no production mocks, fixtures or simulators promoted to real evidence.
7. Do not activate AI Economist, statevector simulated quantum 'truth', or any economic sandbox under the user's zero-simulation requirement.
8. Allow safe unit tests of deterministic functions without disguising them as live external validation.
9. Use no paid tools, cloud deployment, gas, cycles, real financial transfers, registrations or legally consequential filing.
10. Maintain machine-readable gate report with SHA, timestamp, test command, exit code, evidence artifact hash; fail closed for unknown.
11. Open draft PR with precise changes, risk, breaking compatibility, artifacts and unresolved blockers; never merge automatically.
12. Never say '100% genuine green', 'mainnet ready', 'formal proofs completed', or 'mission completed' without gate-by-gate independent verification.
13. Preserve legal language accuracy: informational notices do not automatically bind counterparties, and legal-defense grants depend on actual eligibility and available funds.
14. Avoid privacy-invasive 'God's eye' claims. Satellite data and procurement graph analytics are fallible and require human review.
15. Respect all licenses/terms and privacy laws; credentials or permissions unavailable means BLOCKED, not workaround.

## Verification sources
NIST FIPS 204: https://csrc.nist.gov/pubs/fips/204/final
W3C VC DM 2.0: https://www.w3.org/TR/vc-data-model-2.0/
OASIS Akoma Ntoso: https://www.oasis-open.org/standard/akn-v1-0/
OCDS: https://standard.open-contracting.org/latest/en/
Google Earth Engine noncommercial eligibility: https://earthengine.google.com/noncommercial/
