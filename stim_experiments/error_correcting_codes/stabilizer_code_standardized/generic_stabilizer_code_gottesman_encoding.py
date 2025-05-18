from cirq import Circuit

from stim_experiments.error_correcting_codes.stabilizer_code_standardized.code_standardized_standardized import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_gottesman import StateEncoderGottesman


class GenericStabilizerCodeGottesmanEncoding(GenericStabilizerCode):
    def encode_logical_qubit(self) -> Circuit:
        return StateEncoderGottesman(check_matrix_standardized=self._check_matrix_standardized,
                                     data_qubits=self.data_qubits).get_encoding_circuit()
