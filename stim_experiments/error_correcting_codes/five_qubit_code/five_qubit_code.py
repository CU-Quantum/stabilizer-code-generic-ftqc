from lib2to3.pgen2.grammar import opmap_raw
from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_generator_measurement import \
    ErrorRecoveryByGeneratorMeasurement
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_by_generator_measurement import \
    StateEncoderByGeneratorMeasurement
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_5_qubit


class FiveQubitCode(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None):
        self._check_matrix = CheckMatrix(matrix=get_check_matrix_values_5_qubit())
        super().__init__(num_data_qubits=5,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        phase_corrections = [self._get_phase_corrections(generator_index=generator_index)
                             for generator_index in range(len(self._check_matrix.matrix))]
        return StateEncoderByGeneratorMeasurement(
            check_matrix=self._check_matrix,
            phase_corrections=phase_corrections,
            qubits=self.data_qubits
        ).encode_state()

    def _get_phase_corrections(self, generator_index: int) -> list[Operation]:
        qubits_indices_to_flip_per_generator = [(0, 2), (0, 1, 2, 3), (0, 1, 3, 4), (1, 4)]
        qubits_indices_to_flip = qubits_indices_to_flip_per_generator[generator_index]
        return [Z(self.data_qubits[qubit_index]) for qubit_index in qubits_indices_to_flip]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.Z:
            return Circuit(Z(qubit) for qubit in self.data_qubits)
        if operation.gate == LogicalGateLabel.X:
            return Circuit(X(qubit) for qubit in self.data_qubits)
        return None

    def get_error_correction_circuit(self) -> Circuit:
        return ErrorRecoveryByGeneratorMeasurement(
            check_matrix=self._check_matrix,
            qubits=self.data_qubits
        ).get_error_correction_circuit()
