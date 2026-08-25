from pathlib import Path

from stim_experiments.scripts.gscx import run_gscx_experiment


if __name__ == "__main__":
    run_gscx_experiment(distance=7, save_resume_filepath=Path(__file__).parent / 'save_resume')
