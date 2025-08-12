import argparse

import numpy as np
from numpy._typing import NDArray

from scripts.script_runner import RunnerConfiguration, ScriptRunner, add_runner_configuration_args
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation


class UniversalCnot:
    def __init__(self, run_configuration: RunnerConfiguration,):
        self._run_configuration = run_configuration

    def run_main(self):
        operations = [
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=0, target_qubit_index=1),
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=1),
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=0),
        ]
        return ScriptRunner(
            operations=operations,
            was_successful_func=self._was_successful,
            runner_configuration=self._run_configuration,
        ).run_main()

    def _was_successful(self, measurements_per_shot: list[NDArray[int]]) -> NDArray[bool]:
        return np.array([
            measurement_per_shot[0] == measurement_per_shot[1]
            for measurement_per_shot in measurements_per_shot
        ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='Hadamard Logical Error Rate Calculator',
        description='Runs the universal Hadamard operation twice using surface code and calculates the percentage of zero measurements.')
    add_runner_configuration_args(parser=parser)
    args = parser.parse_args()
    print(f"Running Universal Hadamard Logical Error Rate Calculator with arguments: {args}")

    UniversalCnot(
        run_configuration=RunnerConfiguration(
            num_shots=args.num_shots,
            surface_code_distance=args.surface_code_distance,
            num_measurement_rounds=max(3, args.num_measurement_rounds),
            depolarization_probability_one_qubit=args.prob_one_qubit_error,
            depolarization_probability_two_qubit=args.prob_two_qubit_error,
        )
    ).run_main()
