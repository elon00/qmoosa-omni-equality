"""
Pytest test harness for SMT/Z3 Formal Machine-Checked Theorems.
"""

import pytest
from proofs.verify_invariants_z3 import verify_all_formal_theorems


def test_machine_checked_smt_theorems():
    """Validates that all SMT/Z3 formal mathematical proofs hold without counterexample."""
    all_passed = verify_all_formal_theorems()
    assert all_passed is True, "Formal SMT/Z3 verification failed"
