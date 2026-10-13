"""
Dynamic Macroeconomic Adaptability & Democratic Emergency Governance.
Enables resilient parameter adjustments during economic contractions,
pandemics, or Black Swan crises via 1-Human = 1-Vote Soulbound consensus.
"""

from enum import Enum
from typing import Dict, Any, List
import time


class MacroeconomicRegime(Enum):
    EQUILIBRIUM = "EQUILIBRIUM"                  # Standard baseline: 1M OEQ threshold, 40/20/40 split
    RECESSION_SHOCK = "RECESSION_SHOCK"          # Macro contraction: 500k OEQ threshold, 60/20/20 split
    BLACK_SWAN_CRISIS = "BLACK_SWAN_CRISIS"      # Pandemic/war/crisis: 250k OEQ threshold, 70/20/10 split
    BOOM_EXPANSION = "BOOM_EXPANSION"            # High expansion: 2M OEQ threshold, 30/20/50 split


REGIME_CONFIGS = {
    MacroeconomicRegime.EQUILIBRIUM: {
        "holding_threshold": 1_000_000.0,
        "flow_share_pct": 0.40,
        "legal_share_pct": 0.20,
        "burn_share_pct": 0.40,
        "description": "Standard baseline balanced egalitarian state"
    },
    MacroeconomicRegime.RECESSION_SHOCK: {
        "holding_threshold": 500_000.0,
        "flow_share_pct": 0.60,
        "legal_share_pct": 0.20,
        "burn_share_pct": 0.20,
        "description": "Recession mode: releases hoarded capital as direct citizen stimulus"
    },
    MacroeconomicRegime.BLACK_SWAN_CRISIS: {
        "holding_threshold": 250_000.0,
        "flow_share_pct": 0.70,
        "legal_share_pct": 0.20,
        "burn_share_pct": 0.10,
        "description": "Acute emergency: maximum basic survival income dividend"
    },
    MacroeconomicRegime.BOOM_EXPANSION: {
        "holding_threshold": 2_000_000.0,
        "flow_share_pct": 0.30,
        "legal_share_pct": 0.20,
        "burn_share_pct": 0.50,
        "description": "Anti-inflationary mode: higher burn rate to curb monetary overheating"
    }
}


class DynamicAdaptabilityEngine:
    """
    Governs adaptive parameter shifts while strictly preserving egalitarian invariants.
    """

    def __init__(self, initial_regime: MacroeconomicRegime = MacroeconomicRegime.EQUILIBRIUM):
        self.current_regime = initial_regime
        self.regime_change_proposals: Dict[str, Dict[str, Any]] = {}
        self.history: List[Dict[str, Any]] = [{
            "regime": initial_regime.value,
            "timestamp": int(time.time()),
            "reason": "Genesis Initialized"
        }]

    def get_active_parameters(self) -> Dict[str, Any]:
        """Returns the currently active dynamic economic parameters."""
        cfg = REGIME_CONFIGS[self.current_regime]
        return {
            "active_regime": self.current_regime.value,
            "holding_threshold": cfg["holding_threshold"],
            "flow_share_pct": cfg["flow_share_pct"],
            "legal_share_pct": cfg["legal_share_pct"],
            "burn_share_pct": cfg["burn_share_pct"],
            "description": cfg["description"]
        }

    def propose_regime_shift(
        self,
        proposal_id: str,
        target_regime: MacroeconomicRegime,
        justification: str,
        proposer_citizen_id: str
    ) -> Dict[str, Any]:
        """Creates an on-chain proposal for emergency macroeconomic transition."""
        self.regime_change_proposals[proposal_id] = {
            "id": proposal_id,
            "target_regime": target_regime,
            "justification": justification,
            "proposer": proposer_citizen_id,
            "votes": {},  # citizen_id -> 1 (yes), -1 (no)
            "status": "OPEN",
            "created_at": int(time.time()),
        }
        return self.regime_change_proposals[proposal_id]

    def vote_on_shift(self, proposal_id: str, citizen_id: str, vote_choice: int) -> bool:
        """Casts an equal-weighted vote (1-Human = 1-Vote)."""
        if proposal_id not in self.regime_change_proposals:
            raise KeyError(f"Proposal {proposal_id} does not exist.")
        prop = self.regime_change_proposals[proposal_id]
        if prop["status"] != "OPEN":
            raise ValueError("Proposal voting is closed.")
        if vote_choice not in (1, -1):
            raise ValueError("Vote must be 1 (approve) or -1 (reject).")

        prop["votes"][citizen_id] = vote_choice
        return True

    def execute_regime_shift(self, proposal_id: str, approval_threshold: float = 0.60) -> bool:
        """Executes the transition if supermajority threshold is achieved."""
        prop = self.regime_change_proposals[proposal_id]
        votes = list(prop["votes"].values())
        if not votes:
            return False

        approvals = sum(1 for v in votes if v == 1)
        ratio = approvals / len(votes)

        if ratio >= approval_threshold:
            self.current_regime = prop["target_regime"]
            prop["status"] = "PASSED_EXECUTED"
            self.history.append({
                "regime": self.current_regime.value,
                "timestamp": int(time.time()),
                "reason": f"Democratic Resolution Passed: {prop['justification']} (Approval: {ratio:.1%})"
            })
            return True
        else:
            prop["status"] = "REJECTED"
            return False
