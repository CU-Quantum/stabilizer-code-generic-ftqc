import numpy as np
from numpy._typing import NDArray

from scripts.script_runner import RunnerConfiguration, ScriptRunner, get_runner_configuration_args
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation


class UniversalHadamard:
    def __init__(self, run_configuration: RunnerConfiguration,):
        self._run_configuration = run_configuration

    def run_main(self):
        operations = [
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.Z, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=0)
        ]
        return ScriptRunner(
            operations=operations,
            was_successful_func=self._was_successful,
            runner_configuration=self._run_configuration,
        ).run_main()

    def _was_successful(self, measurements_per_shot: list[NDArray[int]]) -> NDArray[bool]:
        return np.array(measurements_per_shot)[:,0] if measurements_per_shot else np.array([])


if __name__ == "__main__":
    run_configuration = get_runner_configuration_args()
    UniversalHadamard(run_configuration=run_configuration).run_main()
