// SPDX-License-Identifier: Apache-2.0
pragma solidity ^0.8.20;

/**
 * @title OmniEqualityLedger
 * @notice Egalitarian Token with Algorithmic Demurrage & Universal Dividend Redistribution.
 * @dev Enforces wealth-concentration limits, continuous idle decay, and equal flow to registered citizens.
 */
interface ISovereignIdentity {
    function hasValidIdentity(address wallet) external view returns (bool);
}

contract OmniEqualityLedger {
    string public name = "Omni Equality Token";
    string public symbol = "OEQ";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    ISovereignIdentity public immutable sovereignIdentity;
    address public immutable registrar;

    // Holding threshold above which balances incur demurrage (e.g. 1,000,000 tokens)
    uint256 public constant WHALE_THRESHOLD = 1_000_000 * 10**18;
    // 5% annual decay rate represented in basis points (500 bp per year)
    uint256 public constant ANNUAL_DECAY_BPS = 500;
    uint256 public constant SECONDS_PER_YEAR = 365 days;

    mapping(address => uint256) private _balances;
    mapping(address => uint256) public lastDecayTimestamp;
    mapping(address => mapping(address => uint256)) public allowance;

    // Registered Soulbound verified human citizens
    mapping(address => bool) public isVerifiedCitizen;
    address[] public citizenList;

    // Pools
    uint256 public universalFlowPool;
    uint256 public legalDefenseEscrowPool;
    uint256 public totalBurned;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event CitizenRegistered(address indexed citizen);
    event DemurrageAssessed(address indexed whale, uint256 amountDecayed, uint256 poolShare, uint256 legalShare, uint256 burned);
    event DividendsDistributed(uint256 totalDisbursed, uint256 perCitizenAmount);

    constructor(uint256 initialGenesisSupply, address identityContract) {
        require(identityContract != address(0) && identityContract.code.length > 0, "Invalid identity registry");
        sovereignIdentity = ISovereignIdentity(identityContract);
        registrar = msg.sender;
        totalSupply = initialGenesisSupply * 10**18;
        _balances[msg.sender] = totalSupply;
        lastDecayTimestamp[msg.sender] = block.timestamp;
        emit Transfer(address(0), msg.sender, totalSupply);
    }

    function registerCitizen(address citizen) external {
        require(msg.sender == registrar, "Only authorized registrar");
        require(sovereignIdentity.hasValidIdentity(citizen), "Identity verification required");
        require(!isVerifiedCitizen[citizen], "Already registered");
        require(citizen != address(0), "Zero address");
        isVerifiedCitizen[citizen] = true;
        citizenList.push(citizen);
        if (lastDecayTimestamp[citizen] == 0) {
            lastDecayTimestamp[citizen] = block.timestamp;
        }
        emit CitizenRegistered(citizen);
    }

    function citizenCount() external view returns (uint256) {
        return citizenList.length;
    }

    function balanceOf(address account) public view returns (uint256) {
        uint256 rawBal = _balances[account];
        if (rawBal <= WHALE_THRESHOLD) {
            return rawBal;
        }
        uint256 timeElapsed = block.timestamp - lastDecayTimestamp[account];
        if (timeElapsed == 0) {
            return rawBal;
        }
        uint256 excess = rawBal - WHALE_THRESHOLD;
        uint256 decay = (excess * ANNUAL_DECAY_BPS * timeElapsed) / (10000 * SECONDS_PER_YEAR);
        if (decay > excess) decay = excess;
        return rawBal - decay;
    }

    function _settleDemurrage(address account) internal {
        uint256 rawBal = _balances[account];
        if (rawBal <= WHALE_THRESHOLD) {
            lastDecayTimestamp[account] = block.timestamp;
            return;
        }
        uint256 timeElapsed = block.timestamp - lastDecayTimestamp[account];
        if (timeElapsed == 0) return;

        uint256 excess = rawBal - WHALE_THRESHOLD;
        uint256 decay = (excess * ANNUAL_DECAY_BPS * timeElapsed) / (10000 * SECONDS_PER_YEAR);
        if (decay > excess) decay = excess;

        if (decay > 0) {
            _balances[account] = rawBal - decay;
            // 40% to Universal Flow Pool, 20% to Legal Defense Escrow, 40% Burned
            uint256 flowShare = (decay * 40) / 100;
            uint256 legalShare = (decay * 20) / 100;
            uint256 burnShare = decay - flowShare - legalShare;

            universalFlowPool += flowShare;
            legalDefenseEscrowPool += legalShare;
            totalBurned += burnShare;
            totalSupply -= burnShare;

            emit DemurrageAssessed(account, decay, flowShare, legalShare, burnShare);
            emit Transfer(account, address(0), burnShare);
        }
        lastDecayTimestamp[account] = block.timestamp;
    }

    function distributeDemurrageDividends() external {
        uint256 nCitizens = citizenList.length;
        require(nCitizens > 0, "No registered citizens");
        require(universalFlowPool > 0, "No pool accumulated");

        uint256 perCitizen = universalFlowPool / nCitizens;
        require(perCitizen > 0, "Dividend too small");

        uint256 totalDisbursed = perCitizen * nCitizens;
        universalFlowPool -= totalDisbursed;

        for (uint256 i = 0; i < nCitizens; i++) {
            address c = citizenList[i];
            _balances[c] += perCitizen;
            emit Transfer(address(this), c, perCitizen);
        }

        emit DividendsDistributed(totalDisbursed, perCitizen);
    }

    function transfer(address recipient, uint256 amount) external returns (bool) {
        _settleDemurrage(msg.sender);
        _settleDemurrage(recipient);
        require(_balances[msg.sender] >= amount, "Insufficient balance");

        _balances[msg.sender] -= amount;
        _balances[recipient] += amount;
        emit Transfer(msg.sender, recipient, amount);
        return true;
    }

    function approve(address spender, uint256 amount) external returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool) {
        require(allowance[sender][msg.sender] >= amount, "Allowance exceeded");
        allowance[sender][msg.sender] -= amount;

        _settleDemurrage(sender);
        _settleDemurrage(recipient);
        require(_balances[sender] >= amount, "Insufficient balance");

        _balances[sender] -= amount;
        _balances[recipient] += amount;
        emit Transfer(sender, recipient, amount);
        return true;
    }
}
