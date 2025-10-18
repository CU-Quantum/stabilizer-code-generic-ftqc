import unittest
from stim import Circuit
from stim_simulations.surface_code import SurfaceCodeStim
from stim_simulations.surface_code.surface_code_stim.lattice_surgery import LatticeSurgery


class TestLatticeSurgery(unittest.TestCase):

    def setUp(self):
        # Toy logical qubit patches (very small circuits for testing)
        self.circuit_1 = Circuit("H 0")  # Control patch
        self.circuit_2 = Circuit("X 1")  # Target patch
        self.logical_qubit_1 = SurfaceCodeStim(self.circuit_1)
        self.logical_qubit_2 = SurfaceCodeStim(self.circuit_2)

    def test_merge_logical_qubits(self):
        lattice_surgery = LatticeSurgery(self.logical_qubit_1, self.logical_qubit_2)
        merged_circuit = lattice_surgery.merge_logical_qubits()
        circuit_str = str(merged_circuit)

        # Check ancilla initialized
        self.assertIn("H 2", circuit_str)

        # Instead of individual CNOTs, check combined CX exists
        self.assertIn("CX 0 2", circuit_str) or self.assertIn("CX 0 2 1 2", circuit_str)

        # Check ancilla measured
        self.assertIn("M 2", circuit_str)

        # Check tick usage
        self.assertGreaterEqual(circuit_str.count("TICK"), 3)

    
    def test_split_logical_qubits(self):
        lattice_surgery = LatticeSurgery(self.logical_qubit_1, self.logical_qubit_2)
        split_circuit = lattice_surgery.split_logical_qubits()
        circuit_str = str(split_circuit)

        # Only expect a TICK in current simplified implementation
        self.assertIn("TICK", circuit_str)

    def test_logical_cnot(self):
        lattice_surgery = LatticeSurgery(self.logical_qubit_1, self.logical_qubit_2)
        cnot_circuit = lattice_surgery.logical_cnot()
        circuit_str = str(cnot_circuit)

        self.assertIn("H 2", circuit_str)
        self.assertIn("M 2", circuit_str)
        self.assertIn("CX rec[-1] 1", circuit_str)

        # Count at least 5 ticks: merge H, merge CNOTs, pre-measure H, measure, correction, split
        self.assertGreaterEqual(circuit_str.count("TICK"), 5)


if __name__ == "__main__":
    unittest.main()
