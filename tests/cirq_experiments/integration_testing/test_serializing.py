import pytest
import sympy
from cirq import to_json

from cirq_experiments.serialization.custom_json_encoder import CustomJsonEncoder


class TestSerializing:
    def test_serialize_sympy_add(self):
        expr = sympy.Symbol('x') + sympy.Symbol('y')
        to_json(expr)

    def test_serialize_sympy_eq(self):
        expr = sympy.Eq(sympy.Symbol('x'), sympy.Symbol('y'))
        to_json(expr)

    def test_serialize_sympy_and(self):
        expr = sympy.And(sympy.Eq(sympy.Symbol('x'), sympy.Symbol('y')), sympy.Eq(sympy.Symbol('a'), sympy.Symbol('b')))
        with pytest.raises(TypeError):
            to_json(expr)
        to_json(expr, cls=CustomJsonEncoder)
