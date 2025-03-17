from typing import List, Tuple

from stim import Circuit

from stim_experiments.error_correcting_code.error_correcting_code import ErrorCorrectingCode


class SurfaceCodeStim(ErrorCorrectingCode):
    def __init__(self, circuit: Circuit):
        self._circuit = circuit

    def circuit_string(self) -> str:
        return str(repr(self._circuit))

    @property
    def data_coordinates(self) -> List[Tuple[float, float]]:
        distance = int((self._circuit.num_qubits + 1) ** (1/3))
        return [(j * 2 + 1, i * 2 + 1) for i in range(distance) for j in range(distance)]


class TestSurfaceCodeCourseraCustom:
    _error_probability = .2
    _circuit = Circuit.generated(
        "surface_code:rotated_memory_z",
        rounds=3,
        distance=3,
        after_clifford_depolarization=_error_probability,
        after_reset_flip_probability=_error_probability,
        before_measure_flip_probability=_error_probability,
        before_round_data_depolarization=_error_probability,
    )

    def test_circuit_custom_string(self):
        code = SurfaceCodeStim(circuit=self._circuit)
        with open('surface_code_stim.txt', 'r') as file:
            assert code.circuit_string() == file.read()

    def test_data_coordinates(self):
        code = SurfaceCodeStim(circuit=self._circuit)
        assert code.data_coordinates == [(1, 1), (3, 1), (5, 1), (1, 3), (3, 3), (5, 3), (1, 5), (3, 5), (5, 5)]
