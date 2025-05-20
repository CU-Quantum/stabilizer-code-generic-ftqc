from abc import ABC, abstractmethod
from typing import Optional

from cirq import Circuit, LineQubit, MeasurementKey, Operation, X, Z

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.custom_dataclasses.state_encoding import StateEncoding
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_generator_measurement import \
    ErrorRecoveryByGeneratorMeasurement
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_by_generator_measurement import \
    StateEncoderByGeneratorMeasurement


class StabilizerCode(ErrorCorrectingCode, ABC):
    def __init__(self, check_matrix: CheckMatrix, qubits: Optional[list[LineQubit]] = None):
        self._check_matrix = check_matrix
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_logical_qubits=self._check_matrix.num_logical_qubits,
                         qubits=qubits)

    @abstractmethod
    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        pass

    @abstractmethod
    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass

    def encode_logical_qubit(self) -> StateEncoding:
        phase_corrections = [
            self._get_anticommuter_for_generator(generator_index=generator_index)
            for generator_index in range(len(self._check_matrix.matrix))
        ]
        return StateEncoderByGeneratorMeasurement(
            check_matrix=self._check_matrix,
            phase_corrections=phase_corrections,
            qubits=self.data_qubits,
        ).encode_state()

    def get_error_correction_circuit(self) -> Circuit:
        return ErrorRecoveryByGeneratorMeasurement(
            check_matrix=self._check_matrix,
            qubits=self.data_qubits
        ).get_error_correction_circuit()


