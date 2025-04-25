from cirq import Circuit, Gate, LineQubit


class ControlledSingleQubitGatesApplier:
    def __init__(self, gates: list[Gate], targets: list[LineQubit], controls: list[LineQubit]):
        self._gates = gates
        self._targets = targets
        self._controls = controls

    def get_circuit(self) -> Circuit:
        self._validate_inputs()
        return Circuit(
            self._gates[i].on(self._targets[i]).controlled_by(self._controls[i])
            for i in range(len(self._gates))
        )

    def _validate_inputs(self) -> None:
        if len(self._gates) != len(self._targets) or len(self._gates) != len(self._controls):
            raise ValueError(
                f"The number of gates ({len(self._gates)}), targets ({len(self._targets)}), and controls({len(self._controls)}) must be equal.")
        if any(gate.num_qubits() != 1 for gate in self._gates):
            raise ValueError(f"All gates must be single-qubit gates. Was given {self._gates}.")
