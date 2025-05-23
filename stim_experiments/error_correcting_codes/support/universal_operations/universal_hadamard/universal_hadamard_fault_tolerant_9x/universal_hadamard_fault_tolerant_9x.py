from contextlib import contextmanager
from typing import Generator
from uuid import uuid4

import sympy
from cirq import Circuit, CircuitOperation, FrozenCircuit, MeasurementKey, OP_TREE, Operation, \
    R, X

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.universal_hadamard_fault_tolerant_9x_context import \
    UniversalHadamardFaultTolerant9xContext
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_subregister_parity_code.three_subregister_parity_code import \
    ThreeSubregisterParityCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import cx_sequentially_further_qubits_from_first


class UniversalHadamardFaultTolerant9x(UniversalHadamard):
    def get_hadamard_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                self._encode_three_cat(context=context),
                self._cxz_helpers_to_data(context=context),
                self._ensure_subregister_parity_in_plus(context=context),

                self._encode_helper_registers(context=context),
                self._cx_original_to_helpers(context=context),
                self._create_cat_states_on_all_subregisters(context=context),

                self._measure_out_helper(context=context),
                self._reset_ancilla_qubits(context=context),
            )

    def _encode_three_cat(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.three_cat_small]) as encodings_store:
            return [
                context.three_cat_small.encode_logical_qubit(),
                encodings_store.get_all_correction_circuits()
            ]

    def _cxz_helpers_to_data(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        repetition_codes = [RepetitionCode(num_qubits=len(subregister), qubits=subregister)
                            for subregister in context.three_cat_small.subregisters]
        with ActiveEncodingsStore(additional_tracked_encodings=repetition_codes) as encodings_store:
            return [
                self._c_operations_helpers_to_data(operations=context.data_code_logical_x, encodings_store=encodings_store,  context=context),
                self._c_operations_helpers_to_data(operations=context.data_code_logical_z, encodings_store=encodings_store, context=context),
            ]

    def _c_operations_helpers_to_data(self,
                                      operations: list[Operation],
                                      encodings_store: ActiveEncodingsStore,
                                      context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        return [
            [
                ControlledSingleQubitGatesApplier(operations=operations, controls=subregister[:len(operations)]).get_circuit(),
                encodings_store.get_all_correction_circuits(),
            ]
            for subregister in context.three_cat_small.subregisters
        ]

    def _encode_helper_registers(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        additional_universal_hadamard_codes = context.three_subregister_parity_codes_small[1:]
        with ActiveEncodingsStore(additional_tracked_encodings=additional_universal_hadamard_codes) as encodings_store:
            return [
                [code.encode_logical_qubit() for code in additional_universal_hadamard_codes],
                encodings_store.get_all_correction_circuits(),
            ]

    def _cx_original_to_helpers(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=context.three_subregister_parity_codes_small) as encodings_store:
            return [
                [
                    [
                        X(target_qubit).controlled_by(control_qubit)
                        for target_qubit, control_qubit in zip(code.data_qubits, context.three_subregister_parity_codes_small[0].data_qubits)
                    ],
                    encodings_store.get_all_correction_circuits(),
                ] for code in context.three_subregister_parity_codes_small[1:]
            ]

    def _create_cat_states_on_all_subregisters(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.three_cat_large]) as encodings_store:
            return [
                [
                    [
                        cx_sequentially_further_qubits_from_first(qubits=subregister),
                        self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit(),
                    ] for code in context.three_subregister_parity_codes_small for subregister in code.subregisters
                ],
                encodings_store.get_all_correction_circuits(),
            ]

    def _ensure_subregister_parity_in_plus(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        measurement_key = MeasurementKey(f'PREPARE_SUBREGISTER_PARITY_CODE_{uuid4().hex}')
        measurement_symbol = sympy.symbols(measurement_key.name)
        subregister_parity_x, subregister_parity_z = (
            list(context.three_subregister_parity_codes_small[0].get_operation_circuit(
                operation=LogicalOperation(gate=gate, qubit_index=0)
            ).all_operations())
            for gate in (LogicalGateLabel.X, LogicalGateLabel.Z)
        )
        with ActiveEncodingsStore(additional_tracked_encodings=[context.three_subregister_parity_codes_small[0]]) as encodings_store:
            return [
                self._measurer_type(
                    operations=subregister_parity_x + subregister_parity_z + context.data_code_logical_x + context.data_code_logical_z,
                    measurement_key=measurement_key
                ).get_measurement_circuit(),
                CircuitOperation(
                    FrozenCircuit(subregister_parity_z)
                ).with_classical_controls(sympy.Eq(measurement_symbol, 0)),
                encodings_store.get_all_correction_circuits(),
            ]

    def _measure_out_helper(self, context: UniversalHadamardFaultTolerant9xContext) -> OP_TREE:
        measurement_key = MeasurementKey(f'UNIVERSAL_HADAMARD_MEASUREMENT_{uuid4().hex}')
        measurement_key_symbol = sympy.symbols(measurement_key.name)
        logical_z = list(context.three_subregister_parity_code_large.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        ).all_operations())
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            return [
                FrozenCircuit(  # cirq seems to be reversing the order of these operations when not frozen
                    self._measurer_type(operations=logical_z, measurement_key=measurement_key).get_measurement_circuit(),
                    CircuitOperation(FrozenCircuit(context.data_code_logical_x)).with_classical_controls(measurement_key),
                    CircuitOperation(FrozenCircuit(context.data_code_logical_z)).with_classical_controls(sympy.Eq(measurement_key_symbol, 0)),
                ),
                encodings_store.get_all_correction_circuits(),
            ]

    @staticmethod
    def _reset_ancilla_qubits(context: UniversalHadamardFaultTolerant9xContext):
        return [R(qubit) for qubit in context.ancilla_qubits]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalHadamardFaultTolerant9xContext, None, None]:
        num_subregister_parity_codes = 3
        num_qubits_in_desired_encoding = len(self._code.data_qubits)
        num_qubits_per_subregister_parity_code = num_qubits_in_desired_encoding * ThreeSubregisterParityCode.num_cats
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=num_subregister_parity_codes * num_qubits_per_subregister_parity_code) as ancilla_qubits:
            three_subregister_parity_codes = [
                ThreeSubregisterParityCode(
                    num_qubits_in_cat_state=num_qubits_in_desired_encoding,
                    qubits=ancilla_qubits[code_index * num_qubits_per_subregister_parity_code:(code_index + 1) * num_qubits_per_subregister_parity_code],
                )
                for code_index in range(num_subregister_parity_codes)
            ]
            logical_x, logical_z = (
                list(self._code.get_operation_circuit(
                    operation=LogicalOperation(gate=gate, qubit_index=self._qubit_index)
                ).all_operations())
                for gate in (LogicalGateLabel.X, LogicalGateLabel.Z)
            )
            yield UniversalHadamardFaultTolerant9xContext(
                ancilla_qubits=ancilla_qubits,
                three_subregister_parity_codes_small=three_subregister_parity_codes,
                three_subregister_parity_code_large=ThreeSubregisterParityCode(num_qubits_in_cat_state=len(ancilla_qubits) // num_subregister_parity_codes, qubits=ancilla_qubits),
                three_cat_small=ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_desired_encoding, qubits=three_subregister_parity_codes[0].data_qubits),
                three_cat_large=ThreeCatCode(num_qubits_in_cat_state=len(ancilla_qubits) // num_subregister_parity_codes, qubits=ancilla_qubits),
                data_code_logical_x=logical_x,
                data_code_logical_z=logical_z,
            )

    @property
    def _cat_state_creator_type(self) -> type[CatStateCreator]:
        return self._configuration.cat_state_creator_type

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
