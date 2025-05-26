from dataclasses import dataclass
from typing import Optional

from stim_experiments.custom_enums.universal_controlled_operation_type import UniversalControlledOperationType
from stim_experiments.custom_enums.universal_hadamard_type import UniversalHadamardType
from stim_experiments.custom_enums.universal_t_type import UniversalTType
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer


@dataclass
class ConfigurationErrorCorrectingCode:
    measurer_type: type[Measurer] = FaultTolerantMeasurer
    cat_state_creator_type: type[CatStateCreator] = CatStateCreatorFlagPattern
    universal_hadamard_type: UniversalHadamardType = UniversalHadamardType.FAULT_TOLERANT
    universal_controlled_operation_type: UniversalControlledOperationType = UniversalControlledOperationType.FAULT_TOLERANT
    universal_t_type: UniversalTType = UniversalTType.FAULT_TOLERANT
    seed: Optional[int] = None
