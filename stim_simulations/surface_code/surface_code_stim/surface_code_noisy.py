# https://www.coursera.org/learn/quantum-error-correction/ungradedLab/Ygy3i/surface-code-in-stim-lab/lab?path=%2Fedit%2Fdont_look%2Fcorrect_surface_code.py
from stim_simulations.surface_code.surface_code_stim.utilities import adjacent_coords, index_string, prepare_coords


def lattice_with_noise(distance, p):
    datas, x_measures, z_measures, c2i = prepare_coords(distance)

    stim_string = ""
    for i in range(4):
        cx_qubits = []
        for measure in z_measures:
            z_controls = adjacent_coords(measure)
            control = z_controls[i]
            if control in c2i:
                cx_qubits.extend([control, measure])

        for measure in x_measures:
            x_targets = adjacent_coords(measure)
            index_reorder = [0, 2, 1, 3]
            target = x_targets[index_reorder[i]]
            if target in c2i:
                cx_qubits.extend([measure, target])  # flipped order!

        idle_qubits = [coord for coord in c2i.keys() if coord not in cx_qubits]

        stim_string += f"""
        CX {index_string(cx_qubits, c2i)}
        DEPOLARIZE2({p}) {index_string(cx_qubits, c2i)}
        DEPOLARIZE1({p}) {index_string(idle_qubits, c2i)}
        TICK
        """

    return stim_string


def stabilizers_with_noise(distance, p):
    datas, x_measures, z_measures, c2i = prepare_coords(distance)
    all_measures = x_measures + z_measures
    all_qubits = datas + all_measures

    stim_string = f"""
    R {index_string(all_measures, c2i)}
    X_ERROR({p}) {index_string(all_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(datas, c2i)}
    TICK
    H {index_string(x_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(all_qubits, c2i)}
    TICK
    """

    stim_string += lattice_with_noise(distance, p)

    stim_string += f"""
    H {index_string(x_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(all_qubits, c2i)}
    TICK
    X_ERROR({p}) {index_string(all_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(datas, c2i)}
    M {index_string(all_measures, c2i)}
    TICK
    """

    return stim_string


def initialization_step(distance, p):
    datas, x_measures, z_measures, c2i = prepare_coords(distance)
    all_measures = x_measures + z_measures
    all_qubits = datas + all_measures

    stim_string = f"""
    R {index_string(all_qubits, c2i)}
    X_ERROR({p}) {index_string(all_qubits, c2i)}
    TICK
    H {index_string(x_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(all_qubits, c2i)}
    TICK
    """

    stim_string += lattice_with_noise(distance, p)

    stim_string += f"""
    H {index_string(x_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(all_qubits, c2i)}
    TICK
    X_ERROR({p}) {index_string(all_measures, c2i)}
    M {index_string(all_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(datas, c2i)}
    TICK
    """

    for i in range(1, len(z_measures) + 1):
        stim_string += f"DETECTOR({i}, 0) rec[{-i}]\n"
    return stim_string


def rounds_step(distance, rounds, p):
    if rounds <= 2:
        return "\n"
    datas, x_measures, z_measures, c2i = prepare_coords(distance)

    stim_string = f"REPEAT {rounds - 2} {{\n"
    stim_string += stabilizers_with_noise(distance, p)

    num_measures_per_type = len(z_measures)  # number of measures per type per round
    for i in range(1, num_measures_per_type + 1):  # offset to the previous round
        stim_string += f"DETECTOR({i}, 0) rec[{-i}] rec[{-(i + 2 * num_measures_per_type)}]\n"
    for i in range(1, num_measures_per_type + 1):  # offset to the other type and to the previous round
        stim_string += f"DETECTOR({i}, 0) rec[{-(i + num_measures_per_type)}] rec[{-(i + 3 * num_measures_per_type)}]\n"

    stim_string += """
    }
    """  # end repeat block

    return stim_string


def final_step(distance, p):
    datas, x_measures, z_measures, c2i = prepare_coords(distance)
    all_measures = x_measures + z_measures
    all_qubits = datas + all_measures

    stim_string = f"""
    R {index_string(all_measures, c2i)}
    X_ERROR({p}) {index_string(all_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(datas, c2i)}
    TICK
    H {index_string(x_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(all_qubits, c2i)}
    TICK
    """

    stim_string += lattice_with_noise(distance, p)

    stim_string += f"""
    H {index_string(x_measures, c2i)}
    DEPOLARIZE1({p}) {index_string(all_qubits, c2i)}
    TICK
    X_ERROR({p}) {index_string(all_qubits, c2i)}
    M {index_string(all_qubits, c2i)}
    """
    # remember measure order is datas, x_measures, z_measures
    # do previous-round detectors first
    num_measures_per_type = len(z_measures)  # number of measures per type per round
    num_datas = len(datas)
    for i in range(1, num_measures_per_type + 1):  # offset to the previous round
        stim_string += f"DETECTOR({i}, 0) rec[{-i}] rec[{-(i + 2 * num_measures_per_type + num_datas)}]\n"
    for i in range(1, num_measures_per_type + 1):  # offset to the other type and to the previous round
        stim_string += f"DETECTOR({i}, 0) rec[{-(i + num_measures_per_type)}] rec[{-(i + 3 * num_measures_per_type + num_datas)}]\n"

    # now the confusing one: the final data measurements and their adjacent measure measurements
    # create a dict that maps each coord to the record index of the most recent measurement on it
    coord_to_record_index = {coord: i - len(all_qubits) for i, coord in enumerate(all_qubits)}
    for i, measure in enumerate(z_measures):
        record_indices = []
        record_indices.append(coord_to_record_index[measure])
        adjacent_datas = adjacent_coords(measure)

        for data in adjacent_datas:
            if data in all_qubits:
                record_indices.append(coord_to_record_index[data])
        recs = [f"rec[{j}]" for j in record_indices]
        stim_string += f"DETECTOR({i}, 0) {' '.join(recs)}\n"

    obs_recs = [f"rec[{-(i + 2 * num_measures_per_type)}]" for i in range(1, distance + 1)]
    stim_string += f"OBSERVABLE_INCLUDE(0) {' '.join(obs_recs)}"

    return stim_string


def surface_code_circuit_string(distance, rounds, p):
    string = coord_circuit(distance)
    string += initialization_step(distance, p)
    string += rounds_step(distance, rounds, p)
    string += final_step(distance, p)
    return string
