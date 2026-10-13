"""
Post-Quantum Key Lifecycle, Serialization, and Revocation Registry.
Provides production-grade key management for NIST FIPS 204 ML-DSA-65 keys.
"""

import base64
import hashlib
import json
import time
from typing import Dict, Any, Optional, Tuple

from core.pqc.ml_dsa import MLDSA65KeyPair, PK_SIZE, SK_SIZE, SIG_SIZE


class PQCKeySerializer:
    """Serializes and deserializes ML-DSA-65 keys with integrity checksums."""

    @staticmethod
    def export_public_key(pk_bytes: bytes, citizen_id: str) -> str:
        if len(pk_bytes) != PK_SIZE:
            raise ValueError(f"Invalid public key length: {len(pk_bytes)} != {PK_SIZE}")
        b64 = base64.b64encode(pk_bytes).decode("ascii")
        checksum = hashlib.sha256(pk_bytes).hexdigest()[:16]
        payload = {
            "type": "ML-DSA-65-PUBLIC-KEY",
            "citizen_id": citizen_id,
            "checksum": checksum,
            "data": b64,
        }
        return json.dumps(payload, indent=2)

    @staticmethod
    def import_public_key(json_str: str) -> Tuple[bytes, str]:
        obj = json.loads(json_str)
        if obj.get("type") != "ML-DSA-65-PUBLIC-KEY":
            raise ValueError("Invalid key format: expected ML-DSA-65-PUBLIC-KEY")
        pk_bytes = base64.b64decode(obj["data"])
        if len(pk_bytes) != PK_SIZE:
            raise ValueError(f"Corrupted key size: {len(pk_bytes)} != {PK_SIZE}")
        expected_checksum = hashlib.sha256(pk_bytes).hexdigest()[:16]
        if obj.get("checksum") != expected_checksum:
            raise ValueError("Public key checksum mismatch: data corrupted")
        return pk_bytes, obj.get("citizen_id", "")


class KeyRevocationRegistry:
    """
    Manages active vs. revoked ML-DSA-65 public keys with signature authentication.
    Prevents compromised keys from continuing to cast ballots or authorize actions.
    """

    def __init__(self):
        self.active_keys: Dict[str, bytes] = {}      # citizen_id -> pk_bytes
        self.revoked_keys: Dict[str, Dict[str, Any]] = {}  # sha256(pk) -> revocation metadata

    def enroll_key(self, citizen_id: str, pk_bytes: bytes) -> None:
        if len(pk_bytes) != PK_SIZE:
            raise ValueError(f"Invalid ML-DSA-65 key length: {len(pk_bytes)}")
        pk_hash = hashlib.sha256(pk_bytes).hexdigest()
        if pk_hash in self.revoked_keys:
            raise ValueError("Cannot enroll a previously revoked key")
        self.active_keys[citizen_id] = pk_bytes

    def revoke_key(
        self,
        citizen_id: str,
        reason: str,
        revocation_signature: bytes,
        timestamp: Optional[int] = None
    ) -> bool:
        """Revokes a key using an authentic ML-DSA-65 revocation statement."""
        if citizen_id not in self.active_keys:
            raise KeyError(f"Citizen {citizen_id} has no active key registered")
        current_pk = self.active_keys[citizen_id]

        ts = timestamp if timestamp is not None else int(time.time())
        statement = json.dumps({
            "action": "REVOKE_KEY",
            "citizen_id": citizen_id,
            "reason": reason,
            "timestamp": ts
        }, sort_keys=True).encode("utf-8")

        # Verify signature with current active key
        is_valid = MLDSA65KeyPair.verify(current_pk, statement, revocation_signature, ctx=b"OEQ-REVOCATION-V1")
        if not is_valid:
            raise PermissionError("Revocation failed: invalid ML-DSA-65 signature on revocation statement")

        pk_hash = hashlib.sha256(current_pk).hexdigest()
        self.revoked_keys[pk_hash] = {
            "citizen_id": citizen_id,
            "reason": reason,
            "revoked_at": ts,
            "statement_digest": hashlib.sha256(statement).hexdigest()
        }
        del self.active_keys[citizen_id]
        return True

    def is_key_valid(self, citizen_id: str, pk_bytes: bytes) -> bool:
        """Returns True if the key is currently active and not revoked."""
        pk_hash = hashlib.sha256(pk_bytes).hexdigest()
        if pk_hash in self.revoked_keys:
            return False
        return self.active_keys.get(citizen_id) == pk_bytes
