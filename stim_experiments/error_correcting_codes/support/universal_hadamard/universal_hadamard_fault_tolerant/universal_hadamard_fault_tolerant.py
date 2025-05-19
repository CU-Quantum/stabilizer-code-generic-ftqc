from contextlib import contextmanager
from dataclasses import dataclass
from typing import Generator
from uuid import uuid4

from cirq import Circuit, CircuitOperation, FrozenCircuit, KeyCondition, LineQubit, MeasurementKey, OP_TREE, Operation, \
    R, SWAP

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.support.three_cat_subregister_parity_code_to_computational_logical import \
    ThreeCatSubregisterParityCodeToComputationalLogical
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard import UniversalHadamard
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


@dataclass
class UniversalHadamardFaultTolerantContext:
    ancilla_qubits: list[LineQubit]
    encodings_store: ActiveEncodingsStore
    new_encoding: ErrorCorrectingCode
    three_cat: ThreeCatCode
    to_computational_logical: ThreeCatSubregisterParityCodeToComputationalLogical
    logical_x: list[Operation]
    logical_z: list[Operation]


class UniversalHadamardFaultTolerant(UniversalHadamard):
    # TODO allow multi qubit encodings
    def get_hadamard_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                context.three_cat.encode_logical_qubit(),
                self._cx_helpers_to_data(context=context),
                context.to_computational_logical.get_circuit(),
                self._measure_out_original_data(context=context),
                self._reset_ancilla_qubits(context=context),
            )

    def _cx_helpers_to_data(self, context: UniversalHadamardFaultTolerantContext) -> OP_TREE:
        repetition_codes = [RepetitionCode(num_qubits=len(subregister), qubits=subregister)
                            for subregister in context.three_cat.subregisters]
        context.encodings_store.replace_tracked_encodings_with(encodings=repetition_codes)
        return [
            [
                ControlledSingleQubitGatesApplier(operations=context.logical_x,
                                                  controls=subregister[:len(context.logical_x)]).get_circuit(),
                context.encodings_store.get_all_correction_circuits(),
            ]
            for subregister in context.three_cat.subregisters
        ]

    def _measure_out_original_data(self, context: UniversalHadamardFaultTolerantContext) -> OP_TREE:
        measurement_key = MeasurementKey(f'UNIVERSAL_HADAMARD_MEASUREMENT_{uuid4().hex}')
        context.encodings_store.replace_tracked_encodings_with(encodings=[])
        return [
            FrozenCircuit(  # cirq seems to be reversing the order of these operations when not frozen
                self._measurer_type(operations=context.logical_z, measurement_key=measurement_key).get_measurement_circuit(),
                CircuitOperation(
                    context.new_encoding.get_operation_circuit(LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=self._qubit_index)).freeze()
                ).with_classical_controls(KeyCondition(key=measurement_key)),
            ),
            [R(qubit) for qubit in self._code.data_qubits],
            [
                SWAP(context.new_encoding.data_qubits[i], self._code.data_qubits[i])
                for i in range(len(context.new_encoding.data_qubits))
            ],
            context.encodings_store.get_all_correction_circuits(),
        ]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[UniversalHadamardFaultTolerantContext, None, None]:
        num_qubits_in_desired_encoding = len(self._code.data_qubits)
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=3 * num_qubits_in_desired_encoding) as ancilla_qubits:
            with ActiveEncodingsStore() as encoding_store:
                three_cat_subregister_parity_code = ThreeCatSubregisterParityCode(
                    num_qubits_in_cat_state=num_qubits_in_desired_encoding,
                    qubits=ancilla_qubits
                )
                logical_x, logical_z = (
                    list(self._code.get_operation_circuit(
                        operation=LogicalOperation(gate=gate, qubit_index=self._qubit_index)
                    ).all_operations())
                    for gate in (LogicalGateLabel.X, LogicalGateLabel.Z)
                )
                yield UniversalHadamardFaultTolerantContext(
                    ancilla_qubits=ancilla_qubits,
                    encodings_store=encoding_store,
                    new_encoding=self._code.create_new(qubits=three_cat_subregister_parity_code.subregisters[0]),
                    three_cat=ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_desired_encoding, qubits=ancilla_qubits),
                    to_computational_logical=ThreeCatSubregisterParityCodeToComputationalLogical(
                        three_cat_subregister_parity_code=three_cat_subregister_parity_code,
                        desired_encoding=self._code
                    ),
                    logical_x=logical_x,
                    logical_z=logical_z,
                )

    @staticmethod
    def _reset_ancilla_qubits(context: UniversalHadamardFaultTolerantContext):
        return [R(qubit) for qubit in context.ancilla_qubits]

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
