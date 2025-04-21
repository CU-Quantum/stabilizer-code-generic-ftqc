from typing import List, Optional

import numpy.random
import pytest
from cirq import Circuit, H, X, Z, kron, LineQubit
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.state_and_measurements import \
    StateAndMeasurements
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.simulator_using_circuits import SimulatorUsingCircuits
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, \
    KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
from tests.utilities import states_are_equal


# TODO simulate error correction
class LogicalBitsEncodingStub(ErrorCorrectingCode):
    def __init__(self,
                 num_logical_bits: int,
                 num_ancilla_bits: int = 0,
                 initial_logical_qubit_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                 qubit_start_index: int = 0,
                 provided_ancilla_qubits: Optional[List[LineQubit]] = None, ):
        if initial_logical_qubit_state is None:
            initial_logical_qubit_state = kron(*[KET_ZERO_STATE_VECTOR] * num_logical_bits, shape_len=1)
        super().__init__(num_data_qubits=num_logical_bits,
                         num_ancilla_qubits=num_ancilla_bits,
                         num_logical_qubits=num_logical_bits,
                         initial_logical_qubit_state=initial_logical_qubit_state,
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        ancillas_state = kron(*[KET_ZERO_STATE_VECTOR] * self._num_ancilla_qubits, shape_len=1)
        return kron(self._initial_logical_qubit_state, ancillas_state, shape_len=1)

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

    @property
    def _implemented_operations(self) -> List[LogicalGateLabel]:
        return [
            LogicalGateLabel.X,
            LogicalGateLabel.Z,
            LogicalGateLabel.H,
        ]


class TestSimulatorCircuit:
    def test_trivial(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1)
        simulator = SimulatorUsingCircuits(error_correcting_codes=code, operations=[])
        result = simulator.simulate()
        assert result == StateAndMeasurements(
            state=array([]),
            measurements={},
        )

    @pytest.mark.parametrize('codes', [
        LogicalBitsEncodingStub(num_logical_bits=1, num_ancilla_bits=2),
        [
            LogicalBitsEncodingStub(num_logical_bits=1, num_ancilla_bits=1),
            LogicalBitsEncodingStub(num_logical_bits=1, num_ancilla_bits=2)
        ]
    ])
    def test_shared_ancilla_qubits(self, codes: ErrorCorrectingCode | list[ErrorCorrectingCode]):
        operations_requiring_two_encodings = [
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)
        ]
        simulator = SimulatorUsingCircuits(
            error_correcting_codes=codes,
            operations=operations_requiring_two_encodings,
        )
        result = simulator.simulate()

        expected_states_data = kron(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        only_two_ancilla = kron(KET_ZERO_STATE_VECTOR, KET_ZERO_STATE_VECTOR, shape_len=1)
        expected_state = kron(expected_states_data, only_two_ancilla, shape_len=1)
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements={},
        )

    def test_creates_enough_encodings_necessary_for_operations(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1)
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)]
        simulator = SimulatorUsingCircuits(error_correcting_codes=code, operations=operations)
        result = simulator.simulate()
        expected_state = kron(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements={},
        )

    def test_multiple_logical_qubits_single_encoding(self):
        code = LogicalBitsEncodingStub(num_logical_bits=2)
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)]
        simulator = SimulatorUsingCircuits(error_correcting_codes=code, operations=operations)
        result = simulator.simulate()
        expected_state = kron(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR).flatten()
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements={},
        )

    def test_entanglement(self):
        arbitrary_seed = 0
        numpy.random.seed(arbitrary_seed)
        num_trials = 5
        results: list[StateAndMeasurements] = []
        for trial in range(num_trials):
            code = LogicalBitsEncodingStub(num_logical_bits=1)
            operations = [
                TransformationOperation(gate=TransformationGate.H, target_qubit_index=0),
                TransformationOperation(TransformationGate.M, target_qubit_index=0)
            ]
            simulator = SimulatorUsingCircuits(error_correcting_codes=code, operations=operations)
            result = simulator.simulate()
            results.append(result)
        observables = [result.measurements[0][0] for result in results if result.measurements[0]]
        assert any(observables) and not all(observables)
        assert all(states_are_equal(result.state, KET_ONE_STATE_VECTOR if result.measurements[0][0] else KET_ZERO_STATE_VECTOR)
                   for result in results)

    def test_multiple_codes(self):
        codes = [
            LogicalBitsEncodingStub(num_logical_bits=1),
            LogicalBitsEncodingStub(num_logical_bits=2)
        ]

        operations = [
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=2)
        ]

        simulator = SimulatorUsingCircuits(error_correcting_codes=codes, operations=operations)
        result = simulator.simulate()

        expected_state = kron(KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        assert result == StateAndMeasurements(
            state=expected_state,
            measurements={},
        )

    def test_not_enough_logical_qubits_error(self):
        codes = [LogicalBitsEncodingStub(num_logical_bits=1)]

        operations = [
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=1),
        ]

        simulator = SimulatorUsingCircuits(error_correcting_codes=codes, operations=operations)

        with pytest.raises(ValueError, match="Not enough logical qubits available. "
                                             "Operations need at least 2 logical qubits, but 1 was/were provided."):
            simulator.simulate()
