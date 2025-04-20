from typing import List

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, H, R, X, Z, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, int_to_binary_array


class SteaneCode(ErrorCorrectingCode):
    _stabilizer_indices = [(3, 4, 5, 6), (1, 2, 5, 6), (0, 2, 4, 6)]

    def __init__(self, initial_logical_qubit_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, qubit_start_index: int = 0):
        super().__init__(initial_logical_qubit_state=initial_logical_qubit_state,
                         num_data_qubits=7,
                         num_ancilla_qubits=3,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        initial_state = kron(self._initial_logical_qubit_state, *[KET_ZERO_DENSITY_MATRIX] * (len(self.all_qubits) - 1))
        initialize_with_given_state = Circuit(
            [CX(self.data_qubits[0], data_qubit) for data_qubit in self.data_qubits[1:]],
        )
        initial_state_simulation: DensityMatrixTrialResult = DensityMatrixSimulator().simulate(initialize_with_given_state,
                                                                                               qubit_order=self.all_qubits,
                                                                                               initial_state=initial_state)
        initial_state = initial_state_simulation.final_density_matrix

        state_and_measurements = self.error_correcting_code_utilities.get_state_after_circuit(circuit=self.get_error_correction_circuit(),
                                                                                              qubit_order=self.all_qubits,
                                                                                              initial_state=initial_state)
        return state_and_measurements.state

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        return []

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit(
            self._correct_bit_flips(),
            self._correct_phase_flips()
        )

    def _correct_bit_flips(self) -> Circuit:
        syndrome = Circuit(
            [CX(self.data_qubits[data_index], self.ancilla_qubits[ancilla_index])
             for ancilla_index, data_indices in enumerate(self._stabilizer_indices)
             for data_index in data_indices],
        )
        return self._correct_error(syndrome=syndrome, correction_gate=X)

    def _correct_phase_flips(self) -> Circuit:
        syndrome = Circuit(
            [H(ancilla) for ancilla in self.ancilla_qubits],
            [CX(self.ancilla_qubits[ancilla_index], self.data_qubits[data_index])
             for ancilla_index, data_indices in enumerate(self._stabilizer_indices)
             for data_index in data_indices],
            [H(ancilla) for ancilla in self.ancilla_qubits],
        )
        return self._correct_error(syndrome=syndrome, correction_gate=Z)

    def _correct_error(self, syndrome: Circuit, correction_gate: Gate) -> Circuit:
        recovery = Circuit(
            [correction_gate.controlled(num_controls=3, control_values=int_to_binary_array(num=i + 1, num_elements=self._num_ancilla_qubits)).on(
                *self.ancilla_qubits,
                self.data_qubits[i]
            ) for i in range(self._num_data_qubits)]
        )
        circuit = Circuit(
            syndrome,
            recovery,
            [R(ancilla) for ancilla in self.ancilla_qubits],
        )
        return circuit
