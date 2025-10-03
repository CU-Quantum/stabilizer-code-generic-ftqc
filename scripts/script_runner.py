from argparse import ArgumentParser
from dataclasses import asdict, dataclass
from datetime import datetime
from functools import cached_property
from multiprocessing import Pool, cpu_count
from typing import Callable

import numpy as np
from cirq import Circuit, LineQubit, Operation, to_json
from numpy._typing import NDArray

from stim_experiments.algorithms.support.logical_operations_circuit_creator.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.custom_dataclasses.state_and_measurements import Measurements
from stim_experiments.custom_dataclasses.transformation_operation import TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_nondeterministic.support.parity_verifier_sequential import \
    ParityVerifierSequential
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit_sequential import \
    MeasurerWithSingleQubitSequential
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.serialization.custom_json_encoder import CustomJsonEncoder
from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.error_correcting_codes.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


@dataclass
class RunnerConfiguration:
    num_shots: int
    surface_code_distance: int
    num_measurement_rounds: int
    depolarization_probability_one_qubit: float
    depolarization_probability_two_qubit: float
    num_processes: int


def get_runner_configuration_args() -> RunnerConfiguration:
    parser = ArgumentParser()
    parser.add_argument('-s', '--num-shots', type=int, default=10,
                        help='Number of shots to run the algorithm for.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=3,
                        help='Surface code distance.')
    parser.add_argument('-r', '--num-measurement-rounds', type=int, default=3,
                        help='Number of times to measure for majority voting. Minimum is 3.')
    parser.add_argument('-p1', '--prob-one-qubit-error', type=float, default=1e-3,
                        help='Probability of depolarization on one qubit gates.')
    parser.add_argument('-p2', '--prob-two-qubit-error', type=float, default=2e-3,
                        help='Probability of depolarization on two qubit gates.')
    parser.add_argument('-p', '--num-processes', type=int, default=cpu_count(),
                        help='The number of processes to run in parallel.'
                             ' Default is the number of CPUs available on the machine.')
    args = parser.parse_args()
    print(f"Running with arguments: {args}")
    return RunnerConfiguration(
        num_shots=args.num_shots,
        surface_code_distance=args.surface_code_distance,
        num_measurement_rounds=max(3, args.num_measurement_rounds),
        depolarization_probability_one_qubit=args.prob_one_qubit_error,
        depolarization_probability_two_qubit=args.prob_two_qubit_error,
        num_processes=args.num_processes,
    )


def run_circuit(noisy_circuit: NoisyCircuit) -> Measurements:
    return ErrorCorrectingRunnerClifford().run_circuit(noisy_circuit.circuit)


class ScriptRunner:
    def __init__(self,
                 operations: list[TransformationOperation],
                 was_successful_func: Callable[[list[NDArray[int]]], NDArray[bool]],
                 runner_configuration: RunnerConfiguration,
                 ):
        self._operations = operations
        self._was_successful_func = was_successful_func
        self._runner_configuration = runner_configuration

    def run_main(self):
        self._set_configuration()
        start_time = datetime.now()
        print(f"{start_time}: Start runner")
        print(f"----NUMBER OF NOISY CIRCUITS----: {len(self._circuits_noisy)}")
        start_time = self._log_time_period(start_time)

        # results = [run_circuit(x) for x in self._circuits_noisy]
        results: list[Measurements] = []
        with Pool(processes=self._runner_configuration.num_processes, initializer=self._set_configuration) as pool:
            results = pool.map(run_circuit, self._circuits_noisy)
        start_time = self._log_time_period(start_time)

        measurements_per_shot = [result.measurements_per_shot[0] for result in results]
        successful_or_not_shots = self._was_successful_func(measurements_per_shot)
        num_assumed_success = self._runner_configuration.num_shots - len(self._circuits_noisy)
        errored_circuit_indices = np.nonzero(1 - successful_or_not_shots)[0]
        print()
        print(f"----NUMBER OF ERRORED CIRCUITS----: {len(errored_circuit_indices)}")

        errored_circuits = np.array(self._circuits_noisy)[errored_circuit_indices]
        errored_circuits_should_have_been_corrected = \
            [all(count.num_non_identity_errors <= np.floor((self._runner_configuration.surface_code_distance - 1) / 2)
                 for count in circuit_noisy.noisy_operations_count.counts)
             for circuit_noisy in errored_circuits]

        num_successful_shots = np.count_nonzero(successful_or_not_shots) + num_assumed_success
        print()
        print(f"----SUCCESS RATE----: {abs(num_successful_shots) / self._runner_configuration.num_shots * 100:.1f}%")

        print()
        if not any(errored_circuits_should_have_been_corrected):
            print("----SUCCESS----: All circuits that failed had an uncorrectable amount of errors with some correction round.")
        else:
            noisy_operations_with_moment_indices = self._find_noisy_operations_with_moment_indices()
            first_errored_circuit_index = errored_circuit_indices[np.argmax(errored_circuits_should_have_been_corrected)]
            errored_circuit_operations = noisy_operations_with_moment_indices[first_errored_circuit_index]
            errored_circuit_noisy_operations_count = self._circuits_noisy[first_errored_circuit_index].noisy_operations_count
            print(f"----ERROR----: {np.count_nonzero(errored_circuits_should_have_been_corrected)} circuits that failed should have been corrected. "
                  f"Storing first one.")
            with open('errored_circuit_operations.json', 'w') as f:
                to_json(errored_circuit_operations, f, cls=CustomJsonEncoder)
            with open('errored_circuit_counts.json', 'w') as f:
                to_json(asdict(errored_circuit_noisy_operations_count), f, cls=CustomJsonEncoder)

    def _log_time_period(self, start_time: datetime) -> datetime:
        end_time = datetime.now()
        print(f"    Time since last timestamp: {end_time - start_time}")
        return end_time

    def _find_noisy_operations_with_moment_indices(self) -> list[tuple[list[Operation], list[int]]]:
        noisy_operations_with_moment_indices = []
        for errored_circuit in self._circuits_noisy:
            noisy_operations_with_moment_indices.append([])
            noisy_circuit = errored_circuit.circuit
            for correction_round in errored_circuit.noisy_operations_count.counts:
                for non_identity_errors in (correction_round.x_errors, correction_round.y_errors,
                                            correction_round.z_errors):
                    for noisy_path in non_identity_errors.paths:
                        noisy_operations = [noisy_circuit, list(noisy_circuit.all_operations()).__getitem__(noisy_path[0])]
                        for i in noisy_path[1:]:
                            noisy_operations.append(
                                list(noisy_operations[-1].untagged.circuit.all_operations()).__getitem__(i))
                        noisy_moment_indices = [
                            next(j for j, moment in enumerate(noisy_circuit) if noisy_operations[1] in moment)]
                        for i, noisy_operation in enumerate(noisy_operations[2:]):
                            noisy_moment_indices.append(next(
                                j for j, moment in enumerate(noisy_operations[i + 1].untagged.circuit) if
                                noisy_operation in moment))
                        noisy_operations_with_moment_indices[-1].append((noisy_operations, noisy_moment_indices))
        return noisy_operations_with_moment_indices

    @cached_property
    def _circuits_noisy(self) -> list[NoisyCircuit]:
        _get_cache_outside_processes = self._circuit_noiseless
        with Pool(processes=self._runner_configuration.num_processes, initializer=self._set_configuration) as pool:
            noisy_circuits_list = pool.map(self._get_noisy_circuit, [()] * self._runner_configuration.num_shots)
        return [noisy_circuit
                for noisy_circuit in noisy_circuits_list
                if noisy_circuit.noisy_operations_count.num_non_identity_errors]

    def _get_noisy_circuit(self, *args, **kwargs) -> NoisyCircuit:
        return NoisyCircuitCreator(circuit=self._circuit_noiseless).get_noisy_circuit()

    @cached_property
    def _circuit_noiseless(self) -> Circuit:
        circuit_creator = LogicalOperationsCircuitCreator(encodings=self._logical_qubits, operations=self._operations)
        return circuit_creator.get_simulation_circuit()

    @cached_property
    def _logical_qubits(self) -> list[ErrorCorrectingCode]:
        encoding = MultipleCatCode(num_cats=self._runner_configuration.surface_code_distance,
                                   num_qubits_per_cat=self._runner_configuration.surface_code_distance)
        num_qubits_per_encoding = len(encoding.data_qubits)
        data_qubits = LineQubit.range(self._num_logical_qubits * num_qubits_per_encoding)
        return [encoding.create_new(data_qubits[i * num_qubits_per_encoding:(i + 1) * num_qubits_per_encoding])
                for i in range(self._num_logical_qubits)]

    @cached_property
    def _num_logical_qubits(self) -> int:
        max_qubit_index = max(max(operation.target_qubit_index, operation.control_qubit_index or 0) for operation in self._operations)
        max_qubit_num = max_qubit_index + 1
        return max_qubit_num

    def _set_configuration(self) -> None:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.majority_vote_repetitions = self._runner_configuration.num_measurement_rounds
        configuration.noise_parameters.depolarization_probability_one_qubit = self._runner_configuration.depolarization_probability_one_qubit
        configuration.noise_parameters.depolarization_probability_two_qubit = self._runner_configuration.depolarization_probability_two_qubit

        configuration.measurer_type = MeasurerWithSingleQubitSequential
        configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
