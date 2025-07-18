from cmath import exp, sqrt

import pytest
from cirq import Circuit, LineQubit, rz

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex, SimulationOperation, \
    TargetEncoding
from simulations.error_correcting_simulator import \
    get_error_correcting_simulator
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulators.simulator_using_circuits.support.circuit_from_operation_creator import \
    CircuitFromOperationCreator
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, KET_ZERO_STATE_VECTOR, \
    states_are_equal, tensor
from tests.simulators.logical_operations_circuit_generator.support.circuit_from_operation_creator.error_correcting_code_stub_with_x_and_z import \
    ErrorCorrectingCodeStubWithXAndZ
from tests.utilities import set_configuration_to_reduce_ancilla_qubits


class TestControlledOperation:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_configuration_to_reduce_ancilla_qubits()

    def test_default_universal_controlled_operation_used_when_explicitly_set(self):
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        encodings = [ErrorCorrectingCodeStubWithXAndZ(qubits=qubits[:1]), ErrorCorrectingCodeStubWithXAndZ(qubits=qubits[1:])]
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.X,
                    qubit_index=0,
                ),
                encoding=encodings[1],
            ),
            control_encoding=LogicalEncodingIndex(
                encoding=encodings[0],
                qubit_index_relative=0,
                qubit_index_logical=0
            )
        )

        initial_state = tensor(KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR)
        utilities = get_error_correcting_simulator(state=initial_state)
        circuit = CircuitFromOperationCreator(operation=operation).create_circuit()
        simulated_state = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=len(qubits),
            initial_data_state=initial_state,
        ).state
        expected_state = tensor(KET_ONE_STATE_VECTOR, KET_ONE_STATE_VECTOR)
        assert states_are_equal(simulated_state, expected_state)

    def test_provided_controlled_operation_used_when_provided(self):
        ConfigurationErrorCorrectingCodeManager.get_configuration().universal_controlled_operation_type = UniversalControlledOperationCustom

        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        encodings = [ErrorCorrectingCodeStubWithXAndZ(qubits=qubits[:1]), ErrorCorrectingCodeStubWithXAndZ(qubits=qubits[1:])]
        operation = SimulationOperation(
            target_encoding=TargetEncoding(
                operation=LogicalOperation(
                    gate=LogicalGateLabel.X,
                    qubit_index=0,
                ),
                encoding=encodings[1],
            ),
            control_encoding=LogicalEncodingIndex(
                encoding=encodings[0],
                qubit_index_relative=0,
                qubit_index_logical=0
            )
        )

        initial_state = tensor(KET_PLUS_STATE_VECTOR, KET_PLUS_STATE_VECTOR)
        utilities = get_error_correcting_simulator(state=initial_state)
        circuit = CircuitFromOperationCreator(operation=operation).create_circuit()
        simulated_state = utilities.get_state_after_circuit(
            circuit=circuit,
            num_data_qubits=len(qubits),
            initial_data_state=tensor(KET_PLUS_STATE_VECTOR, KET_PLUS_STATE_VECTOR),
        ).state
        expected_state = tensor((1 / sqrt(2)) * (KET_ZERO_STATE_VECTOR + exp(
            1j * UniversalControlledOperationCustom.radian_ids[0]) * KET_ONE_STATE_VECTOR),
                                (1 / sqrt(2)) * (KET_ZERO_STATE_VECTOR + exp(
                                    1j * UniversalControlledOperationCustom.radian_ids[1]) * KET_ONE_STATE_VECTOR))
        assert states_are_equal(simulated_state, expected_state)


class UniversalControlledOperationCustom(UniversalControlledOperation):
    radian_ids = [0.1, 0.2]

    def get_controlled_operation_circuit(self) -> Circuit:
        return Circuit(
            rz(rads=self.radian_ids[0])(self._control.encoding.data_qubits[0]),
            rz(rads=self.radian_ids[1])(self._target.encoding.data_qubits[0]),
        )
