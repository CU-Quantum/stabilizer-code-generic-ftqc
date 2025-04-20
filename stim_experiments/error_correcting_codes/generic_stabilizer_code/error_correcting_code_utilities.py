from abc import ABC, abstractmethod
from typing import List

from cirq import Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, KET_ZERO, LineQubit, Simulator, \
    StateVectorTrialResult
from numpy import array

from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, TYPE_DENSITY_MATRIX, TYPE_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class ErrorCorrectingCodeUtilities(ABC):
    @property
    @abstractmethod
    def zero_state(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    @abstractmethod
    def get_state_after_circuit(self,
                                circuit: Circuit,
                                qubit_order: List[LineQubit],
                                initial_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
                                ) -> StateAndMeasurements:
        pass

    @abstractmethod
    def reshape_state(self, state: TYPE_DENSITY_MATRIX, num_qubits: int) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass


class ErrorCorrectingCodeUtilitiesDensityMatrix(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_DENSITY_MATRIX:
        return KET_ZERO_DENSITY_MATRIX

    def get_state_after_circuit(self,
                                circuit: Circuit,
                                qubit_order: List[LineQubit],
                                initial_state: TYPE_DENSITY_MATRIX
                                ) -> StateAndMeasurements:
        simulator = DensityMatrixSimulator()
        simulation: DensityMatrixTrialResult = simulator.simulate(circuit, qubit_order=qubit_order, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_density_matrix,
            measurements=array(list(simulation.measurements.values())).flatten(),
        )

    def reshape_state(self, state: TYPE_DENSITY_MATRIX, num_qubits: int) -> TYPE_DENSITY_MATRIX:
        return state.reshape(2 ** num_qubits, 2 ** num_qubits)


class ErrorCorrectingCodeUtilitiesStateVector(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_STATE_VECTOR:
        return KET_ZERO.state_vector()

    def get_state_after_circuit(self, circuit: Circuit, qubit_order: List[LineQubit], initial_state: TYPE_STATE_VECTOR) -> StateAndMeasurements:
        simulator = Simulator()
        simulation: StateVectorTrialResult = simulator.simulate(circuit, qubit_order=qubit_order, initial_state=initial_state)
        return StateAndMeasurements(
            state=simulation.final_state_vector,
            measurements=array(list(simulation.measurements.values())).flatten(),
        )

    def reshape_state(self, state: TYPE_STATE_VECTOR, num_qubits: int) -> TYPE_STATE_VECTOR:
        return state.reshape(2 ** num_qubits,)
