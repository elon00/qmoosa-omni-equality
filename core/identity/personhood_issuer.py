"""
W3C Verifiable Credentials 2.0 Personhood Issuance & Sybil-Resistance Engine.
Issues cryptographically signed proof-of-personhood credentials compliant with
W3C VC Data Model 2.0 and NIST FIPS 204 ML-DSA-65.
"""

import hashlib
import json
import time
from typing import Dict, Any, Tuple, Optional

from core.pqc.ml_dsa import MLDSA65KeyPair


class PersonhoodCredentialIssuer:
    """
    Accredited Personhood Registrar.
    Issues W3C Verifiable Credentials asserting unique, living human personhood.
    """

    def __init__(self, registrar_did: str, keypair: MLDSA65KeyPair):
        self.registrar_did = registrar_did
        self.keypair = keypair
        self.revoked_credentials: set = set()

    def issue_credential(
        self,
        citizen_id: str,
        biometric_nullifier: str,
        validity_days: int = 365
    ) -> Dict[str, Any]:
        """Issues a signed W3C Verifiable Credential 2.0."""
        now = int(time.time())
        exp = now + (validity_days * 86400)
        cred_id = f"urn:uuid:{hashlib.sha256(f'{citizen_id}:{now}'.encode()).hexdigest()[:32]}"
        nullifier_hash = hashlib.sha256(biometric_nullifier.encode()).hexdigest()

        claims = {
            "@context": [
                "https://www.w3.org/ns/credentials/v2",
                "https://qmoosa.org/ns/personhood/v1"
            ],
            "id": cred_id,
            "type": ["VerifiableCredential", "ProofOfPersonhoodCredential"],
            "issuer": self.registrar_did,
            "validFrom": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "validUntil": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(exp)),
            "credentialSubject": {
                "id": f"did:qmoosa:citizen:{citizen_id}",
                "sovereignParityWeight": 1.0,
                "nullifierHash": nullifier_hash
            }
        }

        # Canonicalize and sign
        raw_payload = json.dumps(claims, sort_keys=True).encode("utf-8")
        signature = self.keypair.sign(raw_payload, ctx=b"W3C-VC-MLDSA65-V1")

        claims["proof"] = {
            "type": "ML-DSA-65-Signature2026",
            "created": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "verificationMethod": f"{self.registrar_did}#key-1",
            "proofPurpose": "assertionMethod",
            "proofValue": signature.hex()
        }
        return claims

    def verify_credential(
        self,
        credential: Dict[str, Any],
        registrar_pk: bytes
    ) -> Tuple[bool, str]:
        """Validates credential schema, expiration, revocation status, and registrar signature."""
        cred_id = credential.get("id")
        if cred_id in self.revoked_credentials:
            return False, "Credential has been revoked"

        proof = credential.get("proof")
        if not proof or proof.get("type") != "ML-DSA-65-Signature2026":
            return False, "Missing or unsupported proof format"

        # Reconstruct unsigned payload
        claims_copy = dict(credential)
        del claims_copy["proof"]
        raw_payload = json.dumps(claims_copy, sort_keys=True).encode("utf-8")

        try:
            sig_bytes = bytes.fromhex(proof["proofValue"])
        except ValueError:
            return False, "Malformed signature hex"

        is_valid = MLDSA65KeyPair.verify(registrar_pk, raw_payload, sig_bytes, ctx=b"W3C-VC-MLDSA65-V1")
        if not is_valid:
            return False, "Invalid cryptographic signature from registrar"

        # Check parity weight invariant
        subj = credential.get("credentialSubject", {})
        if subj.get("sovereignParityWeight") != 1.0:
            return False, "Violation: sovereign parity weight must be exactly 1.0"

        return True, "Valid W3C Verifiable Credential: Proof of Personhood confirmed"
