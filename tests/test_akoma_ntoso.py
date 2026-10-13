"""
Tests for OASIS Akoma Ntoso XML Legal Export across multiple jurisdictions.
"""

from core.legal_parity.akoma_ntoso import AkomaNtosoExporter
from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor


def test_akoma_ntoso_multijurisdiction():
    auditor = LegalAsymmetryAuditor()
    contract = (
        "Tenant agrees to mandatory binding arbitration waiving jury trial. "
        "Landlord reserves right to unilaterally modify terms without notice."
    )
    audit = auditor.audit_contract(contract)

    for jurisdiction, statute_keyword in [
        ("US", "Uniform Commercial Code § 2-302"),
        ("EU", "Directive 93/13/EEC"),
        ("IN", "Indian Contract Act, 1872"),
        ("UK", "Consumer Rights Act 2015")
    ]:
        xml_output = AkomaNtosoExporter.generate_unconscionability_doc(
            citizen_id="0x1234567890abcdef",
            opposing_entity="MegaCorp Global",
            contract_title="Standard Terms of Adhesion",
            audit_results=audit,
            jurisdiction=jurisdiction
        )

        assert statute_keyword in xml_output
        assert "NOTICE DISCLAIMER" in xml_output
        assert AkomaNtosoExporter.validate_akoma_ntoso_structure(xml_output) is True
