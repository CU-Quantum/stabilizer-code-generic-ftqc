from pathlib import Path

from stim_experiments.scripts.simulate_qec import SimulateQec, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_golay_code_utilities


if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateQec(
        run_configuration=run_configuration,
        target_code=get_golay_code_utilities(),
        num_cat_states=7,
        code_title='Golay Code',
        save_resume_filepath=Path(__file__).parent / 'save_resume',
        max_si=run_configuration.max_si,
    ).run_main()
