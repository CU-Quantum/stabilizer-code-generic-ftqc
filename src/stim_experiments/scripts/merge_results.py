from __future__ import annotations

from pathlib import Path
from typing import List

from sinter import CSV_HEADER, TaskStats

from stim_experiments.scripts.utilities import get_shard_merge_paths, merge_csvs


def write_csv(stats: List[TaskStats], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open('w') as f:
        print(CSV_HEADER, file=f)
        for s in stats:
            print(s.to_csv_line(), file=f)


def main():
    merge_paths = get_shard_merge_paths()
    for output_path, input_paths in merge_paths.items():
        stats = merge_csvs(input_paths)
        for input_path in input_paths:
            Path(input_path).unlink()
        write_csv(stats, output_path)


if __name__ == '__main__':
    main()
