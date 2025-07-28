from typing import List

from cirq import Circuit, LineQubit, M, MeasurementKey, R, X, Z

from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class ParityVerifier:
    def __init__(self, target_qubits: List[LineQubit], measurement_key: MeasurementKey):
        self._target_qubits = target_qubits
        self._measurement_key = measurement_key

    def validate_parity(self) -> Circuit:
        operations = []
        with FreshAncillasPool().parallel(ConfigurationErrorCorrectingCodeManager().get_configuration().parallel):
            for i in range(self._num_target_qubits - 1):
                with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancillas:
                    verifier_ancilla = ancillas[0]
                    operations.append(
                        [
                            R(verifier_ancilla),
                            X(verifier_ancilla).controlled_by(self._target_qubits[i]),
                            X(verifier_ancilla).controlled_by(self._target_qubits[i + 1]),
                            M(verifier_ancilla, key=self._measurement_key),
                            R(verifier_ancilla)
                        ]
                    )
        return Circuit(operations)

    @property
    def _num_target_qubits(self) -> int:
        return len(self._target_qubits)

    @property
    def _parallel(self) -> bool:
        return self._configuration.parallel

    @property
    def _measurer(self) -> type[Measurer]:
        return self._configuration.measurer_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
