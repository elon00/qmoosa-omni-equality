"""
Algorithmic Demurrage & Egalitarian Universal Flow Engine.
Implements continuous anti-hoarding capital decay on whale balances
and redistributes accumulated demurrage dividends equally to all verified citizens.
"""

import math
import time
from typing import Dict, List, Tuple, Any
from core.quantum.metrics import calculate_gini


class EgalitarianDemurragePool:
    """
    Simulates and executes mathematically precise capital circulation.
    Prevents oligarchical wealth concentration by enforcing continuous decay on idle balances.
    """

    def __init__(
        self,
        holding_threshold: float = 1_000_000.0,
        annual_decay_rate: float = 0.05,  # 5% annual demurrage above threshold
        redistribution_ratio: float = 0.50, # 50% redistributed, 50% burned
    ):
        self.holding_threshold = holding_threshold
        self.annual_decay_rate = annual_decay_rate
        # Continuous decay constant lambda = ln(1 + r) / seconds_in_year
        self.seconds_in_year = 365.25 * 86400.0
        self.decay_lambda = math.log(1.0 + annual_decay_rate) / self.seconds_in_year
        self.redistribution_ratio = redistribution_ratio

        self.balances: Dict[str, float] = {}
        self.last_update: Dict[str, float] = {}
        self.verified_citizens: set = set()
        self.accumulated_pool: float = 0.0
        self.total_burned: float = 0.0

    def register_citizen(self, citizen_id: str, initial_balance: float = 0.0, timestamp: float = None):
        self.verified_citizens.add(citizen_id)
        self.balances[citizen_id] = initial_balance
        self.last_update[citizen_id] = timestamp if timestamp is not None else time.time()

    def set_balance(self, entity_id: str, balance: float, timestamp: float = None):
        self.balances[entity_id] = balance
        self.last_update[entity_id] = timestamp if timestamp is not None else time.time()

    def compute_decay(self, entity_id: str, current_time: float = None) -> Tuple[float, float]:
        """
        Calculates accrued decay for an entity since last update.
        Returns:
            (decay_amount, new_balance)
        """
        now = current_time or time.time()
        bal = self.balances.get(entity_id, 0.0)
        last_t = self.last_update.get(entity_id, now)
        elapsed = max(0.0, now - last_t)

        if bal <= self.holding_threshold or elapsed == 0:
            return 0.0, bal

        excess = bal - self.holding_threshold
        # Exponential continuous decay on excess:
        decay_factor = math.exp(-self.decay_lambda * elapsed)
        new_excess = excess * decay_factor
        decay_amount = excess - new_excess

        new_bal = self.holding_threshold + new_excess
        return decay_amount, new_bal

    def apply_decay_and_redistribute(self, current_time: float = None) -> Dict[str, Any]:
        """
        Executes decay across all accounts, pools the proceeds,
        burns the deflationary portion, and evenly disburses equal dividends.
        """
        now = current_time or time.time()
        total_decay_collected = 0.0

        for entity_id in list(self.balances.keys()):
            decay_amt, new_bal = self.compute_decay(entity_id, now)
            if decay_amt > 0:
                self.balances[entity_id] = new_bal
                self.last_update[entity_id] = now
                total_decay_collected += decay_amt

        burned = total_decay_collected * (1.0 - self.redistribution_ratio)
        recycled = total_decay_collected * self.redistribution_ratio
        self.total_burned += burned

        dividend_per_citizen = 0.0
        n_citizens = len(self.verified_citizens)
        if n_citizens > 0 and recycled > 0:
            dividend_per_citizen = recycled / n_citizens
            for c_id in self.verified_citizens:
                self.balances[c_id] = self.balances.get(c_id, 0.0) + dividend_per_citizen
                self.last_update[c_id] = now

        current_gini = calculate_gini(list(self.balances.values())) if self.balances else 0.0

        return {
            "timestamp": now,
            "total_decay_collected": float(total_decay_collected),
            "burned": float(burned),
            "recycled_pool": float(recycled),
            "num_verified_citizens": n_citizens,
            "dividend_per_citizen": float(dividend_per_citizen),
            "total_burned_cumulative": float(self.total_burned),
            "resulting_gini": float(current_gini),
        }
