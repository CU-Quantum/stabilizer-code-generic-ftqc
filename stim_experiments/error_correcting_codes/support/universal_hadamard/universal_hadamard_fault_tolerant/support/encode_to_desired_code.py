from functools import cached_property
from uuid import uuid4

import sympy
from cirq import CircuitOperation, FrozenCircuit, MeasurementKey, OP_TREE

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.support.hadamard_computational_logical_three_subregister_parity_code_context import \
    HadamardComputationalLogicalThreeSubregisterParityCodeContext
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.utilities.utilities import cx_sequentially_further_qubits_from_first


class EncodeToDesiredCode:
    def __init__(self, context: HadamardComputationalLogicalThreeSubregisterParityCodeContext):
        self._context = context

    def get_encoding_circuit(self):
        return [
            self._encode_into_three_of_desired_codes(),
            self._measure_out_additional_codes()
        ]

    def _encode_into_three_of_desired_codes(self) -> OP_TREE:
        return [
            self._encode_into_desired_codes(),
            self._correct_phase_errors(),
        ]

    def _encode_into_desired_codes(self) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=self._context.all_universal_hadamard_codes) as encodings_store:
            return [
                [
                    desired_code.encode_logical_qubit()
                    for desired_code in self._context.all_universal_hadamard_codes
                ],
                encodings_store.get_all_correction_circuits()
            ]

    def _correct_phase_errors(self) -> OP_TREE:
        symptoms = [
            sympy.And(sympy.Eq(self._measurement_key_symbols[0], 1), sympy.Eq(self._measurement_key_symbols[1], 0)),
            sympy.And(sympy.Eq(self._measurement_key_symbols[0], 1), sympy.Eq(self._measurement_key_symbols[1], 1)),
            sympy.And(sympy.Eq(self._measurement_key_symbols[0], 0), sympy.Eq(self._measurement_key_symbols[1], 1)),
        ]
        logical_x_operations, logical_z_operations = (
            [
                list(code.get_operation_circuit(LogicalOperation(gate=gate, qubit_index=0)).all_operations())
                for code in self._context.all_universal_hadamard_codes
            ]
            for gate in (LogicalGateLabel.X, LogicalGateLabel.Z)
        )

        with ActiveEncodingsStore(additional_tracked_encodings=self._context.all_universal_hadamard_codes) as encodings_store:
            return [
                [
                    self._measurer_type(operations=logical_x_operations[i] + logical_x_operations[i + 1],
                                        measurement_key=measurement_key).get_measurement_circuit()
                    for i, measurement_key in enumerate(self._measurement_keys)
                ],
                [
                    CircuitOperation(FrozenCircuit(logical_z)).with_classical_controls(condition)
                    for condition, logical_z in zip(symptoms, logical_z_operations)
                ],
                encodings_store.get_all_correction_circuits(),
            ]

    def _measure_out_additional_codes(self) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[self._context.all_universal_hadamard_codes[0]]) as encodings_store:
            return [
                self._get_measurement_operations(),
                self._get_recovery_operations(),
                encodings_store.get_all_correction_circuits(),
            ]

    def _get_measurement_operations(self) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[self._context.all_universal_hadamard_codes[1]]) as encodings_store:
            operations_per_code = [
                list(code.get_operation_circuit(
                    LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
                ).all_operations())
                for code in self._context.all_universal_hadamard_codes[1:]
            ]
            measurements = [
                self._measurer_type(
                    operations=operations,
                    measurement_key=measurement_key
                ).get_measurement_circuit()
                for measurement_key, operations in zip(self._measurement_keys, operations_per_code)
            ]
            measurements.insert(1, encodings_store.get_all_correction_circuits())
            return measurements

    def _get_recovery_operations(self) -> OP_TREE:
        xor_condition = sympy.Xor(*self._measurement_key_symbols)
        logical_operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        return CircuitOperation(
            FrozenCircuit(
                list(self._context.all_universal_hadamard_codes[0].get_operation_circuit(logical_operation).all_operations())),
        ).with_classical_controls(xor_condition)

    @cached_property
    def _measurement_key_symbols(self) -> list[sympy.Symbol]:
        return sympy.symbols(' '.join([key.name for key in self._measurement_keys]))

    @cached_property
    def _measurement_keys(self) -> list[MeasurementKey]:
        return [MeasurementKey(f'ENCODE_TO_THREE_DESIRED_{uuid4()}') for _ in range(len(self._context.all_universal_hadamard_codes) - 1)]

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
