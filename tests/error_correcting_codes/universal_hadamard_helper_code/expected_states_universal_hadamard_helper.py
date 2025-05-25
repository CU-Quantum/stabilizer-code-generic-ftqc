from typing import Optional

from stim_experiments.utilities.utilities import KET_ONE_STATE_VECTOR, KET_ZERO_STATE_VECTOR, TYPE_STATE_VECTOR, tensor
from tests.error_correcting_codes.expected_states.expected_states import ExpectedStates


class ExpectedStatesUniversalHadamardHelper(ExpectedStates):
    num_qubits = 4

    def __init__(self, num_qubits: Optional[int] = None):
        if num_qubits:
            self.num_qubits = num_qubits

    def get_logical_zero_state_vector(self) -> TYPE_STATE_VECTOR:
        return .5 * (
            tensor(*[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits)
            + tensor(*[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits)
            + tensor(*[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits)
            + tensor(*[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits)
        )

    def get_logical_one_state_vector(self) -> TYPE_STATE_VECTOR:
        return .5 * (
                tensor(*[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits)
                + tensor(*[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits)
                - tensor(*[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits)
                - tensor(*[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ONE_STATE_VECTOR] * self.num_qubits, *[KET_ZERO_STATE_VECTOR] * self.num_qubits)
        )
