from abc import ABC, abstractmethod
from typing import Optional

from cirq import Circuit, DensityMatrixSimulator, KET_ZERO, LineQubit, NOISE_MODEL_LIKE, \
    Simulator, \
    StateVectorTrialResult
from qsimcirq import QSimOptions, QSimSimulator

from stim_experiments.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.utilities import KET_ZERO_DENSITY_MATRIX, KET_ZERO_STATE_VECTOR, TYPE_DENSITY_MATRIX, \
    TYPE_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, get_num_qubits_in_state, is_state_vector, tensor, \
    trace_out_ancillas_in_zero_state


class ErrorCorrectingCodeUtilities(ABC):
    @property
    @abstractmethod
    def zero_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    @abstractmethod
    def _get_simulation_result(self,
                               circuit: Circuit,
                               qubits: list[LineQubit],
                               initial_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                               noise_model: Optional[NOISE_MODEL_LIKE] = None,
                               ) -> StateAndMeasurements:
        pass

    def get_state_after_circuit(self,
                                circuit: Circuit,
                                num_data_qubits: int,
                                initial_data_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                                noise_model: Optional[NOISE_MODEL_LIKE] = None,
                                ) -> StateAndMeasurements:
        if initial_data_state is None:
            initial_data_state = tensor(*[self.zero_state] * num_data_qubits)
        qubits = LineQubit.range(self.get_max_qubit_index(circuit=circuit) + 1)
        num_ancillas = len(qubits) - num_data_qubits
        initial_state = tensor(initial_data_state, *[self.zero_state] * num_ancillas)

        simulation = self._get_simulation_result(circuit=circuit, qubits=qubits, initial_state=initial_state, noise_model=noise_model)
        data_state = trace_out_ancillas_in_zero_state(state=simulation.state, num_ancillas=num_ancillas)

        return StateAndMeasurements(
            state=data_state,
            measurements=simulation.measurements,
        )

    def get_max_qubit_index(self, circuit: Circuit) -> int:
        all_qubits = list(circuit.all_qubits())
        return max(all_qubits).x if all_qubits else -1

    @property
    def _seed(self) -> int:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().seed


class ErrorCorrectingCodeUtilitiesDensityMatrix(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) ->  TYPE_DENSITY_MATRIX:
        return KET_ZERO_DENSITY_MATRIX

    def _get_simulation_result(self,
                               circuit: Circuit,
                               qubits: list[LineQubit],
                               initial_state: Optional[TYPE_DENSITY_MATRIX] = None,
                               noise_model: Optional[NOISE_MODEL_LIKE] = None,
                               ) -> StateAndMeasurements:
        simulator = DensityMatrixSimulator(noise=noise_model, seed=self._seed)
        num_qubits = get_num_qubits_in_state(state=initial_state) if initial_state is not None else len(qubits)
        initial_state = tensor(initial_state, *[KET_ZERO] * (len(qubits) - num_qubits))
        simulation = simulator.simulate(circuit, qubit_order=qubits, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_density_matrix,
            measurements=dict(simulation.measurements),
        )


class ErrorCorrectingCodeUtilitiesStateVector(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_STATE_VECTOR:
        return KET_ZERO_STATE_VECTOR

    def _get_simulation_result(self,
                               circuit: Circuit,
                               qubits: list[LineQubit],
                               initial_state: Optional[TYPE_STATE_VECTOR] = None,
                               noise_model: Optional[NOISE_MODEL_LIKE] = None,
                               ) -> StateAndMeasurements:
        simulator = Simulator(noise=noise_model, seed=self._seed)
        simulation: StateVectorTrialResult = simulator.simulate(circuit, qubit_order=qubits, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_state_vector,
            measurements=dict(simulation.measurements),
        )


class ErrorCorrectingCodeUtilitiesMultiGpu(ErrorCorrectingCodeUtilities):
    """Must be run in cuQuantum Appliance Docker container. See https://quantumai.google/qsim/choose_hw for more information."""
    @property
    def zero_state(self) -> TYPE_STATE_VECTOR:
        return KET_ZERO_DENSITY_MATRIX

    def _get_simulation_result(self,
                               circuit: Circuit,
                               qubits: list[LineQubit],
                               initial_state: Optional[TYPE_DENSITY_MATRIX] = None,
                               noise_model: Optional[NOISE_MODEL_LIKE] = None,
                               ) -> StateAndMeasurements:
        qsim_options = QSimOptions(gpu_mode=16, verbosity=3, denormals_are_zeros=True)
        simulator = QSimSimulator(qsim_options=qsim_options, noise=noise_model, seed=self._seed)
        result = simulator.simulate(program=circuit)
        return StateAndMeasurements(
            state=result.final_state_vector,
            measurements=dict(result.measurements),
        )


def get_error_correcting_code_utilities(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> ErrorCorrectingCodeUtilities:
    return ErrorCorrectingCodeUtilitiesStateVector() if is_state_vector(state=state) else ErrorCorrectingCodeUtilitiesDensityMatrix()
