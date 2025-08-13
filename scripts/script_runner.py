from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime
from functools import cached_property
from multiprocessing import Pool
from typing import Callable

import numpy as np
from cirq import Circuit, LineQubit, Operation
from numpy._typing import NDArray

from stim_experiments.algorithms.support.logical_operations_circuit_creator.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator
from stim_experiments.custom_dataclasses.noisy_circuit import NoisyCircuit
from stim_experiments.custom_dataclasses.state_and_measurements import Measurements
from stim_experiments.custom_dataclasses.transformation_operation import TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.error_correcting_codes.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


@dataclass
class RunnerConfiguration:
    num_shots: int
    surface_code_distance: int
    num_measurement_rounds: int
    depolarization_probability_one_qubit: float = 1e-4
    depolarization_probability_two_qubit: float = 1e-4


def add_runner_configuration_args(parser: ArgumentParser) -> None:
    parser.add_argument('-s', '--num-shots', type=int, default=10,
                        help='Number of shots to run the algorithm for.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=3,
                        help='Surface code distance.')
    parser.add_argument('-r', '--num-measurement-rounds', type=int, default=3,
                        help='Number of times to measure for majority voting. Minimum is 3.')
    parser.add_argument('-p1', '--prob-one-qubit-error', type=int, default=1e-3,
                        help='Probability of depolarization on one qubit gates.')
    parser.add_argument('-p2', '--prob-two-qubit-error', type=int, default=2e-3,
                        help='Probability of depolarization on two qubit gates.')


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

        self._num_shots = self._runner_configuration.num_shots
        self._surface_code_distance = self._runner_configuration.surface_code_distance
        self._num_measurement_rounds = self._runner_configuration.num_measurement_rounds
        self._depolarization_probability_one_qubit = self._runner_configuration.depolarization_probability_one_qubit
        self._depolarization_probability_two_qubit = self._runner_configuration.depolarization_probability_two_qubit

    def run_main(self):
        self._set_configuration()
        start_time = datetime.now()
        print(f"{start_time}: Start runner")
        operation_counts = [noisy_circuit.noisy_operations_count for noisy_circuit in self._circuits_noisy]
        print(f"    {len(operation_counts)} noisy circuit")
        print()
        print(f"    {operation_counts}")

        start_time = self._log_time_period(start_time)
        print()
        print(f"    Starting {len(self._circuits_noisy)} circuit")
        results: list[Measurements] = []

        with Pool(processes=1) as pool:
            results = pool.map(run_circuit, self._circuits_noisy)
        start_time = self._log_time_period(start_time)

        # simulator = ErrorCorrectingRunnerClifford()
        # for i, noisy_circuit in enumerate(self._circuits_noisy):
        #     print()
        #     print(f"    Start circuit {i + 1}/{len(operation_counts)}")
        #     result = simulator.run_circuit(noisy_circuit.circuit)
        #     start_time = self._log_time_period(start_time)
        #     results.append(result)

        measurements_per_shot = [result.measurements_per_shot[0] for result in results]
        sum_measurements_per_shot = self._was_successful_func(measurements_per_shot)
        num_assumed_success = self._num_shots - len(self._circuits_noisy)
        num_successful_shots = np.count_nonzero(sum_measurements_per_shot) + num_assumed_success
        print()
        print(f"----MEASUREMENTS PER SHOT----: {measurements_per_shot}")

        noisy_operations_with_moment_indices = self._find_noisy_operations_with_moment_indices()
        errored_circuits = [noisy_operations_with_moment_indices[i] for i in np.nonzero(sum_measurements_per_shot)[0]]
        print()
        print(f"-----noisy_operations_with_moment_indices----: {noisy_operations_with_moment_indices}")
        print()
        print(f"    ERRORED CIRCUITS: {errored_circuits}")
        print()
        print(f"----SUCCESS RATE----: {abs(num_successful_shots) / self._num_shots * 100:.1f}%")

    def _log_time_period(self, start_time: datetime) -> datetime:
        end_time = datetime.now()
        print(f"    Time Taken: {end_time - start_time}")
        return end_time

    def _set_configuration(self) -> None:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.majority_vote_repetitions = self._num_measurement_rounds
        configuration.noise_parameters.depolarization_probability_one_qubit = self._depolarization_probability_one_qubit
        configuration.noise_parameters.depolarization_probability_two_qubit = self._depolarization_probability_two_qubit

    def _find_noisy_operations_with_moment_indices(self) -> list[tuple[list[Operation], list[int]]]:
        noisy_operations_with_moment_indices = []
        for errored_circuit in self._circuits_noisy:
            noisy_operations_with_moment_indices.append([])
            noisy_circuit = errored_circuit.circuit
            for correction_round in errored_circuit.noisy_operations_count.counts:
                for non_identity_errors in (correction_round.x_errors, correction_round.y_errors,
                                            correction_round.z_errors):
                    for noisy_path in non_identity_errors.paths:
                        noisy_operations = [list(noisy_circuit.all_operations()).__getitem__(noisy_path[0])]
                        for i in noisy_path[1:]:
                            noisy_operations.append(
                                list(noisy_operations[-1].untagged.circuit.all_operations()).__getitem__(i))
                        noisy_moment_indices = [
                            next(j for j, moment in enumerate(noisy_circuit) if noisy_operations[0] in moment)]
                        for i, noisy_operation in enumerate(noisy_operations[1:]):
                            noisy_moment_indices.append(next(
                                j for j, moment in enumerate(noisy_operations[i].untagged.circuit) if
                                noisy_operation in moment))
                        noisy_operations_with_moment_indices[-1].append((noisy_operations, noisy_moment_indices))
        return noisy_operations_with_moment_indices

    @cached_property
    def _circuits_noisy(self) -> list[NoisyCircuit]:
        noisy_circuits_list = [
            NoisyCircuitCreator(circuit=self._circuit_noiseless, num_data_qubits=self._num_data_qubits).get_noisy_circuit()
            for _ in range(self._num_shots)]
        return [noisy_circuit
                for noisy_circuit in noisy_circuits_list
                if noisy_circuit.noisy_operations_count.num_non_identity_errors]

    @cached_property
    def _num_data_qubits(self) -> int:
        return sum(len(logical_qubit.data_qubits) for logical_qubit in self._logical_qubits)

    @cached_property
    def _circuit_noiseless(self) -> Circuit:
        circuit_creator = LogicalOperationsCircuitCreator(encodings=self._logical_qubits, operations=self._operations)
        return circuit_creator.get_simulation_circuit()

    @cached_property
    def _logical_qubits(self) -> list[ErrorCorrectingCode]:
        encoding = MultipleCatCode(num_cats=self._surface_code_distance, num_qubits_per_cat=self._surface_code_distance)
        num_qubits_per_encoding = len(encoding.data_qubits)
        data_qubits = LineQubit.range(self._num_logical_qubits * num_qubits_per_encoding)
        return [encoding.create_new(data_qubits[i * num_qubits_per_encoding:(i + 1) * num_qubits_per_encoding])
                for i in range(self._num_logical_qubits)]

    @cached_property
    def _num_logical_qubits(self) -> int:
        max_qubit_index = max(max(operation.target_qubit_index, operation.control_qubit_index or 0) for operation in self._operations)
        max_qubit_num = max_qubit_index + 1
        return max_qubit_num
