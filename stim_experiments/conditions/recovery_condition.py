from dataclasses import dataclass
from typing import Tuple

from cirq import ClassicalDataStoreReader, MeasurementKey, dataclass_json_dict, json_cirq_type

from stim_experiments.conditions.custom_condition import CustomCondition


@dataclass(frozen=True)
class RecoveryCondition(CustomCondition):
    key: MeasurementKey
    symptom: tuple[int, ...]  # must be tuple instead of list to hash correctly for serialization

    @property
    def keys(self) -> Tuple[MeasurementKey, ...]:
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return RecoveryCondition(replacement, self.symptom) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'{json_cirq_type(type(self))}({self.key!r}, f{self.symptom})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when checking for recovery')
        if not len(self.symptom):
            raise ValueError(f'No symptom was given for key "{self.key}"')
        measurements = [x[0] for x in classical_data.records[self.key]]
        return measurements == list(self.symptom)

    def _json_dict_(self):
        return dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key: MeasurementKey, symptom: tuple[int, ...], **kwargs):
        return cls(key=key, symptom=symptom)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
