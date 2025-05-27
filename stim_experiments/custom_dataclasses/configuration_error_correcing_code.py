from dataclasses import dataclass
from typing import Optional

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_operation.universal_controlled_operation import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import \
    UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import UniversalT


@dataclass
class ConfigurationErrorCorrectingCode:
    measurer_type: type[Measurer]
    cat_state_creator_type: type[CatStateCreator]
    universal_hadamard_type: type[UniversalHadamard]
    universal_controlled_operation_type: type[UniversalControlledOperation]
    universal_t_type: type[UniversalT]
    seed: Optional[int] = None
