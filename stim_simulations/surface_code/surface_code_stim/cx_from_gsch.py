from stim_simulations.surface_code.surface_code_stim.utilities import index_string, prepare_coords



class CxFromGsch:
    def __init__(self, surface_coords_to_index: dict[tuple[int, int], int], physical_error_rate: float = 0.001):
        self._surface_coords_to_index = surface_coords_to_index
        self._physical_error_rate = physical_error_rate

    def perform_cx(self, control_qubit_coords: list[tuple[int, int]], target_qubit_coords: list[tuple[int, int]]):
        control_qubit_pairs = zip(control_qubit_coords, target_qubit_coords)
        cx_qubits = [coord for coords in control_qubit_pairs for coord in coords]
        idle_qubits = [coord for coord in self._surface_coords_to_index.keys() if coord not in cx_qubits]

        return f"""
    CX {index_string(cx_qubits, self._surface_coords_to_index)}
    DEPOLARIZE2({self._physical_error_rate}) {index_string(cx_qubits, self._surface_coords_to_index)}
    DEPOLARIZE1({self._physical_error_rate}) {index_string(idle_qubits, self._surface_coords_to_index)}
    TICK
"""

