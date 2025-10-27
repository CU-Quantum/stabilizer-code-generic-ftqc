from cirq_experiments.error_correcting_codes.stabilizer_standardized_code.stabilizer_standardized_code import \
    StabilizerStandardizedCode
from predefined_check_matrix_values import get_check_matrix_values_dodecacode
from stim_experiments.scripts.simulate_and_plot import SimulateAndPlot, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_dodecacode_utilities

if __name__ == "__main__":
    s = StabilizerStandardizedCode(generators=get_check_matrix_values_dodecacode())

    run_configuration = get_run_configuration()
    SimulateAndPlot(
        run_configuration=run_configuration,
        target_code=get_dodecacode_utilities(),
        num_cat_states=3,
        code_title='Dodecacode',
        filename='dodecacode.pdf'
    ).run_main()
