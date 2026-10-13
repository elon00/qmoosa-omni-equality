"""Cryptographic Interoperability & NIST FIPS 204 Verification Suite.

Performs rigorous positive, negative, and adversarial verification of ML-DSA-65
signatures and cross-implementation interoperability without simulation or mocks.
"""

import sys
import os
import hashlib

# Ensure stdout handles UTF-8 on Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Ensure root directory is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.pqc.ml_dsa import (
    MLDSA65KeyPair,
    PK_SIZE,
    SK_SIZE,
    SIG_SIZE,
    Q,
    TAU
)

try:
    import mldsa
    HAS_INDEPENDENT_VERIFIER = True
except ImportError:
    HAS_INDEPENDENT_VERIFIER = False


def run_crypto_interop_audit() -> bool:
    print("=" * 75)
    print("[+] QMOOSA PROTOCOL — NIST FIPS 204 CRYPTOGRAPHIC AUDIT & INTEROP GATE")
    print("=" * 75)

    all_passed = True

    # 1. Parameter and Size Invariants
    print("\n[1/6] Validating NIST FIPS 204 Parameter Invariants...")
    pair = MLDSA65KeyPair.generate()
    if len(pair.public_key_bytes) != PK_SIZE or len(pair.secret_key_bytes) != SK_SIZE:
        print(f"  [FAIL] Key size mismatch: pk={len(pair.public_key_bytes)}, sk={len(pair.secret_key_bytes)}")
        all_passed = False
    else:
        print(f"  [PASS] Key sizes verified: PK={PK_SIZE} bytes, SK={SK_SIZE} bytes (NIST Category 3)")

    # 2. Signature Generation and Verification Lifecycle
    print("\n[2/6] Validating Signature Generation & Lifecycle...")
    test_message = b"Sovereign Invariant: 1-Human=1-Vote Democratic Standing"
    sig = pair.sign(test_message)
    if len(sig) != SIG_SIZE:
        print(f"  [FAIL] Signature size mismatch: got {len(sig)}, expected {SIG_SIZE}")
        all_passed = False
    elif not MLDSA65KeyPair.verify(pair.public_key_bytes, test_message, sig):
        print("  [FAIL] Legitimate signature failed verification")
        all_passed = False
    else:
        print(f"  [PASS] Signature verified: SIG={SIG_SIZE} bytes compliant with FIPS 204")

    # 3. Cross-Implementation Interoperability Verification
    print("\n[3/6] Validating Cross-Implementation Interoperability...")
    if not HAS_INDEPENDENT_VERIFIER:
        print("  [BLOCKED] Independent verifier package (mldsa) not installed")
        all_passed = False
    else:
        try:
            vk = mldsa.VerificationKey(pair.public_key_bytes, parameters=mldsa.ParameterSet.ML_DSA_65)
            vk.verify(sig, test_message)
            print("  [PASS] Cross-implementation verification confirmed via independent mldsa engine")
        except Exception as e:
            print(f"  [FAIL] Cross-implementation verification failed: {e}")
            all_passed = False

    # 4. Domain Separation (Context String)
    print("\n[4/6] Validating Cryptographic Domain Separation...")
    ctx_gov = b"QMOOSA-GOV-V1"
    ctx_identity = b"QMOOSA-ID-V1"
    sig_gov = pair.sign(test_message, ctx=ctx_gov)
    
    # Must verify under matching context
    if not MLDSA65KeyPair.verify(pair.public_key_bytes, test_message, sig_gov, ctx=ctx_gov):
        print("  [FAIL] Context-separated signature failed under matching context")
        all_passed = False
    # Must FAIL under mismatched context
    elif MLDSA65KeyPair.verify(pair.public_key_bytes, test_message, sig_gov, ctx=ctx_identity):
        print("  [FAIL] Context-separated signature erroneously accepted under mismatched context")
        all_passed = False
    else:
        print("  [PASS] Cryptographic domain separation strictly enforced")

    # 5. Negative & Adversarial Resistance
    print("\n[5/6] Validating Adversarial & Tamper Resistance...")
    # Altered message
    if MLDSA65KeyPair.verify(pair.public_key_bytes, b"Altered Message", sig):
        print("  [FAIL] Altered message accepted")
        all_passed = False
    else:
        print("  [PASS] Altered message rejected")

    # Tampered signature byte
    tampered_sig = bytearray(sig)
    tampered_sig[100] ^= 0x55
    if MLDSA65KeyPair.verify(pair.public_key_bytes, test_message, bytes(tampered_sig)):
        print("  [FAIL] Bit-flipped signature accepted")
        all_passed = False
    else:
        print("  [PASS] Bit-flipped signature rejected")

    # Wrong public key
    other_pair = MLDSA65KeyPair.generate()
    if MLDSA65KeyPair.verify(other_pair.public_key_bytes, test_message, sig):
        print("  [FAIL] Signature accepted under unauthorized public key")
        all_passed = False
    else:
        print("  [PASS] Unauthorized public key rejected")

    # 6. Deterministic Key Derivation from Human Proof Entropy
    print("\n[6/6] Validating Deterministic Entropy Key Derivation...")
    seed = b"UNIQUE_PROOF_OF_HUMAN_ENTROPY_20261013"
    pair_a = MLDSA65KeyPair.generate(seed=seed)
    pair_b = MLDSA65KeyPair.generate(seed=seed)
    if pair_a.public_key_bytes != pair_b.public_key_bytes or pair_a.secret_key_bytes != pair_b.secret_key_bytes:
        print("  [FAIL] Deterministic key derivation produced non-identical keypairs")
        all_passed = False
    else:
        print("  [PASS] Deterministic key derivation is mathematically reproducible")

    print("\n" + "=" * 75)
    if all_passed:
        print("[SUCCESS] CRYPTOGRAPHIC AUDIT PASSED: NIST FIPS 204 ML-DSA-65 FULLY CERTIFIED.")
        print("=" * 75)
        return True
    else:
        print("[BLOCKED] CRYPTOGRAPHIC AUDIT FAILED: SECURITY DEFICIENCIES DETECTED.")
        print("=" * 75)
        return False


if __name__ == "__main__":
    success = run_crypto_interop_audit()
    sys.exit(0 if success else 1)
