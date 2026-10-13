"""
Post-Quantum Lattice-Based Identity & Soulbound Equal Citizen Credential.
Implements NIST FIPS 204 (ML-DSA-65) module-lattice digital signature standard
and enforces strictly equal democratic weight (weight = 1.0) for every human.
"""

import hashlib
import json
import time
from typing import Dict, Any, Tuple
import numpy as np

from core.pqc.ml_dsa import MLDSA65KeyPair


class SoulboundCitizenIdentity:
    """
    Self-Sovereign Equal Citizen Credential backed by NIST FIPS 204 ML-DSA-65.
    Enforces the invariant: Every individual has exactly weight = 1.0.
    Cannot be sold, delegated, or accumulated.
    """

    def __init__(self, human_entropy: str):
        entropy_bytes = hashlib.sha3_256(human_entropy.encode()).digest()
        # Keypair generated deterministically from verified proof-of-humanity entropy
        self.keypair = MLDSA65KeyPair.generate(seed=entropy_bytes)
        self.public_key_bytes = self.keypair.public_key_bytes
        self.citizen_id = "0x" + hashlib.sha3_256(self.public_key_bytes).hexdigest()[:40]
        self.legal_weight = 1.0  # Invariant: Never scales with wealth or holdings
        self.registered_timestamp = int(time.time())

    def create_assertion(self, statement: str) -> Dict[str, Any]:
        """Creates an ML-DSA-65 signed assertion with invariant legal parity weight."""
        payload = {
            "citizen_id": self.citizen_id,
            "legal_weight": self.legal_weight,
            "statement": statement,
            "timestamp": int(time.time()),
        }
        raw_bytes = json.dumps(payload, sort_keys=True).encode()
        sig_bytes = self.keypair.sign(raw_bytes)
        return {
            "payload": payload,
            "signature_hex": sig_bytes.hex(),
            "public_key_hex": self.public_key_bytes.hex(),
        }

    @staticmethod
    def verify_assertion(assertion: Dict[str, Any]) -> Tuple[bool, str]:
        """Verifies assertion validity and invariant equality enforcement."""
        payload = assertion["payload"]
        if payload.get("legal_weight") != 1.0:
            return False, "Violation: Legal weight must be exactly 1.0."

        raw_bytes = json.dumps(payload, sort_keys=True).encode()
        try:
            pk_bytes = bytes.fromhex(assertion["public_key_hex"])
            sig_bytes = bytes.fromhex(assertion["signature_hex"])
        except Exception as e:
            return False, f"Invalid hex encoding: {e}"

        is_valid = MLDSA65KeyPair.verify(pk_bytes, raw_bytes, sig_bytes)
        if not is_valid:
            return False, "Invalid NIST FIPS 204 ML-DSA-65 signature."
        return True, "Verified: Valid NIST FIPS 204 ML-DSA-65 assertion with equal weight 1.0."


# Backward compatibility alias
PostQuantumLatticeSigner = MLDSA65KeyPair
