from cirq import Circuit, H, LineQubit, inverse

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.utilities.utilities import cx_sequentially_further_qubits_from_first


class CatStateCreatorCxFromFirstQubit(CatStateCreator):
    def __init__(self, qubit_register: list[LineQubit]):
        super().__init__(qubit_register=qubit_register)
        self._qubit_register = qubit_register

    def get_cat_state_circuit(self) -> Circuit:
        if not self._qubit_register:
            return Circuit()
        return Circuit(
            H(self._qubit_register[0]),
            cx_sequentially_further_qubits_from_first(qubits=self._qubit_register),
        )

    def decode_state(self) -> Circuit:
        return inverse(self.get_cat_state_circuit())
