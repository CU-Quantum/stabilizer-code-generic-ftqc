from stim_experiments.scripts.simulate_and_plot import SimulateAndPlot, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_dodecacode_utilities

if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateAndPlot(
        run_configuration=run_configuration,
        target_code=get_dodecacode_utilities(),
        num_cat_states=5,
        code_title='Dodecacode',
        filename='dodecacode.pdf'
    ).run_main()
