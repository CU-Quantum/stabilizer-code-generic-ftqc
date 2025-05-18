from dataclasses import dataclass
from typing import Optional

from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


@dataclass
class LogicalEncodingIndex:
    encoding: ErrorCorrectingCode
    qubit_index_relative: int
    qubit_index_logical: int


@dataclass
class TargetEncoding:
    operation: LogicalOperation
    encoding: ErrorCorrectingCode


@dataclass
class SimulationOperation:
    target_encoding: Optional[TargetEncoding] = None
    control_encoding: Optional[LogicalEncodingIndex] = None
