import argparse
from datetime import datetime

import numpy as np
from cirq import LineQubit

from stim_experiments.algorithms.support.logical_operations_circuit_creator.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.error_correcting_codes.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


class SimpleMeasurementLer:
    def __init__(self,
                 num_shots: int,
                 surface_code_distance: int,
                 num_measurement_rounds: int,
                 depolarization_probability_one_qubit: float = 1e-4,
                 depolarization_probability_two_qubit: float = 1e-4,
                 ):
        self._num_shots = num_shots
        self._surface_code_distance = surface_code_distance
        self._num_measurement_rounds = num_measurement_rounds
        self._depolarization_probability_one_qubit = depolarization_probability_one_qubit
        self._depolarization_probability_two_qubit = depolarization_probability_two_qubit

    def run_main(self):
        print(f"Running Universal Hadamard Logical Error Rate Calculator with arguments: {args}")
        self._set_configuration()

        num_logical_qubits = 1
        encoding = MultipleCatCode(num_cats=self._surface_code_distance, num_qubits_per_cat=self._surface_code_distance)
        num_qubits_per_encoding = len(encoding.data_qubits)
        data_qubits = LineQubit.range(num_logical_qubits * num_qubits_per_encoding)
        logical_qubits = [encoding.create_new(data_qubits[i * num_qubits_per_encoding:(i + 1) * num_qubits_per_encoding])
                          for i in range(num_logical_qubits)]

        operations = [
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=0)
        ]
        circuit_creator = LogicalOperationsCircuitCreator(encodings=logical_qubits, operations=operations)
        circuit = circuit_creator.get_simulation_circuit()

        noisy_circuits_list = [NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(data_qubits)).get_noisy_circuit()
                               for _ in range(self._num_shots)]
        noisy_circuits = [noisy_circuit
                          for noisy_circuit in noisy_circuits_list
                          if noisy_circuit.noisy_operations_count.num_non_identity_errors]
        operation_counts = [noisy_circuit.noisy_operations_count for noisy_circuit in noisy_circuits_list]
        start_time = datetime.now()
        print(f"{start_time}: Start simulation")
        print(f"    {operation_counts} noisy operations")
        results = [ErrorCorrectingRunnerClifford().run_circuit(noisy_circuit.circuit) for noisy_circuit in noisy_circuits]
        start_time = self._log_end_time(start_time)
        measurements_per_shot = [result.measurements_per_shot[0] for result in results]
        sum_measurements_per_shot = np.sum(measurements_per_shot, axis=1) if measurements_per_shot else []
        nonzero_shots = np.count_nonzero(sum_measurements_per_shot)
        print(f"    Measurements per shot: {measurements_per_shot}")
        print(f"    {abs(self._num_shots - nonzero_shots) / self._num_shots * 100:.1f}% success rate")

        noisy_operations_with_moment_indices = []
        for errored_circuit in noisy_circuits:
            noisy_operations_with_moment_indices.append([])
            noisy_circuit = errored_circuit.circuit
            for correction_round in errored_circuit.noisy_operations_count.counts:
                for non_identity_errors in (correction_round.x_errors, correction_round.y_errors, correction_round.z_errors):
                    for noisy_path in non_identity_errors.paths:
                        noisy_operations = [list(noisy_circuit.all_operations()).__getitem__(noisy_path[0])]
                        for i in noisy_path[1:]:
                            noisy_operations.append(list(noisy_operations[-1].untagged.circuit.all_operations()).__getitem__(i))
                        noisy_moment_indices = [next(j for j, moment in enumerate(noisy_circuit) if noisy_operations[0] in moment)]
                        for i, noisy_operation in enumerate(noisy_operations[1:]):
                            noisy_moment_indices.append(next(j for j, moment in enumerate(noisy_operations[i].untagged.circuit) if noisy_operation in moment))
                        a = 0
                        noisy_operations_with_moment_indices[-1].append([noisy_operations, noisy_moment_indices])
        errored_circuits = [noisy_operations_with_moment_indices[i] for i in np.nonzero(sum_measurements_per_shot)[0]]
        a = 0

    def _log_end_time(self, start_time: datetime) -> datetime:
        end_time = datetime.now()
        print(f"    Time Taken: {end_time - start_time}")
        return end_time

    def _set_configuration(self) -> None:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.majority_vote_repetitions = self._num_measurement_rounds
        configuration.noise_parameters.depolarization_probability_one_qubit = self._depolarization_probability_one_qubit
        configuration.noise_parameters.depolarization_probability_two_qubit = self._depolarization_probability_two_qubit


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Simple Measurement Error Rate Calculator',
        description='Runs a measurement operation on surface code and calculates the percentage of zero measurements.')
    parser.add_argument('-s', '--num-shots', type=int, default=10, help='Number of shots to run the algorithm for.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=3, help='Surface code distance.')
    parser.add_argument('-r', '--num-measurement-rounds', type=int, default=3, help='Number of times to measure for majority voting. Minimum is 3.')
    parser.add_argument('-p1', '--prob-one-qubit-error', type=int, default=1e-3, help='Probability of depolarization on one qubit gates.')
    parser.add_argument('-p2', '--prob-two-qubit-error', type=int, default=2e-3, help='Probability of depolarization on two qubit gates.')
    args = parser.parse_args()

    SimpleMeasurementLer(
        num_shots=args.num_shots,
        surface_code_distance=args.surface_code_distance,
        num_measurement_rounds=max(3, args.num_measurement_rounds),
        depolarization_probability_one_qubit=args.prob_one_qubit_error,
        depolarization_probability_two_qubit=args.prob_two_qubit_error,
    ).run_main()
