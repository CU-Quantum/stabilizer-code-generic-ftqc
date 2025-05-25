from abc import ABC, abstractmethod

from stim_experiments.custom_dataclasses.state_encoding import StateEncoding


class StateEncoder(ABC):
    @abstractmethod
    def encode_state(self) -> StateEncoding:
        pass
