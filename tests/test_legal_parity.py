"""
Tests for Legal Asymmetry Auditor and Autonomous Parity Advocate.
"""

from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor
from core.legal_parity.auto_advocate import AutoLegalAdvocate


PREDATORY_TERMS_SAMPLE = """
TERMS OF SERVICE AND USER WAIVER
1. DISPUTE RESOLUTION: The user agrees that any dispute shall be resolved through binding arbitration
administered by the American Arbitration Association. User expressly agrees to waive all right to a jury trial in court.
2. CLASS ACTION WAIVER: You agree that you may bring claims only in your individual capacity and not as a plaintiff
or class member in any purported class action or representative proceeding.
3. MODIFICATIONS: The company reserves the right to modify these terms at any time in its sole discretion without prior notice.
4. INDEMNIFICATION: You agree to defend, indemnify and hold harmless the company against all claims, damages, and attorney's fees.
5. LIMITATION: In no event shall company total aggregate liability exceed $0.
6. ATTORNEY FEES: Any attorney's fees incurred in enforcing this agreement shall be paid by user.
"""

FAIR_BILATERAL_SAMPLE = """
MUTUAL COOPERATION AGREEMENT
Both parties agree to solve all disputes through mutual good-faith mediation or courts of law.
Amendments require mutual written signature with 30 days notice.
Each party is responsible for their own negligent acts in reciprocal proportion.
"""


def test_legal_asymmetry_auditor_predatory():
    auditor = LegalAsymmetryAuditor()
    audit = auditor.audit_contract(PREDATORY_TERMS_SAMPLE)

    assert audit["asymmetry_index"] >= 0.70
    assert audit["status"] in ("SEVERE_EXPLOITATIVE_ASYMMETRY", "CRITICAL_UNILATERAL_DOMINANCE")
    assert "MANDATORY_ARBITRATION" in audit["detected_categories"]
    assert "CLASS_ACTION_WAIVER" in audit["detected_categories"]
    assert "UNILATERAL_MODIFICATION" in audit["detected_categories"]
    assert audit["requires_parity_countermeasure"] is True


def test_legal_asymmetry_auditor_fair():
    auditor = LegalAsymmetryAuditor()
    audit = auditor.audit_contract(FAIR_BILATERAL_SAMPLE)

    assert audit["asymmetry_index"] < 0.20
    assert audit["status"] == "BALANCED_PARITY"
    assert audit["requires_parity_countermeasure"] is False


def test_auto_legal_advocate_generation():
    auditor = LegalAsymmetryAuditor()
    audit = auditor.audit_contract(PREDATORY_TERMS_SAMPLE)

    brief = AutoLegalAdvocate.generate_equal_status_defense_brief(
        citizen_id="0x99482103a8f10283",
        opposing_entity="MegaCorp Global LLC",
        contract_title="Consumer Adhesion Agreement",
        audit_results=audit,
    )

    assert "NOTICE OF UNCONSCIONABILITY" in brief
    assert "MegaCorp Global LLC" in brief
    assert "MUTUAL DISPUTE RESOLUTION" in brief
    assert "COLLECTIVE REDRESS PRESERVATION" in brief
