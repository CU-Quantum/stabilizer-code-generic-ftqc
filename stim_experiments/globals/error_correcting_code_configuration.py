from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
    CatStateCreatorFlagPattern
from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer.fault_tolerant_measurer import \
    FaultTolerantMeasurer


class ConfigurationErrorCorrectingCodeManager:
    _configuration = None

    @classmethod
    def get_configuration(cls) -> ConfigurationErrorCorrectingCode:
        if cls._configuration is None:
            from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard_fault_tolerant import \
                UniversalHadamardFaultTolerant
            from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip_fault_tolerant import \
                UniversalControlledFlipFaultTolerant
            from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_fault_tolerant import \
                UniversalTFaultTolerant
            cls._configuration = ConfigurationErrorCorrectingCode(
                measurer_type=FaultTolerantMeasurer,
                cat_state_creator_type=CatStateCreatorFlagPattern,
                universal_hadamard_type=UniversalHadamardFaultTolerant,
                universal_controlled_operation_type=UniversalControlledFlipFaultTolerant,
                universal_t_type=UniversalTFaultTolerant,
            )
        return cls._configuration
