"""
Formal Accounting & Invariant Specification Engine.
Defines machine-verifiable propositions for economic conservation,
demurrage decay bounds, Rawlsian maximin floors, and democratic parity.
"""

from typing import Dict, Any, List, Tuple
import math


class FormalInvariantVerifier:
    """
    Formal logic verifier for core protocol invariants.
    Each theorem tests mathematical bounds and conservation equations.
    """

    @staticmethod
    def verify_supply_conservation(
        initial_supply: float,
        circulating_balances: List[float],
        flow_pool: float,
        legal_escrow: float,
        total_burned: float,
        epsilon: float = 1e-6
    ) -> Tuple[bool, str]:
        """
        Theorem 1 (Conservation of Monetary Value):
        Initial_Supply == Sum(Circulating_Balances) + Flow_Pool + Legal_Escrow + Total_Burned
        """
        current_sum = sum(circulating_balances) + flow_pool + legal_escrow + total_burned
        diff = abs(initial_supply - current_sum)
        if diff <= epsilon:
            return True, f"Conservation holds: diff={diff:.8f} <= {epsilon}"
        return False, f"Conservation VIOLATED: expected {initial_supply}, got {current_sum} (diff={diff})"

    @staticmethod
    def verify_demurrage_monotonicity(
        balance_0: float,
        balance_t: float,
        threshold: float,
        decay_rate: float,
        elapsed_seconds: float,
        epsilon: float = 1e-4
    ) -> Tuple[bool, str]:
        """
        Theorem 2 (Monotonic Exponential Decay to Sovereign Threshold):
        For B_0 > Theta, B(t) = Theta + (B_0 - Theta) * exp(-lambda * t).
        Requires B(t) strictly in [Theta, B_0] and B(t) <= B_0.
        """
        if balance_0 <= threshold:
            # Below threshold, zero decay
            if abs(balance_t - balance_0) <= epsilon:
                return True, "Sub-threshold invariant holds: no decay applied."
            return False, "Sub-threshold violation: balance decayed below threshold without cause."

        theoretical_bt = threshold + (balance_0 - threshold) * math.exp(-decay_rate * elapsed_seconds)
        diff = abs(balance_t - theoretical_bt)
        if diff <= epsilon and balance_t >= threshold and balance_t <= balance_0:
            return True, f"Demurrage decay bounds hold: theoretical={theoretical_bt:.4f}, actual={balance_t:.4f}"
        return False, f"Demurrage bounds VIOLATED: theoretical={theoretical_bt}, actual={balance_t}"

    @staticmethod
    def verify_rawlsian_maximin_monotonicity(
        initial_min_wealth: float,
        post_redistribution_min_wealth: float
    ) -> Tuple[bool, str]:
        """
        Theorem 3 (Rawlsian Maximin Floor Preservation):
        min_i(X_post) >= min_i(X_pre)
        The economic standing of the least advantaged human must never degrade under redistribution.
        """
        if post_redistribution_min_wealth >= initial_min_wealth:
            return True, f"Rawlsian floor preserved: {initial_min_wealth:.2f} -> {post_redistribution_min_wealth:.2f}"
        return False, f"Rawlsian floor VIOLATED: poorest citizen degraded from {initial_min_wealth} to {post_redistribution_min_wealth}"

    @staticmethod
    def verify_democratic_weight_invariant(
        citizen_weights: List[float]
    ) -> Tuple[bool, str]:
        """
        Theorem 4 (Strict Egalitarian Parity):
        For all citizens i, weight_i == 1.0. No variance permitted.
        """
        for idx, w in enumerate(citizen_weights):
            if abs(w - 1.0) > 1e-9:
                return False, f"Democratic invariant VIOLATED: Citizen {idx} has weight {w} != 1.0"
        return True, f"Democratic parity verified: all {len(citizen_weights)} citizens have identical weight 1.0"
