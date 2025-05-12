from dataclasses import dataclass, field
from typing import Tuple
from uuid import uuid4

from cirq import Circuit, ClassicalDataStoreReader, Condition, MeasurementKey, Operation

from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import RecoveryGates, RecoveryOperations
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer


@dataclass(frozen=True)
class RecoveryCondition(Condition):
    # TODO test class
    key: MeasurementKey
    symptom: list[int] = field(default_factory=list)

    @property
    def keys(self) -> Tuple[MeasurementKey, ...]:
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return RecoveryCondition(replacement, self.symptom) if self.key == current else self

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when checking for recovery')
        measurements = [x[0] for x in classical_data.records[self.key]]
        return measurements == self.symptom

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class FaultTolerantErrorCorrection:
    def __init__(self, generator_operations: list[list[Operation]], recoveries: list[RecoveryOperations]):
        self._generator_operations = generator_operations
        self._recoveries = recoveries

    def get_error_correction_circuit(self) -> Circuit:
        measurement_key = MeasurementKey(f'ERROR_CORRECTION_{uuid4()}')

        syndrome_operations = [
            FaultTolerantMeasurer(
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
