from functools import cached_property
from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToOperations
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder
from stim_experiments.error_correcting_codes.support.fault_tolerant_error_correction.fault_tolerant_error_correction import \
    FaultTolerantErrorCorrection
from stim_experiments.error_correcting_codes.support.fault_tolerant_state_encoder.fault_tolerant_state_encoder import \
    FaultTolerantStateEncoder
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode


class UniversalHadamardCode(ErrorCorrectingCode):
    num_cats = ThreeCatCode.num_cats

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        num_data_qubits = num_qubits_in_cat_state * self.num_cats
        num_parity_checks_per_register = num_qubits_in_cat_state - 1
        x_stabilizers = [
            [0] * num_data_qubits + [self._qubit_has_x_stabilizer_in_generator(cat_index=cat_index,
                                                                               parity_check_index=parity_check_index,
                                                                               qubit_index=qubit_index)
                                     for qubit_index in range(num_data_qubits)]
            for cat_index in range(self.num_cats)
            for parity_check_index in range(num_parity_checks_per_register)
        ]
        z_stabilizers = [
            [int(cat_index * self._num_qubits_in_cat_state <= qubit_index < (cat_index + 2) * self._num_qubits_in_cat_state)
             for qubit_index in range(num_data_qubits)] + [0] * num_data_qubits
            for cat_index in range(self.num_cats - 1)
        ]
        self._check_matrix = CheckMatrix(matrix=array(x_stabilizers + z_stabilizers))
        super().__init__(num_data_qubits=self._num_qubits_in_cat_state * self.num_cats,
                         num_logical_qubits=1,
                         qubits=qubits)

    def _qubit_has_x_stabilizer_in_generator(self, cat_index: int, parity_check_index: int, qubit_index: int) -> int:
        low_index = cat_index * self._num_qubits_in_cat_state + parity_check_index
        high_index = low_index + 1
        return int(low_index <= qubit_index <= high_index)

    def encode_logical_qubit(self) -> Circuit:
        phase_corrections = [self._get_phase_correction(generator_index=generator_index)
                             for generator_index in range(len(self._generator_operations))]
        return FaultTolerantStateEncoder(generators=self._generator_operations,
                                         phase_corrections=phase_corrections).encode_state()

    def _get_phase_correction(self, generator_index: int) -> list[Operation]:
        is_x_stabilizer = generator_index < len(self._generator_operations) - 2
        if is_x_stabilizer:
            num_checks_per_register = self._num_qubits_in_cat_state - 1
            register_index = generator_index // num_checks_per_register
            start_index = register_index * self._num_qubits_in_cat_state
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == len(self._generator_operations) - 1
            return [Z(self.data_qubits[0 - is_last_generator])]

    def get_error_correction_circuit(self) -> Circuit:
        return FaultTolerantErrorCorrection(generator_operations=self._generator_operations,
                                            recoveries=RecoveryFinder(check_matrix=self._check_matrix).find_recoveries(),
                                            qubits=self.data_qubits).get_error_correction_circuit()

    @cached_property
    def _generator_operations(self) -> list[list[Operation]]:
        return CheckMatrixToOperations(check_matrix=self._check_matrix, qubits=self.data_qubits).get_operations()

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_in_cat_state)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(self.num_cats)],
            )
        return None

    @cached_property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                for i in range(self.num_cats)]
