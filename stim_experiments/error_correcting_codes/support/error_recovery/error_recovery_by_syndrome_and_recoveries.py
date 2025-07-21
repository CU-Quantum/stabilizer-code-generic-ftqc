from uuid import uuid4

from cirq import Circuit, FrozenCircuit, MeasurementKey, Moment, Operation

from stim_experiments.conditions.recovery_condition import RecoveryCondition
from stim_experiments.custom_dataclasses.recovery import RecoveryOperation
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class ErrorRecoveryByStabilizers:
    def __init__(self, stabilizers: list[list[Operation]], recoveries: list[RecoveryOperation]):
        self._stabilizers = stabilizers
        self._recoveries = recoveries

    def get_error_correction_circuit(self) -> Circuit:
        measurement_key = MeasurementKey(f'ERROR_RECOVERY_{uuid4()}')
        syndrome_operations = [
            self._measurer_type(
                operations=operations,
                measurement_key=measurement_key,
            ).get_measurement_circuit()
            for operations in self._stabilizers
        ]

        recovery_operations = [
            recovery.operation.with_classical_controls(RecoveryCondition(key=measurement_key, symptom=recovery.symptom))
            for recovery in self._recoveries
        ]

        return Circuit(
            syndrome_operations,
            FrozenCircuit(recovery_operations),  # FrozenCircuit in order to ensure separate moment from syndrome extraction
        )

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
