import argparse
from datetime import datetime
from functools import partial
from typing import List, Sequence

import numpy as np
from cirq import Circuit, LineQubit, Moment, NoiseModel, OP_TREE, OpIdentifier, Operation, Qid, depolarize, map_moments
from cirq.devices import InsertionNoiseModel

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.state_and_measurements import Measurements
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from stim_experiments.algorithms.deutsch_josza.deutsch_josza import DeutschJosza
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode


class OneAndTwoQubitGateDepolarization(NoiseModel):
    def __init__(self, depolarization_probability_one_qubit: float, depolarization_probability_two_qubit: float):
        super().__init__()
        self._depolarization_probability_one_qubit = depolarization_probability_one_qubit
        self._depolarization_probability_two_qubit = depolarization_probability_two_qubit
        self.num_noisy_operations = 0

    def noisy_moment(self, moment: Moment, system_qubits: Sequence[Qid]) -> OP_TREE:
        op_tree, inactive_qubits = self._noisy_moment(moment=moment, inactive_qubits=set(system_qubits))
        inactive_depolarization = Circuit(
            depolarize(p=self._depolarization_probability_one_qubit).on(qubit)
            for qubit in inactive_qubits
        )
        return [op_tree, *inactive_depolarization.moments]

    def _noisy_moment(self, moment: Moment, inactive_qubits: set[Qid]) -> (OP_TREE, set[Qid]):
        operations = moment.operations

        noise_ops: List[Operation] = []
        for operation in operations:
            if hasattr(operation, 'circuit'):
                noise_ops_prime: List[Operation] = []
                for mom in operation.circuit.moments:
                    op_tree, inactive_qubits = self._noisy_moment(moment=mom, inactive_qubits=inactive_qubits)
                    noise_ops_prime.append(op_tree)
                noisy_circuit = Circuit(noise_ops_prime)
                operation.circuit = noisy_circuit.freeze()
            else:
                noise_probability = self._depolarization_probability_one_qubit \
                    if len(operation.qubits) == 1 \
                    else self._depolarization_probability_two_qubit
                for qubit in operation.qubits:
                    noise_ops.append(depolarize(p=noise_probability).on(qubit))
                    inactive_qubits.discard(qubit)
                    self.num_noisy_operations += 1
        noise_steps = Circuit(noise_ops)

        return [moment, *noise_steps.moments], inactive_qubits


class DeutschJoszaLerSurfaceCode:
    def __init__(self,
                 num_shots: int,
                 num_input_qubits: int,
                 surface_code_distance: int,
                 is_balanced: bool,
                 num_measurement_rounds: int,
                 depolarization_probability_one_qubit: float = 1e-4,
                 depolarization_probability_two_qubit: float = 1e-4,
                 ):
        self._num_shots = num_shots
        self._num_input_qubits = num_input_qubits
        self._surface_code_distance = surface_code_distance
        self._is_balanced = is_balanced
        self._num_measurement_rounds = num_measurement_rounds
        self._depolarization_probability_one_qubit = depolarization_probability_one_qubit
        self._depolarization_probability_two_qubit = depolarization_probability_two_qubit

        self._num_noisy_operations = 0

    def run_main(self):
        print(f"Running Deutsch-Josza Logical Error Rate Calculator with arguments: {args}")

        num_oracle_qubits = 1
        num_logical_qubits = self._num_input_qubits + num_oracle_qubits
        oracle_qubit_index = self._num_input_qubits
        self._configuration.majority_vote_repetitions = self._num_measurement_rounds

        encoding = MultipleCatCode(num_cats=self._surface_code_distance, num_qubits_per_cat=self._surface_code_distance)
        num_qubits_per_encoding = len(encoding.data_qubits)
        qubits = LineQubit.range(num_logical_qubits * num_qubits_per_encoding)
        logical_qubits = [encoding.create_new(qubits[i * num_qubits_per_encoding:(i + 1) * num_qubits_per_encoding])
                          for i in range(num_logical_qubits)]

        oracle = [
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=i, target_qubit_index=oracle_qubit_index)
            for i in range(self._num_input_qubits)
        ] if self._is_balanced else []
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=oracle_qubit_index)
        circuit = algorithm.get_circuit()

        simulator = ErrorCorrectingRunnerClifford()
        start_time = datetime.now()
        map_func = partial(self.add_noisy_moment, inactive_qubits_all=set(qubits))
        map_moments(circuit=circuit, map_func=map_func, deep=True)
        print(f"{start_time}: Start simulation")
        print(f"    {self._num_noisy_operations} noisy operations")
        result: Measurements = simulator.run_circuit(circuit, num_shots=self._num_shots)
        print(f"    {datetime.now() - start_time}: End simulation")
        sum_measurements_per_shot = np.sum(result.measurements_per_shot, axis=1)
        nonzero_shots = np.count_nonzero(sum_measurements_per_shot)
        print(f"    Measurements per shot: {result.measurements_per_shot}")
        print(f"    {abs(self._num_shots * (not self._is_balanced) - nonzero_shots) / self._num_shots * 100:.1f}% success rate")

    def add_noisy_moment(self, moment: Moment, moment_index: int, inactive_qubits_all: set[Qid]) -> Sequence[Moment]:
        noisy_moment = self._configuration.noise_parameters.add_noisy_moment(moment, moment_index, inactive_qubits_all)
        self._num_noisy_operations += noisy_moment.num_noisy_operations
        return noisy_moment.moments

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Deutsch-Josza Logical Error Rate Calculator',
        description='Runs the Deutsch-Josza algorithm using surface code and calculates the percentage of logical errors in the result.')
    parser.add_argument('-s', '--num-shots', type=int, default=1, help='Number of shots to run the algorithm for.')
    parser.add_argument('-q', '--num-input-qubits', type=int, default=2, help='Number of input qubits.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=3, help='Surface code distance.')
    parser.add_argument('-b', '--is-balanced', action="store_true", help='Surface code distance.')
    parser.add_argument('-r', '--num-measurement-rounds', type=int, default=0, help='Number of times to measure for majority voting.')
    args = parser.parse_args()

    DeutschJoszaLerSurfaceCode(
        num_shots=args.num_shots,
        num_input_qubits=args.num_input_qubits,
        surface_code_distance=args.surface_code_distance,
        is_balanced=args.is_balanced,
        num_measurement_rounds=max(3, args.num_measurement_rounds),
    ).run_main()
