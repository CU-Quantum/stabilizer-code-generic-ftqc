from functools import cached_property
from typing import List, Optional

from cirq import Circuit, LineQubit, M, R, X
from numpy import sqrt

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import ErrorCorrectingCodeUtilities, \
    get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ONE_DENSITY_MATRIX, KET_ONE_STATE_VECTOR, KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


class PairityVerifier:
    def __init__(self,
                 cat_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX,
                 state_qubits: List[LineQubit],
                 ancilla_qubit: Optional[LineQubit] = None):
        self._cat_state = cat_state
        self._state_qubits = state_qubits
        self._ancilla_qubit = ancilla_qubit if ancilla_qubit else LineQubit(self._num_qubits)

    def is_valid_cat_state(self) -> bool:
        num_qubits = len(self._state_qubits)
        for i in range(num_qubits - 1):
            circuit = Circuit(
                X(self._ancilla_qubit).controlled_by(self._state_qubits[i]),
                X(self._ancilla_qubit).controlled_by(self._state_qubits[i + 1]),
                M(self._ancilla_qubit),
                R(self._ancilla_qubit),
            )
            state = self._get_state_after_circuit(circuit=circuit)
            measurement = list(state.measurements.values())[0][0]
            if measurement != 0:
                return False
        return True

    def _get_state_after_circuit(self, circuit: Circuit) -> StateAndMeasurements:
        if self._ancilla_qubit in self._state_qubits:
            return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                 qubit_order=self._state_qubits,
                                                                                 initial_state=self._cat_state)
        else:
            state_with_new_ancilla = tensor(self._cat_state, self._error_correcting_code_utilities.zero_state)
            return self._error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                 qubit_order=self._state_qubits + [self._ancilla_qubit],
                                                                                 initial_state=state_with_new_ancilla)

    @cached_property
    def _error_correcting_code_utilities(self) -> ErrorCorrectingCodeUtilities:
        return get_error_correcting_code_utilities(state=self._cat_state)

    @property
    def _num_qubits(self) -> int:
        return len(self._state_qubits)


class TestCatStateVerifier:
    def test_valid_cat_state_two_qubit(self):
        two_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                               + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        qubits = LineQubit.range(2)
        verifier = PairityVerifier(cat_state=two_qubit_cat_state, state_qubits=qubits)
        assert verifier.is_valid_cat_state()

    def test_invalid_cat_state_two_qubit(self):
        invalid_cat_state = ((1 / sqrt(2)) * tensor(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR))
        qubits = LineQubit.range(2)
        verifier = PairityVerifier(cat_state=invalid_cat_state, state_qubits=qubits)
        assert not verifier.is_valid_cat_state()

    def test_valid_cat_state_three_qubit(self):
        three_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                 + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        qubits = LineQubit.range(3)
        verifier = PairityVerifier(cat_state=three_qubit_cat_state, state_qubits=qubits)
        assert verifier.is_valid_cat_state()

    def test_invalid_cat_state_three_qubit(self):
        three_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR)
                                 + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)))
        qubits = LineQubit.range(3)
        verifier = PairityVerifier(cat_state=three_qubit_cat_state, state_qubits=qubits)
        assert not verifier.is_valid_cat_state()

    def test_can_provide_ancilla_qubit(self):
        two_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                                 + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        bad_ancilla_state = KET_ONE_STATE_VECTOR
        two_qubit_cat_state_with_bad_ancilla = tensor(two_qubit_cat_state, bad_ancilla_state)
        qubits = LineQubit.range(3)
        verifier = PairityVerifier(cat_state=two_qubit_cat_state_with_bad_ancilla,
                                   state_qubits=qubits,
                                   ancilla_qubit=qubits[-1])
        assert not verifier.is_valid_cat_state()

    def test_can_provide_ancilla_outside_state(self):
        two_qubit_cat_state = ((1 / sqrt(2)) * (tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
                               + tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)))
        qubits = LineQubit.range(2)
        verifier = PairityVerifier(cat_state=two_qubit_cat_state,
                                   state_qubits=qubits,
                                   ancilla_qubit=LineQubit(len(qubits)))
        assert verifier.is_valid_cat_state()

    def test_can_use_density_matrix(self):
        two_qubit_cat_state = (.5 * (tensor(KET_ZERO_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX)
                               + tensor(KET_ONE_DENSITY_MATRIX, KET_ONE_DENSITY_MATRIX)))
        qubits = LineQubit.range(2)
        verifier = PairityVerifier(cat_state=two_qubit_cat_state, state_qubits=qubits)
        assert verifier.is_valid_cat_state()
