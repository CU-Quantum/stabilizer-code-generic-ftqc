from abc import ABC, abstractmethod
from functools import cached_property
from typing import List

from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, LineQubit, Simulator, \
    StateVectorTrialResult, kron
from numpy._typing import NDArray

from stim_experiments.simulators.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.utilities import TYPE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX


class ErrorCorrectingCode(ABC):
    def __init__(self, num_data_qubits: int, num_ancilla_qubits: int, initial_logical_qubit_state_density_matrix: TYPE_DENSITY_MATRIX):
        self._initial_logical_qubit_state_density_matrix = initial_logical_qubit_state_density_matrix
        self._num_data_qubits = num_data_qubits
        self._num_ancilla_qubits = num_ancilla_qubits

        self._current_state = kron(*[KET_ZERO_DENSITY_MATRIX for _ in range(len(self.all_qubits))])
        self._encode_logical_qubit()

    @abstractmethod
    def _encode_logical_qubit(self) -> None:
        pass

    @abstractmethod
    def correct_errors(self) -> None:
        pass

    def get_current_state(self) -> NDArray[NDArray[complex]]:
        return self._current_state

    def apply_error(self, gate: Gate, qubit_index: int) -> None:
        circuit = Circuit(gate(self.all_qubits[qubit_index]))
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    @abstractmethod
    def apply_operation(self, operation: LogicalOperation) -> None:
        pass

    def _get_state_after_circuit(self, circuit: Circuit) -> TYPE_DENSITY_MATRIX:
        # simulator = Simulator()
        # simulation: StateVectorTrialResult = simulator.simulate(circuit, qubit_order=self.all_qubits, initial_state=self._current_state)
        # return simulation.final_state_vector
        simulator = DensityMatrixSimulator()
        simulation: DensityMatrixTrialResult = simulator.simulate(circuit, qubit_order=self.all_qubits, initial_state=self._current_state)
        return simulation.final_density_matrix

    @cached_property
    def data_qubits(self) -> List[LineQubit]:
        return self.all_qubits[:self._num_data_qubits]

    @cached_property
    def ancilla_qubits(self) -> List[LineQubit]:
        return self.all_qubits[self._num_data_qubits:]

    @cached_property
    def all_qubits(self) -> List[LineQubit]:
        return LineQubit.range(self._num_data_qubits + self._num_ancilla_qubits)
