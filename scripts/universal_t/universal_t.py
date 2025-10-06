from functools import cached_property

import numpy as np
from numpy._typing import NDArray

from scripts.script_runner import RunnerConfiguration, ScriptRunner, SuccessfulResultsInfoSimulator, \
    get_runner_configuration_args, simulate_circuit
from stim_experiments.custom_dataclasses.state_and_measurements import StateAndMeasurements
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit_sequential import \
    MeasurerWithSingleQubitSequential
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.utilities import states_are_equal


class UniversalT:
    def __init__(self, run_configuration: RunnerConfiguration,):
        self._run_configuration = run_configuration

    def run_main(self):
        return self.script_runner.run_main()

    def was_successful(self, state_and_measurements: list[StateAndMeasurements]) -> NDArray[bool]:
        return np.array([
            states_are_equal(state_and_measurement.state, self.ideal_simulation.state,)
            for state_and_measurement in state_and_measurements
        ])

    @cached_property
    def ideal_simulation(self) -> StateAndMeasurements:
        self._set_ideal_configuration()
        circuit_noiseless = self.script_runner.circuit_noiseless
        return simulate_circuit(circuit=circuit_noiseless, num_data_qubits=len(self.script_runner.circuit_creator.data_qubits))

    def _set_ideal_configuration(self) -> None:
        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.majority_vote_repetitions = 1
        configuration.noise_parameters.depolarization_probability_one_qubit = 0
        configuration.noise_parameters.depolarization_probability_two_qubit = 0

        configuration.measurer_type = MeasurerWithSingleQubitSequential
        configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit

    @property
    def script_runner(self) -> ScriptRunner:
        return ScriptRunner(
            operations=self.operations,
            successful_results_info=SuccessfulResultsInfoSimulator(num_processes=self._run_configuration.num_processes,
                                                                   was_successful_func=self.was_successful,),
            runner_configuration=self._run_configuration,
        )

    @property
    def operations(self) -> list[TransformationOperation]:
        return [TransformationOperation(gate=TransformationGate.T, target_qubit_index=0)]


if __name__ == "__main__":
    run_configuration = get_runner_configuration_args()
    UniversalT(run_configuration=run_configuration).run_main()
