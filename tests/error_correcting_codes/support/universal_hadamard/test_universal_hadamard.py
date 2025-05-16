from uuid import uuid4

import numpy as np
from cirq import Circuit, CircuitOperation, KeyCondition, LineQubit, MeasurementKey, R, SWAP, Z
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_code_to_computational_logical import \
    UniversalHadamardCodeToComputationalLogical
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.universal_hadamard_code.universal_hadamard_code import \
    UniversalHadamardCode
from stim_experiments.singletons.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.singletons.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR
from tests.error_correcting_codes.support.universal_hadamard.single_qubit_code import SingleQubitCode
from tests.utilities import states_are_equal


class UniversalHadamard:
    def __init__(self, code: ErrorCorrectingCode = None):
        self._code = code

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        self._measurer_type = configuration.measurer_type

    def get_hadamard_circuit(self) -> Circuit:
        measurement_key = MeasurementKey(f'UNIVERSAL_HADAMARD_MEASUREMENT_{uuid4().hex}')
        num_qubits_in_desired_encoding = len(self._code.data_qubits)
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=3 * num_qubits_in_desired_encoding) as ancilla_qubits:
            three_cat = ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_desired_encoding, qubits=ancilla_qubits)
            uni_h = UniversalHadamardCode(num_qubits_in_cat_state=num_qubits_in_desired_encoding, qubits=ancilla_qubits)
            new_encoding = self._code.create_new(qubits=uni_h.subregisters[0])
            to_computational_logical = UniversalHadamardCodeToComputationalLogical(universal_hadamard_code=uni_h, desired_encoding=self._code)
            logical_x, logical_z = (list(self._code.get_operation_circuit(operation=LogicalOperation(gate=gate, qubit_index=0)).all_operations())  # allow multi qubit encodings
                                    for gate in (LogicalGateLabel.X, LogicalGateLabel.Z))
            return Circuit(
                three_cat.encode_logical_qubit(),
                [
                    ControlledSingleQubitGatesApplier(operations=logical_x, controls=subregister[:len(logical_x)]).get_circuit()
                    for subregister in three_cat.subregisters
                ],
                to_computational_logical.get_circuit(),
                self._measurer_type(operations=logical_z, measurement_key=measurement_key).get_measurement_circuit(),
                CircuitOperation(
                    new_encoding.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)).freeze()
                ).with_classical_controls(KeyCondition(key=measurement_key)),
                [
                    SWAP(new_encoding.data_qubits[i], self._code.data_qubits[i])
                    for i in range(len(new_encoding.data_qubits))
                ],
                [R(ancilla) for ancilla in ancilla_qubits]
            )


class TestUniversalHadamard:
    def test_random_alpha_beta(self):
        np.random.seed(0)
        initial_state = self._random_complex_unit_vector()
        utilities = get_error_correcting_code_utilities(state=initial_state)
        qubits = LineQubit.range(1)
        code = SingleQubitCode(qubits=qubits)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(code.data_qubits))

        simulated_state = utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                UniversalHadamard(code=code).get_hadamard_circuit(),
            ),
            num_data_qubits=1,
            initial_data_state=initial_state,
        ).state
        expected_state = (1 / np.sqrt(2)) * array([initial_state[0] + initial_state[1], initial_state[0] - initial_state[1]])
        assert states_are_equal(simulated_state, expected_state)

    def _random_complex_unit_vector(self) -> np.ndarray:
        dimension = 2
        random_complex_vector = np.random.randn(dimension) + 1j * np.random.randn(dimension)
        unit_complex_vector = random_complex_vector / np.linalg.norm(random_complex_vector)
        return unit_complex_vector

