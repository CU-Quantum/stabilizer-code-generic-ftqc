from cirq import ClassicalDataStoreReader, Condition, MeasurementKey
from cirq.protocols import json_serialization


class VerificationIsZero(Condition):
    def __init__(self, last_num_measurements: int = 0):
        self.key = MeasurementKey('VERIFICATION')
        self.last_num_measurements = last_num_measurements

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        self.key = replacement
        return self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'VerificationIsZero({self.key!r})'

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when testing classical control')
        num_measurements = len(classical_data.records[self.key])
        all_zero = all(classical_data.get_int(self.key, i) == 0 for i in range(self.last_num_measurements, num_measurements))
        self.last_num_measurements = num_measurements
        return all_zero

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, last_num_measurements: int = 0, **kwargs):
        return cls(last_num_measurements=last_num_measurements)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
