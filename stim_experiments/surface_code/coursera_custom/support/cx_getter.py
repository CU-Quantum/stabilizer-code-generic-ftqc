from stim_experiments.surface_code.coursera_custom.support.utilities import adjacent_coords, index_string


class CxGetter:
    def __init__(self, step_number, error_probability, datas, x_measures, z_measures, all_indices, c2i):
        self._datas = datas
        self._step_number = step_number
        self._error_probability = error_probability
        self._x_measures = x_measures
        self._z_measures = z_measures
        self._all_indices = all_indices
        self._c2i = c2i

        self._cx_pairs_cache = None

    def get_step(self):
        return f"""
            CX {self._get_cx_pairs_indices()}
            DEPOLARIZE2({self._error_probability}) {self._get_cx_pairs_indices()}
            DEPOLARIZE1({self._error_probability}) {self._get_depolarize_1_indices()}
            TICK
            """

    def _get_depolarize_1_indices(self):
        return " ".join(
            [str(index) for index in self._all_indices if str(index) not in self._get_cx_pairs_indices().split(" ")])

    def _get_cx_pairs_indices(self):
        return index_string(self._get_cx_pairs(), self._c2i)

    def _get_cx_pairs(self):
        if not self._cx_pairs_cache:
            xs = sum((self._get_x_stabilizers(data_coord) for data_coord in self._datas), [])
            zs = sum((self._get_z_stabilizers(data_coord) for data_coord in self._datas), [])
            self._cx_pairs_cache = zs + xs
        return self._cx_pairs_cache

    def _get_x_stabilizers(self, data_coord):
        is_second_half = self._step_number // 2
        is_odd_step = self._step_number % 2
        adjacent_index = 2 + (not is_second_half) - 2 * is_odd_step

        stabilizer_coord = adjacent_coords(data_coord)[adjacent_index]
        if stabilizer_coord in self._x_measures:
            return [stabilizer_coord, data_coord]
        return []

    def _get_z_stabilizers(self, data_coord):
        stabilizer_coord = adjacent_coords(data_coord)[3 - self._step_number]
        if stabilizer_coord in self._z_measures:
            return [data_coord, stabilizer_coord]
        return []
