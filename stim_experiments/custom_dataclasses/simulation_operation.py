from dataclasses import dataclass
from typing import Optional

from stim_experiments.custom_dataclasses.logical_operation import LogicalOperation
from stim_experiments.error_correcting_codes.stabilizer_code.stabilizer_code import StabilizerCode


@dataclass
class LogicalEncodingIndex:
    encoding: StabilizerCode
    qubit_index_relative: int
    qubit_index_logical: Optional[int] = None


@dataclass
class TargetEncoding:
    operation: LogicalOperation
    encoding: StabilizerCode


@dataclass
class SimulationOperation:
    target_encoding: Optional[TargetEncoding] = None
    control_encoding: Optional[LogicalEncodingIndex] = None
