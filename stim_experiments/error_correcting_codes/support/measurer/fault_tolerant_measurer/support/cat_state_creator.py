from cirq import Circuit, H, LineQubit, X

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator


class CatStateCreatorCxFromFirstQubit(CatStateCreator):
    # TODO test this class
    def __init__(self, qubit_register: list[LineQubit]):
        super().__init__(qubit_register=qubit_register)
        self._qubit_register = qubit_register

    def get_cat_state_circuit(self) -> Circuit:
        if not self._qubit_register:
            return Circuit()
        return Circuit(
            H(self._qubit_register[0]),
            [X(self._qubit_register[i]).controlled_by(self._qubit_register[0]) for i in range(1, len(self._qubit_register))],
        )
