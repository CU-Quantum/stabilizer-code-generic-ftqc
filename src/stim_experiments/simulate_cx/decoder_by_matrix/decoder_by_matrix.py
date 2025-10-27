from itertools import combinations

import numpy as np
from numpy._typing import NDArray
from sinter import CompiledDecoder, Decoder
from stim import DetectorErrorModel

from stim_experiments.simulate_cx.decoder_by_matrix.compiled_decoder_by_matrix import CompiledDecoderByMatrix


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
            block_1 = list(range(self._num_target_data_qubits)) + list(range(self._num_data_qubits, self._num_data_qubits + self._num_target_data_qubits))
            block_2 = list(range(self._num_target_data_qubits, self._num_data_qubits)) + list(range(self._num_data_qubits + self._num_target_data_qubits, self._symplectic_matrix.shape[1]))
            possible_combos_per_block = [
                [combo for i in range(1, self._num_correctable_errors + 1) for combo in combinations(block, i)]
                for block in (block_1, block_2)
            ]
            possible_combos_all = possible_combos_per_block[0] + \
                                  possible_combos_per_block[1] + \
                                  [combo_1 + combo_2
                                   for combo_1 in possible_combos_per_block[0]
                                   for combo_2 in possible_combos_per_block[1]]
            syndrome_to_noise = {
                tuple(syndrome): noise
                for combo in possible_combos_all
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
        yield from self._propagation_syndromes_and_noises(combo=np.array(combo))

        y_additions = [(np.array(c) + self._num_data_qubits) % self._symplectic_matrix.shape[1] for i in range(len(combo)) for c in combinations(combo, i+1)]
        for y_addition in y_additions:
            y_combo = set(combo).union(set(y_addition))
            yield self._syndrome_and_noise_from_combo(y_combo)
            yield from self._propagation_syndromes_and_noises(combo=np.array(tuple(y_combo)))

    def _propagation_syndromes_and_noises(self, combo):
        if self._modified_index is not None and self._modified_index < len(self._symplectic_matrix):
            yield from self._forward_propagation(combo)
            yield from self._backward_propagation(combo)

    def _forward_propagation(self, combo):
        errors_in_target_x = combo[combo < self._num_target_data_qubits]
        errors_in_target_z = combo[(self._num_data_qubits <= combo) & (combo < self._num_data_qubits + self._num_target_data_qubits)] % self._num_data_qubits
        num_corrected_target_errors = len(errors_in_target_x) + len(errors_in_target_z)
        additional_num_correctable_control_errors = self._num_correctable_errors - num_corrected_target_errors
        if additional_num_correctable_control_errors > 0:
            x_errors_on_control_register = combo[self._num_data_qubits + self._num_target_data_qubits <= combo]
            if len(x_errors_on_control_register):
                modified_row = self._symplectic_matrix[self._modified_index]
                mask_control = np.ones(len(modified_row))
                mask_control[self._num_target_data_qubits:self._num_data_qubits] = np.zeros(self._num_data_qubits - self._num_target_data_qubits)
                target_indices = np.argwhere(np.array(modified_row, dtype=int) & np.array(mask_control,dtype=int) == 1).flatten()
                errors_that_commute_with_target = (target_indices + self._num_data_qubits) % len(modified_row)
                for additional_control_indices in [j for i in range(1, additional_num_correctable_control_errors + 1)
                                                   for j in combinations(errors_that_commute_with_target, i)]:
                    expanded_combo = set(combo).union(set(additional_control_indices))
                    yield self._syndrome_and_noise_from_combo(combo=expanded_combo)

    def _backward_propagation(self, combo):
        errors_in_control_x = combo[(self._num_target_data_qubits <= combo) & (combo < self._num_data_qubits)]
        errors_in_control_z = combo[self._num_data_qubits + self._num_target_data_qubits <= combo] % self._num_data_qubits
        num_corrected_control_errors = len(errors_in_control_x) + len(errors_in_control_z)
        additional_num_correctable_control_errors = self._num_correctable_errors - num_corrected_control_errors
        if additional_num_correctable_control_errors > 0:
            modified_row = self._symplectic_matrix[self._modified_index]
            noise_on_target = combo[(combo < self._num_target_data_qubits) | (combo >= self._num_data_qubits + self._num_target_data_qubits)]
            if len(modified_row[noise_on_target]):
                control_indices = np.argwhere(modified_row[self._num_target_data_qubits:self._num_data_qubits] == 1).flatten() + self._num_target_data_qubits
                for additional_control_indices in [j for i in range(1, additional_num_correctable_control_errors + 1)for j in combinations(control_indices, i)]:
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
