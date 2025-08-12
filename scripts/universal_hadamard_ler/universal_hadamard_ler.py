import argparse

from scripts.script_runner import RunnerConfiguration, ScriptRunner
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation


class UniversalHadamardLer:
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
        num_hadamard_repetitions = 2
        operations = [
            *[TransformationOperation(gate=TransformationGate.H, target_qubit_index=0)
              for _ in range(num_hadamard_repetitions)],
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=0)
        ]
        return ScriptRunner(
            operations=operations,
            runner_configuration=RunnerConfiguration(
                num_shots=self._num_shots,
                surface_code_distance=self._surface_code_distance,
                num_measurement_rounds=self._num_measurement_rounds,
                depolarization_probability_one_qubit=self._depolarization_probability_one_qubit,
                depolarization_probability_two_qubit=self._depolarization_probability_two_qubit,
            ),
        ).run_main()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Hadamard Logical Error Rate Calculator',
        description='Runs the universal Hadamard operation twice using surface code and calculates the percentage of zero measurements.')
    parser.add_argument('-s', '--num-shots', type=int, default=10, help='Number of shots to run the algorithm for.')
    parser.add_argument('-d', '--surface-code-distance', type=int, default=3, help='Surface code distance.')
    parser.add_argument('-r', '--num-measurement-rounds', type=int, default=3, help='Number of times to measure for majority voting. Minimum is 3.')
    parser.add_argument('-p1', '--prob-one-qubit-error', type=int, default=1e-3, help='Probability of depolarization on one qubit gates.')
    parser.add_argument('-p2', '--prob-two-qubit-error', type=int, default=2e-3, help='Probability of depolarization on two qubit gates.')
    args = parser.parse_args()
    print(f"Running Universal Hadamard Logical Error Rate Calculator with arguments: {args}")

    UniversalHadamardLer(
        num_shots=args.num_shots,
        surface_code_distance=args.surface_code_distance,
        num_measurement_rounds=max(3, args.num_measurement_rounds),
        depolarization_probability_one_qubit=args.prob_one_qubit_error,
        depolarization_probability_two_qubit=args.prob_two_qubit_error,
    ).run_main()
