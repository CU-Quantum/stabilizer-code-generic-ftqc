from stim_simulations.surface_code.surface_code_stim.cx_from_gsch import CxFromGsch


class TestCxFromGsch:
    def test_trivial(self):
        circuit = CxFromGsch(surface_coords_to_index={}, physical_error_rate=0.001).perform_cx(
            control_qubit_coords=[], target_qubit_coords=[]
        )
        assert circuit == '\n    CX \n    DEPOLARIZE2(0.001) \n    DEPOLARIZE1(0.001) \n    TICK\n'

    def test_different_physical_error_rate(self):
        circuit = CxFromGsch(surface_coords_to_index={}, physical_error_rate=0.002).perform_cx(
            control_qubit_coords=[], target_qubit_coords=[]
        )
        assert circuit == '\n    CX \n    DEPOLARIZE2(0.002) \n    DEPOLARIZE1(0.002) \n    TICK\n'

    def test_two_coords(self):
        circuit = CxFromGsch(surface_coords_to_index={(0,0): 0, (0,1): 1, (1,0): 2, (1,1): 3}, physical_error_rate=0.001).perform_cx(
            control_qubit_coords=[(0,0), (0,1)], target_qubit_coords=[(1,0), (1,1)]
        )
        assert circuit == '\n    CX 0 2 1 3\n    DEPOLARIZE2(0.001) 0 2 1 3\n    DEPOLARIZE1(0.001) \n    TICK\n'

    def test_idle_noise(self):
        circuit = CxFromGsch(surface_coords_to_index={(0,0): 0}, physical_error_rate=0.001).perform_cx(
            control_qubit_coords=[], target_qubit_coords=[]
        )
        assert circuit == '\n    CX \n    DEPOLARIZE2(0.001) \n    DEPOLARIZE1(0.001) 0\n    TICK\n'

    def test_coords_and_idle(self):
        circuit = CxFromGsch(surface_coords_to_index={(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 3},
                             physical_error_rate=0.001).perform_cx(
            control_qubit_coords=[(0, 0)], target_qubit_coords=[(0, 1)]
        )
        assert circuit == '\n    CX 0 1\n    DEPOLARIZE2(0.001) 0 1\n    DEPOLARIZE1(0.001) 2 3\n    TICK\n'
