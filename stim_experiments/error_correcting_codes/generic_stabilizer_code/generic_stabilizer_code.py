from functools import cached_property
from typing import List, Optional

from cirq import Circuit, Gate, H, LineQubit, Operation, X, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToGates, CheckMatrixToOperations
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_generator_measurement import \
    ErrorRecoveryByGeneratorMeasurement
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_by_generator_measurement import \
    StateEncoderByGeneratorMeasurement
from stim_experiments.error_correcting_codes.support.state_encoder.state_encoder_gottesman import StateEncoderGottesman
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class GenericStabilizerCode(ErrorCorrectingCode):
    def __init__(self,
                 generators: TYPE_CHECK_MATRIX,
                 qubits: Optional[list[LineQubit]] = None):
        self._check_matrix = CheckMatrix(matrix=generators)
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_logical_qubits=self._check_matrix.num_logical_qubits,
                         qubits=qubits)

    def encode_logical_qubit(self) -> Circuit:
        phase_corrections = [[self._get_phase_correction(generator_index=generator_index)]
                             for generator_index in range(len(self._generator_operations))]
        return StateEncoderByGeneratorMeasurement(generators=self._generator_operations,
                                                  phase_corrections=phase_corrections).encode_state()

    def _get_phase_correction(self, generator_index: int) -> Operation:
        gate = Z if generator_index < self._check_matrix_standardized.rank_of_pauli_x_portion else X
        return gate(self._get_qubit_at_index(generator_index))

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.H:
            return self._get_logical_hadamard(operation=operation)
        elif operation.gate in [LogicalGateLabel.X, LogicalGateLabel.Z]:
            return self._get_logical_x_or_z(operation=operation)
        return None

    def _get_logical_hadamard(self, operation: LogicalOperation) -> Circuit:
        should_use_transversal = self._check_matrix_standardized.num_logical_qubits == 1
        return self._hadamard_all_data_qubits() if should_use_transversal else self._universal_logical_hadamard(operation)

    def _hadamard_all_data_qubits(self) -> Circuit:
        circuit = Circuit(
            [H(qubit) for qubit in self.data_qubits],
        )
        self._check_matrix_standardized.swap_xs_and_zs()
        return circuit

    def _universal_logical_hadamard(self, operation) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
            logical_operations = (self._get_logical_operation_gates(gate_label=label)
                                  for label in (LogicalGateLabel.X, LogicalGateLabel.Z))
            logical_cx, logical_cz = (
                [gate(self._get_qubit_at_index(qubit_index=qubit_index)).controlled_by(ancilla_qubits[0])
                 for qubit_index, qubit_gates in enumerate(logical_operation[operation.qubit_index])
                 for gate in qubit_gates]
                for logical_operation in logical_operations
            )
            circuit = Circuit(
                H(ancilla_qubits[0]),
                logical_cx,
                logical_cz,
                H(ancilla_qubits[0]),
                logical_cx,
                X(ancilla_qubits[0]),
                logical_cz,
                H(ancilla_qubits[0]),
            )
            return circuit

    def _get_logical_x_or_z(self, operation: LogicalOperation) -> Circuit:
        logical_gates = self._get_logical_operation_gates(gate_label=operation.gate)
        logical_gates_for_qubit = logical_gates[operation.qubit_index]
        circuit = Circuit(
            [gate(self._get_qubit_at_index(qubit_index=qubit_index))
             for qubit_index, qubit_gates in enumerate(logical_gates_for_qubit)
             for gate in qubit_gates]
        )
        return circuit

    def _get_logical_operation_gates(self, gate_label: LogicalGateLabel) -> Optional[List[List[List[Gate]]]]:
        operation_matrix = self._check_matrix_standardized.logical_xs if gate_label is LogicalGateLabel.X else self._check_matrix_standardized.logical_zs
        return CheckMatrixToGates(check_matrix=CheckMatrix(operation_matrix)).get_gates()

    def get_error_correction_circuit(self) -> Circuit:
        return ErrorRecoveryByGeneratorMeasurement(generator_operations=self._generator_operations,
                                                   recoveries=RecoveryFinder(check_matrix=self._check_matrix_standardized).find_recoveries(),
                                                   qubits=self._ordered_qubits).get_error_correction_circuit()

    @cached_property
    def _generator_operations(self) -> list[list[Operation]]:
        return CheckMatrixToOperations(check_matrix=self._check_matrix_standardized, qubits=self._ordered_qubits).get_operations()

    @property
    def _ordered_qubits(self) -> list[LineQubit]:
        return [self._get_qubit_at_index(qubit_index=qubit_index) for qubit_index in range(self._check_matrix.num_physical_qubits)]

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self.data_qubits[qubit_index]

    @cached_property
    def _check_matrix_standardized(self) -> CheckMatrixStandardized:
        standardizer = CheckMatrixStandardizer(check_matrix=self._check_matrix)
        return standardizer.get_standardized_matrix()

    @property
    def _num_ancilla_qubits(self) -> int:
        return len(self._check_matrix.matrix)


class GenericStabilizerCodeGottesmanEncoding(GenericStabilizerCode):
    def encode_logical_qubit(self) -> Circuit:
        return StateEncoderGottesman(check_matrix_standardized=self._check_matrix_standardized,
                                     data_qubits=self.data_qubits).get_encoding_circuit()
