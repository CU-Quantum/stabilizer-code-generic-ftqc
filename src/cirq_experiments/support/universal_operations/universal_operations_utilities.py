from contextlib import contextmanager
from typing import Generator

from cirq import CircuitOperation, FrozenCircuit, MeasurementKey, OP_TREE, Operation, R, TaggedOperation

from cirq_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from cirq_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from cirq_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext
from cirq_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode
from cirq_experiments.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from cirq_experiments.support.measurer.measurer import Measurer
from cirq_experiments.error_correcting_codes.generalized_shor_code_hadamard.generalized_shor_code_hadamard import \
    GeneralizedShorCodeHadamard
from cirq_experiments.error_correcting_codes.generalized_shor_code.generalized_shor_code import GeneralizedShorCode
from cirq_experiments.globals.active_encodings_store import ActiveEncodingsStore
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


FINAL_C_FLIP_CORRECTION_TAG = 'FINAL_C_FLIP_CORRECTION'


class UniversalOperationsUtilities:
    def __init__(self, num_qubits_for_logical_operations: int):
        self._num_qubits_for_logical_operations = num_qubits_for_logical_operations

    @staticmethod
    def encode_multiple_cat(context: UniversalOperationsContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.multiple_cat_code]) as encodings_store:
            return [
                context.multiple_cat_code.encode_logical_qubit(),
                encodings_store.get_all_correction_circuits()
            ]

    @staticmethod
    def c_operations_helpers_to_data(operations: list[Operation],
                                     context: UniversalOperationsContext,
                                     target_code: StabilizerCode) -> list[OP_TREE]:
        with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
            return [
                [
                    ControlledSingleQubitGatesApplier(operations=operations, controls=subregister[:len(operations)]).get_circuit(),
                    encodings_store.get_all_correction_circuits(
                        additional_correction_circuits=[
                            context.multiple_cat_code.get_modified_stabilizers_error_correction_circuit(
                                subregister_index=i,
                                target_operations=operations,
                                target_code=target_code
                            )
                        ]
                    ),
                ]
                for i, subregister in enumerate(context.multiple_cat_code.subregisters)
            ]

    # @staticmethod
    # def fix_sign_flip_after_subregister_controlled_flips(
    #         observable: list[Operation],
    #         context: UniversalOperationsContext,
    #         measurement_trigger: int = 1
    # ):
    #     measurer_type = ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
    #     measurement_key = MeasurementKey(f'FINAL_C_FLIP_CORRECTION_MEASUREMENT_KEY_{uuid4().hex}')
    #     measurement_symbol = sympy.symbols(measurement_key.name)
    #
    #     with ActiveEncodingsStore(additional_tracked_encodings=[context.cat_parity_code]) as encodings_store:
    #         z_on_gscx = context.cat_parity_code.get_operation_circuit(
    #             operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0))
    #         return TaggedOperation(
    #             CircuitOperation(
    #                 FrozenCircuit(
    #                     [
    #                         encodings_store.get_all_correction_circuits(),
    #                         measurer_type(observables=[observable],
    #                                       measurement_keys=[measurement_key]).get_measurement_circuit(),
    #                         encodings_store.get_all_correction_circuits(),
    #                         CircuitOperation(
    #                             FrozenCircuit(z_on_gscx),
    #                         ).with_classical_controls(sympy.Eq(measurement_symbol, measurement_trigger)),
    #                         encodings_store.get_all_correction_circuits(),
    #                     ]
    #                 )
    #             ),
    #             FINAL_C_FLIP_CORRECTION_TAG
    #         )

    def measure_out_helper(self, measurement_key: MeasurementKey, context: UniversalOperationsContext) -> OP_TREE:
        logical_z = list(context.multiple_cat_code.get_operation_circuit(
            operation=LogicalOperation(gate=LogicalGateLabel.Z, qubit_index=0)
        ).all_operations())
        return self._measurer_type(observables=[logical_z], measurement_keys=[measurement_key]).get_measurement_circuit()

    @staticmethod
    def reset_ancilla_qubits(context: UniversalOperationsContext) -> OP_TREE:
        return TaggedOperation(
            CircuitOperation(
                FrozenCircuit(
                    R(qubit) for qubit in context.ancilla_qubits
                ),
            ),
            f'RESET_HELPER_QUBITS_{context.__class__.__name__}'
        )

    @contextmanager
    def use_fresh_ancilla_qubits(self) -> Generator[UniversalOperationsContext, None, None]:
        minimum_qubits_per_subregister = 3
        num_qubits_per_subregister = max(minimum_qubits_per_subregister, self._num_qubits_for_logical_operations)
        num_qubits_for_subregister_parity_code = num_qubits_per_subregister * self._num_cat_states
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=num_qubits_for_subregister_parity_code) as ancilla_qubits:
            multiple_cat_code = GeneralizedShorCode(num_cats=self._num_cat_states,
                                                    num_qubits_per_cat=self._num_qubits_for_logical_operations,
                                                    qubits=ancilla_qubits)
            cat_parity_code = GeneralizedShorCodeHadamard(num_cats=self._num_cat_states,
                                                          num_qubits_per_cat=self._num_qubits_for_logical_operations,
                                                          qubits=ancilla_qubits)
            yield UniversalOperationsContext(
                ancilla_qubits=ancilla_qubits,
                cat_parity_code=cat_parity_code,
                multiple_cat_code=multiple_cat_code,
            )

    @property
    def _measurer_type(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _num_cat_states(self) -> int:
        return self._configuration.num_cat_states

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
