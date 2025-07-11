import pytest
from numpy.ma.core import allequal

from stim_experiments.custom_dataclasses.state_and_measurements import StateAndMeasurements
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilitiesStateVector
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.simulators.simulator_using_circuits.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator
from tests.utilities import set_configuration_to_reduce_ancilla_qubits, set_seed


class DeutschJosza:
    def __init__(self, logical_qubits: list[MultipleCatCode], oracle: list[TransformationOperation], oracle_qubit_index: int):
        self._logical_qubits = logical_qubits
        self._oracle = oracle
        self._oracle_qubit_index = oracle_qubit_index

    def run_algorithm(self) -> StateAndMeasurements:
        input_qubit_indices = [i for i in range(len(self._logical_qubits)) if i != self._oracle_qubit_index]
        operations = [
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=self._oracle_qubit_index),
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=self._oracle_qubit_index),
            *self._oracle,
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=self._oracle_qubit_index),
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=self._oracle_qubit_index),
            *[TransformationOperation(gate=TransformationGate.M, target_qubit_index=i)
              for i in input_qubit_indices]
        ]
        simulator = LogicalOperationsCircuitCreator(encodings=self._logical_qubits, operations=operations)
        circuit = simulator.get_simulation_circuit()

        utilities = ErrorCorrectingCodeUtilitiesStateVector()
        return utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=len(simulator.data_qubits),
        )


class TestDeutschJosza:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_seed(0)
        set_configuration_to_reduce_ancilla_qubits()

    def test_deutsch_josza_constant(self):
        num_qubits = 3
        logical_qubits = [MultipleCatCode(num_cats=3, num_qubits_per_cat=3) for _ in range(num_qubits)]
        oracle = []
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=2)
        result = algorithm.run_algorithm()
        assert allequal(list(result.measurements.values()), [[0], [0]])

    def test_deutsch_josza_balanced(self):
        num_qubits = 3
        logical_qubits = [MultipleCatCode(num_cats=3, num_qubits_per_cat=3) for _ in range(num_qubits)]
        oracle = [
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=0, target_qubit_index=2),
            TransformationOperation(gate=TransformationGate.CX, control_qubit_index=1, target_qubit_index=2),
        ]
        algorithm = DeutschJosza(logical_qubits=logical_qubits, oracle=oracle, oracle_qubit_index=2)
        result = algorithm.run_algorithm()
        assert not allequal(list(result.measurements.values()), [[0], [0]])
