"""
Tests for W3C Verifiable Credentials 2.0 Personhood Issuance.
"""

from core.pqc.ml_dsa import MLDSA65KeyPair
from core.identity.personhood_issuer import PersonhoodCredentialIssuer


def test_personhood_credential_issuance_and_verification():
    registrar_pair = MLDSA65KeyPair.generate()
    issuer = PersonhoodCredentialIssuer("did:qmoosa:registrar:global-01", registrar_pair)

    cred = issuer.issue_credential(
        citizen_id="0xabc123456789",
        biometric_nullifier="iris_hash_entropy_sample_99",
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
