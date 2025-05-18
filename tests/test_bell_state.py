from typing import List

from cirq import Circuit, H, LineQubit, X, Z, density_matrix_from_state_vector
from numpy._typing import NDArray
from numpy.ma import allequal

from stim_experiments.utilities.utilities import partial_trace


class TestBellState:
    def test_single_qubit_qec_cannot_be_done_on_entangled_state(self):
        partial_traces = [partial_trace(rho, [qubit_index]) for rho in self._bell_states for qubit_index in range(2)]
        for index, rho in enumerate(partial_traces[:-1]):
            assert self._is_indistinguishable(rho, partial_traces[index + 1])

    @property
    def _bell_states(self) -> List[NDArray[NDArray[float]]]:
        qubits = LineQubit.range(3)
        circuits = [
            Circuit(
                H(qubits[0]),
                X(qubits[1]).controlled_by(qubits[0]),
            ),
            Circuit(
                H(qubits[0]),
                Z(qubits[0]),
                X(qubits[1]).controlled_by(qubits[0]),
            ),
            Circuit(
                H(qubits[0]),
                X(qubits[1]),
                X(qubits[1]).controlled_by(qubits[0]),
            ),
            Circuit(
                H(qubits[0]),
                Z(qubits[0]),
                X(qubits[1]),
                X(qubits[1]).controlled_by(qubits[0]),
            ),
        ]
        state_vectors = [circuit.final_state_vector() for circuit in circuits]
        return [density_matrix_from_state_vector(state_vectors) for state_vectors in state_vectors]

    @staticmethod
    def _is_indistinguishable(state_1: NDArray[NDArray[float]], state_2: NDArray[NDArray[float]]) -> bool:
        return allequal(state_1, state_2)
