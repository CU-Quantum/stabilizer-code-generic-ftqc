from typing import List

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode
from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.simulators.custom_dataclasses.simulator_result import SimulatorResult


class SimulatorUsingCircuits:
    def __init__(self, error_correcting_code: ErrorCorrectingCode):
        self._error_correcting_code = error_correcting_code

    def simulate(self, operations: List[LogicalOperation]) -> SimulatorResult:
        for operation in operations:
            self._error_correcting_code.apply_operation(operation=operation)
        return SimulatorResult(
            state=self._error_correcting_code.get_current_state(),
            measurements={},
        )
