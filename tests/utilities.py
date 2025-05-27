import random
from dataclasses import dataclass

import numpy as np
from cirq import Circuit
from numpy import array, sqrt
from numpy._typing import NDArray

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.error_correcting_code_utilities import get_error_correcting_code_utilities
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_cx_from_first_qubit import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.measurer.measurer_with_single_qubit import MeasurerWithSingleQubit
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation_single_ancilla import \
    UniversalControlledOperationSingleAncilla
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard_single_ancilla import \
    UniversalHadamardSingleAncilla
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_singe_ancilla import \
    UniversalTSingleAncilla
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, \
    int_to_binary_array, tensor


def set_seed(seed: int):
    configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
    configuration.seed = seed
    random.seed(seed)
    np.random.seed(seed)


def get_cat_state_vector(num_qubits: int) -> TYPE_STATE_VECTOR:
    return (1 / sqrt(2)) * (tensor(*[KET_ZERO_STATE_VECTOR] * num_qubits) + tensor(*[KET_ONE_STATE_VECTOR] * num_qubits))


def set_configuration_to_reduce_ancilla_qubits() -> None:
    configuration = ConfigurationErrorCorrectingCodeManager.get_configuration()
    configuration.cat_state_creator_type = CatStateCreatorCxFromFirstQubit
    configuration.measurer_type = MeasurerWithSingleQubit
    configuration.universal_hadamard_type = UniversalHadamardSingleAncilla
    configuration.universal_controlled_operation_type = UniversalControlledOperationSingleAncilla
    configuration.universal_t_type = UniversalTSingleAncilla


def random_complex_unit_vector(num_qubits: int) -> np.ndarray:
    dimension = 2 ** num_qubits
    random_complex_vector = np.random.randn(dimension) + 1j * np.random.randn(dimension)
    unit_complex_vector = random_complex_vector / np.linalg.norm(random_complex_vector)
    return unit_complex_vector


@dataclass
class RandomEncodedInitialState:
    initial_state: TYPE_STATE_VECTOR
    initial_coefficients: TYPE_STATE_VECTOR
    computational_basis_states: NDArray[TYPE_STATE_VECTOR]


def get_random_encoded_initial_state(code: ErrorCorrectingCode) -> RandomEncodedInitialState:
    initial_coefficients = random_complex_unit_vector(num_qubits=code.num_logical_qubits)
    utilities = get_error_correcting_code_utilities(state=initial_coefficients)
    computational_basis_states = [int_to_binary_array(i, code.num_logical_qubits)
                                  for i in range(2 ** code.num_logical_qubits)]
    computational_basis_states_encoded = array([
        utilities.get_state_after_circuit(
            circuit=Circuit(
                code.encode_logical_qubit(),
                [code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.X, qubit_index=qubit_index))
                 for qubit_index, is_flipped in enumerate(basis_state)
                 if is_flipped],
            ),
            num_data_qubits=len(code.data_qubits),
        ).state
        for basis_state in computational_basis_states
    ])
    initial_state = sum(
        coefficient * computational_basis_state
        for coefficient, computational_basis_state in zip(initial_coefficients, computational_basis_states_encoded)
    )
    return RandomEncodedInitialState(
        initial_state=initial_state,
        initial_coefficients=initial_coefficients,
        computational_basis_states=computational_basis_states_encoded,
    )
