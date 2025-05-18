from typing import Optional
from uuid import uuid4

from cirq import Circuit, LineQubit, \
    MeasurementKey, X, Z

from stim_experiments.conditions.parity_check_reader import ParityCheckReader
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class ThreeCatCode(ErrorCorrectingCode):
    num_cats = 3

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        super().__init__(num_data_qubits=num_qubits_in_cat_state * self.num_cats,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        return Circuit(
            [
                self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit()
                for subregister in self.subregisters
            ],
            self.get_error_correction_circuit()
        )

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit(
            self._correct_x_errors(),
            self._correct_z_errors()
        )

    def _correct_x_errors(self) -> Circuit:
        circuit = Circuit()
        for cat_index in range(self.num_cats):
            measurement_key = MeasurementKey(f"THREE_CAT_Z_STABILIZER_{cat_index}_{uuid4()}")
            syndrome_measurement = [
                self._measurer_type(operations=[Z(self.data_qubits[cat_index * self._num_qubits_in_cat_state + pair_start_index + i])
                                                for i in range(2)],
                                    measurement_key=measurement_key).get_measurement_circuit()
                for pair_start_index in range(self._num_qubits_in_cat_state - 1)
            ]
            recovery = [
                X(self.data_qubits[cat_index * self._num_qubits_in_cat_state + i])
                    .with_classical_controls(ParityCheckReader(key=measurement_key, qubit_correction_index=i))
                for i in range(self._num_qubits_in_cat_state)
            ] if syndrome_measurement else []
            circuit.append([
                syndrome_measurement,
                recovery
            ])
        return circuit

    def _correct_z_errors(self) -> Circuit:
        circuit = Circuit()
        measurement_key = MeasurementKey(f"THREE_CAT_X_STABILIZER_{uuid4()}")
        for cat_index in range(self.num_cats - 1):
            circuit.append(
                self._measurer_type(
                    operations=[X(self.data_qubits[cat_index * self._num_qubits_in_cat_state + i])
                                for i in range(2 * self._num_qubits_in_cat_state)],
                    measurement_key=measurement_key).get_measurement_circuit()
            )
        circuit.append(
            [
                Z(self.data_qubits[cat_index * self._num_qubits_in_cat_state])
                    .with_classical_controls(ParityCheckReader(key=measurement_key, qubit_correction_index=cat_index))
                for cat_index in range(self.num_cats)
            ]
        )
        return circuit

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(self.num_cats)],
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_in_cat_state)]
            )
        return None

    @property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                for i in range(self.num_cats)]

    @property
    def _cat_state_creator_type(self) -> type[CatStateCreator]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().cat_state_creator_type

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
