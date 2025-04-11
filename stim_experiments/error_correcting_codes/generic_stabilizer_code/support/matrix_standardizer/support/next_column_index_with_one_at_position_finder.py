from numpy._typing import NDArray


class NextColumnIndexWithOneAtPositionFinder:
    def __init__(self, matrix: NDArray[NDArray[bool]], row_index: int, column_index: int):
        self._matrix = matrix
        self._row_index = row_index
        self._column_index = column_index

    def get_column_index(self) -> int:
        start_index = self._column_index + 1
        index = next((i for i, x in enumerate(self._matrix[self._row_index, start_index:]) if x), None)
        if index is None:
            raise IndexError(f"Could not find column after column index {self._column_index} having value 1 at row {self._row_index}.")
        return start_index + index
