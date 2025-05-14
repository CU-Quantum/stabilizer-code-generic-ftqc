import pytest
from cirq import Circuit, LineQubit, X, Z
from numpy import array, sqrt

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
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, tensor
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit
from tests.utilities import states_are_equal


class TestUniversalHadamardCodeHelper:
    # @pytest.fixture(autouse=True)
    # def _setup(self):
    #     arbitrary_num_qubits_in_cat_state = 2
    #     self._main_code = UniversalHadamardCode(num_qubits_in_cat_state=arbitrary_num_qubits_in_cat_state)
    #     self._universal_hadamard_code_helper = UniversalHadamardHelper(code=self._main_code)
    #     self._num_qubits_in_cat_state = arbitrary_num_qubits_in_cat_state
    #     FreshAncillasPool().set_first_ancilla_num(len(self._main_code.data_qubits))

    @pytest.fixture(autouse=True)
    def _set_configuration_to_reduce_ancilla_qubits(self):
        configuration = ConfigurationErrorCorrectingCodeManager.get_configuration()
        configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
        configuration.measurer_type = MeasurerWithSingleQubit
        # TODO include FaultTolerantStateEncoder and possibly FaultTolerantErrorCorrection

    def test_puts_zero_into_plus(self):
        arbitrary_desired_code = GenericStabilizerCode(generators=array([
            [0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 1, 1],
        ]))
        universal_hadamard_code = UniversalHadamardCode(num_qubits_in_cat_state=len(arbitrary_desired_code.data_qubits))
        num_data_qubits = len(universal_hadamard_code.data_qubits)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=num_data_qubits)

        helper = UniversalHadamardHelper(universal_hadamard_code=universal_hadamard_code, desired_encoding=arbitrary_desired_code)
        circuit = helper.get_circuit()

        utilities = get_error_correcting_code_utilities(state=KET_ZERO_STATE_VECTOR)
        simulated_state = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=num_data_qubits,
        ).state
        expected_state = (1 / sqrt(2)) * (tensor(*[KET_ZERO_STATE_VECTOR] * 3) + tensor(*[KET_ONE_STATE_VECTOR] * 3))
        assert states_are_equal(simulated_state, expected_state)


    # def test_use_fresh_ancilla_qubits(self):
    #     expected_helper_codes = [
    #         UniversalHadamardCode(num_qubits_in_cat_state=self._num_qubits_in_cat_state,
    #                               qubits=LineQubit.range(6, 12)),
    #         UniversalHadamardCode(num_qubits_in_cat_state=self._num_qubits_in_cat_state,
    #                               qubits=LineQubit.range(12, 18)),
    #     ]
    #     with self._universal_hadamard_code_helper.use_fresh_ancilla_qubits() as universal_hadamard_code_helper_context:
    #         assert universal_hadamard_code_helper_context == UniversalHadamardHelperContext(
    #             ancilla_qubits=LineQubit.range(6, 18),
    #             helper_codes=expected_helper_codes,
    #             all_universal_hadamard_codes=[self._main_code, *expected_helper_codes],
    #             helper_3cat=ThreeCatCode(num_qubits_in_cat_state=6, qubits=LineQubit.range(18)),
    #         )
    #
    # def test_encode_helper_registers(self):
    #     arbitrary_num_codes = 2
    #
    #     codes = [UniHCodeStub(num_qubits_in_cat_state=1, id_index=i) for i in range(arbitrary_num_codes)]
    #     operations = self._universal_hadamard_code_helper.encode_helper_registers(codes=codes)
    #     expected_circuit = Circuit(X(LineQubit(i)) for i in range(arbitrary_num_codes))
    #     assert list(Circuit(operations).all_operations()) == list(expected_circuit.all_operations())
    #
    # def test_correct_codes(self):
    #     arbitrary_num_codes = 2
    #
    #     codes = [UniHCodeStub(num_qubits_in_cat_state=1, id_index=i) for i in range(arbitrary_num_codes)]
    #     operations = self._universal_hadamard_code_helper.correct_codes(codes=codes)
    #     expected_circuit = Circuit(Z(LineQubit(i)) for i in range(arbitrary_num_codes))
    #     assert list(Circuit(operations).all_operations()) == list(expected_circuit.all_operations())
    #
    # def test_reset_ancilla_qubits(self):
    #     arbitrary_num_qubits = 2
    #
    #     ancillas = LineQubit.range(arbitrary_num_qubits)
    #     operations = self._universal_hadamard_code_helper.reset_ancilla_qubits(ancilla_qubits=ancillas)
    #     expected_circuit = Circuit(R(ancilla) for ancilla in ancillas)
    #     assert list(Circuit(operations).all_operations()) == list(expected_circuit.all_operations())
    #
    # def test_cx_data_to_helpers(self):
    #     with self._universal_hadamard_code_helper.use_fresh_ancilla_qubits() as universal_hadamard_code_helper_context:
    #         self._universal_hadamard_code_helper.cx_data_to_helpers(codes=universal_hadamard_code_helper_context.all_universal_hadamard_codes
    #                                                                 )


class UniHCodeStub(UniversalHadamardCode):
    _id_index = 0

    def __init__(self, num_qubits_in_cat_state: int, id_index: int):
        super().__init__(num_qubits_in_cat_state=num_qubits_in_cat_state)
        self._id_index = id_index

    def encode_logical_qubit(self) -> Circuit:
        return Circuit(X(LineQubit(self._id_index)))

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit(Z(LineQubit(self._id_index)))

