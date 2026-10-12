"""
Autonomous Legal & Regulatory Parity Analyzer.
Audits legal agreements, terms of service, employment contracts, and debt agreements
for systemic asymmetry between institutional/wealthy entities and common citizens.
Calculates the Legal Asymmetry Index and identifies exploitative clauses.
"""

import re
from typing import Dict, List, Any


ASYMMETRIC_CLAUSE_PATTERNS = {
    "MANDATORY_ARBITRATION": [
        r"arbitrat",
        r"waiv.*right to.*court",
        r"waiv.*jury trial",
        r"american arbitration association",
    ],
    "CLASS_ACTION_WAIVER": [
        r"class action waiver",
        r"class action",
        r"class arbitration",
        r"representative proceeding",
        r"collective action",
    ],
    "UNILATERAL_MODIFICATION": [
        r"modify.*terms",
        r"sole discretion",
        r"without prior notice",
        r"reserve the right to amend",
    ],
    "ASYMMETRIC_INDEMNIFICATION": [
        r"indemnif",
        r"hold harmless",
        r"defend.*at your sole expense",
    ],
    "LIMITATION_OF_LIABILITY_EXTREME": [
        r"in no event shall.*be liable",
        r"liability.*exceed",
        r"consequential.*damages",
        r"as-is, where-is",
    ],
    "UNILATERAL_FEE_SHIFTING": [
        r"attorney.*fees",
        r"reimburse.*legal costs",
        r"fees incurred in enforcing",
    ]
}


class LegalAsymmetryAuditor:
    """
    Evaluates legal contracts to ensure vulnerable/poor citizens obtain the same
    protections and status that institutional/rich parties enjoy.
    """

    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "MANDATORY_ARBITRATION": 0.20,
            "CLASS_ACTION_WAIVER": 0.20,
            "UNILATERAL_MODIFICATION": 0.15,
            "ASYMMETRIC_INDEMNIFICATION": 0.15,
            "LIMITATION_OF_LIABILITY_EXTREME": 0.15,
            "UNILATERAL_FEE_SHIFTING": 0.15,
        }

    def audit_contract(self, text: str) -> Dict[str, Any]:
        """
        Scans contract text and computes the Legal Asymmetry Index in range [0.0, 1.0].
        0.0 = Symmetrical, bilateral equality.
        1.0 = Severe systemic predatoriness / class asymmetry.
        """
        text_lower = text.lower()
        findings: Dict[str, List[str]] = {}
        detected_categories = []

        for category, patterns in ASYMMETRIC_CLAUSE_PATTERNS.items():
            matches = []
            for pat in patterns:
                found = re.findall(pat, text_lower)
                if found:
                    matches.extend(found)
            if matches:
                findings[category] = list(set(matches))
                detected_categories.append(category)

        # Compute Asymmetry Index:
        total_score = sum(self.weights[cat] for cat in detected_categories)
        asymmetry_index = min(1.0, max(0.0, total_score))

        # Severity categorization:
        if asymmetry_index < 0.2:
            status = "BALANCED_PARITY"
        elif asymmetry_index < 0.5:
            status = "MODERATE_ASYMMETRY"
        elif asymmetry_index < 0.75:
            status = "SEVERE_EXPLOITATIVE_ASYMMETRY"
        else:
            status = "CRITICAL_UNILATERAL_DOMINANCE"

        return {
            "asymmetry_index": float(asymmetry_index),
            "status": status,
            "detected_categories": detected_categories,
            "findings": findings,
            "requires_parity_countermeasure": asymmetry_index >= 0.2,
        }
