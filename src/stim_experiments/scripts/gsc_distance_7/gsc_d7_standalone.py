"""Standalone GSC [[49,1,7]] test with sinter + exact_mw/BP-OSD + plotting.

Isolates the Generalized Shor Code distance-7 code from the cat-state CX gate
framework, using a phenomenological noise model with nr = distance+1 rounds.
"""

import matplotlib
try:
    import tkinter
    matplotlib.use('TkAgg')
except (ImportError, ModuleNotFoundError):
    matplotlib.use('Agg')

from argparse import ArgumentParser
from pathlib import Path

import numpy as np
import stim
from sinter import Task, collect, plot_error_rate
from matplotlib import pyplot as plt

from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_gscx_code_utilities
from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.decoder_by_matrix.exact_mw_dem_decoder import ExactMwDemDecoder
from stim_experiments.simulate_cx.decoder_by_matrix.bposd_decoder import BpOsdDecoderForSinter


def build_gsc_d7_circuit(p: float, code_capacity: bool = False) -> stim.Circuit:
    return SimulateCx.build_bare_circuit(
        target_code=get_gscx_code_utilities(distance=7),
        physical_error_rate=p,
        num_rounds=8,
    )


def _build_decoder(decoder_name):
    if decoder_name == 'exact_mw':
        return ExactMwDemDecoder()
    elif decoder_name == 'bposd':
        return BpOsdDecoderForSinter()
    raise ValueError(f"Unknown decoder: {decoder_name}")


def run_and_plot(probs=None, max_shots=1_000_000, max_errors=1000, num_workers=4,
                 decoder_name='exact_mw', code_capacity=False, save_resume=None):
    if probs is None:
        probs = [5e-5, 1e-4, 2e-4, 5e-4, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]

    tasks = []
    for p in probs:
        c = build_gsc_d7_circuit(p, code_capacity=code_capacity)
        dem = c.detector_error_model(decompose_errors=False)
        tasks.append(Task(
            circuit=c,
            detector_error_model=dem,
            json_metadata={'physical_error_rate': p, 'distance': 7},
        ))

    decoder = _build_decoder(decoder_name)
    noise_label = 'code_capacity' if code_capacity else 'phenomenological'
    print(f"Running {len(tasks)} tasks with {num_workers} workers, "
          f"decoder={decoder_name}, noise={noise_label}...")
    stats = collect(
        num_workers=num_workers,
        max_shots=max_shots,
        max_errors=max_errors,
        tasks=tasks,
        decoders=[decoder_name],
        custom_decoders={decoder_name: decoder},
        print_progress=True,
        save_resume_filepath=save_resume,
    )

    fig, ax = plt.subplots(1, 1)
    ax.loglog()
    plot_error_rate(ax=ax, stats=stats,
                    x_func=lambda s: s.json_metadata['physical_error_rate'])
    ax.set_xlabel('Physical Error Rate')
    ax.set_ylabel('Logical Error Rate')
    ax.set_title(f'GSC [[49,1,7]] Standalone ({noise_label}, {decoder_name})')
    ax.grid()

    tag = f'gsc_d7_standalone_{noise_label}_{decoder_name}'
    out_path = Path(__file__).parent / f'{tag}.pdf'
    fig.savefig(str(out_path))
    print(f'Plot saved to {out_path}')
    fig.show()
    return stats


if __name__ == '__main__':
    parser = ArgumentParser(
        description='Standalone GSC distance-7 experiment (phenomenological noise).')
    parser.add_argument('-s', '--max-shots', type=int, default=10_000_000,
                        help='Maximum shots per task.')
    parser.add_argument('-e', '--max-errors', type=int, default=1_000,
                        help='Maximum errors per task.')
    parser.add_argument('-w', '--num-workers', type=int, default=4,
                        help='Number of parallel workers.')
    parser.add_argument('-d', '--decoder', type=str, default='exact_mw',
                        choices=['exact_mw', 'bposd'],
                        help='Decoder to use.')
    parser.add_argument('-p', '--probs', type=float, nargs='+',
                        default=[5e-5, 1e-4, 2e-4, 5e-4, 0.001, 0.002, 0.005, 0.01])
    parser.add_argument('--code-capacity', action='store_true',
                        help='Use code-capacity noise model (no measurement errors).')
    parser.add_argument('--save-resume', type=str, default=None,
                        help='Save/resume file path for sinter.')
    args = parser.parse_args()

    run_and_plot(
        probs=args.probs,
        max_shots=args.max_shots,
        max_errors=args.max_errors,
        num_workers=args.num_workers,
        decoder_name=args.decoder,
        code_capacity=args.code_capacity,
        save_resume=args.save_resume,
    )
