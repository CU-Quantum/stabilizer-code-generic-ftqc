import pytest

from stim_experiments.error_correcting_codes.surface_code.coursera_custom.surface_code_coursera_custom import SurfaceCodeCourseraCustom


@pytest.mark.skip("Not implemented")
class TestSurfaceCodeCourseraCustom:
    @pytest.fixture(autouse=True)
    def setup_code(self):
        self._code = SurfaceCodeCourseraCustom(distance=3, error_probability=.2, rounds=3)

    def test_circuit_custom_string(self):
        with open('surface_code_custom.txt', 'r') as file:
            assert self._code.surface_code_string() == file.read()

    def test_data_coordinates(self):
        assert self._code.data_coordinates == [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]

    def test_coordinates_to_index_map(self):
        assert self._code.coordinates_to_index_map == {
            (0.5, 1.5): 13,
            (1, 1): 0,
            (1, 2): 3,
            (1, 3): 6,
            (1.5, 1.5): 10,
            (1.5, 2.5): 15,
            (1.5, 3.5): 12,
            (2, 1): 1,
            (2, 2): 4,
            (2, 3): 7,
            (2.5, 0.5): 9,
            (2.5, 1.5): 14,
            (2.5, 2.5): 11,
            (3, 1): 2,
            (3, 2): 5,
            (3, 3): 8,
            (3.5, 2.5): 16
        }
