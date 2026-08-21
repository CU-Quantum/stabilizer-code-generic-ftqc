from pathlib import Path

from stim_experiments.scripts.simulate_qec import SimulateQec, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_dodecacode_utilities

if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateQec(
        run_configuration=run_configuration,
        target_code=get_dodecacode_utilities(),
        num_cat_states=5,
        code_title='Dodecacode',
        save_resume_filepath=Path(__file__).parent / 'save_resume',
        target_decoder='lookup',
    ).run_main()
