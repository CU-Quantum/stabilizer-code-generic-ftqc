from cirq import Circuit, H, LineQubit, X


class StatePropagator:
    # TODO test this class
    def __init__(self, target_qubits: list[LineQubit], first_qubit_preparer: Circuit):
        self._target_qubits = target_qubits
        self._first_qubit_preparer = first_qubit_preparer

    def create_circuit(self) -> Circuit:
        if not self._target_qubits:
            return Circuit()
        return Circuit(
            self._first_qubit_preparer,
            [X(self._target_qubits[i]).controlled_by(self._target_qubits[i - 1]) for i in range(1, len(self._target_qubits))]
        )
