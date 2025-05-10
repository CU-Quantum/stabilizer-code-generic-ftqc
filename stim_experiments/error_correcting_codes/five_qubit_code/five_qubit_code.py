from typing import Optional

from cirq import Circuit, H, I, LineQubit, Operation, R, X, Y, Z
from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import Recovery
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import FreshAncillasPool


class FiveQubitCode(ErrorCorrectingCode):
    _generators = [
        [X, Z, Z, X, I],
        [I, X, Z, Z, X],
        [X, I, X, Z, Z],
        [Z, X, I, X, Z],
    ]

    @property
    def _flip_corrections(self):
        return [
            [self.data_qubits[i] for i in (0, 2)],
            [self.data_qubits[i] for i in (0,1,2,3)],
            [self.data_qubits[i] for i in (0,1,3,4)],
            [self.data_qubits[i] for i in (1,4)],
        ]

    def __init__(self, qubit_start_index: int = 0):
        super().__init__(num_data_qubits=5,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index)

    def encode_logical_qubit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
            return Circuit(
                self._syndrome_circuit,
                [self._get_phase_corrections(ancilla_index=ancilla_index) for ancilla_index in range(self._num_ancilla_qubits)],
                [H(ancilla) for ancilla in ancilla_qubits],
            )

    @property
    def _syndrome_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
            return Circuit(
                [H(ancilla) for ancilla in ancilla_qubits],
                [gate(self.data_qubits[target_index]).controlled_by(ancilla_qubits[generator])
                 for generator, gates in enumerate(self._generators) for target_index, gate in enumerate(gates)],
                [H(ancilla) for ancilla in ancilla_qubits],
            )

    def _get_phase_corrections(self, ancilla_index: int) -> list[list[Operation]]:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
            fix_qubits = self._flip_corrections[ancilla_index]
            return [
                [Z(fix_qubit).controlled_by(ancilla_qubits[ancilla_index]) for fix_qubit in fix_qubits],
            ]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    @property
    def implemented_operations(self) -> list[LogicalGateLabel]:
        return []

    def get_error_correction_circuit(self) -> Circuit:
        recoveries = [
            Recovery(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 1, 0]
            ),
            Recovery(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 0, 1]
            ),
            Recovery(
                gate=Z,
                qubit_index=2,
                symptom=[0, 0, 1, 0]
            ),
            Recovery(
                gate=Z,
                qubit_index=3,
                symptom=[1, 0, 0, 1]
            ),
            Recovery(
                gate=Z,
                qubit_index=4,
                symptom=[0, 1, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=0,
                symptom=[0, 0, 0, 1]
            ),
            Recovery(
                gate=X,
                qubit_index=1,
                symptom=[1, 0, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=2,
                symptom=[1, 1, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=3,
                symptom=[0, 1, 1, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=4,
                symptom=[0, 0, 1, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=0,
                symptom=[1, 0, 1, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=1,
                symptom=[1, 1, 0, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=2,
                symptom=[1, 1, 1, 0]
            ),
            Recovery(
                gate=Y,
                qubit_index=3,
                symptom=[1, 1, 1, 1]
            ),
            Recovery(
                gate=Y,
                qubit_index=4,
                symptom=[0, 1, 1, 1]
            ),
        ]

        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_ancilla_qubits) as ancilla_qubits:
            recovery_circuit = Circuit(
                [recovery.gate(self.data_qubits[recovery.qubit_index]).controlled_by(*ancilla_qubits, control_values=recovery.symptom)
                 for recovery in recoveries]
            )
            return Circuit(
                self._syndrome_circuit,
                recovery_circuit,
                [R(ancilla) for ancilla in ancilla_qubits],
            )

    @property
    def _num_ancilla_qubits(self) -> int:
        return 4
