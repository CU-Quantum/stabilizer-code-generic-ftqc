from pathlib import Path
from typing import Optional

import numpy as np
from matplotlib import pyplot as plt
from sinter import CSV_HEADER, Task, collect, plot_error_rate
from stim import Circuit

from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.support.cx_from_gsch import CxFromGsch
from stim_experiments.simulate_cx.decoder_by_matrix.bposd_decoder import BpOsdDecoderForSinter
from stim_experiments.simulate_cx.decoder_by_matrix.decoder_by_matrix import DecoderByMatrix
from stim_experiments.simulate_cx.decoder_by_matrix.exact_mw_dem_decoder import ExactMwDemDecoder
from stim_experiments.simulate_cx.decoder_by_matrix.partition_decoder import PartitionDecoder
from stim_experiments.simulate_cx.decoder_by_matrix.symplectic_bposd_decoder import SymplecticBpOsdDecoder
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import StabilizerCodeUtilities, \
    get_dodecacode_utilities, get_five_qubit_code_utilities, get_shor_code_utilities, \
    get_shor_h_observable_x, \
    get_shor_h_observable_z


class SimulateCx:
    def __init__(self,
                 num_cat_states: int,
                 target_code_utilities: StabilizerCodeUtilities,
                 si: int,
                 run_configuration: RunConfiguration,
                 save_resume_filepath: Optional[Path] = None,
                 decode_lookup_table_filepath: Optional[Path] = None,
                 decoder_name: str = 'decoder_by_matrix'):
        self._num_cat_states = num_cat_states
        self._target_code_utilities = target_code_utilities
        self._si = si
        self._run_configuration = run_configuration
        self._save_resume_filepath = save_resume_filepath
        self._decode_lookup_table_filepath = decode_lookup_table_filepath
        self._decoder_name = decoder_name

        self._num_qubits_per_cat_state = int(max(np.count_nonzero(target_code_utilities.z_observable), np.count_nonzero(target_code_utilities.x_observable)))
        self._last_si = self._num_cat_states - 1
        self._control_code_utilities = get_shor_code_utilities(
            num_cat_states=self._num_cat_states,
            num_qubits_per_cat_state=self._num_qubits_per_cat_state,
            z_observable=get_shor_h_observable_z(self._num_cat_states),
            x_observable=get_shor_h_observable_x(self._num_cat_states),
            target_code_utilities=target_code_utilities,
            qubit_id_start=self._target_code_utilities.last_qubit_index + 1,
            row_coord_start=2,
            existing_ancilla_indices=target_code_utilities.all_ancilla_qubits,
        )

    def run_main(self):
        # Ensure unique resume file per shard to avoid cross-node contention
        shard_suffix = f"_shard{self._run_configuration.shard_index}-of-{self._run_configuration.num_shards}"
        save_resume_file = (
            Path(f'{self._save_resume_filepath}_{self._si}{shard_suffix}.csv')
            if self._save_resume_filepath else None
        )
        # Materialize tasks to handle the case where this shard has no work.
        task_list = list(self.generate_sinter_tasks())
        if not task_list:
            return []
        samples = collect(
            num_workers=self._run_configuration.num_workers,
            max_shots=self._run_configuration.max_shots,
            max_errors=self._run_configuration.max_errors,
            tasks=task_list,
            decoders=[self._decoder_name],
            custom_decoders={self._decoder_name: self.build_decoder()},
            print_progress=True,
            save_resume_filepath=save_resume_file,
            count_observable_error_combos=True,
            count_detection_events=True,
        )

        return samples

    def build_decoder(self):
        if self._decoder_name == 'bposd':
            combined_symplectic_matrix, observables = self.get_combined_symplectic()
            return SymplecticBpOsdDecoder(
                symplectic_matrix=combined_symplectic_matrix,
                z_observable=observables[0],
                distance=self._num_cat_states,
                final_detector_generator_indices=[generator_num for generator_num, _ in self._final_detector_generators(self._measured_data_qubits)],
            )
        if self._decoder_name == 'exact_mw':
            combined_symplectic_matrix, _ = self.get_combined_symplectic()
            n_target = len(self._target_code_utilities.symplectic_matrix)
            partition = PartitionDecoder(
                combined_symplectic_matrix=combined_symplectic_matrix,
                num_target_stabilizers=n_target,
                distance=self._num_cat_states,
                modified_index=len(combined_symplectic_matrix) - self._num_cat_states + 1 + self._si if self._cx_is_performed else None,
                target_decoder='bposd' if n_target > 10 else 'lookup',
            )
            return ExactMwDemDecoder(fallback_decoder=partition)
        if self._decoder_name == 'partition':
            combined_symplectic_matrix, _ = self.get_combined_symplectic()
            n_target = len(self._target_code_utilities.symplectic_matrix)
            return PartitionDecoder(
                combined_symplectic_matrix=combined_symplectic_matrix,
                num_target_stabilizers=n_target,
                distance=self._num_cat_states,
                modified_index=len(combined_symplectic_matrix) - self._num_cat_states + 1 + self._si if self._cx_is_performed else None,
                target_decoder='bposd' if n_target > 10 else 'lookup',
            )
        combined_symplectic_matrix, observables = self.get_combined_symplectic()
        decoder_file = Path(f'{self._decode_lookup_table_filepath}_{self._si}.pickle') if self._decode_lookup_table_filepath else None
        return DecoderByMatrix(symplectic_matrix=combined_symplectic_matrix,
                               distance=self._num_cat_states,
                               observables=observables,
                               modified_index=len(combined_symplectic_matrix) - self._num_cat_states + 1 + self._si if self._cx_is_performed else None,
                               num_target_data_qubits=self._num_target_data_qubits,
                               decode_lookup_table=decoder_file,
                               final_detector_generator_indices=[generator_num for generator_num, _ in self._final_detector_generators(self._measured_data_qubits)]
                               )

    def generate_sinter_tasks(self):
        probs = self._run_configuration.depolarization_probabilities
        for idx, p in enumerate(probs):
            c = self.generate_task_circuit(physical_error_rate=p)
            dem = c.detector_error_model(
                decompose_errors=True,
                ignore_decomposition_failures=True,
            )
            yield Task(
                circuit=c,
                detector_error_model=dem,
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

        num_observables = 1
        observables = np.zeros((num_observables, combined_symplectic_matrix.shape[1]), dtype=int)
        first_observable = observables[0]
        # target observable
        first_observable[:len(self._target_code_utilities.z_observable) // 2] = self._target_code_utilities.z_observable[:len(self._target_code_utilities.z_observable) // 2]
        first_observable[len(first_observable) // 2:len(first_observable) // 2 + len(self._target_code_utilities.z_observable) // 2] = self._target_code_utilities.z_observable[len(self._target_code_utilities.z_observable) // 2:]
        # control observable
        first_observable[len(first_observable) // 2 + len(self._target_code_utilities.z_observable) // 2:-(self._num_cat_states - self._si - 1) * self._num_qubits_per_cat_state or None] = np.ones(self._num_qubits_per_cat_state * (self._si + 1))

        return combined_symplectic_matrix, observables

    def generate_task_circuit(self, physical_error_rate: float) -> Circuit:
        control_subregister_indices = self._control_subregister_indices
        all_data_indices = self._target_code_utilities.data_indices + self._control_code_utilities.data_indices

        cx_from_gsch_all = [
            CxFromGsch(control_qubit_indices=control_subregister_indices[i],
                       target_code_utilities=self._target_code_utilities).perform_cx()
            for i in range(self._si + 1)
        ]

        cat_states_circuit = Circuit()
        for subregister in control_subregister_indices:
            cat_states_circuit.append('H', subregister[0])
            targets = subregister[1:]
            indices = [j for i in zip([subregister[0]] * len(targets), targets) for j in i]
            cat_states_circuit.append('CX', indices)

        modified_generator = len(self._control_code_utilities.symplectic_matrix) - self._num_cat_states + 1 + self._si
        modify_stabilizer = None
        if self._stabilizers_are_modified:
            modify_stabilizer = Circuit()
            self._target_code_utilities.apply_stabilizer(self._target_code_utilities.x_observable, modify_stabilizer, list(reversed([self._control_code_utilities.stabilizer_ancilla] + self._control_code_utilities.cat_applier_ancillas)))

        cx_error = Circuit()
        cx_error_qubits = set()
        applied_cx_circuits = [cx_from_gsch_all[-1]] if self._cx_is_performed else []
        for cx_circuit in applied_cx_circuits:
            for instruction in cx_circuit:
                if instruction.name in ('CX', 'CZ'):
                    targets = instruction.targets_copy()
                    cx_error_qubits.update(target.value for target in targets)
                    for i in range(0, len(targets), 2):
                        pert = physical_error_rate * (1.0 + i * 1e-5)
                        cx_error.append('DEPOLARIZE2', [targets[i], targets[i+1]], pert)

        data_error_indices = [index for index in all_data_indices if index not in cx_error_qubits]
        data_error = f"DEPOLARIZE1({physical_error_rate}) {' '.join(map(str, data_error_indices))}" if data_error_indices else ''
        all_data_depolarizing_one_noise = f"DEPOLARIZE1({physical_error_rate}) {' '.join(map(str, all_data_indices))}"
        depolarizing_one_and_two_noise = f"{data_error}\n{cx_error}" if self._cx_is_performed else ''

        target_measurement_indices = sorted(set(np.where(self._target_code_utilities.z_observable == 1)[0] % len(self._target_code_utilities.data_indices)))
        measured_data_qubits = self._measured_data_qubits
        observable_qubits = [self._target_code_utilities.data_indices[q] for q in target_measurement_indices] + \
                            [ind for subreg in control_subregister_indices[:self._si + 1] for ind in subreg]
        num_measured = len(measured_data_qubits)
        observable_recs = ' '.join([f'rec[{-(num_measured - measured_data_qubits.index(q))}]' for q in observable_qubits])
        stabilizer_round = f"""
            {self._target_code_utilities.get_stabilizers(measurement_error_rate=physical_error_rate)}
            {self._control_code_utilities.get_stabilizers(modify_stabilizer=modify_stabilizer, modified_generator=modified_generator, measurement_error_rate=physical_error_rate)}
        """
        num_middle_rounds = self._num_cat_states - 1
        middle_rounds = f"""
            REPEAT {num_middle_rounds} {{
                {all_data_depolarizing_one_noise}
                {stabilizer_round}
                {self._round_detectors_difference()}
            }}
        """ if num_middle_rounds > 0 else ''
        circuit = Circuit(f"""
            {self._target_code_utilities.get_init()}
            {self._control_code_utilities.get_init()}

            {self._target_code_utilities.get_encoding_by_stabilizer()}
            {cat_states_circuit}

            {'\n'.join(map(str, cx_from_gsch_all[:-1]))}
            {all_data_depolarizing_one_noise}
            {cx_from_gsch_all[-1] if self._cx_is_performed else ''}
            {depolarizing_one_and_two_noise}
            {stabilizer_round}
            {self._round_detectors_absolute()}
            {middle_rounds}
            {stabilizer_round}
            {self._round_detectors_difference()}

            M {' '.join(map(str, measured_data_qubits))}
            {self._final_round_detectors(measured_data_qubits)}
            OBSERVABLE_INCLUDE(0) {observable_recs}
        """)

        # with open('fds.svg', 'w') as f: f.write(str(circuit.diagram('detslice-with-ops-svg', tick=range(0, 5), filter_coords=['D42', ])))
        return circuit

    def _round_detectors_absolute(self) -> str:
        num_generators = self._num_generators_per_round
        return '\n'.join([f'DETECTOR rec[{-num_generators + i}]' for i in range(num_generators)])

    def _round_detectors_difference(self) -> str:
        num_generators = self._num_generators_per_round
        return '\n'.join([f'DETECTOR rec[{-num_generators + i}] rec[{-2 * num_generators + i}]' for i in range(num_generators)])

    @property
    def _num_generators_per_round(self) -> int:
        return len(self._target_code_utilities.symplectic_matrix) + len(self._control_code_utilities.symplectic_matrix)

    def _final_detector_generators(self, measured_data_qubits: list[int]):
        num_target_generators = len(self._target_code_utilities.symplectic_matrix)
        for generator_offset, code_utilities in (
                (0, self._target_code_utilities),
                (num_target_generators, self._control_code_utilities),
        ):
            num_data_qubits = len(code_utilities.data_indices)
            for generator_num, generator in enumerate(code_utilities.symplectic_matrix):
                if np.any(generator[:num_data_qubits]):
                    continue
                support = [code_utilities.data_indices[q] for q in np.where(generator[num_data_qubits:] == 1)[0]]
                if not all(qubit in measured_data_qubits for qubit in support):
                    continue
                yield generator_offset + generator_num, support

    def _final_round_detectors(self, measured_data_qubits: list[int]) -> str:
        num_measured = len(measured_data_qubits)
        num_generators = len(self._target_code_utilities.symplectic_matrix) + len(self._control_code_utilities.symplectic_matrix)
        lines = []
        for global_generator_num, support in self._final_detector_generators(measured_data_qubits):
            recs = [f'rec[{-(num_measured - measured_data_qubits.index(qubit))}]' for qubit in support]
            recs.append(f'rec[{-(num_measured + num_generators - global_generator_num)}]')
            lines.append(f"DETECTOR {' '.join(recs)}")
        return '\n'.join(lines)

    @property
    def _stabilizers_are_modified(self):
        return self._cx_is_performed and self._si < self._last_si

    @property
    def _control_subregister_indices(self):
        return [self._control_code_utilities.data_indices[i * self._num_qubits_per_cat_state:(i + 1) * self._num_qubits_per_cat_state] for i in range(self._num_cat_states)]

    @property
    def _measured_data_qubits(self):
        target_measurement_indices = sorted(set(np.where(self._target_code_utilities.z_observable == 1)[0] % len(self._target_code_utilities.data_indices)))
        return [self._target_code_utilities.data_indices[q] for q in target_measurement_indices] + \
               [ind for subreg in self._control_subregister_indices for ind in subreg]

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

    target_code = get_five_qubit_code_utilities()
    samples = SimulateCx(num_cat_states=3,
                         target_code_utilities=target_code,
                         si=0,
                         run_configuration=run_configuration,
                         ).run_main()

    # target_code = get_dodecacode_utilities()
    # samples = SimulateCx(num_cat_states=5,
    #                      target_code_utilities=target_code,
    #                      si=-1,
    #                      run_configuration=run_configuration,
    #                      decode_lookup_table_filepath=Path(__file__).parent.parent / 'scripts' / 'dodecacode' / 'decode_lookup_table_dodeca',
    #                      ).run_main()

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
