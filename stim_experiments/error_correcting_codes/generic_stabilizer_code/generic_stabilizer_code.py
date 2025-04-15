from functools import cached_property
from typing import List, Optional

from cirq import Circuit, Gate, H, KET_ZERO, LineQubit, R, X, Z, kron
from numpy import array, log2

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.logical_qubit_encoder import \
    LogicalQubitEncoder
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToGates
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder
from stim_experiments.simulators.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import TYPE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX, binary_array_to_int, partial_trace


class GenericStabilizerCode(ErrorCorrectingCode):
    def __init__(self,
                 generators: TYPE_CHECK_MATRIX,
                 initial_logical_qubit_state_density_matrix: Optional[TYPE_DENSITY_MATRIX] = None):
        self._check_matrix = CheckMatrix(matrix=generators)
        if initial_logical_qubit_state_density_matrix is None:
            initial_logical_qubit_state_density_matrix = kron(*[KET_ZERO_DENSITY_MATRIX] * self._check_matrix.num_logical_qubits)
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_ancilla_qubits=len(self._check_matrix.matrix),
                         initial_logical_qubit_state_density_matrix=initial_logical_qubit_state_density_matrix)
        self._generators = generators

    def _encode_logical_qubit(self) -> None:
        self._validate_initial_logical_state_size()
        self._initialize_logical_state()
        circuit = self._get_encoding_circuit()
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _validate_initial_logical_state_size(self) -> None:
        num_qubits_in_initial_logical_state = int(log2(self._initial_logical_qubit_state_density_matrix.shape[0]))
        if num_qubits_in_initial_logical_state != self._check_matrix.num_logical_qubits:
            raise ValueError(f"These generators encode {self._check_matrix.num_logical_qubits} logical qubits, but an initial state of {num_qubits_in_initial_logical_state} was given.")

    def _initialize_logical_state(self) -> None:
        data_state = kron(*[KET_ZERO_DENSITY_MATRIX] * (self._num_data_qubits - self._check_matrix.num_logical_qubits),
                          self._initial_logical_qubit_state_density_matrix)
        ancilla_state = kron(*[KET_ZERO_DENSITY_MATRIX] * self._num_ancilla_qubits)
        self._current_state = kron(data_state, ancilla_state)

    def _get_encoding_circuit(self) -> Circuit:
        return LogicalQubitEncoder(check_matrix_standardized=self._check_matrix_standardized,
                                   data_qubits=self.data_qubits).get_encoding_circuit()

    def apply_operation(self, operation: LogicalOperation) -> None:
        if operation.gate == LogicalGateLabel.H:
            logical_xs, logical_zs = (
            self._get_logical_operation_gates(operation=LogicalOperation(label, qubit_index=operation.qubit_index))
            for label in (LogicalGateLabel.X, LogicalGateLabel.Z))

            logical_cz = [gate(self._get_qubit_at_index(qubit_index=qubit_index)).controlled_by(self.ancilla_qubits[0])
                 for qubit_index, qubit_gates in enumerate(logical_zs[operation.qubit_index])
                 for gate in qubit_gates]
            logical_cx = [gate(self._get_qubit_at_index(qubit_index=qubit_index)).controlled_by(self.ancilla_qubits[0])
                 for qubit_index, qubit_gates in enumerate(logical_xs[operation.qubit_index])
                 for gate in qubit_gates]

            circuit = Circuit(
                H(self.ancilla_qubits[0]),
                logical_cx,
                H(self.ancilla_qubits[0]),
                logical_cz,
                H(self.ancilla_qubits[0]),
                logical_cz,
                R(self.ancilla_qubits[0]),
            )
            self._current_state = self._get_state_after_circuit(circuit=circuit)
            return

        logical_gates = self._get_logical_operation_gates(operation=operation)
        if logical_gates is None:
            # TODO test for this
            raise ValueError(f"Unknown gate: {operation.gate}")
        logical_gates_for_qubit = logical_gates[operation.qubit_index] # TODO test for multiple encoded bits, invalid qubit index, etc
        circuit = Circuit(
            [gate(self._get_qubit_at_index(qubit_index=qubit_index))
             for qubit_index, qubit_gates in enumerate(logical_gates_for_qubit)
             for gate in qubit_gates]
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)
        # self._modify_stabilizers(operation=operation)

    def _get_logical_operation_gates(self, operation: LogicalOperation) -> Optional[List[List[List[Gate]]]]:
        if operation.gate == LogicalGateLabel.X:
            return CheckMatrixToGates(check_matrix=CheckMatrix(self._check_matrix_standardized.logical_xs)).get_gates()
        elif operation.gate == LogicalGateLabel.Z:
            return CheckMatrixToGates(check_matrix=CheckMatrix(self._check_matrix_standardized.logical_zs)).get_gates()
        elif operation.gate == LogicalGateLabel.H:
            pass

    def _modify_stabilizers(self, operation: LogicalOperation) -> None:
        if operation.gate == LogicalGateLabel.H:
            self._check_matrix_standardized.swap_xs_and_zs()

    def correct_errors(self) -> None:
        recoveries = RecoveryFinder(check_matrix=self._check_matrix_standardized).find_recoveries()
        generators = CheckMatrixToGates(check_matrix=self._check_matrix_standardized).get_gates()
        circuit = Circuit(
            [H(ancilla) for ancilla in self.ancilla_qubits],
            [gate(self._get_qubit_at_index(target_index)).controlled_by(ancilla)
             for ancilla, generator in zip(self.ancilla_qubits, generators)
             for target_index, qubit_gates in enumerate(generator) for gate in qubit_gates],
            [H(ancilla) for ancilla in self.ancilla_qubits],
            [recovery.gate(self._get_qubit_at_index(recovery.qubit_index)).controlled_by(*self.ancilla_qubits,
                                                                                         control_values=recovery.symptom)
             for symptom_recoveries in recoveries.values() for recovery in symptom_recoveries],
            [R(ancilla) for ancilla in self.ancilla_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self.data_qubits[self._check_matrix_standardized.qubit_order[qubit_index]]

    @cached_property
    def _check_matrix_standardized(self) -> CheckMatrixStandardized:
        standardizer = CheckMatrixStandardizer(check_matrix=self._check_matrix)
        return standardizer.get_standardized_matrix()
