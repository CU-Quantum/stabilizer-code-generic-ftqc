from dataclasses import dataclass
from pathlib import Path

from matplotlib import pyplot as plt
from sinter import TaskStats, plot_error_rate

from stim_experiments.scripts import dodecacode, five_qubit, gscx_distance_3, gscx_distance_5, gscx_distance_7
from stim_experiments.scripts.utilities import get_shard_merge_paths, merge_csvs


@dataclass
class PlotConfig:
    code_title: str
    output_graph_filename: Path
    stats_dir: str
    ymin_order: int


PLOT_CONFIGS = [
    PlotConfig(
        code_title='Five-qubit',
        output_graph_filename=Path(five_qubit.__file__).parent / 'five_qubit.pdf',
        stats_dir=five_qubit.__file__,
        ymin_order=10
    ),
    PlotConfig(
        code_title='Dodecacode',
        output_graph_filename=Path(dodecacode.__file__).parent / 'dodecacode.pdf',
        stats_dir=dodecacode.__file__,
        ymin_order=10,
    ),
    PlotConfig(
        code_title='GSC Distance 3',
        output_graph_filename=Path(gscx_distance_3.__file__).parent / 'gscx_distance_3.pdf',
        stats_dir=gscx_distance_3.__file__,
        ymin_order=10,
    ),
    PlotConfig(
        code_title='GSC Distance 5',
        output_graph_filename=Path(gscx_distance_5.__file__).parent / 'gscx_distance_5.pdf',
        stats_dir=gscx_distance_5.__file__,
        ymin_order=10,
    ),
    PlotConfig(
        code_title='GSC Distance 7',
        output_graph_filename=Path(gscx_distance_7.__file__).parent / 'gscx_distance_7.pdf',
        stats_dir=gscx_distance_7.__file__,
        ymin_order=10,
    ),
]


class Main:
    def main(self):
        for plot_config in PLOT_CONFIGS:
            merge_paths = get_shard_merge_paths(files_in_dirs=[plot_config.stats_dir])
            if not merge_paths:
                continue
            sorted_merge_paths = list(sorted(merge_paths.keys()))
            stats = [merge_csvs(input_paths=[merge_path]) for merge_path in sorted_merge_paths]
            self._plot_qec(stats=stats, plot_config=plot_config)

    def _plot_qec(self, stats: list[list[TaskStats]], plot_config: PlotConfig):
        fig, ax = plt.subplots(1, 1)
        for i, samples in enumerate(stats):
            plot_args = {
                'color': [
                    '#D55E00',
                    '#009E73',
                    '#882255',
                    '#332288',
                    '#999933',
                    '#0072B2',
                    '#000000',
                    '#CC79A7',
                ][i - 1],
                'zorder': list(range(3, 11))[i - 1],
                'linestyle': [
                    (i * .05, ()),  # solid
                    (i * .05, (1, 1)),  # densely dotted
                    (i * .05, (5, 4)),  # densely dashed
                    (i * .05, (5, 7)),  # mediumly dashed
                    (i * .05, (5, 10)),  # loosely dashed
                    (i * .05, (1, 10)),  # loosely dotted
                    (i * .05, (1, 5)),  # dot-dashed
                    (i * .05, (3, 1, 1, 1)),  # dash-dot-dashed
                ][i - 1],
                'marker': ['D', 's', 'o', '^', 'v', '', 'P', 'X'][i - 1],
            }
            is_baseline = not i
            label = "No $\\overline{{CX}}$" if is_baseline else f"$\\overline{{CX}}_{{\\mathcal{{S}}_{i - 1},\\mathcal{{Q}}_1}}$"
            plot_error_rate(
                ax=ax,
                stats=samples,
                group_func=lambda stat: label,
                x_func=lambda stat: stat.json_metadata['physical_error_rate'],
                plot_args_func=lambda index, curve_id: plot_args
            )
        ax.loglog()
        ax.set_ylim(10 ** -plot_config.ymin_order, 1)
        ax.set_xlim(5e-5)
        ax.grid()
        ax.set_title(f'LER of $\\overline{{CX}}$ Controlled by GSCH Targeting {plot_config.code_title}')
        ax.set_ylabel('Logical Error Rate (per shot)')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        fig.savefig(plot_config.output_graph_filename)
        plt.show()


if __name__ == "__main__":
    Main().main()
