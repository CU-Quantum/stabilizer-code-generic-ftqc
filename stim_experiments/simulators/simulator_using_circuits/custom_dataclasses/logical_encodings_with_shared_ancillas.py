from dataclasses import dataclass

from cirq import LineQubit

from stim_experiments.error_correcting_codes.error_correcting_code.error_correcting_code import ErrorCorrectingCode


@dataclass
class LogicalEncodingsWithSharedAncillas:
    encodings: list[ErrorCorrectingCode]
    ancillas: list[LineQubit]
