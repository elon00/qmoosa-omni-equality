"""
Tests for Dynamic Macroeconomic Adaptability and Democratic Emergency Governance.
"""

import pytest
from core.tokenomics.dynamic_governance import (
    DynamicAdaptabilityEngine,
    MacroeconomicRegime,
)


def test_initial_regime_and_active_parameters():
    engine = DynamicAdaptabilityEngine(initial_regime=MacroeconomicRegime.EQUILIBRIUM)
    params = engine.get_active_parameters()

    assert params["active_regime"] == "EQUILIBRIUM"
    assert params["holding_threshold"] == 1_000_000.0
    assert params["flow_share_pct"] == 0.40
    assert params["legal_share_pct"] == 0.20
    assert params["burn_share_pct"] == 0.40


def test_democratic_transition_to_recession_shock():
    engine = DynamicAdaptabilityEngine()
    prop = engine.propose_regime_shift(
        proposal_id="PROP-RECESSION-01",
        target_regime=MacroeconomicRegime.RECESSION_SHOCK,
        justification="Global liquidity contraction requires increased citizen stimulus",
        proposer_citizen_id="0xcitizen_alpha"
    )
    assert prop["id"] == "PROP-RECESSION-01"
    assert prop["status"] == "OPEN"

    # 4 approvals, 1 rejection (80% approval >= 60% supermajority)
    for i in range(4):
        engine.vote_on_shift("PROP-RECESSION-01", f"citizen_{i}", 1)
    engine.vote_on_shift("PROP-RECESSION-01", "citizen_4", -1)

    executed = engine.execute_regime_shift("PROP-RECESSION-01", approval_threshold=0.60)
    assert executed is True
    assert engine.current_regime == MacroeconomicRegime.RECESSION_SHOCK

    # Check that parameters dynamically adjusted
    new_params = engine.get_active_parameters()
    assert new_params["holding_threshold"] == 500_000.0
    assert new_params["flow_share_pct"] == 0.60
    assert new_params["burn_share_pct"] == 0.20
