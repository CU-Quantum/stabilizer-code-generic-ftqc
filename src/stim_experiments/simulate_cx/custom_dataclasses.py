from dataclasses import dataclass
from typing import Optional


@dataclass
class RunConfiguration:
    max_shots: int
    max_errors: int
    depolarization_probabilities: list[float]
    num_workers: int
    # Optional distributed sharding across multiple jobs/nodes (e.g., SLURM array)
    num_shards: int = 1
    shard_index: int = 0
    max_si: Optional[int] = None
    si: Optional[int] = None
