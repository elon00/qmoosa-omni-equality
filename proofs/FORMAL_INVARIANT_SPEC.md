# Qmoosa Omni-Equality Protocol (OEQ) — Formal Mathematical Invariant Specification

> **Normative Mathematical Model & Code-Traceability Matrix**

---

## 1. Axiomatic Theorems

### Theorem 1: Conservation of Economic Supply
$$\text{TotalSupply}_0 = \sum_{i=1}^N \text{Balance}_i(t) + \text{FlowPool}(t) + \text{LegalEscrow}(t) + \text{TotalBurned}(t)$$
* **Python Target:** `core.proofs.accounting_spec.FormalInvariantVerifier.verify_supply_conservation()`
* **Solidity Target:** `OmniEqualityLedger.sol` (Line 111-112: `totalBurned += burnShare; totalSupply -= burnShare;`)
* **Foundry Invariant:** `contracts/test/OmniEqualityLedger.t.sol::invariant_SupplyConservation()`

---

### Theorem 2: Demurrage Monotonicity & Asymptotic Sovereign Bound
$$\forall B_0 > \Theta, \quad B(t) = \Theta + (B_0 - \Theta) e^{-\lambda t}$$
$$\lim_{t \to \infty} B(t) = \Theta \quad \text{and} \quad \frac{dB}{dt} = -\lambda (B(t) - \Theta) \le 0$$
* **Python Target:** `core.proofs.accounting_spec.FormalInvariantVerifier.verify_demurrage_monotonicity()`
* **Solidity Target:** `OmniEqualityLedger.sol::balanceOf()` & `_settleDemurrage()`

---

### Theorem 3: Rawlsian Maximin Monotonic Floor
$$\min_{i \in \{1,\dots,N\}} X_i(t_{\text{post}}) \ge \min_{i \in \{1,\dots,N\}} X_i(t_{\text{pre}})$$
Under continuous demurrage flow redistribution, the absolute economic floor of the least-advantaged verified citizen is strictly non-decreasing.
* **Python Target:** `core.proofs.accounting_spec.FormalInvariantVerifier.verify_rawlsian_maximin_monotonicity()`

---

### Theorem 4: Strict Democratic Parity Invariant
$$\forall i \in \text{Citizens}, \quad w_i \equiv 1.0$$
No citizen may hold, purchase, stake, or accumulate $w_i > 1.0$.
* **Python Target:** `core.proofs.accounting_spec.FormalInvariantVerifier.verify_democratic_weight_invariant()`
* **Solidity Target:** `SovereignIdentity.sol::getDemocraticWeight()` returning constant 1.

---

### Theorem 5: Zero Rounding Leakage in Tripartite Division
$$\forall D \in \mathbb{N}, \quad \text{FlowShare} + \text{LegalShare} + \text{BurnShare} = D$$
$$\text{where} \quad \text{FlowShare} = \lfloor \frac{40 D}{100} \rfloor, \quad \text{LegalShare} = \lfloor \frac{20 D}{100} \rfloor, \quad \text{BurnShare} = D - \text{FlowShare} - \text{LegalShare}$$
* **Python Target:** `tests.test_demurrage::test_tripartite_integer_conservation()`
* **Solidity Target:** `OmniEqualityLedger.sol` (Lines 104-106)
