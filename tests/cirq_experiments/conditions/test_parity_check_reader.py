import pytest
from cirq import ClassicalDataDictionaryStore, MeasurementKey, LineQubit

from cirq_experiments.conditions.parity_check_reader import ParityCheckReader


class TestParityCheckReader:
    @pytest.fixture(autouse=True)
    def _setup(self):
        self._store = ClassicalDataDictionaryStore()
        self._key = MeasurementKey('test_key')

    def test_missing_key(self):
        reader = ParityCheckReader(key=self._key, qubit_correction_index=0)
        with pytest.raises(ValueError, match='Measurement key test_key missing when testing classical control'):
            reader.resolve(classical_data=self._store)

    @pytest.mark.parametrize('measurements', [[int(i - 1 <= j <= i) for j in range(3)] for i in range(4)])
    @pytest.mark.parametrize('qubit_index, measurement_trigger', [
        (0, [1, 0, 0]),
        (1, [1, 1, 0]),
        (2, [0, 1, 1]),
        (3, [0, 0, 1]),
    ])
    def test_resolve(self, measurements: list[int], qubit_index: int, measurement_trigger: list[int]):
        reader = ParityCheckReader(key=self._key, qubit_correction_index=qubit_index)
        should_resolve_to_true = measurements == measurement_trigger
        for measurement in measurements:
            self._store.record_measurement(key=self._key, measurement=(measurement,), qubits=(LineQubit(0),))
        assert reader.resolve(classical_data=self._store) == should_resolve_to_true
