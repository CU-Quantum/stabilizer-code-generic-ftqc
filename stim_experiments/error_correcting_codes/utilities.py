from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities, ErrorCorrectingCodeUtilitiesDensityMatrix, ErrorCorrectingCodeUtilitiesStateVector
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


def is_state_vector(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> bool:
    return len(state.shape) == 1


def get_error_correcting_code_utilities(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> ErrorCorrectingCodeUtilities:
    return ErrorCorrectingCodeUtilitiesStateVector() if is_state_vector(state=state) else ErrorCorrectingCodeUtilitiesDensityMatrix()
