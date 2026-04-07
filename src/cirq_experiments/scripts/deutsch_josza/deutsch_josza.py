import argparse
from datetime import datetime

import numpy as np
from cirq import LineQubit

from cirq_experiments.custom_dataclasses.state_and_measurements import Measurements
from cirq_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from cirq_experiments.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from cirq_experiments.support.measurer.measurer_with_single_qubit_sequential import MeasurerWithSingleQubit
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from cirq_experiments.simulations.error_correcting_runner import ErrorCorrectingRunnerClifford
from cirq_experiments.algorithms.deutsch_josza.deutsch_josza import DeutschJosza
from cirq_experiments.error_correcting_codes.generalized_shor_code.generalized_shor_code import GeneralizedShorCode
from cirq_experiments.utilities.noisy_circuit_creator import NoisyCircuitCreator


class DeutschJosza:
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

    def run_main(self):
        print(f"Running Deutsch-Josza Logical Error Rate Calculator with arguments: {args}")
        self._set_configuration()

        num_oracle_qubits = 1
        num_logical_qubits = self._num_input_qubits + num_oracle_qubits
        oracle_qubit_index = self._num_input_qubits

        encoding = GeneralizedShorCode(num_cats=self._surface_code_distance, num_qubits_per_cat=self._surface_code_distance)
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

        noisy_circuit = NoisyCircuitCreator(circuit=circuit, num_data_qubits=len(qubits)).get_noisy_circuit()
        simulator = ErrorCorrectingRunnerClifford()
        start_time = datetime.now()
        print(f"{start_time}: Start simulation")
        print(f"    {noisy_circuit.noisy_operations_count} noisy operations")
        result: Measurements = simulator.run_circuit(noisy_circuit.circuit, num_shots=self._num_shots)
        print(f"    Time Taken: {datetime.now() - start_time}")
        sum_measurements_per_shot = np.sum(result.measurements_per_shot, axis=1)
        nonzero_shots = np.count_nonzero(sum_measurements_per_shot)
        print(f"    Measurements per shot: {result.measurements_per_shot}")
        print(f"    {abs(self._num_shots * (not self._is_balanced) - nonzero_shots) / self._num_shots * 100:.1f}% success rate")

    def _set_configuration(self) -> None:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.majority_vote_repetitions = self._num_measurement_rounds
        configuration.noise_parameters.depolarization_probability_one_qubit = self._depolarization_probability_one_qubit
        configuration.noise_parameters.depolarization_probability_two_qubit = self._depolarization_probability_two_qubit

        configuration.measurer_type = MeasurerWithSingleQubit
        configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
        configuration.parallel = True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Deutsch-Josza Logical Error Rate Calculator',
        description='Runs the Deutsch-Josza algorithm using surface code and calculates the percentage of logical errors in the result.')
    parser.add_argument('-s', '--num-shots', type=int, default=1, help='Number of shots to run the algorithm for.')
    parser.add_argument('-q', '--num-input-qubits', type=int, default=2, help='Number of input qubits.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=3, help='Surface code distance.')
    parser.add_argument('-b', '--is-balanced', action="store_true", help='Surface code distance.')
    parser.add_argument('-r', '--num-measurement-rounds', type=int, default=3, help='Number of times to measure for majority voting. Minimum is 3.')
    args = parser.parse_args()

    DeutschJosza(
        num_shots=args.num_shots,
        num_input_qubits=args.num_input_qubits,
        surface_code_distance=args.surface_code_distance,
        is_balanced=args.is_balanced,
        num_measurement_rounds=max(3, args.num_measurement_rounds),
    ).run_main()
