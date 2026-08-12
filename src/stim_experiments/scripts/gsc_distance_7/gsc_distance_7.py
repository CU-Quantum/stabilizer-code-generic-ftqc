from pathlib import Path

from stim_experiments.scripts.simulate_qec import SimulateQec, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_gscx_code_utilities


if __name__ == "__main__":
    run_configuration = get_run_configuration()
    SimulateQec(
        run_configuration=run_configuration,
        target_code=get_gscx_code_utilities(distance=7),
        num_cat_states=7,
        code_title='GSC Distance 7',
        save_resume_filepath=Path(__file__).parent / 'save_resume',
    ).run_main()
