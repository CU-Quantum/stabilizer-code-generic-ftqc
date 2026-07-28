import numpy as np
from scipy.sparse import csr_matrix
from ldpc.bposd_decoder import BpOsdDecoder
from sinter import CompiledDecoder, Decoder


def _build_full_check_matrix(symplectic_rows, num_data_qubits):
    num_rows = symplectic_rows.shape[0]
    half = num_data_qubits
    rows = []
    cols = []
    for q in range(num_data_qubits):
        z_triggers = np.where(symplectic_rows[:, half + q] == 1)[0]
        for r in z_triggers:
            rows.append(r)
            cols.append(3 * q + 0)
        x_triggers = np.where(symplectic_rows[:, q] == 1)[0]
        for r in x_triggers:
            rows.append(r)
            cols.append(3 * q + 1)
        for r in np.union1d(z_triggers, x_triggers):
            rows.append(r)
            cols.append(3 * q + 2)
    num_cols = 3 * num_data_qubits
    data = np.ones(len(rows), dtype=np.uint8)
    return csr_matrix((data, (rows, cols)), shape=(num_rows, num_cols))


def _build_z_observable_vector(symplectic_rows, z_observable, num_data_qubits):
    num_cols = 3 * num_data_qubits
    obs = np.zeros(num_cols, dtype=np.uint8)
    half = num_data_qubits
    for q in range(num_data_qubits):
        if z_observable[half + q] == 1:
            obs[3 * q + 1] = 1
            obs[3 * q + 2] = 1
        if z_observable[q] == 1:
            obs[3 * q + 0] = 1
            obs[3 * q + 2] = 1
    return obs


class SymplecticBpOsdDecoder(Decoder):
    def __init__(self, symplectic_matrix, z_observable, distance,
                 final_detector_generator_indices):
        self._symplectic_matrix = symplectic_matrix
        self._z_observable = z_observable
        self._distance = distance
        self._final_detector_generator_indices = final_detector_generator_indices

    def compile_decoder_for_dem(self, *, dem):
        S = self._symplectic_matrix
        n_qubits = S.shape[1] // 2
        pcm = _build_full_check_matrix(S, n_qubits)
        obs = _build_z_observable_vector(S, self._z_observable, n_qubits)

        p = 0.01
        prior = p / 3
        channel = [prior] * pcm.shape[1]

        bposd = BpOsdDecoder(
            pcm, error_channel=channel,
            max_iter=100, bp_method='ms', ms_scaling_factor=0.625,
            schedule='parallel', osd_method='osd_cs', osd_order=10,
        )

        return CompiledSymplecticBpOsdDecoder(
            bposd=bposd, obs=obs,
            num_syndrome_bits=S.shape[0],
            distance=self._distance,
            final_detector_generator_indices=self._final_detector_generator_indices,
        )


class CompiledSymplecticBpOsdDecoder(CompiledDecoder):
    def __init__(self, bposd, obs, num_syndrome_bits, distance,
                 final_detector_generator_indices):
        self._bposd = bposd
        self._obs = obs
        self._num_syndrome_bits = num_syndrome_bits
        self._distance = distance
        self._final_detector_generator_indices = final_detector_generator_indices or []

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data):
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')
        syndromes = self._compute_syndromes(unpacked)
        num_shots = syndromes.shape[0]
        predictions = np.zeros((num_shots, 1), dtype=np.uint8)

        for i in range(num_shots):
            syndrome = syndromes[i]
            if not syndrome.any():
                continue
            correction = self._bposd.decode(syndrome.astype(np.uint8))
            if correction is not None:
                pred = (self._obs @ correction) % 2
                predictions[i, 0] = pred.astype(np.uint8)

        return np.packbits(predictions, axis=1, bitorder='little')

    def _compute_syndromes(self, unpacked):
        num_syn = self._num_syndrome_bits
        num_repeats = self._distance + 1
        differences = unpacked[:, :num_syn * num_repeats]
        differences = differences.reshape(differences.shape[0], num_repeats, num_syn)
        rounds = (np.cumsum(differences, axis=1) % 2).astype(np.uint8)
        syndromes = rounds[:, -1, :]
        if self._final_detector_generator_indices:
            indices = np.array(self._final_detector_generator_indices)
            num_final = len(indices)
            final_start = num_syn * num_repeats
            final_detectors = unpacked[:, final_start:final_start + num_final]
            data_derived = final_detectors ^ syndromes[:, indices]
            syndromes[:, indices] = data_derived
        return syndromes
