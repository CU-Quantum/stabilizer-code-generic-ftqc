from cmath import exp, sqrt

from cirq import Circuit, rz
from numpy import array

from stim_experiments.algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.custom_dataclasses.correction_circuit import CorrectionCircuit
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import SimulationOperation, TargetEncoding
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    states_are_equal
from tests.algorithms.support.logical_operations_circuit_creator.support.circuit_from_operation_creator.error_correcting_code_stub_with_x_and_z import \
    ErrorCorrectingCodeStubWithXAndZ
from tests.error_correcting_codes.support.universal_operations.universal_t.test_universal_t_instances import T_ROTATION
from tests.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits


class TestTDefault:
    def test_universal_t_used_when_encoding_does_not_implement_t(self):
        set_configuration_to_reduce_ancilla_qubits()

        encoding = ErrorCorrectingCodeStubNoT()
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(encoding.data_qubits))
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.T,
                    qubit_index=0,
                ),
                encoding=encoding,
            )
        )

        utilities = get_error_correcting_simulator(state=KET_ZERO_STATE_VECTOR)
        circuit = CircuitFromOperationCreator(operation=operation).create_circuit()
        simulated_state = utilities.run_simulation(
            circuit=circuit,
            num_data_qubits=len(encoding.data_qubits),
            initial_data_state=KET_PLUS_STATE_VECTOR,
        ).state
        assert states_are_equal(simulated_state, KET_ZERO_STATE_VECTOR + T_ROTATION * KET_ONE_STATE_VECTOR)

    def test_native_t_used_when_encoding_does_implement_t(self):
        encoding = ErrorCorrectingCodeStubWithBadT()
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(encoding.data_qubits))
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.T,
                    qubit_index=0,
                ),
                encoding=encoding,
            )
        )

        initial_state = KET_PLUS_STATE_VECTOR
        utilities = get_error_correcting_simulator(state=initial_state)
        circuit = CircuitFromOperationCreator(operation=operation).create_circuit()
        simulated_state = utilities.run_simulation(
            circuit=circuit,
            num_data_qubits=len(encoding.data_qubits),
            initial_data_state=initial_state,
        ).state
        expected_state = (1 / sqrt(2)) * array([1, exp(1j * ErrorCorrectingCodeStubWithBadT.t_radians)])
        assert states_are_equal(simulated_state, expected_state)


class ErrorCorrectingCodeStubNoT(ErrorCorrectingCodeStubWithXAndZ):
    pass


class ErrorCorrectingCodeStubWithBadT(ErrorCorrectingCodeStubNoT):
    t_radians = .3

    def encode_logical_qubit(self):
        pass

    def get_error_correction_circuit(self) -> CorrectionCircuit:
        pass

    def _perform_get_operation_circuit(self, operation: LogicalOperation):
        result = super()._perform_get_operation_circuit(operation)
        if result is not None:
            return result
        elif operation.gate == LogicalGateLabel.T:
            return Circuit(rz(rads=self.t_radians)(self.data_qubits[operation.qubit_index]))
        return None
