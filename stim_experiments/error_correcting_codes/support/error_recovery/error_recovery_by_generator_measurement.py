from uuid import uuid4

from cirq import Circuit, LineQubit, MeasurementKey

from stim_experiments.conditions.recovery_condition import RecoveryCondition
from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.recovery import RecoveryOperations
from stim_experiments.error_correcting_codes.support.check_matrix_to_operations import CheckMatrixToOperations
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.recovery_finder import RecoveryFinder
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class ErrorRecoveryByGeneratorMeasurement:
    def __init__(self, check_matrix: CheckMatrix, qubits: list[LineQubit]):
        self._check_matrix = check_matrix
        self._qubits = qubits

    def get_error_correction_circuit(self) -> Circuit:
        measurement_key = MeasurementKey(f'ERROR_CORRECTION_{uuid4()}')
        generator_operations = CheckMatrixToOperations(check_matrix=self._check_matrix, qubits=self._qubits).get_operations()

        syndrome_operations = [
            self._measurer_type(
                operations=operations,
                measurement_key=measurement_key,
                ).get_measurement_circuit()
            for operations in generator_operations
        ]

        recovery_operations = [
            recovery.operation.with_classical_controls(RecoveryCondition(key=measurement_key, symptom=recovery.symptom))
            for recovery in self._recoveries
        ]

        return Circuit(
            syndrome_operations,
            recovery_operations,
        )

    @property
    def _recoveries(self) -> list[RecoveryOperations]:
        recoveries = RecoveryFinder(check_matrix=self._check_matrix).find_recoveries()
        return [
            RecoveryOperations(
                operation=recovery_gates.gate(self._qubits[recovery_gates.qubit_index]),
                symptom=recovery_gates.symptom
            )
            for recovery_gates in recoveries
        ]

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
