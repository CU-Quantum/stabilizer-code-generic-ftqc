from uuid import uuid4

from cirq import Circuit, LineQubit, MeasurementKey, Operation

from stim_experiments.conditions.recovery_condition import RecoveryCondition
from stim_experiments.custom_dataclasses.recovery import RecoveryGates, RecoveryOperations
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class ErrorRecoveryByGeneratorMeasurement:
    def __init__(self, generator_operations: list[list[Operation]], recoveries: list[RecoveryGates], qubits: list[LineQubit]):
        self._generator_operations = generator_operations
        self._recovery_gates = recoveries
        self._qubits = qubits

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        self._measurer_type = configuration.measurer_type

    def get_error_correction_circuit(self) -> Circuit:
        measurement_key = MeasurementKey(f'ERROR_CORRECTION_{uuid4()}')

        syndrome_operations = [
            self._measurer_type(
                operations=operations,
                measurement_key=measurement_key,
                ).get_measurement_circuit()
            for operations in self._generator_operations
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
        return [
            RecoveryOperations(
                operation=recovery_gates.gate(self._qubits[recovery_gates.qubit_index]),
                symptom=recovery_gates.symptom
            )
            for recovery_gates in self._recovery_gates
        ]
