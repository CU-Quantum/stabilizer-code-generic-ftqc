from stim_experiments.custom_dataclasses.state_and_measurements import StateAndMeasurements
from stim_experiments.custom_dataclasses.transformation_operation import TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilitiesStateVector
from stim_experiments.error_correcting_codes.support.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.simulators.simulator_using_circuits.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator


class DeutschJosza:
    def __init__(self, logical_qubits: list[ErrorCorrectingCode], oracle: list[TransformationOperation], oracle_qubit_index: int):
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
