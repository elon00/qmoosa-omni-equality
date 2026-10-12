// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

/**
 * @title SovereignIdentity
 * @notice Soulbound Token (SBT) guaranteeing exactly 1 human = 1 vote.
 * @dev Non-transferable credential enforcing invariant legal weight = 1.0.
 */
contract SovereignIdentity {
    string public name = "Sovereign Human Identity";
    string public symbol = "SOV-ID";

    struct IdentityRecord {
        bytes32 humanHash;
        uint256 registeredTimestamp;
        bool exists;
    }

    mapping(address => IdentityRecord) public citizens;
    mapping(bytes32 => address) public hashToAddress;
    uint256 public totalCitizens;

    address public immutable registrar;

    event CitizenRegistered(address indexed wallet, bytes32 indexed humanHash);

    modifier onlyRegistrar() {
        require(msg.sender == registrar, "Only registrar");
        _;
    }

    constructor() {
        registrar = msg.sender;
    }

    function registerHuman(address wallet, bytes32 humanHash) external onlyRegistrar {
        require(wallet != address(0), "Zero address");
        require(!citizens[wallet].exists, "Wallet already registered");
        require(hashToAddress[humanHash] == address(0), "Identity entropy already mapped (Sybil prevented)");

        citizens[wallet] = IdentityRecord({
            humanHash: humanHash,
            registeredTimestamp: block.timestamp,
            exists: true
        });
        hashToAddress[humanHash] = wallet;
        totalCitizens++;

        emit CitizenRegistered(wallet, humanHash);
    }

    // Invariant: Non-transferable (Soulbound)
    function transferFrom(address, address, uint256) external pure {
        revert("Soulbound: Non-transferable citizen credential");
    }

    function safeTransferFrom(address, address, uint256) external pure {
        revert("Soulbound: Non-transferable citizen credential");
    }

    function hasValidIdentity(address wallet) external view returns (bool) {
        return citizens[wallet].exists;
    }

    function getDemocraticWeight(address wallet) external view returns (uint256) {
        // Always returns 1 for verified citizens, 0 for non-citizens.
        return citizens[wallet].exists ? 1 : 0;
    }
}
