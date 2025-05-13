from abc import ABC, abstractmethod
from typing import List, Optional

from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, KET_ZERO, LineQubit, NoiseModel, \
    SimulationTrialResult, Simulator, \
    StateVectorTrialResult

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, TYPE_DENSITY_MATRIX, TYPE_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, is_state_vector, tensor, trace_out_ancillas_in_zero_state


class ErrorCorrectingCodeUtilities(ABC):
    # TODO delete this

    @property
    @abstractmethod
    def zero_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    @abstractmethod
    def _get_simulation_result(self,
                               circuit: Circuit,
                               initial_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                               noise_model: Optional[NoiseModel] = None,
                               ) -> StateAndMeasurements:
        pass

    def get_state_after_circuit(self,
                                circuit: Circuit,
                                num_data_qubits: int,
                                initial_data_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                                noise_model: Optional[NoiseModel] = None,
                                ) -> StateAndMeasurements:
        if initial_data_state is None:
            initial_data_state = tensor(*[self.zero_state] * num_data_qubits)
        qubits = LineQubit.range(self.get_max_qubit_index(circuit=circuit) + 1)
        num_ancillas = len(qubits) - num_data_qubits
        initial_state = tensor(initial_data_state, *[self.zero_state] * num_ancillas)

        simulation = self._get_simulation_result(circuit=circuit, initial_state=initial_state, noise_model=noise_model)
        data_state = trace_out_ancillas_in_zero_state(state=simulation.state, num_ancillas=num_ancillas)

        return StateAndMeasurements(
            state=data_state,
            measurements=dict(simulation.measurements),
        )

    def get_max_qubit_index(self, circuit: Circuit) -> int:
        return max(qubit.x for qubit in circuit.all_qubits())


class ErrorCorrectingCodeUtilitiesDensityMatrix(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_DENSITY_MATRIX:
        return KET_ZERO_DENSITY_MATRIX

    def _get_simulation_result(self,
                               circuit: Circuit,
                               initial_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                               noise_model: Optional[NoiseModel] = None,
                               ) -> StateAndMeasurements:
        simulator = DensityMatrixSimulator(noise=noise_model)
        simulation = simulator.simulate(circuit, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_density_matrix,
            measurements=dict(simulation.measurements),
        )


class ErrorCorrectingCodeUtilitiesStateVector(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_STATE_VECTOR:
        return KET_ZERO.state_vector()

    def _get_simulation_result(self,
                               circuit: Circuit,
                               initial_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                               noise_model: Optional[NoiseModel] = None,
                               ) -> StateAndMeasurements:
        simulator = Simulator(noise=noise_model)
        simulation: StateVectorTrialResult = simulator.simulate(circuit, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_state_vector,
            measurements=dict(simulation.measurements),
        )


def get_error_correcting_code_utilities(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> ErrorCorrectingCodeUtilities:
    return ErrorCorrectingCodeUtilitiesStateVector() if is_state_vector(state=state) else ErrorCorrectingCodeUtilitiesDensityMatrix()
