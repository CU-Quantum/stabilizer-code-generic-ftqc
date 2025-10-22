from itertools import combinations

import numpy as np
import pytest
from matplotlib import pyplot as plt
from pymatching import Matching
from scipy.sparse import csc_matrix
from sinter import CSV_HEADER, CompiledDecoder, Decoder, Task, collect, plot_error_rate
from stim import Circuit, DetectorErrorModel

from stim_experiments.surface_code.surface_code_stim.compiled_decoder_by_matrix import CompiledDecoderByMatrix
from stim_experiments.surface_code.surface_code_stim.decoder_by_matrix import DecoderByMatrix


class CompiledDecoderByMatrixRepetition(CompiledDecoder):
    def __init__(self, matching: Matching):
        super().__init__()
        self._matching = matching
        self._symplectic_matrix = np.array([[1, 1, 0], [0, 1, 1]])
        self._distance = 3
        self._observables = np.array([[1, 0, 0]])

    def decode_shots_bit_packed(self, *, bit_packed_detection_event_data: np.ndarray) -> np.ndarray:
        unpacked = np.unpackbits(bit_packed_detection_event_data, axis=1, bitorder='little')[:, :self._symplectic_matrix.shape[0]]
        # from_pymatching_dem_results = self._matching.decode_batch(unpacked)
        # from_pymatching_matrix_results = Matching.from_check_matrix(csc_matrix(self._symplectic_matrix))
        predictions = np.zeros((unpacked.shape[0], len(self._observables)), dtype=np.uint8)
        if unpacked.max():
            possible_combos = [combo for i in range(1, (self._distance - 1) // 2 + 1) for combo in
                               combinations(range(self._symplectic_matrix.shape[1]), i)]
            for combo in possible_combos:
                found_noise = np.zeros(self._symplectic_matrix.shape[1], dtype=np.uint8)
                found_noise[list(combo)] = np.ones(len(combo))
                found_syndrome = (self._symplectic_matrix @ found_noise) % 2
                if not found_syndrome.max():
                    continue
                indices_matching = np.where(np.all(unpacked == found_syndrome, axis=1))[0]
                if len(indices_matching):
                    noisy_shots = np.array([found_noise for _ in range(len(indices_matching))], dtype=np.uint8)
                    predictions[indices_matching] = (noisy_shots @ self._observables.T) % 2
        by_matrix_results = DecoderByMatrix(
            symplectic_matrix=self._symplectic_matrix,
            distance=self._distance,
            observables=self._observables,
        ).compile_decoder_for_dem(dem=None).decode_shots_bit_packed(
            bit_packed_detection_event_data=bit_packed_detection_event_data
        )
        return by_matrix_results


class DecoderByMatrixRepetition(Decoder):
    def compile_decoder_for_dem(
            self,
            *,
            dem: DetectorErrorModel,
    ) -> CompiledDecoder:
        return CompiledDecoderByMatrixRepetition(matching=Matching.from_detector_error_model(dem))


class RepetitionSimulator:
    def __init__(self):
        self._distance = 3

    def run_main(self):
        samples = collect(
            num_workers=1,
            max_shots=1_000_000,
            max_errors=1_000,
            tasks=self.generate_example_tasks(),
            decoders=['decoder_by_matrix'],
            custom_decoders={'decoder_by_matrix': DecoderByMatrixRepetition()},
        )

        # Print samples as CSV data.
        print(CSV_HEADER)
        for sample in samples:
            print(sample.to_csv_line())

        # Render a matplotlib plot of the data.
        fig, ax = plt.subplots(1, 1)
        plot_error_rate(
            ax=ax,
            stats=samples,
            group_func=lambda stat: f"Rotated Surface Code d={stat.json_metadata['distance']}",
            x_func=lambda stat: stat.json_metadata['physical_error_rate'],
        )
        ax.loglog()
        ax.set_ylim(1e-10, 1e-1)
        ax.grid()
        ax.set_title('Logical Error Rate vs Physical Error Rate')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        # Save to file and also open in a window.
        # fig.savefig('plot.png')
        plt.show()

    def generate_example_tasks(self):
        for p in [1e-4, 0.001, 0.005, 0.01]:
            yield Task(
                circuit=self.generate_task_circuit(physical_error_rate=p),
                json_metadata={
                    'physical_error_rate': p,
                    'distance': self._distance,
                },
            )

    def generate_task_circuit(self, physical_error_rate: float) -> Circuit:
        return Circuit(f"""
            QUBIT_COORDS(0, 0) 0
            QUBIT_COORDS(0, 1) 1
            QUBIT_COORDS(0, 2) 2
            QUBIT_COORDS(0, 3) 3
            QUBIT_COORDS(0, 4) 4
            R 0 1 2 3 4 

            X_ERROR({physical_error_rate}) 0 1 2
            TICK
            H 3
            CZ 3 0 3 1
            H 3
            TICK
            H 4
            CZ 4 1 4 2
            H 4

            TICK
            MR 3 4
            DETECTOR rec[-2]
            DETECTOR rec[-1]
            M 0
            OBSERVABLE_INCLUDE(0) rec[-1]
        """)


@pytest.mark.experiment
class TestRepetitionMatrixDecoder:
    def test(self):
        RepetitionSimulator().run_main()
