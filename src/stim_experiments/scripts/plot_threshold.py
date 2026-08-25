from math import prod
from pathlib import Path
from collections import defaultdict

from matplotlib import pyplot as plt

from stim_experiments.scripts import dodecacode, dodecacode_lookup, five_qubit, gscx_distance_7
from stim_experiments.scripts.utilities import get_shard_merge_paths, merge_csvs


class Main:
    def main(self):
        codes = [
            ('Five-qubit', five_qubit.__file__, '#D55E00', 's'),
            ('Dodecacode (BP-OSD)', dodecacode.__file__, '#009E73', 'o'),
            ('Dodecacode (lookup)', dodecacode_lookup.__file__, '#882255', 'P'),
            ('GSCX Distance 7', gscx_distance_7.__file__, '#332288', 'v'),
        ]

        fig, ax = plt.subplots(1, 1)

        for code_name, code_file, color, marker in codes:
            merge_paths = get_shard_merge_paths(files_in_dirs=[code_file])
            if not merge_paths:
                continue

            si_paths = {
                k: v for k, v in merge_paths.items()
                if '-1' not in str(k)
            }
            if not si_paths:
                continue

            rate_ler_map = defaultdict(list)
            for si_path in sorted(si_paths.keys()):
                stats = merge_csvs(input_paths=[si_path])
                for stat in stats:
                    per = stat.json_metadata['physical_error_rate']
                    ler = stat.errors / stat.shots if stat.shots > 0 else 0
                    rate_ler_map[per].append(ler)

            n_sis = len(si_paths)
            sorted_rates = []
            total_lers = []
            for rate in sorted(rate_ler_map.keys()):
                lers = rate_ler_map[rate]
                if len(lers) == n_sis:
                    total_ler = 1 - prod(1 - ler for ler in lers)
                    sorted_rates.append(rate)
                    total_lers.append(total_ler)

            ax.loglog(sorted_rates, total_lers,
                      marker=marker, color=color, label=code_name)

        ax.set_ylim(1e-10, 1)
        ax.set_xlim(5e-5)
        ax.grid()
        ax.set_title(r'Total Logical Error Rate of $\overline{CX}_{GSCX,\mathcal{Q}_1}$')
        ax.set_ylabel('Logical Error Rate')
        ax.set_xlabel('Physical Error Rate')
        ax.legend()

        output_path = Path(__file__).parent / 'threshold.pdf'
        fig.savefig(output_path)
        plt.show()


if __name__ == "__main__":
    Main().main()
