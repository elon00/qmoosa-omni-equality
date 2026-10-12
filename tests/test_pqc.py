"""
Tests for Post-Quantum Lattice Signatures & Democratic Sovereign Identity.
"""

import pytest
from core.pqc.lattice_id import (
    PostQuantumLatticeSigner,
    SoulboundCitizenIdentity,
)
from core.pqc.equal_rights import DemocraticParityLedger


def test_lattice_signer_sign_and_verify():
    signer = PostQuantumLatticeSigner(seed=b"test_entropy_seed_32_bytes_long!")
    msg = b"Declaration of Universal Equal Rights"

    sig = signer.sign(msg)
    assert "z" in sig
    assert "c_hash" in sig
    assert "msg_hash" in sig

    # Verify signature
    is_valid = PostQuantumLatticeSigner.verify(signer.public_key_t, msg, sig)
    assert is_valid is True

    # Tampered message must fail verification
    is_valid_tampered = PostQuantumLatticeSigner.verify(signer.public_key_t, b"Altered Message", sig)
    assert is_valid_tampered is False


def test_soulbound_identity_assertion():
    citizen = SoulboundCitizenIdentity("human_biometric_entropy_449201")
    assert citizen.citizen_id.startswith("0x")
    assert citizen.legal_weight == 1.0

    assertion = citizen.create_assertion("Vote Yes on Universal Housing")
    is_valid, msg = SoulboundCitizenIdentity.verify_assertion(assertion)
    assert is_valid is True
    assert "Verified" in msg

    # Fraudulent weight tampering must be rejected
    assertion_fake = dict(assertion)
    assertion_fake["payload"] = dict(assertion["payload"])
    assertion_fake["payload"]["legal_weight"] = 100.0  # Wealthy attempt to scale vote
    valid_fake, msg_fake = SoulboundCitizenIdentity.verify_assertion(assertion_fake)
    assert valid_fake is False
    assert "Violation" in msg_fake


def test_democratic_parity_ledger():
    ledger = DemocraticParityLedger()
    c1 = ledger.register_citizen("citizen_alpha")
    c2 = ledger.register_citizen("citizen_beta")
    c3 = ledger.register_citizen("citizen_gamma")

    prop = ledger.create_proposal("PROP-001", "Universal Health Guarantee", "Equitable medical supply distribution", c1.citizen_id)
    assert prop["id"] == "PROP-001"

    # Cast votes: 2 approves, 1 reject
    ledger.cast_vote("PROP-001", c1, 1)
    ledger.cast_vote("PROP-001", c2, 1)
    ledger.cast_vote("PROP-001", c3, -1)

    tally = ledger.tally("PROP-001")
    assert tally["total_votes"] == 3
    assert tally["approvals"] == 2
    assert tally["rejections"] == 1
    assert tally["passed"] is True
