from uuid import uuid4

from cirq import ClassicalDataDictionaryStore, Condition, MeasurementKey
from cirq.protocols import json_serialization
from numpy import array, bincount
from numpy._typing import NDArray


class ThreeRepetitionsMajorityVote(Condition):
    def __init__(self, desired_measurement_key: MeasurementKey):
        self.key = MeasurementKey(f'FAULT_TOLERANT_MEASUREMENT_{uuid4().hex}')
        self.desired_measurement_key = desired_measurement_key
        self.number_of_votes = 3

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
            raise ValueError(f'Measurement key {self.key} missing when majority voting.')
        measurements = self._get_measurements(classical_data=classical_data)
        num_measurements = len(measurements)
        if num_measurements == self.number_of_votes:
            majority = int(bincount(measurements).argmax())
            classical_data.record_measurement(key=self.desired_measurement_key,
                                              measurement=(majority,),
                                              qubits=classical_data.measured_qubits[self.key][0],)
            return True
        return False

    def _get_measurements(self, classical_data: ClassicalDataDictionaryStore) -> NDArray[list[int]]:
        num_measurements = len(classical_data.records[self.key])
        return array([classical_data.get_int(self.key, i) for i in range(num_measurements)])

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, desired_measurement_key: MeasurementKey, number_of_votes: int = 3, **kwargs):
        return cls(desired_measurement_key=desired_measurement_key, number_of_votes=number_of_votes)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
