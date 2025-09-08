from collections import defaultdict
from typing import Optional

from cirq import Circuit, LineQubit, Operation, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.correction_circuit import CorrectionCircuit
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.custom_dataclasses.recovery import RecoveryOperation
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from stim_experiments.error_correcting_codes.support.check_matrix_to_operations import CheckMatrixToOperations
from stim_experiments.error_correcting_codes.support.error_recovery.error_recovery_by_stabilizers import \
    ErrorRecoveryByStabilizers
from stim_experiments.error_correcting_codes.support.multiple_cat_code_generators import \
    MultipleCatCodeGenerators
from stim_experiments.error_correcting_codes.support.operations_to_check_matrix import OperationsToCheckMatrix
from stim_experiments.error_correcting_codes.support.recovery_combinations_finder import RecoveryCombinationsFinder
from stim_experiments.error_correcting_codes.support.recovery_finder import RecoveryFinder


class CatParityCode(StabilizerCode):
    def __init__(self, num_cats: int, num_qubits_per_cat: int, qubits: Optional[list[LineQubit]] = None):
        self._num_cats = num_cats
        self._num_qubits_per_cat = max(3, num_qubits_per_cat)

        generator = MultipleCatCodeGenerators(num_qubits_per_cat=self._num_qubits_per_cat,
                                              num_cats=self._num_cats)
        z_stabilizers = generator.get_z_generators()
        x_stabilizers = generator.get_x_generators()

        self.check_matrix = CheckMatrix(matrix=array(z_stabilizers + x_stabilizers))
        super().__init__(check_matrix=self.check_matrix,
                         recovery_combinations_finder=RecoveryCombinationsFinder(max_num_errors=min((self._num_qubits_per_cat - 1) // 2, (self._num_cats - 1) // 2)),
                         qubits=qubits)

    def _get_anticommuter_for_generator(self, generator_index: int) -> list[Operation]:
        x_stabilizer_start_index = self._num_generators - self._num_x_stabilizers
        is_z_stabilizer = generator_index < x_stabilizer_start_index
        if is_z_stabilizer:
            num_checks_per_register = self._num_qubits_per_cat - 1
            subregister_index = generator_index // num_checks_per_register
            start_index = subregister_index * self._num_qubits_per_cat
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == self._num_generators - 1
            if is_last_generator:
                return [Z(self.data_qubits[-1])]
            subregister_index = generator_index - x_stabilizer_start_index
            return [Z(self.data_qubits[i * self._num_qubits_per_cat]) for i in range(subregister_index + 1)]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_per_cat)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_per_cat]) for i in range(self._num_cats)],
            )
        return None

    def get_modified_stabilizers_error_correction_circuit(self,
                                                          subregister_index: int,
                                                          target_operations: list[Operation],
                                                          target_code: StabilizerCode) -> CorrectionCircuit:
        target_stabilizers = CheckMatrixToOperations(check_matrix=target_code.check_matrix, qubits=target_code.data_qubits).get_operations() \
            if target_code.check_matrix is not None else []
        control_stabilizers = CheckMatrixToOperations(check_matrix=self.check_matrix, qubits=self.data_qubits).get_operations()
        if subregister_index < len(self.subregisters) - 1:
            control_stabilizers[-self._num_x_stabilizers + subregister_index] += target_operations
        all_stabilizers = control_stabilizers + target_stabilizers

        # TODO can probably cut down on redundant recovery operations somehow
        all_qubits = self.data_qubits + target_code.data_qubits
        combined_check_matrix = OperationsToCheckMatrix(operations_list=all_stabilizers).get_check_matrix()
        recoveries = RecoveryFinder(check_matrix=combined_check_matrix).find_recovery_operations(qubits=all_qubits)
        blocks = [self, target_code]
        recoveries_per_block = [
            [recovery for recovery in recoveries if recovery.operation.qubits[0] in block.data_qubits]
            for block in blocks
        ]
        recovery_combos_per_block = [
            block.recovery_combinations_finder.find_recovery_operations(recoveries)
            for block, recoveries in zip(blocks, recoveries_per_block)
        ]
        recovery_combos_per_block_by_symptom = [defaultdict(list) for _ in range(len(recovery_combos_per_block))]
        for i, recovery_combos in enumerate(recovery_combos_per_block):
            for recovery in recovery_combos:
                recovery_combos_per_block_by_symptom[i][tuple(recovery.symptom)].append(recovery)
        recovery_combos_per_block_control = recovery_combos_per_block[0]
        recovery_combos_per_block_by_symptom_control = recovery_combos_per_block_by_symptom[0]
        recovery_combos_per_block_by_symptom_target = recovery_combos_per_block_by_symptom[1]
        for symptom_helper, recoveries_helper in recovery_combos_per_block_by_symptom_control.items():
            for symptom_target, recoveries_target in recovery_combos_per_block_by_symptom_target.items():
                symptom_combined = array(list(symptom_target)) ^ array(list(symptom_helper))
                for recovery_helper in recoveries_helper:
                    recovery_combos_per_block_control.append(RecoveryOperation(
                        operation=recovery_helper.operation, # only do helper because target is corrected independently by ActiveEncodingsStore
                        symptom=symptom_combined.tolist(),
                    ))

        return ErrorRecoveryByStabilizers(
            stabilizers=all_stabilizers,
            recoveries=recovery_combos_per_block_control,
        ).get_error_correction_circuit()

    # def get_z_stabilizers_error_correction_circuit(self) -> CorrectionCircuit:
    #     z_stabilizers_symplectic = CheckMatrix(matrix=self.check_matrix.matrix[:-self._num_x_stabilizers])
    #     stabilizers = CheckMatrixToOperations(check_matrix=z_stabilizers_symplectic, qubits=self.data_qubits).get_operations()
    #     recoveries = RecoveryFinder(check_matrix=z_stabilizers_symplectic).find_recovery_operations(qubits=self.data_qubits)
    #     return ErrorRecoveryByStabilizers(
    #         stabilizers=stabilizers,
    #         recoveries=recoveries,
    #     ).get_error_correction_circuit()

    @property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_per_cat:(i + 1) * self._num_qubits_per_cat]
                for i in range(self._num_cats)]

    @property
    def _num_generators(self) -> int:
        return len(self.check_matrix.matrix)

    @property
    def _num_x_stabilizers(self) -> int:
        return self._num_cats - 1
