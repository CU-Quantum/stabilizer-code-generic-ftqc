from typing import Optional

import pytest
from cirq import Circuit, LineQubit, X, Z
from numpy import array, sqrt

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.error_correcting_codes.support.universal_hadamard_helper import \
    UniversalHadamardHelper
from stim_experiments.error_correcting_codes.universal_hadamard_code.universal_hadamard_code import \
    UniversalHadamardCode
from stim_experiments.singletons.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.singletons.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities import KET_MINUS_STATE_VECTOR, KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, \
    KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR, tensor
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit
from tests.utilities import states_are_equal


class TestUniversalHadamardCodeHelper:

    @pytest.fixture(autouse=True)
    def _setup(self):
        self._set_configuration_to_reduce_ancilla_qubits()
        arbitrary_desired_code = SingleQubit()
        self._universal_hadamard_code = UniversalHadamardCode(num_qubits_in_cat_state=len(arbitrary_desired_code.data_qubits))
        self._num_data_qubits = len(self._universal_hadamard_code.data_qubits)
        self._helper = UniversalHadamardHelper(universal_hadamard_code=self._universal_hadamard_code, desired_encoding=arbitrary_desired_code)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=self._num_data_qubits)

    def _set_configuration_to_reduce_ancilla_qubits(self):
        configuration = ConfigurationErrorCorrectingCodeManager.get_configuration()
        configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
        configuration.measurer_type = MeasurerWithSingleQubit

    def test_puts_zero_into_plus(self):
        circuit = Circuit(
            self._universal_hadamard_code.encode_logical_qubit(),
            self._helper.get_circuit()
        )
        expected_state = tensor(KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        assert self._circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def test_puts_one_into_minus(self):
        circuit = Circuit(
            [X(qubit) for qubit in self._universal_hadamard_code.data_qubits],
            self._universal_hadamard_code.encode_logical_qubit(),
            self._helper.get_circuit()
        )
        expected_state = tensor(KET_MINUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        assert self._circuit_results_in_expected_state(circuit=circuit, expected_state=expected_state)

    def _circuit_results_in_expected_state(self, circuit: Circuit, expected_state: TYPE_STATE_VECTOR):
        utilities = get_error_correcting_code_utilities(state=expected_state)
        simulated_state = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=self._num_data_qubits,
        ).state
        return states_are_equal(simulated_state, expected_state)


class SingleQubit(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None):
        super().__init__(num_data_qubits=1,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        return Circuit()

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit()

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(X(self.data_qubits[0]))
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(Z(self.data_qubits[0]))
        return None
