"""
Hamiltonian & QUBO formulation for Egalitarian Resource Allocation.
Converts social inequality minimization and budget preservation constraints
into an Ising Spin Hamiltonian mapped to Pauli-Z operators for QAOA / VQE.
"""

from typing import Dict, List, Tuple
import numpy as np
from qiskit.quantum_info import SparsePauliOp


class EgalitarianQUBO:
    """
    Constructs a Quadratic Unconstrained Binary Optimization (QUBO) problem
    to distribute resources among N agents to achieve maximum socio-economic equality.
    """

    def __init__(
        self,
        initial_endowments: List[float],
        total_budget: int,
        bits_per_agent: int = 1,
        lambda_inequality: float = 1.0,
        lambda_budget: float = 2.0,
        lambda_poverty_floor: float = 1.5,
        poverty_floor: float = 1.0,
    ):
        """
        Args:
            initial_endowments: Initial resources/wealth of each agent (w_i).
            total_budget: Total resources available for redistribution (B).
            bits_per_agent: Number of binary qubits used to encode allocation per agent.
            lambda_inequality: Weight on pairwise disparity minimization.
            lambda_budget: Penalty weight for violating total budget constraint.
            lambda_poverty_floor: Penalty weight for agents ending up below poverty floor.
            poverty_floor: Minimum acceptable resource floor.
        """
        self.w = np.array(initial_endowments, dtype=np.float64)
        self.n_agents = len(self.w)
        self.total_budget = total_budget
        self.bits_per_agent = bits_per_agent
        self.num_qubits = self.n_agents * self.bits_per_agent
        self.lambda_ineq = lambda_inequality
        self.lambda_budget = lambda_budget
        self.lambda_floor = lambda_poverty_floor
        self.poverty_floor = poverty_floor

    def _get_agent_and_bit(self, qubit_idx: int) -> Tuple[int, int]:
        agent_idx = qubit_idx // self.bits_per_agent
        bit_idx = qubit_idx % self.bits_per_agent
        return agent_idx, bit_idx

    def _bit_weight(self, bit_idx: int) -> float:
        return float(2 ** bit_idx)

    def build_qubo_matrix(self) -> Tuple[np.ndarray, float]:
        """
        Constructs the upper-triangular QUBO matrix Q such that Cost(z) = z^T Q z + c.
        Returns:
            Q (np.ndarray): Shape (num_qubits, num_qubits)
            constant_offset (float): Scalar constant offset
        """
        Q = np.zeros((self.num_qubits, self.num_qubits), dtype=np.float64)
        constant = 0.0

        # 1. Budget Constraint: lambda_budget * (sum_i x_i - B)^2
        # sum_i x_i = sum_k c_k z_k
        c_vec = np.zeros(self.num_qubits)
        for k in range(self.num_qubits):
            _, bit_idx = self._get_agent_and_bit(k)
            c_vec[k] = self._bit_weight(bit_idx)

        # Expanding lambda_budget * (c^T z - B)^2:
        # = lambda_budget * ( z^T (c c^T) z - 2B (c^T z) + B^2 )
        constant += self.lambda_budget * (self.total_budget ** 2)
        for k in range(self.num_qubits):
            # Diagonal term includes linear term since z_k^2 = z_k
            Q[k, k] += self.lambda_budget * (c_vec[k] ** 2 - 2.0 * self.total_budget * c_vec[k])
            for l in range(k + 1, self.num_qubits):
                Q[k, l] += self.lambda_budget * 2.0 * c_vec[k] * c_vec[l]

        # 2. Inequality Minimization Constraint:
        # Minimize pairwise disparity: lambda_ineq * sum_{i < j} ((w_i + x_i) - (w_j + x_j))^2
        for i in range(self.n_agents):
            for j in range(i + 1, self.n_agents):
                delta_w = self.w[i] - self.w[j]
                constant += self.lambda_ineq * (delta_w ** 2)

                # Qubit sets for agent i and agent j
                q_i = [i * self.bits_per_agent + b for b in range(self.bits_per_agent)]
                q_j = [j * self.bits_per_agent + b for b in range(self.bits_per_agent)]

                # Linear contribution: 2 * delta_w * (x_i - x_j)
                for k in q_i:
                    _, b = self._get_agent_and_bit(k)
                    val = self._bit_weight(b)
                    Q[k, k] += self.lambda_ineq * (val ** 2 + 2.0 * delta_w * val)
                for l in q_j:
                    _, b = self._get_agent_and_bit(l)
                    val = self._bit_weight(b)
                    Q[l, l] += self.lambda_ineq * (val ** 2 - 2.0 * delta_w * val)

                # Pairwise interactions within x_i:
                for idx_a, k1 in enumerate(q_i):
                    for k2 in q_i[idx_a + 1:]:
                        _, b1 = self._get_agent_and_bit(k1)
                        _, b2 = self._get_agent_and_bit(k2)
                        Q[k1, k2] += self.lambda_ineq * 2.0 * self._bit_weight(b1) * self._bit_weight(b2)

                # Pairwise interactions within x_j:
                for idx_a, l1 in enumerate(q_j):
                    for l2 in q_j[idx_a + 1:]:
                        _, b1 = self._get_agent_and_bit(l1)
                        _, b2 = self._get_agent_and_bit(l2)
                        Q[l1, l2] += self.lambda_ineq * 2.0 * self._bit_weight(b1) * self._bit_weight(b2)

                # Cross interactions: -2 * x_i * x_j
                for k in q_i:
                    for l in q_j:
                        _, b_i = self._get_agent_and_bit(k)
                        _, b_j = self._get_agent_and_bit(l)
                        val = -2.0 * self.lambda_ineq * self._bit_weight(b_i) * self._bit_weight(b_j)
                        if k < l:
                            Q[k, l] += val
                        else:
                            Q[l, k] += val

        return Q, constant

    def to_ising_hamiltonian(self) -> Tuple[SparsePauliOp, float]:
        """
        Converts the QUBO problem into an Ising Spin Hamiltonian:
        Using z_k = (I - sigma_k^z) / 2
        
        Returns:
            SparsePauliOp: Real Qiskit Hamiltonian operator
            float: Energy offset
        """
        Q, constant = self.build_qubo_matrix()
        n = self.num_qubits

        offset = constant
        h_linear = np.zeros(n)
        J_couplings = np.zeros((n, n))

        # Translate z_k -> (1 - Z_k)/2
        for i in range(n):
            # Diagonal Q[i, i] * z_i = Q[i, i] * (1 - Z_i)/2
            offset += 0.5 * Q[i, i]
            h_linear[i] -= 0.5 * Q[i, i]

            for j in range(i + 1, n):
                q_ij = Q[i, j]
                # Q[i, j] * z_i * z_j = Q[i, j] * (1 - Z_i)/2 * (1 - Z_j)/2
                # = Q[i, j] * (1 - Z_i - Z_j + Z_i Z_j) / 4
                offset += 0.25 * q_ij
                h_linear[i] -= 0.25 * q_ij
                h_linear[j] -= 0.25 * q_ij
                J_couplings[i, j] += 0.25 * q_ij

        # Construct Pauli strings for Qiskit
        pauli_list = []

        # Single qubit Z terms
        for i in range(n):
            if abs(h_linear[i]) > 1e-10:
                p_chars = ['I'] * n
                p_chars[i] = 'Z'
                pauli_str = "".join(reversed(p_chars))  # Qiskit little-endian
                pauli_list.append((pauli_str, float(h_linear[i])))

        # Two-qubit ZZ coupling terms
        for i in range(n):
            for j in range(i + 1, n):
                if abs(J_couplings[i, j]) > 1e-10:
                    p_chars = ['I'] * n
                    p_chars[i] = 'Z'
                    p_chars[j] = 'Z'
                    pauli_str = "".join(reversed(p_chars))
                    pauli_list.append((pauli_str, float(J_couplings[i, j])))

        if not pauli_list:
            pauli_list.append(('I' * n, 0.0))

        operator = SparsePauliOp.from_list(pauli_list)
        return operator, float(offset)

    def decode_solution(self, bitstring: str) -> np.ndarray:
        """
        Decodes a binary solution bitstring into final allocated resources per agent.
        bitstring is formatted in qubit index order 0..N-1.
        """
        bits = [int(b) for b in bitstring]
        allocations = np.zeros(self.n_agents, dtype=np.float64)
        for k, bit in enumerate(bits):
            if bit == 1:
                agent_idx, bit_idx = self._get_agent_and_bit(k)
                allocations[agent_idx] += self._bit_weight(bit_idx)
        return allocations
