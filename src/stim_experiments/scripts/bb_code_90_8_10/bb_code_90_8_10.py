from pathlib import Path

from stim_experiments.scripts.simulate_qec import SimulateQec, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_bb_code_90_8_10_utilities


if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateQec(
        run_configuration=run_configuration,
        target_code=get_bb_code_90_8_10_utilities(),
        num_cat_states=10,
        code_title='BB Code [[90,8,10]]',
        save_resume_filepath=Path(__file__).parent / 'save_resume',
    ).run_main()
