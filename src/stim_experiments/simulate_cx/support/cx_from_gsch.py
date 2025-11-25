from stim import Circuit

from stim_experiments.simulate_cx.support.stabilizer_code_utilities import StabilizerCodeUtilities


class CxFromGsch:
    def __init__(self,
                 control_qubit_indices: list[int],
                 target_code_utilities: StabilizerCodeUtilities,):
        self._control_qubit_indices = control_qubit_indices
        self._target_code_utilities = target_code_utilities

    def perform_cx(self, ):
        circuit = Circuit()
        x_observable = self._target_code_utilities.x_observable
        self._target_code_utilities.apply_stabilizer(stabilizer=x_observable, circuit=circuit, ancillas=self._control_qubit_indices)
        return circuit
