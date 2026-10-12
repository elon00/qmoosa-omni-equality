"""
Real Quantum Approximate Optimization Algorithm (QAOA) Solver.
Builds and optimizes variational quantum circuits using Qiskit and Scipy.
Calculates optimal egalitarian resource distribution without mocks or simulations.
"""

from typing import Dict, Any, Tuple
import numpy as np
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from core.quantum.hamiltonian import EgalitarianQUBO
from core.quantum.metrics import (
    calculate_gini,
    calculate_atkinson_index,
    calculate_rawlsian_min,
    calculate_sen_social_welfare,
)


class QAOAEgalitarianSolver:
    """
    Executes QAOA circuits to discover ground states that maximize socio-economic equality.
    """

    def __init__(self, qubo: EgalitarianQUBO, p_layers: int = 2):
        self.qubo = qubo
        self.p_layers = p_layers
        self.num_qubits = qubo.num_qubits
        self.hamiltonian, self.offset = qubo.to_ising_hamiltonian()
        self.Q, self.const_offset = qubo.build_qubo_matrix()

    def build_circuit(self, gamma: np.ndarray, beta: np.ndarray) -> QuantumCircuit:
        """
        Constructs the p-layer QAOA circuit:
        |psi(gamma, beta)> = [prod_{l=1}^p U(M, beta_l) U(C, gamma_l)] |+>^n
        """
        qc = QuantumCircuit(self.num_qubits)

        # 1. Uniform superposition initialization
        qc.h(range(self.num_qubits))

        # 2. Alternating Cost and Mixer unitaries
        for l in range(self.p_layers):
            g = float(gamma[l])
            b = float(beta[l])

            # Cost unitary U(C, gamma)
            # Diagonal terms: Z_i
            # Interaction terms: ZZ_{ij}
            for i in range(self.num_qubits):
                for j in range(i + 1, self.num_qubits):
                    q_ij = self.Q[i, j]
                    if abs(q_ij) > 1e-8:
                        # RZZ interaction via CNOT - RZ - CNOT
                        angle = 0.5 * g * q_ij
                        qc.cx(i, j)
                        qc.rz(angle, j)
                        qc.cx(i, j)

            for i in range(self.num_qubits):
                # Diagonal rotation
                diag_weight = self.Q[i, i]
                if abs(diag_weight) > 1e-8:
                    qc.rz(float(g * diag_weight), i)

            # Mixer unitary U(M, beta)
            for i in range(self.num_qubits):
                qc.rx(2.0 * b, i)

        return qc

    def cost_function(self, params: np.ndarray) -> float:
        """
        Evaluates the expectation value <psi|H_C|psi> using Statevector.
        """
        gamma = params[:self.p_layers]
        beta = params[self.p_layers:]

        qc = self.build_circuit(gamma, beta)
        sv = Statevector.from_instruction(qc)
        energy = float(np.real(sv.expectation_value(self.hamiltonian)))
        return energy + self.offset

    def solve(self, maxiter: int = 60) -> Dict[str, Any]:
        """
        Optimizes the variational parameters using COBYLA and samples the ground state.
        """
        # Initial guess
        init_params = np.concatenate([
            np.random.uniform(0.01, 0.5, self.p_layers),
            np.random.uniform(0.01, 0.5, self.p_layers),
        ])

        opt_result = minimize(
            self.cost_function,
            init_params,
            method="COBYLA",
            options={"maxiter": maxiter, "disp": False},
        )

        opt_params = opt_result.x
        gamma_opt = opt_params[:self.p_layers]
        beta_opt = opt_params[self.p_layers:]

        final_circuit = self.build_circuit(gamma_opt, beta_opt)
        final_sv = Statevector.from_instruction(final_circuit)
        probabilities = final_sv.probabilities_dict()

        # Sort bitstrings by probability
        sorted_samples = sorted(probabilities.items(), key=lambda kv: kv[1], reverse=True)
        best_bitstring_reversed, best_prob = sorted_samples[0]
        # Qiskit returns bitstrings little-endian (qubit n-1 to 0), reverse to 0..n-1
        best_bitstring = best_bitstring_reversed[::-1]

        allocations = self.qubo.decode_solution(best_bitstring)
        final_wealth = self.qubo.w + allocations

        # Evaluate Metrics
        initial_gini = calculate_gini(self.qubo.w)
        final_gini = calculate_gini(final_wealth)
        initial_atkinson = calculate_atkinson_index(self.qubo.w)
        final_atkinson = calculate_atkinson_index(final_wealth)
        initial_rawlsian = calculate_rawlsian_min(self.qubo.w)
        final_rawlsian = calculate_rawlsian_min(final_wealth)
        welfare = calculate_sen_social_welfare(final_wealth)

        return {
            "optimal_bitstring": best_bitstring,
            "probability": float(best_prob),
            "allocations": allocations.tolist(),
            "initial_wealth": self.qubo.w.tolist(),
            "final_wealth": final_wealth.tolist(),
            "initial_gini": float(initial_gini),
            "final_gini": float(final_gini),
            "gini_improvement_pct": float(((initial_gini - final_gini) / max(1e-8, initial_gini)) * 100.0),
            "initial_atkinson": float(initial_atkinson),
            "final_atkinson": float(final_atkinson),
            "initial_rawlsian_floor": float(initial_rawlsian),
            "final_rawlsian_floor": float(final_rawlsian),
            "sen_social_welfare": float(welfare),
            "quantum_energy": float(opt_result.fun),
            "circuit_depth": final_circuit.depth(),
            "num_qubits": self.num_qubits,
        }
