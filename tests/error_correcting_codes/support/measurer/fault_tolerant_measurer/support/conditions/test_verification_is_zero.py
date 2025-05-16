from uuid import uuid4

import pytest
from cirq import Circuit, CircuitOperation, ClassicalDataDictionaryStore, FrozenCircuit, LineQubit, M, MeasurementKey, \
    Simulator

from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero


class TestVerificationIsZero:
    def test_measurements_are_separate_per_instance(self):
        separate_condition_instances = [VerificationIsZero(key=MeasurementKey(f'{uuid4()}')) for _ in range(2)]
        qubits = LineQubit.range(1)
        circuit = Circuit(
            CircuitOperation(
                FrozenCircuit(
                    M(qubits[0], key=condition.key)
                ),
                use_repetition_ids=False,
                repeat_until=condition
            ) for condition in separate_condition_instances
        )
        Simulator().simulate(circuit)
        assert all(separate_condition_instance._last_num_measurements == 1 for separate_condition_instance in separate_condition_instances)

    def test_missing_key(self):
        store = ClassicalDataDictionaryStore()
        condition = VerificationIsZero(key=MeasurementKey(f'{uuid4()}'))
        with pytest.raises(ValueError, match=f'^Measurement key {condition.key} missing when verifying all zeros\\.$'):
            condition.resolve(classical_data=store)

    def test_resolves_when_all_zero(self):
        condition = VerificationIsZero(key=MeasurementKey(f'{uuid4()}'))
        store = ClassicalDataDictionaryStore()
        self._record_measurements(store=store, key=condition.key, measurements=[0, 0])
        assert condition.resolve(store)

    def test_does_not_resolve_when_one_one(self):
        condition = VerificationIsZero(key=MeasurementKey(f'{uuid4()}'))
        store = ClassicalDataDictionaryStore()
        self._record_measurements(store=store, key=condition.key, measurements=[0, 1])
        assert not condition.resolve(store)

    def test_only_measure_most_recent_measurements(self):
        condition = VerificationIsZero(key=MeasurementKey(f'{uuid4()}'))
        store = ClassicalDataDictionaryStore()

        self._record_measurements(store=store, key=condition.key, measurements=[1, 1])
        assert not condition.resolve(store)
        self._record_measurements(store=store, key=condition.key, measurements=[0, 0])
        assert condition.resolve(store)

    def _record_measurements(self, store: ClassicalDataDictionaryStore, key: MeasurementKey, measurements: list[int]):
        for _, measurement in enumerate(measurements):
            store.record_measurement(key=key, measurement=(measurement,), qubits=(LineQubit(0),))
