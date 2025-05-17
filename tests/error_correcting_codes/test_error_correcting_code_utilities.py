import pytest
from cirq import Circuit, LineQubit, M, X
from numpy import array

from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


class TestErrorCorrectingCodeUtilities:
    @pytest.mark.parametrize('initial_state', [
        KET_ZERO_STATE_VECTOR, KET_ZERO_DENSITY_MATRIX
    ])
    def test_multiple_measurements_on_same_qubit_only_uses_last_one(self, initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX):
        initial_state = KET_ZERO_STATE_VECTOR
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)

        num_qubits = 1
        qubit = LineQubit(num_qubits)
        circuit = Circuit(
            M(qubit),
            X(qubit),
            M(qubit),
            X(qubit),
        )

        result = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                         num_data_qubits=num_qubits,
                                                                         initial_data_state=initial_state)
        assert result == StateAndMeasurements(
            state=initial_state,
            measurements={'q(1)': array([1])}
        )

    @pytest.mark.parametrize('initial_state', [
        tensor(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR),
        tensor(KET_ZERO_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX)
    ])
    def test_measurements_on_different_qubits(self, initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX):
        error_correcting_code_utilities = get_error_correcting_code_utilities(state=initial_state)

        qubits = LineQubit.range(2)
        circuit = Circuit(
            X(qubits[1]),
            M(qubits[0]),
            M(qubits[1]),
            X(qubits[1]),
        )

        result = error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                         num_data_qubits=len(qubits),
                                                                         initial_data_state=initial_state)
        assert result == StateAndMeasurements(
            state=initial_state,
            measurements={'q(0)': array([0]), 'q(1)': [1]}
        )
