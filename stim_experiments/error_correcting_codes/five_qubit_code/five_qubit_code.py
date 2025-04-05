from dataclasses import dataclass
from typing import List

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, Gate, H, I, Operation, R, X, Z, kron

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.utilities import DENSITY_MATRIX_TYPE, KET_ZERO_DENSITY_MATRIX


@dataclass
class Recovery:
    gate: Operation
    symptom: List[int]


class FiveQubitCode(ErrorCorrectingCode):
    def __init__(self, initial_logical_qubit_state_density_matrix: DENSITY_MATRIX_TYPE):
        super().__init__(initial_logical_qubit_state_density_matrix=initial_logical_qubit_state_density_matrix, num_data_qubits=5, num_ancilla_qubits=4)

    def _encode_logical_qubit(self) -> None:
        initial_state = kron(self._initial_logical_qubit_state_density_matrix, *[KET_ZERO_DENSITY_MATRIX] * (len(self._qubits) - 1))
        initialize_with_given_state = Circuit(
            [CX(self._data_qubits[0], data_qubit) for data_qubit in self._data_qubits[1:]],
        )
        initial_state_simulation: DensityMatrixTrialResult = DensityMatrixSimulator().simulate(initialize_with_given_state,
                                                                                               qubit_order=self._qubits,
                                                                                               initial_state=initial_state)
        self._current_state = initial_state_simulation.final_density_matrix

        self.correct_errors()

    def correct_errors(self) -> None:
        generators = [
            [X, Z, Z, X, I],
            [I, X, Z, Z, X],
            [X, I, X, Z, Z],
            [Z, X, I, X, Z],
        ]

        recoveries = [
            Recovery(
                gate=X(self._data_qubits[0]),
                symptom=[1, 0, 1, 0]
            ),
            Recovery(
                gate=Z(self._data_qubits[0]),
                symptom=[0, 0, 0, 1]
            ),
            Recovery(
                gate=X(self._data_qubits[1]),
                symptom=[0, 1, 0, 1]
            ),
            Recovery(
                gate=Z(self._data_qubits[1]),
                symptom=[1, 0, 0, 0]
            ),
            Recovery(
                gate=X(self._data_qubits[2]),
                symptom=[0, 0, 1, 0]
            ),
            Recovery(
                gate=Z(self._data_qubits[2]),
                symptom=[1, 1, 0, 0]
            ),
            Recovery(
                gate=X(self._data_qubits[3]),
                symptom=[1, 0, 0, 1]
            ),
            Recovery(
                gate=Z(self._data_qubits[3]),
                symptom=[0, 1, 1, 0]
            ),
            Recovery(
                gate=X(self._data_qubits[4]),
                symptom=[0, 1, 0, 0]
            ),
            Recovery(
                gate=Z(self._data_qubits[4]),
                symptom=[0, 0, 1, 1]
            ),

        ]

        syndrome_circuit = Circuit(
            [H(ancilla) for ancilla in self._ancilla_qubits],
            [gate(self._data_qubits[target_index]).controlled_by(self._ancilla_qubits[generator])
             for generator, gates in enumerate(generators) for target_index, gate in enumerate(gates)],
            [H(ancilla) for ancilla in self._ancilla_qubits],
        )
        recovery_circuit = Circuit(
            [recovery.gate.controlled_by(*self._ancilla_qubits, control_values=recovery.symptom)
             for recovery in recoveries]
        )
        circuit = Circuit(
            syndrome_circuit,
            recovery_circuit,
            [R(ancilla) for ancilla in self._ancilla_qubits],
        )
        self._current_state = self._get_state_after_circuit(circuit=circuit)
