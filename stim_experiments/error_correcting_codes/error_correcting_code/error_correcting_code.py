from abc import ABC, abstractmethod
from functools import cached_property
from typing import List, Optional, Union

from cirq import Circuit, Gate, KET_ZERO, LineQubit, kron
from numpy import array
from numpy._typing import NDArray

from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities, ErrorCorrectingCodeUtilitiesDensityMatrix, ErrorCorrectingCodeUtilitiesStateVector
from stim_experiments.simulators.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.utilities import TYPE_DENSITY_MATRIX, TYPE_STATE_VECTOR


class ErrorCorrectingCode(ABC):
    def __init__(self,
                 num_data_qubits: int,
                 num_ancilla_qubits: int,
                 initial_logical_qubit_state: Union[TYPE_STATE_VECTOR, TYPE_DENSITY_MATRIX],
                 ):
        self._num_data_qubits = num_data_qubits
        self._num_ancilla_qubits = num_ancilla_qubits
        self._initial_logical_qubit_state = initial_logical_qubit_state

        self._current_state = array([])
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
        return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                             qubit_order=self.all_qubits,
                                                                             initial_state=self._current_state)

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        # TODO test that this correctly chooses utilities type
        is_state_vector = len(self._initial_logical_qubit_state.shape) == 1
        return ErrorCorrectingCodeUtilitiesStateVector() if is_state_vector else ErrorCorrectingCodeUtilitiesDensityMatrix()

    @cached_property
    def data_qubits(self) -> List[LineQubit]:
        return self.all_qubits[:self._num_data_qubits]

    @cached_property
    def ancilla_qubits(self) -> List[LineQubit]:
        return self.all_qubits[self._num_data_qubits:]

    @cached_property
    def all_qubits(self) -> List[LineQubit]:
        return LineQubit.range(self._num_data_qubits + self._num_ancilla_qubits)
