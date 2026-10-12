"""
Interactive Command-Line Runner for Qmoosa Omni-Equality Protocol.
Demonstrates end-to-end execution of Quantum Optimization, PQC Signatures,
Legal Parity Audit, and Demurrage Redistribution.
"""

import sys
import os
import json

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.quantum.hamiltonian import EgalitarianQUBO
from core.quantum.qaoa_solver import QAOAEgalitarianSolver
from core.pqc.lattice_id import SoulboundCitizenIdentity
from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor
from core.legal_parity.auto_advocate import AutoLegalAdvocate
from core.tokenomics.demurrage_engine import EgalitarianDemurragePool


def main():
    print("=" * 80)
    print("[+] QMOOSA OMNI-EQUALITY: AUTONOMOUS EGALITARIAN PROTOCOL")
    print("    Post-Quantum Computing + Web 4.0 Decentralized Socio-Economic Parity")
    print("=" * 80)

    # 1. Quantum Optimization
    print("\n[1/4] EXECUTING QUANTUM EQUALITY OPTIMIZATION...")
    initial_wealth = [2.0, 5.0, 15.0]
    total_budget = 8
    print(f"  Initial Agent Wealth: {initial_wealth}")
    print(f"  Distributable Common Pool Budget: {total_budget}")

    qubo = EgalitarianQUBO(initial_wealth, total_budget=total_budget, bits_per_agent=1)
    solver = QAOAEgalitarianSolver(qubo, p_layers=1)
    q_res = solver.solve(maxiter=25)

    print(f"  Quantum Circuit Qubits: {q_res['num_qubits']}")
    print(f"  Measured Ground State: {q_res['optimal_bitstring']}")
    print(f"  Allocated Increments: {q_res['allocations']}")
    print(f"  Final Post-Allocation Wealth: {q_res['final_wealth']}")
    print(f"  Gini Inequality Improvement: {q_res['initial_gini']:.3f} -> {q_res['final_gini']:.3f} ({q_res['gini_improvement_pct']:.1f}% reduction)")
    print(f"  Rawlsian Poverty Floor Raised: {q_res['initial_rawlsian_floor']} -> {q_res['final_rawlsian_floor']}")

    # 2. Post-Quantum Identity
    print("\n[2/4] ISSUING POST-QUANTUM SOULBOUND CITIZEN IDENTITY...")
    citizen = SoulboundCitizenIdentity("moolnivasi_sovereign_citizen_alpha_771")
    print(f"  Citizen Sovereign ID: {citizen.citizen_id}")
    print(f"  Democratic Weight: {citizen.legal_weight} (Invariant: strictly 1.0, non-accumulable)")
    assertion = citizen.create_assertion("Assertion of Universal Dignity & Resource Right")
    valid, msg = SoulboundCitizenIdentity.verify_assertion(assertion)
    print(f"  NIST FIPS 204 Lattice Signature Verification: {'VALID' if valid else 'INVALID'}")

    # 3. Legal Parity Audit
    print("\n[3/4] AUDITING SYSTEMIC LEGAL ASYMMETRY IN ARBITRARY CONTRACT...")
    sample_corporate_terms = (
        "User agrees that any dispute shall be resolved solely through mandatory binding arbitration "
        "and waives all right to a jury trial. The user agrees to a class action waiver. "
        "Company reserves the right to modify these terms at any time in its sole discretion. "
        "User agrees to hold harmless and indemnify company against all attorney fees."
    )
    auditor = LegalAsymmetryAuditor()
    audit = auditor.audit_contract(sample_corporate_terms)
    print(f"  Asymmetry Index: {audit['asymmetry_index']:.2f} / 1.00")
    print(f"  Classification: {audit['status']}")
    print(f"  Detected Abusive Clauses: {audit['detected_categories']}")
    riders = AutoLegalAdvocate.generate_parity_riders(audit["detected_categories"])
    print(f"  Synthesized Bilateral Parity Riders: {len(riders)} clauses generated.")

    # 4. Demurrage Universal Flow
    print("\n[4/4] EXECUTING CONTINUOUS DEMURRAGE ON HOARDED WEALTH...")
    pool = EgalitarianDemurragePool(holding_threshold=1_000_000.0, annual_decay_rate=0.08)
    pool.set_balance("whale_holding", 12_000_000.0, timestamp=0.0)
    for i in range(10):
        pool.register_citizen(f"citizen_{i}", initial_balance=100.0)
    
    res_pool = pool.apply_decay_and_redistribute(current_time=365.25 * 86400.0)
    print(f"  Hoarded Capital Decayed: {res_pool['total_decay_collected']:,.2f} tokens")
    print(f"  Deflationary Burn (50%): {res_pool['burned']:,.2f} tokens")
    print(f"  Universal Flow Pool Disbursed: {res_pool['recycled_pool']:,.2f} tokens")
    print(f"  Direct Equal Dividend: {res_pool['dividend_per_citizen']:,.2f} tokens per citizen")
    print(f"  Population Gini Coefficient Reduced to: {res_pool['resulting_gini']:.3f}")

    print("\n" + "=" * 80)
    print("[OK] EXECUTION COMPLETE: ALL PROTOCOL ENGINES OPERATING IN HARMONY.")
    print("=" * 80)


if __name__ == "__main__":
    main()
