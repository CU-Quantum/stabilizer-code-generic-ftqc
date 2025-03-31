from stim import Circuit


class TestSingleStabilizerDeterminism:
    all_indices = list(range(5))
    data_indices = all_indices[:4]
    stabilizer_index = all_indices[-1]
    top_left_index, top_right_index, bottom_left_index, bottom_right_index = data_indices

    all_indices_str = ' '.join(map(str, all_indices))
    data_indices_str = ' '.join(map(str, data_indices))

    qubit_coords_str = f"""
        QUBIT_COORDS(1,1) {top_left_index}
        QUBIT_COORDS(2,1) {top_right_index}
        QUBIT_COORDS(1,2) {bottom_left_index}
        QUBIT_COORDS(2,2) {bottom_right_index}
        QUBIT_COORDS(1.5,1.5) {stabilizer_index}
        R {' '.join(all_indices_str)}
        """

    x_stabilizer_str = f"""
        H {stabilizer_index}
        CX {stabilizer_index} {top_left_index}
        CX {stabilizer_index} {top_right_index}
        CX {stabilizer_index} {bottom_left_index}
        CX {stabilizer_index} {bottom_right_index}
        H {stabilizer_index}
        """

    z_stabilizer_str = f"""
        CX {top_left_index} {stabilizer_index}
        CX {bottom_left_index} {stabilizer_index}
        CX {top_right_index} {stabilizer_index}
        CX {bottom_right_index} {stabilizer_index}
        """

    def test_single_hadamard_is_not_deterministic(self):
        circuit = Circuit(f"""
            QUBIT_COORDS(1.5,1.5) {self.stabilizer_index}
            R {self.stabilizer_index}

            H {self.stabilizer_index}
            M {self.stabilizer_index}
            """)
        assert not self._is_deterministic(circuit=circuit)

    def test_z_basis_with_x_stabilizer_is_not_deterministic(self):
        circuit = Circuit(f"""
            {self.qubit_coords_str}
            {self.x_stabilizer_str}
            M {self.stabilizer_index}
            """)
        assert not self._is_deterministic(circuit=circuit)

    def test_z_basis_with_z_stabilizer_is_deterministic(self):
        circuit = Circuit(f"""
            {self.qubit_coords_str}
            
            {self.z_stabilizer_str}
            M {self.stabilizer_index}
            """)
        assert self._is_deterministic(circuit=circuit)

    def test_hadamard_basis_with_x_stabilizer_is_deterministic(self):
        circuit = Circuit(f"""
            {self.qubit_coords_str}
            H {' '.join(self.data_indices_str)}

            {self.x_stabilizer_str}
            M {self.stabilizer_index}
            """)
        assert self._is_deterministic(circuit=circuit)

    def test_hadamard_basis_with_z_stabilizer_is_not_deterministic(self):
        circuit = Circuit(f"""
            {self.qubit_coords_str}
            H {' '.join(self.data_indices_str)}
            
            {self.z_stabilizer_str}
            M {self.stabilizer_index}
            """)
        assert not self._is_deterministic(circuit=circuit)

    @staticmethod
    def _is_deterministic(circuit: Circuit) -> bool:
        sampler = circuit.compile_sampler(seed=0)
        measurements = sampler.sample(shots=10).flatten()
        return not any(measurements) or all(measurements)
