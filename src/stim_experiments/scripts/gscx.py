from pathlib import Path

from stim_experiments.scripts.simulate_qec import SimulateQec, get_run_configuration
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_gscx_code_utilities


def run_gscx_experiment(distance: int, save_resume_filepath: Path):
    SimulateQec(
        run_configuration=get_run_configuration(),
        target_code=get_gscx_code_utilities(distance=distance),
        num_cat_states=distance,
        code_title=f'GSC Distance {distance}',
        save_resume_filepath=save_resume_filepath,
    ).run_main()
