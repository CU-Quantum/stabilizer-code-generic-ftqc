from abc import ABC, abstractmethod

from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, LineQubit, kron
from numpy import array
from numpy._typing import NDArray

from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


class ErrorCorrectingCode(ABC):
    def __init__(self, initial_logical_qubit_state_density_matrix: DENSITY_MATRIX_TYPE, num_data_qubits: int, num_ancilla_qubits: int):
        self._initial_logical_qubit_state_density_matrix = initial_logical_qubit_state_density_matrix
        self._num_data_qubits = num_data_qubits
        self._num_ancilla_qubits = num_ancilla_qubits

        self._current_state = array([])
        self._qubits = LineQubit.range(self._num_data_qubits + self._num_ancilla_qubits)
        self._data_qubits = self._qubits[:self._num_data_qubits]
        self._ancilla_qubits = self._qubits[self._num_data_qubits:]

        self._current_state = kron(*[KET_ZERO_DENSITY_MATRIX for _ in range(len(self._qubits))])
        self._encode_logical_qubit()

    @abstractmethod
    def _encode_logical_qubit(self) -> None:
        pass

    @abstractmethod
    def correct_errors(self) -> None:
        pass

    def get_current_state(self) -> NDArray[NDArray[complex]]:
        return self._current_state

    def apply_gate(self, gate: Gate, qubit_index: int) -> None:
        circuit = Circuit(gate(self._qubits[qubit_index]))
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _get_state_after_circuit(self, circuit: Circuit) -> DENSITY_MATRIX_TYPE:
        simulator = DensityMatrixSimulator()
        simulation: DensityMatrixTrialResult = simulator.simulate(circuit, qubit_order=self._qubits, initial_state=self._current_state)
        return simulation.final_density_matrix
