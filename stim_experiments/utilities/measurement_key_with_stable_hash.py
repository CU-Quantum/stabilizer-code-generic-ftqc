from cirq import MeasurementKey


class MeasurementKeyWithStableHash(MeasurementKey):
    """
    The base class uses Python's built-in `hash` function.
    Python’s default hash for strings is randomized per interpreter session for security reasons,
    which causes differences across multiple processes when pickling.

    Computing hash every time rather than caching solves this.
    """
    def __hash__(self):
        return hash(str(self))
