from re import escape

import pytest

from stim_experiments.custom_dataclasses.transformation_operation import \
    TransformationGate, TransformationOperation


class TestTransformationOperation:
    @pytest.mark.parametrize('gate, name', [
        (TransformationGate.X, 'X'),
        (TransformationGate.Z, 'Z')
    ])
    def test_control_on_single_qubit_operation_is_invalid(self, gate: TransformationGate, name: str):
        transformation_operation = TransformationOperation(
            gate=gate,
            target_qubit_index=0,
            control_qubit_index=1,
        )
        with pytest.raises(ValueError, match=escape("Single-qubit gates may have only a target qubit. "
                                                    f"Was given control index 1 for a(n) {name} gate.")):
            transformation_operation.validate()

    @pytest.mark.parametrize('gate, name', [
        (TransformationGate.CX, 'CX'),
        (TransformationGate.CZ, 'CZ')
    ])
    def test_no_control_on_two_qubit_operation_is_invalid(self, gate: TransformationGate, name: str):
        transformation_operation = TransformationOperation(
            gate=gate,
            target_qubit_index=0,
        )
        with pytest.raises(ValueError, match=escape("Double-qubit gates must have a control qubit. "
                                                    f"Was not given a control index for a(n) {name} gate.")):
            transformation_operation.validate()
