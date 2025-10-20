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
            distance=self._distance,
            code_task=f'surface_code:rotated_memory_z',
        )
        subregister_coords = [
            [(1, 1), (3, 1), (5, 1)],
            [(1, 3), (3, 3), (5, 3)],
            [(1, 5), (3, 5), (5, 5)]
        ]
        subregister_indices = [
            [1, 3, 5],
            [8, 10, 12],
            [15, 17, 19]
        ]
        cat_states_circuit = Circuit(f"""
            H 1
            CX 1 3 1 5
            
            H 8
            CX 8 10 8 12
            
            H 15
            CX 15 17 15 19
        """)

        tetrahedral_code = get_stabilizer_code_line(get_check_matrix_values_tetrahedral(), qubit_id_start=26)
        num_data_qubits = 15
        num_ancillas = 14
        tetrahedral_init = Circuit(f"""
            {'\n'.join([f'QUBIT_COORDS(7, {i}) {26 + i}' for i in range(num_data_qubits)])}
            {'\n'.join([f'QUBIT_COORDS(8, {i}) {26 + num_data_qubits + i}' for i in range(num_ancillas)])}
            
            {tetrahedral_code.without_noise()}
            {f'Z {' '.join([str(26 + num_data_qubits + i) for i in range(num_ancillas)])}'}
            {f'R {' '.join([str(26 + num_data_qubits + i) for i in range(num_ancillas)])}'}
        """)

        coords_to_index_map = {k:v for k, v in zip([j for i in subregister_coords for j in i], [j for i in subregister_indices for j in i])}
        for i in range(num_data_qubits):
            coords_to_index_map[(7, i)] = 26 + i
        for i in range(num_ancillas):
            coords_to_index_map[(8, i)] = 26 + num_data_qubits + i
        cx_from_gsch = CxFromGsch(surface_coords_to_index=coords_to_index_map, physical_error_rate=physical_error_rate)
        circuit = Circuit(f"""
            {surface_code.without_noise()}
            
            {cat_states_circuit.without_noise()}
            
            {tetrahedral_init.without_noise()}
            
            {cx_from_gsch.perform_cx(control_qubit_coords=subregister_coords[0], target_qubit_coords=[(7, i) for i in range(len(subregister_coords[0]))])}
            {cx_from_gsch.perform_cx(control_qubit_coords=subregister_coords[1], target_qubit_coords=[(7, len(subregister_coords[0]) + i) for i in range(len(subregister_coords[0]))])}
            {cx_from_gsch.perform_cx(control_qubit_coords=subregister_coords[2], target_qubit_coords=[(7, 2 * len(subregister_coords[0]) + i) for i in range(len(subregister_coords[0]))])}
        """)
        with open('fds.html', 'w') as f: f.write(str(circuit.diagram(type='timeline-3d-html')))
        return circuit


if __name__ == '__main__':
    Main(distance=3).run_main()
