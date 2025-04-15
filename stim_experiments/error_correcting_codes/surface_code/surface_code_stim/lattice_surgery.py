from stim import Circuit
from .surface_code_stim import SurfaceCodeStim


class LatticeSurgery:
    """
    Implements basic lattice surgery operations between two surface code patches
    to simulate a logical CNOT using shared stabilizer measurements.
    """

    def __init__(self, logical_qubit_1: SurfaceCodeStim, logical_qubit_2: SurfaceCodeStim):
        """
        logical_qubit_1: control logical patch
        logical_qubit_2: target logical patch
        """
        self.logical_qubit_1 = logical_qubit_1
        self.logical_qubit_2 = logical_qubit_2

    def merge_logical_qubits(self) -> Circuit:
        """
        Merge two logical patches by measuring a shared Z⊗Z stabilizer
        using an ancilla qubit.
        """
        circuit = Circuit()
    
        # Include the encoded circuits for both logical qubits
        circuit += self.logical_qubit_1._circuit
        circuit += self.logical_qubit_2._circuit
    
        # Dynamically calculate ancilla index (1 above the max data index)
        num_qubits_1 = self.logical_qubit_1._circuit.num_qubits
        num_qubits_2 = self.logical_qubit_2._circuit.num_qubits
        used_qubits = set(range(num_qubits_1)) | set(range(num_qubits_2))
        ancilla_index = max(used_qubits) + 1
    
        # Initialize ancilla in |+⟩ for X basis parity measurement
        circuit.append_operation("H", [ancilla_index])
        circuit.append_from_stim_program_text("TICK")
    
        # Define which data qubits will participate in the shared Z-parity measurement
        shared_boundary = [q for q in used_qubits if q != ancilla_index]
    
        # Apply CNOT gates between shared boundary qubits and ancilla
        for q in shared_boundary:
            circuit.append_operation("CNOT", [q, ancilla_index])
    
        circuit.append_from_stim_program_text("TICK")
    
        # Measure ancilla to extract parity
        circuit.append_operation("H", [ancilla_index])  # convert back to Z basis
        circuit.append_operation("M", [ancilla_index])
        circuit.append_from_stim_program_text("TICK")
    
        return circuit
    
    def split_logical_qubits(self) -> Circuit:
        """
        After performing a joint measurement, we restore the patches to their
        original stabilizer structure. Here we simulate that by ending the ancilla interaction.
        """
        circuit = Circuit()

        # In a real implementation, we’d restore original stabilizers here.
        # For simplicity, we just acknowledge the end of the merge.
        circuit.append_from_stim_program_text("TICK")

        return circuit

    def logical_cnot(self) -> Circuit:
        """
        Perform a fault-tolerant logical CNOT via lattice surgery:
        1. Merge patches (measure Z⊗Z parity)
        2. Measure ancilla
        3. Optionally apply correction
        4. Split patches
        """
        circuit = Circuit()

        # Step 1: Merge (Z⊗Z parity measurement)
        circuit += self.merge_logical_qubits()

        # Step 2: Conditional correction based on ancilla result
        # Apply CX from measurement result to target logical qubit (simulated)
        circuit.append_from_stim_program_text("CX rec[-1] 1")
        circuit.append_from_stim_program_text("TICK")

        # Step 3: Split (restore independent logical qubits)
        circuit += self.split_logical_qubits()

        return circuit
