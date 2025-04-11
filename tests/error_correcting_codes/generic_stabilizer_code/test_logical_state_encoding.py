from functools import cached_property
from typing import List

from cirq import Circuit, Gate, H, LineQubit, Operation, kron
from numpy import allclose

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import \
    CheckMatrix, TYPE_CHECK_MATRIX
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix_standardized import \
    CheckMatrixStandardized
from stim_experiments.error_correcting_codes.generic_stabilizer_code.matrix_standardizer.check_matrix_standardizer import \
    CheckMatrixStandardizer
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ONE_DENSITY_MATRIX, KET_ZERO_DENSITY_MATRIX, \
    partial_trace
from tests.error_correcting_codes.five_qubit_code.expected_states_five_qubit import ExpectedStatesFiveQubit
from tests.error_correcting_codes.generic_stabilizer_code.support.test_check_matrix_to_gates import CheckMatrixToGates
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit, \
    get_check_matrix_values_steane
from tests.error_correcting_codes.steane_code.expected_states_steane import ExpectedStatesSteane


class GenericStabilizerCode(ErrorCorrectingCode):
    def __init__(self,
                 generators: TYPE_CHECK_MATRIX,
                 initial_logical_qubit_state_density_matrix: DENSITY_MATRIX_TYPE = KET_ZERO_DENSITY_MATRIX):
        self._check_matrix = CheckMatrix(matrix=generators)
        super().__init__(num_data_qubits=self._check_matrix.num_physical_qubits,
                         num_ancilla_qubits=1,
                         initial_logical_qubit_state_density_matrix=initial_logical_qubit_state_density_matrix)
        self._generators = generators

    def _encode_logical_qubit(self) -> None:
        data_state = kron(*[KET_ZERO_DENSITY_MATRIX] * (self._num_data_qubits - self._check_matrix.num_logical_qubits), self._initial_logical_qubit_state_density_matrix)
        ancilla_state = kron(*[KET_ZERO_DENSITY_MATRIX] * self._num_ancilla_qubits)
        self._current_state = kron(data_state, ancilla_state)

        hadamards = [H(self._get_qubit_at_index(control_index)) for control_index in range(self._check_matrix.rank_of_pauli_x_portion)]
        circuit = Circuit(
            self._encode_logical_nots(),
            zip(hadamards, self._encode_generators()),
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _encode_logical_nots(self) -> List[List[List[Operation]]]:
        return [self._get_controlled_gates(matrix_form_gates=self._check_matrix_standardized.logical_xs,
                                           control_num=control_num,
                                           control_index=self._num_data_qubits - self._check_matrix.num_logical_qubits + control_num)
                for control_num in range(self._check_matrix.num_logical_qubits)]

    def _encode_generators(self) -> List[List[List[Operation]]]:
        return [self._get_controlled_gates(matrix_form_gates=self._check_matrix_standardized.matrix,
                                           control_num=control_num,
                                           control_index=control_num)
                for control_num in range(self._check_matrix.rank_of_pauli_x_portion)]

    def _get_controlled_gates(self, matrix_form_gates: TYPE_CHECK_MATRIX, control_num: int, control_index: int) -> List[List[Operation]]:
        controlled_gates = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=matrix_form_gates)).get_gates()
        return [self._get_controlled_gates_at_qubit(gates=gates, control_index=control_index, target_index=target_index)
                for target_index, gates in enumerate(controlled_gates[control_num]) if target_index != control_index]

    def _get_controlled_gates_at_qubit(self, gates: List[Gate], control_index: int, target_index: int) -> List[Operation]:
        control_qubit = self._get_qubit_at_index(control_index)
        target_qubit = self._get_qubit_at_index(target_index)
        return [gate(target_qubit).controlled_by(control_qubit) for gate in gates]

    def _get_qubit_at_index(self, qubit_index: int) -> LineQubit:
        return self.data_qubits[self._check_matrix_standardized.qubit_order[qubit_index]]

    def correct_errors(self) -> None:
        pass

    @cached_property
    def _check_matrix_standardized(self) -> CheckMatrixStandardized:
        standardizer = CheckMatrixStandardizer(check_matrix=self._check_matrix)
        return standardizer.get_standardized_matrix()


class TestGenericStabilizerCode:
    def test_logical_zero_steane(self):
        size_of_code_plus_one_ancilla = 8
        expected_state = partial_trace(ExpectedStatesSteane().get_logical_zero_density_matrix(), list(range(size_of_code_plus_one_ancilla)))
        code = GenericStabilizerCode(generators=get_check_matrix_values_steane())
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_zero_five_qubit(self):
        size_of_code_plus_one_ancilla = 6
        expected_state = partial_trace(ExpectedStatesFiveQubit().get_logical_zero_density_matrix(), list(range(size_of_code_plus_one_ancilla)))
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_one_five_qubit(self):
        size_of_code_plus_one_ancilla = 6
        expected_state = partial_trace(ExpectedStatesFiveQubit().get_logical_one_density_matrix(), list(range(size_of_code_plus_one_ancilla)))
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state_density_matrix=KET_ONE_DENSITY_MATRIX)
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)
