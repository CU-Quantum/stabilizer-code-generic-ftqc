from typing import Optional

from cirq import CX, Circuit, DensityMatrixSimulator, DensityMatrixTrialResult, H, I, LineQubit, Operation, R, X, Z, \
    kron

from stim_experiments.error_correcting_codes.custom_dataclasses.recovery import Recovery
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalGateLabel, LogicalOperation
from stim_experiments.utilities import KET_ZERO_DENSITY_MATRIX, TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


class FiveQubitCode(ErrorCorrectingCode):
    _generators = [
        [X, Z, Z, X, I],
        [I, X, Z, Z, X],
        [X, I, X, Z, Z],
        [Z, X, I, X, Z],
    ]

    @property
    def _flip_corrections(self):
        return [
            [self.all_qubits[i] for i in (0, 2)],
            [self.all_qubits[i] for i in (0,1,2,3)],
            [self.all_qubits[i] for i in (0,1,3,4)],
            [self.all_qubits[i] for i in (1,4)],
        ]

    def __init__(self,
                 initial_logical_qubit_state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX,
                 qubit_start_index: int = 0,
                 provided_ancilla_qubits: Optional[list[LineQubit]] = None, ):
        super().__init__(initial_logical_qubit_state=initial_logical_qubit_state,
                         num_data_qubits=5,
                         num_ancilla_qubits=4,
                         num_logical_qubits=1,
                         qubit_start_index=qubit_start_index,
                         provided_ancilla_qubits=provided_ancilla_qubits)

    def encode_logical_qubit(self) -> TYPE_STATE_VECTOR_OR_DENSITY_MATRIX:
        initial_state = kron(self._initial_logical_qubit_state, *[KET_ZERO_DENSITY_MATRIX] * (len(self.all_qubits) - 1))
        initialize_with_given_state = Circuit(
            [CX(self.data_qubits[0], data_qubit) for data_qubit in self.data_qubits[1:]],
        )
        initial_state_simulation: DensityMatrixTrialResult = DensityMatrixSimulator().simulate(initialize_with_given_state,
                                                                                               qubit_order=self.all_qubits,
                                                                                               initial_state=initial_state)
        initial_state = initial_state_simulation.final_density_matrix

        circuit = Circuit(
            self._syndrome_circuit,
            [self._get_phase_corrections(ancilla_index=ancilla_index) for ancilla_index in range(self._num_ancilla_qubits)],
            [H(ancilla) for ancilla in self.ancilla_qubits],
        )
        state_and_measurements = self.error_correcting_code_utilities.get_state_after_circuit(circuit=circuit,
                                                                                              qubit_order=self.all_qubits,
                                                                                              initial_state=initial_state,)
        return state_and_measurements.state

    @property
    def _syndrome_circuit(self) -> Circuit:
        return Circuit(
            [H(ancilla) for ancilla in self.ancilla_qubits],
            [gate(self.data_qubits[target_index]).controlled_by(self.ancilla_qubits[generator])
             for generator, gates in enumerate(self._generators) for target_index, gate in enumerate(gates)],
            [H(ancilla) for ancilla in self.ancilla_qubits],
        )

    def _get_phase_corrections(self, ancilla_index: int) -> list[list[Operation]]:
        fix_qubits = self._flip_corrections[ancilla_index]
        return [
            [Z(fix_qubit).controlled_by(self.ancilla_qubits[ancilla_index]) for fix_qubit in fix_qubits],
        ]

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    @property
    def _implemented_operations(self) -> list[LogicalGateLabel]:
        return []

    def get_error_correction_circuit(self) -> Circuit:
        recoveries = [
            Recovery(
                gate=Z,
                qubit_index=0,
                symptom=[1, 0, 1, 0]
            ),
            Recovery(
                gate=Z,
                qubit_index=1,
                symptom=[0, 1, 0, 1]
            ),
            Recovery(
                gate=Z,
                qubit_index=2,
                symptom=[0, 0, 1, 0]
            ),
            Recovery(
                gate=Z,
                qubit_index=3,
                symptom=[1, 0, 0, 1]
            ),
            Recovery(
                gate=Z,
                qubit_index=4,
                symptom=[0, 1, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=0,
                symptom=[0, 0, 0, 1]
            ),
            Recovery(
                gate=X,
                qubit_index=1,
                symptom=[1, 0, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=2,
                symptom=[1, 1, 0, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=3,
                symptom=[0, 1, 1, 0]
            ),
            Recovery(
                gate=X,
                qubit_index=4,
                symptom=[0, 0, 1, 1]
            ),

        ]

        recovery_circuit = Circuit(
            [recovery.gate(self.data_qubits[recovery.qubit_index]).controlled_by(*self.ancilla_qubits, control_values=recovery.symptom)
             for recovery in recoveries]
        )
        return Circuit(
            self._syndrome_circuit,
            recovery_circuit,
            [R(ancilla) for ancilla in self.ancilla_qubits],
        )
