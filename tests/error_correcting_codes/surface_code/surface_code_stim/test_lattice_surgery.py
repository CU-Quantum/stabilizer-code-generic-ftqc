import unittest
from stim import Circuit
from stim_experiments.error_correcting_codes.surface_code.surface_code_stim.surface_code_stim  import SurfaceCodeStim
from stim_experiments.error_correcting_codes.surface_code.surface_code_stim.lattice_surgery import LatticeSurgery


class TestLatticeSurgery(unittest.TestCase):

    def setUp(self):
        self.circuit_1 = Circuit("H 0")  # Example initial circuit
        self.circuit_2 = Circuit("X 1")
        self.logical_qubit_1 = SurfaceCodeStim(self.circuit_1)
        self.logical_qubit_2 = SurfaceCodeStim(self.circuit_2)

    def test_merge_logical_qubits(self):
        lattice_surgery = LatticeSurgery(self.logical_qubit_1, self.logical_qubit_2)
        merged_circuit = lattice_surgery.merge_logical_qubits()

        self.assertIn("M 0 1 2 3 4 5 6 7", merged_circuit.__str__())
        self.assertIn("TICK", merged_circuit.__str__())

    def test_split_logical_qubits(self):
        lattice_surgery = LatticeSurgery(self.logical_qubit_1, self.logical_qubit_2)
        split_circuit = lattice_surgery.split_logical_qubits()

        self.assertIn("M 0 1 2 3 4 5 6 7", split_circuit.__str__())
        self.assertIn("TICK", split_circuit.__str__())

    def test_logical_cnot(self):
        lattice_surgery = LatticeSurgery(self.logical_qubit_1, self.logical_qubit_2)
        cnot_circuit = lattice_surgery.logical_cnot()

        circuit_str = cnot_circuit.__str__()
        self.assertIn("MX 0", circuit_str)
        self.assertIn("CX rec[-1] 1", circuit_str)
        self.assertEqual(circuit_str.count("TICK"), 3)


if __name__ == "__main__":
    unittest.main()
