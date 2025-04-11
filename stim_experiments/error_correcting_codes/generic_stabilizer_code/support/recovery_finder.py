from collections import defaultdict
from functools import cached_property
from typing import Dict, List

from cirq import Gate, X, Z

from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import Recovery
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToGates
from stim_experiments.utilities import binary_array_to_int


class RecoveryFinder:
    def __init__(self, check_matrix: CheckMatrix):
        self._check_matrix = check_matrix

    def find_recoveries(self) -> Dict[int, List[Recovery]]:
        recoveries = self._find_recoveries()
        recoveries_dict = defaultdict(list)
        for recovery in recoveries:
            symptom_int = binary_array_to_int(binary_array=recovery.symptom)
            if symptom_int:
                recoveries_dict[symptom_int].append(recovery)
        return recoveries_dict

    def _find_recoveries(self) -> List[Recovery]:
        possible_errors = [X, Z]
        return [Recovery(gate=possible_errors[column_index < self._check_matrix.num_physical_qubits],
                         qubit_index=column_index % self._check_matrix.num_physical_qubits,
                         symptom=syndrome.tolist())
                for column_index, syndrome in enumerate(self._check_matrix.matrix.transpose())]

    # def _find_recoveries(self) -> List[Recovery]:
    #     return [self._get_recovery_for_error(error=possible_error, qubit_index=qubit_index)
    #             for qubit_index in range(self._check_matrix.num_physical_qubits)
    #             for possible_error in (X, Z)]
    #
    # def _get_recovery_for_error(self, error: Gate, qubit_index: int) -> Recovery:
    #     return Recovery(
    #         gate=error,
    #         qubit_index=qubit_index,
    #         symptom=[int(bool(stabilizers_on_qubits[qubit_index]) and [error] != stabilizers_on_qubits[qubit_index])
    #                  for stabilizers_on_qubits in self._stabilizer_gates],
    #     )
    #
    # @cached_property
    # def _stabilizer_gates(self) -> List[List[List[Gate]]]:
    #     return CheckMatrixToGates(self._check_matrix).get_gates()
