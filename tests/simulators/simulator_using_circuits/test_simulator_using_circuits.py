from typing import List, Optional

from cirq import Circuit, H, X, Z, kron
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult
from stim_experiments.simulators.simulator_using_circuits.simulator_using_circuits import SimulatorUsingCircuits
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, \
    KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit


class LogicalBitsEncodingStub(ErrorCorrectingCode):
    def __init__(self, num_logical_bits: int,
                 initial_logical_qubit_state: Optional[TYPE_STATE_VECTOR_OR_DENSITY_MATRIX] = None,
                 qubit_start_index: int = 0):
        if initial_logical_qubit_state is None:
            initial_logical_qubit_state = kron(*[KET_ZERO_STATE_VECTOR] * num_logical_bits, shape_len=1)
        super().__init__(num_data_qubits=num_logical_bits,
                         num_ancilla_qubits=0,
                         num_logical_qubits=num_logical_bits,
                         initial_logical_qubit_state=initial_logical_qubit_state,
                         qubit_start_index=qubit_start_index)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        return self._initial_logical_qubit_state

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
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=[])
        result = simulator.simulate()
        assert result == SimulatorResult(
            current_state=array([]),
            measurements={},
        )

    def test_logical_x(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1)
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        expected_state = KET_ONE_STATE_VECTOR
        assert result == SimulatorResult(
            current_state=expected_state,
            measurements={},
        )

    def test_logical_z(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1, initial_logical_qubit_state=KET_ONE_STATE_VECTOR)
        operations = [TransformationOperation(gate=TransformationGate.Z, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        expected_state = -KET_ONE_STATE_VECTOR
        assert result == SimulatorResult(
            current_state=expected_state,
            measurements={},
        )

    def test_logical_h(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1)
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        operations = [TransformationOperation(gate=TransformationGate.H, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        expected_state = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                               initial_logical_qubit_state=kron(KET_PLUS_STATE_VECTOR,
                                                                                KET_ZERO_STATE_VECTOR).flatten()
                                               ).encode_logical_qubit()
        assert result == SimulatorResult(
            current_state=expected_state,
            measurements={},
        )

    def test_multiple_encodings(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1)
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        expected_state = kron(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        assert result == SimulatorResult(
            current_state=expected_state,
            measurements={},
        )

    def test_multiple_logical_qubits_single_encoding(self):
        code = LogicalBitsEncodingStub(num_logical_bits=2)
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        expected_state = kron(KET_ZERO_STATE_VECTOR, KET_ONE_STATE_VECTOR).flatten()
        assert result == SimulatorResult(
            current_state=expected_state,
            measurements={},
        )

    def test_logical_cx(self):
        code = LogicalBitsEncodingStub(num_logical_bits=1)
        operations = [
            TransformationOperation(gate=TransformationGate.X, target_qubit_index=0),
            TransformationOperation(gate=TransformationGate.CX, target_qubit_index=1, control_qubit_index=0)
        ]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        expected_state = kron(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR, shape_len=1)
        assert result == SimulatorResult(
            current_state=expected_state,
            measurements={},
        )
