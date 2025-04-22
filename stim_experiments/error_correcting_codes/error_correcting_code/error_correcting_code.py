from abc import ABC, abstractmethod
from functools import cached_property
from typing import Optional

from cirq import Circuit, Gate, LineQubit

from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.utilities import get_error_correcting_code_utilities
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class ErrorCorrectingCode(ABC):
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance._saved_init_args = (args, kwargs)
        return instance

    def create_new(self, qubit_start_index: int = 0, provided_ancilla_qubits: Optional[list[LineQubit]] = None) -> 'ErrorCorrectingCode':
        self._saved_init_args[1]['qubit_start_index'] = qubit_start_index
        self._saved_init_args[1]['provided_ancilla_qubits'] = provided_ancilla_qubits
        return self.__class__(*self._saved_init_args[0], **self._saved_init_args[1])

    def __init__(self,
                 num_data_qubits: int,
                 num_ancilla_qubits: int,
                 num_logical_qubits: int,
                 initial_logical_qubit_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX,
                 qubit_start_index: int,
                 provided_ancilla_qubits: Optional[list[LineQubit]],
                 ):
        self._num_data_qubits = num_data_qubits
        self._num_ancilla_qubits = num_ancilla_qubits
        self._num_logical_qubits = num_logical_qubits
        self._initial_logical_qubit_state = initial_logical_qubit_state
        self._qubit_start_index = qubit_start_index
        self._provided_ancilla_qubits = provided_ancilla_qubits

    @abstractmethod
    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    @abstractmethod
    def get_error_correction_circuit(self) -> Circuit:
        pass

    @abstractmethod
    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass

    @property
    @abstractmethod
    def _implemented_operations(self) -> list[LogicalGateLabel]:
        pass

    def get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        if operation.gate not in self._implemented_operations:
            raise NotImplementedError(f"Operation {operation.gate.name} is not implemented. Implemented gates are: {[x.name for x in self._implemented_operations]}.")
        if not 0 <= operation.qubit_index < self._num_logical_qubits:
            raise ValueError(f"Qubit index must be between 0 and {self._num_logical_qubits - 1}. Was given {operation.qubit_index}.")
        return self._perform_get_operation_circuit(operation=operation)

    def get_error_circuit(self, gate: Gate, qubit_index: int) -> Circuit:
        return Circuit(gate(self.all_qubits[qubit_index]))

    @property
    def error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._initial_logical_qubit_state)

    @cached_property
    def all_qubits(self) -> list[LineQubit]:
        return self.data_qubits + self.ancilla_qubits

    @cached_property
    def data_qubits(self) -> list[LineQubit]:
        return LineQubit.range(self._qubit_start_index, self._qubit_start_index + self._num_data_qubits)

    @cached_property
    def ancilla_qubits(self) -> list[LineQubit]:
        if self._provided_ancilla_qubits is not None and len(self._provided_ancilla_qubits) != self._num_ancilla_qubits:
            raise ValueError(f"Number of provided ancilla qubits ({len(self._provided_ancilla_qubits)}) does not match "
                             f"the required number ({self._num_ancilla_qubits}).")
        new_ancilla_qubits = LineQubit.range(self._qubit_start_index + self._num_data_qubits,
                                             self._qubit_start_index + self._num_data_qubits + self._num_ancilla_qubits)
        return self._provided_ancilla_qubits or new_ancilla_qubits

    @property
    def num_logical_qubits(self) -> int:
        return self._num_logical_qubits
