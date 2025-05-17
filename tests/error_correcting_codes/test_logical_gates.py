from dataclasses import dataclass

import pytest
from cirq import Circuit, LineQubit, X
from numpy import allclose, sqrt

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from tests.error_correcting_codes.expected_states.expected_states import ExpectedStates
from tests.error_correcting_codes.generic_stabilizer_code.expected_states_generic_5_qubit import \
    ExpectedStatesGenericFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit
from tests.error_correcting_codes.universal_hadamard_code.expected_states_universal_hadamard import \
    ExpectedStatesThreeCatSubregisterParity


@dataclass
class ParametersForLogicalGatesTest:
    code: ErrorCorrectingCode
    expected_states: ExpectedStates


PARAMETERS = {
    "ThreeCatSubregisterParityCode": ParametersForLogicalGatesTest(
        code=ThreeCatSubregisterParityCode(num_qubits_in_cat_state=ExpectedStatesThreeCatSubregisterParity().arbitrary_num_qubits),
        expected_states=ExpectedStatesThreeCatSubregisterParity(),
    ),
    "GenericStabilizerCodeFiveQubit": ParametersForLogicalGatesTest(
        code=GenericStabilizerCode(generators=get_check_matrix_values_5_qubit()),
        expected_states=ExpectedStatesGenericFiveQubit()
    ),
}


PARAMETERS_FLATTENED = [pytest.param(parameters, id=name) for name, parameters in PARAMETERS.items()]


class TestLogicalGates:
    @pytest.fixture(autouse=True, params=PARAMETERS_FLATTENED)
    def _setup(self, request):
        self._parameters: ParametersForLogicalGatesTest = request.param
        self._num_data_qubits = len(self._parameters.code.data_qubits)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(self._parameters.code.data_qubits))

    def test_logical_x(self):
        target_index = self._parameters.code.num_logical_qubits - 1
        operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=target_index)
        circuit = Circuit(
            self._parameters.code.encode_logical_qubit(),
            self._parameters.code.get_operation_circuit(operation=operation)
        )

        initial_data_state = self._parameters.expected_states.get_logical_zero_state_vector()
        utilities = get_error_correcting_code_utilities(state=initial_data_state)
        current_state = utilities.get_state_after_circuit(circuit=circuit,
                                                          num_data_qubits=self._num_data_qubits,
                                                          initial_data_state=initial_data_state)
        expected_state = self._parameters.expected_states.get_logical_one_state_vector()
        assert allclose(current_state.state, expected_state)

    def test_logical_z(self):
        target_index = self._parameters.code.num_logical_qubits - 1
        operation = LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=target_index)
        circuit = Circuit(
            self._parameters.code.encode_logical_qubit(),
            self._parameters.code.get_operation_circuit(operation=operation)
        )
        initial_data_state = (1 / sqrt(2)) * (
            self._parameters.expected_states.get_logical_zero_state_vector()
            + self._parameters.expected_states.get_logical_one_state_vector()
        )
        utilities = get_error_correcting_code_utilities(state=initial_data_state)
        current_state = utilities.get_state_after_circuit(circuit=circuit,
                                                          num_data_qubits=self._num_data_qubits,
                                                          initial_data_state=initial_data_state)
        expected_state = (1 / sqrt(2)) * (
            self._parameters.expected_states.get_logical_zero_state_vector()
            - self._parameters.expected_states.get_logical_one_state_vector()
        )
        assert allclose(current_state.state, expected_state)
