from functools import cached_property
from uuid import uuid4

import sympy
from cirq import Circuit, LineQubit, MeasurementKey, OP_TREE, Operation, R, X

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer, OperationsApplierUsingCatState
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.utilities import FreshAncillasPool


class UniversalHadamardCodeHelper:
    """
    note that this is only valid for the logical computational basis states
    """
    def __init__(self, code: 'UniversalHadamardCode'):
        self._code = code
        self._num_additional_codes = 2

    def get_circuit(self) -> Circuit:
        # TODO create Singleton logical encoding store so that all encodings can be corrected at any time or place throughout the code
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=self._num_data_qubits * self._num_additional_codes) as ancilla_qubits:
            helper_codes = [self._code.create_new(qubits=ancilla_qubits[i * self._num_data_qubits:(i + 1) * self._num_data_qubits])
                            for i in range(self._num_additional_codes)]
            all_universal_hadamard_codes = [self._code] + helper_codes
            helper_3cat = ThreeCatCode(num_qubits_in_cat_state=self._num_data_qubits, qubits=ancilla_qubits + self._code.data_qubits)
            return Circuit(
                self.encode_helper_registers(helper_codes=helper_codes),
                self.correct_codes(codes=all_universal_hadamard_codes),

                self.cx_data_to_helpers(codes=helper_codes, codes_to_correct=all_universal_hadamard_codes),

                self.create_cat_states_on_call_subregisters(codes=helper_codes),
                self.correct_codes(codes=[helper_3cat]),

                self.encode_helper_registers(helper_codes=helper_codes),
                self.correct_codes(codes=all_universal_hadamard_codes),

                self.measure_helper_codes(helper_codes=helper_codes),
                self.reset_ancilla_qubits(ancilla_qubits=ancilla_qubits),
                self.correct_codes(codes=[self._code]),

                self.get_recovery_circuit(),
            )

    def get_recovery_circuit(self):
        return OperationsApplierUsingCatState(
            operations=self._get_operations_for_recovery(),
            condition=self._get_xor_condition()
        ).get_circuit()

    def _get_operations_for_recovery(self) -> list[Operation]:
        logical_operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        return list(self._code.get_operation_circuit(logical_operation).all_operations())

    def _get_xor_condition(self) -> sympy.Expr:
        measurement_key_symbols = sympy.symbols(' '.join([key.name for key in self._measurement_keys]))
        return sympy.Xor(*measurement_key_symbols)

    @staticmethod
    def reset_ancilla_qubits(ancilla_qubits: list[LineQubit]):
        return [R(qubit) for qubit in ancilla_qubits]

    def measure_helper_codes(self, helper_codes: list['UniversalHadamardCode']) -> list[Circuit]:
        return [
            FaultTolerantMeasurer(
                operations=list(code.get_operation_circuit(
                    LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
                ).all_operations()),
                measurement_key=measurement_key
            ).get_measurement_circuit()
            for measurement_key, code in zip(self._measurement_keys, helper_codes)
        ]

    @cached_property
    def _measurement_keys(self) -> list[MeasurementKey]:
        return [MeasurementKey(f'UNIVERSAL_HADAMARD_CODE_MEASURE_{uuid4()}') for _ in range(self._num_additional_codes)]

    @staticmethod
    def create_cat_states_on_call_subregisters(codes: list['UniversalHadamardCode']) -> OP_TREE:
        return [
            [
                [X(subregister[i]).controlled_by(subregister[0]) for i in range(1, len(subregister))],
                CatStateCreatorFlagPattern(qubit_register=subregister).get_cat_state_circuit(),
            ] for code in codes for subregister in code.subregisters
        ]

    def cx_data_to_helpers(self, codes: list['UniversalHadamardCode'], codes_to_correct: list[ErrorCorrectingCode]) -> OP_TREE:
        return [
            [
                self.cx_data_to_helper(code=code),
                self.correct_codes(codes=codes_to_correct),
            ] for code in codes
        ]

    def cx_data_to_helper(self, code: 'UniversalHadamardCode') -> list[list[Operation]]:
        return [X(target_qubit).controlled_by(control_qubit)
                for target_qubit, control_qubit in zip(code.data_qubits, self._code.data_qubits)]

    @staticmethod
    def encode_helper_registers(helper_codes: list['UniversalHadamardCode']) -> list[Circuit]:
        return [code.encode_logical_qubit() for code in helper_codes]

    @staticmethod
    def correct_codes(codes: list[ErrorCorrectingCode]) -> list[Circuit]:
        return [code.get_error_correction_circuit() for code in codes]

    @property
    def _num_qubits_in_cat_state(self) -> int:
        return len(self._code.subregisters[0])

    @property
    def _num_data_qubits(self) -> int:
        return len(self._code.data_qubits)
