from dataclasses import dataclass

from numpy._typing import NDArray


@dataclass
class CheckMatrixStandardized:
    matrix: NDArray[NDArray[bool]]
