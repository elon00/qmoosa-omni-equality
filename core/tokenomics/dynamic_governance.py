"""Fail-closed, authenticated off-chain governance prototype.

This is NOT proof of unique human identity or on-chain governance. Keys must be
bound to verified persons by a separately audited enrollment/issuer service.
"""
import json
import time
from enum import Enum
from hashlib import sha256
from typing import Dict
from core.pqc.ml_dsa import MLDSA65KeyPair

CTX = b"OEQ-GOVERNANCE-V1"

class MacroeconomicRegime(Enum):
    EQUILIBRIUM = "EQUILIBRIUM"
    RECESSION_SHOCK = "RECESSION_SHOCK"
    BLACK_SWAN_CRISIS = "BLACK_SWAN_CRISIS"
    BOOM_EXPANSION = "BOOM_EXPANSION"

REGIME_CONFIGS = {
    MacroeconomicRegime.EQUILIBRIUM: dict(holding_threshold=1_000_000.0,flow_share_pct=.40,legal_share_pct=.20,burn_share_pct=.40),
    MacroeconomicRegime.RECESSION_SHOCK: dict(holding_threshold=500_000.0,flow_share_pct=.60,legal_share_pct=.20,burn_share_pct=.20),
    MacroeconomicRegime.BLACK_SWAN_CRISIS: dict(holding_threshold=250_000.0,flow_share_pct=.70,legal_share_pct=.20,burn_share_pct=.10),
    MacroeconomicRegime.BOOM_EXPANSION: dict(holding_threshold=2_000_000.0,flow_share_pct=.30,legal_share_pct=.20,burn_share_pct=.50),
}

def canonical(payload):
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()

class DynamicAdaptabilityEngine:
    """Authenticated off-chain voting. Signatures do NOT independently prove personhood."""
    def __init__(self, eligible_voters: Dict[str, bytes], initial_regime=MacroeconomicRegime.EQUILIBRIUM,
                 quorum_numerator=1, quorum_denominator=2):
        if not eligible_voters or len(eligible_voters) != len(set(eligible_voters)):
            raise ValueError("Non-empty, unique voter registry required")
        if any(not k or not isinstance(v, bytes) or len(v) != 1952 for k, v in eligible_voters.items()):
            raise ValueError("Valid ML-DSA-65 public keys required")
        if not (0 < quorum_numerator <= quorum_denominator):
            raise ValueError("Invalid quorum")
        self.registry = dict(eligible_voters)
        self.quorum_numerator, self.quorum_denominator = quorum_numerator, quorum_denominator
        self.current_regime = initial_regime
        self.regime_change_proposals = {}
        self.history = [{"regime": initial_regime.value, "timestamp": int(time.time()), "reason": "Initialized"}]

    def get_active_parameters(self):
        return dict(active_regime=self.current_regime.value, **REGIME_CONFIGS[self.current_regime])

    @staticmethod
    def proposal_payload(proposal_id, target_regime, justification, deadline):
        return canonical(dict(domain="OEQ-PROPOSAL-V1", proposal_id=proposal_id,
                              target_regime=target_regime.value, justification=justification,
                              deadline=deadline))

    @staticmethod
    def ballot_payload(proposal_id, proposal_digest, citizen_id, vote_choice, deadline):
        return canonical(dict(domain="OEQ-BALLOT-V1", proposal_id=proposal_id,
                              proposal_digest=proposal_digest, citizen_id=citizen_id,
                              vote=vote_choice, deadline=deadline))

    def propose_regime_shift(self, proposal_id, target_regime, justification, proposer_citizen_id,
                             deadline, signature, now=None):
        now = int(time.time()) if now is None else int(now)
        if proposer_citizen_id not in self.registry:
            raise PermissionError("Ineligible proposer")
        if not proposal_id or proposal_id in self.regime_change_proposals:
            raise ValueError("Duplicate or empty proposal ID")
        if not isinstance(target_regime, MacroeconomicRegime) or not justification.strip():
            raise ValueError("Invalid proposal")
        if not isinstance(deadline, int) or deadline <= now:
            raise ValueError("Deadline must be in the future")
        data = self.proposal_payload(proposal_id, target_regime, justification, deadline)
        if not MLDSA65KeyPair.verify(self.registry[proposer_citizen_id], data, signature, ctx=CTX):
            raise PermissionError("Invalid proposer signature")
        digest = sha256(data).hexdigest()
        prop = dict(id=proposal_id, target_regime=target_regime, justification=justification,
                    proposer=proposer_citizen_id, votes={}, status="OPEN", created_at=now,
                    deadline=deadline, proposal_digest=digest, voter_snapshot=dict(self.registry))
        self.regime_change_proposals[proposal_id] = prop
        return prop

    def vote_on_shift(self, proposal_id, citizen_id, vote_choice, signature, now=None):
        now = int(time.time()) if now is None else int(now)
        prop = self.regime_change_proposals[proposal_id]
        if prop["status"] != "OPEN" or now >= prop["deadline"]:
            raise ValueError("Voting closed")
        if citizen_id not in prop["voter_snapshot"]:
            raise PermissionError("Ineligible voter")
        if citizen_id in prop["votes"]:
            raise ValueError("Duplicate ballot/replay rejected")
        if type(vote_choice) is not int or vote_choice not in (1, -1):
            raise ValueError("Invalid vote")
        payload = self.ballot_payload(proposal_id, prop["proposal_digest"], citizen_id,
                                      vote_choice, prop["deadline"])
        if not MLDSA65KeyPair.verify(prop["voter_snapshot"][citizen_id], payload, signature, ctx=CTX):
            raise PermissionError("Invalid ballot signature")
        prop["votes"][citizen_id] = vote_choice
        return True

    def execute_regime_shift(self, proposal_id, now=None):
        now = int(time.time()) if now is None else int(now)
        prop = self.regime_change_proposals[proposal_id]
        if prop["status"] != "OPEN":
            raise ValueError("Already finalized")
        if now < prop["deadline"]:
            raise ValueError("Voting window not finished")
        total_eligible = len(prop["voter_snapshot"])
        participation = len(prop["votes"])
        approvals = sum(v == 1 for v in prop["votes"].values())
        quorum_met = participation * self.quorum_denominator >= total_eligible * self.quorum_numerator
        supermajority_met = approvals * 5 >= participation * 3  # 60% of valid participating votes
        if quorum_met and participation > 0 and supermajority_met:
            self.current_regime = prop["target_regime"]
            prop["status"] = "PASSED_EXECUTED"
            self.history.append({"regime": self.current_regime.value, "timestamp": now,
                                 "reason": "Authenticated vote; off-chain only"})
            return True
        prop["status"] = "REJECTED"
        return False
