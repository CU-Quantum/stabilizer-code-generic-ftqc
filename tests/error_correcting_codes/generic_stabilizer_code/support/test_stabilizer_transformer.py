import pytest
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    StabilizerTransformer
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation


class TestStabilizerTransformer:
    def test_operation_has_out_of_bounds_target(self):
        check = CheckMatrix(matrix=array([[0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        with pytest.raises(IndexError):
            transformer.apply(operations=[TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)])

    def test_operation_has_out_of_bounds_control(self):
        check = CheckMatrix(matrix=array([[0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        with pytest.raises(IndexError):
            transformer.apply(operations=[
                TransformationOperation(gate=TransformationGate.CX, target_qubit_index=0, control_qubit_index=1)])

    def test_cx_on_x_control(self):
        check = CheckMatrix(matrix=array([[1, 0, 0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[1, 1, 0, 0]]

    def test_cx_on_x_target(self):
        check = CheckMatrix(matrix=array([[0, 1, 0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 1, 0, 0]]

    def test_cx_on_z_control(self):
        check = CheckMatrix(matrix=array([[0, 0, 1, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 0, 1, 0]]

    def test_cx_on_z_target(self):
        check = CheckMatrix(matrix=array([[0, 0, 0, 1]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 0, 1, 1]]

    def test_cz_on_x_control(self):
        check = CheckMatrix(matrix=array([[1, 0, 0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CZ, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[1, 0, 1, 0]]

    def test_cz_on_x_target(self):
        check = CheckMatrix(matrix=array([[0, 1, 0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CZ, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 1, 0, 0]]

    def test_cz_on_z_control(self):
        check = CheckMatrix(matrix=array([[0, 0, 1, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CZ, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 0, 0, 1]]

    def test_cz_on_negative_z_control(self):  # TODO test negatives for other operations
        check = CheckMatrix(matrix=array([[0, 0, -1, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CZ, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 0, 0, -1]]

    def test_cz_on_z_target(self):
        check = CheckMatrix(matrix=array([[0, 0, 0, 1]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[
            TransformationOperation(gate=TransformationGate.CZ, target_qubit_index=1, control_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 0, 0, 1]]

    def test_h_on_x_target(self):
        check = CheckMatrix(matrix=array([[1, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[TransformationOperation(gate=TransformationGate.H, target_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 1]]

    def test_h_on_z_target(self):
        check = CheckMatrix(matrix=array([[0, 1]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[TransformationOperation(gate=TransformationGate.H, target_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[1, 0]]

    def test_x_on_identity(self):
        check = CheckMatrix(matrix=array([[0, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[TransformationOperation(gate=TransformationGate.X, target_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, 0]]

    def test_x_on_x_target(self):
        check = CheckMatrix(matrix=array([[1, 0]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[TransformationOperation(gate=TransformationGate.X, target_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[1, 0]]

    def test_x_on_z_target(self):
        check = CheckMatrix(matrix=array([[0, 1]]))
        transformer = StabilizerTransformer(check_matrix=check)
        transformer.apply(operations=[TransformationOperation(gate=TransformationGate.X, target_qubit_index=0)])
        new_check = transformer.get_current_check_matrix()
        assert new_check.matrix.tolist() == [[0, -1]]
