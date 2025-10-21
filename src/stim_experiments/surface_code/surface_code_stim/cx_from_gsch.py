class CxFromGsch:
    def __init__(self,
                 control_qubit_indices: list[int],
                 target_qubit_indices: list[int],
                 possible_idle_qubit_indices: list[int],
                 physical_error_rate: float = 0.001):
        self._control_qubit_indices = control_qubit_indices
        self._target_qubit_indices = target_qubit_indices
        self._possible_idle_qubit_indices = possible_idle_qubit_indices
        self._physical_error_rate = physical_error_rate

    def perform_cx(self, ):
        control_qubit_pairs = zip(self._control_qubit_indices, self._target_qubit_indices)
        cx_qubits = [coord for coords in control_qubit_pairs for coord in coords]
        idle_qubits = [coord for coord in self._possible_idle_qubit_indices if coord not in cx_qubits]

        return f"""
            CX {' '.join(map(str, cx_qubits))}
            DEPOLARIZE2({self._physical_error_rate}) {' '.join(map(str, cx_qubits))}
            DEPOLARIZE1({self._physical_error_rate}) {' '.join(map(str, idle_qubits))}
        """
