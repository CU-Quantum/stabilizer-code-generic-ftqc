from cirq import Circuit, M

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
                [
                    OperationsApplierUsingSingleQubitHadamardControl(
                        operations=operations,
                        measurement_qubit=measurement_qubit,
                    ).get_application_circuit()
                    for operations, measurement_qubit in zip(self._observables, ancilla_qubits)
                ],
                [M(qubit, key=self._measurement_keys[i]) for i, qubit in enumerate(ancilla_qubits)],
            ]
            return Circuit(operations)
