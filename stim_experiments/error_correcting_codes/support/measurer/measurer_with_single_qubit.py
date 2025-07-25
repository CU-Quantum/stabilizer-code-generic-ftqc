from cirq import Circuit, M, R

from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_single_qubit_hadamard_control import \
    OperationsApplierUsingSingleQubitHadamardControl
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class MeasurerWithSingleQubit(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        if not self._operations:
            return Circuit()
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            measuring_qubit = ancilla_qubits[0]
            operations = [
                R(measuring_qubit),
                OperationsApplierUsingSingleQubitHadamardControl(
                    operations=self._operations,
                    measurement_qubit=measuring_qubit,
                ).get_application_circuit(),
                M(measuring_qubit, key=self._measurement_key),
                R(measuring_qubit)
            ]
            return Circuit(operations)
