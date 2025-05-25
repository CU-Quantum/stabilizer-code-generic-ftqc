from stim_experiments.custom_dataclasses.state_encoding import StateEncoding
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_gottesman import StateEncoderGottesman


class StabilizerStandardizedCodeGottesmanEncoding(StabilizerStandardizedCode):
    def encode_logical_qubit(self) -> StateEncoding:
        return StateEncoderGottesman(check_matrix_standardized=self._check_matrix_standardized,
                                     data_qubits=self.data_qubits).get_encoding_circuit()
