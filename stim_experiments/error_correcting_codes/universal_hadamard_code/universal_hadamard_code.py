from functools import cached_property
from typing import Optional
from uuid import uuid4

import sympy
from cirq import Circuit, CircuitOperation, FrozenCircuit, LineQubit, MeasurementKey, Operation, R, X, Z
from numpy import array

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.generic_stabilizer_code.custom_dataclasses.check_matrix import CheckMatrix
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.check_matrix_to_gates import \
    CheckMatrixToOperations
from stim_experiments.error_correcting_codes.generic_stabilizer_code.support.recovery_finder import RecoveryFinder
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.fault_tolerant_error_correction.fault_tolerant_error_correction import \
    FaultTolerantErrorCorrection
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer, OperationsApplierUsingCatState
from stim_experiments.error_correcting_codes.support.fault_tolerant_state_encoder.fault_tolerant_state_encoder import \
    FaultTolerantStateEncoder
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities import FreshAncillasPool


class UniversalHadamardCode(ErrorCorrectingCode):
    num_cats = ThreeCatCode.num_cats

    def __init__(self, num_qubits_in_cat_state: int, qubits: Optional[list[LineQubit]] = None):
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
                         qubits=qubits)

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
            # TODO create Singleton logical encoding store so that all encodings can be corrected at any time or place throughout the code
            # note that this is not valid for an arbitrary state and should only be used as part of the Universal Hadamard Gate
            num_additional_codes = 2
            measurement_keys = [MeasurementKey(f'UNIVERSAL_HADAMARD_CODE_MEASURE_{uuid4()}') for _ in range(num_additional_codes)]
            measurement_key_symbols = sympy.symbols(' '.join([key.name for key in measurement_keys]))
            xor_measurements = sympy.Xor(*measurement_key_symbols)
            with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_data_qubits * num_additional_codes) as ancilla_qubits:
                helper_codes = [UniversalHadamardCode(num_qubits_in_cat_state=self._num_qubits_in_cat_state,
                                                      qubits=ancilla_qubits[i * self._num_data_qubits:(i + 1) * self._num_data_qubits])
                                for i in range(num_additional_codes)]
                helper_3cat = ThreeCatCode(num_qubits_in_cat_state=self._num_qubits_in_cat_state * self.num_cats,
                                           qubits=ancilla_qubits + self.data_qubits)
                return Circuit(
                    [
                        [
                            code.encode_logical_qubit(),

                            code.get_error_correction_circuit(),
                            self.get_error_correction_circuit(),
                            [X(target_qubit).controlled_by(control_qubit) for target_qubit, control_qubit in zip(code.data_qubits, self.data_qubits)],
                            code.get_error_correction_circuit(),

                            self.get_error_correction_circuit(),
                            [
                                [
                                    [X(subregister[i]).controlled_by(subregister[0])
                                     for i in range(1, self._num_qubits_in_cat_state)],
                                    CatStateCreatorFlagPattern(qubit_register=subregister).get_cat_state_circuit(),
                                ] for subregister in code.subregisters
                            ],
                        ] for code in helper_codes
                    ],
                    helper_3cat.get_error_correction_circuit(),
                    [code.encode_logical_qubit() for code in helper_codes],
                    [
                        [
                            code.get_error_correction_circuit(),
                            FaultTolerantMeasurer(
                                operations=list(code.get_operation_circuit(
                                    LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
                                ).all_operations()),
                                measurement_key=measurement_key
                            ).get_measurement_circuit(),
                        ] for measurement_key, code in zip(measurement_keys, helper_codes)
                    ],
                    OperationsApplierUsingCatState(
                        operations=list(self.get_operation_circuit(
                            LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
                        ).all_operations()),
                        condition=xor_measurements
                    ).get_circuit(),
                    [
                        R(qubit) for qubit in ancilla_qubits
                    ]
                )
        return None

    @cached_property
    def subregisters(self) -> list[list[LineQubit]]:
        return [self.data_qubits[i * self._num_qubits_in_cat_state:(i + 1) * self._num_qubits_in_cat_state]
                for i in range(self.num_cats)]
