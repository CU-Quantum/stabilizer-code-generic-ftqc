from stim_experiments.surface_code.coursera_custom.support.cx_getter import CxGetter
from stim_experiments.surface_code.coursera_custom.support.utilities import adjacent_coords, coord_circuit, index_string, prepare_coords


class SurfaceCode:
    def __init__(self, distance: int, error_probability: float, rounds: int):
        self._distance = distance
        self._error_probability = error_probability
        self._rounds = rounds

    def surface_code_circuit_string(self) -> str:
        string = coord_circuit(self._distance)
        string += self._initialization_step()
        string += self._rounds_step()
        string += self._final_step()
        return string


    def _initialization_step(self) -> str:
        datas, x_measures, z_measures, c2i = prepare_coords(self._distance)
        all_measures = x_measures + z_measures
        all_qubits = datas + all_measures
        # Use `lattice_with_noise` to create the first round of stabilizer
        #  measurements in the surface code. Reference but don't use
        #  `stabilizers_with_noise`. Add first-round detectors.

        detectors_z = "\n".join([f"DETECTOR({index + 1},0) rec[-{index + 1}]" for index in range(len(z_measures))])

        final = f"""
        R {index_string(all_qubits, c2i)}
        X_ERROR({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        H {index_string(x_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        {self._lattice_with_noise()}
    
        H {index_string(x_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        X_ERROR({self._error_probability}) {index_string(all_measures, c2i)}
        M {index_string(x_measures, c2i)} {index_string(z_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(datas, c2i)}
        TICK
    
        {detectors_z}
        """
        return final

    def _lattice_with_noise(self) -> str:
        datas, x_measures, z_measures, c2i = prepare_coords(self._distance)
        all_indices = [c2i[index] for index in datas + x_measures + z_measures]
        # create a stim circuit string for just the lattice of CX gates
        #  required by the stabilizers.

        steps = [CxGetter(i, self._error_probability, datas, x_measures, z_measures, all_indices, c2i).get_step() for i in range(4)]
        final = "\n".join(steps)
        return final


    def _rounds_step(self) -> str:
        datas, x_measures, z_measures, c2i = prepare_coords(self._distance)
        # Use `stabilizers_with_noise` to implement the `REPEAT` block of
        #  stabilizers. Include the mid-round detectors.
        all_detectors = x_measures + z_measures

        detectors_x = "\n".join([
            f"DETECTOR({index + 1},0) rec[-{index + 1 + len(z_measures)}] rec[-{index + 1 + len(z_measures) + len(all_detectors)}]"
            for index in range(len(x_measures))])

        detectors_z = "\n".join(
            [f"DETECTOR({index + 1},0) rec[-{index + 1}] rec[-{index + 1 + len(all_detectors)}]" for index in
             range(len(z_measures))])

        stim_string = f"""
        REPEAT {self._rounds - 2} {{
            {self._stabilizers_with_noise()}
            {detectors_z}
            {detectors_x}
        }}
        """
        return stim_string


    def _stabilizers_with_noise(self) -> str:
        datas, x_measures, z_measures, c2i = prepare_coords(self._distance)
        all_measures = x_measures + z_measures
        all_qubits = datas + all_measures
        # Use `lattice_with_noise` to create a full lattice of stabilizers
        #  including the resets and measurements. No detectors yet.

        x_resets = []
        return f"""
        R {index_string(all_measures, c2i)}
        X_ERROR({self._error_probability}) {index_string(all_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(datas, c2i)}
        TICK
    
        H {index_string(x_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        {self._lattice_with_noise()}
    
        H {index_string(x_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        X_ERROR({self._error_probability}) {index_string(all_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(datas, c2i)}
        M {index_string(all_measures, c2i)}
        TICK
        """


    def _final_step(self) -> str:
        datas, x_measures, z_measures, c2i = prepare_coords(self._distance)
        all_measures = x_measures + z_measures
        all_qubits = datas + all_measures
        # Use `lattice_with_noise` to implement the final round of stabilizer
        #  measurements and the final data measurements. Add the last round
        #  detectors, the final data measure detectors, and the
        #  `OBSERVABLE_INCLUDE` instruction.

        detectors_x = "\n".join([
            f"DETECTOR({index + 1},0) rec[-{index + 1 + len(z_measures)}] rec[-{index + 1 + len(z_measures) + len(all_qubits)}]"
            for index in range(len(x_measures))])

        detectors_z = "\n".join(
            [f"DETECTOR({index + 1},0) rec[-{index + 1}] rec[-{index + 1 + len(all_qubits)}]" for index in
             range(len(z_measures))])

        detectors_three = "\n".join([
            f"DETECTOR({index},0) rec[-{len(z_measures) - index}] {' '.join([f'rec[-{len(all_qubits) - c2i[adjacent_coord]}]' for adjacent_coord in adjacent_coords(z_meas_coord) if adjacent_coord in datas])}"
            for index, z_meas_coord in enumerate(z_measures)])

        stim_string = f"""
        R {index_string(all_measures, c2i)}
        X_ERROR({self._error_probability}) {index_string(all_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(datas, c2i)}
        TICK
    
        H {index_string(x_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        {self._lattice_with_noise()}
    
        H {index_string(x_measures, c2i)}
        DEPOLARIZE1({self._error_probability}) {index_string(all_qubits, c2i)}
        TICK
    
        X_ERROR({self._error_probability}) {index_string(all_qubits, c2i)}
        M {index_string(datas, c2i)} {index_string(x_measures, c2i)} {index_string(z_measures, c2i)}
    
        {detectors_z}
        {detectors_x}
        {detectors_three}
    
        OBSERVABLE_INCLUDE(0) {' '.join(f'rec[-{len(all_measures) + 1 + i}]' for i in range(self._distance))}
        """
        return stim_string
