from matplotlib import pyplot as plt
from sinter import CSV_HEADER, plot_error_rate

from stim_experiments.simulate_cx.simulate_cx import SimulateCx
from stim_experiments.simulate_cx.stabilizer_code_utilities import get_five_qubit_code_utilities


class FiveQubit:
    def run_main(self):
        target_code = get_five_qubit_code_utilities()
        samples_list = [SimulateCx(num_cat_states=3, target_code_utilities=target_code, si=i).run_main() for i in range(3)]

        # Print samples as CSV data.
        print(CSV_HEADER)
        for samples in samples_list:
            for sample in samples:
                print(sample.to_csv_line())

        # Render a matplotlib plot of the data.
        fig, ax = plt.subplots(1, 1)
        for i, samples in enumerate(samples_list):
            plot_error_rate(
                ax=ax,
                stats=samples,
                group_func=lambda stat: f"$CX_{{s{i},L1}}$",
                x_func=lambda stat: stat.json_metadata['physical_error_rate'],
                plot_args_func=lambda index, curve_id: {'color': f'C{i}'}
            )
        ax.loglog()
        ax.set_ylim(1e-10, 1e-1)
        ax.grid()
        ax.set_title('LER of CX Controlled by GSCH targeting Five Qubit Code')
        ax.set_ylabel('Logical Error Probability (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        # Save to file and also open in a window.
        # fig.savefig('plot.png')
        plt.show()


if __name__ == "__main__":
    FiveQubit().run_main()
