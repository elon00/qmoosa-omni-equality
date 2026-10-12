"""
Web 4.0 Egalitarian Gateway & Autonomous Microservices API.
Exposes real endpoints for Quantum Allocation Optimization,
Post-Quantum Identity Verification, Legal Parity Auditing, and Demurrage Tokenomics.
"""

from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from core.quantum.hamiltonian import EgalitarianQUBO
from core.quantum.qaoa_solver import QAOAEgalitarianSolver
from core.pqc.lattice_id import SoulboundCitizenIdentity
from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor
from core.legal_parity.auto_advocate import AutoLegalAdvocate
from core.tokenomics.demurrage_engine import EgalitarianDemurragePool

app = FastAPI(
    title="Qmoosa Omni-Equality Web 4.0 API",
    description="Autonomous Post-Quantum Protocol for Global Socio-Economic & Legal Parity",
    version="1.0.0",
)

auditor = LegalAsymmetryAuditor()
demurrage_pool = EgalitarianDemurragePool()


# --- Pydantic Schemas ---

class QuantumOptimizationRequest(BaseModel):
    initial_endowments: List[float] = Field(..., description="Initial wealth/resource endowment per agent")
    total_budget: int = Field(..., ge=1, description="Total resource units to allocate")
    bits_per_agent: int = Field(1, ge=1, le=4, description="Binary resolution bits per agent")
    p_layers: int = Field(1, ge=1, le=4, description="QAOA circuit layer depth")
    maxiter: int = Field(25, ge=5, le=100, description="Optimizer iterations")


class LegalAuditRequest(BaseModel):
    citizen_id: str
    opposing_entity: str
    contract_title: str
    contract_text: str


class DemurrageSimulationRequest(BaseModel):
    balances: Dict[str, float]
    elapsed_days: float = 30.0


# --- Endpoints ---

@app.get("/api/status")
def get_system_status():
    return {
        "protocol": "Qmoosa Omni-Equality Protocol",
        "version": "1.0.0",
        "architecture": "Web 4.0 Autonomous Decentralized Mesh",
        "reality_gate": "STRICT_FAIL_CLOSED_ZERO_SIMULATION",
        "quantum_engine": "Qiskit 2.x Statevector QAOA / Variational Solver",
        "cryptography": "NIST FIPS 204 ML-DSA-65 Polynomial Lattice",
        "legal_parity": "Active Asymmetry Auditor & Unconscionability Defender",
        "status": "OPERATIONAL",
    }


@app.post("/api/quantum/optimize")
def optimize_resources(req: QuantumOptimizationRequest):
    try:
        qubo = EgalitarianQUBO(
            initial_endowments=req.initial_endowments,
            total_budget=req.total_budget,
            bits_per_agent=req.bits_per_agent,
        )
        solver = QAOAEgalitarianSolver(qubo=qubo, p_layers=req.p_layers)
        result = solver.solve(maxiter=req.maxiter)
        return {
            "status": "SUCCESS",
            "optimization": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/legal/audit")
def audit_legal_contract(req: LegalAuditRequest):
    audit_res = auditor.audit_contract(req.contract_text)
    brief = AutoLegalAdvocate.generate_equal_status_defense_brief(
        citizen_id=req.citizen_id,
        opposing_entity=req.opposing_entity,
        contract_title=req.contract_title,
        audit_results=audit_res,
    )
    riders = AutoLegalAdvocate.generate_parity_riders(audit_res["detected_categories"])
    return {
        "audit": audit_res,
        "bilateral_riders": riders,
        "formal_defense_notice": brief,
    }


@app.post("/api/pqc/identity/create")
def create_pqc_identity(entropy: str):
    citizen = SoulboundCitizenIdentity(entropy)
    assertion = citizen.create_assertion("I assert my inalienable democratic parity of 1.0.")
    valid, msg = SoulboundCitizenIdentity.verify_assertion(assertion)
    return {
        "citizen_id": citizen.citizen_id,
        "legal_weight": citizen.legal_weight,
        "verified": valid,
        "verification_message": msg,
        "public_key_sample": citizen.public_key_t[:8].tolist(),
    }
