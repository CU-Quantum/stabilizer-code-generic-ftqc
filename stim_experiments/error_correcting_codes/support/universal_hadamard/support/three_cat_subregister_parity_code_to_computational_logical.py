from contextlib import contextmanager
from typing import Generator, Optional

from cirq import Circuit, OP_TREE, R, X

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_hadamard.support.encode_to_desired_code import \
    EncodeToDesiredCode
from stim_experiments.error_correcting_codes.support.universal_hadamard.support.three_cat_subregister_parity_code_to_computational_logical_context import \
    ThreeCatSubregisterParityCodeToComputationalLogicalContext
from stim_experiments.error_correcting_codes.three_cat_code.three_cat_code import ThreeCatCode
from stim_experiments.error_correcting_codes.three_cat_subregister_parity_code.three_cat_subregister_parity_code import \
    ThreeCatSubregisterParityCode
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.utilities.utilities import cx_sequentially_further_qubits_from_first


class ThreeCatSubregisterParityCodeToComputationalLogical:
    def __init__(self,
                 three_cat_subregister_parity_code: ThreeCatSubregisterParityCode,
                 desired_encoding: ErrorCorrectingCode,
                 ):
        self._three_cat_subregister_parity_code = three_cat_subregister_parity_code
        self._desired_encoding = desired_encoding

        self._circuit = Circuit()
        self._context: Optional[ThreeCatSubregisterParityCodeToComputationalLogicalContext] = None
        self._encodings_store: Optional[ActiveEncodingsStore] = None

    def get_circuit(self) -> Circuit:
        with self._use_fresh_ancilla_qubits() as context:
            with ActiveEncodingsStore() as encoding_store:
                self._context = context
                self._encodings_store = encoding_store

                return Circuit(
                    self._encode_helper_registers(),
                    self._cx_data_to_helpers(),
                    self._create_cat_states_on_all_subregisters(),
                    self._encode_to_desired_code(),
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
        return [
            EncodeToDesiredCode(desired_encoding=self._desired_encoding,
                                context=self._context,
                                encodings_store=self._encodings_store).get_encoding_circuit()
        ]

    @contextmanager
    def _use_fresh_ancilla_qubits(self) -> Generator[
        ThreeCatSubregisterParityCodeToComputationalLogicalContext, None, None]:
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
            yield ThreeCatSubregisterParityCodeToComputationalLogicalContext(
                ancilla_qubits=ancilla_qubits,
                additional_universal_hadamard_codes=additional_universal_hadamard_codes,
                all_universal_hadamard_codes=[self._three_cat_subregister_parity_code] + additional_universal_hadamard_codes,
                helper_3cat=helper_3cat,
            )

    def _reset_ancilla_qubits(self):
        return [R(qubit) for qubit in self._context.ancilla_qubits]

    @property
    def _cat_state_creator_type(self) -> type[CatStateCreator]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().cat_state_creator_type

    @property
    def _measurer_type(self) -> type[Measurer]:
        return ConfigurationErrorCorrectingCodeManager().get_configuration().measurer_type
