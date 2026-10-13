# Governance Decision: Tripartite Demurrage Accounting Policy

**Resolution ID**: `OEQ-GOV-2026-001`  
**Status**: `RATIFIED & LOCKED`  
**Scope**: Smart Contract & Off-Chain Engine Reconciliation

---

## 1. Executive Summary
Prior drafts referenced an unrefined 50/50 model (50% burn, 50% flow pool). Following security and operational reviews, the **Tripartite Egalitarian Split** is formally locked across both on-chain smart contracts (`contracts/OmniEqualityLedger.sol`) and off-chain execution engines (`core/tokenomics/demurrage_engine.py`).

## 2. Allocation Ratios
For any assessed continuous demurrage decay $\Delta B$ on whale balances exceeding $\Theta = 1,000,000\text{ OEQ}$:

| Allocation Target | Percentage | Purpose |
| :--- | :--- | :--- |
| **Universal Flow Dividend Pool** | **40%** | Direct egalitarian stream disbursed equally to all verified Soulbound citizens. |
| **Legal Defense Escrow Pool** | **20%** | Dedicated community escrow subsidizing legal representation for non-institutional citizens facing litigation from predatory corporations. |
| **Deflationary Burn** | **40%** | Permanently burned from total supply, preventing token inflation. |

## 3. Mathematical Invariant
At all points in time:
$$\text{flowShare} + \text{legalShare} + \text{burnShare} \equiv \Delta B$$
$$\text{totalSupply} + \text{totalBurned} \equiv \text{initialGenesisSupply}$$

Zero tokens are leaked, withheld, or minted out of thin air.
