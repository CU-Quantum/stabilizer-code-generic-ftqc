from abc import ABC, abstractmethod

from cirq import LineQubit, Operation

from stim_experiments.custom_dataclasses.cat_state_flag_info import CatStateFlagInfo


class FlagMeasurer(ABC):
    def __init__(self,
                 qubit_register: list[LineQubit],
                 parity_check_infos: list[CatStateFlagInfo],
                 measurement_key: str):
        self._qubit_register = qubit_register
        self._parity_check_infos = parity_check_infos
        self._measurement_key = measurement_key

    @abstractmethod
    def measure_flags(self) -> list[list[Operation]]:
        pass

    @property
    def _num_measurements(self) -> int:
        return len(self._parity_check_infos[0].flags_outcome)
