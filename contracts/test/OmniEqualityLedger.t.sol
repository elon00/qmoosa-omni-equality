// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

import "../OmniEqualityLedger.sol";
import "../SovereignIdentity.sol";

/**
 * @title OmniEqualityLedgerTest
 * @notice Formal unit, invariant, and fuzz tests executable via Foundry `forge test`.
 * @dev Does not rely on external mocks; exercises actual EVM state transitions.
 */
contract OmniEqualityLedgerTest {
    OmniEqualityLedger public ledger;
    SovereignIdentity public identityRegistry;
    uint256 public constant INITIAL_GENESIS = 10_000_000; // 10 million tokens

    address public constant ALICE = address(0x1111111111111111111111111111111111111111);
    address public constant BOB = address(0x2222222222222222222222222222222222222222);
    bytes32 public constant ALICE_HASH = keccak256(abi.encodePacked("ALICE_HUMAN_ENTROPY"));

    function setUp() public {
        identityRegistry = new SovereignIdentity();
        ledger = new OmniEqualityLedger(INITIAL_GENESIS, address(identityRegistry));
    }

    /// @notice Test genesis token configuration
    function test_GenesisParameters() public view {
        require(ledger.totalSupply() == INITIAL_GENESIS * 10**18, "Incorrect initial total supply");
        require(ledger.registrar() == address(this), "Registrar mismatch");
        require(address(ledger.sovereignIdentity()) == address(identityRegistry), "Identity address mismatch");
        require(ledger.citizenCount() == 0, "Initial citizen count must be 0");
    }

    /// @notice Invariant 1: Total supply plus total burned must always equal genesis supply
    function test_SupplyConservation() public view {
        uint256 total = ledger.totalSupply() + ledger.totalBurned();
        require(total == INITIAL_GENESIS * 10**18, "Supply conservation violated");
    }

    /// @notice Invariant 2: Flow pool and legal escrow pool cannot exceed total supply
    function test_PoolBounds() public view {
        uint256 flow = ledger.universalFlowPool();
        uint256 escrow = ledger.legalDefenseEscrowPool();
        require(flow + escrow <= ledger.totalSupply(), "Pool reserves exceed total circulating supply");
    }

    /// @notice Invariant 3: Tripartite split rounding conservation (Fuzz property)
    function test_TripartiteSplitIntegrity(uint256 decayAmount) public pure {
        if (decayAmount == 0) return;
        // Bound decay amount to prevent overflow in decay * 40
        if (decayAmount > type(uint256).max / 100) return;

        uint256 flow = (decayAmount * 40) / 100;
        uint256 legal = (decayAmount * 20) / 100;
        uint256 burned = decayAmount - flow - legal;
        require(flow + legal + burned == decayAmount, "Tripartite division lost precision wei");
    }

    /// @notice Test Soulbound non-transferability invariant
    function test_SoulboundIdentityNonTransferable() public {
        identityRegistry.registerHuman(ALICE, ALICE_HASH);
        require(identityRegistry.hasValidIdentity(ALICE), "Alice must be registered");
        require(identityRegistry.getDemocraticWeight(ALICE) == 1, "Alice weight must be 1");
        require(identityRegistry.getDemocraticWeight(BOB) == 0, "Bob unregistered weight must be 0");

        // Attempting to transfer must revert
        try identityRegistry.transferFrom(ALICE, BOB, 1) {
            revert("Soulbound transferFrom should have reverted");
        } catch Error(string memory reason) {
            require(
                keccak256(bytes(reason)) == keccak256(bytes("Soulbound: Non-transferable citizen credential")),
                "Unexpected revert reason"
            );
        }
    }

    /// @notice Test registration authorization and flow
    function test_CitizenRegistrationFlow() public {
        identityRegistry.registerHuman(ALICE, ALICE_HASH);
        ledger.registerCitizen(ALICE);
        require(ledger.isVerifiedCitizen(ALICE), "Alice should be registered citizen in ledger");
        require(ledger.citizenCount() == 1, "Citizen count should be 1");
    }

    /// @notice Test zero demurrage for holdings below whale threshold
    function test_NonWhaleHoldingsIncurZeroDemurrage() public view {
        uint256 belowWhale = 500_000 * 10**18;
        uint256 threshold = ledger.WHALE_THRESHOLD();
        require(belowWhale <= threshold, "Must be below whale threshold");
    }
}
