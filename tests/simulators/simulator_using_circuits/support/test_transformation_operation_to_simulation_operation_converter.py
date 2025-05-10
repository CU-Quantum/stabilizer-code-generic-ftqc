from enum import Enum, auto
from typing import List, Optional

import pytest
from cirq import Circuit, H, LineQubit, X, Z

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.simulator_using_circuits.custom_dataclasses.simulation_operation import \
    LogicalEncodingIndex, SimulationOperation, TargetEncoding
from stim_experiments.simulators.simulator_using_circuits.support.transformation_operation_to_simulation_operation import \
    TransformationOperationToSimulationOperationConverter
from stim_experiments.utilities import KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX, tensor


class ErrorCorrectingCodeStub(ErrorCorrectingCode):
    def __init__(self, num_logical_qubits: int = 1, qubit_start_index: int = 0, provided_ancilla_qubits: Optional[list[LineQubit]] = None, ):
        super().__init__(num_data_qubits=num_logical_qubits,
                         num_ancilla_qubits=0,
                         num_logical_qubits=num_logical_qubits,
                         initial_logical_qubit_state=tensor(*[KET_ZERO_STATE_VECTOR] * num_logical_qubits),
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        pass

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == TransformationGate.H:
            return Circuit(H(self.data_qubits[0]))
        if operation.gate == TransformationGate.X:
            return Circuit(X(self.data_qubits[0]))
        if operation.gate == TransformationGate.Z:
            return Circuit(Z(self.data_qubits[0]))
        return None

    @property
    def implemented_operations(self) -> List[LogicalGateLabel]:
        return [
            LogicalGateLabel.H,
            LogicalGateLabel.X,
            LogicalGateLabel.Z,
        ]


class TestTransformationOperationToSimulationOperationConverter:
    @pytest.mark.parametrize(['transformation_gate', 'logical_gate_label'], [
        (TransformationGate.X, LogicalGateLabel.X),
        (TransformationGate.Z, LogicalGateLabel.Z),
        (TransformationGate.H, LogicalGateLabel.H),
    ])
    def test_basic_target(self, transformation_gate: TransformationGate, logical_gate_label: LogicalGateLabel):
        code = ErrorCorrectingCodeStub()
        transformation_operation = TransformationOperation(gate=transformation_gate, target_qubit_index=0)
        converter = TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                          encodings=[code])
        simulation_operation = converter.get_simulation_operation()
        assert simulation_operation == SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=logical_gate_label,
                    qubit_index=0,
                ),
                encoding=code,
            )
        )

    def test_target_on_multiple_encodings(self):
        encodings = [
            ErrorCorrectingCodeStub(),
            ErrorCorrectingCodeStub(qubit_start_index=1)
        ]
        transformation_operation = TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)
        converter = TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                          encodings=encodings)
        simulation_operation = converter.get_simulation_operation()
        assert simulation_operation == SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.X,
                    qubit_index=0,
                ),
                encoding=encodings[1],
            )
        )

    def test_target_on_multiqubit_encodings(self):
        encodings = [
            ErrorCorrectingCodeStub(num_logical_qubits=2),
            ErrorCorrectingCodeStub(num_logical_qubits=2, qubit_start_index=2)
        ]
        transformation_operation = TransformationOperation(gate=TransformationGate.X, target_qubit_index=3)
        converter = TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                          encodings=encodings)
        simulation_operation = converter.get_simulation_operation()
        assert simulation_operation == SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.X,
                    qubit_index=1,
                ),
                encoding=encodings[1],
            )
        )

    @pytest.mark.parametrize(['transformation_gate', 'logical_gate_label'], [
        (TransformationGate.CX, LogicalGateLabel.X),
        (TransformationGate.CZ, LogicalGateLabel.Z),
    ])
    def test_controlled_operation(self, transformation_gate: TransformationGate, logical_gate_label: LogicalGateLabel):
        encodings = [
            ErrorCorrectingCodeStub(),
            ErrorCorrectingCodeStub(qubit_start_index=1)
        ]
        transformation_operation = TransformationOperation(gate=transformation_gate, target_qubit_index=0, control_qubit_index=1)
        converter = TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                          encodings=encodings)
        simulation_operation = converter.get_simulation_operation()
        assert simulation_operation == SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=logical_gate_label,
                    qubit_index=0,
                ),
                encoding=encodings[0],
            ),
            control_encoding=LogicalEncodingIndex(
                encoding=encodings[1],
                qubit_index_relative=0,
            )
        )

    def test_measurement_operation(self):
        encodings = [
            ErrorCorrectingCodeStub(),
        ]
        transformation_operation = TransformationOperation(gate=TransformationGate.M, target_qubit_index=0)
        converter = TransformationOperationToSimulationOperationConverter(transformation_operation=transformation_operation,
                                                                          encodings=encodings)
        simulation_operation = converter.get_simulation_operation()
        assert simulation_operation == SimulationOperation(
            control_encoding=LogicalEncodingIndex(
                encoding=encodings[0],
                qubit_index_relative=0,
            )
        )

    def test_validates_operation(self):
        invalid_transformation_operation = TransformationOperation(gate=TransformationGate.X, target_qubit_index=0, control_qubit_index=1)
        converter = TransformationOperationToSimulationOperationConverter(
            transformation_operation=invalid_transformation_operation,
            encodings=[])
        with pytest.raises(ValueError):
            converter.get_simulation_operation()

    def test_unimplemented_transformation_operation(self):
        class InvalidTransformationGate(Enum):
            INVALID = auto()
        transformation_operation = TransformationOperation(gate=InvalidTransformationGate.INVALID,
                                                           target_qubit_index=0)
        converter = TransformationOperationToSimulationOperationConverter(
            transformation_operation=transformation_operation,
            encodings=[])
        with pytest.raises(ValueError, match="Unimplemented transformation gate INVALID."):
            converter.get_simulation_operation()
