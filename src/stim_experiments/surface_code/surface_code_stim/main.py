import numpy as np
from matplotlib import pyplot as plt
from sinter import CSV_HEADER, Task, collect, plot_error_rate
from stim import Circuit

from generalized_shor_code_generators import GeneralizedShorCodeGenerators
from predefined_check_matrix_values import get_check_matrix_values_tetrahedral
from stim_experiments.surface_code.surface_code_stim.cx_from_gsch import CxFromGsch
from stim_experiments.surface_code.surface_code_stim.decoder_by_matrix import DecoderByMatrix
from stim_experiments.surface_code.surface_code_stim.stabilizer_code_utilities import StabilizerCodeUtilities


class Main:
    def __init__(self, distance: int):
        self._distance = distance

    def run_main(self):
        combined_symplectic_matrix, observable = self.get_combined_symplectic()

        samples = collect(
            num_workers=5,
            max_shots=1_000_000,
            max_errors=1000,
            tasks=self.generate_example_tasks(),
            decoders=['decoder_by_matrix'],
            custom_decoders={'decoder_by_matrix': DecoderByMatrix(symplectic_matrix=combined_symplectic_matrix, distance=self._distance, observables=np.array([observable]))},
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
            group_func=lambda stat: f"Rotated Surface Code d={stat.json_metadata['distance']}",
            x_func=lambda stat: stat.json_metadata['physical_error_rate'],
        )
        ax.loglog()
        ax.set_ylim(1e-5, 1)
        ax.grid()
        ax.set_title('Logical Error Rate vs Physical Error Rate')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        # Save to file and also open in a window.
        # fig.savefig('plot.png')
        plt.show()

    def get_combined_symplectic(self):
        shor_code_generators = GeneralizedShorCodeGenerators(num_cats=self._distance, num_qubits_per_cat=self._distance)
        shor_code_symplectic_matrix = np.array(
            shor_code_generators.get_z_generators() + shor_code_generators.get_x_generators())
        t_native_symplectic_matrix = get_check_matrix_values_tetrahedral()
        combined_symplectic_matrix_shor = np.concatenate([
            shor_code_symplectic_matrix[:, :shor_code_symplectic_matrix.shape[1] // 2],
            np.zeros((shor_code_symplectic_matrix.shape[0], t_native_symplectic_matrix.shape[1] // 2)),
            shor_code_symplectic_matrix[:, shor_code_symplectic_matrix.shape[1] // 2:],
            np.zeros((shor_code_symplectic_matrix.shape[0], t_native_symplectic_matrix.shape[1] // 2)),
        ], axis=1)
        combined_symplectic_matrix_t_native = np.concatenate([
            np.zeros((t_native_symplectic_matrix.shape[0], shor_code_symplectic_matrix.shape[1] // 2)),
            t_native_symplectic_matrix[:, :t_native_symplectic_matrix.shape[1] // 2],
            np.zeros((t_native_symplectic_matrix.shape[0], shor_code_symplectic_matrix.shape[1] // 2)),
            t_native_symplectic_matrix[:, t_native_symplectic_matrix.shape[1] // 2:],
        ], axis=1)
        combined_symplectic_matrix_shor[-self._distance + 1][
            [shor_code_symplectic_matrix.shape[1] // 2 + i for i in range(7)]] = np.ones(7)
        combined_symplectic_matrix = np.concatenate(
            [combined_symplectic_matrix_shor, combined_symplectic_matrix_t_native])

        observable = np.zeros(combined_symplectic_matrix.shape[1])
        observable[observable.shape[0] // 2 + 1] = 1
        observable[
            [observable.shape[0] // 2 + shor_code_symplectic_matrix.shape[1] // 2 + i for i in range(3)]] = np.ones(3)

        return combined_symplectic_matrix, observable

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
        shor_code_generators = GeneralizedShorCodeGenerators(num_cats=self._distance, num_qubits_per_cat=self._distance)
        shor_code_symplectic_matrix = shor_code_generators.get_z_generators() + shor_code_generators.get_x_generators()
        shor_anticommutors = [
            np.concatenate([np.ones(np.argmax(shor_code_symplectic_matrix[i][-len(shor_code_symplectic_matrix[0]) // 2 - 1:])), np.zeros(len(shor_code_symplectic_matrix[0]) - np.argmax(shor_code_symplectic_matrix[i][-len(shor_code_symplectic_matrix[0]) // 2 - 1:]))])
             if i <= len(shor_code_symplectic_matrix) - self._distance
             else np.concatenate([np.zeros(len(shor_code_symplectic_matrix[0]) // 2), [int(not j % self._distance and j // self._distance < i - (len(shor_code_symplectic_matrix) - self._distance)) for j in range(len(shor_code_symplectic_matrix[0]) // 2)]])
            for i in range(len(shor_code_symplectic_matrix))
        ]
        generalized_shor_code_utilities = StabilizerCodeUtilities(np.array(shor_code_symplectic_matrix), np.array(shor_anticommutors))

        last_qubit_index = generalized_shor_code_utilities.ancilla_indices[-1]
        last_qubit_row_coord = 1
        t_native_anticommutors = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        ])
        t_native_code_utiilities = StabilizerCodeUtilities(get_check_matrix_values_tetrahedral(), t_native_anticommutors, qubit_id_start=last_qubit_index+1, row_coord_start=last_qubit_row_coord+1)
        num_qubits_for_x_obs_in_t_native = 7
        num_qubits_for_z_obs_in_t_native = 3

        shor_data_subregister_indices = [generalized_shor_code_utilities.data_indices[i * self._distance:(i + 1) * self._distance] for i in range(self._distance)]
        all_data_indices = generalized_shor_code_utilities.data_indices + t_native_code_utiilities.data_indices

        cx_from_gsch = CxFromGsch(control_qubit_indices=shor_data_subregister_indices[0],
                                  target_qubit_indices=t_native_code_utiilities.data_indices[:num_qubits_for_x_obs_in_t_native],
                                  possible_idle_qubit_indices=all_data_indices,
                                  physical_error_rate=physical_error_rate)

        cat_states_circuit = Circuit()
        for subregister in shor_data_subregister_indices:
            cat_states_circuit.append('H', subregister[0])
            targets = subregister[1:]
            indices = [j for i in zip([subregister[0]] * len(targets), targets) for j in i]
            cat_states_circuit.append('CX', indices)

        modified_ancilla = generalized_shor_code_utilities.ancilla_indices[-self._distance + 1]
        modified_stabilizer = f"""
            H {modified_ancilla}
            CX {' '.join(str(j) for i in zip([modified_ancilla] * num_qubits_for_x_obs_in_t_native, t_native_code_utiilities.data_indices[:num_qubits_for_x_obs_in_t_native]) for j in i)}
            H {modified_ancilla}
        """

        circuit = Circuit(f"""
            {generalized_shor_code_utilities.get_init()}
            {t_native_code_utiilities.get_init()}

            TICK
            {cat_states_circuit}
            {t_native_code_utiilities.get_encoding_by_stabilizer()}

            TICK
            {cx_from_gsch.perform_cx()}

            TICK
            {generalized_shor_code_utilities.get_stabilizers()}
            {t_native_code_utiilities.get_stabilizers()}
            {modified_stabilizer}
            TICK
            {f'MR {' '.join(map(str, generalized_shor_code_utilities.ancilla_indices))}'}
            {f'MR {' '.join(map(str, t_native_code_utiilities.ancilla_indices))}'}

            {'\n'.join([f'DETECTOR rec[{-len(generalized_shor_code_utilities.ancilla_indices) - len(t_native_code_utiilities.ancilla_indices) + i}]' for i in range(len(generalized_shor_code_utilities.ancilla_indices))])}
            {'\n'.join([f'DETECTOR rec[{-len(t_native_code_utiilities.ancilla_indices) + i}]' for i in range(len(t_native_code_utiilities.ancilla_indices))])}

            TICK
            MR {' '.join([str(subreg[0]) for subreg in shor_data_subregister_indices[:1]] + list(map(str, t_native_code_utiilities.data_indices[:num_qubits_for_z_obs_in_t_native])))}
            OBSERVABLE_INCLUDE(0) {' '.join([f'rec[-{i+1}]' for i in range(1 + num_qubits_for_z_obs_in_t_native)])}
        """)

        # with open('fds.svg', 'w') as f: f.write(str(circuit.diagram('detslice-with-ops-svg', tick=range(0, 5), filter_coords=['D42', ])))
        return circuit


if __name__ == '__main__':
    Main(distance=7).run_main()
