from typing import Optional

from cirq import Circuit

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.utilities import KET_ZERO_STATE_VECTOR


class ThreeCatCode(ErrorCorrectingCode):
    num_repetitions = 3

    def __init__(self, num_qubits_in_cat_state: int):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        super().__init__(num_data_qubits=num_qubits_in_cat_state * self.num_repetitions,
                         num_ancilla_qubits=0,
                         num_logical_qubits=1,
                         qubit_start_index=0,
                         provided_ancilla_qubits=None)

    def encode_logical_qubit(self) -> Circuit:
        return Circuit(
            CatStateCreatorFlagPattern(qubit_register=self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                                       ).get_cat_state_circuit()
            for i in range(self.num_repetitions)
        )

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass

    @property
    def _implemented_operations(self) -> list[LogicalGateLabel]:
        return []
