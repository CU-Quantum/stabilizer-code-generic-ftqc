from uuid import uuid4

from cirq import ClassicalDataDictionaryStore, Condition, MeasurementKey
from cirq.protocols import json_serialization
from numpy import array, bincount
from numpy._typing import NDArray

from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager


class MajorityVote(Condition):
    def __init__(self, desired_measurement_key: MeasurementKey):
        self.key = MeasurementKey(f'FAULT_TOLERANT_MEASUREMENT_{uuid4().hex}')
        self.desired_measurement_key = desired_measurement_key
        self.number_of_votes = ConfigurationErrorCorrectingCodeManager().get_configuration().majority_vote_repetitions
        self._start_index = 0

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return MajorityVote(replacement) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'MajorityVote({self.desired_measurement_key!r})'

    def resolve(self, classical_data: ClassicalDataDictionaryStore) -> bool:
        if self.key not in classical_data.keys():
            raise ValueError(f'Measurement key {self.key} missing when majority voting.')
        measurements = self._get_measurements(classical_data=classical_data)
        latest_measurements = measurements[self._start_index:]
        num_measurements = len(latest_measurements)
        if num_measurements == self.number_of_votes:
            majority = int(bincount(latest_measurements).argmax())
            classical_data.record_measurement(key=self.desired_measurement_key,
                                              measurement=(majority,),
                                              qubits=classical_data.measured_qubits[self.key][0],)
            self._start_index += self.number_of_votes
            return True
        return False

    def _get_measurements(self, classical_data: ClassicalDataDictionaryStore) -> NDArray[list[int]]:
        num_measurements = len(classical_data.records[self.key])
        return array([classical_data.get_int(self.key, i) for i in range(num_measurements)])

    def _json_dict_(self):
        return json_serialization.dataclass_json_dict(self)

    @classmethod
    def _from_json_dict_(cls, desired_measurement_key: MeasurementKey, **kwargs):
        return cls(desired_measurement_key=desired_measurement_key)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')
