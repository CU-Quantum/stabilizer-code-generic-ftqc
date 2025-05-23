from abc import ABC, abstractmethod

from cirq import Circuit

from stim_experiments.custom_dataclasses.simulation_operation import LogicalEncodingIndex, TargetEncoding


class UniversalControlledOperation(ABC):
    def __init__(self, control: LogicalEncodingIndex, target: TargetEncoding):
        self._control = control
        self._target = target

    @abstractmethod
    def get_controlled_operation_circuit(self) -> Circuit:
        pass
