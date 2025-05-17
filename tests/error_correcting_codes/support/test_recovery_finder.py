from cirq import X, Y, Z
from numpy import array

from stim_experiments.custom_dataclasses.recovery import RecoveryGates
from stim_experiments.custom_dataclasses.check_matrix import \
    CheckMatrix
from stim_experiments.error_correcting_codes.support.recovery_finder import RecoveryFinder


class TestRecoveryFinder:
    def test_one_x_stabilizer(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == [
            RecoveryGates(
                gate=Z,
                qubit_index=0,
                symptom=[1]
            ),
        ]

    def test_one_z_stabilizer(self):
        check_matrix = CheckMatrix(matrix=array([[0, 1]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == [
            RecoveryGates(
                gate=X,
                qubit_index=0,
                symptom=[1]
            ),
        ]

    def test_one_y_stabilizer(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0, 0, 0], [0, 0, 1, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == [
            RecoveryGates(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0]
            ),
            RecoveryGates(
                gate=X,
                qubit_index=0,
                symptom=[0, 1]
            ),
            RecoveryGates(
                gate=Y,
                qubit_index=0,
                symptom=[1, 1]
            )
        ]

    def test_y_stabilizer_handles_mod_2(self):
        check_matrix = CheckMatrix(matrix=array([[1, 1]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == [
            RecoveryGates(
                gate=X,
                qubit_index=0,
                symptom=[1]
            ),
        ]

    def test_two_x_stabilizers(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0, 0, 0], [1, 0, 0, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == [
            RecoveryGates(
                gate=Z,
                qubit_index=0,
                symptom=[1, 1]
            ),
        ]

    def test_two_stabilizers_one_x_on_second_qubit(self):
        check_matrix = CheckMatrix(matrix=array([[0, 1, 0, 0], [0, 0, 0, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == [
            RecoveryGates(
                gate=Z,
                qubit_index=1,
                symptom=[1, 0]
            ),
        ]

    def test_no_symptoms_of_all_zero(self):
        check_matrix = CheckMatrix(matrix=array([[0, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == []
