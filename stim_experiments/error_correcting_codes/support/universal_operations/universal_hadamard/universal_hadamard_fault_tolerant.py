from contextlib import contextmanager
from dataclasses import asdict
from functools import cached_property
from typing import Generator
from uuid import uuid4

import sympy
from cirq import Circuit, CircuitOperation, FrozenCircuit, Moment, OP_TREE, Operation, TaggedOperation

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.universal_hadamard_fault_tolerant_context import \
    UniversalHadamardFaultTolerantContext
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier import DELAYED_NOISE_TAG
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.utilities.measurement_key_with_stable_hash import MeasurementKeyWithStableHash


UNIVERSAL_HADAMARD_MEASUREMENT_TAG = 'UNIVERSAL_HADAMARD_MEASUREMENT_TAG'
UNIVERSAL_HADAMARD_CZ_TAG = 'UNIVERSAL_HADAMARD_CZ'
UNIVERSAL_HADAMARD_CX_TAG = 'UNIVERSAL_HADAMARD_CX'


class UniversalHadamardFaultTolerant(UniversalHadamard):
    def get_hadamard_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                self._reset_ancilla_qubits(context=context),
                self._encode_three_cat(context=context),
                self._czx_helpers_to_data(context=context),
                self._measure_out_helper(context=context),
            )

    def _encode_three_cat(self, context: UniversalHadamardFaultTolerantContext) -> OP_TREE:
        return self._universal_operations_utilities.encode_multiple_cat(context=context)

    def _czx_helpers_to_data(self, context: UniversalHadamardFaultTolerantContext) -> OP_TREE:
        operations_on_target = context.data_code_logical_x + context.data_code_logical_z
        operations_on_control = sum([
            list(context.cat_parity_code.get_operation_circuit(
                operation=LogicalOperation(gate=gate_label, qubit_index=0)).all_operations())
            for gate_label in (LogicalGateLabel.X, LogicalGateLabel.Z)
        ], [])
        return [
            [
                TaggedOperation(
                    CircuitOperation(
                        FrozenCircuit(
                            self._universal_operations_utilities.c_operations_helpers_to_data(
                                operations=operations,
                                context=context
                            )
                        )
                    ),
                    tag
                )
                for operations, tag in zip((context.data_code_logical_x, context.data_code_logical_z),
                                           (UNIVERSAL_HADAMARD_CX_TAG, UNIVERSAL_HADAMARD_CZ_TAG))
            ],
            TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        self._universal_operations_utilities.fix_sign_flip_after_subregister_controlled_flips(
                            observable=operations_on_control + operations_on_target,
                            context=context,
                            measurement_trigger=0,
                        )
                    )
                ),

            ),
        ]

    def _measure_out_helper(self, context: UniversalHadamardFaultTolerantContext) -> OP_TREE:
        measurement_key = MeasurementKeyWithStableHash(f'UNIVERSAL_HADAMARD_MEASUREMENT_{uuid4().hex}')
        measurement_key_symbol = sympy.symbols(measurement_key.name)
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            return TaggedOperation(
                CircuitOperation(
                    FrozenCircuit(
                        self._universal_operations_utilities.measure_out_helper(measurement_key=measurement_key, context=context),
                        encodings_store.get_all_correction_circuits(),
                        TaggedOperation(
                            CircuitOperation(
                                FrozenCircuit(
                                    CircuitOperation(
                                        FrozenCircuit(context.data_code_logical_x)).with_classical_controls(
                                        measurement_key),
                                    CircuitOperation(
                                        FrozenCircuit(context.data_code_logical_z)).with_classical_controls(
                                        sympy.Eq(measurement_key_symbol, 0)),
                                )
                            ),
                            DELAYED_NOISE_TAG
                        ),
                    )
                ),
                UNIVERSAL_HADAMARD_MEASUREMENT_TAG
            )

    def _reset_ancilla_qubits(self, context: UniversalHadamardFaultTolerantContext):
        return self._universal_operations_utilities.reset_ancilla_qubits(context=context)

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalHadamardFaultTolerantContext, None, None]:
        with self._universal_operations_utilities.use_fresh_ancilla_qubits() as base_context:
            yield UniversalHadamardFaultTolerantContext(
                **asdict(base_context),
                data_code_logical_x=self._data_logical_x,
                data_code_logical_z=self._data_logical_z,
            )

    @cached_property
    def _universal_operations_utilities(self) -> UniversalOperationsUtilities:
        num_qubits_for_logical_operations = max(len(self._data_logical_x), len(self._data_logical_z))
        return UniversalOperationsUtilities(num_qubits_for_logical_operations=num_qubits_for_logical_operations)

    @property
    def _data_logical_x(self) -> list[Operation]:
        return self._get_data_logical_operations(gate_label=LogicalGateLabel.X)

    @property
    def _data_logical_z(self) -> list[Operation]:
        return self._get_data_logical_operations(gate_label=LogicalGateLabel.Z)

    def _get_data_logical_operations(self, gate_label: LogicalGateLabel) -> list[Operation]:
        return list(self._code.get_operation_circuit(
            operation=LogicalOperation(gate=gate_label, qubit_index=self._qubit_index)
        ).all_operations())
