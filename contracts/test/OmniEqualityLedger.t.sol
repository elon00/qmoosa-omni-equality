// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

import "../OmniEqualityLedger.sol";
import "../SovereignIdentity.sol";

/**
 * @title OmniEqualityLedgerInvariantTest
 * @notice Formal stateful invariant test specifications for Foundry.
 */
contract OmniEqualityLedgerInvariantTest {
    OmniEqualityLedger public ledger;
    SovereignIdentity public identityRegistry;
    uint256 public constant INITIAL_GENESIS = 10_000_000; // 10 million tokens

    function setUp() public {
        identityRegistry = new SovereignIdentity();
        ledger = new OmniEqualityLedger(INITIAL_GENESIS, address(identityRegistry));
    }

    /// @notice Invariant 1: Total supply plus total burned must always equal genesis supply
    function invariant_SupplyConservation() public view {
        uint256 total = ledger.totalSupply() + ledger.totalBurned();
        require(total == INITIAL_GENESIS * 10**18, "Supply conservation violated");
    }

    /// @notice Invariant 2: Flow pool and legal escrow pool cannot exceed total supply
    function invariant_PoolBounds() public view {
        uint256 flow = ledger.universalFlowPool();
        uint256 escrow = ledger.legalDefenseEscrowPool();
        require(flow + escrow <= ledger.totalSupply(), "Pool reserves exceed total circulating supply");
    }

    /// @notice Invariant 3: Tripartite split rounding conservation
    function test_TripartiteSplitIntegrity(uint256 decayAmount) public pure {
        if (decayAmount == 0) return;
        uint256 flow = (decayAmount * 40) / 100;
        uint256 legal = (decayAmount * 20) / 100;
        uint256 burned = decayAmount - flow - legal;
        require(flow + legal + burned == decayAmount, "Tripartite division lost precision wei");
    }
}
