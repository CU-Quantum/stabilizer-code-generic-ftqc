from abc import ABC, abstractmethod
from functools import cached_property
from typing import List

from cirq import Circuit, Gate, LineQubit
from numpy import array
from numpy._typing import NDArray
from numpy.ma.core import allequal

from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities, ErrorCorrectingCodeUtilitiesDensityMatrix, ErrorCorrectingCodeUtilitiesStateVector
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class ErrorCorrectingCode(ABC):
    def __new__(cls, *args, **kwargs):
        cls._saved_init_args = (args, kwargs)
        return super().__new__(cls)

    def create_new(self) -> 'ErrorCorrectingCode':
        return self.__class__(*self._saved_init_args[0], **self._saved_init_args[1])

    def __init__(self,
                 num_data_qubits: int,
                 num_ancilla_qubits: int,
                 num_logical_qubits: int,
                 initial_logical_qubit_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX,
                 ):
        self._num_data_qubits = num_data_qubits
        self._num_ancilla_qubits = num_ancilla_qubits
        self._num_logical_qubits = num_logical_qubits
        self._initial_logical_qubit_state = initial_logical_qubit_state

        self._current_state = array([])
        self._encode_logical_qubit()

    @abstractmethod
    def _encode_logical_qubit(self) -> None:
        pass

    @abstractmethod
    def correct_errors(self) -> None:
        pass

    @abstractmethod
    def _perform_apply_operation(self, operation: LogicalOperation) -> None:
        pass

    @property
    @abstractmethod
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        pass

    def apply_operation(self, operation: LogicalOperation) -> None:
        if operation.gate not in self._implemented_operations:
            raise NotImplementedError(f"Operation {operation.gate.name} is not implemented. Implemented gates are: {[x.name for x in self._implemented_operations]}.")
        if not 0 <= operation.qubit_index < self._num_logical_qubits:
            raise ValueError(f"Qubit index must be between 0 and {self._num_logical_qubits - 1}. Was given {operation.qubit_index}.")
        self._perform_apply_operation(operation=operation)

    def get_current_state(self) -> NDArray[NDArray[complex]]:
        return self._current_state

    def apply_error(self, gate: Gate, qubit_index: int) -> None:
        circuit = Circuit(gate(self.all_qubits[qubit_index]))
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _get_state_after_circuit(self, circuit: Circuit) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                             qubit_order=self.all_qubits,
                                                                             initial_state=self._current_state)

    @property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
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

    @property
    def num_logical_qubits(self) -> int:
        return self._num_logical_qubits

    def __eq__(self, other):
        return allequal(self.get_current_state(), other.get_current_state())
