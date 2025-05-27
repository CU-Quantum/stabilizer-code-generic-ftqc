from contextlib import contextmanager
from dataclasses import asdict
from functools import cached_property
from typing import Generator
from uuid import uuid4

import sympy
from cirq import Circuit, CircuitOperation, FrozenCircuit, MeasurementKey, OP_TREE, Operation, \
    R

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.universal_hadamard_fault_tolerant_3x_context import \
    UniversalHadamardFaultTolerant3xContext
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_operations_utilities import \
    UniversalOperationsUtilities
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import \
    CatParityCode
from stim_experiments.error_correcting_codes.universal_hadamard_helper_code.universal_hadamard_helper_code import \
    UniversalHadamardHelperCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class UniversalHadamardFaultTolerant(UniversalHadamard):
    def get_hadamard_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                self._encode_three_cat(context=context),
                self._czx_helpers_to_data(context=context),
                self._ensure_subregister_parity_in_plus(context=context),
                self._measure_out_helper(context=context),
                self._reset_ancilla_qubits(context=context),
            )

    def _encode_three_cat(self, context: UniversalHadamardFaultTolerant3xContext) -> OP_TREE:
        return self._universal_operations_utilities.encode_three_cat(context=context)

    def _czx_helpers_to_data(self, context: UniversalHadamardFaultTolerant3xContext) -> OP_TREE:
        return [
            self._universal_operations_utilities.c_operations_helpers_to_data(
                operations=operations,
                context=context
            )
            for operations in (context.data_code_logical_x, context.data_code_logical_z)
        ]

    def _ensure_subregister_parity_in_plus(self, context: UniversalHadamardFaultTolerant3xContext) -> OP_TREE:
        cat_parity_x, cat_parity_z = (
            list(context.cat_parity_code.get_operation_circuit(
                operation=LogicalOperation(gate=gate, qubit_index=0)
            ).all_operations())
            for gate in (LogicalGateLabel.X, LogicalGateLabel.Z)
        )
        return self._universal_operations_utilities.ensure_cat_parity_code_in_plus(
            observable=cat_parity_x + cat_parity_z + context.data_code_logical_x + context.data_code_logical_z,
            context=context,
            trigger_value=0,
        )

    def _measure_out_helper(self, context: UniversalHadamardFaultTolerant3xContext) -> OP_TREE:
        measurement_key = MeasurementKey(f'UNIVERSAL_HADAMARD_MEASUREMENT_{uuid4().hex}')
        measurement_key_symbol = sympy.symbols(measurement_key.name)
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            return [
                FrozenCircuit(  # cirq seems to be reversing the order of these operations when not frozen
                    self._universal_operations_utilities.measure_out_helper(measurement_key=measurement_key, context=context),
                    encodings_store.get_all_correction_circuits(),
                    CircuitOperation(FrozenCircuit(context.data_code_logical_x)).with_classical_controls(measurement_key),
                    CircuitOperation(FrozenCircuit(context.data_code_logical_z)).with_classical_controls(sympy.Eq(measurement_key_symbol, 0)),
                ),
                encodings_store.get_all_correction_circuits(),
            ]

    def _reset_ancilla_qubits(self, context: UniversalHadamardFaultTolerant3xContext):
        return self._universal_operations_utilities.reset_ancilla_qubits(context=context)

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalHadamardFaultTolerant3xContext, None, None]:
        with self._universal_operations_utilities.use_fresh_ancilla_qubits() as base_context:
            yield UniversalHadamardFaultTolerant3xContext(
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
