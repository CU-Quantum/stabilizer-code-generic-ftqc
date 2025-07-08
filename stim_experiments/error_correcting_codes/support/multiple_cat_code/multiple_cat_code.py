from typing import Optional

from cirq import Circuit, X, Z

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import CatParityCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class MultipleCatCode(CatParityCode):
    def encode_logical_qubit(self) -> Circuit:
        return Circuit(
            [
                self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit()
                for subregister in self.subregisters
            ],
            self.get_error_correction_circuit()
        )

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(self._num_cats)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_in_cat_state)]
            )
        return None

    @property
    def _cat_state_creator_type(self) -> type[CatStateCreator]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().cat_state_creator_type
