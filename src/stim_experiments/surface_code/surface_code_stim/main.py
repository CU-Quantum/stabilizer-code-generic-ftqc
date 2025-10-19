from matplotlib import pyplot as plt
from sinter import CSV_HEADER, Task, collect, plot_error_rate
from stim import Circuit

from generalized_shor_code_generators import GeneralizedShorCodeGenerators
from stim_experiments.surface_code.surface_code_stim.decoder_by_matrix import DecoderByMatrix


class Main:
    def __init__(self, distance: int):
        self._distance = distance

    def run_main(self):
        surface_code_generators = GeneralizedShorCodeGenerators(num_cats=self._distance, num_qubits_per_cat=self._distance)
        surface_code_symplectic_matrix = surface_code_generators.get_z_generators() + surface_code_generators.get_x_generators()

        samples = collect(
            num_workers=1,
            max_shots=1_000_000,
            max_errors=1000,
            tasks=self.generate_example_tasks(),
            decoders=['decoder_by_matrix'],
            custom_decoders={'decoder_by_matrix': DecoderByMatrix(symplectic_matrix=surface_code_symplectic_matrix)},
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
            group_func=lambda stat: f"Rotated Surface Code d={stat.json_metadata['d']}",
            x_func=lambda stat: stat.json_metadata['p'],
        )
        ax.loglog()
        ax.set_ylim(1e-5, 1)
        ax.grid()
        ax.set_title('Logical Error Rate vs Physical Error Rate')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        # Save to file and also open in a window.
        fig.savefig('plot.png')
        plt.show()

    def generate_example_tasks(self):
        for p in [0.001, 0.005, 0.01]:
            yield Task(
                circuit=self.generate_task_circuit(physical_error_rate=p),
                json_metadata={
                    'physical_error_rate': p,
                    'distance': self._distance,
                },
            )

    def generate_task_circuit(self, physical_error_rate: float) -> Circuit:
        circuit = Circuit.generated(
            rounds=1,
            distance=self._distance,
            code_task=f'surface_code:rotated_memory_x',
        )
        return circuit


if __name__ == '__main__':
    Main(distance=3).run_main()
