from cirq import kron

from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.stabilizer_transformer import \
    TransformationGate, TransformationOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult
from stim_experiments.simulators.simulator_using_circuits.simulator_using_circuits import SimulatorUsingCircuits
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_PLUS_STATE_VECTOR, \
    KET_ZERO_STATE_VECTOR
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_4_qubit, \
    get_check_matrix_values_5_qubit


class TestSimulatorCircuit:
    def test_trivial(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=[])
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[],
            measurements={},
        )

    def test_logical_x(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_STATE_VECTOR)],
            measurements={},
        )

    def test_logical_z(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_STATE_VECTOR)
        operations = [TransformationOperation(gate=TransformationGate.Z, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=-KET_ONE_STATE_VECTOR)],
            measurements={},
        )

    def test_logical_h(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        operations = [TransformationOperation(gate=TransformationGate.H, target_qubit_index=0)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                             initial_logical_qubit_state=kron(KET_PLUS_STATE_VECTOR,
                                                                              KET_ZERO_STATE_VECTOR).flatten())
                       ],
            measurements={},
        )

    def test_multiple_encodings(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ZERO_STATE_VECTOR),
                       GenericStabilizerCode(generators=get_check_matrix_values_5_qubit(), initial_logical_qubit_state=KET_ONE_STATE_VECTOR)],
            measurements={},
        )

    def test_multiple_logical_qubits_single_encoding(self):
        code = GenericStabilizerCode(generators=get_check_matrix_values_4_qubit())
        operations = [TransformationOperation(gate=TransformationGate.X, target_qubit_index=1)]
        simulator = SimulatorUsingCircuits(error_correcting_code=code, operations=operations)
        result = simulator.simulate()
        assert result == SimulatorResult(
            encodings=[GenericStabilizerCode(generators=get_check_matrix_values_4_qubit(),
                                             initial_logical_qubit_state=kron(KET_ZERO_STATE_VECTOR,
                                                                              KET_ONE_STATE_VECTOR).flatten()),
                       ],
            measurements={},
        )
