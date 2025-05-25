class RepetitionZStabilizersGenerator:
    def __init__(self, num_qubits: int):
        self._num_qubits = num_qubits

    def get_stabilizers(self) -> list[list[int]]:
        num_parity_checks_per_register = self._num_qubits - 1
        return [
            [self._qubit_has_x_stabilizer_in_generator(parity_check_index=parity_check_index,
                                                       qubit_index=qubit_index)
             for qubit_index in range(self._num_qubits)]
            for parity_check_index in range(num_parity_checks_per_register)
        ]

    def _qubit_has_x_stabilizer_in_generator(self, parity_check_index: int, qubit_index: int) -> int:
        low_index = parity_check_index
        high_index = low_index + 1
        return int(low_index <= qubit_index <= high_index)
