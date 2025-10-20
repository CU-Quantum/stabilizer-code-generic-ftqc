from matplotlib import pyplot as plt
from sinter import CSV_HEADER, Task, collect, plot_error_rate
from stim import Circuit

from generalized_shor_code_generators import GeneralizedShorCodeGenerators
from predefined_check_matrix_values import get_check_matrix_values_tetrahedral
from stim_experiments.surface_code.surface_code_stim.cx_from_gsch import CxFromGsch
from stim_experiments.surface_code.surface_code_stim.decoder_by_matrix import DecoderByMatrix
from stim_experiments.surface_code.surface_code_stim.tetrahedral_code import get_stabilizer_code_line


class Main:
    def __init__(self, distance: int):
        self._distance = distance

    def run_main(self):
        surface_code_generators = GeneralizedShorCodeGenerators(num_cats=self._distance, num_qubits_per_cat=self._distance)
        surface_code_symplectic_matrix = surface_code_generators.get_z_generators() + surface_code_generators.get_x_generators()

        samples = collect(
            num_workers=1,
            max_shots=1_000_000,
            max_errors=1000,
            tasks=self.generate_example_tasks(),
            decoders=['decoder_by_matrix'],
            custom_decoders={'decoder_by_matrix': DecoderByMatrix(symplectic_matrix=surface_code_symplectic_matrix)},
        )

        # Print samples as CSV data.
        print(CSV_HEADER)
        for sample in samples:
            print(sample.to_csv_line())

        # Render a matplotlib plot of the data.
        fig, ax = plt.subplots(1, 1)
        plot_error_rate(
            ax=ax,
            stats=samples,
            group_func=lambda stat: f"Rotated Surface Code d={stat.json_metadata['d']}",
            x_func=lambda stat: stat.json_metadata['p'],
        )
        ax.loglog()
        ax.set_ylim(1e-5, 1)
        ax.grid()
        ax.set_title('Logical Error Rate vs Physical Error Rate')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        # Save to file and also open in a window.
        fig.savefig('plot.png')
        plt.show()

    def generate_example_tasks(self):
        for p in [0.001, 0.005, 0.01]:
            yield Task(
                circuit=self.generate_task_circuit(physical_error_rate=p),
                json_metadata={
                    'physical_error_rate': p,
                    'distance': self._distance,
                },
            )

    def generate_task_circuit(self, physical_error_rate: float) -> Circuit:
        surface_code = Circuit.generated(
            rounds=1,
            distance=7,
            code_task=f'surface_code:rotated_memory_z',
        )
        subregister_coords = [
            [(2 * j + 1, 2 * i + 1) for j in range(self._distance)]
            for i in range(self._distance)
        ]

        subregister_indices = [
            [2 * j + 1 + (2 * self._distance + 1) * i for j in range(self._distance)]
            for i in range(self._distance)
        ]

        cat_states_circuit = Circuit()
        for subregister in subregister_indices:
            cat_states_circuit.append('H', subregister[0])
            targets = subregister[1:]
            indices = [j for i in zip([subregister[0]] * len(targets), targets) for j in i]
            cat_states_circuit.append('CX', indices)

        last_qubit_index = 117
        last_qubit_row_coord = 14
        tetrahedral_code = get_stabilizer_code_line(get_check_matrix_values_tetrahedral(), qubit_id_start=last_qubit_index)
        num_data_qubits = 15
        num_ancillas = 14
        tetrahedral_init = Circuit(f"""
            {'\n'.join([f'QUBIT_COORDS({last_qubit_row_coord+1}, {i}) {last_qubit_index + i}' for i in range(num_data_qubits)])}
            {'\n'.join([f'QUBIT_COORDS({last_qubit_row_coord+2}, {i}) {last_qubit_index + num_data_qubits + i}' for i in range(num_ancillas)])}
            
            {tetrahedral_code.without_noise()}
            {f'Z {' '.join([str(last_qubit_index + num_data_qubits + i) for i in range(num_ancillas)])}'}
            {f'R {' '.join([str(last_qubit_index + num_data_qubits + i) for i in range(num_ancillas)])}'}
        """)

        coords_to_index_map = {k:v for k, v in zip([j for i in subregister_coords for j in i], [j for i in subregister_indices for j in i])}
        for i in range(num_data_qubits):
            coords_to_index_map[(last_qubit_row_coord+1, i)] = last_qubit_index + i
        for i in range(num_ancillas):
            coords_to_index_map[(last_qubit_row_coord+2, i)] = last_qubit_index + num_data_qubits + i
        cx_from_gsch = CxFromGsch(surface_coords_to_index=coords_to_index_map, physical_error_rate=physical_error_rate)
        circuit = Circuit(f"""
            QUBIT_COORDS(1, 1) 1
            QUBIT_COORDS(2, 0) 2
            QUBIT_COORDS(3, 1) 3
            QUBIT_COORDS(5, 1) 5
            QUBIT_COORDS(6, 0) 6
            QUBIT_COORDS(7, 1) 7
            QUBIT_COORDS(9, 1) 9
            QUBIT_COORDS(10, 0) 10
            QUBIT_COORDS(11, 1) 11
            QUBIT_COORDS(13, 1) 13
            QUBIT_COORDS(1, 3) 16
            QUBIT_COORDS(2, 2) 17
            QUBIT_COORDS(3, 3) 18
            QUBIT_COORDS(4, 2) 19
            QUBIT_COORDS(5, 3) 20
            QUBIT_COORDS(6, 2) 21
            QUBIT_COORDS(7, 3) 22
            QUBIT_COORDS(8, 2) 23
            QUBIT_COORDS(9, 3) 24
            QUBIT_COORDS(10, 2) 25
            QUBIT_COORDS(11, 3) 26
            QUBIT_COORDS(12, 2) 27
            QUBIT_COORDS(13, 3) 28
            QUBIT_COORDS(14, 2) 29
            QUBIT_COORDS(0, 4) 30
            QUBIT_COORDS(1, 5) 31
            QUBIT_COORDS(2, 4) 32
            QUBIT_COORDS(3, 5) 33
            QUBIT_COORDS(4, 4) 34
            QUBIT_COORDS(5, 5) 35
            QUBIT_COORDS(6, 4) 36
            QUBIT_COORDS(7, 5) 37
            QUBIT_COORDS(8, 4) 38
            QUBIT_COORDS(9, 5) 39
            QUBIT_COORDS(10, 4) 40
            QUBIT_COORDS(11, 5) 41
            QUBIT_COORDS(12, 4) 42
            QUBIT_COORDS(13, 5) 43
            QUBIT_COORDS(1, 7) 46
            QUBIT_COORDS(2, 6) 47
            QUBIT_COORDS(3, 7) 48
            QUBIT_COORDS(4, 6) 49
            QUBIT_COORDS(5, 7) 50
            QUBIT_COORDS(6, 6) 51
            QUBIT_COORDS(7, 7) 52
            QUBIT_COORDS(8, 6) 53
            QUBIT_COORDS(9, 7) 54
            QUBIT_COORDS(10, 6) 55
            QUBIT_COORDS(11, 7) 56
            QUBIT_COORDS(12, 6) 57
            QUBIT_COORDS(13, 7) 58
            QUBIT_COORDS(14, 6) 59
            QUBIT_COORDS(0, 8) 60
            QUBIT_COORDS(1, 9) 61
            QUBIT_COORDS(2, 8) 62
            QUBIT_COORDS(3, 9) 63
            QUBIT_COORDS(4, 8) 64
            QUBIT_COORDS(5, 9) 65
            QUBIT_COORDS(6, 8) 66
            QUBIT_COORDS(7, 9) 67
            QUBIT_COORDS(8, 8) 68
            QUBIT_COORDS(9, 9) 69
            QUBIT_COORDS(10, 8) 70
            QUBIT_COORDS(11, 9) 71
            QUBIT_COORDS(12, 8) 72
            QUBIT_COORDS(13, 9) 73
            QUBIT_COORDS(1, 11) 76
            QUBIT_COORDS(2, 10) 77
            QUBIT_COORDS(3, 11) 78
            QUBIT_COORDS(4, 10) 79
            QUBIT_COORDS(5, 11) 80
            QUBIT_COORDS(6, 10) 81
            QUBIT_COORDS(7, 11) 82
            QUBIT_COORDS(8, 10) 83
            QUBIT_COORDS(9, 11) 84
            QUBIT_COORDS(10, 10) 85
            QUBIT_COORDS(11, 11) 86
            QUBIT_COORDS(12, 10) 87
            QUBIT_COORDS(13, 11) 88
            QUBIT_COORDS(14, 10) 89
            QUBIT_COORDS(0, 12) 90
            QUBIT_COORDS(1, 13) 91
            QUBIT_COORDS(2, 12) 92
            QUBIT_COORDS(3, 13) 93
            QUBIT_COORDS(4, 12) 94
            QUBIT_COORDS(5, 13) 95
            QUBIT_COORDS(6, 12) 96
            QUBIT_COORDS(7, 13) 97
            QUBIT_COORDS(8, 12) 98
            QUBIT_COORDS(9, 13) 99
            QUBIT_COORDS(10, 12) 100
            QUBIT_COORDS(11, 13) 101
            QUBIT_COORDS(12, 12) 102
            QUBIT_COORDS(13, 13) 103
            QUBIT_COORDS(4, 14) 109
            QUBIT_COORDS(8, 14) 113
            QUBIT_COORDS(12, 14) 117
            R 1 3 5 7 9 11 13 16 18 20 22 24 26 28 31 33 35 37 39 41 43 46 48 50 52 54 56 58 61 63 65 67 69 71 73 76 78 80 82 84 86 88 91 93 95 97 99 101 103 2 6 10 17 19 21 23 25 27 29 30 32 34 36 38 40 42 47 49 51 53 55 57 59 60 62 64 66 68 70 72 77 79 81 83 85 87 89 90 92 94 96 98 100 102 109 113 117

            {cat_states_circuit.without_noise()}

            {tetrahedral_init.without_noise()}

            {cx_from_gsch.perform_cx(control_qubit_coords=subregister_coords[0], target_qubit_coords=[(last_qubit_row_coord+1, i) for i in range(len(subregister_coords[0]))])}
        """)
        with open('fds.html', 'w') as f: f.write(str(circuit.diagram(type='timeline-3d-html')))
        return circuit


if __name__ == '__main__':
    Main(distance=7).run_main()
