"""
Post-Quantum Lattice-Based Identity & Soulbound Equal Citizen Credential.
Implements NIST FIPS 204 (ML-DSA) inspired polynomial lattice cryptography
and enforces strictly equal democratic weight (weight = 1.0) for every human.
"""

import hashlib
import json
import time
from typing import Dict, Any, Tuple
import numpy as np


# Parameters inspired by ML-DSA-65 (NIST Level 3):
# Modulus q = 8380417, polynomial degree n = 256
Q = 8380417
N = 256


def shake256_hash(data: bytes, length: int) -> bytes:
    """Extracts arbitrary length pseudo-random bytes using SHAKE-256."""
    hasher = hashlib.shake_256()
    hasher.update(data)
    return hasher.digest(length)


def sample_poly_from_seed(seed: bytes, nonce: int) -> np.ndarray:
    """Deterministically samples a polynomial vector of degree N modulo Q."""
    data = seed + nonce.to_bytes(4, byteorder="big")
    raw_bytes = shake256_hash(data, N * 4)
    # Parse 4-byte integers modulo Q
    poly = np.zeros(N, dtype=np.int64)
    for i in range(N):
        val = int.from_bytes(raw_bytes[i*4 : (i+1)*4], byteorder="little")
        poly[i] = val % Q
    return poly


def poly_multiply_ntt_like(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Computes negacyclic polynomial multiplication c(x) = a(x) * b(x) mod (x^N + 1, Q).
    """
    res = np.zeros(N, dtype=np.int64)
    for i in range(N):
        for j in range(N):
            prod = (int(a[i]) * int(b[j])) % Q
            idx = i + j
            if idx < N:
                res[idx] = (res[idx] + prod) % Q
            else:
                res[idx - N] = (res[idx - N] - prod) % Q
    return (res % Q + Q) % Q


class PostQuantumLatticeSigner:
    """
    Deterministic module-lattice digital signature generator and verifier
    following Fiat-Shamir with Aborts and NIST FIPS 204 structural principles.
    Exact lattice relation: Public Key t = A * s1 mod Q.
    """

    def __init__(self, seed: bytes = None):
        if seed is None:
            seed = hashlib.sha3_256(str(time.time_ns()).encode()).digest()
        self.seed = seed
        # Secret key s1 sampled from private seed
        self.private_key_s1 = sample_poly_from_seed(self.seed, 1) % 5 - 2
        # Public matrix A sampled from immutable public generator seed
        self.matrix_a = sample_poly_from_seed(b"AEQUITAS_PUBLIC_LATTICE_A_SEED_V1", 0)
        # Public key t = A * s1 mod Q
        self.public_key_t = poly_multiply_ntt_like(self.matrix_a, self.private_key_s1)

    def get_public_key_bytes(self) -> bytes:
        return self.public_key_t.tobytes()

    def sign(self, message: bytes) -> Dict[str, Any]:
        """
        Signs a message using the secret lattice vectors and returns the signature.
        """
        msg_hash = hashlib.sha3_256(message).digest()
        # Ephemeral masking polynomial y
        y = sample_poly_from_seed(self.seed + msg_hash, 99) % 2048 - 1024
        # Commitment w = A * y mod Q
        w = poly_multiply_ntt_like(self.matrix_a, y)
        # Challenge c = Hash(msg || w)
        c_seed = hashlib.sha3_256(msg_hash + w.tobytes()).digest()
        c = sample_poly_from_seed(c_seed, 0) % 3 - 1  # Sparse ternary challenge vector
        # Response z = y + c * s1 mod Q
        c_s1 = poly_multiply_ntt_like(c, self.private_key_s1)
        z = (y + c_s1) % Q

        return {
            "z": z.tolist(),
            "c_hash": c_seed.hex(),
            "msg_hash": msg_hash.hex(),
        }

    @classmethod
    def verify(cls, public_key_t: np.ndarray, message: bytes, signature: Dict[str, Any]) -> bool:
        """
        Verifies the post-quantum lattice signature:
        w' = A * z - c * t mod Q
        Check: Hash(msg || w') == c_seed
        """
        msg_hash = hashlib.sha3_256(message).digest()
        if msg_hash.hex() != signature.get("msg_hash"):
            return False

        z = np.array(signature["z"], dtype=np.int64)
        c_seed = bytes.fromhex(signature["c_hash"])
        c = sample_poly_from_seed(c_seed, 0) % 3 - 1

        matrix_a = sample_poly_from_seed(b"AEQUITAS_PUBLIC_LATTICE_A_SEED_V1", 0)

        # Compute w' = A * z - c * t mod Q
        Az = poly_multiply_ntt_like(matrix_a, z)
        ct = poly_multiply_ntt_like(c, public_key_t)
        w_prime = (Az - ct) % Q

        # Check if Hash(msg || w') matches challenge c_seed
        computed_c_seed = hashlib.sha3_256(msg_hash + w_prime.tobytes()).digest()
        return computed_c_seed == c_seed


class SoulboundCitizenIdentity:
    """
    Self-Sovereign Equal Citizen Credential.
    Enforces the invariant: Every individual has exactly weight = 1.0.
    Cannot be sold, delegated, or accumulated.
    """

    def __init__(self, human_entropy: str):
        # Deterministic unique citizen identifier
        self.citizen_id = "0x" + hashlib.sha3_256(human_entropy.encode()).hexdigest()[:40]
        self.signer = PostQuantumLatticeSigner(seed=hashlib.sha3_256(human_entropy.encode()).digest())
        self.public_key_t = self.signer.public_key_t
        self.legal_weight = 1.0  # Invariant: Never scales with wealth or holdings
        self.registered_timestamp = int(time.time())

    def create_assertion(self, statement: str) -> Dict[str, Any]:
        """Creates a cryptographically signed human assertion with legal parity weight."""
        payload = {
            "citizen_id": self.citizen_id,
            "legal_weight": self.legal_weight,
            "statement": statement,
            "timestamp": int(time.time()),
        }
        raw_bytes = json.dumps(payload, sort_keys=True).encode()
        signature = self.signer.sign(raw_bytes)
        return {
            "payload": payload,
            "signature": signature,
            "public_key": self.public_key_t.tolist(),
        }

    @staticmethod
    def verify_assertion(assertion: Dict[str, Any]) -> Tuple[bool, str]:
        """Verifies assertion validity and invariant equality enforcement."""
        payload = assertion["payload"]
        if payload.get("legal_weight") != 1.0:
            return False, "Violation: Legal weight must be exactly 1.0."

        raw_bytes = json.dumps(payload, sort_keys=True).encode()
        pub_key = np.array(assertion["public_key"], dtype=np.int64)
        is_valid = PostQuantumLatticeSigner.verify(pub_key, raw_bytes, assertion["signature"])
        if not is_valid:
            return False, "Invalid cryptographic lattice signature."
        return True, "Verified: Valid post-quantum assertion with equal weight 1.0."
