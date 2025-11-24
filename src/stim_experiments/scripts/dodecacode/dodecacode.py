from os import path
from pathlib import Path

from stim_experiments.scripts.simulate_and_plot import SimulateAndPlot, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_dodecacode_utilities

if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateAndPlot(
        run_configuration=run_configuration,
        target_code=get_dodecacode_utilities(),
        num_cat_states=5,
        code_title='Dodecacode',
        output_graph_filename='dodecacode.pdf',
        ymin_order=12,
        save_resume_filepath=Path(__file__).parent / 'save_resume.csv',
        decode_lookup_table_filepath=Path(__file__).parent / 'decode_lookup_table_dodeca'
    ).run_main()
