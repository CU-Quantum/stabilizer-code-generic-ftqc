from __future__ import annotations

import argparse
import glob
from pathlib import Path
from typing import Iterable, List

from sinter import CSV_HEADER, stats_from_csv_files, plot_error_rate
from matplotlib import pyplot as plt


def merge_csvs(input_paths: Iterable[Path]) -> List['sinter.TaskStats']:
    # sinter.stats_from_csv_files will combine duplicate task rows (same strong_id)
    # by summing shots/errors/discards/etc. across files.
    return stats_from_csv_files(*input_paths)


def write_csv(stats: List['sinter.TaskStats'], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w') as f:
        print(CSV_HEADER, file=f)
        for s in stats:
            print(s.to_csv_line(), file=f)


def maybe_plot(stats: List['sinter.TaskStats'], title: str | None, ymin_order: int | None, output_pdf: Path | None) -> None:
    if output_pdf is None and title is None:
        return
    fig, ax = plt.subplots(1, 1)
    # Group into a single curve unless the caller wants to separate externally.
    plot_error_rate(
        ax=ax,
        stats=stats,
        group_func=lambda _: title or 'merged',
        x_func=lambda stat: stat.json_metadata.get('physical_error_rate', None),
    )
    ax.loglog()
    if ymin_order is not None:
        ax.set_ylim(1 * 10 ** -ymin_order, 1e-1)
    ax.grid()
    if title:
        ax.set_title(title)
    ax.set_ylabel('Logical Error Probability (per shot)')
    ax.set_xlabel('Physical Error Rate')
    ax.legend()
    if output_pdf is not None:
        output_pdf.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(output_pdf)
    else:
        plt.show()


def main():
    parser = argparse.ArgumentParser(description='Merge per-shard Sinter CSVs into a single combined CSV and optionally plot.')
    parser.add_argument('--glob', dest='glob_pattern', type=str, required=False,
                        help='Glob pattern to match input CSVs (e.g., "results/.../save_resume_*_shard*-of-*.csv").')
    parser.add_argument('--inputs', nargs='*', type=str, required=False,
                        help='Explicit list of input CSV file paths to merge.')
    parser.add_argument('--output', type=str, required=True,
                        help='Output combined CSV file path to write.')
    parser.add_argument('--plot-pdf', type=str, default=None,
                        help='Optional: write a PDF plot to this path using merged data.')
    parser.add_argument('--title', type=str, default=None,
                        help='Optional: title for the plot.')
    parser.add_argument('--ymin-order', type=int, default=None,
                        help='Optional: set ymin to 10^-order for the plot (e.g., 10 for 1e-10).')

    args = parser.parse_args()

    # Collect input paths
    input_paths: list[Path] = []
    if args.inputs:
        input_paths.extend(Path(p) for p in args.inputs)
    if args.glob_pattern:
        input_paths.extend(Path(p) for p in glob.glob(args.glob_pattern))
    # De-duplicate and ensure they exist
    input_paths = sorted({p.resolve() for p in input_paths if Path(p).exists()})
    if not input_paths:
        raise SystemExit('No input CSVs found. Provide --inputs and/or --glob.')

    stats = merge_csvs(input_paths)
    output_path = Path(args.output)
    write_csv(stats, output_path)

    if args.plot_pdf or args.title:
        maybe_plot(stats, title=args.title, ymin_order=args.ymin_order,
                   output_pdf=Path(args.plot_pdf) if args.plot_pdf else None)


if __name__ == '__main__':
    main()
