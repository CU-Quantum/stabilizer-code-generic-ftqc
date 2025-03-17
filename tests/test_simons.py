from functools import cached_property

import stim

class RepetitionCodeSimonsAlgorithm:
    def __init__(self, logical_qubits: int):
        self._logical_qubits = logical_qubits

    def get_current_state(self) -> str:
        circuit = stim.Circuit.generated(
            "repetition_code:memory",
            rounds=25,
            distance=9,
            before_round_data_depolarization=0.04,
            before_measure_flip_probability=0.01)

    @cached_property
    def _circuit(self) -> stim.Circuit:
        from surface_code import prepare_coords
        distance = 3
        datas, x_measures, z_measures, c2i = prepare_coords(distance)
        print('data qubits', datas)
        print('x measures', x_measures)
        print('z_measures', z_measures)


class TestSimons:
    def test_zero_state(self):
        simons_code = RepetitionCodeSimonsAlgorithm(logical_qubits=2)
        current_states = simons_code.get_current_states()
        assert current_states == [0, 0]

