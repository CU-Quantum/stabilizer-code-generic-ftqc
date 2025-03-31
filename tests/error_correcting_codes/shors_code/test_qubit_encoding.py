from functools import cached_property
from typing import List

from cirq import CX, Circuit, H, LineQubit, X, density_matrix_from_state_vector
from numpy.ma.core import allclose

from stim_experiments.error_correcting_codes.shors_code.test_qubit_encoding import ShorsRepetitionCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX


class TestLogicalState:
    def test_logical_zero(self):
        assert self._encoding_matches_expected(initial_state=KET_ZERO_DENSITY_MATRIX, expected_state=self._expected_state_zero)

    def test_logical_one(self):
        assert self._encoding_matches_expected(initial_state=KET_ONE_DENSITY_MATRIX, expected_state=self._expected_state_one)

    @staticmethod
    def _encoding_matches_expected(initial_state: DENSITY_MATRIX_TYPE, expected_state: DENSITY_MATRIX_TYPE) -> DENSITY_MATRIX_TYPE:
        code = ShorsRepetitionCode(initial_qubit_state_density_matrix=initial_state)
        current_state = code.get_current_state()
        return allclose(current_state, expected_state, atol=1e-14)

    @property
    def _expected_state_zero(self) -> DENSITY_MATRIX_TYPE:
        circuit = self._get_logical_zero_circuit()
        return self._get_expected_state(circuit)

    @property
    def _expected_state_one(self) -> DENSITY_MATRIX_TYPE:
        circuit = self._get_logical_zero_circuit()
        circuit.insert(0, X(self._circuit_qubits[0]))
        return self._get_expected_state(circuit)

    def _get_logical_zero_circuit(self) -> Circuit:
        qubits = self._circuit_qubits
        return Circuit(
            CX(qubits[0], qubits[3]),
            CX(qubits[0], qubits[6]),
            H(qubits[0]),
            H(qubits[3]),
            H(qubits[6]),
            CX(qubits[0], qubits[1]),
            CX(qubits[0], qubits[2]),
            CX(qubits[3], qubits[4]),
            CX(qubits[3], qubits[5]),
            CX(qubits[6], qubits[7]),
            CX(qubits[6], qubits[8]),
        )

    @staticmethod
    def _get_expected_state(circuit: Circuit) -> DENSITY_MATRIX_TYPE:
        expected_state = circuit.final_state_vector()
        return density_matrix_from_state_vector(expected_state)

    @cached_property
    def _circuit_qubits(self) -> List[LineQubit]:
        return LineQubit.range(9)

