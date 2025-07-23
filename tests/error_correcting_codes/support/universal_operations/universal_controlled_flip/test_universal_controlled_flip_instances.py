import pytest
from cirq import Circuit, LineQubit

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex, TargetEncoding
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCodeOneLogical
from stim_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip_fault_tolerant import \
    UniversalControlledFlipFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip_single_ancilla import \
    UniversalControlledOperationSingleAncilla
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import get_error_correcting_simulator
from stim_experiments.utilities.predefined_check_matrix_values import get_check_matrix_values_4_qubit
from stim_experiments.utilities.utilities import states_are_equal, tensor
from tests.utilities_for_tests import get_random_encoded_initial_state, set_configuration_to_reduce_ancilla_qubits, set_seed


class TestUniversalControlledOperationInstances:
    @pytest.fixture(autouse=True, params=range(3))
    def _seed(self, request):
        set_seed(seed=request.param)
        set_configuration_to_reduce_ancilla_qubits()

    @pytest.mark.parametrize('universal_controlled_operation_type', [
        pytest.param(UniversalControlledFlipFaultTolerant, id='UniversalControlledOperationFaultTolerant'),
        pytest.param(UniversalControlledOperationSingleAncilla, id='UniversalControlledOperationSingleAncilla'),
    ])
    def test_cx_single_qubit_encoding(self, universal_controlled_operation_type: type[UniversalControlledOperation]):
        qubits = LineQubit.range(2)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        code_control, code_target = codes = [RepetitionCodeOneLogical(num_qubits=1, qubits=code_qubits)
                                             for code_qubits in (qubits[:1], qubits[1:])]
        encoding_control = LogicalEncodingIndex(encoding=code_control, qubit_index_relative=0)
        encoding_target = TargetEncoding(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0),
                                         encoding=code_target)
        universal_controlled_operation = universal_controlled_operation_type(control=encoding_control, target=encoding_target)

        encoded_initial_states_control, encoded_initial_states_target = encoded_initial_states = [get_random_encoded_initial_state(code=code_control)
                                                                                                  for _ in range(len(codes))]
        initial_state = tensor(*[encoded_initial_state.initial_state for encoded_initial_state in encoded_initial_states])
        utilities = get_error_correcting_simulator(state=encoded_initial_states_control.initial_state)

        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                [code.encode_logical_qubit() for code in codes],
                universal_controlled_operation.get_controlled_operation_circuit(),
            ),
            num_data_qubits=len(qubits),
            initial_data_state=initial_state,
        ).state
        notted_target = sum(encoded_initial_states_target.initial_coefficients[i] * encoded_initial_states_target.computational_basis_states[1 - i]
                            for i in range(2))
        expected_state = (
            encoded_initial_states_control.initial_coefficients[0]
                * tensor(encoded_initial_states_control.computational_basis_states[0],
                         encoded_initial_states_target.initial_state)
            +
            encoded_initial_states_control.initial_coefficients[1]
                * tensor(encoded_initial_states_control.computational_basis_states[1],
                         notted_target)
        )
        assert states_are_equal(simulated_state, expected_state)

    @pytest.mark.parametrize('universal_controlled_operation_type', [
        pytest.param(UniversalControlledFlipFaultTolerant, id='UniversalControlledOperationFaultTolerant'),
        pytest.param(UniversalControlledOperationSingleAncilla, id='UniversalControlledOperationSingleAncilla'),
    ])
    def test_cx_multi_qubit_encoding(self, universal_controlled_operation_type: type[UniversalControlledOperation]):
        qubits = LineQubit.range(8)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        code_control, code_target = codes = [
            StabilizerStandardizedCode(
                generators=get_check_matrix_values_4_qubit(),
                qubits=code_qubits,
            )
            for code_qubits in (qubits[:4], qubits[4:])
        ]
        encoding_control = LogicalEncodingIndex(encoding=code_control, qubit_index_relative=1)
        encoding_target = TargetEncoding(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=1),
                                         encoding=code_target)
        universal_controlled_operation = universal_controlled_operation_type(control=encoding_control, target=encoding_target)

        encoded_initial_states_control, encoded_initial_states_target = encoded_initial_states = [get_random_encoded_initial_state(code=code_control)
                                                                                                  for _ in range(len(codes))]
        initial_state = tensor(*[encoded_initial_state.initial_state for encoded_initial_state in encoded_initial_states])
        utilities = get_error_correcting_simulator(state=encoded_initial_states_control.initial_state)

        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                [code.encode_logical_qubit() for code in codes],
                universal_controlled_operation.get_controlled_operation_circuit(),
            ),
            num_data_qubits=len(qubits),
            initial_data_state=initial_state,
        ).state
        target_permutation = [1, 0, 3, 2]
        notted_target = sum(encoded_initial_states_target.initial_coefficients[i] * encoded_initial_states_target.computational_basis_states[permutation]
                            for i, permutation in enumerate(target_permutation))
        expected_state = (
            encoded_initial_states_control.initial_coefficients[0]
                * tensor(encoded_initial_states_control.computational_basis_states[0],
                         encoded_initial_states_target.initial_state)
            +
            encoded_initial_states_control.initial_coefficients[1]
                * tensor(encoded_initial_states_control.computational_basis_states[1],
                         notted_target)
            +
            encoded_initial_states_control.initial_coefficients[2]
                * tensor(encoded_initial_states_control.computational_basis_states[2],
                         encoded_initial_states_target.initial_state)
            +
            encoded_initial_states_control.initial_coefficients[3]
                * tensor(encoded_initial_states_control.computational_basis_states[3],
                         notted_target)
        )
        assert states_are_equal(simulated_state, expected_state)

    @pytest.mark.parametrize('universal_controlled_operation_type', [
        pytest.param(UniversalControlledFlipFaultTolerant, id='UniversalControlledOperationFaultTolerant'),
        pytest.param(UniversalControlledOperationSingleAncilla, id='UniversalControlledOperationSingleAncilla'),
    ])
    def test_same_multi_qubit_encoding(self, universal_controlled_operation_type: type[UniversalControlledOperation]):
        qubits = LineQubit.range(4)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        code = StabilizerStandardizedCode(
            generators=get_check_matrix_values_4_qubit(),
            qubits=qubits,
        )
        encoding_control = LogicalEncodingIndex(encoding=code, qubit_index_relative=0)
        encoding_target = TargetEncoding(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=1),
                                         encoding=code)
        universal_controlled_operation = universal_controlled_operation_type(control=encoding_control, target=encoding_target)

        encoded_initial_states = get_random_encoded_initial_state(code=code)
        utilities = get_error_correcting_simulator(state=encoded_initial_states.initial_state)

        simulated_state = utilities.run_simulation(
            circuit=Circuit(
                code.encode_logical_qubit(),
                universal_controlled_operation.get_controlled_operation_circuit(),
            ),
            num_data_qubits=len(qubits),
            initial_data_state=encoded_initial_states.initial_state,
        ).state
        expected_state = (
                encoded_initial_states.initial_coefficients[0] * encoded_initial_states.computational_basis_states[0]
                +
                encoded_initial_states.initial_coefficients[1] * encoded_initial_states.computational_basis_states[1]
                +
                encoded_initial_states.initial_coefficients[2] * encoded_initial_states.computational_basis_states[3]
                +
                encoded_initial_states.initial_coefficients[3] * encoded_initial_states.computational_basis_states[2]
        )
        assert states_are_equal(simulated_state, expected_state)
