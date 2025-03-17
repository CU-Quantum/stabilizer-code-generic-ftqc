from stim_experiments.surface_code.coursera_custom.surface_code_coursera_custom import SurfaceCodeCourseraCustom


class TestSurfaceCode:
    def test_circuit_custom_string(self):
        code = SurfaceCodeCourseraCustom(distance=3, error_probability=.2, rounds=3)
        with open('surface_code_custom.txt', 'r') as file:
            assert code.circuit_string() == file.read()
