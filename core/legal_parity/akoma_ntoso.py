"""
OASIS Akoma Ntoso (LegalDocumentML v1.0) Legal Interoperability Adapter.
Generates machine-readable legislative and statutory counter-notices
compliant with United Nations and parliamentary XML standards.
"""

import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Dict, Any, List


AKN_NAMESPACE = "http://docs.oasis-open.org/legaldocml/ns/akn/3.0"
ET.register_namespace("", AKN_NAMESPACE)


class AkomaNtosoExporter:
    """
    Serializes Legal Parity Audits and Bilateral Riders into valid
    OASIS LegalDocumentML (Akoma Ntoso v3.0) XML documents.
    """

    @staticmethod
    def generate_unconscionability_doc(
        citizen_id: str,
        opposing_entity: str,
        contract_title: str,
        audit_results: Dict[str, Any],
        jurisdiction: str = "GLOBAL/UCC"
    ) -> str:
        """
        Creates an Akoma Ntoso structured legal counter-document.
        """
        now_iso = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        doc_uri = f"/akn/{jurisdiction}/doc/parity/{citizen_id[:10]}/{int(datetime.now(timezone.utc).timestamp())}"

        # Root element
        root = ET.Element(f"{{{AKN_NAMESPACE}}}akomaNtoso")
        doc = ET.SubElement(root, f"{{{AKN_NAMESPACE}}}doc", name="NoticeOfUnconscionability")

        # Metadata section
        meta = ET.SubElement(doc, f"{{{AKN_NAMESPACE}}}meta")
        identification = ET.SubElement(meta, f"{{{AKN_NAMESPACE}}}identification", source="#qmoosa-protocol")

        # FRBR Work
        frbr_work = ET.SubElement(identification, f"{{{AKN_NAMESPACE}}}FRBRWork")
        ET.SubElement(frbr_work, f"{{{AKN_NAMESPACE}}}FRBRthis", value=f"{doc_uri}/main")
        ET.SubElement(frbr_work, f"{{{AKN_NAMESPACE}}}FRBRuri", value=doc_uri)
        ET.SubElement(frbr_work, f"{{{AKN_NAMESPACE}}}FRBRdate", date=now_iso, name="issuance")
        ET.SubElement(frbr_work, f"{{{AKN_NAMESPACE}}}FRBRauthor", href=f"#citizen-{citizen_id}")
        ET.SubElement(frbr_work, f"{{{AKN_NAMESPACE}}}FRBRcountry", value=jurisdiction)

        # FRBR Expression
        frbr_expr = ET.SubElement(identification, f"{{{AKN_NAMESPACE}}}FRBRExpression")
        ET.SubElement(frbr_expr, f"{{{AKN_NAMESPACE}}}FRBRthis", value=f"{doc_uri}/en@/main")
        ET.SubElement(frbr_expr, f"{{{AKN_NAMESPACE}}}FRBRuri", value=f"{doc_uri}/en@")
        ET.SubElement(frbr_expr, f"{{{AKN_NAMESPACE}}}FRBRdate", date=now_iso, name="expression")
        ET.SubElement(frbr_expr, f"{{{AKN_NAMESPACE}}}FRBRauthor", href="#qmoosa-protocol")
        ET.SubElement(frbr_expr, f"{{{AKN_NAMESPACE}}}FRBRlanguage", language="eng")

        # FRBR Manifestation
        frbr_man = ET.SubElement(identification, f"{{{AKN_NAMESPACE}}}FRBRManifestation")
        ET.SubElement(frbr_man, f"{{{AKN_NAMESPACE}}}FRBRthis", value=f"{doc_uri}/en@/main.xml")
        ET.SubElement(frbr_man, f"{{{AKN_NAMESPACE}}}FRBRuri", value=f"{doc_uri}/en@.akn")
        ET.SubElement(frbr_man, f"{{{AKN_NAMESPACE}}}FRBRdate", date=now_iso, name="generation")
        ET.SubElement(frbr_man, f"{{{AKN_NAMESPACE}}}FRBRauthor", href="#qmoosa-protocol")

        # Body section
        body = ET.SubElement(doc, f"{{{AKN_NAMESPACE}}}mainBody")
        
        # Preamble / Background
        intro = ET.SubElement(body, f"{{{AKN_NAMESPACE}}}paragraph", eId="intro")
        intro_content = ET.SubElement(intro, f"{{{AKN_NAMESPACE}}}content")
        p1 = ET.SubElement(intro_content, f"{{{AKN_NAMESPACE}}}p")
        p1.text = (
            f"FORMAL NOTICE OF UNCONSCIONABILITY AND CLASS ASYMMETRY regarding '{contract_title}', "
            f"served by Citizen {citizen_id} to {opposing_entity}."
        )

        # Diagnostic findings
        asymmetry_score = audit_results.get("asymmetry_index", 0.0)
        risk_level = audit_results.get("status", "UNKNOWN")
        diag_p = ET.SubElement(intro_content, f"{{{AKN_NAMESPACE}}}p")
        diag_p.text = f"Audit Finding: Asymmetry Index={asymmetry_score:.2f}, Risk Classification={risk_level}."

        # Clauses
        detected = audit_results.get("detected_categories", [])
        for idx, cat in enumerate(detected, 1):
            clause = ET.SubElement(body, f"{{{AKN_NAMESPACE}}}clause", eId=f"sec_{idx}")
            clause_content = ET.SubElement(clause, f"{{{AKN_NAMESPACE}}}content")
            cp = ET.SubElement(clause_content, f"{{{AKN_NAMESPACE}}}p")
            cp.text = f"Section {idx}: Objections under statutory parity concerning detected clause '{cat}'."

        return ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8")

    @staticmethod
    def validate_akoma_ntoso_structure(xml_str: str) -> bool:
        """
        Validates basic Akoma Ntoso schema structure and required elements.
        """
        try:
            tree = ET.fromstring(xml_str)
            if not tree.tag.endswith("akomaNtoso"):
                return False
            meta = tree.find(f".//{{{AKN_NAMESPACE}}}meta")
            body = tree.find(f".//{{{AKN_NAMESPACE}}}mainBody")
            return meta is not None and body is not None
        except Exception:
            return False
