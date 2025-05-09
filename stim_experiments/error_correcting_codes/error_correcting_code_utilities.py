from abc import ABC, abstractmethod
from typing import List, Optional

from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, KET_ZERO, LineQubit, NoiseModel, Simulator, \
    StateVectorTrialResult

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, TYPE_DENSITY_MATRIX, TYPE_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, is_state_vector


class ErrorCorrectingCodeUtilities(ABC):
    # TODO delete this

    @property
    @abstractmethod
    def zero_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    @abstractmethod
    def get_state_after_circuit(self,
                                circuit: Circuit,
                                qubit_order: List[LineQubit],
                                initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX,
                                noise_model: Optional[NoiseModel] = None,
                                ) -> StateAndMeasurements:
        pass

    def get_max_qubit_index(self, circuit: Circuit) -> int:
        return max(qubit.x for qubit in circuit.all_qubits())


class ErrorCorrectingCodeUtilitiesDensityMatrix(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_DENSITY_MATRIX:
        return KET_ZERO_DENSITY_MATRIX

    def get_state_after_circuit(self,
                                qubit_order: List[LineQubit],
                                circuit: Circuit,
                                initial_state: TYPE_DENSITY_MATRIX,
                                noise_model: Optional[NoiseModel] = None,
                                ) -> StateAndMeasurements:
        simulator = DensityMatrixSimulator(noise=noise_model)
        simulation: DensityMatrixTrialResult = simulator.simulate(circuit, qubit_order=qubit_order, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_density_matrix,
            measurements=dict(simulation.measurements),
        )


class ErrorCorrectingCodeUtilitiesStateVector(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_STATE_VECTOR:
        return KET_ZERO.state_vector()

    def get_state_after_circuit(self,
                                circuit: Circuit,
                                qubit_order: List[LineQubit],
                                initial_state: TYPE_STATE_VECTOR,
                                noise_model: Optional[NoiseModel] = None
                                ) -> StateAndMeasurements:
        simulator = Simulator(noise=noise_model)
        simulation: StateVectorTrialResult = simulator.simulate(circuit, qubit_order=qubit_order, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_state_vector,
            measurements=dict(simulation.measurements),
        )


def get_error_correcting_code_utilities(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> ErrorCorrectingCodeUtilities:
    return ErrorCorrectingCodeUtilitiesStateVector() if is_state_vector(state=state) else ErrorCorrectingCodeUtilitiesDensityMatrix()
