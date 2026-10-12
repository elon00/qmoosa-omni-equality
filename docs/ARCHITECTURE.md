# System Architecture & Technical Specifications

## High-Level Topology

```
+-------------------------------------------------------------------------+
|                       WEB 4.0 INTERFACE LAYER                           |
|       FastAPI Gateway | Decentralized Client | Autonomous Agent Mesh   |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                  AUTONOMOUS LEGAL PARITY LAYER                          |
|    Asymmetry Auditor | Unconscionability Motions | Bilateral Riders     |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|                  QUANTUM OPTIMIZATION ENGINE                            |
|       Qiskit 2.x | QAOA Statevector Variational Solver | QUBO/Ising     |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|               POST-QUANTUM CRYPTOGRAPHY & IDENTITY                      |
|       NIST FIPS 204 ML-DSA-65 | Soulbound Citizen Credentials (SBT)     |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
|               SMART CONTRACT & VALUE CIRCULATION LAYER                  |
|    OmniEqualityLedger.sol | Demurrage Pool | Universal Dividend Escrow   |
+-------------------------------------------------------------------------+
```

## Module Directory Structure

| Module Path | Core Purpose | Reality Assurance |
| :--- | :--- | :--- |
| `core/quantum/hamiltonian.py` | QUBO & Ising Hamiltonian mapping | Exact quadratic matrix & Pauli-$Z$ operators |
| `core/quantum/qaoa_solver.py` | Qiskit variational quantum circuit solver | Real quantum statevector expectation evaluation |
| `core/quantum/metrics.py` | Gini, Atkinson & Rawlsian metrics | Exact mathematical formulation |
| `core/pqc/lattice_id.py` | NIST FIPS 204 ML-DSA lattice signatures | Deterministic polynomial arithmetic modulo $q$ |
| `core/pqc/equal_rights.py` | Democratic 1-human=1-vote consensus | Verifiable cryptographic proposal voting |
| `core/legal_parity/asymmetry_analyzer.py` | Adhesion contract asymmetry auditing | Syntactic pattern matching across 6 dimensions |
| `core/legal_parity/auto_advocate.py` | Autonomous legal defense generation | Bilateral rider generation under UCC § 2-302 |
| `core/tokenomics/demurrage_engine.py` | Continuous capital decay & dividend flow | Continuous exponential decay math |
| `contracts/OmniEqualityLedger.sol` | Solidity smart contract | On-chain demurrage & dividend payouts |
| `contracts/SovereignIdentity.sol` | Soulbound identity contract | Non-transferable citizen credential |
| `scripts/check.py` | Fail-closed Reality Gate | Exit code 2 on any deviation |

## API Endpoints (`api/server.py`)

- `GET /api/status`: System status and active cryptographic parameters.
- `POST /api/quantum/optimize`: Solves multi-agent allocation with QAOA.
- `POST /api/legal/audit`: Scans legal contracts and outputs defense brief.
- `POST /api/pqc/identity/create`: Issues and verifies a Post-Quantum Soulbound assertion.
