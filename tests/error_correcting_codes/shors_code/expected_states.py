from functools import cached_property
from typing import List

from cirq import CX, Circuit, H, LineQubit, X, density_matrix_from_state_vector

from stim_experiments.utilities import DENSITY_MATRIX_TYPE


class ExpectedStatesUtilities:
    def get_logical_one_circuit(self) -> Circuit:
        circuit = self.get_logical_zero_circuit()
        circuit.insert(0, X(self.circuit_qubits[0]))
        return circuit

    def get_logical_zero_circuit(self) -> Circuit:
        qubits = self.circuit_qubits
        return Circuit(
            CX(qubits[0], qubits[3]),
            CX(qubits[0], qubits[6]),
            H(qubits[0]),
            H(qubits[3]),
            H(qubits[6]),
            CX(qubits[0], qubits[1]),
            CX(qubits[0], qubits[2]),
            CX(qubits[3], qubits[4]),
            CX(qubits[3], qubits[5]),
            CX(qubits[6], qubits[7]),
            CX(qubits[6], qubits[8]),
        )

    @staticmethod
    def get_expected_state(circuit: Circuit) -> DENSITY_MATRIX_TYPE:
        expected_state = circuit.final_state_vector()
        return density_matrix_from_state_vector(expected_state)

    @cached_property
    def circuit_qubits(self) -> List[LineQubit]:
        return LineQubit.range(9)
