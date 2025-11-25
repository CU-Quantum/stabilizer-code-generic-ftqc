from dataclasses import dataclass

from cirq import ClassicalDataStoreReader, MeasurementKey, dataclass_json_dict, json_cirq_type

from cirq_experiments.conditions.custom_condition import CustomCondition


@dataclass(frozen=True)
class ParityCheckReader(CustomCondition):
    key: MeasurementKey
    qubit_correction_index: int = 0

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return ParityCheckReader(replacement, self.qubit_correction_index) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'{json_cirq_type(type(self))}({self.key!r}, f{self.qubit_correction_index})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when testing classical control')
        measurements = [x[0] for x in classical_data.records[self.key]]
        if not self.qubit_correction_index:
            return measurements[self.qubit_correction_index] and not measurements[self.qubit_correction_index + 1]
        elif self.qubit_correction_index == len(measurements):
            return not measurements[self.qubit_correction_index - 2] and measurements[self.qubit_correction_index - 1]
        else:
            return bool(measurements[self.qubit_correction_index - 1] and measurements[self.qubit_correction_index])

    def _json_dict_(self):
        return dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, key, qubit_correction_index, **kwargs):
        return cls(key=key, qubit_correction_index=qubit_correction_index)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
