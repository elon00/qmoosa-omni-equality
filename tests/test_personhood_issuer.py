"""
Tests for W3C Verifiable Credentials 2.0 Personhood Issuance & Lifecycle.
"""

import time
import pytest
from core.pqc.ml_dsa import MLDSA65KeyPair
from core.identity.personhood_issuer import PersonhoodCredentialIssuer


def test_personhood_credential_issuance_and_verification():
    registrar_pair = MLDSA65KeyPair.generate()
    issuer = PersonhoodCredentialIssuer("did:qmoosa:registrar:global-01", registrar_pair)

    nullifier = PersonhoodCredentialIssuer.derive_biometric_nullifier(b"raw_iris_telemetry_entropy_vector_01")
    assert len(nullifier) == 64

    cred = issuer.issue_credential(
        citizen_id="0xabc123456789",
        biometric_nullifier=nullifier,
        validity_days=180
    )

    assert cred["type"] == ["VerifiableCredential", "ProofOfPersonhoodCredential"]
    assert cred["credentialSubject"]["sovereignParityWeight"] == 1.0

    valid, msg = issuer.verify_credential(cred, registrar_pair.public_key_bytes)
    assert valid is True
    assert "Proof of Personhood confirmed" in msg

    # Test tampering: altered weight
    tampered_cred = dict(cred)
    tampered_cred["credentialSubject"] = dict(cred["credentialSubject"])
    tampered_cred["credentialSubject"]["sovereignParityWeight"] = 5.0
    valid_tamper, msg_tamper = issuer.verify_credential(tampered_cred, registrar_pair.public_key_bytes)
    assert valid_tamper is False
    assert "sovereign parity weight must be exactly 1.0" in msg_tamper

    # Test tampering: altered citizen ID while preserving weight 1.0
    tampered_id = dict(cred)
    tampered_id["credentialSubject"] = dict(cred["credentialSubject"])
    tampered_id["credentialSubject"]["id"] = "did:qmoosa:citizen:0xattacker999"
    valid_id, msg_id = issuer.verify_credential(tampered_id, registrar_pair.public_key_bytes)
    assert valid_id is False
    assert "Invalid cryptographic signature from registrar" in msg_id


def test_personhood_credential_expiration():
    registrar_pair = MLDSA65KeyPair.generate()
    issuer = PersonhoodCredentialIssuer("did:qmoosa:registrar:global-01", registrar_pair)

    now = int(time.time())
    # Issue credential that expired yesterday (issued 10 days ago, valid for 5 days)
    past_issuance = now - (10 * 86400)
    expired_cred = issuer.issue_credential(
        citizen_id="0xexpired123",
        biometric_nullifier="dummy_nullifier",
        validity_days=5,
        issuance_time=past_issuance
    )

    valid, msg = issuer.verify_credential(expired_cred, registrar_pair.public_key_bytes, current_time=now)
    assert valid is False
    assert "Credential has expired" in msg


def test_personhood_credential_revocation():
    registrar_pair = MLDSA65KeyPair.generate()
    issuer = PersonhoodCredentialIssuer("did:qmoosa:registrar:global-01", registrar_pair)

    cred = issuer.issue_credential(
        citizen_id="0xrevoked456",
        biometric_nullifier="dummy_nullifier",
        validity_days=30
    )

    cred_id = cred["id"]
    issuer.revoke_credential(cred_id, reason="Subject requested key pair rotation")

    valid, msg = issuer.verify_credential(cred, registrar_pair.public_key_bytes)
    assert valid is False
    assert "Credential has been revoked" in msg


def test_biometric_nullifier_determinism_and_privacy():
    raw_data = b"confidential_iris_scan_vector_vector_xyz"
    n1 = PersonhoodCredentialIssuer.derive_biometric_nullifier(raw_data)
    n2 = PersonhoodCredentialIssuer.derive_biometric_nullifier(raw_data)
    assert n1 == n2

    diff_raw = b"confidential_iris_scan_vector_vector_abc"
    n3 = PersonhoodCredentialIssuer.derive_biometric_nullifier(diff_raw)
    assert n1 != n3

    with pytest.raises(ValueError):
        PersonhoodCredentialIssuer.derive_biometric_nullifier(b"")
