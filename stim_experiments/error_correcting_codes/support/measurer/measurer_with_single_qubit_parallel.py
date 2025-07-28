from cirq import Circuit, M, ResetChannel

from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_single_qubit_hadamard_control import \
    OperationsApplierUsingSingleQubitHadamardControl
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class MeasurerWithSingleQubitParallel(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        if not self._observables:
            return Circuit()
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._observables)) as ancilla_qubits:
            operations = [
                ResetChannel().on_each(*ancilla_qubits),
                [
                    OperationsApplierUsingSingleQubitHadamardControl(
                        operations=operations,
                        measurement_qubit=self._measurement_keys[i],
                    ).get_application_circuit()
                    for i, (operations, measurement_key) in enumerate(zip(self._observables, self._measurement_keys))
                ],
                [M(qubit, key=self._measurement_keys[i]) for i, qubit in enumerate(ancilla_qubits)],
                ResetChannel().on_each(*ancilla_qubits),
            ]
            return Circuit(operations)
