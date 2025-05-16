from contextlib import contextmanager
from dataclasses import dataclass
from functools import cached_property
from typing import Generator, Optional
from uuid import uuid4

import sympy
from cirq import Circuit, CircuitOperation, FrozenCircuit, LineQubit, MeasurementKey, OP_TREE, Operation, R, X

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities import cx_sequentially_further_qubits_from_first


@dataclass
class ThreeCatSubregisterParityCodeToComputationalLogicalContext:
    ancilla_qubits: list[LineQubit]
    additional_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]
    all_universal_hadamard_codes: list[ThreeCatSubregisterParityCode]
    helper_3cat: ThreeCatCode


class ThreeCatSubregisterParityCodeToComputationalLogical:
    def __init__(self,
                 three_cat_subregister_parity_code: ThreeCatSubregisterParityCode,
                 desired_encoding: ErrorCorrectingCode,
                 ):
        self._three_cat_subregister_parity_code = three_cat_subregister_parity_code
        self._desired_encoding = desired_encoding

        configuration = ConfigurationErrorCorrectingCodeManager().get_configuration()
        self._cat_state_creator_type = configuration.cat_state_creator_type
        self._measurer_type = configuration.measurer_type

        self._circuit = Circuit()
        self._context: Optional[ThreeCatSubregisterParityCodeToComputationalLogicalContext] = None
        self._encodings_store: Optional[ActiveEncodingsStore] = None
        self._three_desired_codes = []

    def get_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            with ActiveEncodingsStore() as encoding_store:
                self._context = context
                self._encodings_store = encoding_store
                self._three_desired_codes = [
                    self._desired_encoding.create_new(qubits=code.subregisters[0])
                    for code in self._context.all_universal_hadamard_codes
                ]

                return Circuit(
                    self._encode_helper_registers(),
                    self._cx_data_to_helpers(),
                    self._create_cat_states_on_all_subregisters(),
                    self._encode_to_desired_code(),
                    self._measure_out_additional_codes(),
                    self._reset_ancilla_qubits(),
                )

    def _encode_helper_registers(self) -> OP_TREE:
        self._encodings_store.replace_tracked_encodings_with(encodings=self._context.all_universal_hadamard_codes)
        codes = self._context.additional_universal_hadamard_codes
        return [
            [code.encode_logical_qubit() for code in codes],
            self._encodings_store.get_all_correction_circuits(),
        ]

    def _cx_data_to_helpers(self) -> OP_TREE:
        return [
            [
                self._cx_data_to_helper(code=code),
                self._encodings_store.get_all_correction_circuits(),
            ] for code in self._context.additional_universal_hadamard_codes
        ]

    def _cx_data_to_helper(self, code: ThreeCatSubregisterParityCode) -> OP_TREE:
        return [X(target_qubit).controlled_by(control_qubit)
                for target_qubit, control_qubit in zip(code.data_qubits, self._three_cat_subregister_parity_code.data_qubits)]

    def _create_cat_states_on_all_subregisters(self) -> OP_TREE:
        self._encodings_store.replace_tracked_encodings_with(encodings=[self._context.helper_3cat])
        return [
            [
                [
                    cx_sequentially_further_qubits_from_first(qubits=subregister),
                    self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit(),
                ] for code in self._context.all_universal_hadamard_codes for subregister in code.subregisters
            ],
            self._encodings_store.get_all_correction_circuits(),
        ]

    def _encode_to_desired_code(self) -> OP_TREE:
        def get_unentangle_extra_subregisters() -> OP_TREE:
            small_3cat_qubits = [qubit for code in self._three_desired_codes for qubit in code.data_qubits]
            small_3cat = ThreeCatCode(num_qubits_in_cat_state=len(self._three_desired_codes[0].data_qubits), qubits=small_3cat_qubits)
            self._encodings_store.replace_tracked_encodings_with(encodings=[small_3cat])
            return [
                [
                    cx_sequentially_further_qubits_from_first(qubits=code.data_qubits[len(code.subregisters[0]) - 1:])
                    for code in self._context.all_universal_hadamard_codes
                ],
                self._encodings_store.get_all_correction_circuits()
            ]

        def encode_into_three_desired_codes() -> OP_TREE:
            self._encodings_store.replace_tracked_encodings_with(encodings=self._three_desired_codes)
            return [
                [
                    desired_code.encode_logical_qubit()
                    for desired_code in self._three_desired_codes
                ],
                self._encodings_store.get_all_correction_circuits()
            ]

        def correct_phase_errors() -> OP_TREE:
            symptoms = [
                sympy.And(sympy.Eq(self._measurement_key_symbols[0], 1), sympy.Eq(self._measurement_key_symbols[1], 0)),
                sympy.And(sympy.Eq(self._measurement_key_symbols[0], 1), sympy.Eq(self._measurement_key_symbols[1], 1)),
                sympy.And(sympy.Eq(self._measurement_key_symbols[0], 0), sympy.Eq(self._measurement_key_symbols[1], 1)),
            ]
            logical_x_operations, logical_z_operations = (
                [
                    list(code.get_operation_circuit(LogicalOperation(gate=gate, qubit_index=0)).all_operations()) # TODO allow for multiqubit encoding
                    for code in self._three_desired_codes
                ]
                for gate in (LogicalGateLabel.X, LogicalGateLabel.Z)
            )

            self._encodings_store.replace_tracked_encodings_with(encodings=self._three_desired_codes)
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
                self._encodings_store.get_all_correction_circuits(),
            ]

        return [
            get_unentangle_extra_subregisters(),
            encode_into_three_desired_codes(),
            correct_phase_errors()
        ]

    def _measure_out_additional_codes(self) -> OP_TREE:
        self._encodings_store.replace_tracked_encodings_with(encodings=[self._three_desired_codes[0]])
        operations_per_code = [
            list(code.get_operation_circuit(
                LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)  # TODO allow for multiqubit encoding
            ).all_operations())
            for code in self._three_desired_codes[1:]
        ]
        xor_condition = sympy.Xor(*self._measurement_key_symbols)
        logical_operation = LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0)
        return [
            [
                self._measurer_type(
                    operations=operations,
                    measurement_key=measurement_key
                ).get_measurement_circuit()
                for measurement_key, operations in zip(self._measurement_keys, operations_per_code)
            ],
            self._encodings_store.get_all_correction_circuits(),
            CircuitOperation(
                FrozenCircuit(
                    list(self._three_desired_codes[0].get_operation_circuit(logical_operation).all_operations())),
            ).with_classical_controls(xor_condition),
            self._encodings_store.get_all_correction_circuits(),
        ]

    @cached_property
    def _measurement_key_symbols(self) -> list[sympy.Symbol]:
        return sympy.symbols(' '.join([key.name for key in self._measurement_keys]))

    @cached_property
    def _measurement_keys(self) -> list[MeasurementKey]:
        return [MeasurementKey(f'UNIVERSAL_HADAMARD_CODE_MEASURE_{uuid4()}') for _ in range(self._num_additional_parity_to_computational_codes)]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[ThreeCatSubregisterParityCodeToComputationalLogicalContext, None, None]:
        num_qubits_in_universal_hadamard_code = len(self._three_cat_subregister_parity_code.data_qubits)
        num_ancilla_qubits = num_qubits_in_universal_hadamard_code * self._num_additional_parity_to_computational_codes
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=num_ancilla_qubits) as ancilla_qubits:
            additional_universal_hadamard_codes = [
                self._three_cat_subregister_parity_code.create_new(
                    qubits=ancilla_qubits[i * num_qubits_in_universal_hadamard_code:(i + 1) * num_qubits_in_universal_hadamard_code]
                )
                for i in range(self._num_additional_parity_to_computational_codes)
            ]
            helper_3cat = ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_universal_hadamard_code,
                                       qubits=self._three_cat_subregister_parity_code.data_qubits + ancilla_qubits)
            yield ThreeCatSubregisterParityCodeToComputationalLogicalContext(
                ancilla_qubits=ancilla_qubits,
                additional_universal_hadamard_codes=additional_universal_hadamard_codes,
                all_universal_hadamard_codes=[self._three_cat_subregister_parity_code] + additional_universal_hadamard_codes,
                helper_3cat=helper_3cat,
            )

    def _reset_ancilla_qubits(self):
        return [R(qubit) for qubit in self._context.ancilla_qubits]

    @property
    def _num_additional_parity_to_computational_codes(self) -> int:
        return 2
