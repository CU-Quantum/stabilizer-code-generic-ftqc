from dataclasses import dataclass
from typing import Optional

from stim_experiments.custom_dataclasses.noise_parameters import NoiseParameters
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator import CatStateCreator
from stim_experiments.error_correcting_codes.support.cat_state_creator.cat_state_creator_basic_nondeterministic.support.parity_verifier import \
    ParityVerifier
from stim_experiments.error_correcting_codes.support.measurer.measurer import Measurer
from stim_experiments.error_correcting_codes.support.universal_operations.universal_controlled_flip.universal_controlled_flip import \
    UniversalControlledOperation
from stim_experiments.error_correcting_codes.support.universal_operations.universal_hadamard.universal_hadamard import \
    UniversalHadamard
from stim_experiments.error_correcting_codes.support.universal_operations.universal_t.universal_t import UniversalT


@dataclass
class ConfigurationErrorCorrectingCode:
    majority_vote_repetitions: int
    noise_parameters: NoiseParameters
    num_cat_states: int
    seed: Optional[int]

    cat_state_creator_type: type[CatStateCreator]
    measurer_type: type[Measurer]
    parity_verifier_type: type[ParityVerifier]
    universal_hadamard_type: type[UniversalHadamard]
    universal_controlled_operation_type: type[UniversalControlledOperation]
    universal_t_type: type[UniversalT]
