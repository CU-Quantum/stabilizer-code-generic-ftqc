from dataclasses import dataclass
from typing import Dict

from numpy import array
from numpy._typing import NDArray

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.utilities import TYPE_DENSITY_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit


class SimulatorCircuit:
    pass


@dataclass
class SimulatorResult:
    state: TYPE_DENSITY_MATRIX
    measurements: Dict[str, NDArray[bool]]

    def __eq__(self, other):
        keys = zip(self.measurements, other.measurements)
        values = zip(self.measurements.values(), other.measurements.values())
        return (self.state.tolist() == other.state.tolist()
                and all(key == other_key for key, other_key in keys)
                and all(value == other_value for value, other_value in values))


class SimulatorUsingCircuits:
    def __init__(self, error_correcting_code: ErrorCorrectingCode):
        self._error_correcting_code = error_correcting_code

    def simulate(self, circuit: SimulatorCircuit) -> SimulatorResult:
        return SimulatorResult(
            state=array([[]]),
            measurements={},
        )


class TestSimulatorCircuit:
    def test_trivial(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        simulator = SimulatorUsingCircuits(error_correcting_code=code)
        circuit = SimulatorCircuit()
        result = simulator.simulate(circuit=circuit)
        assert result == SimulatorResult(
            state=array([[]]),
            measurements={},
        )
