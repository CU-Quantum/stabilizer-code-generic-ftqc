from dataclasses import dataclass, field

from cirq import Circuit, MeasurementKey


@dataclass
class StateEncoding:
    circuit: Circuit
    measurement_keys: list[MeasurementKey] = field(default_factory=list)

    def __iter__(self):
        # TODO test this
        yield from self.circuit
