# Qmoosa Omni-Equality Protocol (OEQ) — Release Gates & Evidence Framework

> **Normative Framework for Fail-Closed System Verification**

---

## 1. Release Gate Status Taxonomy

Every subsystem, security layer, and external interface in Qmoosa Omni-Equality Protocol is governed by an explicit status enum. Transitions from lower to higher assurance require reproducible, verifiable evidence.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        RELEASE GATE STATUS TAXONOMY                    │
├──────────────────────────┬─────────────────────────────────────────────┤
│ STATUS ENUM              │ MEANING & EVIDENCE REQUIREMENT              │
├──────────────────────────┼─────────────────────────────────────────────┤
│ NOT_IMPLEMENTED          │ Feature or interface is defined in spec     │
│                          │ but has no executable implementation.       │
├──────────────────────────┼─────────────────────────────────────────────┤
│ IMPLEMENTED_UNVERIFIED   │ Code exists in repo, but has not completed  │
│                          │ formal tests or security checks.            │
├──────────────────────────┼─────────────────────────────────────────────┤
│ VERIFIED_LOCAL           │ Passes reproducible unit tests, static type │
│                          │ audits, and local sandbox verification.     │
├──────────────────────────┼─────────────────────────────────────────────┤
│ VERIFIED_EXTERNAL        │ Successfully authenticated against a live,  │
│                          │ licensed, non-mocked external authority.    │
├──────────────────────────┼─────────────────────────────────────────────┤
│ VERIFIED_TESTNET         │ Deployed to an authenticated public testnet │
│                          │ with on-chain transaction hash proofs.      │
├──────────────────────────┼─────────────────────────────────────────────┤
│ BLOCKED                  │ Security flaw, missing credential, failed   │
│                          │ audit, or unproven invariant halts release. │
└──────────────────────────┴─────────────────────────────────────────────┘
```

---

## 2. Gate Definitions (Gate 0 through Gate 7)

### Gate 0: Truth Baseline & Security Scope
* **Objective:** Audit dependencies, state trust boundaries, record known vulnerabilities.
* **Pass Criteria:** Threat model document published; dependencies audited; 0-spend invariant locked.
* **Current Status:** **VERIFIED_LOCAL**

### Gate 1: Cryptographic Authentication (P0)
* **Objective:** Standardized, unforgeable NIST FIPS 204 ML-DSA-65 post-quantum signatures.
* **Pass Criteria:** Official NIST test vector verification; secret-key non-leakage; reject malformed signatures; domain separation; cross-implementation interoperability.
* **Current Status:** **VERIFIED_LOCAL** (NIST FIPS 204 ML-DSA-65 standard verified across dual independent engines in `verify_crypto_interop.py`)

### Gate 2: Governance & Voting Integrity (P0)
* **Objective:** Sybil-proof, replay-protected, snapshot-based democratic governance.
* **Pass Criteria:** Cryptographically signed ballots; eligibility checks against immutable voter snapshot; quorum validation; supermajority calculation against verified voters.
* **Current Status:** **VERIFIED_LOCAL** (ML-DSA-65 signed ballots, voter-set snapshots, >=50% quorum, and replay protection verified in `test_dynamic_governance.py`)

### Gate 3: Smart Contract & EVM Invariants (P0–P1)
* **Objective:** Mathematically sound, exploit-proof on-chain economic execution.
* **Pass Criteria:** Bytecode compiled with pinned toolchain; 5 formal runtime invariants proven; conservation of supply; demurrage decay mathematical proofs.
* **Current Status:** **VERIFIED_LOCAL** (Solidity 0.8.20 reproducible compilation and 5 formal runtime invariants passing)

### Gate 4: Legal Interoperability & Provenance (P1)
* **Objective:** UN/OASIS Akoma Ntoso legislative document processing.
* **Pass Criteria:** OASIS LegalDocumentML v3.0 XML schema validation; accurate statutory citations; human legal review disclaimers.
* **Current Status:** **VERIFIED_LOCAL** (OASIS Akoma Ntoso export and schema validation verified in `test_akoma_ntoso.py`)

### Gate 5: Evidence-Based Planetary & Procurement Intelligence (P2)
* **Objective:** Authenticated Copernicus Sentinel and OCDS procurement ingestion.
* **Pass Criteria:** Canonical SHA-256 digests; explicit licensing verification (CC-BY-4.0 / CC-0); clear uncertainty bounds; mandatory human equity review.
* **Current Status:** **VERIFIED_LOCAL** (Copernicus Sentinel & OCDS ingestion verified in `test_data_provenance.py`)

### Gate 6: Formal Verification & Mathematical Rigor (P2–P3)
* **Objective:** Formal propositions for monetary conservation, demurrage bounds, and Rawlsian floors.
* **Pass Criteria:** Conservation theorems verified; Rawlsian maximin floor preservation proven; strict egalitarian voting parity validated.
* **Current Status:** **VERIFIED_LOCAL** (Formal invariant equations verified in `test_formal_invariants.py`)

### Gate 7: Institutional Readiness & Mainnet Authorization
* **Objective:** Multi-jurisdiction legal, operational, and external security sign-off.
* **Pass Criteria:** Independent external security audit; zero critical/high CVEs; explicit written user authorization before testnet or mainnet deployment.
* **Current Status:** **BLOCKED** (Zero spend invariant locked; no mainnet funds, gas, or cycles expended)
