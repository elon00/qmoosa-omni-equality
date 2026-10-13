"""
Citizen-Centric Interface & Practical Onboarding Engine.
Translates complex legal audits into simple, actionable steps for regular humans.
Provides concrete action paths: Pre-Signing Riders, Post-Signing Notices, and Legal Escrow Bounties.
"""

from typing import Dict, List, Any
from core.legal_parity.asymmetry_analyzer import LegalAsymmetryAuditor
from core.legal_parity.auto_advocate import AutoLegalAdvocate


PLAIN_LANGUAGE_EXPLANATIONS = {
    "MANDATORY_ARBITRATION": {
        "en": "Warning: You are giving up your right to take this company to a regular public court or consumer forum.",
        "hi": "चेतावनी: आप इस कंपनी के खिलाफ सामान्य अदालत या उपभोक्ता फोरम जाने का अपना संवैधानिक अधिकार खो रहे हैं।"
    },
    "CLASS_ACTION_WAIVER": {
        "en": "Warning: If this company harms thousands of people at once, you cannot join others to fight together; you must fight alone.",
        "hi": "चेतावनी: यदि यह कंपनी हजारों लोगों के साथ धोखाधड़ी करती है, तो भी आप सामूहिक रूप से केस नहीं कर सकते; आपको अकेले लड़ना होगा।"
    },
    "UNILATERAL_MODIFICATION": {
        "en": "Warning: The company can secretly change rules, fees, or interest rates at any time without asking you.",
        "hi": "चेतावनी: कंपनी बिना आपकी सहमति के किसी भी समय नियम, फीस या ब्याज दरें अपनी मर्जी से बदल सकती है।"
    },
    "ASYMMETRIC_INDEMNIFICATION": {
        "en": "Warning: If anything goes wrong, you have to pay the company's legal costs and damages, but they pay nothing to you.",
        "hi": "चेतावनी: किसी भी नुकसान की स्थिति में आपको कंपनी का कानूनी खर्च भरना होगा, लेकिन कंपनी आपकी कोई भरपाई नहीं करेगी।"
    },
    "LIMITATION_OF_LIABILITY_EXTREME": {
        "en": "Warning: The company exempts itself from all responsibility if their product, app, or service causes you financial loss.",
        "hi": "चेतावनी: यदि कंपनी की सेवा या ऐप से आपका आर्थिक नुकसान होता है, तो कंपनी अपनी सारी जिम्मेदारी से हाथ धो लेती है।"
    },
    "UNILATERAL_FEE_SHIFTING": {
        "en": "Warning: You are forced to pay the company's expensive corporate lawyers if there is any dispute.",
        "hi": "चेतावनी: किसी भी विवाद में आपको कंपनी के महंगे वकीलों की फीस भरने के लिए बाध्य किया जा रहा है।"
    }
}


class CitizenOnboardingEngine:
    """
    Empowers ordinary citizens with actionable, 3-step legal parity tools.
    """

    def __init__(self):
        self.auditor = LegalAsymmetryAuditor()

    def process_citizen_document(
        self,
        document_text: str,
        citizen_id: str,
        opposing_entity: str,
        document_title: str
    ) -> Dict[str, Any]:
        """
        Processes a submitted contract and creates a comprehensive, plain-language action plan.
        """
        audit = self.auditor.audit_contract(document_text)
        detected = audit.get("detected_categories", [])

        # 1. Plain language breakdown
        simple_warnings_en = []
        simple_warnings_hi = []
        for cat in detected:
            if cat in PLAIN_LANGUAGE_EXPLANATIONS:
                simple_warnings_en.append(PLAIN_LANGUAGE_EXPLANATIONS[cat]["en"])
                simple_warnings_hi.append(PLAIN_LANGUAGE_EXPLANATIONS[cat]["hi"])

        # 2. Synthesize concrete riders
        riders = AutoLegalAdvocate.generate_parity_riders(detected)

        # 3. Step-by-Step Action Roadmap for Citizen
        action_plan = {
            "step_1_diagnosis": {
                "risk_level": audit.get("status"),
                "asymmetry_score": f"{audit.get('asymmetry_index', 0.0):.0%}",
                "simple_summary_en": simple_warnings_en,
                "simple_summary_hi": simple_warnings_hi,
            },
            "step_2_practical_options": [
                {
                    "option_id": "PRE_SIGNING_RIDER",
                    "title": "Attach Bilateral Parity Rider (अनुबंध पर हस्ताक्षर करने से पहले)",
                    "instruction": "Print or append the attached Bilateral Rider to the contract before signing. This formally protects your rights.",
                    "document_content": riders,
                },
                {
                    "option_id": "POST_SIGNING_OBJECTION",
                    "title": "Serve Formal Notice of Unconscionability (हस्ताक्षर के बाद विवाद की स्थिति में)",
                    "instruction": "If a dispute or unfair fee arises, send this formal notice via registered post or email to the entity's grievance officer.",
                    "formal_notice": AutoLegalAdvocate.generate_equal_status_defense_brief(
                        citizen_id=citizen_id,
                        opposing_entity=opposing_entity,
                        contract_title=document_title,
                        audit_results=audit,
                    ),
                },
                {
                    "option_id": "CLAIM_LEGAL_ESCROW_DEFENSE",
                    "title": "Apply for Legal Defense Escrow Grant (निःशुल्क कानूनी सहायता)",
                    "instruction": "If the corporate entity takes legal action against you, apply for an automatic grant from the 20% Demurrage Legal Defense Pool.",
                    "eligible": audit.get("asymmetry_index", 0.0) >= 0.50,
                    "grant_status": "APPROVED_ELIGIBLE" if audit.get("asymmetry_index", 0.0) >= 0.50 else "NOT_REQUIRED",
                }
            ]
        }

        return action_plan
