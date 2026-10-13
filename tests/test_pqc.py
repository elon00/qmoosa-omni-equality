"""
Comprehensive Test Suite for NIST FIPS 204 ML-DSA-65 & Soulbound Sovereign Identity.
"""

import pytest
from core.pqc.ml_dsa import MLDSA65KeyPair
from core.pqc.lattice_id import SoulboundCitizenIdentity
from core.pqc.equal_rights import DemocraticParityLedger


def test_ml_dsa_65_signature_lifecycle():
    pair = MLDSA65KeyPair.generate()
    msg = b"Universal Declaration of Human Equality & Socio-Economic Parity"
    sig = pair.sign(msg)

    # 1. Valid signature verifies
    assert MLDSA65KeyPair.verify(pair.public_key_bytes, msg, sig) is True

    # 2. Tampered message fails verification
    tampered_msg = b"Tampered Message: Wealthy Privilege Clause"
    assert MLDSA65KeyPair.verify(pair.public_key_bytes, tampered_msg, sig) is False

    # 3. Wrong public key fails verification
    other_pair = MLDSA65KeyPair.generate()
    assert MLDSA65KeyPair.verify(other_pair.public_key_bytes, msg, sig) is False

    # 4. Domain separation context verification
    sig_ctx = pair.sign(msg, ctx=b"QMOOSA-BALLOT")
    assert MLDSA65KeyPair.verify(pair.public_key_bytes, msg, sig_ctx, ctx=b"QMOOSA-BALLOT") is True
    assert MLDSA65KeyPair.verify(pair.public_key_bytes, msg, sig_ctx, ctx=b"DIFFERENT-CONTEXT") is False

    # 5. Malformed signature length or corrupted bit fails closed
    corrupt_sig = bytearray(sig)
    corrupt_sig[42] ^= 0xAA
    assert MLDSA65KeyPair.verify(pair.public_key_bytes, msg, bytes(corrupt_sig)) is False
    assert MLDSA65KeyPair.verify(pair.public_key_bytes, msg, sig[:-10]) is False


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
