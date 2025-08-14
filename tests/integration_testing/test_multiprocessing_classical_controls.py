from multiprocessing import Pool
from typing import Tuple

import pytest
from cirq import Circuit, ClassicalDataStoreReader, Condition, LineQubit, M, MeasurementKey, X

from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.utilities.measurement_key_with_stable_hash import MeasurementKeyWithStableHash


class ConditionWithCustomEq(Condition):
    def __init__(self, key: MeasurementKey):
        self._key = key

    @property
    def keys(self) -> Tuple[MeasurementKey, ...]:
        return (self._key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return ConditionWithCustomEq(replacement) if self._key == current else self

    def resolve(self, classical_data: ClassicalDataStoreReader) -> bool:
        if self._key not in list(classical_data._measurement_types.keys()):
            raise ValueError(f'Not found')
        return True

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class TestMultiprocessingClassicalControls:
    def test_multiprocessing_no_classical_control(self):
        arbitrary_measurement_key = MeasurementKey('arbitrary_key')
        qubits = LineQubit.range(1)
        circuit = Circuit(
            M(qubits[0], key=arbitrary_measurement_key),
            X(qubits[0])
        )
        with Pool(processes=1) as pool:
            pool.map(ErrorCorrectingRunnerClifford().run_circuit, [circuit])

    def test_single_thread_basic_classical_control_succeeds(self):
        arbitrary_measurement_key = MeasurementKey('arbitrary_key')
        qubits = LineQubit.range(1)
        circuit = Circuit(
            M(qubits[0], key=arbitrary_measurement_key),
            X(qubits[0]).with_classical_controls(arbitrary_measurement_key)
        )
        ErrorCorrectingRunnerClifford().run_circuit(circuit)

    def test_multiprocessing_basic_classical_control_fails(self):
        arbitrary_measurement_key = MeasurementKey('arbitrary_key')
        qubits = LineQubit.range(1)
        circuit = Circuit(
            M(qubits[0], key=arbitrary_measurement_key),
            X(qubits[0]).with_classical_controls(arbitrary_measurement_key)
        )
        with pytest.raises(KeyError):
            with Pool(processes=1) as pool:
                pool.map(ErrorCorrectingRunnerClifford().run_circuit, [circuit])

    def test_multiprocessing_basic_classical_control_succeeds_when_circuit_built_inside_thread(self):
        with Pool(processes=1) as pool:
            pool.map(self._create_and_run_circuit, iterable=[()])

    def _create_and_run_circuit(*args, **kwargs):
        arbitrary_measurement_key = MeasurementKey('arbitrary_key')
        qubits = LineQubit.range(1)
        circuit = Circuit(
            M(qubits[0], key=arbitrary_measurement_key),
            X(qubits[0]).with_classical_controls(arbitrary_measurement_key)
        )
        return ErrorCorrectingRunnerClifford().run_circuit(circuit)

    def test_multiprocessing_basic_classical_control_succeeds_when_searching_for_key_in_list(self):
        arbitrary_measurement_key = MeasurementKey('arbitrary_key')
        qubits = LineQubit.range(1)
        circuit = Circuit(
            M(qubits[0], key=arbitrary_measurement_key),
            X(qubits[0]).with_classical_controls(ConditionWithCustomEq(arbitrary_measurement_key))
        )
        with Pool(processes=1) as pool:
            pool.map(ErrorCorrectingRunnerClifford().run_circuit, [circuit])

    def test_multiprocessing_basic_classical_control_succeeds_with_custom_hash(self):
        arbitrary_measurement_key = MeasurementKeyWithStableHash('arbitrary_key')
        qubits = LineQubit.range(1)
        circuit = Circuit(
            M(qubits[0], key=arbitrary_measurement_key),
            X(qubits[0]).with_classical_controls(arbitrary_measurement_key)
        )
        with Pool(processes=1) as pool:
            pool.map(ErrorCorrectingRunnerClifford().run_circuit, [circuit])
