from itertools import combinations

import numpy as np
from numpy._typing import NDArray
from sinter import CompiledDecoder, Decoder
from stim import DetectorErrorModel

from stim_experiments.simulate_cx.compiled_decoder_by_matrix import CompiledDecoderByMatrix


class DecoderByMatrix(Decoder):
    def __init__(self,
                 symplectic_matrix: NDArray[NDArray[int]],
                 distance: int,
                 observables: NDArray[int],
                 modified_index: int,
                 num_target_data_qubits: int,):
        self._symplectic_matrix = symplectic_matrix
        self._distance = distance
        self._observables = observables
        self._modified_index = modified_index
        self._num_target_data_qubits = num_target_data_qubits
        self._cache = None

    def compile_decoder_for_dem(
            self,
            *,
            dem: DetectorErrorModel,
    ) -> CompiledDecoder:
        if self._cache is None:
            possible_combos = [combo
                               for i in range(1, self._num_correctable_errors + 1)
                               for combo in combinations(range(self._symplectic_matrix.shape[1]), i)]
            syndrome_to_noise = {
                tuple(syndrome): noise
                for combo in possible_combos
                for syndrome, noise in list(self._syndrome_and_noise_from_non_y_combo(combo))
                if syndrome.max()
            }
            self._cache = CompiledDecoderByMatrix(
                syndrome_to_noise=syndrome_to_noise,
                distance=self._distance,
                observables=self._observables
            )
        return self._cache

    def _syndrome_and_noise_from_non_y_combo(self, combo):
        yield self._syndrome_and_noise_from_combo(combo=combo)
        yield from self._phase_propagation_syndromes_and_noises(combo=np.array(combo))

        y_additions = [(np.array(c) + self._num_data_qubits) % self._symplectic_matrix.shape[1] for i in range(len(combo)) for c in combinations(combo, i+1)]
        for y_addition in y_additions:
            y_combo = set(np.concatenate([combo, y_addition]))
            yield self._syndrome_and_noise_from_combo(y_combo)
            yield from self._phase_propagation_syndromes_and_noises(combo=np.array(tuple(y_combo)))

    def _phase_propagation_syndromes_and_noises(self, combo):
        num_errors_in_control_x = combo[(self._num_target_data_qubits <= combo) & (combo < self._num_data_qubits)]
        num_errors_in_control_z = combo[self._num_data_qubits + self._num_target_data_qubits <= combo]
        num_corrected_control_errors = np.count_nonzero(num_errors_in_control_x) + np.count_nonzero(num_errors_in_control_z)
        additional_num_correctable_control_errors = self._num_correctable_errors - num_corrected_control_errors
        if additional_num_correctable_control_errors > 0 and self._modified_index < len(self._symplectic_matrix):
            modified_row = self._symplectic_matrix[self._modified_index]
            noise_on_target = combo[(combo < self._num_target_data_qubits) | (combo >= self._num_data_qubits + self._num_target_data_qubits)]
            if np.count_nonzero(modified_row[noise_on_target]):
                control_indices = np.argwhere(modified_row[self._num_target_data_qubits:self._num_data_qubits] == 1).flatten() + self._num_target_data_qubits
                for additional_control_indices in [j for i in range(1, additional_num_correctable_control_errors + 1) for j in combinations(control_indices, i)]:
                    expanded_combo = set(combo).union(set(additional_control_indices))
                    yield self._syndrome_and_noise_from_combo(combo=expanded_combo)

    def _syndrome_and_noise_from_combo(self, combo):
            found_noise = np.zeros(self._symplectic_matrix.shape[1], dtype=np.uint8)
            found_noise[list(combo)] = np.ones(len(combo))
            found_syndrome = (self._symplectic_matrix @ found_noise) % 2
            return found_syndrome, found_noise

    @property
    def _num_correctable_errors(self):
        return (self._distance - 1) // 2

    @property
    def _num_data_qubits(self):
        return self._symplectic_matrix.shape[1] // 2
