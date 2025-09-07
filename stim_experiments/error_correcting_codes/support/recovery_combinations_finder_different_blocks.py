from collections import defaultdict
from dataclasses import dataclass, replace
from itertools import combinations
from typing import Optional

import numpy as np
from cirq import LineQubit, X, Y, Z

from stim_experiments.custom_dataclasses.recovery import RecoveryGate, RecoveryOperation


@dataclass
class BlockErrorInfo:
    max_num_errors: Optional[int] = None
    max_num_x_errors: Optional[int] = None
    max_num_z_errors: Optional[int] = None


class RecoveryCombinationsFinderDifferentBlocks:
    pass
