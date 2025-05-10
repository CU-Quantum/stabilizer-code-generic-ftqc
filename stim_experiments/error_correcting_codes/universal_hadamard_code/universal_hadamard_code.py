from typing import Optional

from cirq import Circuit
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode


class UniversalHadamardCode(ErrorCorrectingCode):
    # TODO test this
    num_cats = 3

    def __init__(self, num_qubits_in_cat_state: int, qubit_start_index: int = 0):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        num_data_qubits = num_qubits_in_cat_state * self.num_cats
        num_parity_checks_per_register = num_qubits_in_cat_state - 1
        x_stabilizers = [
            [0] * num_data_qubits + [self._qubit_has_x_stabilizer_in_generator(cat_index=cat_index,
                                                                               parity_check_index=parity_check_index,
                                                                               qubit_index=qubit_index)
                                     for qubit_index in range(num_data_qubits)]
            for cat_index in range(self.num_cats)
            for parity_check_index in range(num_parity_checks_per_register)
        ]
        z_stabilizers = [
            [int(cat_index * self._num_qubits_in_cat_state <= qubit_index < (cat_index + 2) * self._num_qubits_in_cat_state)
             for qubit_index in range(num_data_qubits)] + [0] * num_data_qubits
            for cat_index in range(self.num_cats - 1)
        ]
        self._alias = GenericStabilizerCode(generators=array(x_stabilizers + z_stabilizers))
        super().__init__(num_data_qubits=len(self._alias.data_qubits),
                         num_logical_qubits=self._alias.num_logical_qubits,
                         qubit_start_index=qubit_start_index)

    def _qubit_has_x_stabilizer_in_generator(self, cat_index: int, parity_check_index: int, qubit_index: int) -> int:
        low_index = cat_index * self._num_qubits_in_cat_state + parity_check_index
        high_index = low_index + 1
        return int(low_index <= qubit_index <= high_index)

    def encode_logical_qubit(self) -> Circuit:
        return self._alias.encode_logical_qubit()

    def get_error_correction_circuit(self) -> Circuit:
        return self._alias.get_error_correction_circuit()

    def get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        return self._alias.get_operation_circuit(operation=operation)

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass

    @property
    def implemented_operations(self) -> list[LogicalGateLabel]:
        return self._alias.implemented_operations
