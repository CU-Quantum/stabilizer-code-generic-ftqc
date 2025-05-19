from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities.repetition_z_stabilizers_generator import RepetitionZStabilizersGenerator


class ThreeCatSubregisterParityCode(StabilizerCode):
    num_cats = ThreeCatCode.num_cats

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        num_data_qubits = num_qubits_in_cat_state * self.num_cats

        z_stabilizers_in_cat_state = RepetitionZStabilizersGenerator(num_qubits=self._num_qubits_in_cat_state).get_stabilizers()
        pauli_x_portion_of_z_stabilizers = [0] * num_data_qubits
        z_stabilizers = [
            pauli_x_portion_of_z_stabilizers
            + [0] * cat_index * self._num_qubits_in_cat_state
            + stabilizer
            + [0] * (self.num_cats - cat_index - 1) * self._num_qubits_in_cat_state
            for cat_index in range(self.num_cats)
            for stabilizer in z_stabilizers_in_cat_state
        ]

        x_stabilizers = [
            [int(cat_index * self._num_qubits_in_cat_state <= qubit_index < (cat_index + 2) * self._num_qubits_in_cat_state)
             for qubit_index in range(num_data_qubits)] + [0] * num_data_qubits
            for cat_index in range(self.num_cats - 1)
        ]

        self._check_matrix = CheckMatrix(matrix=array(z_stabilizers + x_stabilizers))
        super().__init__(check_matrix=self._check_matrix, qubits=qubits)

    def _qubit_has_x_stabilizer_in_generator(self, cat_index: int, parity_check_index: int, qubit_index: int) -> int:
        low_index = cat_index * self._num_qubits_in_cat_state + parity_check_index
        high_index = low_index + 1
        return int(low_index <= qubit_index <= high_index)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        is_z_stabilizer = generator_index < self._num_generators - 2
        if is_z_stabilizer:
            num_checks_per_register = self._num_qubits_in_cat_state - 1
            register_index = generator_index // num_checks_per_register
            start_index = register_index * self._num_qubits_in_cat_state
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == self._num_generators - 1
            return [Z(self.data_qubits[0 - is_last_generator])]

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

    @property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                for i in range(self.num_cats)]

    @property
    def _num_generators(self) -> int:
        return len(self._check_matrix.matrix)
