from functools import cached_property
from typing import List, Optional

from cirq import Circuit, Gate, H, LineQubit, Operation, X, Z

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from stim_experiments.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.error_correcting_codes.support.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from stim_experiments.error_correcting_codes.support.check_matrix_to_gates import CheckMatrixToGates
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class CodeStabilizerStandardized(StabilizerCode):
    def __init__(self,
                 generators: TYPE_CHECK_MATRIX,
                 qubits: Optional[list[LineQubit]] = None):
        self._check_matrix = CheckMatrix(matrix=generators)
        super().__init__(check_matrix=self._check_matrix_standardized, qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        gate = Z if generator_index < self._check_matrix_standardized.rank_of_pauli_x_portion else X
        return [gate(self._ordered_qubits[generator_index])]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.H:
            return self._universal_logical_hadamard(operation=operation)
        elif operation.gate in [LogicalGateLabel.X, LogicalGateLabel.Z]:
            return self._get_logical_x_or_z(operation=operation)
        return None

    def _universal_logical_hadamard(self, operation) -> Circuit:
        # TODO turn this into a non-ft strategy
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            ancilla_qubit = ancilla_qubits[0]
            logical_operations = (self._get_logical_operation_gates(gate_label=label)
                                  for label in (LogicalGateLabel.X, LogicalGateLabel.Z))
            logical_cx, logical_cz = (
                [gate(self._get_qubit_at_index(qubit_index=qubit_index)).controlled_by(ancilla_qubit)
                 for qubit_index, qubit_gates in enumerate(logical_operation[operation.qubit_index])
                 for gate in qubit_gates]
                for logical_operation in logical_operations
            )
            circuit = Circuit(
                H(ancilla_qubit),
                logical_cx,
                logical_cz,
                H(ancilla_qubit),
                logical_cx,
                X(ancilla_qubit),
                logical_cz,
                H(ancilla_qubit),
            )
            return circuit

    def _get_logical_x_or_z(self, operation: LogicalOperation) -> Circuit:
        if operation.gate in [LogicalGateLabel.X, LogicalGateLabel.Z]:
            logical_gates = self._get_logical_operation_gates(gate_label=operation.gate)
            logical_gates_for_qubit = logical_gates[operation.qubit_index]
            circuit = Circuit(
                [gate(self._ordered_qubits[qubit_index])
                 for qubit_index, qubit_gates in enumerate(logical_gates_for_qubit)
                 for gate in qubit_gates]
            )
            return circuit
        return None

    def _get_logical_operation_gates(self, gate_label: LogicalGateLabel) -> Optional[List[List[List[Gate]]]]:
        operation_matrix = self._check_matrix_standardized.logical_xs if gate_label is LogicalGateLabel.X else self._check_matrix_standardized.logical_zs
        return CheckMatrixToGates(check_matrix=CheckMatrix(operation_matrix)).get_gates()

    @cached_property
    def _check_matrix_standardized(self) -> CheckMatrixStandardized:
        standardizer = CheckMatrixStandardizer(check_matrix=self._check_matrix)
        return standardizer.get_standardized_matrix()

    @property
    def _ordered_qubits(self) -> list[LineQubit]:
        return [self._get_qubit_at_index(qubit_index=qubit_index) for qubit_index in range(self._check_matrix.num_physical_qubits)]

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self.data_qubits[qubit_index]
