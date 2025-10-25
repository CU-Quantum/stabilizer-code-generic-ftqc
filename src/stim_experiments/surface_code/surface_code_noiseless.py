# https://www.coursera.org/learn/quantum-error-correction/ungradedLab/Ygy3i/surface-code-in-stim-lab/lab?path=%2Fedit%2Fdont_look%2Fcorrect_surface_code.py
from stim_experiments.surface_code.utilities import adjacent_coords, coord_circuit, index_string, \
    prepare_coords


def lattice_without_noise(distance, p):
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

        stim_string += f"""
        CX {index_string(cx_qubits, c2i)}
        TICK
        """

    return stim_string


def stabilizers_without_noise(distance, p):
    datas, x_measures, z_measures, c2i = prepare_coords(distance)
    all_measures = x_measures + z_measures
    all_qubits = datas + all_measures

    stim_string = f"""
    R {index_string(all_measures, c2i)}
    TICK
    H {index_string(x_measures, c2i)}
    TICK
    """

    stim_string += lattice_without_noise(distance, p)

    stim_string += f"""
    H {index_string(x_measures, c2i)}
    TICK
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
    TICK
    H {index_string(x_measures, c2i)}
    TICK
    """

    stim_string += lattice_without_noise(distance, p)

    stim_string += f"""
    H {index_string(x_measures, c2i)}
    TICK
    M {index_string(all_measures, c2i)}
    TICK
    """

    return stim_string


def rounds_step(distance, rounds, p):
    if rounds <= 2:
        return "\n"

    stim_string = f"REPEAT {rounds - 2} {{\n"
    stim_string += stabilizers_without_noise(distance, p)

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
    TICK
    H {index_string(x_measures, c2i)}
    TICK
    """

    stim_string += lattice_without_noise(distance, p)

    stim_string += f"""
    H {index_string(x_measures, c2i)}
    TICK
    M {index_string(all_qubits, c2i)}
    """

    return stim_string


def surface_code_circuit_string(distance, rounds, p):
    string = coord_circuit(distance)
    string += initialization_step(distance, p)
    string += rounds_step(distance, rounds, p)
    string += final_step(distance, p)
    return string
