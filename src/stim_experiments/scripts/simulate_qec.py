from argparse import ArgumentParser
from multiprocessing import cpu_count
import os
from pathlib import Path
from typing import Optional

from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import StabilizerCodeUtilities


def get_run_configuration() -> RunConfiguration:
    parser = ArgumentParser()
    parser.add_argument('-s', '--max-shots', type=int, default=100_000_000,
                        help='Maximum number of shots to run the algorithm for.')
    parser.add_argument('-e', '--max-errors', type=int, default=1_000,
                        help='Maximum number of errors.')
    parser.add_argument('-p', '--depolarization-probabilities', type=float, nargs='+',
                        default=[1e-5, 5e-5, 1e-4, 5e-4, 0.001, 0.005, 0.01],
                        help='Maximum number of errors.')
    # Respect SLURM_CPUS_PER_TASK if present; otherwise fall back to local cpu_count().
    slurm_cpus = int(os.environ.get('SLURM_CPUS_PER_TASK', '0') or '0')
    default_workers = slurm_cpus if slurm_cpus > 0 else cpu_count()
    parser.add_argument('-w', '--num-workers', type=int, default=default_workers,
                        help='The number of processes to run in parallel. '
                             'Default is $SLURM_CPUS_PER_TASK if set, else the local CPU count.')
    # Sharding across multiple jobs (e.g., SLURM array). Default from SLURM env if available.
    default_num_shards = int(os.environ.get('SLURM_ARRAY_TASK_COUNT', '1') or '1')
    default_shard_index = int(os.environ.get('SLURM_ARRAY_TASK_ID', '0') or '0')
    parser.add_argument('--num-shards', type=int, default=default_num_shards,
                        help='Total number of shards (e.g., SLURM array size). Default from $SLURM_ARRAY_TASK_COUNT or 1.')
    parser.add_argument('--shard-index', type=int, default=default_shard_index,
                        help='Index of this shard (e.g., SLURM array task ID). Default from $SLURM_ARRAY_TASK_ID or 0.')
    parser.add_argument('--max-si', type=int, default=None,
                        help='Only simulate si values up to this (inclusive). Default: all.')
    parser.add_argument('--si', type=int, default=None,
                        help='Only simulate this specific si value. Default: all.')
    args = parser.parse_args()
    print(f"Running with arguments: {args}")
    return RunConfiguration(
        max_shots=args.max_shots,
        max_errors=args.max_errors,
        depolarization_probabilities=args.depolarization_probabilities,
        num_workers=args.num_workers,
        num_shards=args.num_shards,
        shard_index=args.shard_index,
        max_si=args.max_si,
        si=args.si,
    )


class SimulateQec:
    def __init__(self,
                 run_configuration: RunConfiguration,
                 target_code: StabilizerCodeUtilities,
                 num_cat_states: int,
                 code_title: str,
                 save_resume_filepath: Optional[Path] = None,
                 ymin_order: int = 10,
                 target_decoder: Optional[str] = None):
        self._run_configuration = run_configuration
        self._target_code = target_code
        self._num_cat_states = num_cat_states
        self._code_title = code_title
        self._ymin_order = ymin_order
        self._save_resume_filepath = save_resume_filepath
        self._target_decoder = target_decoder

    def run_main(self):
        target_code = self._target_code
        si_values = [self._run_configuration.si] if self._run_configuration.si is not None \
            else range(-1, self._num_cat_states)
        for i in si_values:
            if self._run_configuration.max_si is not None and i > self._run_configuration.max_si:
                continue
            SimulateCx(num_cat_states=self._num_cat_states,
                       target_code_utilities=target_code,
                       si=i,
                       run_configuration=self._run_configuration,
                       save_resume_filepath=self._save_resume_filepath,
                       target_decoder=self._target_decoder,
                       ).run_main()
