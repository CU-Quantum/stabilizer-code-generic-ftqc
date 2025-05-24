from unittest.mock import MagicMock, patch

import pytest
from cirq import Circuit, LineQubit

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import SimulationOperation, TargetEncoding
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.simulators.simulator_using_circuits.support.circuit_from_operation_creator import CircuitFromOperationCreator


class ErrorCorrectingCodeStubNoHadamard(ErrorCorrectingCode):
    def __init__(self, num_logical_qubits: int = 1, qubits=None):
        super().__init__(num_data_qubits=num_logical_qubits,
                         num_logical_qubits=num_logical_qubits,
                         qubits=qubits or LineQubit.range(num_logical_qubits))

    def encode_logical_qubit(self):
        pass

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation):
        return None


class ErrorCorrectingCodeStubWithHadamard(ErrorCorrectingCode):
    def __init__(self, num_logical_qubits: int = 1, qubits=None):
        super().__init__(num_data_qubits=num_logical_qubits,
                         num_logical_qubits=num_logical_qubits,
                         qubits=qubits or LineQubit.range(num_logical_qubits))

    def encode_logical_qubit(self):
        pass

    def get_error_correction_circuit(self) -> Circuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation):
        if operation.gate == LogicalGateLabel.H:
            return Circuit()
        return None


class UniversalHadamardStub(UniversalHadamard):
    universal_used = False

    def __init__(self, code: ErrorCorrectingCode, qubit_index: int):
        super().__init__(code=code, qubit_index=qubit_index)
        self.__class__.universal_used = False

    def get_hadamard_circuit(self) -> Circuit:
        self.__class__.universal_used = True
        return Circuit()


class TestCircuitFromOperationCreator:
    @pytest.fixture(autouse=True)
    def _reset_universal_hadamard_stub(self):
        UniversalHadamardStub.universal_used = False
        yield
        UniversalHadamardStub.universal_used = False

    def test_universal_hadamard_used_when_encoding_does_not_implement_hadamard(self):
        encoding = ErrorCorrectingCodeStubNoHadamard()
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.H,
                    qubit_index=0,
                ),
                encoding=encoding,
            )
        )
        creator = CircuitFromOperationCreator(operation=operation)

        from stim_experiments.utilities import universal_hadamard_type_factory
        with patch(f'{universal_hadamard_type_factory.__name__}.UniversalHadamardTypeFactory.get_universal_hadamard_type', return_value=UniversalHadamardStub):
            _ = creator.create_circuit()
            assert UniversalHadamardStub.universal_used

    def test_native_hadamard_used_when_encoding_does_implement_hadamard(self):
        encoding = ErrorCorrectingCodeStubWithHadamard()
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.H,
                    qubit_index=0,
                ),
                encoding=encoding,
            )
        )
        creator = CircuitFromOperationCreator(operation=operation)

        from stim_experiments.utilities import universal_hadamard_type_factory
        with patch(f'{universal_hadamard_type_factory.__name__}.UniversalHadamardTypeFactory.get_universal_hadamard_type', return_value=UniversalHadamardStub):
            _ = creator.create_circuit()
            assert not UniversalHadamardStub.universal_used
