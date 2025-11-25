from pathlib import Path

from stim_experiments.scripts.simulate_and_plot import SimulateAndPlot, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_five_qubit_code_utilities


if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateAndPlot(
        run_configuration=run_configuration,
        target_code=get_five_qubit_code_utilities(),
        num_cat_states=3,
        code_title='Five Qubit Code',
        output_graph_filename='five_qubit.pdf',
        save_resume_filepath=Path(__file__).parent / 'save_resume',
        ymin_order=10
    ).run_main()
