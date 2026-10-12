"""
Metrics for Socio-Economic Equality & Welfare Evaluation.
Mathematical implementations of Gini Coefficient, Atkinson Index,
Rawlsian Maximin, and Social Welfare Functions.
"""

from typing import Sequence, Union
import numpy as np


def calculate_gini(values: Union[Sequence[float], np.ndarray]) -> float:
    """
    Computes the exact Gini coefficient for a distribution of resources or income.
    
    Formula:
        G = (sum_{i=1}^n sum_{j=1}^n |x_i - x_j|) / (2 * n * sum_{i=1}^n x_i)
        
    Returns:
        float: Gini coefficient in range [0, 1].
               0.0 = Absolute equality (everyone has identical resources).
               1.0 = Absolute inequality (one person holds all resources).
    """
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return 0.0
    if np.any(arr < 0):
        raise ValueError("Values for Gini calculation must be non-negative.")
    
    total = np.sum(arr)
    if total == 0:
        return 0.0
    
    n = arr.shape[0]
    if n == 1:
        return 0.0
    
    # Efficient calculation using sorted values:
    sorted_arr = np.sort(arr)
    index = np.arange(1, n + 1)
    gini = (2.0 * np.sum(index * sorted_arr)) / (n * total) - (n + 1.0) / n
    return float(np.clip(gini, 0.0, 1.0))


def calculate_atkinson_index(
    values: Union[Sequence[float], np.ndarray],
    epsilon: float = 0.5
) -> float:
    """
    Calculates Atkinson Inequality Index for inequality aversion parameter epsilon.
    
    Formula:
        A_eps = 1 - (1 / mu) * [ (1/n) * sum(x_i^(1 - eps)) ]^(1 / (1 - eps))
        
    Args:
        values: Distribution array
        epsilon: Inequality aversion (epsilon > 0, epsilon != 1)
    """
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return 0.0
    
    # Guard against zero values when applying power:
    arr = np.maximum(arr, 1e-12)
    mu = np.mean(arr)
    if mu <= 0:
        return 0.0
    
    n = len(arr)
    if abs(epsilon - 1.0) < 1e-6:
        # Limit as epsilon -> 1 is geometric mean
        geom_mean = np.exp(np.mean(np.log(arr)))
        return float(np.clip(1.0 - (geom_mean / mu), 0.0, 1.0))
    else:
        power = 1.0 - epsilon
        mean_power = np.mean(arr ** power)
        y_e = mean_power ** (1.0 / power)
        return float(np.clip(1.0 - (y_e / mu), 0.0, 1.0))


def calculate_rawlsian_min(values: Union[Sequence[float], np.ndarray]) -> float:
    """
    Rawlsian Maximin metric: Returns the minimum utility/resource held by any agent.
    A social state S_1 is preferred over S_2 if min(S_1) > min(S_2).
    """
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return 0.0
    return float(np.min(arr))


def calculate_sen_social_welfare(values: Union[Sequence[float], np.ndarray]) -> float:
    """
    Sen's Social Welfare Function:
        W = mu * (1 - Gini)
        
    Combines mean prosperity with egalitarian distribution.
    """
    arr = np.asarray(values, dtype=np.float64)
    if arr.size == 0:
        return 0.0
    mu = float(np.mean(arr))
    gini = calculate_gini(arr)
    return float(mu * (1.0 - gini))
