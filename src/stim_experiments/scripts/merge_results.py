from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Iterable, List

from sinter import CSV_HEADER, stats_from_csv_files

from stim_experiments.scripts import dodecacode, five_qubit


def merge_csvs(input_paths: Iterable[Path]) -> List['sinter.TaskStats']:
    return stats_from_csv_files(*input_paths)


def write_csv(stats: List['sinter.TaskStats'], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w') as f:
        print(CSV_HEADER, file=f)
        for s in stats:
            print(s.to_csv_line(), file=f)


def main():
    shard_dirs = [Path(five_qubit.__file__).parent, Path(dodecacode.__file__).parent]
    for shard_dir in shard_dirs:
        shard_filenames = list(shard_dir.glob('save_resume_*.csv'))
        merge_paths = defaultdict(list)
        for shard_filename in shard_filenames:
            output_path_pieces = shard_filename.name.split('.')[0].split('_')[:3]
            output_path = shard_filename.parent / f'{'_'.join(output_path_pieces)}.csv'
            merge_paths[output_path].append(str(shard_filename))
        for output_path, input_paths in merge_paths.items():
            stats = merge_csvs(input_paths)
            for input_path in input_paths:
                Path(input_path).unlink()
            write_csv(stats, output_path)


if __name__ == '__main__':
    main()
