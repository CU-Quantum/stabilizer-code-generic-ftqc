from stim import Circuit
from .surface_code_stim import SurfaceCodeStim


class LatticeSurgery:
    def __init__(self, logical_qubit_1: SurfaceCodeStim, logical_qubit_2: SurfaceCodeStim):
        self.logical_qubit_1 = logical_qubit_1
        self.logical_qubit_2 = logical_qubit_2

    def merge_logical_qubits(self) -> Circuit:
        merged_circuit = Circuit()

        merged_circuit += self.logical_qubit_1._circuit
        merged_circuit += self.logical_qubit_2._circuit

        merged_circuit.append_operation("M", [0, 1, 2, 3, 4, 5, 6, 7])
        merged_circuit.append_from_stim_program_text("TICK")

        return merged_circuit

    def split_logical_qubits(self) -> Circuit:
        split_circuit = Circuit()

        split_circuit.append_operation("M", [0, 1, 2, 3, 4, 5, 6, 7])
        split_circuit.append_from_stim_program_text("TICK")

        return split_circuit

    def logical_cnot(self) -> Circuit:
        cnot_circuit = Circuit()

        cnot_circuit += self.merge_logical_qubits()

        cnot_circuit.append_operation("MX", [0])
        cnot_circuit.append_from_stim_program_text("CX rec[-1] 1")
        cnot_circuit.append_from_stim_program_text("TICK")

        cnot_circuit += self.split_logical_qubits()

        return cnot_circuit
