from typing import Optional

from cirq import Circuit, LineQubit, MeasurementKey, Operation, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.state_encoding import StateEncoding
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_generator_measurement import \
    ErrorRecoveryByGeneratorMeasurement
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_by_generator_measurement import \
    StateEncoderByGeneratorMeasurement
from stim_experiments.utilities.repetition_z_stabilizers_generator import RepetitionZStabilizersGenerator


class RepetitionCode(ErrorCorrectingCode):
    def __init__(self, num_qubits: int, qubits: Optional[list[LineQubit]] = None):
        self._check_matrix = None
        if num_qubits >= 3:
            z_stabilizers = [
                [0] * num_qubits + z_stabilizer
                for z_stabilizer in RepetitionZStabilizersGenerator(num_qubits=num_qubits).get_stabilizers()
            ]
            self._check_matrix = CheckMatrix(matrix=array(z_stabilizers))
        super().__init__(num_data_qubits=num_qubits,
                         num_logical_qubits=1,
                         qubits=qubits)

    def encode_logical_qubit(self) -> StateEncoding:
        if self._check_matrix is None:
            return StateEncoding(
                circuit=Circuit()
            )
        phase_corrections = [
            self._get_anticommuter_for_generator(generator_index=generator_index)
            for generator_index in range(len(self._check_matrix.matrix))
        ]
        return StateEncoderByGeneratorMeasurement(
            check_matrix=self._check_matrix,
            phase_corrections=phase_corrections,
            qubits=self.data_qubits,
        ).encode_state()

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        return [X(self.data_qubits[qubit_index]) for qubit_index in range(generator_index + 1)]

    def get_error_correction_circuit(self) -> Circuit:
        if self._check_matrix is None:
            return Circuit()
        return ErrorRecoveryByGeneratorMeasurement(
            check_matrix=self._check_matrix,
            qubits=self.data_qubits
        ).get_error_correction_circuit()

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.Z:
            return Circuit(Z(self.data_qubits[0]))
        if operation.gate == LogicalGateLabel.X:
            return Circuit(X(qubit) for qubit in self.data_qubits)
        return None
