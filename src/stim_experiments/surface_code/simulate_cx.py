import numpy as np
from matplotlib import pyplot as plt
from numpy._typing import NDArray
from sinter import CSV_HEADER, Task, collect, plot_error_rate
from stim import Circuit

from generalized_shor_code_generators import GeneralizedShorCodeGenerators
from predefined_check_matrix_values import get_check_matrix_values_tetrahedral
from stim_experiments.surface_code.cx_from_gsch import CxFromGsch
from stim_experiments.surface_code.decoder_by_matrix import DecoderByMatrix
from stim_experiments.surface_code.stabilizer_code_utilities import StabilizerCodeUtilities


def get_shor_h_observable_z(distance: int) -> NDArray:
    return np.concatenate([np.zeros(distance ** 2), *[np.concatenate([[1], np.zeros(distance - 1)])] * distance])


def get_shor_h_observable_x(distance: int) -> NDArray:
    return np.concatenate([np.ones(distance), np.zeros(distance * (distance - 1) + distance ** 2)])


def get_shor_code_utilities(num_cat_states: int,
                            num_qubits_per_cat_state: int,
                            z_observable: NDArray, 
                            x_observable: NDArray,
                            qubit_id_start: int = 0,
                            row_coord_start: int = 0
                            ) -> StabilizerCodeUtilities:
    shor_code_generators = GeneralizedShorCodeGenerators(num_cats=num_cat_states, num_qubits_per_cat=num_qubits_per_cat_state)
    shor_code_symplectic_matrix = shor_code_generators.get_z_generators() + shor_code_generators.get_x_generators()
    shor_anticommutors = [
        np.concatenate(
            [np.ones(np.argmax(shor_code_symplectic_matrix[i][-len(shor_code_symplectic_matrix[0]) // 2 - 1:])),
             np.zeros(len(shor_code_symplectic_matrix[0]) - np.argmax(
                 shor_code_symplectic_matrix[i][-len(shor_code_symplectic_matrix[0]) // 2 - 1:]))])
        if i <= len(shor_code_symplectic_matrix) - num_cat_states
        else np.concatenate([np.zeros(len(shor_code_symplectic_matrix[0]) // 2), [
            int(not j % num_qubits_per_cat_state and j // num_qubits_per_cat_state < i - (
                        len(shor_code_symplectic_matrix) - num_cat_states)) for j in
            range(len(shor_code_symplectic_matrix[0]) // 2)]])
        for i in range(len(shor_code_symplectic_matrix))
    ]
    return StabilizerCodeUtilities(
        symplectic_matrix=np.array(shor_code_symplectic_matrix), 
        generator_anticommutators=np.array(shor_anticommutors),
        z_observable=z_observable,
        x_observable=x_observable,
        qubit_id_start=qubit_id_start,
        row_coord_start=row_coord_start
    )


def get_15_1_3_reed_solomon_code_utilities():
    t_native_anticommutators = np.array([
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
    observable_z = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    observable_x = np.array([1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    return StabilizerCodeUtilities(
        symplectic_matrix=get_check_matrix_values_tetrahedral(),
        generator_anticommutators=t_native_anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )


def get_3_repetition_code_utilities():
    symplectic_matrix = np.array([
        [0, 0, 0, 1, 1, 0],
        [0, 0, 0, 0, 1, 1],
    ])
    anticommutators = np.array([
        [1, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
    ])
    observable_z = np.array([0, 0, 0, 1, 1, 1])
    observable_x = np.array([1, 1, 1, 0, 0, 0])
    return StabilizerCodeUtilities(
        symplectic_matrix=symplectic_matrix,
        generator_anticommutators=anticommutators,
        z_observable=observable_z,
        x_observable=observable_x
    )


class SimulateCx:
    def __init__(self, num_cat_states: int, target_code_utilities: StabilizerCodeUtilities, si: int):
        self._num_cat_states = num_cat_states
        self._target_code_utilities = target_code_utilities
        self._si = si

        self._num_qubits_per_cat_state = int(max(np.count_nonzero(target_code_utilities.z_observable), np.count_nonzero(target_code_utilities.x_observable)))
        self._control_code_utilities = get_shor_code_utilities(
            num_cat_states=self._num_cat_states,
            num_qubits_per_cat_state=self._num_qubits_per_cat_state,
            z_observable=get_shor_h_observable_z(self._num_cat_states),
            x_observable=get_shor_h_observable_x(self._num_cat_states),
            qubit_id_start=self._target_code_utilities.ancilla_indices[-1]+1,
            row_coord_start=2,
        )

    def run_main(self):
        combined_symplectic_matrix, observable = self.get_combined_symplectic()

        samples = collect(
            num_workers=5,
            max_shots=1_000_000_000,
            max_errors=100_000,
            tasks=self.generate_example_tasks(),
            decoders=['decoder_by_matrix'],
            custom_decoders={'decoder_by_matrix': DecoderByMatrix(symplectic_matrix=combined_symplectic_matrix, distance=self._num_cat_states, observables=np.array([observable]))},
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
        ax.set_ylim(1e-10, 1e-1)
        ax.grid()
        ax.set_title('Logical Error Rate vs Physical Error Rate')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        # Save to file and also open in a window.
        # fig.savefig('plot.png')
        plt.show()

    def get_combined_symplectic(self):
        target_symplectic_matrix_solo = self._target_code_utilities.symplectic_matrix
        control_symplectic_matrix_solo = self._control_code_utilities.symplectic_matrix
        target_symplectic_matrix_expanded = np.concatenate([
            target_symplectic_matrix_solo[:, :target_symplectic_matrix_solo.shape[1] // 2],
            np.zeros((target_symplectic_matrix_solo.shape[0], control_symplectic_matrix_solo.shape[1] // 2)),
            target_symplectic_matrix_solo[:, target_symplectic_matrix_solo.shape[1] // 2:],
            np.zeros((target_symplectic_matrix_solo.shape[0], control_symplectic_matrix_solo.shape[1] // 2)),
        ], axis=1)
        control_symplectic_matrix_expanded = np.concatenate([
            np.zeros((control_symplectic_matrix_solo.shape[0], target_symplectic_matrix_solo.shape[1] // 2)),
            control_symplectic_matrix_solo[:, :control_symplectic_matrix_solo.shape[1] // 2],
            np.zeros((control_symplectic_matrix_solo.shape[0], target_symplectic_matrix_solo.shape[1] // 2)),
            control_symplectic_matrix_solo[:, control_symplectic_matrix_solo.shape[1] // 2:],
        ], axis=1)
        control_symplectic_matrix_expanded[-self._num_cat_states + 1 + self._si][
            :len(self._target_code_utilities.x_observable) // 2] = self._target_code_utilities.x_observable[:len(self._target_code_utilities.x_observable) // 2]
        control_symplectic_matrix_expanded[-self._num_cat_states + 1 + self._si][
            control_symplectic_matrix_expanded.shape[1] // 2:control_symplectic_matrix_expanded.shape[1] //2 + len(self._target_code_utilities.x_observable) // 2] \
            = self._target_code_utilities.x_observable[len(self._target_code_utilities.x_observable) // 2:]
        combined_symplectic_matrix = np.concatenate([target_symplectic_matrix_expanded, control_symplectic_matrix_expanded])

        observable = np.zeros(combined_symplectic_matrix.shape[1])
        # target observable
        observable[:len(self._target_code_utilities.z_observable) // 2] = self._target_code_utilities.z_observable[:len(self._target_code_utilities.z_observable) // 2]
        observable[len(observable) // 2:len(observable) // 2 + len(self._target_code_utilities.z_observable) // 2] = self._target_code_utilities.z_observable[len(self._target_code_utilities.z_observable) // 2:]
        # control observable
        observable[[len(observable) // 2 + len(self._target_code_utilities.z_observable) // 2 + i for i in range(self._si + 1)]] = np.ones(self._si + 1)

        return combined_symplectic_matrix, observable

    def generate_example_tasks(self):
        for p in [1e-5, 5e-5, 1e-4, 5e-4, 0.001, 0.005, 0.01]:
            yield Task(
                circuit=self.generate_task_circuit(physical_error_rate=p),
                json_metadata={
                    'physical_error_rate': p,
                    'distance': self._num_cat_states,
                },
            )

    def generate_task_circuit(self, physical_error_rate: float) -> Circuit:
        control_subregister_indices = [self._control_code_utilities.data_indices[i * self._num_qubits_per_cat_state:(i + 1) * self._num_qubits_per_cat_state] for i in range(self._num_cat_states)]
        all_data_indices = self._control_code_utilities.data_indices + self._target_code_utilities.data_indices

        # TODO: allow for targets NOT logical gates with not only CX operations
        cx_from_gsch = CxFromGsch(control_qubit_indices=control_subregister_indices[0],
                                  target_qubit_indices=self._target_code_utilities.data_indices[:len(self._target_code_utilities.x_observable)],
                                  possible_idle_qubit_indices=all_data_indices,
                                  physical_error_rate=physical_error_rate)
        cat_states_circuit = Circuit()
        for subregister in control_subregister_indices:
            cat_states_circuit.append('H', subregister[0])
            targets = subregister[1:]
            indices = [j for i in zip([subregister[0]] * len(targets), targets) for j in i]
            cat_states_circuit.append('CX', indices)
        modified_ancilla = self._control_code_utilities.ancilla_indices[-self._num_cat_states + 1 + self._si]
        modified_stabilizer = f"""
            H {modified_ancilla}
            CX {' '.join(str(j) for i in zip([modified_ancilla] * len(self._target_code_utilities.x_observable), self._target_code_utilities.data_indices[:np.count_nonzero(self._target_code_utilities.x_observable)]) for j in i)}
            H {modified_ancilla}
        """

        target_measurement_indices = set(np.where(self._target_code_utilities.z_observable == 1)[0] % len(self._target_code_utilities.data_indices))
        circuit = Circuit(f"""
            {self._target_code_utilities.get_init()}
            {self._control_code_utilities.get_init()}

            TICK
            {self._target_code_utilities.get_encoding_by_stabilizer()}
            {cat_states_circuit}

            TICK
            {cx_from_gsch.perform_cx()}

            TICK
            {self._target_code_utilities.get_stabilizers()}
            {self._control_code_utilities.get_stabilizers()}
            {modified_stabilizer}
            TICK
            {f'MR {' '.join(map(str, self._target_code_utilities.ancilla_indices))}'}
            {f'MR {' '.join(map(str, self._control_code_utilities.ancilla_indices))}'}

            {'\n'.join([f'DETECTOR rec[{-len(self._target_code_utilities.ancilla_indices) - len(self._control_code_utilities.ancilla_indices) + i}]' for i in range(len(self._target_code_utilities.ancilla_indices))])}
            {'\n'.join([f'DETECTOR rec[{-len(self._control_code_utilities.ancilla_indices) + i}]' for i in range(len(self._control_code_utilities.ancilla_indices))])}

            TICK
            MR {' '.join(list(map(str, target_measurement_indices)) + [str(subreg[0]) for subreg in control_subregister_indices[:self._si + 1]])}
            OBSERVABLE_INCLUDE(0) {' '.join([f'rec[-{i+1}]' for i in range(1 + len(target_measurement_indices) + self._si)])}
        """)

        # with open('fds.svg', 'w') as f: f.write(str(circuit.diagram('detslice-with-ops-svg', tick=range(0, 5), filter_coords=['D42', ])))
        return circuit


if __name__ == '__main__':
    # target_code = get_3_repetition_code_utilities()
    # target_code = get_shor_code_utilities(num_cat_states=3, num_qubits_per_cat_state=3, z_observable=get_shor_h_observable_z(distance=3), x_observable=get_shor_h_observable_x(distance=3))
    target_code = get_15_1_3_reed_solomon_code_utilities()
    SimulateCx(num_cat_states=3, target_code_utilities=target_code, si=0).run_main()
