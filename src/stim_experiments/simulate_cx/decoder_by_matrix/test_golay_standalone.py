"""Standalone Golay [[23,1,7]] test with sinter + BP-OSD + plotting."""

import matplotlib
try:
    import tkinter
    matplotlib.use('TkAgg')
except (ImportError, ModuleNotFoundError):
    matplotlib.use('Agg')

import numpy as np
import stim
from ldpc.bposd_decoder import BpOsdDecoder
from ldpc.ckt_noise import detector_error_model_to_check_matrices
from sinter import Task, collect, plot_error_rate, Decoder, CompiledDecoder
from matplotlib import pyplot as plt

from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_golay_code_utilities


def build_golay_circuit(p: float) -> stim.Circuit:
    """Build standalone Golay phenomenological noise circuit."""
    utils = get_golay_code_utilities()
    S = utils.symplectic_matrix
    n = len(utils.data_indices)
    ng = S.shape[0]
    nr = 8  # distance + 1
    z_obs = utils.z_observable
    dqs = utils.data_indices

    c = stim.Circuit()
    c.append_from_stim_program_text(str(utils.get_init()))
    c.append_from_stim_program_text(str(utils.get_encoding_by_stabilizer()))

    for r in range(nr):
        if r < nr - 1:
            for q in dqs:
                c.append("DEPOLARIZE1", [q], p)
        meas_p = 0.0 if r == nr - 1 else p
        c.append_from_stim_program_text(
            str(utils.get_stabilizers(measurement_error_rate=meas_p)))

        if r == 0:
            for i in range(ng):
                c.append("DETECTOR", [stim.target_rec(-ng + i)])
        else:
            for i in range(ng):
                c.append("DETECTOR",
                         [stim.target_rec(-ng + i),
                          stim.target_rec(-2 * ng + i)])

    for q in dqs:
        c.append("M", [q])

    for i in range(ng):
        stab = S[i]
        z_part = stab[n:]
        support = [dqs[q_] for q_ in range(n) if z_part[q_]]
        if support and all(q_ in dqs for q_ in support):
            targets = [stim.target_rec(-n + dqs.index(q_)) for q_ in support]
            targets.append(stim.target_rec(-n - ng + i))
            c.append("DETECTOR", targets)

    obs_idx = sorted(set(np.where(z_obs == 1)[0] % n))
    for q_ in obs_idx:
        idx = dqs.index(q_)
        c.append("OBSERVABLE_INCLUDE", [stim.target_rec(-n + idx)], 0)

    return c


class GolayBposdDecoder(Decoder):
    """sinter Decoder wrapper around ldpc BP-OSD."""

    def compile_decoder_for_dem(self, *, dem):
        matrices = detector_error_model_to_check_matrices(
            dem, allow_undecomposed_hyperedges=True)
        check_matrix = matrices.check_matrix
        observables_matrix = matrices.observables_matrix.toarray().astype(np.uint8)
        priors = list(matrices.priors)
        bposd = BpOsdDecoder(
            check_matrix, error_channel=priors,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10,
        )
        return CompiledGolayBposd(bposd, observables_matrix, dem.num_detectors)


class CompiledGolayBposd(CompiledDecoder):
    def __init__(self, bposd, obs, num_detectors):
        super().__init__()
        self._bposd = bposd
        self._obs = obs
        self._num_detectors = num_detectors

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1,
                                 bitorder='little')[:, :self._num_detectors]
        n_shots = unpacked.shape[0]
        predictions = np.zeros((n_shots, (self._obs.shape[0] + 7) // 8),
                               dtype=np.uint8)
        for i in range(n_shots):
            syn = unpacked[i].astype(np.uint8)
            if not syn.any():
                continue
            corr = self._bposd.decode(syn)
            if corr is not None:
                pred = (self._obs @ corr) % 2
                predictions[i] = np.packbits(
                    pred.astype(np.uint8).reshape(1, -1),
                    axis=1, bitorder='little')[0]
        return predictions


def run_and_plot(probs=None, max_shots=1_000_000, max_errors=1000, num_workers=4):
    """Run sinter simulation and plot LER vs p."""
    if probs is None:
        probs = [.0002, .0005, .0007, 0.001, 0.002, 0.005, 0.01]

    tasks = []
    for p in probs:
        c = build_golay_circuit(p)
        dem = c.detector_error_model(
            decompose_errors=True, ignore_decomposition_failures=True)
        tasks.append(Task(
            circuit=c,
            detector_error_model=dem,
            json_metadata={'physical_error_rate': p, 'distance': 7},
        ))

    print(f"Running {len(tasks)} tasks with {num_workers} workers...")
    stats = collect(
        num_workers=num_workers,
        max_shots=max_shots,
        max_errors=max_errors,
        tasks=tasks,
        decoders=['bposd'],
        custom_decoders={'bposd': GolayBposdDecoder()},
        print_progress=True,
    )

    fig, ax = plt.subplots(1, 1)
    ax.loglog()
    plot_error_rate(ax=ax, stats=stats,
                    x_func=lambda s: s.json_metadata['physical_error_rate'])
    ax.set_xlabel('Physical Error Rate')
    ax.set_ylabel('Logical Error Rate')
    ax.set_title('Golay [[23,1,7]] Standalone (Phenomenological Noise)')
    ax.grid()
    fig.savefig('golay_standalone.pdf')
    if matplotlib.get_backend() != 'Agg':
        plt.show()
    return stats


if __name__ == '__main__':
    run_and_plot()
