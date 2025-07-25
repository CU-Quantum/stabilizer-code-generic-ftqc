from stim_experiments.custom_dataclasses.configuration_error_correcing_code import ConfigurationErrorCorrectingCode
from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters


class ConfigurationErrorCorrectingCodeManager:
    _configuration = None

    @classmethod
    def get_configuration(cls) -> ConfigurationErrorCorrectingCode:
        if cls._configuration is None:
            cls.reset_configuration()
        return cls._configuration

    @classmethod
    def reset_configuration(cls) -> None:
        from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
            CatStateCreatorFlagPattern
        from stim_experiments.error_correcting_codes.support.measurer.fault_tolerant_measurer import \
            FaultTolerantMeasurer
        from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip_fault_tolerant import \
            UniversalControlledFlipFaultTolerant
        from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard_fault_tolerant import \
            UniversalHadamardFaultTolerant
        from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t_fault_tolerant import \
            UniversalTFaultTolerant
        cls._configuration = ConfigurationErrorCorrectingCode(
            cat_state_creator_type=CatStateCreatorFlagPattern,
            majority_vote_repetitions=3,
            measurer_type=FaultTolerantMeasurer,
            noise_parameters=NoiseParameters(
                depolarization_probability_one_qubit=1e-4,
                depolarization_probability_two_qubit=2e-4,
            ),
            num_cat_states=3,
            parallel=True,
            seed=None,
            universal_hadamard_type=UniversalHadamardFaultTolerant,
            universal_controlled_operation_type=UniversalControlledFlipFaultTolerant,
            universal_t_type=UniversalTFaultTolerant,
        )
