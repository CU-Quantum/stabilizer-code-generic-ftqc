from cirq import Circuit, H, LineQubit, X


class CatStateCreatorFlagPattern:
    """
    Idea comes from https://quantum-journal.org/papers/q-2023-10-24-1154/
    Note that you apparently cannot use this for syndrome measurement.
    """
    def __init__(self, qubit_register: list[LineQubit]):
        self._qubit_register = qubit_register

    def get_cat_state_circuit(self) -> Circuit:
        control_qubit = self._qubit_register[0]
        return Circuit(
            [H(control_qubit)],
            [X(target_qubit).controlled_by(control_qubit) for target_qubit in self._qubit_register[1:]], # TODO make this reversed, and test
        )
