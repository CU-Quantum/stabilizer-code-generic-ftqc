from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from typing import Generator
from uuid import uuid4

import sympy
from cirq import Circuit, CircuitOperation, FrozenCircuit, LineQubit, MeasurementKey, OP_TREE, Operation, R, X

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.singletons.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.singletons.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities import cx_sequentially_further_qubits_from_first


@dataclass
class UniversalHadamardCodeToComputationalLogicalContext:
    ancilla_qubits: list[LineQubit]
    additional_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]
    all_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]
    helper_3cat: ThreeCatCode


class ThreeCatSubregisterParityCodeToComputationalLogical:
    def __init__(self,
                 universal_hadamard_code: ThreeCatSubregisterParityCode,
                 desired_encoding: ErrorCorrectingCode,
                 ):
        self._universal_hadamard_code = universal_hadamard_code
        self._desired_encoding = desired_encoding

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        self._cat_state_creator_type = configuration.cat_state_creator_type
        self._measurer_type = configuration.measurer_type

    def get_circuit(self) -> Circuit:
        # TODO create Singleton logical encoding store so that all encodings can be corrected at any time or place throughout the code
        with self._use_fresh_ancilla_qubits() as universal_hadamard_code_helper_context:
            ancilla_qubits = universal_hadamard_code_helper_context.ancilla_qubits
            additional_universal_hadamard_codes = universal_hadamard_code_helper_context.additional_universal_hadamard_codes
            all_universal_hadamard_codes = universal_hadamard_code_helper_context.all_universal_hadamard_codes
            large_3cat = universal_hadamard_code_helper_context.helper_3cat

            three_desired_codes = [
                self._desired_encoding.create_new(qubits=code.subregisters[0])
                for code in all_universal_hadamard_codes
            ]
            return Circuit(
                self._encode_helper_registers(codes=additional_universal_hadamard_codes),
                self._correct_codes(codes=all_universal_hadamard_codes),

                self._cx_data_to_helpers(codes=additional_universal_hadamard_codes, codes_to_correct=all_universal_hadamard_codes),

                self._create_cat_states_on_all_subregisters(codes=all_universal_hadamard_codes),
                self._correct_codes(codes=[large_3cat]),

                self._encode_to_desired_code(desired_codes=three_desired_codes, all_universal_hadamard_codes=all_universal_hadamard_codes),

                self._measure_helper_codes(helper_codes=three_desired_codes[1:]),
                self._correct_codes(codes=[three_desired_codes[0]]),
                self._get_recovery_circuit(desired_code=three_desired_codes[0]),

                self._reset_ancilla_qubits(ancilla_qubits=ancilla_qubits),
            )

    @staticmethod
    def _cx_additional_universal_hadamard_codes(codes: list[ErrorCorrectingCode]) -> OP_TREE:
        return [
            cx_sequentially_further_qubits_from_first(qubits=code.data_qubits)
            for code in codes
        ]

    def _cx_data_to_helpers(self, codes: list[ThreeCatSubregisterParityCode], codes_to_correct: list[ErrorCorrectingCode]) -> OP_TREE:
        return [
            [
                self._cx_data_to_helper(code=code),
                self._correct_codes(codes=codes_to_correct),
            ] for code in codes
        ]

    def _cx_data_to_helper(self, code: ThreeCatSubregisterParityCode) -> list[list[Operation]]:
        return [X(target_qubit).controlled_by(control_qubit)
                for target_qubit, control_qubit in zip(code.data_qubits, self._universal_hadamard_code.data_qubits)]

    def _create_cat_states_on_all_subregisters(self, codes: list[ThreeCatSubregisterParityCode]) -> OP_TREE:
        return [
            [
                cx_sequentially_further_qubits_from_first(qubits=subregister),
                self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit(),
            ] for code in codes for subregister in code.subregisters
        ]

    def _encode_to_desired_code(self, desired_codes: list[ErrorCorrectingCode], all_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]) -> OP_TREE:
        unentangle_extra_subregisters = [
            cx_sequentially_further_qubits_from_first(qubits=code.data_qubits[len(code.subregisters[0]) - 1:])
            for code in all_universal_hadamard_codes
        ]
        small_3cat_qubits = [qubit for code in desired_codes for qubit in code.data_qubits]
        small_3cat = ThreeCatCode(num_qubits_in_cat_state=len(desired_codes[0].data_qubits), qubits=small_3cat_qubits)
        logical_x_operations = [
            list(code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)).all_operations()) # TODO allow for multiqubit encoding
            for code in desired_codes
        ]

        symptoms = [
            sympy.And(sympy.Eq(self._measurement_key_symbols[0], 1), sympy.Eq(self._measurement_key_symbols[1], 0)),
            sympy.And(sympy.Eq(self._measurement_key_symbols[0], 1), sympy.Eq(self._measurement_key_symbols[1], 1)),
            sympy.And(sympy.Eq(self._measurement_key_symbols[0], 0), sympy.Eq(self._measurement_key_symbols[1], 1)),
        ]
        logical_z_operations = [
            list(code.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)).all_operations()) # TODO allow for multiqubit encoding
            for code in desired_codes
        ]

        return [
            unentangle_extra_subregisters,
            small_3cat.get_error_correction_circuit(),
            [
                desired_code.encode_logical_qubit()
                for desired_code in desired_codes
            ],
            self._correct_codes(codes=desired_codes),
            [
                self._measurer_type(operations=logical_x_operations[i] + logical_x_operations[i + 1], measurement_key=measurement_key).get_measurement_circuit()
                for i, measurement_key in enumerate(self._measurement_keys)
            ],
            [
                CircuitOperation(FrozenCircuit(logical_z)).with_classical_controls(condition)
                for condition, logical_z in zip(symptoms, logical_z_operations)
            ]
        ]

    def _measure_helper_codes(self, helper_codes: list[ErrorCorrectingCode]) -> list[Circuit]:
        operations_per_code = [
            list(code.get_operation_circuit(
                LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)  # TODO allow for multiqubit encoding
            ).all_operations())
            for code in helper_codes
        ]
        return [
            self._measurer_type(
                operations=operations,
                measurement_key=measurement_key
            ).get_measurement_circuit()
            for measurement_key, operations in zip(self._measurement_keys, operations_per_code)
        ]

    def _get_recovery_circuit(self, desired_code: ErrorCorrectingCode) -> Circuit:
        xor_condition = sympy.Xor(*self._measurement_key_symbols)
        logical_operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        return Circuit(
            CircuitOperation(
                FrozenCircuit(list(desired_code.get_operation_circuit(logical_operation).all_operations())),
            ).with_classical_controls(xor_condition)
        )

    @cached_property
    def _measurement_key_symbols(self) -> list[sympy.Symbol]:
        return sympy.symbols(' '.join([key.name for key in self._measurement_keys]))

    @cached_property
    def _measurement_keys(self) -> list[MeasurementKey]:
        return [MeasurementKey(f'UNIVERSAL_HADAMARD_CODE_MEASURE_{uuid4()}') for _ in range(self._num_additional_universal_hadamard_codes)]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalHadamardCodeToComputationalLogicalContext, None, None]:
        num_qubits_in_universal_hadamard_code = len(self._universal_hadamard_code.data_qubits)
        num_ancilla_qubits = num_qubits_in_universal_hadamard_code * self._num_additional_universal_hadamard_codes
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=num_ancilla_qubits) as ancilla_qubits:
            additional_universal_hadamard_codes = [
                self._universal_hadamard_code.create_new(
                    qubits=ancilla_qubits[i * num_qubits_in_universal_hadamard_code:(i + 1) * num_qubits_in_universal_hadamard_code]
                )
                for i in range(self._num_additional_universal_hadamard_codes)
            ]
            helper_3cat = ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_universal_hadamard_code,
                                       qubits=self._universal_hadamard_code.data_qubits + ancilla_qubits)
            yield UniversalHadamardCodeToComputationalLogicalContext(
                ancilla_qubits=ancilla_qubits,
                additional_universal_hadamard_codes=additional_universal_hadamard_codes,
                all_universal_hadamard_codes=[self._universal_hadamard_code] + additional_universal_hadamard_codes,
                helper_3cat=helper_3cat,
            )

    @staticmethod
    def _encode_helper_registers(codes: list[ErrorCorrectingCode]) -> list[Circuit]:
        return [code.encode_logical_qubit() for code in codes]

    @staticmethod
    def _correct_codes(codes: list[ErrorCorrectingCode]) -> list[Circuit]:
        return [code.get_error_correction_circuit() for code in codes]

    @staticmethod
    def _reset_ancilla_qubits(ancilla_qubits: list[LineQubit]):
        return [R(qubit) for qubit in ancilla_qubits]

    @property
    def _num_additional_universal_hadamard_codes(self) -> int:
        return 2
