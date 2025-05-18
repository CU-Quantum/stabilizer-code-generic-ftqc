from typing import Optional

import numpy.random
import pytest
from cirq import Circuit, H, I, X, Z, LineQubit
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_enums.universal_hadamard_type import UniversalHadamardType
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.simulators.simulator_using_circuits.logical_operations_circuit_creator import LogicalOperationsCircuitCreator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, \
    get_num_qubits_in_state, states_are_equal, tensor


class LogicalBitsEncodingStub(ErrorCorrectingCode):
    def __init__(self, num_logical_bits: int, qubits: Optional[list[LineQubit]] = None):
        super().__init__(num_data_qubits=num_logical_bits,
                         num_logical_qubits=num_logical_bits,
                         qubits=qubits)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return Circuit([I(qubit) for qubit in self.data_qubits])

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Circuit:
        gates = []
        if operation.gate == LogicalGateLabel.X:
            gates = [X(self.data_qubits[operation.qubit_index])]
        elif operation.gate == LogicalGateLabel.Z:
            gates = [Z(self.data_qubits[operation.qubit_index])]
        elif operation.gate == LogicalGateLabel.H:
            gates = [H(self.data_qubits[operation.qubit_index])]
        return Circuit(gates)


class TestLogicalOperationsSimulator:
    def test_trivial(self):
        encodings = []
        simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=[])
        result = simulator.get_simulation_circuit()
        assert result == Circuit()

    @pytest.mark.skip('Universal CX/CZ not yet implemented.')
    def test_entanglement(self):
        arbitrary_seed = 0
        numpy.random.seed(arbitrary_seed)
        ConfigurationErrorCorrectingCodeManager().get_configuration().universal_hadamard_type = UniversalHadamardType.SINGLE_ANCILLA

        num_trials = 5
        results: list[StateAndMeasurements] = []
        for trial in range(num_trials):
            encodings = [
                LogicalBitsEncodingStub(num_logical_bits=1),
                LogicalBitsEncodingStub(num_logical_bits=1, qubits=LineQubit.range(1, 2))
            ]
            operations = [
                TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
                TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0),
                TransformationOperation(TransformationGate.M, target_qubit_index=1)
            ]
            simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)
            circuit = simulator.get_simulation_circuit()

            utilities = get_error_correcting_code_utilities(state=KET_ZERO_STATE_VECTOR)
            result = utilities.get_state_after_circuit(
                circuit=circuit,
                num_data_qubits=len(simulator.data_qubits),
            )
            results.append(result)
        observables = [result.measurements['1'][0] for result in results]
        assert any(observables) and not all(observables)
        assert all(states_are_equal(result.state, tensor(*[KET_ONE_STATE_VECTOR if observable else KET_ZERO_STATE_VECTOR] * 2))
                   for observable, result in zip(observables, results))

    def test_not_enough_logical_qubits_error(self):
        encodings = [LogicalBitsEncodingStub(num_logical_bits=1)]

        operations = [
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=1),
        ]

        simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)

        with pytest.raises(ValueError, match="Not enough logical qubits available. "
                                             "Operations need at least 2 logical qubits, but 1 was/were provided."):
            simulator.get_simulation_circuit()
