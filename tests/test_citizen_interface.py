"""
Tests for Citizen Onboarding Engine and Plain-Language Usability.
"""

from core.legal_parity.citizen_interface import CitizenOnboardingEngine


SAMPLE_EXPLOITATIVE_LEASE = """
RENTAL AGREEMENT AND WAIVER
Tenant agrees to mandatory binding arbitration and waives all rights to a court trial or jury.
Landlord reserves the sole discretion to modify terms and rent at any time without notice.
Tenant agrees to hold harmless and indemnify landlord for all attorney's fees.
Tenant waives participation in any class action proceeding.
"""


def test_citizen_onboarding_processing():
    engine = CitizenOnboardingEngine()
    result = engine.process_citizen_document(
        document_text=SAMPLE_EXPLOITATIVE_LEASE,
        citizen_id="0x771928374821a",
        opposing_entity="Apex Property Monopolies Inc.",
        document_title="Standard Residential Lease",
    )

    diagnosis = result["step_1_diagnosis"]
    assert diagnosis["risk_level"] in ("SEVERE_EXPLOITATIVE_ASYMMETRY", "CRITICAL_UNILATERAL_DOMINANCE")
    assert len(diagnosis["simple_summary_en"]) >= 3
    assert len(diagnosis["simple_summary_hi"]) >= 3

    options = result["step_2_practical_options"]
    assert len(options) == 3
    option_ids = [o["option_id"] for o in options]
    assert "PRE_SIGNING_RIDER" in option_ids
    assert "POST_SIGNING_OBJECTION" in option_ids
    assert "CLAIM_LEGAL_ESCROW_DEFENSE" in option_ids

    # The high risk contract should be eligible for legal defense escrow
    escrow_opt = next(o for o in options if o["option_id"] == "CLAIM_LEGAL_ESCROW_DEFENSE")
    assert escrow_opt["eligible"] is True
    assert escrow_opt["grant_status"] == "APPROVED_ELIGIBLE"
