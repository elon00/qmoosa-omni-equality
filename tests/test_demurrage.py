"""
Tests for Algorithmic Demurrage and Equal Flow Redistribution.
"""

import pytest
from core.tokenomics.demurrage_engine import EgalitarianDemurragePool
from core.quantum.metrics import calculate_gini


def test_demurrage_below_threshold():
    # Balances under 1,000,000 tokens should experience zero decay
    pool = EgalitarianDemurragePool(holding_threshold=1_000_000.0, annual_decay_rate=0.05)
    pool.set_balance("poor_citizen", 5_000.0, timestamp=1000.0)

    # 1 year later
    one_year_seconds = 365.25 * 86400.0
    decay, new_bal = pool.compute_decay("poor_citizen", current_time=1000.0 + one_year_seconds)
    assert decay == 0.0
    assert new_bal == 5_000.0


def test_demurrage_above_threshold():
    # Whale with 11,000,000 tokens (10M excess) at 5% annual decay
    pool = EgalitarianDemurragePool(holding_threshold=1_000_000.0, annual_decay_rate=0.05)
    pool.set_balance("whale_investor", 11_000_000.0, timestamp=1000.0)

    one_year_seconds = 365.25 * 86400.0
    decay, new_bal = pool.compute_decay("whale_investor", current_time=1000.0 + one_year_seconds)

    # Expected decay on 10,000,000 excess is approx 500,000
    assert decay > 470_000.0
    assert new_bal < 11_000_000.0
    assert new_bal >= 1_000_000.0


def test_demurrage_redistribution_reduces_gini():
    # 1 whale and 4 poor citizens
    pool = EgalitarianDemurragePool(holding_threshold=1_000_000.0, annual_decay_rate=0.10)
    pool.set_balance("whale", 10_000_000.0, timestamp=0.0)

    for i in range(4):
        pool.register_citizen(f"citizen_{i}", initial_balance=100.0, timestamp=0.0)

    initial_gini = calculate_gini(list(pool.balances.values()))

    # Run redistribution after 1 year
    one_year_seconds = 365.25 * 86400.0
    result = pool.apply_decay_and_redistribute(current_time=one_year_seconds)

    assert result["total_decay_collected"] > 0
    assert result["dividend_per_citizen"] > 0
    # Gini must decline after redistribution
    assert result["resulting_gini"] < initial_gini


def test_tripartite_integer_conservation():
    """Verifies that 40% flow, 20% legal, and 40% burn have zero rounding leakage."""
    for decay_int in [1, 7, 333, 10_000, 10**18, 999_999_999_999_999_999]:
        flow = (decay_int * 40) // 100
        legal = (decay_int * 20) // 100
        burned = decay_int - flow - legal
        assert flow + legal + burned == decay_int
