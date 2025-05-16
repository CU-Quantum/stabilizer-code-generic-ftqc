from typing import Optional
from uuid import uuid4

import sympy
from cirq import CX, Circuit, CircuitOperation, FrozenCircuit, H, LineQubit, MeasurementKey, R, X, Z

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.globals.fresh_ancillas_pool import FreshAncillasPool


class ShorsRepetitionCode(ErrorCorrectingCode):
    def __init__(self, qubits: Optional[list[LineQubit]] = None,):
        super().__init__(num_data_qubits=9,
                         num_logical_qubits=1,
                         qubits=qubits)
        self._measurer_type = self._configuration.measurer_type

    def encode_logical_qubit(self) -> Circuit:
        # TODO make FT
        outer_qubits_indices = list(range(0, self._num_data_qubits, 3))
        outer_qubits = [self.data_qubits[i] for i in outer_qubits_indices]
        return Circuit(
            [CX(outer_qubits[0], target_qubit) for target_qubit in outer_qubits[1:]],
            [H(target_qubit) for target_qubit in outer_qubits],
            [CX(self.data_qubits[control_qubit_index], self.data_qubits[control_qubit_index + i + 1])
             for control_qubit_index in outer_qubits_indices
             for i in range(2)],
        )

    def _perform_get_operation_circuit(self, operation: LogicalOperation) -> None:
        pass

    def get_error_correction_circuit(self) -> Circuit:
        return Circuit(
            self._correct_bit_flips(),
            self._correct_phase_flips()
        )

    def _correct_bit_flips(self) -> list[Circuit]:
        return [self._correct_bit_flip(block_number=i) for i in range(3)]

    def _correct_bit_flip(self, block_number: int) -> Circuit:
        block_start_index = 3 * block_number
        measurement_keys = [MeasurementKey(f'SHORS_REPETITION_CORRECT_X_{block_number}_{uuid4().hex}') for _ in range(2)]
        measurement_key_symbols = sympy.symbols([key.name for key in measurement_keys])
        syndrome = Circuit(
            self._measurer_type(
                operations=[Z(self.data_qubits[i]) for i in range(block_start_index + j, block_start_index + j + 2)],
                measurement_key=measurement_keys[j]
            ).get_measurement_circuit()
            for j in range(2)
        )
        correction = Circuit(
            X(self.data_qubits[block_start_index + 2]).with_classical_controls(
                sympy.Eq(measurement_key_symbols[0], 0),
                sympy.Eq(measurement_key_symbols[1], 1),
            ),
            X(self.data_qubits[block_start_index]).with_classical_controls(
                sympy.Eq(measurement_key_symbols[0], 1),
                sympy.Eq(measurement_key_symbols[1], 0),
            ),
            X(self.data_qubits[block_start_index + 1]).with_classical_controls(
                sympy.Eq(measurement_key_symbols[0], 1),
                sympy.Eq(measurement_key_symbols[1], 1),
            ),
        )
        circuit = Circuit(
            syndrome,
            correction,
        )
        return circuit

    def _correct_phase_flips(self) -> Circuit:
        measurement_keys = [MeasurementKey(f'SHORS_REPETITION_CORRECT_Z_{uuid4().hex}') for _ in range(2)]
        measurement_key_symbols = sympy.symbols([key.name for key in measurement_keys])
        syndrome = Circuit(
            self._measurer_type(
                operations=[X(self.data_qubits[i]) for i in range(j * 3, j * 3 + 6)],
                measurement_key=measurement_keys[j]
            ).get_measurement_circuit()
            for j in range(2)
        )
        correction = Circuit(
            CircuitOperation(
              FrozenCircuit(
                  [Z(self.data_qubits[i]) for i in range(6, 9)]
              )
            ).with_classical_controls(
                sympy.Eq(measurement_key_symbols[0], 0),
                sympy.Eq(measurement_key_symbols[1], 1),
            ),
            CircuitOperation(
              FrozenCircuit(
                  [Z(self.data_qubits[i]) for i in range(3)]
              )
            ).with_classical_controls(
                sympy.Eq(measurement_key_symbols[0], 1),
                sympy.Eq(measurement_key_symbols[1], 0),
            ),
            CircuitOperation(
              FrozenCircuit(
                  [Z(self.data_qubits[i]) for i in range(3, 6)]
              )
            ).with_classical_controls(
                sympy.Eq(measurement_key_symbols[0], 1),
                sympy.Eq(measurement_key_symbols[1], 1),
            ),
        )
        circuit = Circuit(
            syndrome,
            correction,
        )
        return circuit
