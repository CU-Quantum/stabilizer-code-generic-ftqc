import pytest
from stim import Circuit

from stim_simulations.surface_code import SurfaceCodeStim


@pytest.mark.skip("Not implemented")
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

    @pytest.fixture(autouse=True)
    def _setup_code(self):
        self._code = SurfaceCodeStim(circuit=self._circuit)

    def test_circuit_custom_string(self):
        with open('surface_code_stim.txt', 'r') as file:
            assert self._code.surface_code_string() == file.read()

    def test_data_coordinates(self):
        assert self._code.data_coordinates == [(1, 1), (3, 1), (5, 1), (1, 3), (3, 3), (5, 3), (1, 5), (3, 5), (5, 5)]

    def test_coordinates_to_index_map(self):
        assert self._code.coordinates_to_index_map == {
            (0.0, 4.0): 14,
            (1.0, 1.0): 1,
            (1.0, 3.0): 8,
            (1.0, 5.0): 15,
            (2.0, 0.0): 2,
            (2.0, 2.0): 9,
            (2.0, 4.0): 16,
            (3.0, 1.0): 3,
            (3.0, 3.0): 10,
            (3.0, 5.0): 17,
            (4.0, 2.0): 11,
            (4.0, 4.0): 18,
            (4.0, 6.0): 25,
            (5.0, 1.0): 5,
            (5.0, 3.0): 12,
            (5.0, 5.0): 19,
            (6.0, 2.0): 13
        }
