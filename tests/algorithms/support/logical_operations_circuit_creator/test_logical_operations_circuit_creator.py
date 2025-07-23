from typing import Optional

import pytest
from cirq import Circuit, H, I, X, Z, LineQubit

from stim_experiments.algorithms.support.logical_operations_circuit_creator.logical_operations_circuit_creator import \
    LogicalOperationsCircuitCreator
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, \
    states_are_equal, tensor
from tests.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits, set_seed


ENCODING_OPERATION_MARK = I


class LogicalBitsEncodingStub(ErrorCorrectingCode):
    def __init__(self, num_logical_bits: int, qubits: Optional[list[LineQubit]] = None):
        super().__init__(num_data_qubits=num_logical_bits,
                         num_logical_qubits=num_logical_bits,
                         qubits=qubits)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return Circuit([ENCODING_OPERATION_MARK(qubit) for qubit in self.data_qubits])

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


class TestLogicalOperationsCircuitCreator:
    def test_trivial(self):
        encodings = []
        simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=[])
        result = simulator.get_simulation_circuit()
        assert result == Circuit()

    def test_qubits_are_encoded(self):
        qubits = LineQubit.range(1)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))

        encodings = [LogicalBitsEncodingStub(num_logical_bits=1, qubits=qubits)]
        operations = []
        simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)
        circuit = simulator.get_simulation_circuit()
        encoding_operation_exists = list(circuit.findall_operations_with_gate_type(ENCODING_OPERATION_MARK.__class__))
        assert encoding_operation_exists

    def test_entanglement(self):
        set_configuration_to_reduce_ancilla_qubits()

        num_trials = 5
        results: list[StateAndMeasurements] = []
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))

        encodings = [
            LogicalBitsEncodingStub(num_logical_bits=1, qubits=qubits[:1]),
            LogicalBitsEncodingStub(num_logical_bits=1, qubits=qubits[1:])
        ]
        operations = [
            TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0),
            TransformationOperation(gate=TransformationGate.M, target_qubit_index=1)
        ]
        for trial in range(num_trials):
            set_seed(seed=trial)
            simulator = LogicalOperationsCircuitCreator(encodings=encodings, operations=operations)
            circuit = simulator.get_simulation_circuit()

            utilities = get_error_correcting_simulator(state=KET_ZERO_STATE_VECTOR)
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
