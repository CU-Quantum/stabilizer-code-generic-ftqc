from stim_experiments.surface_code.coursera_custom.surface_code import SurfaceCode


class TestSurfaceCode:
    def test_circuit_custom_string(self):
        code = SurfaceCode(distance=3, error_probability=.2, rounds=3)
        with open('surface_code_custom.txt', 'r') as file:
            assert code.surface_code_circuit_string() == file.read()
