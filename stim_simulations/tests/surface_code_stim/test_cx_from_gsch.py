from stim_simulations.surface_code.surface_code_stim.cx_from_gsch import CxFromGsch


class TestCxFromGsch:
    def test_trivial(self):
        circuit = CxFromGsch(surface_coords_to_index={}, physical_error_rate=0.001).perform_cx(
            control_qubit_coords=[], target_qubit_coords=[]
        )
        assert circuit == '\n    CX \n    DEPOLARIZE2(0.001) \n    DEPOLARIZE1(0.001) \n    TICK\n'
