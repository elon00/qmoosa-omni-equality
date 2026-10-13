"""
Tests for Formal Accounting Invariants and Conservation Theorems.
"""

from core.proofs.accounting_spec import FormalInvariantVerifier


def test_formal_supply_conservation():
    initial_supply = 10_000_000.0
    circulating = [3_000_000.0, 2_000_000.0, 1_000_000.0]  # Sum = 6M
    flow_pool = 1_600_000.0                                 # 40% of 4M surplus
    legal_escrow = 800_000.0                                # 20% of 4M surplus
    total_burned = 1_600_000.0                              # 40% of 4M surplus
    # 6M + 1.6M + 0.8M + 1.6M = 10M

    valid, msg = FormalInvariantVerifier.verify_supply_conservation(
        initial_supply=initial_supply,
        circulating_balances=circulating,
        flow_pool=flow_pool,
        legal_escrow=legal_escrow,
        total_burned=total_burned
    )
    assert valid is True
    assert "Conservation holds" in msg


def test_formal_demurrage_and_rawlsian_floor():
    # Demurrage test
    valid_demurrage, _ = FormalInvariantVerifier.verify_demurrage_monotonicity(
        balance_0=2_000_000.0,
        balance_t=1_900_000.0,
        threshold=1_000_000.0,
        decay_rate=0.05,
        elapsed_seconds=2.1072  # theoretical ~1.9M
    )
    # Rawlsian floor test
    valid_rawlsian, msg = FormalInvariantVerifier.verify_rawlsian_maximin_monotonicity(
        initial_min_wealth=500.0,
        post_redistribution_min_wealth=1200.0
    )
    assert valid_rawlsian is True
    assert "floor preserved" in msg

    # Democratic parity test
    valid_weights, _ = FormalInvariantVerifier.verify_democratic_weight_invariant([1.0] * 100)
    assert valid_weights is True
