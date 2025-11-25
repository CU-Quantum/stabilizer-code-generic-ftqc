from cirq import Circuit

from cirq_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from cirq_experiments.support.cat_state_creator.cat_state_creator import CatStateCreator
from cirq_experiments.support.cat_state_creator.cat_state_creator_basic_nondeterministic.cat_state_creator_basic_nondeterministic import \
    CatStateCreatorBasicNondeterministic
from cirq_experiments.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from cirq_experiments.support.operations_applier.operations_applier import OperationsApplier
from cirq_experiments.globals.error_correcting_code_configuration import ConfigurationErrorCorrectingCodeManager
from cirq_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class OperationsApplierUsingCatStateControl(OperationsApplier):
    def _perform_get_application_circuit(self) -> Circuit:
        with FreshAncillasPool().use_fresh_ancillas(num_ancillas=len(self._operations) - 1) as ancilla_qubits:
            control_qubits = [self._measurement_qubit] + ancilla_qubits
            cat_state_creator = CatStateCreatorBasicNondeterministic(qubit_register=control_qubits)
            return Circuit(
                cat_state_creator.get_cat_state_circuit(),
                ControlledSingleQubitGatesApplier(operations=self._operations, controls=control_qubits).get_circuit(),
                cat_state_creator.decode_state(),
            )

    @property
    def _cat_state_creator_type(self) -> type[CatStateCreator]:
        return self._configuration.cat_state_creator_type

    @property
    def _configuration(self) -> ConfigurationErrorCorrectingCode:
        return ConfigurationErrorCorrectingCodeManager().get_configuration()
