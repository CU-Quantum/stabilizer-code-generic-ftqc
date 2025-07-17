from typing import Optional

from cirq import Circuit, LineQubit, NOISE_MODEL_LIKE

from custom_dataclasses.state_and_measurements import StateAndMeasurements
from error_correcting_codes.error_correcting_code_utilities import ErrorCorrectingCodeUtilities
from utilities.utilities import KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class SimulatorClifford(ErrorCorrectingCodeUtilities):
    @property
    def zero_state(self) -> TYPE_STATE_VECTOR:
        return KET_ZERO_STATE_VECTOR

    def _get_simulation_result(self,
                               circuit: Circuit,
                               qubits: list[LineQubit],
                               initial_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                               noise_model: Optional[NOISE_MODEL_LIKE] = None) -> StateAndMeasurements:
        return StateAndMeasurements(state=KET_ZERO_STATE_VECTOR, measurements={})


class TestSimulatorClifford:
    def test_trivial(self):
        circuit = Circuit()
        simulator =  SimulatorClifford()
        result = simulator.get_state_after_circuit(circuit=circuit, num_data_qubits=0)
        assert result == StateAndMeasurements(state=KET_ZERO_STATE_VECTOR, measurements={})
