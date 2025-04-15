from re import escape
from typing import List

import pytest
from cirq import LineQubit, X
from numpy import kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.simulators.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_DENSITY_MATRIX, \
    KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class CodeStub(ErrorCorrectingCode):
    def __init__(self,
                 initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX = KET_ZERO_STATE_VECTOR,
                 num_data_qubits: int = 1,
                 num_ancilla_qubits: int = 0,
                 num_logical_qubits: int = 1):
        super().__init__(num_data_qubits=num_data_qubits, num_ancilla_qubits=num_ancilla_qubits, num_logical_qubits=num_logical_qubits, initial_logical_qubit_state=initial_state)
        self.operation_applied = False

    def _encode_logical_qubit(self) -> None:
        self._current_state = self._initial_logical_qubit_state

    def correct_errors(self) -> None:
        pass

    def _perform_apply_operation(self, operation: LogicalOperation) -> None:
        self.operation_applied = True

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        return [LogicalGateLabel.Z, LogicalGateLabel.H]


class TestErrorCorrectingCode:
    def test_encodes_logical_qubit(self):
        code = CodeStub(initial_state=KET_ZERO_DENSITY_MATRIX)
        current_state = code.get_current_state()
        assert current_state.tolist() == KET_ZERO_DENSITY_MATRIX.tolist()

    def test_correctly_applies_errors(self):
        code = CodeStub(initial_state=KET_ZERO_STATE_VECTOR)
        code.apply_error(gate=X, qubit_index=0)
        current_state = code.get_current_state()
        assert current_state.tolist() == KET_ONE_STATE_VECTOR.tolist()

        initial_state_two_qubits = kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR).flatten()
        code = CodeStub(initial_state=initial_state_two_qubits, num_data_qubits=2)
        code.apply_error(gate=X, qubit_index=1)
        current_state = code.get_current_state()
        expected_state_two_qubits = kron(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR).flatten()
        assert current_state.tolist() == expected_state_two_qubits.tolist()

    def test_correctly_chooses_density_matrix_type(self):
        code = CodeStub(initial_state=KET_ZERO_DENSITY_MATRIX)
        code.apply_error(gate=X, qubit_index=0)
        current_state = code.get_current_state()
        assert current_state.shape == (2, 2)

    def test_correctly_chooses_state_vector_type(self):
        code = CodeStub(initial_state=KET_ONE_STATE_VECTOR)
        code.apply_error(gate=X, qubit_index=0)
        current_state = code.get_current_state()
        assert current_state.shape == (2,)

    def test_can_get_data_qubits(self):
        expected_num_qubits = 2
        code = CodeStub(num_data_qubits=expected_num_qubits)
        assert code.data_qubits == LineQubit.range(expected_num_qubits)

    def test_can_get_ancilla_qubits(self):
        expected_num_data_qubits = 2
        expected_num_ancilla_qubits = 2
        code = CodeStub(num_data_qubits=expected_num_data_qubits, num_ancilla_qubits=expected_num_ancilla_qubits)
        assert code.ancilla_qubits == LineQubit.range(expected_num_data_qubits, expected_num_data_qubits + expected_num_ancilla_qubits)

    def test_can_get_all_qubits(self):
        expected_data_qubits = 2
        expected_ancilla_qubits = 2
        code = CodeStub(num_data_qubits=expected_data_qubits, num_ancilla_qubits=expected_ancilla_qubits)
        assert code.all_qubits == LineQubit.range(expected_data_qubits + expected_ancilla_qubits)

    def test_cannot_apply_unimplemented_operation(self):
        code = CodeStub()
        with pytest.raises(NotImplementedError, match=escape("Operation X is not implemented. Implemented gates are: ['Z', 'H'].")):
            code.apply_operation(LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0))
        assert not code.operation_applied

    def test_apply_implemented_operation(self):
        code = CodeStub()
        code.apply_operation(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
        assert code.operation_applied

    def test_qubit_index_must_be_at_least_zero(self):
        code = CodeStub(num_logical_qubits=2)
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 1. Was given -1."):
            code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=-1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))

    def test_qubit_index_must_be_at_most_largest_logical_index(self):
        code = CodeStub(num_logical_qubits=2)
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 1. Was given 2."):
            code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=2))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))

        code = CodeStub(num_logical_qubits=1)
        with pytest.raises(ValueError, match="Qubit index must be between 0 and 0. Was given 1."):
            code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=1))
        code.apply_operation(operation=LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0))
