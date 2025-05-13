from stim_experiments.error_correcting_codes.universal_hadamard_code.support.universal_hadamard_code_helper import \
    UniversalHadamardCodeHelper
from stim_experiments.error_correcting_codes.universal_hadamard_code.universal_hadamard_code import \
    UniversalHadamardCode


class TestUniversalHadamardCodeHelper:
    def test_something(self):
        code = UniversalHadamardCode(num_qubits_in_cat_state=3)
        UniversalHadamardCodeHelper(code=code)
