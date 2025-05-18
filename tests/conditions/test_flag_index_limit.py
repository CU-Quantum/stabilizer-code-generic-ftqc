import numpy as np
import pytest
from cirq import ClassicalDataDictionaryStore, MeasurementKey, LineQubit
from numpy import array

from stim_experiments.conditions.flag_index_limit import FlagIndexLimit


class TestFlagIndexLimit:
    def test_missing_key(self):
        store = ClassicalDataDictionaryStore()
        key = MeasurementKey('test_key')
        condition = FlagIndexLimit(key=key, parity_check_index=0, flag_sequence=array([]))

        with pytest.raises(ValueError, match='^Measurement key "test_key" missing when checking flags$'):
            condition.resolve(classical_data=store)

    def test_empty_flag_sequence(self):
        store = ClassicalDataDictionaryStore()
        key = MeasurementKey('test_key')
        store.record_measurement(key=key, measurement=(0,), qubits=(LineQubit(0),))

        condition1 = FlagIndexLimit(key=key, parity_check_index=0, flag_sequence=array([]))
        with pytest.raises(ValueError, match='^No flag sequence was given for key "test_key"$'):
            condition1.resolve(classical_data=store)

    def test_num_measurements_dont_match_num_flags(self):
        store = ClassicalDataDictionaryStore()
        key = MeasurementKey('test_key')
        flag_sequence = np.array([[0, 1]])
        condition = FlagIndexLimit(key=key, parity_check_index=0, flag_sequence=flag_sequence)

        store.record_measurement(key=key, measurement=(0,), qubits=(LineQubit(0),))
        with pytest.raises(ValueError, match='^Number of measurements for key "test_key" \\(1\\) does not match number of flags \\(2\\)$'):
            condition.resolve(classical_data=store)

        store.record_measurement(key=key, measurement=(1,), qubits=(LineQubit(0),))
        assert condition.resolve(classical_data=store)

        store.record_measurement(key=key, measurement=(0,), qubits=(LineQubit(0),))
        with pytest.raises(ValueError, match='^Number of measurements for key "test_key" \\(3\\) does not match number of flags \\(2\\)$'):
            condition.resolve(classical_data=store)

    def test_parity_check_index_less_than_or_equal_to_first_occurrence(self):
        store = ClassicalDataDictionaryStore()
        key = MeasurementKey('test_key')
        flag_sequence = np.array([[0, 1], [1, 0], [1, 1]])

        store.record_measurement(key=key, measurement=(1,), qubits=(LineQubit(0),))
        store.record_measurement(key=key, measurement=(0,), qubits=(LineQubit(0),))
        conditions = [FlagIndexLimit(key=key, parity_check_index=i, flag_sequence=flag_sequence)
                      for i in range(3)]
        assert conditions[0].resolve(classical_data=store)
        assert conditions[1].resolve(classical_data=store)
        assert not conditions[2].resolve(classical_data=store)
