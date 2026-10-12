"""
Comprehensive Test Suite for Quantum Hamiltonian & QAOA Optimization.
Verifies real mathematical calculations with zero mock or simulation.
"""

import pytest
import numpy as np
from core.quantum.metrics import (
    calculate_gini,
    calculate_atkinson_index,
    calculate_rawlsian_min,
    calculate_sen_social_welfare,
)
from core.quantum.hamiltonian import EgalitarianQUBO
from core.quantum.qaoa_solver import QAOAEgalitarianSolver


def test_gini_boundary_cases():
    # Perfectly equal distribution -> Gini = 0.0
    equal_dist = [10.0, 10.0, 10.0, 10.0]
    assert calculate_gini(equal_dist) == pytest.approx(0.0, abs=1e-6)

    # Empty / zero -> Gini = 0.0
    assert calculate_gini([]) == 0.0
    assert calculate_gini([0.0, 0.0]) == 0.0

    # Highly unequal distribution -> Gini near 1.0
    unequal_dist = [0.0, 0.0, 0.0, 1000.0]
    gini_unequal = calculate_gini(unequal_dist)
    assert gini_unequal > 0.70


def test_atkinson_and_rawlsian():
    dist = [2.0, 5.0, 15.0]
    assert calculate_rawlsian_min(dist) == 2.0

    atk = calculate_atkinson_index(dist, epsilon=0.5)
    assert 0.0 <= atk <= 1.0

    welfare = calculate_sen_social_welfare(dist)
    assert welfare > 0.0


def test_qubo_matrix_construction():
    endowments = [1.0, 4.0, 10.0]
    qubo = EgalitarianQUBO(endowments, total_budget=6, bits_per_agent=1)
    Q, offset = qubo.build_qubo_matrix()

    assert Q.shape == (3, 3)
    assert offset > 0.0

    # Convert to Ising
    hamiltonian, h_offset = qubo.to_ising_hamiltonian()
    assert hamiltonian.num_qubits == 3
    assert len(hamiltonian) > 0


def test_qaoa_solver_execution():
    # 3 agents with significant inequality:
    # Agent 0: 1 unit, Agent 1: 3 units, Agent 2: 12 units
    endowments = [1.0, 3.0, 12.0]
    qubo = EgalitarianQUBO(
        initial_endowments=endowments,
        total_budget=8,
        bits_per_agent=1,
        lambda_inequality=2.0,
        lambda_budget=3.0,
    )
    solver = QAOAEgalitarianSolver(qubo, p_layers=1)
    res = solver.solve(maxiter=20)

    assert "optimal_bitstring" in res
    assert len(res["optimal_bitstring"]) == 3
    assert res["initial_gini"] > 0.40
    # The optimal allocation must improve or maintain social distribution:
    assert res["final_rawlsian_floor"] >= res["initial_rawlsian_floor"]
    assert res["num_qubits"] == 3
