from stim_experiments.error_correcting_codes.generic_stabilizer_code.error_correcting_code_utilities import \
    ErrorCorrectingCodeUtilities, ErrorCorrectingCodeUtilitiesDensityMatrix, ErrorCorrectingCodeUtilitiesStateVector
from stim_experiments.utilities import TYPE_STATE_VECTOR_OR_DENSITY_MATRIX


def get_error_correcting_code_utilities(state: TYPE_STATE_VECTOR_OR_DENSITY_MATRIX) -> ErrorCorrectingCodeUtilities:
    is_state_vector = len(state.shape) == 1
    return ErrorCorrectingCodeUtilitiesStateVector() if is_state_vector else ErrorCorrectingCodeUtilitiesDensityMatrix()
