import pytest
from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, LineQubit, X, Z
from numpy import allclose, log2

from stim_experiments.error_correcting_codes.shors_code.shors_repetition_code import ShorsRepetitionCode
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX
from tests.error_correcting_codes.shors_code.expected_states_shor import ExpectedStatesShor


class TestCorrections:
    _expected_states_utilities = ExpectedStatesShor()
    _qubit_indices_in_different_positions_in_different_blocks = [0, 4, 8]

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_bit_flip_error_is_correctly_applied(self, qubit_index: int):
        assert self._state_matches_expected_after_error(error_gate=X, qubit_index=qubit_index)

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_phase_flip_error_is_correctly_applied(self, qubit_index: int):
        assert self._state_matches_expected_after_error(error_gate=Z, qubit_index=qubit_index)

    def _state_matches_expected_after_error(self, error_gate: Gate, qubit_index: int) -> bool:
        code = ShorsRepetitionCode(initial_qubit_state_density_matrix=KET_ZERO_DENSITY_MATRIX)
        code.apply_gate(error_gate, qubit_index=qubit_index)
        current_state = code.get_current_state()

        initial_state = self._expected_states_utilities.get_logical_zero_density_matrix()
        num_qubits = int(log2(initial_state.shape[0]))
        qubits = LineQubit.range(num_qubits)
        circuit = Circuit(
            error_gate(qubits[qubit_index])
        )
        simulation: DensityMatrixTrialResult = DensityMatrixSimulator().simulate(circuit,
                                                                                 qubit_order=qubits,
                                                                                 initial_state=initial_state)
        expected_state = simulation.final_density_matrix

        return allclose(current_state, expected_state, atol=1e-7)

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_bit_flip_error_is_corrected(self, qubit_index: int):
        code = ShorsRepetitionCode(initial_qubit_state_density_matrix=KET_ZERO_DENSITY_MATRIX)
        code.apply_gate(X, qubit_index=qubit_index)
        code.correct_errors()
        current_state = code.get_current_state()

        expected_state = self._expected_states_utilities.get_logical_zero_density_matrix()
        assert allclose(current_state, expected_state, atol=1e-7)

    @pytest.mark.parametrize('qubit_index', _qubit_indices_in_different_positions_in_different_blocks)
    def test_phase_flip_error_is_corrected(self, qubit_index: int):
        code = ShorsRepetitionCode(initial_qubit_state_density_matrix=KET_ZERO_DENSITY_MATRIX)
        code.apply_gate(Z, qubit_index=qubit_index)
        code.correct_errors()
        current_state = code.get_current_state()

        expected_state = self._expected_states_utilities.get_logical_zero_density_matrix()
        assert allclose(current_state, expected_state, atol=1e-7)
