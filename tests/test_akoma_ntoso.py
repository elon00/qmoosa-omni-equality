"""
Tests for OASIS Akoma Ntoso XML Legal Export.
"""

from core.legal_parity.akoma_ntoso import AkomaNtosoExporter
from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor


def test_akoma_ntoso_generation_and_validation():
    auditor = LegalAsymmetryAuditor()
    contract = (
        "Tenant agrees to mandatory arbitration and waives trial by jury. "
        "Landlord may unilaterally modify terms without notice. "
        "Tenant waives class action participation."
    )
    audit = auditor.audit_contract(contract)

    xml_output = AkomaNtosoExporter.generate_unconscionability_doc(
        citizen_id="0x998877665544332211",
        opposing_entity="MegaCorp Real Estate Ltd.",
        contract_title="Commercial Adhesion Lease",
        audit_results=audit,
        jurisdiction="US/NY"
    )

    assert "akomaNtoso" in xml_output
    assert "FRBRWork" in xml_output
    assert "NoticeOfUnconscionability" in xml_output
    assert "MegaCorp Real Estate Ltd." in xml_output

    is_valid = AkomaNtosoExporter.validate_akoma_ntoso_structure(xml_output)
    assert is_valid is True
