from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from typing import Generator, Type
from uuid import uuid4

import sympy
from cirq import Circuit, LineQubit, MeasurementKey, OP_TREE, Operation, R, X

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import OperationsApplier
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_cat_state import \
    OperationsApplierUsingCatState
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.universal_hadamard_code.universal_hadamard_code import \
    UniversalHadamardCode
from stim_experiments.utilities import FreshAncillasPool, cx_sequentially_further_qubits_from_first


@dataclass
class UniversalHadamardHelperContext:
    ancilla_qubits: list[LineQubit]
    additional_universal_hadamard_codes: list[UniversalHadamardCode]
    all_universal_hadamard_codes: list[UniversalHadamardCode]
    helper_3cat: ThreeCatCode


class UniversalHadamardHelper:
    """
    note that this is only valid for the logical computational basis states
    """
    def __init__(self,
                 universal_hadamard_code: UniversalHadamardCode,
                 desired_encoding: ErrorCorrectingCode,
                 cat_state_creator_type: Type[CatStateCreator] = CatStateCreatorFlagPattern,
                 measurer_type: Type[Measurer] = FaultTolerantMeasurer,
                 operations_applier_type: Type[OperationsApplier] = OperationsApplierUsingCatState,
                 ):
        self._universal_hadamard_code = universal_hadamard_code
        self._desired_encoding = desired_encoding
        self._cat_state_creator_type = cat_state_creator_type
        self._measurer_type = measurer_type
        self._operations_applier_type = operations_applier_type

    def get_circuit(self) -> Circuit:
        # TODO create Singleton logical encoding store so that all encodings can be corrected at any time or place throughout the code
        with self.use_fresh_ancilla_qubits() as universal_hadamard_code_helper_context:
            ancilla_qubits = universal_hadamard_code_helper_context.ancilla_qubits
            additional_universal_hadamard_codes = universal_hadamard_code_helper_context.additional_universal_hadamard_codes
            all_universal_hadamard_codes = universal_hadamard_code_helper_context.all_universal_hadamard_codes
            helper_3cat = universal_hadamard_code_helper_context.helper_3cat
            return Circuit(
                self.encode_helper_registers(codes=additional_universal_hadamard_codes),
                self.correct_codes(codes=all_universal_hadamard_codes),

                self.cx_data_to_helpers(codes=additional_universal_hadamard_codes, codes_to_correct=all_universal_hadamard_codes),

                self.create_cat_states_on_all_subregisters(codes=all_universal_hadamard_codes),
                self.correct_codes(codes=[helper_3cat]),

                self.encode_to_desired_code(),
                self.correct_codes(codes=[self._desired_encoding] + additional_universal_hadamard_codes),

                self.measure_helper_codes(helper_codes=additional_universal_hadamard_codes),
                self.reset_ancilla_qubits(ancilla_qubits=ancilla_qubits),
                self.correct_codes(codes=[self._desired_encoding]),

                self.get_recovery_circuit(),
            )

    def cx_data_to_helpers(self, codes: list[UniversalHadamardCode], codes_to_correct: list[ErrorCorrectingCode]) -> OP_TREE:
        return [
            [
                self._cx_data_to_helper(code=code),
                self.correct_codes(codes=codes_to_correct),
            ] for code in codes
        ]

    def _cx_data_to_helper(self, code: UniversalHadamardCode) -> list[list[Operation]]:
        return [X(target_qubit).controlled_by(control_qubit)
                for target_qubit, control_qubit in zip(code.data_qubits, self._universal_hadamard_code.data_qubits)]

    def create_cat_states_on_all_subregisters(self, codes: list[UniversalHadamardCode]) -> OP_TREE:
        return [
            [
                cx_sequentially_further_qubits_from_first(qubits=subregister),
                self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit(),
            ] for code in codes for subregister in code.subregisters
        ]

    def encode_to_desired_code(self):
        desired_code = self._desired_encoding.create_new(qubits=self._universal_hadamard_code.subregisters[0])
        unentangle_extra_subregisters = [  # TODO do this for all three uni h codes, then correct with 3cat before encoding desired
            X(self._universal_hadamard_code.data_qubits[0]).controlled_by(self._universal_hadamard_code.data_qubits[i])
            for i in range(len(self._universal_hadamard_code.subregisters[0]), len(self._universal_hadamard_code.data_qubits))
        ]
        return [
            unentangle_extra_subregisters,
            desired_code.encode_logical_qubit()
        ]

    def measure_helper_codes(self, helper_codes: list[UniversalHadamardCode]) -> list[Circuit]:
        return [
            self._measurer_type(
                operations=list(code.get_operation_circuit(
                    LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)  # TODO allow for multiqubit encoding
                ).all_operations()),
                measurement_key=measurement_key
            ).get_measurement_circuit()
            for measurement_key, code in zip(self._measurement_keys, helper_codes)
        ]

    @cached_property
    def _measurement_keys(self) -> list[MeasurementKey]:
        return [MeasurementKey(f'UNIVERSAL_HADAMARD_CODE_MEASURE_{uuid4()}') for _ in range(self._num_additional_universal_hadamard_codes)]

    def get_recovery_circuit(self) -> Circuit:
        return self._operations_applier_type(
            operations=self._get_operations_for_recovery(),
            condition=self._get_xor_condition()
        ).get_application_circuit()

    def _get_operations_for_recovery(self) -> list[Operation]:
        logical_operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        return list(self._desired_encoding.get_operation_circuit(logical_operation).all_operations())

    def _get_xor_condition(self) -> sympy.Expr:
        measurement_key_symbols = sympy.symbols(' '.join([key.name for key in self._measurement_keys]))
        return sympy.Xor(*measurement_key_symbols)

    @contextmanager
    def use_fresh_ancilla_qubits(self) -> Generator[UniversalHadamardHelperContext, None, None]:
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
            yield UniversalHadamardHelperContext(
                ancilla_qubits=ancilla_qubits,
                additional_universal_hadamard_codes=additional_universal_hadamard_codes,
                all_universal_hadamard_codes=[self._universal_hadamard_code] + additional_universal_hadamard_codes,
                helper_3cat=helper_3cat,
            )

    @staticmethod
    def encode_helper_registers(codes: list[ErrorCorrectingCode]) -> list[Circuit]:
        return [code.encode_logical_qubit() for code in codes]

    @staticmethod
    def correct_codes(codes: list[ErrorCorrectingCode]) -> list[Circuit]:
        return [code.get_error_correction_circuit() for code in codes]

    @staticmethod
    def reset_ancilla_qubits(ancilla_qubits: list[LineQubit]):
        return [R(qubit) for qubit in ancilla_qubits]

    @property
    def _num_additional_universal_hadamard_codes(self) -> int:
        return 2
