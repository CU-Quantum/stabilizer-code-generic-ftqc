from typing import Optional

from cirq import Circuit, LineQubit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode


class ShorsRepetitionCode(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None,):
        self._alias = MultipleCatCode(num_cats=3, num_qubits_in_cat_state=3, qubits=qubits)
        super().__init__(num_data_qubits=len(self._alias.data_qubits),
                         num_logical_qubits=self._alias.num_logical_qubits,
                         qubits=self._alias.data_qubits)

    def encode_logical_qubit(self) -> Circuit:
        return self._alias.encode_logical_qubit()

    def get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        return self._alias.get_operation_circuit(operation=operation)

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    def get_error_correction_circuit(self) -> Circuit:
        return self._alias.get_error_correction_circuit()
