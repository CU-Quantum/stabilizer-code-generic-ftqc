from stim_experiments.surface_code.coursera_custom.surface_code_coursera_custom import SurfaceCodeCourseraCustom


class TestSurfaceCodeCourseraCustom:
    def test_circuit_custom_string(self):
        code = SurfaceCodeCourseraCustom(distance=3, error_probability=.2, rounds=3)
        with open('surface_code_custom.txt', 'r') as file:
            assert code.circuit_string() == file.read()

    def test_data_coordinates(self):
        code = SurfaceCodeCourseraCustom(distance=3, error_probability=.2, rounds=3)
        assert code.data_coordinates == [(1, 1), (2, 1), (3, 1), (1, 2), (2, 2), (3, 2), (1, 3), (2, 3), (3, 3)]
