from cirq_experiments.custom_dataclasses.noise_parameters import NoiseParameters


class ConfigurationErrorCorrectingCodeManager:
    _configuration = None

    @classmethod
    def get_configuration(cls) -> 'ConfigurationErrorCorrectingCode':
        if cls._configuration is None:
            cls.reset_configuration()
        return cls._configuration

    @classmethod
    def reset_configuration(cls) -> None:
        from cirq_experiments.support.cat_state_creator.cat_state_creator_flag_pattern.cat_state_creator_flag_pattern import \
            CatStateCreatorFlagPattern
        from cirq_experiments.support.measurer.fault_tolerant_measurer_sequential import \
            FaultTolerantMeasurerSequential
        from cirq_experiments.support.universal_operations.universal_controlled_flip.universal_controlled_flip_fault_tolerant import \
            UniversalControlledFlipFaultTolerant
        from cirq_experiments.support.universal_operations.universal_hadamard.universal_hadamard_fault_tolerant import \
            UniversalHadamardFaultTolerant
        from cirq_experiments.support.universal_operations.universal_t.universal_t_fault_tolerant import \
            UniversalTFaultTolerant
        from cirq_experiments.support.cat_state_creator.cat_state_creator_basic_nondeterministic.support.parity_verifier_sequential import \
            ParityVerifierSequential
        from cirq_experiments.custom_dataclasses.configuration_error_correcing_code import \
            ConfigurationErrorCorrectingCode
        cls._configuration = ConfigurationErrorCorrectingCode(
            cat_state_creator_type=CatStateCreatorFlagPattern,
            majority_vote_repetitions=3,
            measurer_type=FaultTolerantMeasurerSequential,
            noise_parameters=NoiseParameters(
                depolarization_probability_one_qubit=1e-4,
                depolarization_probability_two_qubit=2e-4,
            ),
            num_cat_states=3,
            parity_verifier_type=ParityVerifierSequential,
            seed=None,
            universal_hadamard_type=UniversalHadamardFaultTolerant,
            universal_controlled_operation_type=UniversalControlledFlipFaultTolerant,
            universal_t_type=UniversalTFaultTolerant,
        )
