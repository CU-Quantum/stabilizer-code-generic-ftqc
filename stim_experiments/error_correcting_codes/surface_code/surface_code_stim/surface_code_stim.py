from typing import Dict, Iterable, List, Tuple

from stim import Circuit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code_stim import ErrorCorrectingCodeStim


class SurfaceCodeStim(ErrorCorrectingCodeStim):
    def __init__(self, circuit: Circuit):
        super().__init__()
        self._circuit = circuit

    def surface_code_string(self) -> str:
        self._circuit.get_final_qubit_coordinates()
        return str(repr(self._circuit))

    @property
    def data_coordinates(self) -> List[Tuple[float, float]]:
        distance = int((self._circuit.num_qubits + 1) ** (1/3))
        return [(j * 2 + 1, i * 2 + 1) for i in range(distance) for j in range(distance)]

    @property
    def coordinates_to_index_map(self) -> Dict[Iterable[float], int]:
        return {tuple(y): x for x, y in self._circuit.get_final_qubit_coordinates().items()}
