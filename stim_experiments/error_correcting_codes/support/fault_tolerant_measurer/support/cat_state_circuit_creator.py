from cirq import Circuit, H, LineQubit, X


class CatStateCircuitCreator:
    def __init__(self, target_qubits: list[LineQubit] = None):
        self._target_qubits = target_qubits

    def create_circuit(self) -> Circuit:
        if not self._target_qubits:
            return Circuit()
        return Circuit(
            H(self._target_qubits[0]),
            [X(self._target_qubits[i]).controlled_by(self._target_qubits[i - 1]) for i in range(1, len(self._target_qubits))]
        )
