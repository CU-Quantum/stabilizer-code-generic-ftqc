from dataclasses import dataclass, field
from typing import Tuple

from cirq import ClassicalDataStoreReader, Condition, MeasurementKey


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
