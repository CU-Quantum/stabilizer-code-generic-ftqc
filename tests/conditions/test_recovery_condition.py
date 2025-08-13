import pytest
from cirq import ClassicalDataDictionaryStore, MeasurementKey, LineQubit

from stim_experiments.conditions.recovery_condition import RecoveryCondition


class TestRecoveryCondition:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._store = ClassicalDataDictionaryStore()
        self._key = MeasurementKey('test_key')
        self._symptom = [1, 0, 1]
        self._condition = RecoveryCondition(key=self._key, symptom=tuple(self._symptom))
        self._qubit = LineQubit(0)

    def test_missing_key(self):
        with pytest.raises(ValueError, match='Measurement key test_key missing when checking for recovery'):
            self._condition.resolve(classical_data=self._store)

    def test_resolve_matching_symptom(self):
        for measurement in self._symptom:
            self._store.record_measurement(key=self._key, measurement=(measurement,), qubits=(self._qubit,))
        assert self._condition.resolve(classical_data=self._store)

    def test_resolve_non_matching_symptom(self):
        different_symptom = [1, 1, 1]
        for measurement in different_symptom:
            self._store.record_measurement(key=self._key, measurement=(measurement,), qubits=(self._qubit,))
        assert not self._condition.resolve(classical_data=self._store)

    def test_resolve_different_length_symptom(self):
        different_length_symptom = self._symptom + [1]
        for measurement in different_length_symptom:
            self._store.record_measurement(key=self._key, measurement=(measurement,), qubits=(self._qubit,))

    def test_empty_symptom(self):
        condition = RecoveryCondition(key=self._key, symptom=())
        self._store.record_measurement(key=self._key, measurement=(0,), qubits=(self._qubit,))
        with pytest.raises(ValueError, match='^No symptom was given for key "test_key"$'):
            condition.resolve(classical_data=self._store)
