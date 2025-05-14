from cirq import LineQubit

from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.universal_hadamard_code.support.universal_hadamard_code_helper import \
    UniversalHadamardCodeHelper, UniversalHadamardCodeHelperContext
from stim_experiments.error_correcting_codes.universal_hadamard_code.universal_hadamard_code import \
    UniversalHadamardCode
from stim_experiments.utilities import FreshAncillasPool


class TestUniversalHadamardCodeHelper:
    def test_use_fresh_ancilla_qubits(self):
        arbitrary_num_qubits_in_cat_state = 5
        code = UniversalHadamardCode(num_qubits_in_cat_state=arbitrary_num_qubits_in_cat_state)
        universal_hadamard_code_helper = UniversalHadamardCodeHelper(code=code)
        FreshAncillasPool().set_first_ancilla_num(len(code.data_qubits))

        expected_helper_codes = [
            UniversalHadamardCode(num_qubits_in_cat_state=arbitrary_num_qubits_in_cat_state,
                                  qubits=LineQubit.range(15, 30)),
            UniversalHadamardCode(num_qubits_in_cat_state=arbitrary_num_qubits_in_cat_state,
                                  qubits=LineQubit.range(30, 45)),
        ]
        with universal_hadamard_code_helper.use_fresh_ancilla_qubits() as universal_hadamard_code_helper_context:
            assert universal_hadamard_code_helper_context == UniversalHadamardCodeHelperContext(
                ancilla_qubits=LineQubit.range(15, 45),
                helper_codes=expected_helper_codes,
                all_universal_hadamard_codes=[code, *expected_helper_codes],
                helper_3cat=ThreeCatCode(num_qubits_in_cat_state=15, qubits=LineQubit.range(45)),
            )
