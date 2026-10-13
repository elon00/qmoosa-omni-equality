"""
Strict Fail-Closed Reality Gate Verification Suite.
Verifies all 7 technical layers of Qmoosa Omni-Equality Protocol.
Enforces ZERO MOCKS, ZERO SIMULATIONS, and 100% GENUINE EXECUTION.
"""

import sys
import os
import time
import subprocess
import numpy as np

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.quantum.hamiltonian import EgalitarianQUBO
from core.quantum.qaoa_solver import QAOAEgalitarianSolver
from core.quantum.metrics import calculate_gini, calculate_atkinson_index, calculate_rawlsian_min
from core.pqc.lattice_id import PostQuantumLatticeSigner, SoulboundCitizenIdentity
from core.pqc.equal_rights import DemocraticParityLedger
from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor
from core.legal_parity.auto_advocate import AutoLegalAdvocate
from core.tokenomics.demurrage_engine import EgalitarianDemurragePool


class RealityGateRunner:
    def __init__(self):
        self.passes = 0
        self.total = 0

    def record_step(self, layer_name: str, passed: bool, details: str = ""):
        self.total += 1
        if passed:
            self.passes += 1
            print(f"  [PASS] {layer_name}: {details}")
        else:
            print(f"  [FAIL] {layer_name}: {details}")

    def run_all(self) -> bool:
        print("\n" + "=" * 75)
        print("[+] QMOOSA OMNI-EQUALITY PROTOCOL - REALITY GATE VERIFICATION (ZERO MOCKS)")
        print("=" * 75 + "\n")

        # -------------------------------------------------------------
        # LAYER 1: Codebase Reality Audit (No mocks / no simulations)
        # -------------------------------------------------------------
        print("Layer 1: Codebase Zero-Mock Audit...")
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        mock_found = False
        forbidden = ["unittest.mock", "MagicMock", "create_autospec"]
        for current_path, _, files in os.walk(os.path.join(root_dir, "core")):
            for f in files:
                if f.endswith(".py"):
                    full_p = os.path.join(current_path, f)
                    with open(full_p, "r", encoding="utf-8") as fh:
                        content = fh.read()
                        for term in forbidden:
                            if term in content:
                                mock_found = True
                                print(f"      Violation in {f}: contains {term}")
        self.record_step("Layer 1: Static Reality Gate", not mock_found, "Zero mock libraries in core engine")

        # -------------------------------------------------------------
        # LAYER 2: Quantum Hamiltonian & QAOA Optimization
        # -------------------------------------------------------------
        print("\nLayer 2: Quantum Hamiltonian & QAOA Engine...")
        endowments = [1.0, 4.0, 10.0]
        budget = 6
        qubo = EgalitarianQUBO(endowments, total_budget=budget, bits_per_agent=1)
        Q, offset = qubo.build_qubo_matrix()
        H, h_offset = qubo.to_ising_hamiltonian()
        
        solver = QAOAEgalitarianSolver(qubo, p_layers=1)
        res = solver.solve(maxiter=20)
        
        q_valid = (
            res["num_qubits"] == 3
            and res["initial_gini"] > 0.0
            and res["sen_social_welfare"] > 0.0
            and len(res["optimal_bitstring"]) == 3
        )
        self.record_step(
            "Layer 2: Quantum Optimization",
            q_valid,
            f"Qubits={res['num_qubits']}, Gini: {res['initial_gini']:.3f} -> {res['final_gini']:.3f}"
        )

        # -------------------------------------------------------------
        # LAYER 3: Post-Quantum Cryptography & Soulbound Identity
        # -------------------------------------------------------------
        print("\nLayer 3: Post-Quantum Lattice Cryptography & 1-Human=1-Vote...")
        from core.pqc.ml_dsa import MLDSA65KeyPair
        pair = MLDSA65KeyPair.generate(seed=b"REALITY_GATE_PQC_TEST_SEED_123456789")
        test_payload = b"Equality Manifesto: Inalienable Democratic Standing"
        sig = pair.sign(test_payload)
        sig_valid = MLDSA65KeyPair.verify(pair.public_key_bytes, test_payload, sig)
        sig_tamper_rejected = not MLDSA65KeyPair.verify(pair.public_key_bytes, b"Altered Message", sig)
        wrong_pair = MLDSA65KeyPair.generate()
        wrong_key_rejected = not MLDSA65KeyPair.verify(wrong_pair.public_key_bytes, test_payload, sig)

        citizen = SoulboundCitizenIdentity("human_proof_entropy_reality_check_01")
        assertion = citizen.create_assertion("Equitable Land & Resource Guarantee")
        assert_valid, _ = SoulboundCitizenIdentity.verify_assertion(assertion)
        pqc_ok = sig_valid and sig_tamper_rejected and wrong_key_rejected and assert_valid and (citizen.legal_weight == 1.0)
        self.record_step(
            "Layer 3: PQC Lattice Signatures",
            pqc_ok,
            f"NIST FIPS 204 ML-DSA-65 Verified: Citizen ID={citizen.citizen_id[:14]}... Weight={citizen.legal_weight}"
        )

        # -------------------------------------------------------------
        # LAYER 4: Autonomous Legal Parity & Asymmetry Auditor
        # -------------------------------------------------------------
        print("\nLayer 4: Legal Parity & Class Asymmetry Neutralizer...")
        sample_contract = (
            "User agrees to mandatory binding arbitration waiving jury trial. "
            "Company may modify terms at any time in its sole discretion. "
            "Class action waiver applies to all representative proceedings. "
            "User indemnifies company against all attorney fees."
        )
        auditor = LegalAsymmetryAuditor()
        audit = auditor.audit_contract(sample_contract)
        defense_brief = AutoLegalAdvocate.generate_equal_status_defense_brief(
            citizen_id=citizen.citizen_id,
            opposing_entity="Global Conglomerate Corp",
            contract_title="Preprinted Terms of Adhesion",
            audit_results=audit,
        )
        legal_ok = (audit["asymmetry_index"] >= 0.5) and ("NOTICE OF UNCONSCIONABILITY" in defense_brief)
        self.record_step(
            "Layer 4: Legal Parity Engine",
            legal_ok,
            f"Asymmetry Index={audit['asymmetry_index']:.2f}, Status={audit['status']}"
        )

        # -------------------------------------------------------------
        # LAYER 5: Demurrage & Universal Flow Pool
        # -------------------------------------------------------------
        print("\nLayer 5: Continuous Demurrage & Universal Redistribution...")
        pool = EgalitarianDemurragePool(holding_threshold=1_000_000.0, annual_decay_rate=0.08)
        pool.set_balance("billionaire_whale", 10_000_000.0, timestamp=0.0)
        for i in range(5):
            pool.register_citizen(f"citizen_beneficiary_{i}", initial_balance=50.0, timestamp=0.0)
        
        init_gini = calculate_gini(list(pool.balances.values()))
        # 1 year later
        decay_res = pool.apply_decay_and_redistribute(current_time=365.25 * 86400.0)
        demurrage_ok = (decay_res["total_decay_collected"] > 0) and (decay_res["resulting_gini"] < init_gini)
        self.record_step(
            "Layer 5: Demurrage Flow Pool",
            demurrage_ok,
            f"Gini reduced: {init_gini:.3f} -> {decay_res['resulting_gini']:.3f}, Universal Flow Pool={decay_res['universal_flow_pool']:.2f}, Legal Escrow={decay_res['legal_defense_escrow']:.2f}"
        )

        # -------------------------------------------------------------
        # LAYER 6: Smart Contract Verification
        # -------------------------------------------------------------
        print("\nLayer 6: Smart Contract Compilation & Runtime Invariant Verification...")
        verify_script = os.path.join(root_dir, "scripts", "verify_contracts.js")
        contracts_ok = False
        contracts_detail = "BLOCKED: Verification script missing"

        if os.path.exists(verify_script):
            res_contract = subprocess.run(
                ["node", verify_script],
                cwd=root_dir,
                capture_output=True,
                text=True,
            )
            if res_contract.returncode == 0:
                contracts_ok = True
                contracts_detail = "Solidity 0.8.20 compiled cleanly; 5 formal runtime invariants proven"
            else:
                contracts_ok = False
                contracts_detail = f"Compilation/Invariant failure: {res_contract.stderr.strip() or res_contract.stdout.strip()}"

        self.record_step("Layer 6: Smart Contracts", contracts_ok, contracts_detail)

        # -------------------------------------------------------------
        # LAYER 7: Pytest Full Suite Execution
        # -------------------------------------------------------------
        print("\nLayer 7: Executing Pytest Suite across all unit tests...")
        res_test = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-q"],
            cwd=root_dir,
            capture_output=True,
            text=True,
        )
        test_ok = (res_test.returncode == 0)
        summary_line = res_test.stdout.strip().split("\n")[-1] if res_test.stdout else "Tests executed"
        self.record_step("Layer 7: Unit Test Suite", test_ok, summary_line)

        # -------------------------------------------------------------
        # FINAL CERTIFICATION
        # -------------------------------------------------------------
        print("\n" + "=" * 75)
        all_passed = (self.passes == self.total)
        if all_passed:
            print("[SUCCESS] REALITY GATE PASSED: ALL 7 TECHNICAL LAYERS ARE GENUINE GREEN.")
            print("          Functional checks only; security certification requires independent evidence.")
            print("=" * 75 + "\n")
            return True
        else:
            print(f"[FAILED] REALITY GATE HALTED: {self.total - self.passes} layers failed. Mainnet release BLOCKED.")
            print("=" * 75 + "\n")
            return False


if __name__ == "__main__":
    runner = RealityGateRunner()
    success = runner.run_all()
    sys.exit(0 if success else 2)
