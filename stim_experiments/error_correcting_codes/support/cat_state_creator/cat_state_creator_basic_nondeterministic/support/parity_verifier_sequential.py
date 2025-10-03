from cirq import Circuit, M, R, X

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_nondeterministic.support.parity_verifier import \
    ParityVerifier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class ParityVerifierSequential(ParityVerifier):
    def validate_parity(self) -> Circuit:
        if self._num_target_qubits <= 1:
            return Circuit()
        operations = []
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancillas:
            verifier_ancilla = ancillas[0]
            for i in range(self._num_target_qubits - 1):
                operations.append(
                    [
                        R(verifier_ancilla),
                        X(verifier_ancilla).controlled_by(self._target_qubits[i]),
                        X(verifier_ancilla).controlled_by(self._target_qubits[i + 1]),
                        M(verifier_ancilla, key=self._measurement_key),
                    ]
                )
        return Circuit(operations)

    @property
    def _num_target_qubits(self) -> int:
        return len(self._target_qubits)

    @property
    def _measurer(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
