# Qmoosa Omni-Equality Protocol (OEQ) — Security Threat Model & Baseline Truth

> **Version:** 1.0.0 (Phase 0 Baseline)  
> **Date:** October 13, 2026  
> **Status:** SECURITY AUDIT BASELINE — CRITICAL REMEDIATION REQUIRED  
> **Doctrine:** No mock evidence. No fabricated results. No silent fallbacks. Fail-closed security.

---

## 1. System Overview & Trust Boundaries

The Qmoosa Omni-Equality Protocol aims to provide post-quantum sovereign identity, automated legal parity, and egalitarian wealth distribution. Before any component can be deployed or presented to sovereign institutions (Parliaments, UN, Central Banks), all trust boundaries, structural flaws, and threat vectors must be rigorously cataloged and bounded.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   TRUST BOUNDARIES                                     │
├────────────────────────────────┬───────────────────────┬───────────────────────────────┤
│ UNTRUSTED / EXTERNAL           │ PERIMETER VALIDATION  │ CORE TRUSTED COMPUTATION      │
├────────────────────────────────┼───────────────────────┼───────────────────────────────┤
│ • Unauthenticated Client Inputs│ • ML-DSA-65 Signature │ • Egalitarian Ledger State    │
│ • Commercial Adhesion Contracts│ • W3C DID / VC Checks │ • Demurrage Accounting Core   │
│ • External Geospatial Oracles  │ • Akoma Ntoso Schema  │ • Soulbound Voting Ledger     │
│ • Procurement Databases (OCDS) │ • Schema Sanitization │ • Formal Invariant Engine     │
└────────────────────────────────┴───────────────────────┴───────────────────────────────┘
```

---

## 2. Threat Vector Catalog & Existing Vulnerability Assessment

### 🔴 Threat Vector 1: Forgeable Custom Lattice Signature (CRITICAL VULNERABILITY)
* **Vulnerable Component:** `core/pqc/ml_dsa.py` (Custom `MLDSA65KeyPair.verify()`)
* **Root Cause:** The custom implementation verified commitment `w1_seed` and sample `c`, but did not mathematically bind the signature to the private key polynomial ($s_1, s_2$) through the lattice relation ($A \cdot z - c \cdot t \equiv w \pmod q$).
* **Exploit Scenario:** An attacker knowing any public key and message could synthesize an arbitrary 32-byte `w1_seed`, derive $c$, and generate a valid signature passing `verify()` without possessing the secret key.
* **Impact:** Complete breakdown of the 1-Human=1-Vote guarantee; attackers could forge votes for any citizen.
* **Remediation Status:** **BLOCKED** until replaced with a standard, independently reviewed, interoperable implementation of NIST FIPS 204 ML-DSA-65 passing official test vectors.

---

### 🔴 Threat Vector 2: Unauthenticated Citizen Identity in Governance (HIGH VULNERABILITY)
* **Vulnerable Component:** `core/tokenomics/dynamic_governance.py` (`cast_vote()`)
* **Root Cause:** Function accepts plain string `citizen_id` without verifying an active cryptographic signature or cryptographic proof of unique personhood.
* **Exploit Scenario:** An attacker can generate millions of random strings (`"0x1111..."`, `"0x2222..."`) and overwhelm referendums to force economic regime changes.
* **Impact:** Sybil attacks, plutocratic manipulation, fraudulent macroeconomic state shifts.
* **Remediation Status:** **BLOCKED** until voter-set snapshots, signature-authenticated ballots, quorum enforcement, and replay protection are verified.

---

### 🟡 Threat Vector 3: Smart Contract Arithmetic vs. EVM Execution Discrepancy
* **Vulnerable Component:** `scripts/verify_contracts.js`
* **Root Cause:** Contract verification previously relied on JavaScript client-side arithmetic simulation of demurrage instead of stateful on-chain EVM transactions.
* **Exploit Scenario:** EVM precision truncation, integer division rounding errors, or gas limit re-entrancy could diverge from the off-chain JavaScript formulas.
* **Impact:** Ledger state corruption, unexpected balance drain, or unauthorized inflation.
* **Remediation Status:** **IMPLEMENTED_UNVERIFIED** locally; requires pinned Foundry invariant/fuzz test suite executing in genuine local EVM with formal Lean 4 accounting proofs.

---

### 🟡 Threat Vector 4: Supply Chain & Dependency Surface
* **Vulnerable Component:** Node.js `node_modules` (`tmp <=0.2.5` through `solc`)
* **Root Cause:** Upstream dependency advisory (GHSA-52f5-9888-hmc6 / GHSA-ph9p-34f9-6g65) creates arbitrary directory traversal risks in temporary build directories.
* **Remediation Status:** Pinned toolchain and isolated environment required; dependency audit must fail-closed on unreviewed critical vulnerabilities.

---

### 🔵 Threat Vector 5: Simulation vs. Physical Reality Fallacy
* **Vulnerable Component:** `core/quantum/qaoa_solver.py` (Qiskit Statevector)
* **Root Cause:** Off-chain simulation on classical CPU running matrix vector products is mathematically valid as a numerical optimization algorithm, but cannot be claimed as "physical quantum hardware execution".
* **Remediation Status:** Under the strict zero-simulation directive, classical optimization metrics must be clearly documented as classical algorithmic solvers. Physical quantum execution claims are disallowed until authenticated quantum processor (QPU) telemetry is cryptographically verified with authorized budgets.

---

## 3. Zero-Spend & Non-Interference Invariants

To eliminate financial, legal, and operational risks:
1. **0 Gas / 0 Token Spend:** No real funds, testnet faucets, mainnet tokens, or gas fees may be spent without explicit manual operator authorization.
2. **0 Cloud / API Costs:** No paid subscriptions, paid Vertex AI builders, or metered APIs may be provisioned.
3. **No Autonomous Legal Bindings:** Informational notices generated by the Legal Parity Engine must remain explicitly informational draft recommendations; they must never claim to be automatically binding judicial rulings.
4. **No Automated Mainnet Transfers:** Demurrage flow pools must remain in verified local execution until formal security audits and regulatory compliance reviews are signed off.

---

## 4. Remediation Exit Gate (Gate 0)

| Requirement | Verification Method | Status |
|:---|:---|:---|
| Threat Model Published | Comprehensive threat surface cataloged in `SECURITY_THREAT_MODEL.md` | **PASSED** |
| Known Critical Vulnerabilities Cataloged | ML-DSA forgeability & Governance unauthenticated IDs recorded | **PASSED** |
| Zero-Spend Invariant Enforced | Enforced across all scripts and configuration | **PASSED** |
| Release Gates Specification Defined | Documented in `RELEASE_GATES.md` with fail-closed statuses | **PASSED** |

**Gate 0 Exit Decision:** **PASSED (Security Scope Approved for P0 Execution)**
