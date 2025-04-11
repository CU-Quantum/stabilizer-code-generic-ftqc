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
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX
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
                         num_ancilla_qubits=len(generators),
                         initial_logical_qubit_state_density_matrix=initial_logical_qubit_state_density_matrix)
        self._generators = generators

    def _encode_logical_qubit(self) -> None:
        circuit = Circuit(
            self._encode_logical_nots(),
            [H(self._get_qubit_at_index(control_index)) for control_index in range(self._check_matrix.rank_of_pauli_x_portion)],
            self._encode_generators(),
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)

    def _encode_logical_nots(self) -> List[List[List[Operation]]]:
        return [self._get_controlled_logical_not_gates(control_num=control_num)
                for control_num in range(self._check_matrix.num_logical_qubits)]

    def _get_controlled_logical_not_gates(self, control_num: int) -> List[List[Operation]]:
        logical_xs = self._check_matrix_standardized.logical_xs
        logical_x_gates = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=logical_xs)).get_gates()

        control_index = self._check_matrix.num_physical_qubits - self._check_matrix.num_logical_qubits + control_num
        return [self._get_controlled_gates_at_qubit(gates=gates, control_index=control_index, target_index=target_index)
                for target_index, gates in enumerate(logical_x_gates[control_num]) if target_index != control_index]

    def _encode_generators(self) -> List[List[List[Operation]]]:
        return [self._get_controlled_generator_gates(control_num=control_num)
                for control_num in range(self._check_matrix.rank_of_pauli_x_portion)]

    def _get_controlled_generator_gates(self, control_num: int) -> List[List[Operation]]:
        generators = self._check_matrix_standardized.matrix[:self._check_matrix_standardized.rank_of_pauli_x_portion]
        generator_gates = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=generators)).get_gates()

        return [self._get_controlled_gates_at_qubit(gates=gates, control_index=control_num, target_index=target_index)
                for target_index, gates in enumerate(generator_gates[control_num]) if target_index != control_num]

    def _get_controlled_gates_at_qubit(self, gates: List[Gate], control_index: int, target_index: int) -> List[Operation]:
        return [gate(self._get_qubit_at_index(target_index)).controlled_by(self._get_qubit_at_index(control_index))
                for gate in gates]

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
        expected_state = kron(ExpectedStatesSteane().get_logical_zero_density_matrix(), *[KET_ZERO_DENSITY_MATRIX] * 3)
        code = GenericStabilizerCode(generators=get_check_matrix_values_steane())
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    def test_logical_zero_five_qubit(self):
        expected_state = ExpectedStatesFiveQubit().get_logical_zero_density_matrix()
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        current_state = code.get_current_state()
        assert allclose(current_state, expected_state, atol=1e-7)

    # def test_logical_one(self):
    #     expected_state = ExpectedStatesFiveQubit().get_logical_one_density_matrix()
    #     code = FiveQubitCode(initial_logical_qubit_state_density_matrix=KET_ONE_DENSITY_MATRIX)
    #     current_state = code.get_current_state()
    #     assert allclose(current_state, expected_state, atol=1e-7)
