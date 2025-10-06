import numpy as np
from numpy._typing import NDArray

from scripts.script_runner import RunnerConfiguration, ScriptRunner, SuccessfulResultsInfoRunner, \
    get_runner_configuration_args
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation


class UniversalCnot:
    def __init__(self, run_configuration: RunnerConfiguration,):
        self._run_configuration = run_configuration

    def run_main(self):
        operations = [
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=0, target_qubit_index=1),
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=1),
        ]
        return ScriptRunner(
            operations=operations,
            successful_results_info=SuccessfulResultsInfoRunner(num_processes=self._run_configuration.num_processes,
                                                                was_successful_func=self.was_successful),
            runner_configuration=self._run_configuration,
        ).run_main()

    @staticmethod
    def was_successful(measurements_per_shot: list[NDArray[int]]) -> NDArray[bool]:
        return np.array([
            measurement_per_shot[0] == measurement_per_shot[1]
            for measurement_per_shot in measurements_per_shot
        ])


if __name__ == "__main__":
    run_configuration = get_runner_configuration_args()
    UniversalCnot(run_configuration=run_configuration).run_main()
