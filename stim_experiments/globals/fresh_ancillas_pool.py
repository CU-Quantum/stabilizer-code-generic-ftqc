from contextlib import contextmanager
from typing import Generator

from cirq import LineQubit


class FreshAncillasPool:
    # TODO add async locking

    _pool: list[LineQubit] = []
    _next_ancilla_num = 0

    @classmethod
    def set_first_ancilla_num(cls, first_ancilla_num: int):
        if first_ancilla_num < 0:
            raise ValueError("First ancilla number must be non-negative.")
        cls._pool = []
        cls._next_ancilla_num = first_ancilla_num

    @contextmanager
    def use_fresh_ancillas(self, num_ancillas: int) -> Generator[list[LineQubit], None, None]:
        ancillas = []
        while len(ancillas) < num_ancillas:
            if self._pool:
                ancillas.append(self._pool.pop())
            else:
                ancillas.append(LineQubit(self._next_ancilla_num))
                self.__class__._next_ancilla_num += 1

        yield ancillas

        for ancillas in reversed(ancillas):
            self._pool.append(ancillas)
