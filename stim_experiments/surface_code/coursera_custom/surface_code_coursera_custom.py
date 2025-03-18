from typing import Dict, Iterable, List, Tuple

from stim_experiments.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.surface_code.coursera_custom.support.cx_getter import CxGetter
from stim_experiments.surface_code.coursera_custom.support.utilities import adjacent_coords, coord_circuit, index_string, prepare_coords


class SurfaceCodeCourseraCustom(ErrorCorrectingCode):
    def __init__(self, distance: int, error_probability: float, rounds: int):
        super().__init__()
        self._distance = distance
        self._error_probability = error_probability
        self._rounds = rounds

    def surface_code_string(self) -> str:
        string = coord_circuit(self._distance)
        string += self._initialization_step()
        string += self._rounds_step()
        string += self._final_step()
        return string

    def _initialization_step(self) -> str:
        # Use `lattice_with_noise` to create the first round of stabilizer
        #  measurements in the surface code. Reference but don't use
        #  `stabilizers_with_noise`. Add first-round detectors.

        detectors_z = "\n".join([f"DETECTOR({index + 1},0) rec[-{index + 1}]" for index in range(len(self._z_measures))])

        final = f"""
        R {index_string(self._all_qubits, self._coordinates_to_index_map)}
        X_ERROR({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        H {index_string(self._x_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        {self._lattice_with_noise()}
    
        H {index_string(self._x_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        X_ERROR({self._error_probability}) {index_string(self._all_measures, self._coordinates_to_index_map)}
        M {index_string(self._x_measures, self._coordinates_to_index_map)} {index_string(self._z_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self.data_coordinates, self._coordinates_to_index_map)}
        TICK
    
        {detectors_z}
        """
        return final

    def _lattice_with_noise(self) -> str:
        all_indices = [self._coordinates_to_index_map[index] for index in self.data_coordinates + self._x_measures + self._z_measures]
        # create a stim circuit string for just the lattice of CX gates
        #  required by the stabilizers.

        steps = [CxGetter(i, self._error_probability, self.data_coordinates, self._x_measures, self._z_measures, all_indices, self._coordinates_to_index_map).get_step() for i in range(4)]
        final = "\n".join(steps)
        return final

    def _rounds_step(self) -> str:
        # Use `stabilizers_with_noise` to implement the `REPEAT` block of
        #  stabilizers. Include the mid-round detectors.
        all_detectors = self._x_measures + self._z_measures

        detectors_x = "\n".join([
            f"DETECTOR({index + 1},0) rec[-{index + 1 + len(self._z_measures)}] rec[-{index + 1 + len(self._z_measures) + len(all_detectors)}]"
            for index in range(len(self._x_measures))])

        detectors_z = "\n".join(
            [f"DETECTOR({index + 1},0) rec[-{index + 1}] rec[-{index + 1 + len(all_detectors)}]" for index in
             range(len(self._z_measures))])

        stim_string = f"""
        REPEAT {self._rounds - 2} {{
            {self._stabilizers_with_noise()}
            {detectors_z}
            {detectors_x}
        }}
        """
        return stim_string

    def _stabilizers_with_noise(self) -> str:
        # Use `lattice_with_noise` to create a full lattice of stabilizers
        #  including the resets and measurements. No detectors yet.

        x_resets = []
        return f"""
        R {index_string(self._all_measures, self._coordinates_to_index_map)}
        X_ERROR({self._error_probability}) {index_string(self._all_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self.data_coordinates, self._coordinates_to_index_map)}
        TICK
    
        H {index_string(self._x_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        {self._lattice_with_noise()}
    
        H {index_string(self._x_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        X_ERROR({self._error_probability}) {index_string(self._all_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self.data_coordinates, self._coordinates_to_index_map)}
        M {index_string(self._all_measures, self._coordinates_to_index_map)}
        TICK
        """

    def _final_step(self) -> str:
        # Use `lattice_with_noise` to implement the final round of stabilizer
        #  measurements and the final data measurements. Add the last round
        #  detectors, the final data measure detectors, and the
        #  `OBSERVABLE_INCLUDE` instruction.

        detectors_x = "\n".join([
            f"DETECTOR({index + 1},0) rec[-{index + 1 + len(self._z_measures)}] rec[-{index + 1 + len(self._z_measures) + len(self._all_qubits)}]"
            for index in range(len(self._x_measures))])

        detectors_z = "\n".join(
            [f"DETECTOR({index + 1},0) rec[-{index + 1}] rec[-{index + 1 + len(self._all_qubits)}]" for index in
             range(len(self._z_measures))])

        detectors_three = "\n".join([
            f"DETECTOR({index},0) rec[-{len(self._z_measures) - index}] {' '.join([f'rec[-{len(self._all_qubits) - self._coordinates_to_index_map[adjacent_coord]}]' for adjacent_coord in adjacent_coords(z_meas_coord) if adjacent_coord in self.data_coordinates])}"
            for index, z_meas_coord in enumerate(self._z_measures)])

        stim_string = f"""
        R {index_string(self._all_measures, self._coordinates_to_index_map)}
        X_ERROR({self._error_probability}) {index_string(self._all_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self.data_coordinates, self._coordinates_to_index_map)}
        TICK
    
        H {index_string(self._x_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        {self._lattice_with_noise()}
    
        H {index_string(self._x_measures, self._coordinates_to_index_map)}
        DEPOLARIZE1({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        TICK
    
        X_ERROR({self._error_probability}) {index_string(self._all_qubits, self._coordinates_to_index_map)}
        M {index_string(self.data_coordinates, self._coordinates_to_index_map)} {index_string(self._x_measures, self._coordinates_to_index_map)} {index_string(self._z_measures, self._coordinates_to_index_map)}
    
        {detectors_z}
        {detectors_x}
        {detectors_three}
    
        OBSERVABLE_INCLUDE(0) {' '.join(f'rec[-{len(self._all_measures) + 1 + i}]' for i in range(self._distance))}
        """
        return stim_string

    @property
    def _all_qubits(self) -> List[Tuple[float, float]]:
        return self.data_coordinates + self._all_measures

    @property
    def data_coordinates(self) -> List[Tuple[float, float]]:
        return self._prepared_coords[0]

    @property
    def _all_measures(self) -> List[Tuple[float, float]]:
        return self._x_measures + self._z_measures

    @property
    def _x_measures(self) -> List[Tuple[float, float]]:
        return self._prepared_coords[1]

    @property
    def _z_measures(self) -> List[Tuple[float, float]]:
        return self._prepared_coords[2]

    @property
    def coordinates_to_index_map(self) -> Dict[Iterable[float], int]:
        return self._prepared_coords[3]

    @property
    def _prepared_coords(self) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]], List[Tuple[float, float]], Dict[Tuple[float, float], int]]:
        return prepare_coords(self._distance)
