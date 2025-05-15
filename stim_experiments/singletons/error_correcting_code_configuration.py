from dataclasses import dataclass
from typing import Type

from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer


@dataclass
class ConfigurationErrorCorrectingCode:
    measurer_type: Type[Measurer] = FaultTolerantMeasurer
    cat_state_creator_type: Type[CatStateCreator] = CatStateCreatorFlagPattern


class ConfigurationErrorCorrectingCodeManager:
    _configuration = None

    @classmethod
    def get_configuration(cls) -> ConfigurationErrorCorrectingCode:
        if cls._configuration is None:
            cls._configuration = ConfigurationErrorCorrectingCode()
        return cls._configuration
