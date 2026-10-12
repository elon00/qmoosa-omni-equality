"""
Equal Rights & Democratic Parity Consensus Engine.
Ensures that all governance votes, resource allocation vetoes,
and rule amendments adhere to 1-Human = 1-Vote or Quadratic Funding
with equal credit endowments, preventing plutocratic takeover.
"""

from typing import Dict, List, Any
import numpy as np
from core.pqc.lattice_id import SoulboundCitizenIdentity


class DemocraticParityLedger:
    """
    Maintains registered Soulbound identities and computes egalitarian consensus.
    """

    def __init__(self):
        self.registered_citizens: Dict[str, SoulboundCitizenIdentity] = {}
        self.proposals: Dict[str, Dict[str, Any]] = {}

    def register_citizen(self, human_entropy: str) -> SoulboundCitizenIdentity:
        citizen = SoulboundCitizenIdentity(human_entropy)
        if citizen.citizen_id in self.registered_citizens:
            raise ValueError(f"Citizen {citizen.citizen_id} already registered.")
        self.registered_citizens[citizen.citizen_id] = citizen
        return citizen

    def create_proposal(self, proposal_id: str, title: str, description: str, creator_id: str) -> Dict[str, Any]:
        if creator_id not in self.registered_citizens:
            raise PermissionError("Only registered citizens can create proposals.")
        self.proposals[proposal_id] = {
            "id": proposal_id,
            "title": title,
            "description": description,
            "creator": creator_id,
            "votes": {},  # citizen_id -> vote (-1, 0, 1) or quadratic voice credits
            "tallied": False,
            "passed": False,
        }
        return self.proposals[proposal_id]

    def cast_vote(self, proposal_id: str, citizen: SoulboundCitizenIdentity, vote_choice: int) -> bool:
        """
        Casts a vote. Regardless of an individual's financial wealth,
        every citizen has equal vote weight: -1, 0, or 1.
        """
        if proposal_id not in self.proposals:
            raise KeyError(f"Proposal {proposal_id} does not exist.")
        if citizen.citizen_id not in self.registered_citizens:
            raise PermissionError("Unregistered citizen cannot vote.")
        if vote_choice not in (-1, 0, 1):
            raise ValueError("Vote must be -1 (reject), 0 (abstain), or 1 (approve).")

        # Create signed assertion
        assertion = citizen.create_assertion(f"VOTE:{proposal_id}:{vote_choice}")
        is_valid, msg = SoulboundCitizenIdentity.verify_assertion(assertion)
        if not is_valid:
            raise ValueError(f"Signature verification failed: {msg}")

        self.proposals[proposal_id]["votes"][citizen.citizen_id] = vote_choice
        return True

    def tally(self, proposal_id: str, approval_threshold: float = 0.5) -> Dict[str, Any]:
        """Tallies proposal votes with equal weighting."""
        prop = self.proposals[proposal_id]
        votes = list(prop["votes"].values())
        if not votes:
            return {"total_votes": 0, "approvals": 0, "rejections": 0, "passed": False}

        approvals = sum(1 for v in votes if v == 1)
        rejections = sum(1 for v in votes if v == -1)
        total = len(votes)

        passed = (approvals / total) > approval_threshold
        prop["tallied"] = True
        prop["passed"] = passed

        return {
            "proposal_id": proposal_id,
            "total_votes": total,
            "approvals": approvals,
            "rejections": rejections,
            "approval_ratio": float(approvals / total),
            "passed": passed,
        }
