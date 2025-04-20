from dataclasses import dataclass
from typing import Optional

from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


@dataclass
class ControlEncoding:
    encoding: ErrorCorrectingCode
    qubit_index: int


@dataclass
class TargetEncoding:
    operation: LogicalOperation
    encoding: ErrorCorrectingCode


@dataclass
class SimulationOperation:
    target_encoding: Optional[TargetEncoding] = None
    control_encoding: Optional[ControlEncoding] = None
