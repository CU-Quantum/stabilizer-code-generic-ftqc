import pytest
from cirq import Circuit, LineQubit, OP_TREE, Operation, Y

from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.custom_dataclasses.universal_operations_context import UniversalOperationsContext
from stim_experiments.error_correcting_codes.cat_parity_code.cat_parity_code import CatParityCode
from stim_experiments.error_correcting_codes.multiple_cat_code.multiple_cat_code import MultipleCatCode
from stim_experiments.error_correcting_codes.support.controlled_single_qubit_gates_applier import \
    ControlledSingleQubitGatesApplier
from stim_experiments.globals.active_encodings_store import ActiveEncodingsStore
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool
from stim_experiments.simulations.error_correcting_simulator import ErrorCorrectingSimulatorStateVector
from stim_experiments.utilities.utilities import states_are_equal
from tests.utilities_for_tests import set_configuration_to_reduce_ancilla_qubits, set_seed


def control_from_gpch(operations: list[Operation], context: UniversalOperationsContext) -> list[OP_TREE]:
    with ActiveEncodingsStore(additional_tracked_encodings=[]) as encodings_store:
        return [
            [
                ControlledSingleQubitGatesApplier(operations=operations, controls=subregister[:len(operations)]).get_circuit(),
                encodings_store.get_all_correction_circuits(
                    additional_correction_circuits=[
                        context.cat_parity_code.get_modified_stabilizers_error_correction_circuit(
                            subregister_control_index=i,
                            target_operations=operations,
                        )
                    ]
                ),
            ]
            for i, subregister in enumerate(context.multiple_cat_code.subregisters)
        ]


class TestModifiedStabilizers:
    @pytest.fixture(autouse=True)
    def _setup(self):
        set_seed(0)
        set_configuration_to_reduce_ancilla_qubits()

    def test_no_errors(self):
        error_circuit = Circuit()
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def test_error_on_first_qubit_of_third_cat_state_of_ghch_3_3(self):
        error_circuit = Circuit(
            Y(LineQubit(6))
        )
        assert self._correct_with_modified_stabilizers(error_circuit=error_circuit)

    def _correct_with_modified_stabilizers(self, error_circuit: Circuit):
        qubits = LineQubit.range(18)
        FreshAncillasPool().set_first_ancilla_num(first_ancilla_num=len(qubits))
        simulator = ErrorCorrectingSimulatorStateVector()

        control = CatParityCode(num_cats=3, num_qubits_per_cat=3, qubits=qubits[:9])
        target = MultipleCatCode(num_cats=3, num_qubits_per_cat=3, qubits=qubits[9:])
        x_operation_target = target.get_operation_circuit(operation=LogicalOperation(gate=LogicalGateLabel.X, qubit_index=0))

        encoding_circuit = Circuit(
            control.encode_logical_qubit(),
            target.encode_logical_qubit(),
        )
        initial_state = simulator.run_simulation(encoding_circuit, num_data_qubits=len(qubits))

        target_operations = list(x_operation_target.all_operations())
        correction_circuit = control_from_gpch(
            operations=target_operations,
            context=UniversalOperationsContext(
                ancilla_qubits=[],
                cat_parity_code=control,
                multiple_cat_code=MultipleCatCode(
                    num_cats=len(control.subregisters),
                    num_qubits_per_cat=len(control.subregisters[0]),
                    qubits=control.data_qubits),
            )
        )

        full_circuit = Circuit(
            encoding_circuit,
            error_circuit,
            correction_circuit,
        )
        result = simulator.run_simulation(full_circuit, num_data_qubits=len(qubits))
        return states_are_equal(result.state, initial_state.state)
