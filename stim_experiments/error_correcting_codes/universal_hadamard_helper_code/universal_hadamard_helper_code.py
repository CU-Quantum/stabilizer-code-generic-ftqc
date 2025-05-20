from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities.repetition_z_stabilizers_multicat_generator import \
    RepetitionZStabilizersMulticatGenerator


class UniversalHadamardHelperCode(StabilizerCode):
    """
    This is used in the universal hadamard. It does not correct phase errors on the first qubit, which only affects
    the global phase when used as part of the universal hadamard.
    """
    num_cats = ThreeCatCode.num_cats

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        num_data_qubits = num_qubits_in_cat_state * self.num_cats

        z_stabilizers = RepetitionZStabilizersMulticatGenerator(num_qubits_in_cat=self._num_qubits_in_cat_state,
                                                                num_cats=self.num_cats).get_stabilizers()
        x_stabilizers = [
            [int(cat_index * self._num_qubits_in_cat_state <= qubit_index < (
                        cat_index + 1) * self._num_qubits_in_cat_state)
             for qubit_index in range(num_data_qubits)] + [1] + [0] * (num_data_qubits - 1)
            for cat_index in range(1, self.num_cats)
        ]

        self._check_matrix = CheckMatrix(matrix=array(z_stabilizers + x_stabilizers))
        super().__init__(check_matrix=self._check_matrix, qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        num_generators = len(self._check_matrix.matrix)
        is_z_stabilizer = generator_index < num_generators - 2
        if is_z_stabilizer:
            num_checks_per_register = self._num_qubits_in_cat_state - 1
            register_index = generator_index // num_checks_per_register
            start_index = register_index * self._num_qubits_in_cat_state
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in
                    range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == num_generators - 1
            return Z(self.data_qubits[(is_last_generator + 1) * self._num_qubits_in_cat_state])

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            x_portion = [X(qubit) for qubit in self.data_qubits[:self._num_qubits_in_cat_state]]
            z_portion = [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(1, self.num_cats)]
            return Circuit(
                x_portion + z_portion
            )
        if operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[0])]
            )
        return None
