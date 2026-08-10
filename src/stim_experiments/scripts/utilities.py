from collections import defaultdict
from pathlib import Path
from typing import Iterable, List, Optional

from sinter import TaskStats, stats_from_csv_files

from stim_experiments.scripts import dodecacode, five_qubit, golay, gsc_distance_7


def get_shard_merge_paths(files_in_dirs: Optional[list[str]] = None) -> dict[Path, list[Path]]:
    if files_in_dirs is None:
        files_in_dirs = [five_qubit.__file__, dodecacode.__file__, golay.__file__, gsc_distance_7.__file__]
    merge_paths = defaultdict(list)
    shard_dirs = [Path(file_in_dir).parent for file_in_dir in files_in_dirs]
    for shard_dir in shard_dirs:
        shard_filepaths = list(shard_dir.glob('save_resume_*.csv'))
        for shard_filepath in shard_filepaths:
            output_path_pieces = shard_filepath.name.split('.')[0].split('_')[:3]
            output_path = shard_filepath.parent / f'{'_'.join(output_path_pieces)}.csv'
            merge_paths[output_path].append(shard_filepath)
    return merge_paths


def merge_csvs(input_paths: Iterable[Path]) -> List[TaskStats]:
    return stats_from_csv_files(*input_paths)
