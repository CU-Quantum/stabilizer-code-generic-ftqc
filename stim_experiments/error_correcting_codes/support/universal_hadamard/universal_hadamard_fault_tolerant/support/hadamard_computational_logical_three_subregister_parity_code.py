from contextlib import contextmanager
from typing import Generator, Optional

from cirq import Circuit, OP_TREE, R, X

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.repetition_code.repetition_code import RepetitionCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.support.encode_to_desired_code import \
    EncodeToDesiredCode
from stim_experiments.error_correcting_codes.support.universal_hadamard.universal_hadamard_fault_tolerant.support.hadamard_computational_logical_three_subregister_parity_code_context import \
    HadamardComputationalLogicalThreeSubregisterParityCodeContext
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import cx_sequentially_further_qubits_from_first


class HadamardComputationalLogicalThreeSubregisterParityCode:
    def __init__(self, three_cat_subregister_parity_code: ThreeCatSubregisterParityCode,):
        self._three_cat_subregister_parity_code = three_cat_subregister_parity_code
        self._circuit = Circuit()

    def get_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            return Circuit(
                self._encode_helper_registers(context=context),
                self._cx_original_to_helpers(context=context),
                self._create_cat_states_on_all_subregisters(context=context),
                self._encode_to_desired_code(context=context),
                self._reset_ancilla_qubits(context=context),
            )

    def _encode_helper_registers(self, context: HadamardComputationalLogicalThreeSubregisterParityCodeContext) -> OP_TREE:
        codes = context.additional_universal_hadamard_codes
        with ActiveEncodingsStore(additional_tracked_encodings=codes) as encodings_store:
            return [
                [code.encode_logical_qubit() for code in codes],
                encodings_store.get_all_correction_circuits(),
            ]

    def _cx_original_to_helpers(self, context: HadamardComputationalLogicalThreeSubregisterParityCodeContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=context.all_universal_hadamard_codes) as encodings_store:
            return [
                [
                    self._cx_original_to_helper(code=code),
                    encodings_store.get_all_correction_circuits(),
                ] for code in context.additional_universal_hadamard_codes
            ]

    def _cx_original_to_helper(self, code: ThreeCatSubregisterParityCode) -> OP_TREE:
        return [X(target_qubit).controlled_by(control_qubit)
                for target_qubit, control_qubit in zip(code.data_qubits, self._three_cat_subregister_parity_code.data_qubits)]

    def _create_cat_states_on_all_subregisters(self, context: HadamardComputationalLogicalThreeSubregisterParityCodeContext) -> OP_TREE:
        with ActiveEncodingsStore(additional_tracked_encodings=[context.helper_3cat]) as encodings_store:
            return [
                [
                    [
                        cx_sequentially_further_qubits_from_first(qubits=subregister),
                        self._cat_state_creator_type(qubit_register=subregister).get_cat_state_circuit(),
                    ] for code in context.all_universal_hadamard_codes for subregister in code.subregisters
                ],
                encodings_store.get_all_correction_circuits(),
            ]

    def _encode_to_desired_code(self, context: HadamardComputationalLogicalThreeSubregisterParityCodeContext) -> OP_TREE:
        return EncodeToDesiredCode(context=context).get_encoding_circuit()

    def _reset_ancilla_qubits(self, context: HadamardComputationalLogicalThreeSubregisterParityCodeContext):
        return [R(qubit) for qubit in context.ancilla_qubits]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[
        HadamardComputationalLogicalThreeSubregisterParityCodeContext, None, None]:
        num_additional_parity_to_computational_codes = 2
        num_qubits_in_universal_hadamard_code = len(self._three_cat_subregister_parity_code.data_qubits)
        num_ancilla_qubits = num_qubits_in_universal_hadamard_code * num_additional_parity_to_computational_codes
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=num_ancilla_qubits) as ancilla_qubits:
            additional_universal_hadamard_codes = [
                self._three_cat_subregister_parity_code.create_new(
                    qubits=ancilla_qubits[i * num_qubits_in_universal_hadamard_code:(i + 1) * num_qubits_in_universal_hadamard_code]
                )
                for i in range(num_additional_parity_to_computational_codes)
            ]
            helper_3cat = ThreeCatCode(num_qubits_in_cat_state=num_qubits_in_universal_hadamard_code,
                                       qubits=self._three_cat_subregister_parity_code.data_qubits + ancilla_qubits)
            yield HadamardComputationalLogicalThreeSubregisterParityCodeContext(
                ancilla_qubits=ancilla_qubits,
                additional_universal_hadamard_codes=additional_universal_hadamard_codes,
                all_universal_hadamard_codes=[self._three_cat_subregister_parity_code] + additional_universal_hadamard_codes,
                helper_3cat=helper_3cat,
            )

    @property
    def _cat_state_creator_type(self) -> type[CatStateCreator]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().cat_state_creator_type

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
