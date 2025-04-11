from cirq import X, Z
from numpy import array

from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import Recovery
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import \
    CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder


class TestRecoveryFinder:
    def test_one_x_stabilizer(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == {
            1: [
                Recovery(
                    gate=Z,
                    qubit_index=0,
                    symptom=[1]
                )
            ],
        }

    def test_one_z_stabilizer(self):
        check_matrix = CheckMatrix(matrix=array([[0, 1]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == {
            1: [
                Recovery(
                    gate=X,
                    qubit_index=0,
                    symptom=[1]
                )
            ],
        }

    def test_one_y_stabilizer(self):
        check_matrix = CheckMatrix(matrix=array([[1, 1]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == {
            1: [
                Recovery(
                    gate=Z,
                    qubit_index=0,
                    symptom=[1]
                ),
                Recovery(
                    gate=X,
                    qubit_index=0,
                    symptom=[1]
                ),
            ],
        }

    def test_two_x_stabilizers(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0, 0, 0], [1, 0, 0, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == {
            3: [
                Recovery(
                    gate=Z,
                    qubit_index=0,
                    symptom=[1, 1]
                ),
            ],
        }

    def test_two_stabilizers_one_x_on_second_qubit(self):
        check_matrix = CheckMatrix(matrix=array([[0, 1, 0, 0], [0, 0, 0, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recoveries()
        assert recoveries == {
            2: [
                Recovery(
                    gate=Z,
                    qubit_index=1,
                    symptom=[1, 0]
                ),
            ],
        }
