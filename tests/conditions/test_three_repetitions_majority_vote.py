import pytest
from cirq import ClassicalDataDictionaryStore, MeasurementKey, LineQubit

from stim_experiments.conditions.three_repetitions_majority_vote import ThreeRepetitionsMajorityVote


class TestThreeRepetitionsMajorityVote:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._store = ClassicalDataDictionaryStore()
        self._desired_key = MeasurementKey('desired_key')
        self._condition = ThreeRepetitionsMajorityVote(desired_measurement_key=self._desired_key)
        self._qubit = LineQubit(0)

    def test_missing_key(self):
        with pytest.raises(ValueError, match=f'Measurement key {self._condition.key} missing when majority voting.'):
            self._condition.resolve(classical_data=self._store)

    def test_resolve_with_majority_1(self):
        self._record_measurements([1, 1, 0])
        assert self._condition.resolve(classical_data=self._store)
        assert self._store.get_int(self._desired_key, 0) == 1

    def test_resolve_with_majority_0(self):
        self._record_measurements([0, 0, 1])
        assert self._condition.resolve(classical_data=self._store)
        assert self._store.get_int(self._desired_key, 0) == 0

    def test_resolve_with_majority_equal(self):
        self._record_measurements([1, 1, 1])
        assert self._condition.resolve(classical_data=self._store)
        assert self._store.get_int(self._desired_key, 0) == 1

    def test_resolve_with_insufficient_number_of_votes(self):
        self._record_measurements([1, 1])
        assert not self._condition.resolve(classical_data=self._store)
        assert self._desired_key not in self._store.keys()

    def test_resolve_with_excess_number_of_votes(self):
        self._record_measurements([1, 1, 1, 1])
        assert not self._condition.resolve(classical_data=self._store)
        assert self._desired_key not in self._store.keys()

    def _record_measurements(self, measurements: list[int]):
        for measurement in measurements:
            self._store.record_measurement(key=self._condition.key, measurement=(measurement,), qubits=(self._qubit,))
