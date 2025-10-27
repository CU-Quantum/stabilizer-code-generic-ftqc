import numpy as np
from matplotlib import pyplot as plt
from sinter import CSV_HEADER, Task, collect, plot_error_rate
from stim import Circuit

from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.support.cx_from_gsch import CxFromGsch
from stim_experiments.simulate_cx.decoder_by_matrix.decoder_by_matrix import DecoderByMatrix
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import StabilizerCodeUtilities, \
    get_dodecacode_utilities, get_five_qubit_code_utilities, get_shor_code_utilities, \
    get_shor_h_observable_x, \
    get_shor_h_observable_z


class SimulateCx:
    def __init__(self, num_cat_states: int, target_code_utilities: StabilizerCodeUtilities, si: int, run_configuration: RunConfiguration):
        self._num_cat_states = num_cat_states
        self._target_code_utilities = target_code_utilities
        self._si = si
        self._run_configuration = run_configuration

        self._num_qubits_per_cat_state = int(max(np.count_nonzero(target_code_utilities.z_observable), np.count_nonzero(target_code_utilities.x_observable)))
        self._last_si = self._num_cat_states - 1
        self._control_code_utilities = get_shor_code_utilities(
            num_cat_states=self._num_cat_states,
            num_qubits_per_cat_state=self._num_qubits_per_cat_state,
            z_observable=get_shor_h_observable_z(self._num_cat_states),
            x_observable=get_shor_h_observable_x(self._num_cat_states),
            qubit_id_start=self._target_code_utilities.last_qubit_index + 1,
            row_coord_start=2,
        )

    def run_main(self):
        combined_symplectic_matrix, observable = self.get_combined_symplectic()

        samples = collect(
            num_workers=self._run_configuration.num_workers,
            max_shots=self._run_configuration.max_shots,
            max_errors=self._run_configuration.max_errors,
            tasks=self.generate_example_tasks(),
            decoders=['decoder_by_matrix'],
            custom_decoders={'decoder_by_matrix': DecoderByMatrix(symplectic_matrix=combined_symplectic_matrix,
                                                                  distance=self._num_cat_states,
                                                                  observables=np.array([observable]),
                                                                  modified_index=len(combined_symplectic_matrix) - self._num_cat_states + 1 + self._si if self._cx_is_performed else None,
                                                                  num_target_data_qubits=self._num_target_data_qubits
                                                                  )},
        )

        return samples

    def generate_example_tasks(self):
        for p in self._run_configuration.depolarization_probabilities:
            yield Task(
                circuit=self.generate_task_circuit(physical_error_rate=p),
                json_metadata={
                    'physical_error_rate': p,
                    'distance': self._num_cat_states,
                },
            )

    def get_combined_symplectic(self):
        target_symplectic_matrix_solo = self._target_code_utilities.symplectic_matrix
        control_symplectic_matrix_solo = self._control_code_utilities.symplectic_matrix
        target_symplectic_matrix_expanded = np.concatenate([
            target_symplectic_matrix_solo[:, :self._num_target_data_qubits],
            np.zeros((target_symplectic_matrix_solo.shape[0], control_symplectic_matrix_solo.shape[1] // 2)),
            target_symplectic_matrix_solo[:, self._num_target_data_qubits:],
            np.zeros((target_symplectic_matrix_solo.shape[0], control_symplectic_matrix_solo.shape[1] // 2)),
        ], axis=1)
        control_symplectic_matrix_expanded = np.concatenate([
            np.zeros((control_symplectic_matrix_solo.shape[0], self._num_target_data_qubits)),
            control_symplectic_matrix_solo[:, :control_symplectic_matrix_solo.shape[1] // 2],
            np.zeros((control_symplectic_matrix_solo.shape[0], self._num_target_data_qubits)),
            control_symplectic_matrix_solo[:, control_symplectic_matrix_solo.shape[1] // 2:],
        ], axis=1)
        if self._stabilizers_are_modified:
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
        observable[[len(observable) // 2 + len(self._target_code_utilities.z_observable) // 2 + i * self._num_qubits_per_cat_state for i in range(1 + self._si)]] = np.ones(1 + self._si)
        observable[self._num_target_data_qubits + self._num_qubits_per_cat_state * (self._si + 1):len(observable) // 2] = np.ones((self._num_cat_states - self._si - 1) * self._num_qubits_per_cat_state)

        return combined_symplectic_matrix, observable

    def generate_task_circuit(self, physical_error_rate: float) -> Circuit:
        control_subregister_indices = [self._control_code_utilities.data_indices[i * self._num_qubits_per_cat_state:(i + 1) * self._num_qubits_per_cat_state] for i in range(self._num_cat_states)]
        all_data_indices = self._target_code_utilities.data_indices + self._control_code_utilities.data_indices

        cx_from_gsch_all = [
            CxFromGsch(control_qubit_indices=control_subregister_indices[i],
                       target_code_utilities=self._target_code_utilities)
            for i in range(self._si + 1)
        ]

        cat_states_circuit = Circuit()
        for subregister in control_subregister_indices:
            cat_states_circuit.append('H', subregister[0])
            targets = subregister[1:]
            indices = [j for i in zip([subregister[0]] * len(targets), targets) for j in i]
            cat_states_circuit.append('CX', indices)

        modified_ancilla = self._control_code_utilities.ancilla_indices[-self._num_cat_states + 1 + self._si]
        modified_targets = [j for i in zip([modified_ancilla] * len(self._target_code_utilities.x_observable), self._target_code_utilities.data_indices[:np.count_nonzero(self._target_code_utilities.x_observable)]) for j in i] \
            if self._stabilizers_are_modified else []
        cx_error = f"DEPOLARIZE1({physical_error_rate}) {' '.join(map(str, all_data_indices))}" if self._cx_is_performed else ""

        num_subregister_to_uncat = self._num_cat_states - self._si - 1
        uncat_subregisters = Circuit()
        if num_subregister_to_uncat:
            for subregister in control_subregister_indices[-num_subregister_to_uncat:]:
                indices = [j for i in zip([subregister[0]] * len(subregister), subregister[1:]) for j in i]
                uncat_subregisters.append('CX', indices)
                uncat_subregisters.append('H', subregister[0])

        target_measurement_indices = set(np.where(self._target_code_utilities.z_observable == 1)[0] % len(self._target_code_utilities.data_indices))
        circuit = Circuit(f"""
            {self._target_code_utilities.get_init()}
            {self._control_code_utilities.get_init()}

            {self._target_code_utilities.get_encoding_by_stabilizer()}
            {cat_states_circuit}

            {'\n'.join([cx_from_gsch.perform_cx() for cx_from_gsch in cx_from_gsch_all[:-1]])}
            {cx_error}
            {cx_from_gsch_all[-1].perform_cx() if self._cx_is_performed else ''}

            DEPOLARIZE1({physical_error_rate}) {' '.join(map(str, all_data_indices))}
            REPEAT {self._num_cat_states} {{
                {self._target_code_utilities.get_stabilizers()}
                {self._control_code_utilities.get_stabilizers(modified_targets=modified_targets, modified_ancilla=modified_ancilla)}
            
                {'\n'.join([f'DETECTOR rec[{-len(self._target_code_utilities.ancilla_indices) - len(self._control_code_utilities.ancilla_indices) + i}]' for i in range(len(self._target_code_utilities.ancilla_indices))])}
                {'\n'.join([f'DETECTOR rec[{-len(self._control_code_utilities.ancilla_indices) + i}]' for i in range(len(self._control_code_utilities.ancilla_indices))])}
            }}

            {uncat_subregisters}
            M {' '.join(list(map(str, target_measurement_indices)) + [str(subreg[0]) for subreg in control_subregister_indices])}
            OBSERVABLE_INCLUDE(0) {' '.join([f'rec[-{i+1}]' for i in range(len(target_measurement_indices) + len(control_subregister_indices))])}
        """)

        # with open('fds.svg', 'w') as f: f.write(str(circuit.diagram('detslice-with-ops-svg', tick=range(0, 5), filter_coords=['D42', ])))
        return circuit

    @property
    def _stabilizers_are_modified(self):
        return self._cx_is_performed and self._si < self._last_si

    @property
    def _cx_is_performed(self):
        return 0 <= self._si

    @property
    def _num_target_data_qubits(self):
        return len(self._target_code_utilities.data_indices)


if __name__ == '__main__':
    run_configuration = RunConfiguration(
        max_shots=1_000_000,
        max_errors=1_000,
        depolarization_probabilities=[1e-4, 5e-4, 0.001, 0.005, 0.01],
        num_workers=5
    )

    # target_code = get_3_repetition_code_utilities()
    # target_code = get_15_1_3_reed_solomon_code_utilities()
    # target_code = get_shor_code_utilities(num_cat_states=3, num_qubits_per_cat_state=3, z_observable=get_shor_h_observable_z(distance=3), x_observable=get_shor_h_observable_x(distance=3))
    target_code = get_dodecacode_utilities()
    samples = SimulateCx(num_cat_states=5, target_code_utilities=target_code, si=1, run_configuration=run_configuration).run_main()

    print(CSV_HEADER)
    for sample in samples:
        print(sample.to_csv_line())

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

    plt.show()
