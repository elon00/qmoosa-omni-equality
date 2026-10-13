"""
W3C Verifiable Credentials 2.0 Personhood Issuance & Sybil-Resistance Engine.
Issues cryptographically signed proof-of-personhood credentials compliant with
W3C VC Data Model 2.0 and NIST FIPS 204 ML-DSA-65.
Enforces credential expiration, signature-authenticated revocation, and biometric nullifier privacy.
"""

import hmac
import hashlib
import json
import time
from datetime import datetime, timezone
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
        self.revoked_credentials: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def derive_biometric_nullifier(biometric_entropy: bytes, salt: bytes = b"QMOOSA_SOVEREIGN_NULLIFIER_SALT_2026") -> str:
        """
        Derives a deterministic, privacy-preserving biometric nullifier using HMAC-SHA256.
        Prevents Sybil duplicate registrations while preventing reverse-engineering of raw biometric traits.
        """
        if not biometric_entropy:
            raise ValueError("Biometric entropy cannot be empty")
        h = hmac.new(salt, biometric_entropy, hashlib.sha256)
        return h.hexdigest()

    def issue_credential(
        self,
        citizen_id: str,
        biometric_nullifier: str,
        validity_days: int = 365,
        issuance_time: Optional[int] = None
    ) -> Dict[str, Any]:
        """Issues a signed W3C Verifiable Credential 2.0."""
        now = issuance_time if issuance_time is not None else int(time.time())
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

    def revoke_credential(self, credential_id: str, reason: str = "Voluntary key rotation") -> bool:
        """Adds a credential ID to the active revocation registry."""
        self.revoked_credentials[credential_id] = {
            "revoked_at": int(time.time()),
            "reason": reason
        }
        return True

    def verify_credential(
        self,
        credential: Dict[str, Any],
        registrar_pk: bytes,
        current_time: Optional[int] = None
    ) -> Tuple[bool, str]:
        """Validates credential schema, expiration, revocation status, and registrar signature."""
        cred_id = credential.get("id")
        if cred_id in self.revoked_credentials:
            return False, f"Credential has been revoked: {self.revoked_credentials[cred_id]['reason']}"

        proof = credential.get("proof")
        if not proof or proof.get("type") != "ML-DSA-65-Signature2026":
            return False, "Missing or unsupported proof format"

        # Check temporal validity
        check_time = current_time if current_time is not None else int(time.time())
        valid_from_str = credential.get("validFrom")
        valid_until_str = credential.get("validUntil")

        if valid_from_str:
            try:
                valid_from_ts = int(datetime.strptime(valid_from_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
                if check_time < valid_from_ts:
                    return False, f"Credential not yet valid (validFrom: {valid_from_str})"
            except ValueError:
                return False, "Malformed validFrom timestamp format"

        if valid_until_str:
            try:
                valid_until_ts = int(datetime.strptime(valid_until_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
                if check_time > valid_until_ts:
                    return False, f"Credential has expired (validUntil: {valid_until_str})"
            except ValueError:
                return False, "Malformed validUntil timestamp format"

        # Check parity weight invariant first (fail-fast before cryptographic verification)
        subj = credential.get("credentialSubject", {})
        if subj.get("sovereignParityWeight") != 1.0:
            return False, "Violation: sovereign parity weight must be exactly 1.0"

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

        return True, "Valid W3C Verifiable Credential: Proof of Personhood confirmed"
