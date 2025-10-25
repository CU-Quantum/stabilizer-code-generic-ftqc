class CxFromGsch:
    def __init__(self,
                 control_qubit_indices: list[int],
                 target_qubit_indices: list[int]):
        self._control_qubit_indices = control_qubit_indices
        self._target_qubit_indices = target_qubit_indices

    def perform_cx(self, ):
        control_qubit_pairs = zip(self._control_qubit_indices, self._target_qubit_indices)
        cx_qubits = [coord for coords in control_qubit_pairs for coord in coords]

        return f"""
            CX {' '.join(map(str, cx_qubits))}
        # """
