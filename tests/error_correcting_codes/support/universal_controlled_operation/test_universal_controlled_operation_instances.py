import random

import numpy as np
import pytest
from cirq import Circuit, LineQubit

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex, TargetEncoding
from stim_experiments.custom_enums.universal_hadamard_type import UniversalHadamardType
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation_fault_tolerant import \
    UniversalControlledOperationFaultTolerant
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation_single_ancilla import \
    UniversalControlledOperationSingleAncilla
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import states_are_equal, tensor
from tests.utilities import get_random_encoded_initial_state


class TestUniversalControlledOperationInstances:
    @pytest.fixture(autouse=True, params=range(3))
    def _seed(self, request):
        seed = request.param
        random.seed(seed)
        np.random.seed(seed)

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        configuration.seed = seed
        configuration.universal_hadamard_type = UniversalHadamardType.SINGLE_ANCILLA

    @pytest.mark.parametrize('universal_controlled_operation_type', [
        pytest.param(UniversalControlledOperationSingleAncilla, id='UniversalControlledOperationSingleAncilla'),
        pytest.param(UniversalControlledOperationFaultTolerant, id='UniversalControlledOperationFaultTolerant'),
    ])
    def test_cx_single_qubit_encoding(self, universal_controlled_operation_type: type[UniversalControlledOperation]):
        qubits = LineQubit.range(2)
        code_control, code_target = codes = [RepetitionCode(num_qubits=1, qubits=code_qubits)
                                             for code_qubits in (qubits[:1], qubits[1:])]
        encoding_control = LogicalEncodingIndex(encoding=code_control, qubit_index_relative=0)
        encoding_target = TargetEncoding(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0),
                                         encoding=code_target)
        universal_controlled_operation = universal_controlled_operation_type(control=encoding_control, target=encoding_target)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))

        encoded_initial_states_control, encoded_initial_states_target = encoded_initial_states = [get_random_encoded_initial_state(code=code_control)
                                                                                                  for _ in range(len(codes))]
        initial_state = tensor(*[encoded_initial_state.initial_state for encoded_initial_state in encoded_initial_states])
        utilities = get_error_correcting_code_utilities(state=encoded_initial_states_control.initial_state)

        simulated_state = utilities.get_state_after_circuit(
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

    # TODO Nick test multiqubit encodings
    # TODO Nick test CX between qubits in same multiqubit encoding
