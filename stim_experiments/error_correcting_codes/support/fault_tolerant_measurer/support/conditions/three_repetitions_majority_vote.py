from uuid import uuid4

from cirq import ClassicalDataDictionaryStore, Condition, MeasurementKey
from cirq.protocols import json_serialization
from numpy import array, bincount


class ThreeRepetitionsMajorityVote(Condition):
    def __init__(self, desired_measurement_key: str):
        self.key = MeasurementKey(f'FAULT_TOLERANT_MEASUREMENT_{uuid4().hex}')
        self.desired_measurement_key = desired_measurement_key

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        self.key = replacement
        return self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'ThreeRepetitionsMajorityVote({self.key!r})'

    def resolve(self, classical_data: ClassicalDataDictionaryStore) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when testing classical control')
        num_measurements = len(classical_data.records[self.key])
        if num_measurements == 3:
            measurements = array([classical_data.get_int(self.key, i) for i in range(num_measurements)])  # TODO doesn't seem to be varying in measurement
            majority = int(bincount(measurements).argmax())
            classical_data.record_measurement(key=MeasurementKey(self.desired_measurement_key),
                                              measurement=(majority,),
                                              qubits=classical_data.measured_qubits[self.key][0],)
            return True
        return False

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, desired_measurement_key: str, **kwargs):
        return cls(desired_measurement_key=desired_measurement_key)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
