from functools import cached_property
from typing import List, Optional, Union

from cirq import Circuit, Gate, H, KET_ZERO, LineQubit, R, X

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
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import TYPE_DENSITY_MATRIX, TYPE_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, \
    get_num_qubits_in_state, tensor


class GenericStabilizerCode(ErrorCorrectingCode):
    def __init__(self,
                 generators: TYPE_CHECK_MATRIX,
                 initial_logical_qubit_state: Optional[Union[TYPE_STATE_VECTOR, TYPE_DENSITY_MATRIX]] = None,
                 qubit_start_index: int = 0,
                 provided_ancilla_qubits: Optional[list[LineQubit]] = None,
                 ):
        self._check_matrix = CheckMatrix(matrix=generators)
        if initial_logical_qubit_state is None:
            initial_logical_qubit_state = tensor(*[KET_ZERO.state_vector()] * self._check_matrix.num_logical_qubits).reshape(2 ** self._check_matrix.num_logical_qubits,)
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_ancilla_qubits=len(self._check_matrix.matrix),
                         num_logical_qubits=self._check_matrix.num_logical_qubits,
                         initial_logical_qubit_state=initial_logical_qubit_state,
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits)
        self._generators = generators

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        self._validate_initial_logical_state_size()
        initial_state = self._initialize_logical_state()
        circuit = self._get_encoding_circuit()
        state_and_measurements = self.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=self.all_qubits,
                                                                                              initial_state=initial_state)
        return state_and_measurements.state

    def _validate_initial_logical_state_size(self) -> None:
        num_qubits_in_initial_logical_state = get_num_qubits_in_state(self._initial_logical_qubit_state)
        if num_qubits_in_initial_logical_state != self._check_matrix.num_logical_qubits:
            raise ValueError(f"These generators encode {self._check_matrix.num_logical_qubits} logical qubits, but an initial state of {num_qubits_in_initial_logical_state} was given.")

    def _initialize_logical_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        data_state = tensor(*[self.error_correcting_code_utilities.zero_state] * (self._num_data_qubits - self._check_matrix.num_logical_qubits),
                          self._initial_logical_qubit_state)
        ancilla_state = tensor(*[self.error_correcting_code_utilities.zero_state] * self._num_ancilla_qubits)
        return tensor(data_state, ancilla_state)

    def _get_encoding_circuit(self) -> Circuit:
        return LogicalQubitEncoder(check_matrix_standardized=self._check_matrix_standardized,
                                   data_qubits=self.data_qubits).get_encoding_circuit()

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        return self._get_logical_hadamard(operation=operation) \
            if operation.gate == LogicalGateLabel.H \
            else self._get_logical_x_or_z(operation=operation)

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
        logical_operations = (self._get_logical_operation_gates(gate_label=label)
                              for label in (LogicalGateLabel.X, LogicalGateLabel.Z))
        logical_cx, logical_cz = (
            [gate(self._get_qubit_at_index(qubit_index=qubit_index)).controlled_by(self.ancilla_qubits[0])
             for qubit_index, qubit_gates in enumerate(logical_operation[operation.qubit_index])
             for gate in qubit_gates]
            for logical_operation in logical_operations
        )
        circuit = Circuit(
            H(self.ancilla_qubits[0]),
            logical_cx,
            logical_cz,
            H(self.ancilla_qubits[0]),
            logical_cx,
            X(self.ancilla_qubits[0]),
            logical_cz,
            H(self.ancilla_qubits[0]),
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

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        return [LogicalGateLabel.X, LogicalGateLabel.Z, LogicalGateLabel.H]

    def get_error_correction_circuit(self) -> Circuit:
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
        return circuit

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self.data_qubits[self._check_matrix_standardized.qubit_order[qubit_index]]

    @cached_property
    def _check_matrix_standardized(self) -> CheckMatrixStandardized:
        standardizer = CheckMatrixStandardizer(check_matrix=self._check_matrix)
        return standardizer.get_standardized_matrix()
