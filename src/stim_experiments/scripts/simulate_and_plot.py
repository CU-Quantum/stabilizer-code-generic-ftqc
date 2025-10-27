from argparse import ArgumentParser
from multiprocessing import cpu_count

from matplotlib import pyplot as plt
from sinter import CSV_HEADER, plot_error_rate

from stim_experiments.simulate_cx.custom_dataclasses import RunConfiguration
from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.support.stabilizer_code_utilities import StabilizerCodeUtilities


def get_run_configuration() -> RunConfiguration:
    parser = ArgumentParser()
    parser.add_argument('-s', '--max-shots', type=int, default=100_000_000,
                        help='Maximum number of shots to run the algorithm for.')
    parser.add_argument('-e', '--max-errors', type=int, default=10_000,
                        help='Maximum number of errors.')
    parser.add_argument('-p', '--depolarization-probabilities', type=float, nargs='+',
                        default=[1e-5, 5e-5, 1e-4, 5e-4, 0.001, 0.005, 0.01],
                        help='Maximum number of errors.')
    parser.add_argument('-w', '--num-workers', type=int, default=cpu_count(),
                        help='The number of processes to run in parallel.'
                             ' Default is the number of CPUs available on the machine.')
    args = parser.parse_args()
    print(f"Running with arguments: {args}")
    return RunConfiguration(
        max_shots=args.max_shots,
        max_errors=args.max_errors,
        depolarization_probabilities=args.depolarization_probabilities,
        num_workers=args.num_workers
    )


class SimulateAndPlot:
    def __init__(self,
                 run_configuration: RunConfiguration,
                 target_code: StabilizerCodeUtilities,
                 num_cat_states: int,
                 code_title: str,
                 filename: str):
        self._run_configuration = run_configuration
        self._target_code = target_code
        self._num_cat_states = num_cat_states
        self._code_title = code_title
        self._filename = filename

    def run_main(self):
        target_code = self._target_code
        samples_list = [SimulateCx(num_cat_states=self._num_cat_states,
                                   target_code_utilities=target_code,
                                   si=i,
                                   run_configuration=self._run_configuration,
                                   ).run_main()
                        for i in range(-1, self._num_cat_states)]

        # Print samples as CSV data.
        print(CSV_HEADER)
        for samples in samples_list:
            for sample in samples:
                print(sample.to_csv_line())

        fig, ax = plt.subplots(1, 1)
        for i, samples in enumerate(samples_list):
            plot_args = {'color': f'C{i}'}
            is_baseline = not i
            if is_baseline:
                plot_args['linestyle'] = '--'
            label = "No CX" if is_baseline else f"$CX_{{s{i-1},L1}}$"
            plot_error_rate(
                ax=ax,
                stats=samples,
                group_func=lambda stat: label,
                x_func=lambda stat: stat.json_metadata['physical_error_rate'],
                plot_args_func=lambda index, curve_id: plot_args
            )
        ax.loglog()
        ax.set_ylim(1e-10, 1e-1)
        ax.grid()
        ax.set_title(f'LER of CX Controlled by GSCH Targeting {self._code_title}')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        fig.savefig(self._filename)
        plt.show()
