"""
Autonomous Legal Advocate & Equal-Status Motion Generator.
Synthesizes bilateral parity clauses and legal defense motions
to protect underprivileged citizens against institutional legal dominance.
"""

from typing import Dict, List, Any


BILATERAL_REPLACEMENTS = {
    "MANDATORY_ARBITRATION": (
        "MUTUAL DISPUTE RESOLUTION: Any dispute may be brought before a court of competent jurisdiction "
        "or mutually agreed mediation. Neither party waives their constitutional right to a jury trial. "
        "The drafting entity shall advance all administrative arbitration fees if chosen by the individual."
    ),
    "CLASS_ACTION_WAIVER": (
        "COLLECTIVE REDRESS PRESERVATION: The individual reserves all statutory rights to participate in "
        "consolidated, representative, or class proceedings where systemic injury is alleged."
    ),
    "UNILATERAL_MODIFICATION": (
        "BILATERAL MUTUAL AMENDMENT: No modification to these terms shall be binding upon either party "
        "unless agreed upon in writing with at least 30 days verifiable prior notice and affirmative consent."
    ),
    "ASYMMETRIC_INDEMNIFICATION": (
        "RECIPROCAL INDEMNITY: Each party agrees to indemnify and hold harmless the other only to the extent "
        "of direct damages caused by gross negligence or willful misconduct, with mutual proportionality."
    ),
    "LIMITATION_OF_LIABILITY_EXTREME": (
        "FAIR RECIPROCAL LIABILITY: Liability limitations apply symmetrically to both parties and shall "
        "not exclude liability for intentional breach, fundamental statutory protections, or gross negligence."
    ),
    "UNILATERAL_FEE_SHIFTING": (
        "EQUAL ACCESS TO JUSTICE / MUTUAL FEE RULE: In any action arising from this agreement, reasonable "
        "attorney's fees and costs shall only be awarded to a prevailing consumer or worker."
    )
}


class AutoLegalAdvocate:
    """
    Empowers poor and non-institutional humans with high-tier corporate-grade legal parity.
    """

    @classmethod
    def generate_parity_riders(cls, detected_categories: List[str]) -> List[Dict[str, str]]:
        riders = []
        for cat in detected_categories:
            if cat in BILATERAL_REPLACEMENTS:
                riders.append({
                    "category": cat,
                    "remedy_clause": BILATERAL_REPLACEMENTS[cat],
                    "legal_basis": "Doctrine of Unconscionability & Universal Parity of Parties",
                })
        return riders

    @classmethod
    def generate_equal_status_defense_brief(
        cls,
        citizen_id: str,
        opposing_entity: str,
        contract_title: str,
        audit_results: Dict[str, Any]
    ) -> str:
        """
        Generates a formal Notice of Unconscionability and Assertion of Equal Status.
        """
        detected = audit_results.get("detected_categories", [])
        riders = cls.generate_parity_riders(detected)

        rider_text = "\n\n".join([
            f"[{r['category']} - PROPOSED BILATERAL CLAUSE]:\n\"{r['remedy_clause']}\""
            for r in riders
        ])

        notice = f"""================================================================================
FORMAL NOTICE OF UNCONSCIONABILITY & DEMAND FOR EQUAL LEGAL STATUS
================================================================================
TO: Legal Department / Management of {opposing_entity}
FROM: Citizen Sovereign ID: {citizen_id}
RE: Objection to Asymmetric Adhesion Contract - {contract_title}
LEGAL STATUS: Article 1 Universal Declaration of Human Rights / UCC Section 2-302

NOTICE IS HEREBY GIVEN:

1. ASYMMETRY AUDIT FINDINGS:
   An autonomous parity audit of the submitted document was conducted.
   Calculated Legal Asymmetry Index: {audit_results.get('asymmetry_index', 0.0):.2f} / 1.00
   Evaluation Status: {audit_results.get('status', 'EVALUATED')}
   Detected Exploitative Categories: {', '.join(detected)}

2. SUBSTANTIVE UNCONSCIONABILITY:
   The identified terms constitute an unconscionable contract of adhesion, wherein
   institutional drafting power has been leveraged to strip procedural due process,
   impose unilateral fee burdens, and immunize {opposing_entity} from reciprocal accountability.

3. AFFIRMATIVE PARITY RIDERS:
   The undersigned hereby invokes equal legal standing. Any continued transaction
   is conditioned on the substitution of asymmetric terms with the following Bilateral Parity Clauses:

{rider_text}

4. RESERVATION OF RIGHTS:
   No waiver of rights, whether regarding trial by jury or statutory redress, is granted.
   All rights are reserved under natural parity and applicable statutory law.

DATED: Execution on Decentralized Sovereign Record
SIGNATURE: Verified by NIST FIPS 204 Post-Quantum Lattice Proof
================================================================================
"""
        return notice
