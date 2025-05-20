from stim_experiments.utilities.repetition_z_stabilizers_generator import RepetitionZStabilizersGenerator


class RepetitionZStabilizersMulticatGenerator:
    def __init__(self, num_qubits_in_cat: int, num_cats: int):
        self._num_qubits_in_cat = num_qubits_in_cat
        self._num_cats = num_cats

    def get_stabilizers(self) -> list[list[int]]:
        num_data_qubits = self._num_qubits_in_cat * self._num_cats

        z_stabilizers_in_cat_state = RepetitionZStabilizersGenerator(
            num_qubits=self._num_qubits_in_cat).get_stabilizers()
        pauli_x_portion_of_z_stabilizers = [0] * num_data_qubits
        return [
            pauli_x_portion_of_z_stabilizers
            + [0] * cat_index * self._num_qubits_in_cat
            + stabilizer
            + [0] * (self._num_cats - cat_index - 1) * self._num_qubits_in_cat
            for cat_index in range(self._num_cats)
            for stabilizer in z_stabilizers_in_cat_state
        ]
