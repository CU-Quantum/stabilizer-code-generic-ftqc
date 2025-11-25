from json import JSONEncoder

import sympy
from cirq.protocols.json_serialization import CirqEncoder


class CustomJsonEncoder(CirqEncoder):
    def default(self, o):
        if isinstance(o, sympy.And):
            return {'cirq_type': 'sympy.And', 'args': o.args}
        return super().default(o=o)
