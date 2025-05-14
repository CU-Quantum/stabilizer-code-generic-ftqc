from cirq import Circuit, H, M, R

from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.utilities import FreshAncillasPool
from stim_experiments.error_correcting_codes.support.operations_applier.operations_applier_using_single_qubit_hadamard_control import \
    OperationsApplierUsingSingleQubitHadamardControl


class MeasurerWithSingleQubit(Measurer):
    def get_measurement_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=1) as ancilla_qubits:
            measuring_qubit = ancilla_qubits[0]
            return Circuit(
                H(measuring_qubit),
                OperationsApplierUsingSingleQubitHadamardControl(
                    operations=[
                        operation.controlled_by(measuring_qubit)
                        for operation in self._operations
                    ],
                    measurement_qubit=measuring_qubit,
                ).get_application_circuit(),
                H(measuring_qubit),
                M(measuring_qubit, key=self._measurement_key),
                R(measuring_qubit)
            )
