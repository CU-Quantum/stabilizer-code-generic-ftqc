from functools import cached_property
from typing import Optional
from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, KeyCondition, MeasurementKey, Operation, R, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import RecoveryOperations
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.five_qubit_code.five_qubit_code import FiveQubitCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.generic_stabilizer_code import \
    GenericStabilizerCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToGates, CheckMatrixToOperations
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.fault_tolerant_error_correction.fault_tolerant_error_correction import \
    FaultTolerantErrorCorrection
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.cat_state_creator import \
    CatStateCreatorCxFromFirstQubit
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.support.conditions.verification_is_zero import \
    VerificationIsZero
from stim_experiments.error_correcting_codes.support.fault_tolerant_state_encoder.fault_tolerant_state_encoder import \
    FaultTolerantStateEncoder
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities import FreshAncillasPool
from tests.error_correcting_codes.generic_stabilizer_code.utilities import get_check_matrix_values_5_qubit


class UniversalHadamardCode(ErrorCorrectingCode):
    num_cats = ThreeCatCode.num_cats

    def __init__(self, num_qubits_in_cat_state: int, qubit_start_index: int = 0):
        self._num_qubits_in_cat_state = num_qubits_in_cat_state
        num_data_qubits = num_qubits_in_cat_state * self.num_cats
        num_parity_checks_per_register = num_qubits_in_cat_state - 1
        x_stabilizers = [
            [0] * num_data_qubits + [self._qubit_has_x_stabilizer_in_generator(cat_index=cat_index,
                                                                               parity_check_index=parity_check_index,
                                                                               qubit_index=qubit_index)
                                     for qubit_index in range(num_data_qubits)]
            for cat_index in range(self.num_cats)
            for parity_check_index in range(num_parity_checks_per_register)
        ]
        z_stabilizers = [
            [int(cat_index * self._num_qubits_in_cat_state <= qubit_index < (cat_index + 2) * self._num_qubits_in_cat_state)
             for qubit_index in range(num_data_qubits)] + [0] * num_data_qubits
            for cat_index in range(self.num_cats - 1)
        ]
        self._check_matrix = CheckMatrix(matrix=array(x_stabilizers + z_stabilizers))
        super().__init__(num_data_qubits=self._num_qubits_in_cat_state * self.num_cats,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index)

    def _qubit_has_x_stabilizer_in_generator(self, cat_index: int, parity_check_index: int, qubit_index: int) -> int:
        low_index = cat_index * self._num_qubits_in_cat_state + parity_check_index
        high_index = low_index + 1
        return int(low_index <= qubit_index <= high_index)

    def encode_logical_qubit(self) -> Circuit:
        phase_corrections = [self._get_phase_correction(generator_index=generator_index)
                             for generator_index in range(len(self._generator_operations))]
        return FaultTolerantStateEncoder(generators=self._generator_operations,
                                         phase_corrections=phase_corrections).encode_state()

    def _get_phase_correction(self, generator_index: int) -> list[Operation]:
        is_x_stabilizer = generator_index < len(self._generator_operations) - 2
        if is_x_stabilizer:
            num_checks_per_register = self._num_qubits_in_cat_state - 1
            register_index = generator_index // num_checks_per_register
            start_index = register_index * self._num_qubits_in_cat_state
            relative_generator_index = generator_index % num_checks_per_register
            return [X(self.data_qubits[qubit_index]) for qubit_index in range(start_index, start_index + relative_generator_index + 1)]
        else:
            is_last_generator = generator_index == len(self._generator_operations) - 1
            return [Z(self.data_qubits[0 - is_last_generator])]

    def get_error_correction_circuit(self) -> Circuit:
        return FaultTolerantErrorCorrection(generator_operations=self._generator_operations,
                                            recoveries=RecoveryFinder(check_matrix=self._check_matrix).find_recoveries(),
                                            qubits=self.data_qubits).get_error_correction_circuit()

    @cached_property
    def _generator_operations(self) -> list[list[Operation]]:
        return CheckMatrixToOperations(check_matrix=self._check_matrix, qubits=self.data_qubits).get_operations()

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> Optional[Circuit]:
        if operation.gate == LogicalGateLabel.X:
            return Circuit(
                [X(self.data_qubits[i]) for i in range(self._num_qubits_in_cat_state)]
            )
        elif operation.gate == LogicalGateLabel.Z:
            return Circuit(
                [Z(self.data_qubits[i * self._num_qubits_in_cat_state]) for i in range(self.num_cats)],
            )
        elif operation.gate == LogicalGateLabel.H:
            generic_five_qubit = GenericStabilizerCode(generators=get_check_matrix_values_5_qubit())
            num_qubits_needed_per_register = len(generic_five_qubit.data_qubits)
            extra_qubits_per_register = max(0, num_qubits_needed_per_register - self._num_qubits_in_cat_state)
            with FreshAncillasPool().use_fresh_ancillas(num_ancillas=extra_qubits_per_register * self.num_cats) as ancilla_qubits:
                extra_qubits_per_register = [ancilla_qubits[i * extra_qubits_per_register:(i + 1) * extra_qubits_per_register]
                                             for i in range(self.num_cats)]
                data_registers = [self.data_qubits[start_index:start_index + self._num_qubits_in_cat_state]
                                  for start_index in range(0, len(self.data_qubits), self._num_qubits_in_cat_state)]
                registers = [data_register + extra_qubits for data_register, extra_qubits in zip(data_registers, extra_qubits_per_register)]
                five_qubit_codes = [generic_five_qubit.create_new(qubit_start_index=i * num_qubits_needed_per_register)
                                    for i in range(self.num_cats)]
                return Circuit(
                    [
                        [
                            [
                                [
                                    X(register[i]).controlled_by(register[num_qubits_needed_per_register - 1]),
                                    R(register[i]),
                                ] for i in range(num_qubits_needed_per_register, self._num_qubits_in_cat_state)
                            ],
                            [
                                [
                                    [
                                        X(register[i]).controlled_by(register[self._num_qubits_in_cat_state - 1])
                                        for i in range(self._num_qubits_in_cat_state, num_qubits_needed_per_register)
                                    ],
                                    CatStateCreatorFlagPattern(qubit_register=register[self._num_qubits_in_cat_state:num_qubits_needed_per_register]).correct_errors(),
                                ],
                                CatStateCreatorFlagPattern(qubit_register=register).correct_errors(),
                            ]
                        ] for register in registers
                    ],
                    [
                        [
                            code.encode_logical_qubit(),
                            code.get_error_correction_circuit(),
                            code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.H, qubit_index=0)),
                            code.get_error_correction_circuit(),
                            code.decode_logical_qubit(),
                        ] for code in five_qubit_codes
                    ],
                    [
                        [
                            [
                                [
                                    X(register[i]).controlled_by(register[num_qubits_needed_per_register - 1])
                                    for i in range(self._num_qubits_in_cat_state - 1, num_qubits_needed_per_register, -1)
                                ],
                                CatStateCreatorFlagPattern(qubit_register=data_register).correct_errors(),
                            ],
                            [
                                [
                                    [
                                        X(register[i]).controlled_by(register[self._num_qubits_in_cat_state - 1]),
                                        R(register[i]),
                                    ] for i in range(num_qubits_needed_per_register - 1, self._num_qubits_in_cat_state, -1)
                                ],
                                CatStateCreatorFlagPattern(qubit_register=data_register).correct_errors(),
                            ]
                        ] for data_register, register in zip(data_registers, registers)
                    ],
                    self.get_error_correction_circuit()
                )
        return None
