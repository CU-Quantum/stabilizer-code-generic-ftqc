from typing import List, Optional

from cirq import Circuit, ClassicalDataStoreReader, Condition, KeyCondition, LineQubit, M, MeasurementKey, R, \
    X
from cirq.protocols import json_serialization
from numpy import array, sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import \
    get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.utilities import get_cat_state_vector


class VerificationIsZero(Condition):
    def __init__(self, last_num_measurements: int = 0):
        self.key = MeasurementKey('VERIFICATION')
        self.last_num_measurements = last_num_measurements

    @property
    def keys(self):
        return (self.key,)

    def replace_key(self, current: MeasurementKey, replacement: MeasurementKey):
        self.key = replacement
        return self

    def __str__(self):
        return str(self.key)

    def __repr__(self):
        return f'VerificationIsZero({self.key!r})'

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
    def _from_json_dict_(cls, last_num_measurements: int = 0, **kwargs):
        return cls(last_num_measurements=last_num_measurements)

    @property
    def qasm(self):
        raise ValueError('QASM is defined only for SympyConditions of type key == constant.')


class ParityVerifier:
    def __init__(self,
                 target_qubits: List[LineQubit],
                 verifier_ancilla: Optional[LineQubit] = None):
        self._target_qubits = target_qubits
        self._verifier_ancilla = verifier_ancilla

    def validate_parity(self) -> Circuit:
        return Circuit(
                [
                    X(self._verifier_ancilla).controlled_by(self._target_qubits[i]),
                    X(self._verifier_ancilla).controlled_by(self._target_qubits[i + 1]),
                    M(self._verifier_ancilla, key=VerificationIsZero().key),
                    R(self._verifier_ancilla),
                ]
                for i in range(self._num_target_qubits - 1)
        )

    @property
    def _num_target_qubits(self) -> int:
        return len(self._target_qubits)


class TestParityVerifier:
    def test_trivial(self):
        verifier = ParityVerifier(target_qubits=[], verifier_ancilla=LineQubit(0))
        circuit = verifier.validate_parity()
        assert circuit == Circuit()

    def test_valid_cat_state_one_qubit(self):
        qubits = LineQubit.range(1)
        verifier = ParityVerifier(target_qubits=qubits, verifier_ancilla=qubits[0])
        circuit = verifier.validate_parity()

        one_qubit_cat_state = get_cat_state_vector(num_qubits=1)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=one_qubit_cat_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=one_qubit_cat_state,
                                                                        qubit_order=qubits,)
        assert state == StateAndMeasurements(
            state=one_qubit_cat_state,
            measurements={}
        )

    def test_valid_cat_state_two_qubit(self):
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        two_qubit_cat_state = get_cat_state_vector(num_qubits=2)
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(two_qubit_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits,)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([0])}
        )

    def test_invalid_cat_state_two_qubit(self):
        qubits = LineQubit.range(3)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        invalid_cat_state = tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(invalid_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits,)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([1])}
        )

    def test_valid_cat_state_three_qubit(self):
        qubits = LineQubit.range(4)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        three_qubit_cat_state = get_cat_state_vector(num_qubits=3)
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(three_qubit_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([0])}
        )

    def test_invalid_cat_state_three_qubit(self):
        qubits = LineQubit.range(4)
        verifier = ParityVerifier(target_qubits=qubits[:-1], verifier_ancilla=qubits[-1])
        circuit = verifier.validate_parity()

        invalid_three_qubit_cat_state = (
                    (1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
                                     + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)))
        ancilla_state = KET_ZERO_STATE_VECTOR
        initial_state = tensor(invalid_three_qubit_cat_state, ancilla_state)
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)
        state = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                        initial_state=initial_state,
                                                                        qubit_order=qubits)
        assert state == StateAndMeasurements(
            state=initial_state,
            measurements={str(VerificationIsZero().key): array([1])}
        )
