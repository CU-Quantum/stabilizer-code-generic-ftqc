from functools import cached_property
from typing import List, Optional
from uuid import uuid4

from cirq import Circuit, CircuitOperation, Gate, H, KeyCondition, LineQubit, MeasurementKey, R, X, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix, \
    TYPE_CHECK_MATRIX
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.logical_qubit_encoder import \
    LogicalQubitEncoderGottesman
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToGates
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.utilities import FreshAncillasPool, int_to_binary_array


class GenericStabilizerCode(ErrorCorrectingCode):
    def __init__(self, generators: TYPE_CHECK_MATRIX, qubit_start_index: int = 0):
        self._check_matrix = CheckMatrix(matrix=generators)
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_logical_qubits=self._check_matrix.num_logical_qubits,
                         qubit_start_index=qubit_start_index)
        self._generators = generators

    def encode_logical_qubit(self) -> Circuit:
        return LogicalQubitEncoderGottesman(check_matrix_standardized=self._check_matrix_standardized,
                                            data_qubits=self.data_qubits).get_encoding_circuit()
        # with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
        #     logical_z_measuring_qubit = ancilla_qubits[0]
        #     z_measurement_key = MeasurementKey(f'ENCODING_{uuid4()}')
        #     logical_operation_circuits = [(self._get_logical_x_or_z(LogicalOperation(qubit_index=i, gate=gate))
        #                                   for gate in (LogicalGateLabel.Z, LogicalGateLabel.X))
        #                                   for i in range(self.num_logical_qubits)]
        #     return Circuit(
        #         LogicalQubitEncoderGottesman(check_matrix_standardized=self._check_matrix_standardized,
        #                                      data_qubits=self.data_qubits).get_encoding_circuit(),
        #         [
        #             [
        #                 FaultTolerantMeasurer(
        #                     operations=list(z_circuit.all_operations()),
        #                     measurement_qubit=logical_z_measuring_qubit,
        #                     measurement_key=z_measurement_key
        #                 ).get_measurement_circuit(),
        #                 CircuitOperation(x_circuit.freeze()).with_classical_controls(KeyCondition(z_measurement_key))
        #             ]
        #             for z_circuit, x_circuit in logical_operation_circuits
        #         ]
        #     )
        # with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
        #     return Circuit(
        #         self._get_syndrome_measurement_circuit(ancilla_qubits=ancilla_qubits),
        #         [Z(self.data_qubits[i]).controlled_by(ancilla_qubits[i])
        #          for i in range(self._num_ancilla_qubits)],
        #     )

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

    @property
    def implemented_operations(self) -> List[LogicalGateLabel]:
        return [LogicalGateLabel.X, LogicalGateLabel.Z, LogicalGateLabel.H]

    def get_error_correction_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
            recoveries = RecoveryFinder(check_matrix=self._check_matrix_standardized).find_recoveries()
            circuit = Circuit(
                self._get_syndrome_measurement_circuit(ancilla_qubits=ancilla_qubits),
                [recovery.gate(self._get_qubit_at_index(recovery.qubit_index)).controlled_by(*ancilla_qubits,
                                                                                             control_values=recovery.symptom)
                 for symptom_recoveries in recoveries.values() for recovery in symptom_recoveries],
                [R(ancilla) for ancilla in ancilla_qubits],
            )
            return circuit

    def _get_syndrome_measurement_circuit(self, ancilla_qubits: list[LineQubit]) -> Circuit:
        # TODO measure syndromes one generator at a time
        generators = CheckMatrixToGates(check_matrix=self._check_matrix_standardized).get_gates()
        return Circuit(
            [H(ancilla) for ancilla in ancilla_qubits],
            [gate(self._get_qubit_at_index(target_index)).controlled_by(ancilla)
             for ancilla, generator in zip(ancilla_qubits, generators)
             for target_index, qubit_gates in enumerate(generator) for gate in qubit_gates],
            [H(ancilla) for ancilla in ancilla_qubits],
        )

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self.data_qubits[qubit_index]

    @cached_property
    def _check_matrix_standardized(self) -> CheckMatrixStandardized:
        standardizer = CheckMatrixStandardizer(check_matrix=self._check_matrix)
        return standardizer.get_standardized_matrix()

    @property
    def _num_ancilla_qubits(self) -> int:
        return len(self._check_matrix.matrix)
