from cirq import X, Z
from numpy import array

from stim_experiments.custom_dataclasses.check_matrix import \
    CheckMatrix
from stim_experiments.error_correcting_codes.support.check_matrix_to_gates import \
    CheckMatrixToGates
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit


class TestCheckMatrixToGates:
    def test_x_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[1, 0]])))
        gates = converter.get_gates()
        assert gates == [[[X]]]

    def test_z_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[0, 1]])))
        gates = converter.get_gates()
        assert gates == [[[Z]]]

    def test_y_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[1, 1]])))
        gates = converter.get_gates()
        assert gates == [[[X, Z]]]

    def test_4_qubit(self):
        check_matrix = CheckMatrix(matrix=get_check_matrix_values_4_qubit())
        converter = CheckMatrixToGates(check_matrix=check_matrix)
        gates = converter.get_gates()
        assert gates == [
            [[X], [Z], [Z], [X]],
            [[X, Z], [X], [X], [X, Z]],
        ]

    def test_minus_x_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[-1, 0]])))
        gates = converter.get_gates()
        assert gates == [[[Z, X, Z]]]

    def test_minus_z_gate(self):
        converter = CheckMatrixToGates(check_matrix=CheckMatrix(matrix=array([[0, -1]])))
        gates = converter.get_gates()
        assert gates == [[[X, Z, X]]]
