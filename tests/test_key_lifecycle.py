"""
Tests for Post-Quantum Key Lifecycle, Serialization, and Revocation Registry.
"""

import json
import pytest
from core.pqc.ml_dsa import MLDSA65KeyPair
from core.pqc.key_lifecycle import PQCKeySerializer, KeyRevocationRegistry


def test_key_serialization_roundtrip():
    pair = MLDSA65KeyPair.generate()
    exported = PQCKeySerializer.export_public_key(pair.public_key_bytes, "citizen_alice")
    assert "ML-DSA-65-PUBLIC-KEY" in exported
    assert "checksum" in exported

    imported_pk, citizen_id = PQCKeySerializer.import_public_key(exported)
    assert imported_pk == pair.public_key_bytes
    assert citizen_id == "citizen_alice"


def test_key_revocation_workflow():
    registry = KeyRevocationRegistry()
    pair = MLDSA65KeyPair.generate()
    registry.enroll_key("citizen_bob", pair.public_key_bytes)

    assert registry.is_key_valid("citizen_bob", pair.public_key_bytes) is True

    # Construct and sign revocation statement
    statement = json.dumps({
        "action": "REVOKE_KEY",
        "citizen_id": "citizen_bob",
        "reason": "Suspected device compromise",
        "timestamp": 1700000000
    }, sort_keys=True).encode("utf-8")
    sig = pair.sign(statement, ctx=b"OEQ-REVOCATION-V1")

    revoked = registry.revoke_key("citizen_bob", "Suspected device compromise", sig, timestamp=1700000000)
    assert revoked is True

    # After revocation, key is invalid
    assert registry.is_key_valid("citizen_bob", pair.public_key_bytes) is False

    # Attempting to re-enroll revoked key fails
    with pytest.raises(ValueError, match="previously revoked"):
        registry.enroll_key("citizen_bob", pair.public_key_bytes)
