from dataclasses import dataclass
from functools import cached_property
from typing import List, Optional

from cirq import Circuit, ClassicalDataStoreReader, Condition, KeyCondition, LineQubit, M, MeasurementKey, Operation, R, \
    X
from cirq.protocols import json_serialization
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import ErrorCorrectingCodeUtilities, \
    get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


class VerificationIsZero(Condition):
    def __init__(self, last_num_measurements: int = 0):
        self.key = MeasurementKey('VERIFICATION')
        self.last_num_measurements = last_num_measurements

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        return KeyCondition(replacement) if self.key == current else self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'cirq.KeyCondition({self.key!r})'

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
    def _from_json_dict_(cls, key, **kwargs):
        return cls(key=key)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class ParityVerifier:
    def __init__(self,
                 target_qubits: List[LineQubit],
                 ancilla_qubit: Optional[LineQubit] = None):
        self._target_qubits = target_qubits
        self._ancilla_qubit = ancilla_qubit if ancilla_qubit else LineQubit(self._num_qubits)

    def is_valid_cat_state(self) -> list[list[Operation]]:
        return [
                [
                    X(self._ancilla_qubit).controlled_by(self._target_qubits[i]),
                    X(self._ancilla_qubit).controlled_by(self._target_qubits[i + 1]),
                    M(self._ancilla_qubit, key=VerificationIsZero().key),
                    R(self._ancilla_qubit),
                ]
                for i in range(self._num_qubits - 1)
            ]
        # num_qubits = len(self._state_qubits)
        # for i in range(num_qubits - 1):
        #     circuit = Circuit(
        #         X(self._ancilla_qubit).controlled_by(self._state_qubits[i]),
        #         X(self._ancilla_qubit).controlled_by(self._state_qubits[i + 1]),
        #         M(self._ancilla_qubit),
        #         R(self._ancilla_qubit),
        #     )
        #     state = self._get_state_after_circuit(circuit=circuit)
        #     measurement = list(state.measurements.values())[0][0]
        #     if measurement != 0:
        #         return False
        # return True

    def _get_state_after_circuit(self, circuit: Circuit) -> StateAndMeasurements:
        if self._ancilla_qubit in self._target_qubits:
            return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                 qubit_order=self._target_qubits,
                                                                                 initial_state=self._cat_state)
        else:
            state_with_new_ancilla = tensor(self._cat_state, self._error_correcting_code_utilities.zero_state)
            return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                 qubit_order=self._target_qubits + [self._ancilla_qubit],
                                                                                 initial_state=state_with_new_ancilla)

    @cached_property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._cat_state)

    @property
    def _num_qubits(self) -> int:
        return len(self._target_qubits)


class TestParityVerifier:
    def test_valid_cat_state_two_qubit(self):
        two_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                               + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        qubits = LineQubit.range(2)
        verifier = ParityVerifier(cat_state=two_qubit_cat_state, target_qubits=qubits)
        assert verifier.is_valid_cat_state()

    def test_invalid_cat_state_two_qubit(self):
        invalid_cat_state = ((1 / sqrt(2)) * tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        qubits = LineQubit.range(2)
        verifier = ParityVerifier(cat_state=invalid_cat_state, target_qubits=qubits)
        assert not verifier.is_valid_cat_state()

    def test_valid_cat_state_three_qubit(self):
        three_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                 + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(cat_state=three_qubit_cat_state, target_qubits=qubits)
        assert verifier.is_valid_cat_state()

    def test_invalid_cat_state_three_qubit(self):
        three_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
                                 + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)))
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(cat_state=three_qubit_cat_state, target_qubits=qubits)
        assert not verifier.is_valid_cat_state()

    def test_can_provide_ancilla_qubit(self):
        two_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                 + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        bad_ancilla_state = KET_ONE_STATE_VECTOR
        two_qubit_cat_state_with_bad_ancilla = tensor(two_qubit_cat_state, bad_ancilla_state)
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(cat_state=two_qubit_cat_state_with_bad_ancilla,
                                  target_qubits=qubits,
                                  ancilla_qubit=qubits[-1])
        assert not verifier.is_valid_cat_state()

    def test_can_provide_ancilla_outside_state(self):
        two_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                               + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        qubits = LineQubit.range(2)
        verifier = ParityVerifier(cat_state=two_qubit_cat_state,
                                  target_qubits=qubits,
                                  ancilla_qubit=LineQubit(len(qubits)))
        assert verifier.is_valid_cat_state()

    def test_can_use_density_matrix(self):
        two_qubit_cat_state = (.5 * (tensor(KET_ZERO_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX)
                               + tensor(KET_ONE_DENSITY_MATRIX, KET_ONE_DENSITY_MATRIX)))
        qubits = LineQubit.range(2)
        verifier = ParityVerifier(cat_state=two_qubit_cat_state, target_qubits=qubits)
        assert verifier.is_valid_cat_state()
