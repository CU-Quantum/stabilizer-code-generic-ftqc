from abc import ABC, abstractmethod
from typing import Optional

from cirq import Circuit, LineQubit, Operation

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_check_matrix import \
    ErrorRecoveryByCheckMatrix
from stim_experiments.error_correcting_codes.support.recovery_combinations_finder import RecoveryCombinationsFinder
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_by_generator_measurement import \
    StateEncoderByGeneratorMeasurement


class StabilizerCode(ErrorCorrectingCode, ABC):
    def __init__(self,
                 check_matrix: CheckMatrix,
                 recovery_combinations_finder: Optional[RecoveryCombinationsFinder] = None,
                 qubits: Optional[list[LineQubit]] = None):
        self._check_matrix = check_matrix
        self._recovery_combinations_finder = recovery_combinations_finder
        if self._recovery_combinations_finder is None:
            self._recovery_combinations_finder = RecoveryCombinationsFinder(max_num_errors=1)
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_logical_qubits=self._check_matrix.num_logical_qubits,
                         qubits=qubits)

    @abstractmethod
    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        pass

    @abstractmethod
    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        pass

    def encode_logical_qubit(self) -> Circuit:
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
        return ErrorRecoveryByCheckMatrix(
            check_matrix=self._check_matrix,
            qubits=self.data_qubits,
            recovery_combinations_finder=self._recovery_combinations_finder
        ).get_error_correction_circuit()
