from cirq import LineQubit, X, Y, Z
from numpy import array

from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.recovery import RecoveryGate, RecoveryOperation
from stim_experiments.error_correcting_codes.support.recovery_combinations_finder import RecoveryCombinationsFinder
from stim_experiments.error_correcting_codes.support.recovery_finder import RecoveryFinder


class TestRecoveryCombinationsFinder:
    def test_max_zero_errors(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recovery_gates()
        combos = RecoveryCombinationsFinder(max_num_errors=0).find_recoveries(single_error_recoveries=recoveries)
        assert combos == []

    def test_max_one_errors(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recovery_gates()
        combos = RecoveryCombinationsFinder(max_num_errors=1).find_recoveries(single_error_recoveries=recoveries)
        assert combos == [
            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1]
            )
        ]

    def test_gates_max_two_errors(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0, 0, 0], [0, 0, 0, 1]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recovery_gates()
        combos = RecoveryCombinationsFinder(max_num_errors=2).find_recoveries(single_error_recoveries=recoveries)
        assert combos == [
            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=1,
                symptom=[0, 1]
            ),
            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=1,
                symptom=[1, 1]
            ),
        ]

    def test_operations_max_two_errors(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0, 0, 0], [0, 0, 0, 1]]))
        num_qubits = 2
        qubits = LineQubit.range(num_qubits)
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recovery_operations(qubits=qubits)
        combos = RecoveryCombinationsFinder(max_num_errors=2).find_recoveries(single_error_recoveries=recoveries)
        assert combos == [
            RecoveryOperation(
                operation=Z(qubits[0]),
                symptom=[1, 0]
            ),
            RecoveryOperation(
                operation=X(qubits[1]),
                symptom=[0, 1]
            ),
            RecoveryOperation(
                operation=Z(qubits[0]),
                symptom=[1, 1]
            ),
            RecoveryOperation(
                operation=X(qubits[1]),
                symptom=[1, 1]
            ),
        ]

    def test_different_max_x_z(self):
        check_matrix = CheckMatrix(matrix=array([
            [1, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 1],
        ]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recovery_gates()
        combos = RecoveryCombinationsFinder(max_num_x_errors=2, max_num_z_errors=1).find_recoveries(single_error_recoveries=recoveries)
        assert combos == [
            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 0, 0]
            ),
            RecoveryGate(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 0, 0]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=2,
                symptom=[0, 0, 1, 0]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=3,
                symptom=[0, 0, 0, 1]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 1, 0]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=2,
                symptom=[1, 0, 1, 0]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 0, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=3,
                symptom=[1, 0, 0, 1]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 1, 0]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=2,
                symptom=[0, 1, 1, 0]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 0, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=3,
                symptom=[0, 1, 0, 1]
            ),

            RecoveryGate(
                gate=X,
                qubit_index=2,
                symptom=[0, 0, 1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=3,
                symptom=[0, 0, 1, 1]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=2,
                symptom=[1, 0, 1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=3,
                symptom=[1, 0, 1, 1]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=2,
                symptom=[0, 1, 1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=3,
                symptom=[0, 1, 1, 1]
            ),
        ]

    def test_different_max_x_z_with_y_errors(self):
        check_matrix = CheckMatrix(matrix=array([[1, 0, 0, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0]]))
        recoveries = RecoveryFinder(check_matrix=check_matrix).find_recovery_gates()
        combos = RecoveryCombinationsFinder(max_num_x_errors=2, max_num_z_errors=1).find_recoveries(single_error_recoveries=recoveries)
        assert combos == [
            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 0]
            ),
            RecoveryGate(
                gate=Z,
                qubit_index=1,
                symptom=[0, 0, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=0,
                symptom=[0, 1, 0]
            ),
            RecoveryGate(
                gate=Y,
                qubit_index=0,
                symptom=[1, 1, 0]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=0,
                symptom=[1, 1, 0]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=0,
                symptom=[1, 1, 0]
            ),

            RecoveryGate(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 1]
            ),
            RecoveryGate(
                gate=X,
                qubit_index=0,
                symptom=[0, 1, 1]
            ),

            RecoveryGate(
                gate=X,
                qubit_index=0,
                symptom=[1, 0, 0]
            ),
            RecoveryGate(
                gate=Y,
                qubit_index=0,
                symptom=[1, 0, 0]
            ),
        ]
