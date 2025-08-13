import cirq

from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCountPerShot
from stim_experiments.custom_dataclasses.noisy_operations_count import NoisyOperationsCount
from stim_experiments.conditions.verification_is_zero import VerificationIsZero
from stim_experiments.conditions.multiple_conditions import MultipleConditions
from stim_experiments.conditions.recovery_condition import RecoveryCondition


a = [([cirq.TaggedOperation(cirq.CircuitOperation(
    circuit=cirq.FrozenCircuit([
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(36)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(36)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(36), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(36), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_13d06e54c1a145bc815683d0a58d025e')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_13d06e54c1a145bc815683d0a58d025e')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(36), cirq.LineQubit(0)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(1)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(36), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(36)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(37)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(37)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(37), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(37), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_8882408eeccf4be485eb4364daf631cd')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_8882408eeccf4be485eb4364daf631cd')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(37), cirq.LineQubit(1)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(2)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(37), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(37)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(38)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(38)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(38), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(38), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_257ae834cfcc4a6eba4745721e179ce5')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_257ae834cfcc4a6eba4745721e179ce5')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(38), cirq.LineQubit(3)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(4)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(38), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(38)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(39)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(39)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(39), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(39), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_507c1fd7163c4d8db9208fe8ad08d398')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_507c1fd7163c4d8db9208fe8ad08d398')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(39), cirq.LineQubit(4)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(5)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(39), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(39)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(40)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(40)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(40), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(40), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_24f19dc453174146b5cde466cbb2b735')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_24f19dc453174146b5cde466cbb2b735')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(40), cirq.LineQubit(6)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(7)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(40), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(40)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(41)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(41)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(41), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(41), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_6475bb118ddf464d9aeb1df26d067647')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_6475bb118ddf464d9aeb1df26d067647')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(41), cirq.LineQubit(7)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(8)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(41), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(41)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(42)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                    cirq.ResetChannel()(cirq.LineQubit(46)),
                                    cirq.ResetChannel()(cirq.LineQubit(47)),
                                    cirq.ResetChannel()(cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(42)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(46)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(47)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(49)),
                                    cirq.ResetChannel()(cirq.LineQubit(50)),
                                    cirq.ResetChannel()(cirq.LineQubit(51)),
                                    cirq.ResetChannel()(cirq.LineQubit(52)),
                                    cirq.ResetChannel()(cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(49), key=cirq.MeasurementKey(name='VERIFICATION_a58dfe8577ac48fba567b509366085c9')),
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(50), key=cirq.MeasurementKey(name='VERIFICATION_a58dfe8577ac48fba567b509366085c9')),
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(51), key=cirq.MeasurementKey(name='VERIFICATION_a58dfe8577ac48fba567b509366085c9')),
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(52), key=cirq.MeasurementKey(name='VERIFICATION_a58dfe8577ac48fba567b509366085c9')),
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(53), key=cirq.MeasurementKey(name='VERIFICATION_a58dfe8577ac48fba567b509366085c9')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_a58dfe8577ac48fba567b509366085c9')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(0)),
                        cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(1)),
                        cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(2)),
                        cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(3)),
                        cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(4)),
                        cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(5)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(48)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(47)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(46)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(45)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(42)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(43)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                    cirq.ResetChannel()(cirq.LineQubit(46)),
                                    cirq.ResetChannel()(cirq.LineQubit(47)),
                                    cirq.ResetChannel()(cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(43)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(46)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(47)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(49)),
                                    cirq.ResetChannel()(cirq.LineQubit(50)),
                                    cirq.ResetChannel()(cirq.LineQubit(51)),
                                    cirq.ResetChannel()(cirq.LineQubit(52)),
                                    cirq.ResetChannel()(cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(49), key=cirq.MeasurementKey(name='VERIFICATION_84e5ea78f4fa45ac8a2c62f21aa59dd9')),
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(50), key=cirq.MeasurementKey(name='VERIFICATION_84e5ea78f4fa45ac8a2c62f21aa59dd9')),
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(51), key=cirq.MeasurementKey(name='VERIFICATION_84e5ea78f4fa45ac8a2c62f21aa59dd9')),
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(52), key=cirq.MeasurementKey(name='VERIFICATION_84e5ea78f4fa45ac8a2c62f21aa59dd9')),
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(53), key=cirq.MeasurementKey(name='VERIFICATION_84e5ea78f4fa45ac8a2c62f21aa59dd9')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_84e5ea78f4fa45ac8a2c62f21aa59dd9')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(3)),
                        cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(4)),
                        cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(5)),
                        cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(6)),
                        cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(7)),
                        cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(8)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(48)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(47)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(46)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(45)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(43)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(36), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_34a430fe75cc4a2494fa0ce8432d932b')),
                        cirq.measure(cirq.LineQubit(37), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4899c38a2d304b88be98a54d4902896f')),
                        cirq.measure(cirq.LineQubit(38), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_52beaa04ce024bfb9a9e3d3d7655447a')),
                        cirq.measure(cirq.LineQubit(39), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4bbb08d3c2ec44eeb2ef32b0a0bd5acf')),
                        cirq.measure(cirq.LineQubit(40), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_30ee47cdeddc4ca48f1a321634c9fbb9')),
                        cirq.measure(cirq.LineQubit(41), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_01e52bf3beab487d8e42764118198b8f')),
                        cirq.measure(cirq.LineQubit(42), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4f5f13b6161a4e62872405f872ed5069')),
                        cirq.measure(cirq.LineQubit(43), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4439dd3cafb44706b4abbc53d89317f0')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_34a430fe75cc4a2494fa0ce8432d932b'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4899c38a2d304b88be98a54d4902896f'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_52beaa04ce024bfb9a9e3d3d7655447a'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4bbb08d3c2ec44eeb2ef32b0a0bd5acf'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_30ee47cdeddc4ca48f1a321634c9fbb9'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_01e52bf3beab487d8e42764118198b8f'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4f5f13b6161a4e62872405f872ed5069'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_4439dd3cafb44706b4abbc53d89317f0'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 0, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 1, 0, 0])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 1, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 1, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 1, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_4538696a32554b5999706aaa73d8c6c7'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(42)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(44)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(46)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(48)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(39)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(40)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(37)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(50)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(41)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(52)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(43)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(45)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(36)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(47)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(51)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(38)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(49)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(53)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(36)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(36)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(36), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(36), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_003f53aa60b74965b9f5547f8c330837')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_003f53aa60b74965b9f5547f8c330837')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(36), cirq.LineQubit(9)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(10)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(36), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(36)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(37)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(37)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(37), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(37), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_f2ae20a08ef34d6094bd647970b2361d')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_f2ae20a08ef34d6094bd647970b2361d')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(37), cirq.LineQubit(10)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(11)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(37), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(37)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(38)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(38)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(38), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(38), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_4c0f69962e44455ca380c36a27640654')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_4c0f69962e44455ca380c36a27640654')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(38), cirq.LineQubit(12)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(13)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(38), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(38)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(39)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(39)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(39), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(39), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_602d56eb20aa4328a6ddec0b5e275d30')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_602d56eb20aa4328a6ddec0b5e275d30')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(39), cirq.LineQubit(13)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(14)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(39), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(39)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(40)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(40)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(40), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(40), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_d14a4e8ae2814d4a820b0ace9c003e35')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_d14a4e8ae2814d4a820b0ace9c003e35')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(40), cirq.LineQubit(15)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(16)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(40), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(40)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(41)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(41)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(41), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(41), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_84bc108737864ad2bcee14c7b3b7a36d')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_84bc108737864ad2bcee14c7b3b7a36d')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(41), cirq.LineQubit(16)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(17)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(41), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(41)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(42)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                    cirq.ResetChannel()(cirq.LineQubit(46)),
                                    cirq.ResetChannel()(cirq.LineQubit(47)),
                                    cirq.ResetChannel()(cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(42)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(46)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(47)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(49)),
                                    cirq.ResetChannel()(cirq.LineQubit(50)),
                                    cirq.ResetChannel()(cirq.LineQubit(51)),
                                    cirq.ResetChannel()(cirq.LineQubit(52)),
                                    cirq.ResetChannel()(cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(49), key=cirq.MeasurementKey(name='VERIFICATION_ac86a95d8d91464294b0a2108a512cc4')),
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(50), key=cirq.MeasurementKey(name='VERIFICATION_ac86a95d8d91464294b0a2108a512cc4')),
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(51), key=cirq.MeasurementKey(name='VERIFICATION_ac86a95d8d91464294b0a2108a512cc4')),
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(52), key=cirq.MeasurementKey(name='VERIFICATION_ac86a95d8d91464294b0a2108a512cc4')),
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(53), key=cirq.MeasurementKey(name='VERIFICATION_ac86a95d8d91464294b0a2108a512cc4')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_ac86a95d8d91464294b0a2108a512cc4')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(9)),
                        cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(10)),
                        cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(11)),
                        cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(12)),
                        cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(13)),
                        cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(14)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(48)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(47)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(46)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(45)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(42)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(43)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                    cirq.ResetChannel()(cirq.LineQubit(46)),
                                    cirq.ResetChannel()(cirq.LineQubit(47)),
                                    cirq.ResetChannel()(cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(43)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(46)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(47)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(49)),
                                    cirq.ResetChannel()(cirq.LineQubit(50)),
                                    cirq.ResetChannel()(cirq.LineQubit(51)),
                                    cirq.ResetChannel()(cirq.LineQubit(52)),
                                    cirq.ResetChannel()(cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(49), key=cirq.MeasurementKey(name='VERIFICATION_08ea19d460b841008c0d97a48478b907')),
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(50), key=cirq.MeasurementKey(name='VERIFICATION_08ea19d460b841008c0d97a48478b907')),
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(51), key=cirq.MeasurementKey(name='VERIFICATION_08ea19d460b841008c0d97a48478b907')),
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(52), key=cirq.MeasurementKey(name='VERIFICATION_08ea19d460b841008c0d97a48478b907')),
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(53), key=cirq.MeasurementKey(name='VERIFICATION_08ea19d460b841008c0d97a48478b907')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_08ea19d460b841008c0d97a48478b907')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(12)),
                        cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(13)),
                        cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(14)),
                        cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(15)),
                        cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(16)),
                        cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(17)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(48)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(47)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(46)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(45)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(43)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(36), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d249465e8b934c0c81ea84a667328ea1')),
                        cirq.measure(cirq.LineQubit(37), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_6ef1e2eeeebb4d1ba14d89178ede8e34')),
                        cirq.measure(cirq.LineQubit(38), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_053fc7aa984b483aad8569ae9ce7280e')),
                        cirq.measure(cirq.LineQubit(39), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_8ffcb071d05d4627a0842d35b3be4407')),
                        cirq.measure(cirq.LineQubit(40), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_7760b3fe93964fac9c2fa894467bfa92')),
                        cirq.measure(cirq.LineQubit(41), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_52d956c3490c4617882738c1b81d18c4')),
                        cirq.measure(cirq.LineQubit(42), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_f41cc02614154fd4835594be41c77e9e')),
                        cirq.measure(cirq.LineQubit(43), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_c9e653b1a4ba4bf29d37cfed8b3e8cd0')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d249465e8b934c0c81ea84a667328ea1'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_6ef1e2eeeebb4d1ba14d89178ede8e34'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_053fc7aa984b483aad8569ae9ce7280e'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_8ffcb071d05d4627a0842d35b3be4407'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_7760b3fe93964fac9c2fa894467bfa92'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_52d956c3490c4617882738c1b81d18c4'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_f41cc02614154fd4835594be41c77e9e'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_c9e653b1a4ba4bf29d37cfed8b3e8cd0'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(9)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 0, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(10)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(12)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(13)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(15)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(16)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 1, 0, 0])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 1, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(9)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(10)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(12)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(13)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(15)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(16)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 1, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 1, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(12)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(13)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(15)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(16)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(9)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(10)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(15)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(16)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(9)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(10)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(12)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(13)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_d036729a46994f84ba00769d7f80fda6'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(42)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(44)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(46)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(48)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(39)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(40)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(37)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(50)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(41)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(52)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(43)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(45)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(36)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(47)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(51)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(38)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(49)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(53)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(36)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(36)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(36), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(36), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_1ee3bc0eefab44409b9f7a6a6ba46e85')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_1ee3bc0eefab44409b9f7a6a6ba46e85')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(36), cirq.LineQubit(27)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(28)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(36), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(36)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(37)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(37)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(37), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(37), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_150c9455f1b440c7bbe4842b5398a774')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_150c9455f1b440c7bbe4842b5398a774')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(37), cirq.LineQubit(28)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(29)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(37), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(37)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(38)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(38)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(38), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(38), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_c24afe6f6da144d1a7fe9f99ed5ab5e5')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_c24afe6f6da144d1a7fe9f99ed5ab5e5')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(38), cirq.LineQubit(30)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(31)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(38), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(38)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(39)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(39)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(39), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(39), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_1930f5b997e34520b7d134923c9047fa')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_1930f5b997e34520b7d134923c9047fa')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(39), cirq.LineQubit(31)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(32)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(39), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(39)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(40)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(40)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(40), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(40), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_389657225720449fa0c2ee8b18779ea7')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_389657225720449fa0c2ee8b18779ea7')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(40), cirq.LineQubit(33)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(34)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(40), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(40)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(41)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(41)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(41), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(41), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(45), key=cirq.MeasurementKey(name='VERIFICATION_cb2ca208b2de40dc97e7c69a6a984c47')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_cb2ca208b2de40dc97e7c69a6a984c47')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(41), cirq.LineQubit(34)),
                        cirq.CZ(cirq.LineQubit(44), cirq.LineQubit(35)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(41), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(41)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(42)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                    cirq.ResetChannel()(cirq.LineQubit(46)),
                                    cirq.ResetChannel()(cirq.LineQubit(47)),
                                    cirq.ResetChannel()(cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(42)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(46)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(47)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(49)),
                                    cirq.ResetChannel()(cirq.LineQubit(50)),
                                    cirq.ResetChannel()(cirq.LineQubit(51)),
                                    cirq.ResetChannel()(cirq.LineQubit(52)),
                                    cirq.ResetChannel()(cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(49), key=cirq.MeasurementKey(name='VERIFICATION_cfa31870b46e4eccaac4e5555f5e35a1')),
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(50), key=cirq.MeasurementKey(name='VERIFICATION_cfa31870b46e4eccaac4e5555f5e35a1')),
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(51), key=cirq.MeasurementKey(name='VERIFICATION_cfa31870b46e4eccaac4e5555f5e35a1')),
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(52), key=cirq.MeasurementKey(name='VERIFICATION_cfa31870b46e4eccaac4e5555f5e35a1')),
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(53), key=cirq.MeasurementKey(name='VERIFICATION_cfa31870b46e4eccaac4e5555f5e35a1')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_cfa31870b46e4eccaac4e5555f5e35a1')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(42), cirq.LineQubit(27)),
                        cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(28)),
                        cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(29)),
                        cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(30)),
                        cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(31)),
                        cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(32)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(48)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(47)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(46)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(45)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(42), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(42)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(43)),
                                    cirq.ResetChannel()(cirq.LineQubit(44)),
                                    cirq.ResetChannel()(cirq.LineQubit(45)),
                                    cirq.ResetChannel()(cirq.LineQubit(46)),
                                    cirq.ResetChannel()(cirq.LineQubit(47)),
                                    cirq.ResetChannel()(cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(43)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(44)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(45)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(46)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(47)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(48)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(49)),
                                    cirq.ResetChannel()(cirq.LineQubit(50)),
                                    cirq.ResetChannel()(cirq.LineQubit(51)),
                                    cirq.ResetChannel()(cirq.LineQubit(52)),
                                    cirq.ResetChannel()(cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(49)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(49), key=cirq.MeasurementKey(name='VERIFICATION_1cce339f04234fb1a22566757ed9439f')),
                                    cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(50)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(50), key=cirq.MeasurementKey(name='VERIFICATION_1cce339f04234fb1a22566757ed9439f')),
                                    cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(51)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(51), key=cirq.MeasurementKey(name='VERIFICATION_1cce339f04234fb1a22566757ed9439f')),
                                    cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(52)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(52), key=cirq.MeasurementKey(name='VERIFICATION_1cce339f04234fb1a22566757ed9439f')),
                                    cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(53)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(53), key=cirq.MeasurementKey(name='VERIFICATION_1cce339f04234fb1a22566757ed9439f')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_1cce339f04234fb1a22566757ed9439f')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(43), cirq.LineQubit(30)),
                        cirq.CNOT(cirq.LineQubit(44), cirq.LineQubit(31)),
                        cirq.CNOT(cirq.LineQubit(45), cirq.LineQubit(32)),
                        cirq.CNOT(cirq.LineQubit(46), cirq.LineQubit(33)),
                        cirq.CNOT(cirq.LineQubit(47), cirq.LineQubit(34)),
                        cirq.CNOT(cirq.LineQubit(48), cirq.LineQubit(35)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(48)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(47)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(46)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(45)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(43), cirq.LineQubit(44)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(43)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(36), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_5318129d79f54f97969dfeb3d2cacf10')),
                        cirq.measure(cirq.LineQubit(37), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_f8261c057c40476996e3f0aa5079fa62')),
                        cirq.measure(cirq.LineQubit(38), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_a0bd71580a5d41c6ae76d4971d0643a8')),
                        cirq.measure(cirq.LineQubit(39), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_7e33a9452b99450c91dd6c7c72d7c00a')),
                        cirq.measure(cirq.LineQubit(40), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_2306c1c9a11d4c69a4cc1d2b9e40fedd')),
                        cirq.measure(cirq.LineQubit(41), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_46259474c67149fc85a70fa710b2c1c9')),
                        cirq.measure(cirq.LineQubit(42), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_3976bdafe8e444b496ffc29398554ed1')),
                        cirq.measure(cirq.LineQubit(43), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_da66b49a44484d55a3789c2bd0c1ed90')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_5318129d79f54f97969dfeb3d2cacf10'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_f8261c057c40476996e3f0aa5079fa62'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_a0bd71580a5d41c6ae76d4971d0643a8'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_7e33a9452b99450c91dd6c7c72d7c00a'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_2306c1c9a11d4c69a4cc1d2b9e40fedd'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_46259474c67149fc85a70fa710b2c1c9'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_3976bdafe8e444b496ffc29398554ed1'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_da66b49a44484d55a3789c2bd0c1ed90'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(27)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 0, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(28)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(30)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(31)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(33)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(34)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 1, 0, 0])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 1, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(27)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(28)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(30)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(31)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(33)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(34)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 1, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 1, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(30)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(31)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(33)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(34)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(27)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(28)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(33)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(34)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(27)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(28)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(30)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(31)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(29)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(35)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(32)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_67ac6323cc084910a2f55d08e5134127'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.Y(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(42)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(44)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(46)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(48)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(39)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(40)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(37)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(50)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(41)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(52)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(43)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(45)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(36)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(47)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(51)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(38)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(49)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(53)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
    ]),
), 'CORRECTION_ROUND'), cirq.TaggedOperation(cirq.Y(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit')], [156, 11]), ([cirq.TaggedOperation(cirq.Z(cirq.LineQubit(52)), 'NoisyChannel','NoisyChannel_OneQubit')], [181])]

b = NoisyOperationsCountPerCorrectionRound(counts=[NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=810, paths=[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [37], [38], [39], [40], [41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69], [70], [71], [72], [73], [74], [75], [76], [77], [78], [79], [80], [81], [82], [83], [84], [85], [86], [87], [88], [89], [90], [91], [92], [93], [94], [95], [96], [97], [98], [99], [100], [101], [102], [103], [104], [105], [106], [107], [108], [109], [111], [112], [113], [114], [115], [116], [117], [118], [119], [120], [121], [122], [123], [124], [125], [126], [127], [128], [129], [130], [131], [132], [133], [134], [135], [136], [137], [138], [139], [140], [141], [142], [143], [144], [145], [146], [147], [148], [149], [150], [151], [152], [153], [154], [155], [156], [157], [158], [159], [160], [161], [162], [163], [164], [166], [167], [168], [169], [170], [171], [172], [173], [174], [175], [176], [177], [178], [179], [180], [181], [182], [183], [184], [185], [186], [187], [188], [189], [190], [191], [192], [193], [194], [195], [196], [197], [198], [199], [200], [201], [202], [203], [204], [205], [206], [207], [208], [209], [210], [211], [212], [213], [214], [215], [216], [217], [218], [219], [221], [222], [223], [224], [225], [226], [227], [228], [229], [230], [231], [232], [233], [234], [235], [236], [237], [238], [239], [240], [241], [242], [243], [244], [245], [246], [247], [248], [249], [250], [251], [252], [253], [254], [255], [256], [257], [258], [259], [260], [261], [262], [263], [264], [265], [266], [267], [268], [269], [270], [271], [272], [273], [274], [276], [277], [278], [279], [280], [281], [282], [283], [284], [285], [286], [287], [288], [289], [290], [291], [292], [293], [294], [295], [296], [297], [298], [299], [300], [301], [302], [303], [304], [305], [306], [307], [308], [309], [310], [311], [312], [313], [314], [315], [316], [317], [318], [319], [320], [321], [322], [323], [324], [325], [326], [327], [328], [329], [331], [332], [333], [334], [335], [336], [337], [338], [339], [340], [341], [342], [343], [344], [345], [346], [347], [348], [349], [350], [351], [352], [353], [354], [355], [356], [357], [358], [359], [360], [361], [362], [363], [364], [365], [366], [367], [368], [369], [370], [371], [372], [373], [374], [375], [376], [377], [378], [379], [380], [381], [382], [383], [384], [386], [387], [388], [389], [390], [391], [392], [393], [394], [395], [396], [397], [398], [399], [400], [401], [402], [403], [404], [405], [406], [407], [408], [409], [410], [411], [412], [413], [414], [415], [416], [417], [418], [419], [420], [421], [422], [423], [424], [425], [426], [427], [428], [429], [430], [431], [432], [433], [434], [435], [436], [437], [438], [439], [441], [442], [443], [444], [445], [446], [447], [448], [449], [450], [451], [452], [453], [454], [455], [456], [457], [458], [459], [460], [461], [462], [463], [464], [465], [466], [467], [468], [469], [470], [471], [472], [473], [474], [475], [476], [477], [478], [479], [480], [481], [482], [483], [484], [485], [486], [487], [488], [489], [490], [491], [492], [493], [494], [496], [497], [498], [499], [500], [501], [502], [503], [504], [505], [506], [507], [508], [509], [510], [511], [512], [513], [514], [515], [516], [517], [518], [519], [520], [521], [522], [524], [525], [526], [527], [528], [529], [530], [531], [532], [533], [534], [535], [536], [537], [538], [539], [540], [541], [542], [543], [544], [545], [546], [547], [548], [549], [550], [551], [552], [553], [554], [555], [556], [557], [558], [559], [560], [561], [562], [563], [564], [565], [566], [567], [568], [569], [570], [571], [572], [573], [574], [575], [576], [577], [578, 1], [578, 2], [578, 3], [578, 4], [578, 5], [578, 6], [578, 7], [578, 8], [578, 9], [578, 10], [578, 11], [578, 12], [578, 13], [578, 14], [578, 15], [578, 16], [578, 17], [578, 18], [578, 19], [578, 20], [578, 21], [578, 22], [578, 23], [578, 24], [578, 25], [578, 26], [578, 27], [578, 29], [578, 30], [578, 31], [578, 32], [578, 33], [578, 34], [578, 35], [578, 36], [578, 37], [578, 38], [578, 39], [578, 40], [578, 41], [578, 42], [578, 43], [578, 44], [578, 45], [578, 46], [578, 47], [578, 48], [578, 49], [578, 50], [578, 51], [578, 52], [578, 53], [578, 54], [578, 55], [578, 56], [578, 57], [578, 58], [578, 59], [578, 60], [578, 61], [578, 62], [578, 63], [578, 64], [578, 65], [578, 66], [578, 67], [578, 68], [578, 69], [578, 70], [578, 71], [578, 72], [578, 73], [578, 74], [578, 75], [578, 76], [578, 77], [578, 78], [578, 79], [578, 80], [578, 81], [578, 82], [578, 84], [578, 85], [578, 86], [578, 87], [578, 88], [578, 89], [578, 90], [578, 91], [578, 92], [578, 93], [578, 94], [578, 95], [578, 96], [578, 97], [578, 98], [578, 99], [578, 100], [578, 101], [578, 102], [578, 103], [578, 104], [578, 105], [578, 106], [578, 107], [578, 108], [578, 109], [578, 110], [578, 112], [578, 113], [578, 114], [578, 115], [578, 116], [578, 117], [578, 118], [578, 119], [578, 120], [578, 121], [578, 122], [578, 123], [578, 124], [578, 125], [578, 126], [578, 127], [578, 128], [578, 129], [578, 130], [578, 131], [578, 132], [578, 133], [578, 134], [578, 135], [578, 136], [578, 137], [578, 138], [578, 139], [578, 140], [578, 141], [578, 142], [578, 143], [578, 144], [578, 145], [578, 146], [578, 147], [578, 148], [578, 149], [578, 150], [578, 151], [578, 152], [578, 153], [578, 154], [578, 155], [578, 156], [578, 157], [578, 158], [578, 159], [578, 160], [578, 161], [578, 162], [578, 163], [578, 164], [578, 165], [578, 167], [578, 168], [578, 169], [578, 170], [578, 171], [578, 172], [578, 173], [578, 174], [578, 175], [578, 176], [578, 177], [578, 178], [578, 179], [578, 180], [578, 181], [578, 182], [578, 183], [578, 184], [578, 185], [578, 186], [578, 187], [578, 188], [578, 189], [578, 190], [578, 191], [578, 192], [578, 193], [578, 195], [578, 196], [578, 197], [578, 198], [578, 199], [578, 200], [578, 201], [578, 202], [578, 203], [578, 204], [578, 205], [578, 206], [578, 207], [578, 208], [578, 209], [578, 210], [578, 211], [578, 212], [578, 213], [578, 214], [578, 215], [578, 216], [578, 217], [578, 218], [578, 219], [578, 220], [578, 221], [578, 222], [578, 223], [578, 224], [578, 225], [578, 226], [578, 227], [578, 228], [578, 229], [578, 230], [578, 231], [578, 232], [578, 233], [578, 234], [578, 235], [578, 236], [578, 237], [578, 238], [578, 239], [578, 240], [578, 241], [578, 242], [578, 243], [578, 244], [578, 245], [578, 246], [578, 247], [578, 248]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=798, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=891, paths=[[580], [581], [582], [583], [584], [585], [586], [587], [588], [589], [590], [591], [592], [593], [594], [595], [596], [597], [598], [599], [600], [601], [602], [603], [604], [605], [606], [607], [608], [609], [610], [611], [612], [613], [614], [615], [616], [617], [618], [619], [620], [621], [622], [623], [624], [625], [626], [627], [628], [629], [630], [631], [632], [633], [635], [636], [637], [638], [639], [640], [641], [642], [643], [644], [645], [646], [647], [648], [649], [650], [651], [652], [653], [654], [655], [656], [657], [658], [659], [660], [661], [662], [663], [664], [665], [666], [667], [668], [669], [670], [671], [672], [673], [674], [675], [676], [677], [678], [679], [680], [681], [682], [683], [684], [685], [686], [687], [688], [690], [691], [692], [693], [694], [695], [696], [697], [698], [699], [700], [701], [702], [703], [704], [705], [706], [707], [708], [709], [710], [711], [712], [713], [714], [715], [716], [717], [718], [719], [720], [721], [722], [723], [724], [725], [726], [727], [728], [729], [730], [731], [732], [733], [734], [735], [736], [737], [738], [739], [740], [741], [742], [743], [745], [746], [747], [748], [749], [750], [751], [752], [753], [754], [755], [756], [757], [758], [759], [760], [761], [762], [763], [764], [765], [766], [767], [768], [769], [770], [771], [772], [773], [774], [775], [776], [777], [778], [779], [780], [781], [782], [783], [784], [785], [786], [787], [788], [789], [790], [791], [792], [793], [794], [795], [796], [797], [798], [800], [801], [802], [803], [804], [805], [806], [807], [808], [809], [810], [811], [812], [813], [814], [815], [816], [817], [818], [819], [820], [821], [822], [823], [824], [825], [826], [827], [828], [829], [830], [831], [832], [833], [834], [835], [836], [837], [838], [839], [840], [841], [842], [843], [844], [845], [846], [847], [848], [849], [850], [851], [852], [853], [855], [856], [857], [858], [859], [860], [861], [862], [863], [864], [865], [866], [867], [868], [869], [870], [871], [872], [873], [874], [875], [876], [877], [878], [879], [880], [881], [882], [883], [884], [885], [886], [887], [888], [889], [890], [891], [892], [893], [894], [895], [896], [897], [898], [899], [900], [901], [902], [903], [904], [905], [906], [907], [908], [910], [911], [912], [913], [914], [915], [916], [917], [918], [919], [920], [921], [922], [923], [924], [925], [926], [927], [928], [929], [930], [931], [932], [933], [934], [935], [936], [937], [938], [939], [940], [941], [942], [943], [944], [945], [946], [947], [948], [949], [950], [951], [952], [953], [954], [955], [956], [957], [958], [959], [960], [961], [962], [963], [965], [966], [967], [968], [969], [970], [971], [972], [973], [974], [975], [976], [977], [978], [979], [980], [981], [982], [983], [984], [985], [986], [987], [988], [989], [990], [991], [992], [993], [994], [995], [996], [997], [998], [999], [1000], [1001], [1002], [1003], [1004], [1005], [1006], [1007], [1008], [1009], [1010], [1011], [1012], [1013], [1014], [1015], [1016], [1017], [1018], [1020], [1021], [1022], [1023], [1024], [1025], [1026], [1027], [1028], [1029], [1030], [1031], [1032], [1033], [1034], [1035], [1036], [1037], [1038], [1039], [1040], [1041], [1042], [1043], [1044], [1045], [1046], [1047], [1048], [1049], [1050], [1051], [1052], [1053], [1054], [1055], [1056], [1057], [1058], [1059], [1060], [1061], [1062], [1063], [1064], [1065], [1066], [1067], [1068], [1069], [1070], [1071], [1072], [1073], [1075], [1076], [1077], [1078], [1079], [1080], [1081], [1082], [1083], [1084], [1085], [1086], [1087], [1088], [1089], [1090], [1091], [1092], [1093], [1094], [1095], [1096], [1097], [1098], [1099], [1100], [1101], [1103], [1104], [1105], [1106], [1107], [1108], [1109], [1110], [1111], [1112], [1113], [1114], [1115], [1116], [1117], [1118], [1119], [1120], [1121], [1122], [1123], [1124], [1125], [1126], [1127], [1128], [1129], [1130], [1131], [1132], [1133], [1134], [1135], [1136], [1137], [1138], [1139], [1140], [1141], [1142], [1143], [1144], [1145], [1146], [1147], [1148], [1149], [1150], [1151], [1152], [1153], [1154], [1155], [1156], [1157, 1], [1157, 2], [1157, 3], [1157, 4], [1157, 5], [1157, 6], [1157, 7], [1157, 8], [1157, 9], [1157, 10], [1157, 11], [1157, 12], [1157, 13], [1157, 14], [1157, 15], [1157, 16], [1157, 17], [1157, 18], [1157, 19], [1157, 20], [1157, 21], [1157, 22], [1157, 23], [1157, 24], [1157, 25], [1157, 26], [1157, 27], [1157, 29], [1157, 30], [1157, 31], [1157, 32], [1157, 33], [1157, 34], [1157, 35], [1157, 36], [1157, 37], [1157, 38], [1157, 39], [1157, 40], [1157, 41], [1157, 42], [1157, 43], [1157, 44], [1157, 45], [1157, 46], [1157, 47], [1157, 48], [1157, 49], [1157, 50], [1157, 51], [1157, 52], [1157, 53], [1157, 54], [1157, 55], [1157, 56], [1157, 57], [1157, 58], [1157, 59], [1157, 60], [1157, 61], [1157, 62], [1157, 63], [1157, 64], [1157, 65], [1157, 66], [1157, 67], [1157, 68], [1157, 69], [1157, 70], [1157, 71], [1157, 72], [1157, 73], [1157, 74], [1157, 75], [1157, 76], [1157, 77], [1157, 78], [1157, 79], [1157, 80], [1157, 81], [1157, 82], [1157, 84], [1157, 85], [1157, 86], [1157, 87], [1157, 88], [1157, 89], [1157, 90], [1157, 91], [1157, 92], [1157, 93], [1157, 94], [1157, 95], [1157, 96], [1157, 97], [1157, 98], [1157, 99], [1157, 100], [1157, 101], [1157, 102], [1157, 103], [1157, 104], [1157, 105], [1157, 106], [1157, 107], [1157, 108], [1157, 109], [1157, 110], [1157, 112], [1157, 113], [1157, 114], [1157, 115], [1157, 116], [1157, 117], [1157, 118], [1157, 119], [1157, 120], [1157, 121], [1157, 122], [1157, 123], [1157, 124], [1157, 125], [1157, 126], [1157, 127], [1157, 128], [1157, 129], [1157, 130], [1157, 131], [1157, 132], [1157, 133], [1157, 134], [1157, 135], [1157, 136], [1157, 137], [1157, 138], [1157, 139], [1157, 140], [1157, 141], [1157, 142], [1157, 143], [1157, 144], [1157, 145], [1157, 146], [1157, 147], [1157, 148], [1157, 149], [1157, 150], [1157, 151], [1157, 152], [1157, 153], [1157, 154], [1157, 155], [1157, 156], [1157, 157], [1157, 158], [1157, 159], [1157, 160], [1157, 161], [1157, 162], [1157, 163], [1157, 164], [1157, 165], [1157, 167], [1157, 168], [1157, 169], [1157, 170], [1157, 171], [1157, 172], [1157, 173], [1157, 174], [1157, 175], [1157, 176], [1157, 177], [1157, 178], [1157, 179], [1157, 180], [1157, 181], [1157, 182], [1157, 183], [1157, 184], [1157, 185], [1157, 186], [1157, 187], [1157, 188], [1157, 189], [1157, 190], [1157, 191], [1157, 192], [1157, 193], [1157, 195], [1157, 196], [1157, 197], [1157, 198], [1157, 199], [1157, 200], [1157, 201], [1157, 202], [1157, 203], [1157, 204], [1157, 205], [1157, 206], [1157, 207], [1157, 208], [1157, 209], [1157, 210], [1157, 211], [1157, 212], [1157, 213], [1157, 214], [1157, 215], [1157, 216], [1157, 217], [1157, 218], [1157, 219], [1157, 220], [1157, 221], [1157, 222], [1157, 223], [1157, 224], [1157, 225], [1157, 226], [1157, 227], [1157, 228], [1157, 229], [1157, 230], [1157, 231], [1157, 232], [1157, 233], [1157, 234], [1157, 235], [1157, 236], [1157, 237], [1157, 238], [1157, 239], [1157, 240], [1157, 241], [1157, 242], [1157, 243], [1157, 244], [1157, 245], [1157, 246], [1157, 247], [1157, 248], [1157, 250], [1157, 251], [1157, 252], [1157, 253], [1157, 254], [1157, 255], [1157, 256], [1157, 257], [1157, 258], [1157, 259], [1157, 260], [1157, 261], [1157, 262], [1157, 263], [1157, 264], [1157, 265], [1157, 266], [1157, 267], [1157, 268], [1157, 269], [1157, 270], [1157, 271], [1157, 272], [1157, 273], [1157, 274], [1157, 275], [1157, 276], [1157, 278], [1157, 279], [1157, 280], [1157, 281], [1157, 282], [1157, 283], [1157, 284], [1157, 285], [1157, 286], [1157, 287], [1157, 288], [1157, 289], [1157, 290], [1157, 291], [1157, 292], [1157, 293], [1157, 294], [1157, 295], [1157, 296], [1157, 297], [1157, 298], [1157, 299], [1157, 300], [1157, 301], [1157, 302], [1157, 303], [1157, 304], [1157, 305], [1157, 306], [1157, 307], [1157, 308], [1157, 309], [1157, 310], [1157, 311], [1157, 312], [1157, 313], [1157, 314], [1157, 315], [1157, 316], [1157, 317], [1157, 318], [1157, 319], [1157, 320], [1157, 321], [1157, 322], [1157, 323], [1157, 324], [1157, 325], [1157, 326], [1157, 327], [1157, 328], [1157, 329], [1157, 330], [1157, 331]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=879, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=864, paths=[[1167], [1168], [1169], [1170], [1171], [1172], [1173], [1174], [1175], [1176], [1177], [1178], [1179], [1180], [1181], [1182], [1183], [1184], [1185], [1186], [1187], [1188], [1189], [1190], [1191], [1192], [1193], [1194], [1195], [1196], [1197], [1198], [1199], [1200], [1201], [1202], [1203], [1204], [1205], [1206], [1207], [1208], [1209], [1210], [1211], [1212], [1213], [1214], [1215], [1216], [1217], [1218], [1219], [1220], [1222], [1223], [1224], [1225], [1226], [1227], [1228], [1229], [1230], [1231], [1232], [1233], [1234], [1235], [1236], [1237], [1238], [1239], [1240], [1241], [1242], [1243], [1244], [1245], [1246], [1247], [1248], [1249], [1250], [1251], [1252], [1253], [1254], [1255], [1256], [1257], [1258], [1259], [1260], [1261], [1262], [1263], [1264], [1265], [1266], [1267], [1268], [1269], [1270], [1271], [1272], [1273], [1274], [1275], [1277], [1278], [1279], [1280], [1281], [1282], [1283], [1284], [1285], [1286], [1287], [1288], [1289], [1290], [1291], [1292], [1293], [1294], [1295], [1296], [1297], [1298], [1299], [1300], [1301], [1302], [1303], [1304], [1305], [1306], [1307], [1308], [1309], [1310], [1311], [1312], [1313], [1314], [1315], [1316], [1317], [1318], [1319], [1320], [1321], [1322], [1323], [1324], [1325], [1326], [1327], [1328], [1329], [1330], [1332], [1333], [1334], [1335], [1336], [1337], [1338], [1339], [1340], [1341], [1342], [1343], [1344], [1345], [1346], [1347], [1348], [1349], [1350], [1351], [1352], [1353], [1354], [1355], [1356], [1357], [1358], [1359], [1360], [1361], [1362], [1363], [1364], [1365], [1366], [1367], [1368], [1369], [1370], [1371], [1372], [1373], [1374], [1375], [1376], [1377], [1378], [1379], [1380], [1381], [1382], [1383], [1384], [1385], [1387], [1388], [1389], [1390], [1391], [1392], [1393], [1394], [1395], [1396], [1397], [1398], [1399], [1400], [1401], [1402], [1403], [1404], [1405], [1406], [1407], [1408], [1409], [1410], [1411], [1412], [1413], [1414], [1415], [1416], [1417], [1418], [1419], [1420], [1421], [1422], [1423], [1424], [1425], [1426], [1427], [1428], [1429], [1430], [1431], [1432], [1433], [1434], [1435], [1436], [1437], [1438], [1439], [1440], [1442], [1443], [1444], [1445], [1446], [1447], [1448], [1449], [1450], [1451], [1452], [1453], [1454], [1455], [1456], [1457], [1458], [1459], [1460], [1461], [1462], [1463], [1464], [1465], [1466], [1467], [1468], [1469], [1470], [1471], [1472], [1473], [1474], [1475], [1476], [1477], [1478], [1479], [1480], [1481], [1482], [1483], [1484], [1485], [1486], [1487], [1488], [1489], [1490], [1491], [1492], [1493], [1494], [1495], [1497], [1498], [1499], [1500], [1501], [1502], [1503], [1504], [1505], [1506], [1507], [1508], [1509], [1510], [1511], [1512], [1513], [1514], [1515], [1516], [1517], [1518], [1519], [1520], [1521], [1522], [1523], [1524], [1525], [1526], [1527], [1528], [1529], [1530], [1531], [1532], [1533], [1534], [1535], [1536], [1537], [1538], [1539], [1540], [1541], [1542], [1543], [1544], [1545], [1546], [1547], [1548], [1549], [1550], [1552], [1553], [1554], [1555], [1556], [1557], [1558], [1559], [1560], [1561], [1562], [1563], [1564], [1565], [1566], [1567], [1568], [1569], [1570], [1571], [1572], [1573], [1574], [1575], [1576], [1577], [1578], [1579], [1580], [1581], [1582], [1583], [1584], [1585], [1586], [1587], [1588], [1589], [1590], [1591], [1592], [1593], [1594], [1595], [1596], [1597], [1598], [1599], [1600], [1601], [1602], [1603], [1604], [1605], [1607], [1608], [1609], [1610], [1611], [1612], [1613], [1614], [1615], [1616], [1617], [1618], [1619], [1620], [1621], [1622], [1623], [1624], [1625], [1626], [1627], [1628], [1629], [1630], [1631], [1632], [1633], [1634], [1635], [1636], [1637], [1638], [1639], [1640], [1641], [1642], [1643], [1644], [1645], [1646], [1647], [1648], [1649], [1650], [1651], [1652], [1653], [1654], [1655], [1656], [1657], [1658], [1659], [1660], [1662], [1663], [1664], [1665], [1666], [1667], [1668], [1669], [1670], [1671], [1672], [1673], [1674], [1675], [1676], [1677], [1678], [1679], [1680], [1681], [1682], [1683], [1684], [1685], [1686], [1687], [1688], [1689], [1690], [1691], [1692], [1693], [1694], [1695], [1696], [1697], [1698], [1699], [1700], [1701], [1702], [1703], [1704], [1705], [1706], [1707], [1708], [1709], [1710], [1711], [1712], [1713], [1714], [1715], [1717], [1718], [1719], [1720], [1721], [1722], [1723], [1724], [1725], [1726], [1727], [1728], [1729], [1730], [1731], [1732], [1733], [1734], [1735], [1736], [1737], [1738], [1739], [1740], [1741], [1742], [1743], [1745], [1746], [1747], [1748], [1749], [1750], [1751], [1752], [1753], [1754], [1755], [1756], [1757], [1758], [1759], [1760], [1761], [1762], [1763], [1764], [1765], [1766], [1767], [1768], [1769], [1770], [1771], [1772], [1773], [1774], [1775], [1776], [1777], [1778], [1779], [1780], [1781], [1782], [1783], [1784], [1785], [1786], [1787], [1788], [1789], [1790], [1791], [1792], [1793], [1794], [1795], [1796], [1797], [1798], [1799, 1], [1799, 2], [1799, 3], [1799, 4], [1799, 5], [1799, 6], [1799, 7], [1799, 8], [1799, 9], [1799, 10], [1799, 11], [1799, 12], [1799, 13], [1799, 14], [1799, 15], [1799, 16], [1799, 17], [1799, 18], [1799, 19], [1799, 20], [1799, 21], [1799, 22], [1799, 23], [1799, 24], [1799, 25], [1799, 26], [1799, 27], [1799, 29], [1799, 30], [1799, 31], [1799, 32], [1799, 33], [1799, 34], [1799, 35], [1799, 36], [1799, 37], [1799, 38], [1799, 39], [1799, 40], [1799, 41], [1799, 42], [1799, 43], [1799, 44], [1799, 45], [1799, 46], [1799, 47], [1799, 48], [1799, 49], [1799, 50], [1799, 51], [1799, 52], [1799, 53], [1799, 54], [1799, 55], [1799, 56], [1799, 57], [1799, 58], [1799, 59], [1799, 60], [1799, 61], [1799, 62], [1799, 63], [1799, 64], [1799, 65], [1799, 66], [1799, 67], [1799, 68], [1799, 69], [1799, 70], [1799, 71], [1799, 72], [1799, 73], [1799, 74], [1799, 75], [1799, 76], [1799, 77], [1799, 78], [1799, 79], [1799, 80], [1799, 81], [1799, 82], [1799, 84], [1799, 85], [1799, 86], [1799, 87], [1799, 88], [1799, 89], [1799, 90], [1799, 91], [1799, 92], [1799, 93], [1799, 94], [1799, 95], [1799, 96], [1799, 97], [1799, 98], [1799, 99], [1799, 100], [1799, 101], [1799, 102], [1799, 103], [1799, 104], [1799, 105], [1799, 106], [1799, 107], [1799, 108], [1799, 109], [1799, 110], [1799, 112], [1799, 113], [1799, 114], [1799, 115], [1799, 116], [1799, 117], [1799, 118], [1799, 119], [1799, 120], [1799, 121], [1799, 122], [1799, 123], [1799, 124], [1799, 125], [1799, 126], [1799, 127], [1799, 128], [1799, 129], [1799, 130], [1799, 131], [1799, 132], [1799, 133], [1799, 134], [1799, 135], [1799, 136], [1799, 137], [1799, 138], [1799, 139], [1799, 140], [1799, 141], [1799, 142], [1799, 143], [1799, 144], [1799, 145], [1799, 146], [1799, 147], [1799, 148], [1799, 149], [1799, 150], [1799, 151], [1799, 152], [1799, 153], [1799, 154], [1799, 155], [1799, 156], [1799, 157], [1799, 158], [1799, 159], [1799, 160], [1799, 161], [1799, 162], [1799, 163], [1799, 164], [1799, 165], [1799, 167], [1799, 168], [1799, 169], [1799, 170], [1799, 171], [1799, 172], [1799, 173], [1799, 174], [1799, 175], [1799, 176], [1799, 177], [1799, 178], [1799, 179], [1799, 180], [1799, 181], [1799, 182], [1799, 183], [1799, 184], [1799, 185], [1799, 186], [1799, 187], [1799, 188], [1799, 189], [1799, 190], [1799, 191], [1799, 192], [1799, 193], [1799, 195], [1799, 196], [1799, 197], [1799, 198], [1799, 199], [1799, 200], [1799, 201], [1799, 202], [1799, 203], [1799, 204], [1799, 205], [1799, 206], [1799, 207], [1799, 208], [1799, 209], [1799, 210], [1799, 211], [1799, 212], [1799, 213], [1799, 214], [1799, 215], [1799, 216], [1799, 217], [1799, 218], [1799, 219], [1799, 220], [1799, 221], [1799, 222], [1799, 223], [1799, 224], [1799, 225], [1799, 226], [1799, 227], [1799, 228], [1799, 229], [1799, 230], [1799, 231], [1799, 232], [1799, 233], [1799, 234], [1799, 235], [1799, 236], [1799, 237], [1799, 238], [1799, 239], [1799, 240], [1799, 241], [1799, 242], [1799, 243], [1799, 244], [1799, 245], [1799, 246], [1799, 247], [1799, 248]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=852, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[1803], [1804], [1805], [1806], [1807], [1808], [1809], [1810], [1811], [1812], [1813], [1814], [1815], [1816], [1817], [1818], [1819], [1820], [1821], [1822], [1823], [1824], [1825], [1826], [1827], [1828], [1829], [1830], [1831], [1832], [1833], [1834], [1835], [1836], [1837], [1838], [1839], [1840], [1841], [1842], [1843], [1844], [1845], [1846], [1847], [1848], [1849], [1850], [1851], [1852], [1853], [1854], [1855], [1856], [1857, 1], [1857, 2], [1857, 3], [1857, 4], [1857, 5], [1857, 6], [1857, 7], [1857, 8], [1857, 9], [1857, 10], [1857, 11], [1857, 12], [1857, 13], [1857, 14], [1857, 15], [1857, 16], [1857, 17], [1857, 18], [1857, 19], [1857, 20], [1857, 21], [1857, 22], [1857, 23], [1857, 24], [1857, 25], [1857, 26], [1857, 27], [1857, 29], [1857, 30], [1857, 31], [1857, 32], [1857, 33], [1857, 34], [1857, 35], [1857, 36], [1857, 37], [1857, 38], [1857, 39], [1857, 40], [1857, 41], [1857, 42], [1857, 43], [1857, 44], [1857, 45], [1857, 46], [1857, 47], [1857, 48], [1857, 49], [1857, 50], [1857, 51], [1857, 52], [1857, 53], [1857, 54], [1857, 55], [1857, 56], [1857, 57], [1857, 58], [1857, 59], [1857, 60], [1857, 61], [1857, 62], [1857, 63], [1857, 64], [1857, 65], [1857, 66], [1857, 67], [1857, 68], [1857, 69], [1857, 70], [1857, 71], [1857, 72], [1857, 73], [1857, 74], [1857, 75], [1857, 76], [1857, 77], [1857, 78], [1857, 79], [1857, 80], [1857, 81], [1857, 82], [1857, 84], [1857, 85], [1857, 86], [1857, 87], [1857, 88], [1857, 89], [1857, 90], [1857, 91], [1857, 92], [1857, 93], [1857, 94], [1857, 95], [1857, 96], [1857, 97], [1857, 98], [1857, 99], [1857, 100], [1857, 101], [1857, 102], [1857, 103], [1857, 104], [1857, 105], [1857, 106], [1857, 107], [1857, 108], [1857, 109], [1857, 110], [1857, 112], [1857, 113], [1857, 114], [1857, 115], [1857, 116], [1857, 117], [1857, 118], [1857, 119], [1857, 120], [1857, 121], [1857, 122], [1857, 123], [1857, 124], [1857, 125], [1857, 126], [1857, 127], [1857, 128], [1857, 129], [1857, 130], [1857, 131], [1857, 132], [1857, 133], [1857, 134], [1857, 135], [1857, 136], [1857, 137], [1857, 138], [1857, 139], [1857, 140], [1857, 141], [1857, 142], [1857, 143], [1857, 144], [1857, 145], [1857, 146], [1857, 147], [1857, 148], [1857, 149], [1857, 150], [1857, 151], [1857, 152], [1857, 153], [1857, 154], [1857, 155], [1857, 156], [1857, 157], [1857, 158], [1857, 159], [1857, 160], [1857, 161], [1857, 162], [1857, 163], [1857, 164], [1857, 165], [1857, 167], [1857, 168], [1857, 169], [1857, 170], [1857, 171], [1857, 172], [1857, 173], [1857, 174], [1857, 175], [1857, 176], [1857, 177], [1857, 178], [1857, 179], [1857, 180], [1857, 181], [1857, 182], [1857, 183], [1857, 184], [1857, 185], [1857, 186], [1857, 187], [1857, 188], [1857, 189], [1857, 190], [1857, 191], [1857, 192], [1857, 193], [1857, 194], [1857, 195], [1857, 196], [1857, 197], [1857, 198], [1857, 199], [1857, 200], [1857, 201], [1857, 202], [1857, 203], [1857, 204], [1857, 205], [1857, 206], [1857, 207], [1857, 208], [1857, 209], [1857, 210], [1857, 211], [1857, 212], [1857, 213], [1857, 215], [1857, 216], [1857, 217], [1857, 218], [1857, 219], [1857, 220], [1857, 221], [1857, 222], [1857, 223], [1857, 224], [1857, 225], [1857, 226], [1857, 227], [1857, 228], [1857, 229], [1857, 230], [1857, 231], [1857, 232], [1857, 233], [1857, 234], [1857, 235], [1857, 236], [1857, 237], [1857, 238], [1857, 239], [1857, 240], [1857, 241], [1857, 242], [1857, 243], [1857, 244], [1857, 245], [1857, 246], [1857, 247], [1857, 248], [1857, 249], [1857, 250], [1857, 251], [1857, 252], [1857, 253], [1857, 254], [1857, 255], [1857, 256], [1857, 257], [1857, 258], [1857, 259], [1857, 260], [1857, 261], [1857, 262], [1857, 263], [1857, 264], [1857, 265], [1857, 266], [1857, 267], [1857, 268], [1857, 270], [1857, 271], [1857, 272], [1857, 273], [1857, 274], [1857, 275], [1857, 276], [1857, 277], [1857, 278], [1857, 279], [1857, 280], [1857, 281], [1857, 282], [1857, 283], [1857, 284], [1857, 285], [1857, 286], [1857, 287], [1857, 288], [1857, 289], [1857, 290], [1857, 291], [1857, 292], [1857, 293], [1857, 294], [1857, 295], [1857, 296], [1857, 297], [1857, 298], [1857, 299], [1857, 300], [1857, 301], [1857, 302], [1857, 303], [1857, 304], [1857, 305], [1857, 306], [1857, 307], [1857, 308], [1857, 309], [1857, 310], [1857, 311], [1857, 312], [1857, 313], [1857, 314], [1857, 315], [1857, 316], [1857, 318], [1857, 319], [1857, 320], [1857, 321], [1857, 322], [1857, 323], [1857, 324], [1857, 325], [1857, 326], [1857, 327], [1857, 328], [1857, 329], [1857, 330], [1857, 331], [1857, 332], [1857, 333], [1857, 334], [1857, 335], [1857, 336], [1857, 337], [1857, 338], [1857, 339], [1857, 340], [1857, 341], [1857, 342], [1857, 343], [1857, 344], [1857, 345], [1857, 346], [1857, 347], [1857, 348], [1857, 349], [1857, 350], [1857, 351], [1857, 352], [1857, 353], [1857, 354], [1857, 355], [1857, 356], [1857, 357], [1857, 358], [1857, 359], [1857, 360], [1857, 361], [1857, 362], [1857, 363], [1857, 364], [1857, 365], [1857, 366], [1857, 367], [1857, 368], [1857, 369], [1857, 370], [1857, 371], [1857, 373], [1857, 374], [1857, 375], [1857, 376], [1857, 377], [1857, 378], [1857, 379], [1857, 380], [1857, 381], [1857, 382], [1857, 383], [1857, 384], [1857, 385], [1857, 386], [1857, 387], [1857, 388], [1857, 389], [1857, 390], [1857, 391], [1857, 392], [1857, 393], [1857, 394], [1857, 395], [1857, 396], [1857, 397], [1857, 398], [1857, 399], [1857, 400], [1857, 401], [1857, 402], [1857, 403], [1857, 404], [1857, 405], [1857, 406], [1857, 407], [1857, 408], [1857, 409], [1857, 410], [1857, 411], [1857, 412], [1857, 413], [1857, 414], [1857, 415], [1857, 416], [1857, 417], [1857, 418], [1857, 419], [1857, 421], [1857, 422], [1857, 423], [1857, 424], [1857, 425], [1857, 426], [1857, 427], [1857, 428], [1857, 429], [1857, 430], [1857, 431], [1857, 432], [1857, 433], [1857, 434], [1857, 435], [1857, 436], [1857, 437], [1857, 438], [1857, 439], [1857, 440], [1857, 441], [1857, 442], [1857, 443], [1857, 444], [1857, 445], [1857, 446], [1857, 447], [1857, 448], [1857, 449], [1857, 450], [1857, 451], [1857, 452], [1857, 453], [1857, 454], [1857, 455], [1857, 456], [1857, 457], [1857, 458], [1857, 459], [1857, 460], [1857, 461], [1857, 462], [1857, 463], [1857, 464], [1857, 465], [1857, 466], [1857, 467], [1857, 468], [1857, 469], [1857, 470], [1857, 471], [1857, 472], [1857, 473], [1857, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[1861], [1862], [1863], [1864], [1865], [1866], [1867], [1868], [1869], [1870], [1871], [1872], [1873], [1874], [1875], [1876], [1877], [1878], [1879], [1880], [1881], [1882], [1883], [1884], [1885], [1886], [1887], [1888], [1889], [1890], [1891], [1892], [1893], [1894], [1895], [1896], [1897], [1898], [1899], [1900], [1901], [1902], [1903], [1904], [1905], [1906], [1907], [1908], [1909], [1910], [1911], [1912], [1913], [1914], [1915, 1], [1915, 2], [1915, 3], [1915, 4], [1915, 5], [1915, 6], [1915, 7], [1915, 8], [1915, 9], [1915, 10], [1915, 11], [1915, 12], [1915, 13], [1915, 14], [1915, 15], [1915, 16], [1915, 17], [1915, 18], [1915, 19], [1915, 20], [1915, 21], [1915, 22], [1915, 23], [1915, 24], [1915, 25], [1915, 26], [1915, 27], [1915, 29], [1915, 30], [1915, 31], [1915, 32], [1915, 33], [1915, 34], [1915, 35], [1915, 36], [1915, 37], [1915, 38], [1915, 39], [1915, 40], [1915, 41], [1915, 42], [1915, 43], [1915, 44], [1915, 45], [1915, 46], [1915, 47], [1915, 48], [1915, 49], [1915, 50], [1915, 51], [1915, 52], [1915, 53], [1915, 54], [1915, 55], [1915, 56], [1915, 57], [1915, 58], [1915, 59], [1915, 60], [1915, 61], [1915, 62], [1915, 63], [1915, 64], [1915, 65], [1915, 66], [1915, 67], [1915, 68], [1915, 69], [1915, 70], [1915, 71], [1915, 72], [1915, 73], [1915, 74], [1915, 75], [1915, 76], [1915, 77], [1915, 78], [1915, 79], [1915, 80], [1915, 81], [1915, 82], [1915, 84], [1915, 85], [1915, 86], [1915, 87], [1915, 88], [1915, 89], [1915, 90], [1915, 91], [1915, 92], [1915, 93], [1915, 94], [1915, 95], [1915, 96], [1915, 97], [1915, 98], [1915, 99], [1915, 100], [1915, 101], [1915, 102], [1915, 103], [1915, 104], [1915, 105], [1915, 106], [1915, 107], [1915, 108], [1915, 109], [1915, 110], [1915, 112], [1915, 113], [1915, 114], [1915, 115], [1915, 116], [1915, 117], [1915, 118], [1915, 119], [1915, 120], [1915, 121], [1915, 122], [1915, 123], [1915, 124], [1915, 125], [1915, 126], [1915, 127], [1915, 128], [1915, 129], [1915, 130], [1915, 131], [1915, 132], [1915, 133], [1915, 134], [1915, 135], [1915, 136], [1915, 137], [1915, 138], [1915, 139], [1915, 140], [1915, 141], [1915, 142], [1915, 143], [1915, 144], [1915, 145], [1915, 146], [1915, 147], [1915, 148], [1915, 149], [1915, 150], [1915, 151], [1915, 152], [1915, 153], [1915, 154], [1915, 155], [1915, 156], [1915, 157], [1915, 158], [1915, 159], [1915, 160], [1915, 161], [1915, 162], [1915, 163], [1915, 164], [1915, 165], [1915, 167], [1915, 168], [1915, 169], [1915, 170], [1915, 171], [1915, 172], [1915, 173], [1915, 174], [1915, 175], [1915, 176], [1915, 177], [1915, 178], [1915, 179], [1915, 180], [1915, 181], [1915, 182], [1915, 183], [1915, 184], [1915, 185], [1915, 186], [1915, 187], [1915, 188], [1915, 189], [1915, 190], [1915, 191], [1915, 192], [1915, 193], [1915, 194], [1915, 195], [1915, 196], [1915, 197], [1915, 198], [1915, 199], [1915, 200], [1915, 201], [1915, 202], [1915, 203], [1915, 204], [1915, 205], [1915, 206], [1915, 207], [1915, 208], [1915, 209], [1915, 210], [1915, 211], [1915, 212], [1915, 213], [1915, 215], [1915, 216], [1915, 217], [1915, 218], [1915, 219], [1915, 220], [1915, 221], [1915, 222], [1915, 223], [1915, 224], [1915, 225], [1915, 226], [1915, 227], [1915, 228], [1915, 229], [1915, 230], [1915, 231], [1915, 232], [1915, 233], [1915, 234], [1915, 235], [1915, 236], [1915, 237], [1915, 238], [1915, 239], [1915, 240], [1915, 241], [1915, 242], [1915, 243], [1915, 244], [1915, 245], [1915, 246], [1915, 247], [1915, 248], [1915, 249], [1915, 250], [1915, 251], [1915, 252], [1915, 253], [1915, 254], [1915, 255], [1915, 256], [1915, 257], [1915, 258], [1915, 259], [1915, 260], [1915, 261], [1915, 262], [1915, 263], [1915, 264], [1915, 265], [1915, 266], [1915, 267], [1915, 268], [1915, 270], [1915, 271], [1915, 272], [1915, 273], [1915, 274], [1915, 275], [1915, 276], [1915, 277], [1915, 278], [1915, 279], [1915, 280], [1915, 281], [1915, 282], [1915, 283], [1915, 284], [1915, 285], [1915, 286], [1915, 287], [1915, 288], [1915, 289], [1915, 290], [1915, 291], [1915, 292], [1915, 293], [1915, 294], [1915, 295], [1915, 296], [1915, 297], [1915, 298], [1915, 299], [1915, 300], [1915, 301], [1915, 302], [1915, 303], [1915, 304], [1915, 305], [1915, 306], [1915, 307], [1915, 308], [1915, 309], [1915, 310], [1915, 311], [1915, 312], [1915, 313], [1915, 314], [1915, 315], [1915, 316], [1915, 318], [1915, 319], [1915, 320], [1915, 321], [1915, 322], [1915, 323], [1915, 324], [1915, 325], [1915, 326], [1915, 327], [1915, 328], [1915, 329], [1915, 330], [1915, 331], [1915, 332], [1915, 333], [1915, 334], [1915, 335], [1915, 336], [1915, 337], [1915, 338], [1915, 339], [1915, 340], [1915, 341], [1915, 342], [1915, 343], [1915, 344], [1915, 345], [1915, 346], [1915, 347], [1915, 348], [1915, 349], [1915, 350], [1915, 351], [1915, 352], [1915, 353], [1915, 354], [1915, 355], [1915, 356], [1915, 357], [1915, 358], [1915, 359], [1915, 360], [1915, 361], [1915, 362], [1915, 363], [1915, 364], [1915, 365], [1915, 366], [1915, 367], [1915, 368], [1915, 369], [1915, 370], [1915, 371], [1915, 373], [1915, 374], [1915, 375], [1915, 376], [1915, 377], [1915, 378], [1915, 379], [1915, 380], [1915, 381], [1915, 382], [1915, 383], [1915, 384], [1915, 385], [1915, 386], [1915, 387], [1915, 388], [1915, 389], [1915, 390], [1915, 391], [1915, 392], [1915, 393], [1915, 394], [1915, 395], [1915, 396], [1915, 397], [1915, 398], [1915, 399], [1915, 400], [1915, 401], [1915, 402], [1915, 403], [1915, 404], [1915, 405], [1915, 406], [1915, 407], [1915, 408], [1915, 409], [1915, 410], [1915, 411], [1915, 412], [1915, 413], [1915, 414], [1915, 415], [1915, 416], [1915, 417], [1915, 418], [1915, 419], [1915, 421], [1915, 422], [1915, 423], [1915, 424], [1915, 425], [1915, 426], [1915, 427], [1915, 428], [1915, 429], [1915, 430], [1915, 431], [1915, 432], [1915, 433], [1915, 434], [1915, 435], [1915, 436], [1915, 437], [1915, 438], [1915, 439], [1915, 440], [1915, 441], [1915, 442], [1915, 443], [1915, 444], [1915, 445], [1915, 446], [1915, 447], [1915, 448], [1915, 449], [1915, 450], [1915, 451], [1915, 452], [1915, 453], [1915, 454], [1915, 455], [1915, 456], [1915, 457], [1915, 458], [1915, 459], [1915, 460], [1915, 461], [1915, 462], [1915, 463], [1915, 464], [1915, 465], [1915, 466], [1915, 467], [1915, 468], [1915, 469], [1915, 470], [1915, 471], [1915, 472], [1915, 473], [1915, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[1919], [1920], [1921], [1922], [1923], [1924], [1925], [1926], [1927], [1928], [1929], [1930], [1931], [1932], [1933], [1934], [1935], [1936], [1937], [1938], [1939], [1940], [1941], [1942], [1943], [1944], [1945], [1946], [1947], [1948], [1949], [1950], [1951], [1952], [1953], [1954], [1955], [1956], [1957], [1958], [1959], [1960], [1961], [1962], [1963], [1964], [1965], [1966], [1967], [1968], [1969], [1970], [1971], [1972], [1973, 1], [1973, 2], [1973, 3], [1973, 4], [1973, 5], [1973, 6], [1973, 7], [1973, 8], [1973, 9], [1973, 10], [1973, 11], [1973, 12], [1973, 13], [1973, 14], [1973, 15], [1973, 16], [1973, 17], [1973, 18], [1973, 19], [1973, 20], [1973, 21], [1973, 22], [1973, 23], [1973, 24], [1973, 25], [1973, 26], [1973, 27], [1973, 29], [1973, 30], [1973, 31], [1973, 32], [1973, 33], [1973, 34], [1973, 35], [1973, 36], [1973, 37], [1973, 38], [1973, 39], [1973, 40], [1973, 41], [1973, 42], [1973, 43], [1973, 44], [1973, 45], [1973, 46], [1973, 47], [1973, 48], [1973, 49], [1973, 50], [1973, 51], [1973, 52], [1973, 53], [1973, 54], [1973, 55], [1973, 56], [1973, 57], [1973, 58], [1973, 59], [1973, 60], [1973, 61], [1973, 62], [1973, 63], [1973, 64], [1973, 65], [1973, 66], [1973, 67], [1973, 68], [1973, 69], [1973, 70], [1973, 71], [1973, 72], [1973, 73], [1973, 74], [1973, 75], [1973, 76], [1973, 77], [1973, 78], [1973, 79], [1973, 80], [1973, 81], [1973, 82], [1973, 84], [1973, 85], [1973, 86], [1973, 87], [1973, 88], [1973, 89], [1973, 90], [1973, 91], [1973, 92], [1973, 93], [1973, 94], [1973, 95], [1973, 96], [1973, 97], [1973, 98], [1973, 99], [1973, 100], [1973, 101], [1973, 102], [1973, 103], [1973, 104], [1973, 105], [1973, 106], [1973, 107], [1973, 108], [1973, 109], [1973, 110], [1973, 112], [1973, 113], [1973, 114], [1973, 115], [1973, 116], [1973, 117], [1973, 118], [1973, 119], [1973, 120], [1973, 121], [1973, 122], [1973, 123], [1973, 124], [1973, 125], [1973, 126], [1973, 127], [1973, 128], [1973, 129], [1973, 130], [1973, 131], [1973, 132], [1973, 133], [1973, 134], [1973, 135], [1973, 136], [1973, 137], [1973, 138], [1973, 139], [1973, 140], [1973, 141], [1973, 142], [1973, 143], [1973, 144], [1973, 145], [1973, 146], [1973, 147], [1973, 148], [1973, 149], [1973, 150], [1973, 151], [1973, 152], [1973, 153], [1973, 154], [1973, 155], [1973, 156], [1973, 157], [1973, 158], [1973, 159], [1973, 160], [1973, 161], [1973, 162], [1973, 163], [1973, 164], [1973, 165], [1973, 167], [1973, 168], [1973, 169], [1973, 170], [1973, 171], [1973, 172], [1973, 173], [1973, 174], [1973, 175], [1973, 176], [1973, 177], [1973, 178], [1973, 179], [1973, 180], [1973, 181], [1973, 182], [1973, 183], [1973, 184], [1973, 185], [1973, 186], [1973, 187], [1973, 188], [1973, 189], [1973, 190], [1973, 191], [1973, 192], [1973, 193], [1973, 194], [1973, 195], [1973, 196], [1973, 197], [1973, 198], [1973, 199], [1973, 200], [1973, 201], [1973, 202], [1973, 203], [1973, 204], [1973, 205], [1973, 206], [1973, 207], [1973, 208], [1973, 209], [1973, 210], [1973, 211], [1973, 212], [1973, 213], [1973, 215], [1973, 216], [1973, 217], [1973, 218], [1973, 219], [1973, 220], [1973, 221], [1973, 222], [1973, 223], [1973, 224], [1973, 225], [1973, 226], [1973, 227], [1973, 228], [1973, 229], [1973, 230], [1973, 231], [1973, 232], [1973, 233], [1973, 234], [1973, 235], [1973, 236], [1973, 237], [1973, 238], [1973, 239], [1973, 240], [1973, 241], [1973, 242], [1973, 243], [1973, 244], [1973, 245], [1973, 246], [1973, 247], [1973, 248], [1973, 249], [1973, 250], [1973, 251], [1973, 252], [1973, 253], [1973, 254], [1973, 255], [1973, 256], [1973, 257], [1973, 258], [1973, 259], [1973, 260], [1973, 261], [1973, 262], [1973, 263], [1973, 264], [1973, 265], [1973, 266], [1973, 267], [1973, 268], [1973, 270], [1973, 271], [1973, 272], [1973, 273], [1973, 274], [1973, 275], [1973, 276], [1973, 277], [1973, 278], [1973, 279], [1973, 280], [1973, 281], [1973, 282], [1973, 283], [1973, 284], [1973, 285], [1973, 286], [1973, 287], [1973, 288], [1973, 289], [1973, 290], [1973, 291], [1973, 292], [1973, 293], [1973, 294], [1973, 295], [1973, 296], [1973, 297], [1973, 298], [1973, 299], [1973, 300], [1973, 301], [1973, 302], [1973, 303], [1973, 304], [1973, 305], [1973, 306], [1973, 307], [1973, 308], [1973, 309], [1973, 310], [1973, 311], [1973, 312], [1973, 313], [1973, 314], [1973, 315], [1973, 316], [1973, 318], [1973, 319], [1973, 320], [1973, 321], [1973, 322], [1973, 323], [1973, 324], [1973, 325], [1973, 326], [1973, 327], [1973, 328], [1973, 329], [1973, 330], [1973, 331], [1973, 332], [1973, 333], [1973, 334], [1973, 335], [1973, 336], [1973, 337], [1973, 338], [1973, 339], [1973, 340], [1973, 341], [1973, 342], [1973, 343], [1973, 344], [1973, 345], [1973, 346], [1973, 347], [1973, 348], [1973, 349], [1973, 350], [1973, 351], [1973, 352], [1973, 353], [1973, 354], [1973, 355], [1973, 356], [1973, 357], [1973, 358], [1973, 359], [1973, 360], [1973, 361], [1973, 362], [1973, 363], [1973, 364], [1973, 365], [1973, 366], [1973, 367], [1973, 368], [1973, 369], [1973, 370], [1973, 371], [1973, 373], [1973, 374], [1973, 375], [1973, 376], [1973, 377], [1973, 378], [1973, 379], [1973, 380], [1973, 381], [1973, 382], [1973, 383], [1973, 384], [1973, 385], [1973, 386], [1973, 387], [1973, 388], [1973, 389], [1973, 390], [1973, 391], [1973, 392], [1973, 393], [1973, 394], [1973, 395], [1973, 396], [1973, 397], [1973, 398], [1973, 399], [1973, 400], [1973, 401], [1973, 402], [1973, 403], [1973, 404], [1973, 405], [1973, 406], [1973, 407], [1973, 408], [1973, 409], [1973, 410], [1973, 411], [1973, 412], [1973, 413], [1973, 414], [1973, 415], [1973, 416], [1973, 417], [1973, 418], [1973, 419], [1973, 421], [1973, 422], [1973, 423], [1973, 424], [1973, 425], [1973, 426], [1973, 427], [1973, 428], [1973, 429], [1973, 430], [1973, 431], [1973, 432], [1973, 433], [1973, 434], [1973, 435], [1973, 436], [1973, 437], [1973, 438], [1973, 439], [1973, 440], [1973, 441], [1973, 442], [1973, 443], [1973, 444], [1973, 445], [1973, 446], [1973, 447], [1973, 448], [1973, 449], [1973, 450], [1973, 451], [1973, 452], [1973, 453], [1973, 454], [1973, 455], [1973, 456], [1973, 457], [1973, 458], [1973, 459], [1973, 460], [1973, 461], [1973, 462], [1973, 463], [1973, 464], [1973, 465], [1973, 466], [1973, 467], [1973, 468], [1973, 469], [1973, 470], [1973, 471], [1973, 472], [1973, 473], [1973, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[1977], [1978], [1979], [1980], [1981], [1982], [1983], [1984], [1985], [1986], [1987], [1988], [1989], [1990], [1991], [1992], [1993], [1994], [1995], [1996], [1997], [1998], [1999], [2000], [2001], [2002], [2003], [2004], [2005], [2006], [2007], [2008], [2009], [2010], [2011], [2012], [2013], [2014], [2015], [2016], [2017], [2018], [2019], [2020], [2021], [2022], [2023], [2024], [2025], [2026], [2027], [2028], [2029], [2030], [2031, 1], [2031, 2], [2031, 3], [2031, 4], [2031, 5], [2031, 6], [2031, 7], [2031, 8], [2031, 9], [2031, 10], [2031, 11], [2031, 12], [2031, 13], [2031, 14], [2031, 15], [2031, 16], [2031, 17], [2031, 18], [2031, 19], [2031, 20], [2031, 21], [2031, 22], [2031, 23], [2031, 24], [2031, 25], [2031, 26], [2031, 27], [2031, 29], [2031, 30], [2031, 31], [2031, 32], [2031, 33], [2031, 34], [2031, 35], [2031, 36], [2031, 37], [2031, 38], [2031, 39], [2031, 40], [2031, 41], [2031, 42], [2031, 43], [2031, 44], [2031, 45], [2031, 46], [2031, 47], [2031, 48], [2031, 49], [2031, 50], [2031, 51], [2031, 52], [2031, 53], [2031, 54], [2031, 55], [2031, 56], [2031, 57], [2031, 58], [2031, 59], [2031, 60], [2031, 61], [2031, 62], [2031, 63], [2031, 64], [2031, 65], [2031, 66], [2031, 67], [2031, 68], [2031, 69], [2031, 70], [2031, 71], [2031, 72], [2031, 73], [2031, 74], [2031, 75], [2031, 76], [2031, 77], [2031, 78], [2031, 79], [2031, 80], [2031, 81], [2031, 82], [2031, 84], [2031, 85], [2031, 86], [2031, 87], [2031, 88], [2031, 89], [2031, 90], [2031, 91], [2031, 92], [2031, 93], [2031, 94], [2031, 95], [2031, 96], [2031, 97], [2031, 98], [2031, 99], [2031, 100], [2031, 101], [2031, 102], [2031, 103], [2031, 104], [2031, 105], [2031, 106], [2031, 107], [2031, 108], [2031, 109], [2031, 110], [2031, 112], [2031, 113], [2031, 114], [2031, 115], [2031, 116], [2031, 117], [2031, 118], [2031, 119], [2031, 120], [2031, 121], [2031, 122], [2031, 123], [2031, 124], [2031, 125], [2031, 126], [2031, 127], [2031, 128], [2031, 129], [2031, 130], [2031, 131], [2031, 132], [2031, 133], [2031, 134], [2031, 135], [2031, 136], [2031, 137], [2031, 138], [2031, 139], [2031, 140], [2031, 141], [2031, 142], [2031, 143], [2031, 144], [2031, 145], [2031, 146], [2031, 147], [2031, 148], [2031, 149], [2031, 150], [2031, 151], [2031, 152], [2031, 153], [2031, 154], [2031, 155], [2031, 156], [2031, 157], [2031, 158], [2031, 159], [2031, 160], [2031, 161], [2031, 162], [2031, 163], [2031, 164], [2031, 165], [2031, 167], [2031, 168], [2031, 169], [2031, 170], [2031, 171], [2031, 172], [2031, 173], [2031, 174], [2031, 175], [2031, 176], [2031, 177], [2031, 178], [2031, 179], [2031, 180], [2031, 181], [2031, 182], [2031, 183], [2031, 184], [2031, 185], [2031, 186], [2031, 187], [2031, 188], [2031, 189], [2031, 190], [2031, 191], [2031, 192], [2031, 193], [2031, 194], [2031, 195], [2031, 196], [2031, 197], [2031, 198], [2031, 199], [2031, 200], [2031, 201], [2031, 202], [2031, 203], [2031, 204], [2031, 205], [2031, 206], [2031, 207], [2031, 208], [2031, 209], [2031, 210], [2031, 211], [2031, 212], [2031, 213], [2031, 215], [2031, 216], [2031, 217], [2031, 218], [2031, 219], [2031, 220], [2031, 221], [2031, 222], [2031, 223], [2031, 224], [2031, 225], [2031, 226], [2031, 227], [2031, 228], [2031, 229], [2031, 230], [2031, 231], [2031, 232], [2031, 233], [2031, 234], [2031, 235], [2031, 236], [2031, 237], [2031, 238], [2031, 239], [2031, 240], [2031, 241], [2031, 242], [2031, 243], [2031, 244], [2031, 245], [2031, 246], [2031, 247], [2031, 248], [2031, 249], [2031, 250], [2031, 251], [2031, 252], [2031, 253], [2031, 254], [2031, 255], [2031, 256], [2031, 257], [2031, 258], [2031, 259], [2031, 260], [2031, 261], [2031, 262], [2031, 263], [2031, 264], [2031, 265], [2031, 266], [2031, 267], [2031, 268], [2031, 270], [2031, 271], [2031, 272], [2031, 273], [2031, 274], [2031, 275], [2031, 276], [2031, 277], [2031, 278], [2031, 279], [2031, 280], [2031, 281], [2031, 282], [2031, 283], [2031, 284], [2031, 285], [2031, 286], [2031, 287], [2031, 288], [2031, 289], [2031, 290], [2031, 291], [2031, 292], [2031, 293], [2031, 294], [2031, 295], [2031, 296], [2031, 297], [2031, 298], [2031, 299], [2031, 300], [2031, 301], [2031, 302], [2031, 303], [2031, 304], [2031, 305], [2031, 306], [2031, 307], [2031, 308], [2031, 309], [2031, 310], [2031, 311], [2031, 312], [2031, 313], [2031, 314], [2031, 315], [2031, 316], [2031, 318], [2031, 319], [2031, 320], [2031, 321], [2031, 322], [2031, 323], [2031, 324], [2031, 325], [2031, 326], [2031, 327], [2031, 328], [2031, 329], [2031, 330], [2031, 331], [2031, 332], [2031, 333], [2031, 334], [2031, 335], [2031, 336], [2031, 337], [2031, 338], [2031, 339], [2031, 340], [2031, 341], [2031, 342], [2031, 343], [2031, 344], [2031, 345], [2031, 346], [2031, 347], [2031, 348], [2031, 349], [2031, 350], [2031, 351], [2031, 352], [2031, 353], [2031, 354], [2031, 355], [2031, 356], [2031, 357], [2031, 358], [2031, 359], [2031, 360], [2031, 361], [2031, 362], [2031, 363], [2031, 364], [2031, 365], [2031, 366], [2031, 367], [2031, 368], [2031, 369], [2031, 370], [2031, 371], [2031, 373], [2031, 374], [2031, 375], [2031, 376], [2031, 377], [2031, 378], [2031, 379], [2031, 380], [2031, 381], [2031, 382], [2031, 383], [2031, 384], [2031, 385], [2031, 386], [2031, 387], [2031, 388], [2031, 389], [2031, 390], [2031, 391], [2031, 392], [2031, 393], [2031, 394], [2031, 395], [2031, 396], [2031, 397], [2031, 398], [2031, 399], [2031, 400], [2031, 401], [2031, 402], [2031, 403], [2031, 404], [2031, 405], [2031, 406], [2031, 407], [2031, 408], [2031, 409], [2031, 410], [2031, 411], [2031, 412], [2031, 413], [2031, 414], [2031, 415], [2031, 416], [2031, 417], [2031, 418], [2031, 419], [2031, 421], [2031, 422], [2031, 423], [2031, 424], [2031, 425], [2031, 426], [2031, 427], [2031, 428], [2031, 429], [2031, 430], [2031, 431], [2031, 432], [2031, 433], [2031, 434], [2031, 435], [2031, 436], [2031, 437], [2031, 438], [2031, 439], [2031, 440], [2031, 441], [2031, 442], [2031, 443], [2031, 444], [2031, 445], [2031, 446], [2031, 447], [2031, 448], [2031, 449], [2031, 450], [2031, 451], [2031, 452], [2031, 453], [2031, 454], [2031, 455], [2031, 456], [2031, 457], [2031, 458], [2031, 459], [2031, 460], [2031, 461], [2031, 462], [2031, 463], [2031, 464], [2031, 465], [2031, 466], [2031, 467], [2031, 468], [2031, 469], [2031, 470], [2031, 471], [2031, 472], [2031, 473], [2031, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[2035], [2036], [2037], [2038], [2039], [2040], [2041], [2042], [2043], [2044], [2045], [2046], [2047], [2048], [2049], [2050], [2051], [2052], [2053], [2054], [2055], [2056], [2057], [2058], [2059], [2060], [2061], [2062], [2063], [2064], [2065], [2066], [2067], [2068], [2069], [2070], [2071], [2072], [2073], [2074], [2075], [2076], [2077], [2078], [2079], [2080], [2081], [2082], [2083], [2084], [2085], [2086], [2087], [2088], [2089, 1], [2089, 2], [2089, 3], [2089, 4], [2089, 5], [2089, 6], [2089, 7], [2089, 8], [2089, 9], [2089, 10], [2089, 11], [2089, 12], [2089, 13], [2089, 14], [2089, 15], [2089, 16], [2089, 17], [2089, 18], [2089, 19], [2089, 20], [2089, 21], [2089, 22], [2089, 23], [2089, 24], [2089, 25], [2089, 26], [2089, 27], [2089, 29], [2089, 30], [2089, 31], [2089, 32], [2089, 33], [2089, 34], [2089, 35], [2089, 36], [2089, 37], [2089, 38], [2089, 39], [2089, 40], [2089, 41], [2089, 42], [2089, 43], [2089, 44], [2089, 45], [2089, 46], [2089, 47], [2089, 48], [2089, 49], [2089, 50], [2089, 51], [2089, 52], [2089, 53], [2089, 54], [2089, 55], [2089, 56], [2089, 57], [2089, 58], [2089, 59], [2089, 60], [2089, 61], [2089, 62], [2089, 63], [2089, 64], [2089, 65], [2089, 66], [2089, 67], [2089, 68], [2089, 69], [2089, 70], [2089, 71], [2089, 72], [2089, 73], [2089, 74], [2089, 75], [2089, 76], [2089, 77], [2089, 78], [2089, 79], [2089, 80], [2089, 81], [2089, 82], [2089, 84], [2089, 85], [2089, 86], [2089, 87], [2089, 88], [2089, 89], [2089, 90], [2089, 91], [2089, 92], [2089, 93], [2089, 94], [2089, 95], [2089, 96], [2089, 97], [2089, 98], [2089, 99], [2089, 100], [2089, 101], [2089, 102], [2089, 103], [2089, 104], [2089, 105], [2089, 106], [2089, 107], [2089, 108], [2089, 109], [2089, 110], [2089, 112], [2089, 113], [2089, 114], [2089, 115], [2089, 116], [2089, 117], [2089, 118], [2089, 119], [2089, 120], [2089, 121], [2089, 122], [2089, 123], [2089, 124], [2089, 125], [2089, 126], [2089, 127], [2089, 128], [2089, 129], [2089, 130], [2089, 131], [2089, 132], [2089, 133], [2089, 134], [2089, 135], [2089, 136], [2089, 137], [2089, 138], [2089, 139], [2089, 140], [2089, 141], [2089, 142], [2089, 143], [2089, 144], [2089, 145], [2089, 146], [2089, 147], [2089, 148], [2089, 149], [2089, 150], [2089, 151], [2089, 152], [2089, 153], [2089, 154], [2089, 155], [2089, 156], [2089, 157], [2089, 158], [2089, 159], [2089, 160], [2089, 161], [2089, 162], [2089, 163], [2089, 164], [2089, 165], [2089, 167], [2089, 168], [2089, 169], [2089, 170], [2089, 171], [2089, 172], [2089, 173], [2089, 174], [2089, 175], [2089, 176], [2089, 177], [2089, 178], [2089, 179], [2089, 180], [2089, 181], [2089, 182], [2089, 183], [2089, 184], [2089, 185], [2089, 186], [2089, 187], [2089, 188], [2089, 189], [2089, 190], [2089, 191], [2089, 192], [2089, 193], [2089, 194], [2089, 195], [2089, 196], [2089, 197], [2089, 198], [2089, 199], [2089, 200], [2089, 201], [2089, 202], [2089, 203], [2089, 204], [2089, 205], [2089, 206], [2089, 207], [2089, 208], [2089, 209], [2089, 210], [2089, 211], [2089, 212], [2089, 213], [2089, 215], [2089, 216], [2089, 217], [2089, 218], [2089, 219], [2089, 220], [2089, 221], [2089, 222], [2089, 223], [2089, 224], [2089, 225], [2089, 226], [2089, 227], [2089, 228], [2089, 229], [2089, 230], [2089, 231], [2089, 232], [2089, 233], [2089, 234], [2089, 235], [2089, 236], [2089, 237], [2089, 238], [2089, 239], [2089, 240], [2089, 241], [2089, 242], [2089, 243], [2089, 244], [2089, 245], [2089, 246], [2089, 247], [2089, 248], [2089, 249], [2089, 250], [2089, 251], [2089, 252], [2089, 253], [2089, 254], [2089, 255], [2089, 256], [2089, 257], [2089, 258], [2089, 259], [2089, 260], [2089, 261], [2089, 262], [2089, 263], [2089, 264], [2089, 265], [2089, 266], [2089, 267], [2089, 268], [2089, 270], [2089, 271], [2089, 272], [2089, 273], [2089, 274], [2089, 275], [2089, 276], [2089, 277], [2089, 278], [2089, 279], [2089, 280], [2089, 281], [2089, 282], [2089, 283], [2089, 284], [2089, 285], [2089, 286], [2089, 287], [2089, 288], [2089, 289], [2089, 290], [2089, 291], [2089, 292], [2089, 293], [2089, 294], [2089, 295], [2089, 296], [2089, 297], [2089, 298], [2089, 299], [2089, 300], [2089, 301], [2089, 302], [2089, 303], [2089, 304], [2089, 305], [2089, 306], [2089, 307], [2089, 308], [2089, 309], [2089, 310], [2089, 311], [2089, 312], [2089, 313], [2089, 314], [2089, 315], [2089, 316], [2089, 318], [2089, 319], [2089, 320], [2089, 321], [2089, 322], [2089, 323], [2089, 324], [2089, 325], [2089, 326], [2089, 327], [2089, 328], [2089, 329], [2089, 330], [2089, 331], [2089, 332], [2089, 333], [2089, 334], [2089, 335], [2089, 336], [2089, 337], [2089, 338], [2089, 339], [2089, 340], [2089, 341], [2089, 342], [2089, 343], [2089, 344], [2089, 345], [2089, 346], [2089, 347], [2089, 348], [2089, 349], [2089, 350], [2089, 351], [2089, 352], [2089, 353], [2089, 354], [2089, 355], [2089, 356], [2089, 357], [2089, 358], [2089, 359], [2089, 360], [2089, 361], [2089, 362], [2089, 363], [2089, 364], [2089, 365], [2089, 366], [2089, 367], [2089, 368], [2089, 369], [2089, 370], [2089, 371], [2089, 373], [2089, 374], [2089, 375], [2089, 376], [2089, 377], [2089, 378], [2089, 379], [2089, 380], [2089, 381], [2089, 382], [2089, 383], [2089, 384], [2089, 385], [2089, 386], [2089, 387], [2089, 388], [2089, 389], [2089, 390], [2089, 391], [2089, 392], [2089, 393], [2089, 394], [2089, 395], [2089, 396], [2089, 397], [2089, 398], [2089, 399], [2089, 400], [2089, 401], [2089, 402], [2089, 403], [2089, 404], [2089, 405], [2089, 406], [2089, 407], [2089, 408], [2089, 409], [2089, 410], [2089, 411], [2089, 412], [2089, 413], [2089, 414], [2089, 415], [2089, 416], [2089, 417], [2089, 418], [2089, 419], [2089, 421], [2089, 422], [2089, 423], [2089, 424], [2089, 425], [2089, 426], [2089, 427], [2089, 428], [2089, 429], [2089, 430], [2089, 431], [2089, 432], [2089, 433], [2089, 434], [2089, 435], [2089, 436], [2089, 437], [2089, 438], [2089, 439], [2089, 440], [2089, 441], [2089, 442], [2089, 443], [2089, 444], [2089, 445], [2089, 446], [2089, 447], [2089, 448], [2089, 449], [2089, 450], [2089, 451], [2089, 452], [2089, 453], [2089, 454], [2089, 455], [2089, 456], [2089, 457], [2089, 458], [2089, 459], [2089, 460], [2089, 461], [2089, 462], [2089, 463], [2089, 464], [2089, 465], [2089, 466], [2089, 467], [2089, 468], [2089, 469], [2089, 470], [2089, 471], [2089, 472], [2089, 473], [2089, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[2093], [2094], [2095], [2096], [2097], [2098], [2099], [2100], [2101], [2102], [2103], [2104], [2105], [2106], [2107], [2108], [2109], [2110], [2111], [2112], [2113], [2114], [2115], [2116], [2117], [2118], [2119], [2120], [2121], [2122], [2123], [2124], [2125], [2126], [2127], [2128], [2129], [2130], [2131], [2132], [2133], [2134], [2135], [2136], [2137], [2138], [2139], [2140], [2141], [2142], [2143], [2144], [2145], [2146], [2147, 1], [2147, 2], [2147, 3], [2147, 4], [2147, 5], [2147, 6], [2147, 7], [2147, 8], [2147, 9], [2147, 10], [2147, 11], [2147, 12], [2147, 13], [2147, 14], [2147, 15], [2147, 16], [2147, 17], [2147, 18], [2147, 19], [2147, 20], [2147, 21], [2147, 22], [2147, 23], [2147, 24], [2147, 25], [2147, 26], [2147, 27], [2147, 29], [2147, 30], [2147, 31], [2147, 32], [2147, 33], [2147, 34], [2147, 35], [2147, 36], [2147, 37], [2147, 38], [2147, 39], [2147, 40], [2147, 41], [2147, 42], [2147, 43], [2147, 44], [2147, 45], [2147, 46], [2147, 47], [2147, 48], [2147, 49], [2147, 50], [2147, 51], [2147, 52], [2147, 53], [2147, 54], [2147, 55], [2147, 56], [2147, 57], [2147, 58], [2147, 59], [2147, 60], [2147, 61], [2147, 62], [2147, 63], [2147, 64], [2147, 65], [2147, 66], [2147, 67], [2147, 68], [2147, 69], [2147, 70], [2147, 71], [2147, 72], [2147, 73], [2147, 74], [2147, 75], [2147, 76], [2147, 77], [2147, 78], [2147, 79], [2147, 80], [2147, 81], [2147, 82], [2147, 84], [2147, 85], [2147, 86], [2147, 87], [2147, 88], [2147, 89], [2147, 90], [2147, 91], [2147, 92], [2147, 93], [2147, 94], [2147, 95], [2147, 96], [2147, 97], [2147, 98], [2147, 99], [2147, 100], [2147, 101], [2147, 102], [2147, 103], [2147, 104], [2147, 105], [2147, 106], [2147, 107], [2147, 108], [2147, 109], [2147, 110], [2147, 112], [2147, 113], [2147, 114], [2147, 115], [2147, 116], [2147, 117], [2147, 118], [2147, 119], [2147, 120], [2147, 121], [2147, 122], [2147, 123], [2147, 124], [2147, 125], [2147, 126], [2147, 127], [2147, 128], [2147, 129], [2147, 130], [2147, 131], [2147, 132], [2147, 133], [2147, 134], [2147, 135], [2147, 136], [2147, 137], [2147, 138], [2147, 139], [2147, 140], [2147, 141], [2147, 142], [2147, 143], [2147, 144], [2147, 145], [2147, 146], [2147, 147], [2147, 148], [2147, 149], [2147, 150], [2147, 151], [2147, 152], [2147, 153], [2147, 154], [2147, 155], [2147, 156], [2147, 157], [2147, 158], [2147, 159], [2147, 160], [2147, 161], [2147, 162], [2147, 163], [2147, 164], [2147, 165], [2147, 167], [2147, 168], [2147, 169], [2147, 170], [2147, 171], [2147, 172], [2147, 173], [2147, 174], [2147, 175], [2147, 176], [2147, 177], [2147, 178], [2147, 179], [2147, 180], [2147, 181], [2147, 182], [2147, 183], [2147, 184], [2147, 185], [2147, 186], [2147, 187], [2147, 188], [2147, 189], [2147, 190], [2147, 191], [2147, 192], [2147, 193], [2147, 194], [2147, 195], [2147, 196], [2147, 197], [2147, 198], [2147, 199], [2147, 200], [2147, 201], [2147, 202], [2147, 203], [2147, 204], [2147, 205], [2147, 206], [2147, 207], [2147, 208], [2147, 209], [2147, 210], [2147, 211], [2147, 212], [2147, 213], [2147, 215], [2147, 216], [2147, 217], [2147, 218], [2147, 219], [2147, 220], [2147, 221], [2147, 222], [2147, 223], [2147, 224], [2147, 225], [2147, 226], [2147, 227], [2147, 228], [2147, 229], [2147, 230], [2147, 231], [2147, 232], [2147, 233], [2147, 234], [2147, 235], [2147, 236], [2147, 237], [2147, 238], [2147, 239], [2147, 240], [2147, 241], [2147, 242], [2147, 243], [2147, 244], [2147, 245], [2147, 246], [2147, 247], [2147, 248], [2147, 249], [2147, 250], [2147, 251], [2147, 252], [2147, 253], [2147, 254], [2147, 255], [2147, 256], [2147, 257], [2147, 258], [2147, 259], [2147, 260], [2147, 261], [2147, 262], [2147, 263], [2147, 264], [2147, 265], [2147, 266], [2147, 267], [2147, 268], [2147, 270], [2147, 271], [2147, 272], [2147, 273], [2147, 274], [2147, 275], [2147, 276], [2147, 277], [2147, 278], [2147, 279], [2147, 280], [2147, 281], [2147, 282], [2147, 283], [2147, 284], [2147, 285], [2147, 286], [2147, 287], [2147, 288], [2147, 289], [2147, 290], [2147, 291], [2147, 292], [2147, 293], [2147, 294], [2147, 295], [2147, 296], [2147, 297], [2147, 298], [2147, 299], [2147, 300], [2147, 301], [2147, 302], [2147, 303], [2147, 304], [2147, 305], [2147, 306], [2147, 307], [2147, 308], [2147, 309], [2147, 310], [2147, 311], [2147, 312], [2147, 313], [2147, 314], [2147, 315], [2147, 316], [2147, 318], [2147, 319], [2147, 320], [2147, 321], [2147, 322], [2147, 323], [2147, 324], [2147, 325], [2147, 326], [2147, 327], [2147, 328], [2147, 329], [2147, 330], [2147, 331], [2147, 332], [2147, 333], [2147, 334], [2147, 335], [2147, 336], [2147, 337], [2147, 338], [2147, 339], [2147, 340], [2147, 341], [2147, 342], [2147, 343], [2147, 344], [2147, 345], [2147, 346], [2147, 347], [2147, 348], [2147, 349], [2147, 350], [2147, 351], [2147, 352], [2147, 353], [2147, 354], [2147, 355], [2147, 356], [2147, 357], [2147, 358], [2147, 359], [2147, 360], [2147, 361], [2147, 362], [2147, 363], [2147, 364], [2147, 365], [2147, 366], [2147, 367], [2147, 368], [2147, 369], [2147, 370], [2147, 371], [2147, 373], [2147, 374], [2147, 375], [2147, 376], [2147, 377], [2147, 378], [2147, 379], [2147, 380], [2147, 381], [2147, 382], [2147, 383], [2147, 384], [2147, 385], [2147, 386], [2147, 387], [2147, 388], [2147, 389], [2147, 390], [2147, 391], [2147, 392], [2147, 393], [2147, 394], [2147, 395], [2147, 396], [2147, 397], [2147, 398], [2147, 399], [2147, 400], [2147, 401], [2147, 402], [2147, 403], [2147, 404], [2147, 405], [2147, 406], [2147, 407], [2147, 408], [2147, 409], [2147, 410], [2147, 411], [2147, 412], [2147, 413], [2147, 414], [2147, 415], [2147, 416], [2147, 417], [2147, 418], [2147, 419], [2147, 421], [2147, 422], [2147, 423], [2147, 424], [2147, 425], [2147, 426], [2147, 427], [2147, 428], [2147, 429], [2147, 430], [2147, 431], [2147, 432], [2147, 433], [2147, 434], [2147, 435], [2147, 436], [2147, 437], [2147, 438], [2147, 439], [2147, 440], [2147, 441], [2147, 442], [2147, 443], [2147, 444], [2147, 445], [2147, 446], [2147, 447], [2147, 448], [2147, 449], [2147, 450], [2147, 451], [2147, 452], [2147, 453], [2147, 454], [2147, 455], [2147, 456], [2147, 457], [2147, 458], [2147, 459], [2147, 460], [2147, 461], [2147, 462], [2147, 463], [2147, 464], [2147, 465], [2147, 466], [2147, 467], [2147, 468], [2147, 469], [2147, 470], [2147, 471], [2147, 472], [2147, 473], [2147, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=208, paths=[[2149], [2150], [2151], [2152], [2153], [2154], [2155], [2156], [2157], [2158], [2159], [2160], [2161], [2162], [2163], [2164], [2165], [2166], [2167], [2168], [2169], [2170], [2171], [2172], [2173], [2174], [2175], [2176], [2177], [2178], [2179], [2180], [2181], [2182], [2183], [2184], [2185], [2186], [2187], [2188], [2189], [2190], [2191], [2192], [2193], [2194], [2195, 1], [2195, 2], [2195, 3], [2195, 4], [2195, 5], [2195, 6], [2195, 7], [2195, 8], [2195, 9], [2195, 10], [2195, 11], [2195, 12], [2195, 13], [2195, 14], [2195, 15], [2195, 16], [2195, 17], [2195, 18], [2195, 19], [2195, 20], [2195, 21], [2195, 22], [2195, 23], [2195, 24], [2195, 25], [2195, 26], [2195, 27], [2195, 29], [2195, 30], [2195, 31], [2195, 32], [2195, 33], [2195, 34], [2195, 35], [2195, 36], [2195, 37], [2195, 38], [2195, 39], [2195, 40], [2195, 41], [2195, 42], [2195, 43], [2195, 44], [2195, 45], [2195, 46], [2195, 47], [2195, 48], [2195, 49], [2195, 50], [2195, 51], [2195, 52], [2195, 53], [2195, 54], [2195, 55], [2195, 56], [2195, 57], [2195, 58], [2195, 59], [2195, 60], [2195, 61], [2195, 62], [2195, 63], [2195, 64], [2195, 65], [2195, 66], [2195, 67], [2195, 68], [2195, 69], [2195, 70], [2195, 71], [2195, 72], [2195, 73], [2195, 74], [2195, 75], [2195, 76], [2195, 77], [2195, 78], [2195, 79], [2195, 80], [2195, 81], [2195, 82], [2195, 84], [2195, 85], [2195, 86], [2195, 87], [2195, 88], [2195, 89], [2195, 90], [2195, 91], [2195, 92], [2195, 93], [2195, 94], [2195, 95], [2195, 96], [2195, 97], [2195, 98], [2195, 99], [2195, 100], [2195, 101], [2195, 102], [2195, 103], [2195, 104], [2195, 105], [2195, 106], [2195, 107], [2195, 108], [2195, 109], [2195, 110], [2195, 112], [2195, 113], [2195, 114], [2195, 115], [2195, 116], [2195, 117], [2195, 118], [2195, 119], [2195, 120], [2195, 121], [2195, 122], [2195, 123], [2195, 124], [2195, 125], [2195, 126], [2195, 127], [2195, 128], [2195, 129], [2195, 130], [2195, 131], [2195, 132], [2195, 133], [2195, 134], [2195, 135], [2195, 136], [2195, 137], [2195, 138], [2195, 139], [2195, 140], [2195, 141], [2195, 142], [2195, 143], [2195, 144], [2195, 145], [2195, 146], [2195, 147], [2195, 148], [2195, 149], [2195, 150], [2195, 151], [2195, 152], [2195, 153], [2195, 154], [2195, 155], [2195, 156], [2195, 157], [2195, 158], [2195, 159], [2195, 160], [2195, 161], [2195, 162], [2195, 163], [2195, 164], [2195, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=208, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=264, paths=[[2197], [2198], [2199], [2200], [2201], [2202], [2203], [2204], [2205], [2206], [2207], [2208], [2209], [2210], [2211], [2212], [2213], [2214], [2215], [2216], [2217], [2218], [2219], [2220], [2221], [2222], [2223], [2224], [2225], [2226], [2227], [2228], [2229], [2230], [2231], [2232], [2233], [2234], [2235], [2236], [2237], [2238], [2239], [2240], [2241], [2242], [2243], [2244], [2245], [2246], [2247], [2249], [2250], [2251], [2252], [2253], [2254], [2255], [2256], [2257], [2258], [2259], [2260], [2261], [2262], [2263], [2264], [2265], [2266], [2267], [2268], [2269], [2270], [2271], [2272], [2273], [2274], [2275], [2276], [2277], [2278], [2279], [2280], [2281], [2282], [2283], [2284], [2285], [2286], [2287], [2288], [2289], [2290], [2291], [2292], [2293], [2294], [2295], [2296], [2297], [2298], [2299], [2300, 1], [2300, 2], [2300, 3], [2300, 4], [2300, 5], [2300, 6], [2300, 7], [2300, 8], [2300, 9], [2300, 10], [2300, 11], [2300, 12], [2300, 13], [2300, 14], [2300, 15], [2300, 16], [2300, 17], [2300, 18], [2300, 19], [2300, 20], [2300, 21], [2300, 22], [2300, 23], [2300, 24], [2300, 25], [2300, 26], [2300, 27], [2300, 29], [2300, 30], [2300, 31], [2300, 32], [2300, 33], [2300, 34], [2300, 35], [2300, 36], [2300, 37], [2300, 38], [2300, 39], [2300, 40], [2300, 41], [2300, 42], [2300, 43], [2300, 44], [2300, 45], [2300, 46], [2300, 47], [2300, 48], [2300, 49], [2300, 50], [2300, 51], [2300, 52], [2300, 53], [2300, 54], [2300, 55], [2300, 56], [2300, 57], [2300, 58], [2300, 59], [2300, 60], [2300, 61], [2300, 62], [2300, 63], [2300, 64], [2300, 65], [2300, 66], [2300, 67], [2300, 68], [2300, 69], [2300, 70], [2300, 71], [2300, 72], [2300, 73], [2300, 74], [2300, 75], [2300, 76], [2300, 77], [2300, 78], [2300, 79], [2300, 80], [2300, 81], [2300, 82], [2300, 84], [2300, 85], [2300, 86], [2300, 87], [2300, 88], [2300, 89], [2300, 90], [2300, 91], [2300, 92], [2300, 93], [2300, 94], [2300, 95], [2300, 96], [2300, 97], [2300, 98], [2300, 99], [2300, 100], [2300, 101], [2300, 102], [2300, 103], [2300, 104], [2300, 105], [2300, 106], [2300, 107], [2300, 108], [2300, 109], [2300, 110], [2300, 112], [2300, 113], [2300, 114], [2300, 115], [2300, 116], [2300, 117], [2300, 118], [2300, 119], [2300, 120], [2300, 121], [2300, 122], [2300, 123], [2300, 124], [2300, 125], [2300, 126], [2300, 127], [2300, 128], [2300, 129], [2300, 130], [2300, 131], [2300, 132], [2300, 133], [2300, 134], [2300, 135], [2300, 136], [2300, 137], [2300, 138], [2300, 139], [2300, 140], [2300, 141], [2300, 142], [2300, 143], [2300, 144], [2300, 145], [2300, 146], [2300, 147], [2300, 148], [2300, 149], [2300, 150], [2300, 151], [2300, 152], [2300, 153], [2300, 154], [2300, 155], [2300, 156], [2300, 157], [2300, 158], [2300, 159], [2300, 160], [2300, 161], [2300, 162], [2300, 163], [2300, 164], [2300, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=264, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=162, paths=[[2301, 1], [2301, 2], [2301, 3], [2301, 4], [2301, 5], [2301, 6], [2301, 7], [2301, 8], [2301, 9], [2301, 10], [2301, 11], [2301, 12], [2301, 13], [2301, 14], [2301, 15], [2301, 16], [2301, 17], [2301, 18], [2301, 19], [2301, 20], [2301, 21], [2301, 22], [2301, 23], [2301, 24], [2301, 25], [2301, 26], [2301, 27], [2301, 29], [2301, 30], [2301, 31], [2301, 32], [2301, 33], [2301, 34], [2301, 35], [2301, 36], [2301, 37], [2301, 38], [2301, 39], [2301, 40], [2301, 41], [2301, 42], [2301, 43], [2301, 44], [2301, 45], [2301, 46], [2301, 47], [2301, 48], [2301, 49], [2301, 50], [2301, 51], [2301, 52], [2301, 53], [2301, 54], [2301, 55], [2301, 56], [2301, 57], [2301, 58], [2301, 59], [2301, 60], [2301, 61], [2301, 62], [2301, 63], [2301, 64], [2301, 65], [2301, 66], [2301, 67], [2301, 68], [2301, 69], [2301, 70], [2301, 71], [2301, 72], [2301, 73], [2301, 74], [2301, 75], [2301, 76], [2301, 77], [2301, 78], [2301, 79], [2301, 80], [2301, 81], [2301, 82], [2301, 84], [2301, 85], [2301, 86], [2301, 87], [2301, 88], [2301, 89], [2301, 90], [2301, 91], [2301, 92], [2301, 93], [2301, 94], [2301, 95], [2301, 96], [2301, 97], [2301, 98], [2301, 99], [2301, 100], [2301, 101], [2301, 102], [2301, 103], [2301, 104], [2301, 105], [2301, 106], [2301, 107], [2301, 108], [2301, 109], [2301, 110], [2301, 112], [2301, 113], [2301, 114], [2301, 115], [2301, 116], [2301, 117], [2301, 118], [2301, 119], [2301, 120], [2301, 121], [2301, 122], [2301, 123], [2301, 124], [2301, 125], [2301, 126], [2301, 127], [2301, 128], [2301, 129], [2301, 130], [2301, 131], [2301, 132], [2301, 133], [2301, 134], [2301, 135], [2301, 136], [2301, 137], [2301, 138], [2301, 139], [2301, 140], [2301, 141], [2301, 142], [2301, 143], [2301, 144], [2301, 145], [2301, 146], [2301, 147], [2301, 148], [2301, 149], [2301, 150], [2301, 151], [2301, 152], [2301, 153], [2301, 154], [2301, 155], [2301, 156], [2301, 157], [2301, 158], [2301, 159], [2301, 160], [2301, 161], [2301, 162], [2301, 163], [2301, 164], [2301, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=162, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=864, paths=[[2311], [2312], [2313], [2314], [2315], [2316], [2317], [2318], [2319], [2320], [2321], [2322], [2323], [2324], [2325], [2326], [2327], [2328], [2329], [2330], [2331], [2332], [2333], [2334], [2335], [2336], [2337], [2338], [2339], [2340], [2341], [2342], [2343], [2344], [2345], [2346], [2347], [2348], [2349], [2350], [2351], [2352], [2353], [2354], [2355], [2356], [2357], [2358], [2359], [2360], [2361], [2362], [2363], [2364], [2366], [2367], [2368], [2369], [2370], [2371], [2372], [2373], [2374], [2375], [2376], [2377], [2378], [2379], [2380], [2381], [2382], [2383], [2384], [2385], [2386], [2387], [2388], [2389], [2390], [2391], [2392], [2393], [2394], [2395], [2396], [2397], [2398], [2399], [2400], [2401], [2402], [2403], [2404], [2405], [2406], [2407], [2408], [2409], [2410], [2411], [2412], [2413], [2414], [2415], [2416], [2417], [2418], [2419], [2421], [2422], [2423], [2424], [2425], [2426], [2427], [2428], [2429], [2430], [2431], [2432], [2433], [2434], [2435], [2436], [2437], [2438], [2439], [2440], [2441], [2442], [2443], [2444], [2445], [2446], [2447], [2448], [2449], [2450], [2451], [2452], [2453], [2454], [2455], [2456], [2457], [2458], [2459], [2460], [2461], [2462], [2463], [2464], [2465], [2466], [2467], [2468], [2469], [2470], [2471], [2472], [2473], [2474], [2476], [2477], [2478], [2479], [2480], [2481], [2482], [2483], [2484], [2485], [2486], [2487], [2488], [2489], [2490], [2491], [2492], [2493], [2494], [2495], [2496], [2497], [2498], [2499], [2500], [2501], [2502], [2503], [2504], [2505], [2506], [2507], [2508], [2509], [2510], [2511], [2512], [2513], [2514], [2515], [2516], [2517], [2518], [2519], [2520], [2521], [2522], [2523], [2524], [2525], [2526], [2527], [2528], [2529], [2531], [2532], [2533], [2534], [2535], [2536], [2537], [2538], [2539], [2540], [2541], [2542], [2543], [2544], [2545], [2546], [2547], [2548], [2549], [2550], [2551], [2552], [2553], [2554], [2555], [2556], [2557], [2558], [2559], [2560], [2561], [2562], [2563], [2564], [2565], [2566], [2567], [2568], [2569], [2570], [2571], [2572], [2573], [2574], [2575], [2576], [2577], [2578], [2579], [2580], [2581], [2582], [2583], [2584], [2586], [2587], [2588], [2589], [2590], [2591], [2592], [2593], [2594], [2595], [2596], [2597], [2598], [2599], [2600], [2601], [2602], [2603], [2604], [2605], [2606], [2607], [2608], [2609], [2610], [2611], [2612], [2613], [2614], [2615], [2616], [2617], [2618], [2619], [2620], [2621], [2622], [2623], [2624], [2625], [2626], [2627], [2628], [2629], [2630], [2631], [2632], [2633], [2634], [2635], [2636], [2637], [2638], [2639], [2641], [2642], [2643], [2644], [2645], [2646], [2647], [2648], [2649], [2650], [2651], [2652], [2653], [2654], [2655], [2656], [2657], [2658], [2659], [2660], [2661], [2662], [2663], [2664], [2665], [2666], [2667], [2668], [2669], [2670], [2671], [2672], [2673], [2674], [2675], [2676], [2677], [2678], [2679], [2680], [2681], [2682], [2683], [2684], [2685], [2686], [2687], [2688], [2689], [2690], [2691], [2692], [2693], [2694], [2696], [2697], [2698], [2699], [2700], [2701], [2702], [2703], [2704], [2705], [2706], [2707], [2708], [2709], [2710], [2711], [2712], [2713], [2714], [2715], [2716], [2717], [2718], [2719], [2720], [2721], [2722], [2723], [2724], [2725], [2726], [2727], [2728], [2729], [2730], [2731], [2732], [2733], [2734], [2735], [2736], [2737], [2738], [2739], [2740], [2741], [2742], [2743], [2744], [2745], [2746], [2747], [2748], [2749], [2751], [2752], [2753], [2754], [2755], [2756], [2757], [2758], [2759], [2760], [2761], [2762], [2763], [2764], [2765], [2766], [2767], [2768], [2769], [2770], [2771], [2772], [2773], [2774], [2775], [2776], [2777], [2778], [2779], [2780], [2781], [2782], [2783], [2784], [2785], [2786], [2787], [2788], [2789], [2790], [2791], [2792], [2793], [2794], [2795], [2796], [2797], [2798], [2799], [2800], [2801], [2802], [2803], [2804], [2806], [2807], [2808], [2809], [2810], [2811], [2812], [2813], [2814], [2815], [2816], [2817], [2818], [2819], [2820], [2821], [2822], [2823], [2824], [2825], [2826], [2827], [2828], [2829], [2830], [2831], [2832], [2833], [2834], [2835], [2836], [2837], [2838], [2839], [2840], [2841], [2842], [2843], [2844], [2845], [2846], [2847], [2848], [2849], [2850], [2851], [2852], [2853], [2854], [2855], [2856], [2857], [2858], [2859], [2861], [2862], [2863], [2864], [2865], [2866], [2867], [2868], [2869], [2870], [2871], [2872], [2873], [2874], [2875], [2876], [2877], [2878], [2879], [2880], [2881], [2882], [2883], [2884], [2885], [2886], [2887], [2889], [2890], [2891], [2892], [2893], [2894], [2895], [2896], [2897], [2898], [2899], [2900], [2901], [2902], [2903], [2904], [2905], [2906], [2907], [2908], [2909], [2910], [2911], [2912], [2913], [2914], [2915], [2916], [2917], [2918], [2919], [2920], [2921], [2922], [2923], [2924], [2925], [2926], [2927], [2928], [2929], [2930], [2931], [2932], [2933], [2934], [2935], [2936], [2937], [2938], [2939], [2940], [2941], [2942], [2943, 1], [2943, 2], [2943, 3], [2943, 4], [2943, 5], [2943, 6], [2943, 7], [2943, 8], [2943, 9], [2943, 10], [2943, 11], [2943, 12], [2943, 13], [2943, 14], [2943, 15], [2943, 16], [2943, 17], [2943, 18], [2943, 19], [2943, 20], [2943, 21], [2943, 22], [2943, 23], [2943, 24], [2943, 25], [2943, 26], [2943, 27], [2943, 29], [2943, 30], [2943, 31], [2943, 32], [2943, 33], [2943, 34], [2943, 35], [2943, 36], [2943, 37], [2943, 38], [2943, 39], [2943, 40], [2943, 41], [2943, 42], [2943, 43], [2943, 44], [2943, 45], [2943, 46], [2943, 47], [2943, 48], [2943, 49], [2943, 50], [2943, 51], [2943, 52], [2943, 53], [2943, 54], [2943, 55], [2943, 56], [2943, 57], [2943, 58], [2943, 59], [2943, 60], [2943, 61], [2943, 62], [2943, 63], [2943, 64], [2943, 65], [2943, 66], [2943, 67], [2943, 68], [2943, 69], [2943, 70], [2943, 71], [2943, 72], [2943, 73], [2943, 74], [2943, 75], [2943, 76], [2943, 77], [2943, 78], [2943, 79], [2943, 80], [2943, 81], [2943, 82], [2943, 84], [2943, 85], [2943, 86], [2943, 87], [2943, 88], [2943, 89], [2943, 90], [2943, 91], [2943, 92], [2943, 93], [2943, 94], [2943, 95], [2943, 96], [2943, 97], [2943, 98], [2943, 99], [2943, 100], [2943, 101], [2943, 102], [2943, 103], [2943, 104], [2943, 105], [2943, 106], [2943, 107], [2943, 108], [2943, 109], [2943, 110], [2943, 112], [2943, 113], [2943, 114], [2943, 115], [2943, 116], [2943, 117], [2943, 118], [2943, 119], [2943, 120], [2943, 121], [2943, 122], [2943, 123], [2943, 124], [2943, 125], [2943, 126], [2943, 127], [2943, 128], [2943, 129], [2943, 130], [2943, 131], [2943, 132], [2943, 133], [2943, 134], [2943, 135], [2943, 136], [2943, 137], [2943, 138], [2943, 139], [2943, 140], [2943, 141], [2943, 142], [2943, 143], [2943, 144], [2943, 145], [2943, 146], [2943, 147], [2943, 148], [2943, 149], [2943, 150], [2943, 151], [2943, 152], [2943, 153], [2943, 154], [2943, 155], [2943, 156], [2943, 157], [2943, 158], [2943, 159], [2943, 160], [2943, 161], [2943, 162], [2943, 163], [2943, 164], [2943, 165], [2943, 167], [2943, 168], [2943, 169], [2943, 170], [2943, 171], [2943, 172], [2943, 173], [2943, 174], [2943, 175], [2943, 176], [2943, 177], [2943, 178], [2943, 179], [2943, 180], [2943, 181], [2943, 182], [2943, 183], [2943, 184], [2943, 185], [2943, 186], [2943, 187], [2943, 188], [2943, 189], [2943, 190], [2943, 191], [2943, 192], [2943, 193], [2943, 195], [2943, 196], [2943, 197], [2943, 198], [2943, 199], [2943, 200], [2943, 201], [2943, 202], [2943, 203], [2943, 204], [2943, 205], [2943, 206], [2943, 207], [2943, 208], [2943, 209], [2943, 210], [2943, 211], [2943, 212], [2943, 213], [2943, 214], [2943, 215], [2943, 216], [2943, 217], [2943, 218], [2943, 219], [2943, 220], [2943, 221], [2943, 222], [2943, 223], [2943, 224], [2943, 225], [2943, 226], [2943, 227], [2943, 228], [2943, 229], [2943, 230], [2943, 231], [2943, 232], [2943, 233], [2943, 234], [2943, 235], [2943, 236], [2943, 237], [2943, 238], [2943, 239], [2943, 240], [2943, 241], [2943, 242], [2943, 243], [2943, 244], [2943, 245], [2943, 246], [2943, 247], [2943, 248]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=852, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[2947], [2948], [2949], [2950], [2951], [2952], [2953], [2954], [2955], [2956], [2957], [2958], [2959], [2960], [2961], [2962], [2963], [2964], [2965], [2966], [2967], [2968], [2969], [2970], [2971], [2972], [2973], [2974], [2975], [2976], [2977], [2978], [2979], [2980], [2981], [2982], [2983], [2984], [2985], [2986], [2987], [2988], [2989], [2990], [2991], [2992], [2993], [2994], [2995], [2996], [2997], [2998], [2999], [3000], [3001, 1], [3001, 2], [3001, 3], [3001, 4], [3001, 5], [3001, 6], [3001, 7], [3001, 8], [3001, 9], [3001, 10], [3001, 11], [3001, 12], [3001, 13], [3001, 14], [3001, 15], [3001, 16], [3001, 17], [3001, 18], [3001, 19], [3001, 20], [3001, 21], [3001, 22], [3001, 23], [3001, 24], [3001, 25], [3001, 26], [3001, 27], [3001, 29], [3001, 30], [3001, 31], [3001, 32], [3001, 33], [3001, 34], [3001, 35], [3001, 36], [3001, 37], [3001, 38], [3001, 39], [3001, 40], [3001, 41], [3001, 42], [3001, 43], [3001, 44], [3001, 45], [3001, 46], [3001, 47], [3001, 48], [3001, 49], [3001, 50], [3001, 51], [3001, 52], [3001, 53], [3001, 54], [3001, 55], [3001, 56], [3001, 57], [3001, 58], [3001, 59], [3001, 60], [3001, 61], [3001, 62], [3001, 63], [3001, 64], [3001, 65], [3001, 66], [3001, 67], [3001, 68], [3001, 69], [3001, 70], [3001, 71], [3001, 72], [3001, 73], [3001, 74], [3001, 75], [3001, 76], [3001, 77], [3001, 78], [3001, 79], [3001, 80], [3001, 81], [3001, 82], [3001, 84], [3001, 85], [3001, 86], [3001, 87], [3001, 88], [3001, 89], [3001, 90], [3001, 91], [3001, 92], [3001, 93], [3001, 94], [3001, 95], [3001, 96], [3001, 97], [3001, 98], [3001, 99], [3001, 100], [3001, 101], [3001, 102], [3001, 103], [3001, 104], [3001, 105], [3001, 106], [3001, 107], [3001, 108], [3001, 109], [3001, 110], [3001, 112], [3001, 113], [3001, 114], [3001, 115], [3001, 116], [3001, 117], [3001, 118], [3001, 119], [3001, 120], [3001, 121], [3001, 122], [3001, 123], [3001, 124], [3001, 125], [3001, 126], [3001, 127], [3001, 128], [3001, 129], [3001, 130], [3001, 131], [3001, 132], [3001, 133], [3001, 134], [3001, 135], [3001, 136], [3001, 137], [3001, 138], [3001, 139], [3001, 140], [3001, 141], [3001, 142], [3001, 143], [3001, 144], [3001, 145], [3001, 146], [3001, 147], [3001, 148], [3001, 149], [3001, 150], [3001, 151], [3001, 152], [3001, 153], [3001, 154], [3001, 155], [3001, 156], [3001, 157], [3001, 158], [3001, 159], [3001, 160], [3001, 161], [3001, 162], [3001, 163], [3001, 164], [3001, 165], [3001, 167], [3001, 168], [3001, 169], [3001, 170], [3001, 171], [3001, 172], [3001, 173], [3001, 174], [3001, 175], [3001, 176], [3001, 177], [3001, 178], [3001, 179], [3001, 180], [3001, 181], [3001, 182], [3001, 183], [3001, 184], [3001, 185], [3001, 186], [3001, 187], [3001, 188], [3001, 189], [3001, 190], [3001, 191], [3001, 192], [3001, 193], [3001, 194], [3001, 195], [3001, 196], [3001, 197], [3001, 198], [3001, 199], [3001, 200], [3001, 201], [3001, 202], [3001, 203], [3001, 204], [3001, 205], [3001, 206], [3001, 207], [3001, 208], [3001, 209], [3001, 210], [3001, 211], [3001, 212], [3001, 213], [3001, 215], [3001, 216], [3001, 217], [3001, 218], [3001, 219], [3001, 220], [3001, 221], [3001, 222], [3001, 223], [3001, 224], [3001, 225], [3001, 226], [3001, 227], [3001, 228], [3001, 229], [3001, 230], [3001, 231], [3001, 232], [3001, 233], [3001, 234], [3001, 235], [3001, 236], [3001, 237], [3001, 238], [3001, 239], [3001, 240], [3001, 241], [3001, 242], [3001, 243], [3001, 244], [3001, 245], [3001, 246], [3001, 247], [3001, 248], [3001, 249], [3001, 250], [3001, 251], [3001, 252], [3001, 253], [3001, 254], [3001, 255], [3001, 256], [3001, 257], [3001, 258], [3001, 259], [3001, 260], [3001, 261], [3001, 262], [3001, 263], [3001, 264], [3001, 265], [3001, 266], [3001, 267], [3001, 268], [3001, 270], [3001, 271], [3001, 272], [3001, 273], [3001, 274], [3001, 275], [3001, 276], [3001, 277], [3001, 278], [3001, 279], [3001, 280], [3001, 281], [3001, 282], [3001, 283], [3001, 284], [3001, 285], [3001, 286], [3001, 287], [3001, 288], [3001, 289], [3001, 290], [3001, 291], [3001, 292], [3001, 293], [3001, 294], [3001, 295], [3001, 296], [3001, 297], [3001, 298], [3001, 299], [3001, 300], [3001, 301], [3001, 302], [3001, 303], [3001, 304], [3001, 305], [3001, 306], [3001, 307], [3001, 308], [3001, 309], [3001, 310], [3001, 311], [3001, 312], [3001, 313], [3001, 314], [3001, 315], [3001, 316], [3001, 318], [3001, 319], [3001, 320], [3001, 321], [3001, 322], [3001, 323], [3001, 324], [3001, 325], [3001, 326], [3001, 327], [3001, 328], [3001, 329], [3001, 330], [3001, 331], [3001, 332], [3001, 333], [3001, 334], [3001, 335], [3001, 336], [3001, 337], [3001, 338], [3001, 339], [3001, 340], [3001, 341], [3001, 342], [3001, 343], [3001, 344], [3001, 345], [3001, 346], [3001, 347], [3001, 348], [3001, 349], [3001, 350], [3001, 351], [3001, 352], [3001, 353], [3001, 354], [3001, 355], [3001, 356], [3001, 357], [3001, 358], [3001, 359], [3001, 360], [3001, 361], [3001, 362], [3001, 363], [3001, 364], [3001, 365], [3001, 366], [3001, 367], [3001, 368], [3001, 369], [3001, 370], [3001, 371], [3001, 373], [3001, 374], [3001, 375], [3001, 376], [3001, 377], [3001, 378], [3001, 379], [3001, 380], [3001, 381], [3001, 382], [3001, 383], [3001, 384], [3001, 385], [3001, 386], [3001, 387], [3001, 388], [3001, 389], [3001, 390], [3001, 391], [3001, 392], [3001, 393], [3001, 394], [3001, 395], [3001, 396], [3001, 397], [3001, 398], [3001, 399], [3001, 400], [3001, 401], [3001, 402], [3001, 403], [3001, 404], [3001, 405], [3001, 406], [3001, 407], [3001, 408], [3001, 409], [3001, 410], [3001, 411], [3001, 412], [3001, 413], [3001, 414], [3001, 415], [3001, 416], [3001, 417], [3001, 418], [3001, 419], [3001, 421], [3001, 422], [3001, 423], [3001, 424], [3001, 425], [3001, 426], [3001, 427], [3001, 428], [3001, 429], [3001, 430], [3001, 431], [3001, 432], [3001, 433], [3001, 434], [3001, 435], [3001, 436], [3001, 437], [3001, 438], [3001, 439], [3001, 440], [3001, 441], [3001, 442], [3001, 443], [3001, 444], [3001, 445], [3001, 446], [3001, 447], [3001, 448], [3001, 449], [3001, 450], [3001, 451], [3001, 452], [3001, 453], [3001, 454], [3001, 455], [3001, 456], [3001, 457], [3001, 458], [3001, 459], [3001, 460], [3001, 461], [3001, 462], [3001, 463], [3001, 464], [3001, 465], [3001, 466], [3001, 467], [3001, 468], [3001, 469], [3001, 470], [3001, 471], [3001, 472], [3001, 473], [3001, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3005], [3006], [3007], [3008], [3009], [3010], [3011], [3012], [3013], [3014], [3015], [3016], [3017], [3018], [3019], [3020], [3021], [3022], [3023], [3024], [3025], [3026], [3027], [3028], [3029], [3030], [3031], [3032], [3033], [3034], [3035], [3036], [3037], [3038], [3039], [3040], [3041], [3042], [3043], [3044], [3045], [3046], [3047], [3048], [3049], [3050], [3051], [3052], [3053], [3054], [3055], [3056], [3057], [3058], [3059, 1], [3059, 2], [3059, 3], [3059, 4], [3059, 5], [3059, 6], [3059, 7], [3059, 8], [3059, 9], [3059, 10], [3059, 11], [3059, 12], [3059, 13], [3059, 14], [3059, 15], [3059, 16], [3059, 17], [3059, 18], [3059, 19], [3059, 20], [3059, 21], [3059, 22], [3059, 23], [3059, 24], [3059, 25], [3059, 26], [3059, 27], [3059, 29], [3059, 30], [3059, 31], [3059, 32], [3059, 33], [3059, 34], [3059, 35], [3059, 36], [3059, 37], [3059, 38], [3059, 39], [3059, 40], [3059, 41], [3059, 42], [3059, 43], [3059, 44], [3059, 45], [3059, 46], [3059, 47], [3059, 48], [3059, 49], [3059, 50], [3059, 51], [3059, 52], [3059, 53], [3059, 54], [3059, 55], [3059, 56], [3059, 57], [3059, 58], [3059, 59], [3059, 60], [3059, 61], [3059, 62], [3059, 63], [3059, 64], [3059, 65], [3059, 66], [3059, 67], [3059, 68], [3059, 69], [3059, 70], [3059, 71], [3059, 72], [3059, 73], [3059, 74], [3059, 75], [3059, 76], [3059, 77], [3059, 78], [3059, 79], [3059, 80], [3059, 81], [3059, 82], [3059, 84], [3059, 85], [3059, 86], [3059, 87], [3059, 88], [3059, 89], [3059, 90], [3059, 91], [3059, 92], [3059, 93], [3059, 94], [3059, 95], [3059, 96], [3059, 97], [3059, 98], [3059, 99], [3059, 100], [3059, 101], [3059, 102], [3059, 103], [3059, 104], [3059, 105], [3059, 106], [3059, 107], [3059, 108], [3059, 109], [3059, 110], [3059, 112], [3059, 113], [3059, 114], [3059, 115], [3059, 116], [3059, 117], [3059, 118], [3059, 119], [3059, 120], [3059, 121], [3059, 122], [3059, 123], [3059, 124], [3059, 125], [3059, 126], [3059, 127], [3059, 128], [3059, 129], [3059, 130], [3059, 131], [3059, 132], [3059, 133], [3059, 134], [3059, 135], [3059, 136], [3059, 137], [3059, 138], [3059, 139], [3059, 140], [3059, 141], [3059, 142], [3059, 143], [3059, 144], [3059, 145], [3059, 146], [3059, 147], [3059, 148], [3059, 149], [3059, 150], [3059, 151], [3059, 152], [3059, 153], [3059, 154], [3059, 155], [3059, 156], [3059, 157], [3059, 158], [3059, 159], [3059, 160], [3059, 161], [3059, 162], [3059, 163], [3059, 164], [3059, 165], [3059, 167], [3059, 168], [3059, 169], [3059, 170], [3059, 171], [3059, 172], [3059, 173], [3059, 174], [3059, 175], [3059, 176], [3059, 177], [3059, 178], [3059, 179], [3059, 180], [3059, 181], [3059, 182], [3059, 183], [3059, 184], [3059, 185], [3059, 186], [3059, 187], [3059, 188], [3059, 189], [3059, 190], [3059, 191], [3059, 192], [3059, 193], [3059, 194], [3059, 195], [3059, 196], [3059, 197], [3059, 198], [3059, 199], [3059, 200], [3059, 201], [3059, 202], [3059, 203], [3059, 204], [3059, 205], [3059, 206], [3059, 207], [3059, 208], [3059, 209], [3059, 210], [3059, 211], [3059, 212], [3059, 213], [3059, 215], [3059, 216], [3059, 217], [3059, 218], [3059, 219], [3059, 220], [3059, 221], [3059, 222], [3059, 223], [3059, 224], [3059, 225], [3059, 226], [3059, 227], [3059, 228], [3059, 229], [3059, 230], [3059, 231], [3059, 232], [3059, 233], [3059, 234], [3059, 235], [3059, 236], [3059, 237], [3059, 238], [3059, 239], [3059, 240], [3059, 241], [3059, 242], [3059, 243], [3059, 244], [3059, 245], [3059, 246], [3059, 247], [3059, 248], [3059, 249], [3059, 250], [3059, 251], [3059, 252], [3059, 253], [3059, 254], [3059, 255], [3059, 256], [3059, 257], [3059, 258], [3059, 259], [3059, 260], [3059, 261], [3059, 262], [3059, 263], [3059, 264], [3059, 265], [3059, 266], [3059, 267], [3059, 268], [3059, 270], [3059, 271], [3059, 272], [3059, 273], [3059, 274], [3059, 275], [3059, 276], [3059, 277], [3059, 278], [3059, 279], [3059, 280], [3059, 281], [3059, 282], [3059, 283], [3059, 284], [3059, 285], [3059, 286], [3059, 287], [3059, 288], [3059, 289], [3059, 290], [3059, 291], [3059, 292], [3059, 293], [3059, 294], [3059, 295], [3059, 296], [3059, 297], [3059, 298], [3059, 299], [3059, 300], [3059, 301], [3059, 302], [3059, 303], [3059, 304], [3059, 305], [3059, 306], [3059, 307], [3059, 308], [3059, 309], [3059, 310], [3059, 311], [3059, 312], [3059, 313], [3059, 314], [3059, 315], [3059, 316], [3059, 318], [3059, 319], [3059, 320], [3059, 321], [3059, 322], [3059, 323], [3059, 324], [3059, 325], [3059, 326], [3059, 327], [3059, 328], [3059, 329], [3059, 330], [3059, 331], [3059, 332], [3059, 333], [3059, 334], [3059, 335], [3059, 336], [3059, 337], [3059, 338], [3059, 339], [3059, 340], [3059, 341], [3059, 342], [3059, 343], [3059, 344], [3059, 345], [3059, 346], [3059, 347], [3059, 348], [3059, 349], [3059, 350], [3059, 351], [3059, 352], [3059, 353], [3059, 354], [3059, 355], [3059, 356], [3059, 357], [3059, 358], [3059, 359], [3059, 360], [3059, 361], [3059, 362], [3059, 363], [3059, 364], [3059, 365], [3059, 366], [3059, 367], [3059, 368], [3059, 369], [3059, 370], [3059, 371], [3059, 373], [3059, 374], [3059, 375], [3059, 376], [3059, 377], [3059, 378], [3059, 379], [3059, 380], [3059, 381], [3059, 382], [3059, 383], [3059, 384], [3059, 385], [3059, 386], [3059, 387], [3059, 388], [3059, 389], [3059, 390], [3059, 391], [3059, 392], [3059, 393], [3059, 394], [3059, 395], [3059, 396], [3059, 397], [3059, 398], [3059, 399], [3059, 400], [3059, 401], [3059, 402], [3059, 403], [3059, 404], [3059, 405], [3059, 406], [3059, 407], [3059, 408], [3059, 409], [3059, 410], [3059, 411], [3059, 412], [3059, 413], [3059, 414], [3059, 415], [3059, 416], [3059, 417], [3059, 418], [3059, 419], [3059, 421], [3059, 422], [3059, 423], [3059, 424], [3059, 425], [3059, 426], [3059, 427], [3059, 428], [3059, 429], [3059, 430], [3059, 431], [3059, 432], [3059, 433], [3059, 434], [3059, 435], [3059, 436], [3059, 437], [3059, 438], [3059, 439], [3059, 440], [3059, 441], [3059, 442], [3059, 443], [3059, 444], [3059, 445], [3059, 446], [3059, 447], [3059, 448], [3059, 449], [3059, 450], [3059, 451], [3059, 452], [3059, 453], [3059, 454], [3059, 455], [3059, 456], [3059, 457], [3059, 458], [3059, 459], [3059, 460], [3059, 461], [3059, 462], [3059, 463], [3059, 464], [3059, 465], [3059, 466], [3059, 467], [3059, 468], [3059, 469], [3059, 470], [3059, 471], [3059, 472], [3059, 473], [3059, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3063], [3064], [3065], [3066], [3067], [3068], [3069], [3070], [3071], [3072], [3073], [3074], [3075], [3076], [3077], [3078], [3079], [3080], [3081], [3082], [3083], [3084], [3085], [3086], [3087], [3088], [3089], [3090], [3091], [3092], [3093], [3094], [3095], [3096], [3097], [3098], [3099], [3100], [3101], [3102], [3103], [3104], [3105], [3106], [3107], [3108], [3109], [3110], [3111], [3112], [3113], [3114], [3115], [3116], [3117, 1], [3117, 2], [3117, 3], [3117, 4], [3117, 5], [3117, 6], [3117, 7], [3117, 8], [3117, 9], [3117, 10], [3117, 11], [3117, 12], [3117, 13], [3117, 14], [3117, 15], [3117, 16], [3117, 17], [3117, 18], [3117, 19], [3117, 20], [3117, 21], [3117, 22], [3117, 23], [3117, 24], [3117, 25], [3117, 26], [3117, 27], [3117, 29], [3117, 30], [3117, 31], [3117, 32], [3117, 33], [3117, 34], [3117, 35], [3117, 36], [3117, 37], [3117, 38], [3117, 39], [3117, 40], [3117, 41], [3117, 42], [3117, 43], [3117, 44], [3117, 45], [3117, 46], [3117, 47], [3117, 48], [3117, 49], [3117, 50], [3117, 51], [3117, 52], [3117, 53], [3117, 54], [3117, 55], [3117, 56], [3117, 57], [3117, 58], [3117, 59], [3117, 60], [3117, 61], [3117, 62], [3117, 63], [3117, 64], [3117, 65], [3117, 66], [3117, 67], [3117, 68], [3117, 69], [3117, 70], [3117, 71], [3117, 72], [3117, 73], [3117, 74], [3117, 75], [3117, 76], [3117, 77], [3117, 78], [3117, 79], [3117, 80], [3117, 81], [3117, 82], [3117, 84], [3117, 85], [3117, 86], [3117, 87], [3117, 88], [3117, 89], [3117, 90], [3117, 91], [3117, 92], [3117, 93], [3117, 94], [3117, 95], [3117, 96], [3117, 97], [3117, 98], [3117, 99], [3117, 100], [3117, 101], [3117, 102], [3117, 103], [3117, 104], [3117, 105], [3117, 106], [3117, 107], [3117, 108], [3117, 109], [3117, 110], [3117, 112], [3117, 113], [3117, 114], [3117, 115], [3117, 116], [3117, 117], [3117, 118], [3117, 119], [3117, 120], [3117, 121], [3117, 122], [3117, 123], [3117, 124], [3117, 125], [3117, 126], [3117, 127], [3117, 128], [3117, 129], [3117, 130], [3117, 131], [3117, 132], [3117, 133], [3117, 134], [3117, 135], [3117, 136], [3117, 137], [3117, 138], [3117, 139], [3117, 140], [3117, 141], [3117, 142], [3117, 143], [3117, 144], [3117, 145], [3117, 146], [3117, 147], [3117, 148], [3117, 149], [3117, 150], [3117, 151], [3117, 152], [3117, 153], [3117, 154], [3117, 155], [3117, 156], [3117, 157], [3117, 158], [3117, 159], [3117, 160], [3117, 161], [3117, 162], [3117, 163], [3117, 164], [3117, 165], [3117, 167], [3117, 168], [3117, 169], [3117, 170], [3117, 171], [3117, 172], [3117, 173], [3117, 174], [3117, 175], [3117, 176], [3117, 177], [3117, 178], [3117, 179], [3117, 180], [3117, 181], [3117, 182], [3117, 183], [3117, 184], [3117, 185], [3117, 186], [3117, 187], [3117, 188], [3117, 189], [3117, 190], [3117, 191], [3117, 192], [3117, 193], [3117, 194], [3117, 195], [3117, 196], [3117, 197], [3117, 198], [3117, 199], [3117, 200], [3117, 201], [3117, 202], [3117, 203], [3117, 204], [3117, 205], [3117, 206], [3117, 207], [3117, 208], [3117, 209], [3117, 210], [3117, 211], [3117, 212], [3117, 213], [3117, 215], [3117, 216], [3117, 217], [3117, 218], [3117, 219], [3117, 220], [3117, 221], [3117, 222], [3117, 223], [3117, 224], [3117, 225], [3117, 226], [3117, 227], [3117, 228], [3117, 229], [3117, 230], [3117, 231], [3117, 232], [3117, 233], [3117, 234], [3117, 235], [3117, 236], [3117, 237], [3117, 238], [3117, 239], [3117, 240], [3117, 241], [3117, 242], [3117, 243], [3117, 244], [3117, 245], [3117, 246], [3117, 247], [3117, 248], [3117, 249], [3117, 250], [3117, 251], [3117, 252], [3117, 253], [3117, 254], [3117, 255], [3117, 256], [3117, 257], [3117, 258], [3117, 259], [3117, 260], [3117, 261], [3117, 262], [3117, 263], [3117, 264], [3117, 265], [3117, 266], [3117, 267], [3117, 268], [3117, 270], [3117, 271], [3117, 272], [3117, 273], [3117, 274], [3117, 275], [3117, 276], [3117, 277], [3117, 278], [3117, 279], [3117, 280], [3117, 281], [3117, 282], [3117, 283], [3117, 284], [3117, 285], [3117, 286], [3117, 287], [3117, 288], [3117, 289], [3117, 290], [3117, 291], [3117, 292], [3117, 293], [3117, 294], [3117, 295], [3117, 296], [3117, 297], [3117, 298], [3117, 299], [3117, 300], [3117, 301], [3117, 302], [3117, 303], [3117, 304], [3117, 305], [3117, 306], [3117, 307], [3117, 308], [3117, 309], [3117, 310], [3117, 311], [3117, 312], [3117, 313], [3117, 314], [3117, 315], [3117, 316], [3117, 318], [3117, 319], [3117, 320], [3117, 321], [3117, 322], [3117, 323], [3117, 324], [3117, 325], [3117, 326], [3117, 327], [3117, 328], [3117, 329], [3117, 330], [3117, 331], [3117, 332], [3117, 333], [3117, 334], [3117, 335], [3117, 336], [3117, 337], [3117, 338], [3117, 339], [3117, 340], [3117, 341], [3117, 342], [3117, 343], [3117, 344], [3117, 345], [3117, 346], [3117, 347], [3117, 348], [3117, 349], [3117, 350], [3117, 351], [3117, 352], [3117, 353], [3117, 354], [3117, 355], [3117, 356], [3117, 357], [3117, 358], [3117, 359], [3117, 360], [3117, 361], [3117, 362], [3117, 363], [3117, 364], [3117, 365], [3117, 366], [3117, 367], [3117, 368], [3117, 369], [3117, 370], [3117, 371], [3117, 373], [3117, 374], [3117, 375], [3117, 376], [3117, 377], [3117, 378], [3117, 379], [3117, 380], [3117, 381], [3117, 382], [3117, 383], [3117, 384], [3117, 385], [3117, 386], [3117, 387], [3117, 388], [3117, 389], [3117, 390], [3117, 391], [3117, 392], [3117, 393], [3117, 394], [3117, 395], [3117, 396], [3117, 397], [3117, 398], [3117, 399], [3117, 400], [3117, 401], [3117, 402], [3117, 403], [3117, 404], [3117, 405], [3117, 406], [3117, 407], [3117, 408], [3117, 409], [3117, 410], [3117, 411], [3117, 412], [3117, 413], [3117, 414], [3117, 415], [3117, 416], [3117, 417], [3117, 418], [3117, 419], [3117, 421], [3117, 422], [3117, 423], [3117, 424], [3117, 425], [3117, 426], [3117, 427], [3117, 428], [3117, 429], [3117, 430], [3117, 431], [3117, 432], [3117, 433], [3117, 434], [3117, 435], [3117, 436], [3117, 437], [3117, 438], [3117, 439], [3117, 440], [3117, 441], [3117, 442], [3117, 443], [3117, 444], [3117, 445], [3117, 446], [3117, 447], [3117, 448], [3117, 449], [3117, 450], [3117, 451], [3117, 452], [3117, 453], [3117, 454], [3117, 455], [3117, 456], [3117, 457], [3117, 458], [3117, 459], [3117, 460], [3117, 461], [3117, 462], [3117, 463], [3117, 464], [3117, 465], [3117, 466], [3117, 467], [3117, 468], [3117, 469], [3117, 470], [3117, 471], [3117, 472], [3117, 473], [3117, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=863, paths=[[3127], [3128], [3129], [3130], [3131], [3132], [3133], [3134], [3135], [3136], [3137], [3138], [3139], [3140], [3141], [3142], [3143], [3144], [3145], [3146], [3147], [3148], [3149], [3150], [3151], [3152], [3153], [3154], [3155], [3156], [3157], [3158], [3159], [3160], [3161], [3162], [3163], [3164], [3165], [3166], [3167], [3168], [3169], [3170], [3171], [3172], [3173], [3174], [3175], [3176], [3177], [3178], [3179], [3180], [3182], [3183], [3184], [3185], [3186], [3187], [3188], [3189], [3190], [3191], [3192], [3193], [3194], [3195], [3196], [3197], [3198], [3199], [3200], [3201], [3202], [3203], [3204], [3205], [3206], [3207], [3208], [3209], [3210], [3211], [3212], [3213], [3214], [3215], [3216], [3217], [3218], [3219], [3220], [3221], [3222], [3223], [3224], [3225], [3226], [3227], [3228], [3229], [3230], [3231], [3232], [3233], [3234], [3235], [3237], [3238], [3239], [3240], [3241], [3242], [3243], [3244], [3245], [3246], [3247], [3248], [3249], [3250], [3251], [3252], [3253], [3254], [3255], [3256], [3257], [3258], [3259], [3260], [3261], [3262], [3263], [3264], [3265], [3266], [3267], [3268], [3269], [3270], [3271], [3272], [3273], [3274], [3275], [3276], [3277], [3278], [3279], [3280], [3281], [3282], [3283], [3284], [3285], [3286], [3287], [3288], [3289], [3290], [3292], [3293], [3294], [3295], [3296], [3297], [3298], [3299], [3300], [3301], [3302], [3303], [3304], [3305], [3306], [3307], [3308], [3309], [3310], [3311], [3312], [3313], [3314], [3315], [3316], [3317], [3318], [3319], [3320], [3321], [3322], [3323], [3324], [3325], [3326], [3327], [3328], [3329], [3330], [3331], [3332], [3333], [3334], [3335], [3336], [3337], [3338], [3339], [3340], [3341], [3342], [3343], [3344], [3345], [3347], [3348], [3349], [3350], [3351], [3352], [3353], [3354], [3355], [3356], [3357], [3358], [3359], [3360], [3361], [3362], [3363], [3364], [3365], [3366], [3367], [3368], [3369], [3370], [3371], [3372], [3373], [3374], [3375], [3376], [3377], [3378], [3379], [3380], [3381], [3382], [3383], [3384], [3385], [3386], [3387], [3388], [3389], [3390], [3391], [3392], [3393], [3394], [3395], [3396], [3397], [3398], [3399], [3400], [3402], [3403], [3404], [3405], [3406], [3407], [3408], [3409], [3410], [3411], [3412], [3413], [3414], [3415], [3416], [3417], [3418], [3419], [3420], [3421], [3422], [3423], [3424], [3425], [3426], [3427], [3428], [3429], [3430], [3431], [3432], [3433], [3434], [3435], [3436], [3437], [3438], [3439], [3440], [3441], [3442], [3443], [3444], [3445], [3446], [3447], [3448], [3449], [3450], [3451], [3452], [3453], [3454], [3455], [3457], [3458], [3459], [3460], [3461], [3462], [3463], [3464], [3465], [3466], [3467], [3468], [3469], [3470], [3471], [3472], [3473], [3474], [3475], [3476], [3477], [3478], [3479], [3480], [3481], [3482], [3483], [3484], [3485], [3486], [3487], [3488], [3489], [3490], [3491], [3492], [3493], [3494], [3495], [3496], [3497], [3498], [3499], [3500], [3501], [3502], [3503], [3504], [3505], [3506], [3507], [3508], [3509], [3510], [3512], [3513], [3514], [3515], [3516], [3517], [3518], [3519], [3520], [3521], [3522], [3523], [3524], [3525], [3526], [3527], [3528], [3529], [3530], [3531], [3532], [3533], [3534], [3535], [3536], [3537], [3538], [3539], [3540], [3541], [3542], [3543], [3544], [3545], [3546], [3547], [3548], [3549], [3550], [3551], [3552], [3553], [3554], [3555], [3556], [3557], [3558], [3559], [3560], [3561], [3562], [3563], [3564], [3565], [3567], [3568], [3569], [3570], [3571], [3572], [3573], [3574], [3575], [3576], [3577], [3578], [3579], [3580], [3581], [3582], [3583], [3584], [3585], [3586], [3587], [3588], [3589], [3590], [3591], [3592], [3593], [3594], [3595], [3596], [3597], [3598], [3599], [3600], [3601], [3602], [3603], [3604], [3605], [3606], [3607], [3608], [3609], [3610], [3611], [3612], [3613], [3614], [3615], [3616], [3617], [3618], [3619], [3620], [3622], [3623], [3624], [3625], [3626], [3627], [3628], [3629], [3630], [3631], [3632], [3633], [3634], [3635], [3636], [3637], [3638], [3639], [3640], [3641], [3642], [3643], [3644], [3645], [3646], [3647], [3648], [3649], [3650], [3651], [3652], [3653], [3654], [3655], [3656], [3657], [3658], [3659], [3660], [3661], [3662], [3663], [3664], [3665], [3666], [3667], [3668], [3669], [3670], [3671], [3672], [3673], [3674], [3675], [3677], [3678], [3679], [3680], [3681], [3682], [3683], [3684], [3685], [3686], [3687], [3688], [3689], [3690], [3691], [3692], [3693], [3694], [3695], [3696], [3697], [3698], [3699], [3700], [3701], [3702], [3703], [3705], [3706], [3707], [3708], [3709], [3710], [3711], [3712], [3713], [3714], [3715], [3716], [3717], [3718], [3719], [3720], [3721], [3722], [3723], [3724], [3725], [3726], [3727], [3728], [3729], [3730], [3731], [3732], [3733], [3734], [3735], [3736], [3737], [3738], [3739], [3740], [3741], [3742], [3743], [3744], [3745], [3746], [3747], [3748], [3749], [3750], [3751], [3752], [3753], [3754], [3755], [3756], [3757], [3758], [3759, 1], [3759, 2], [3759, 3], [3759, 4], [3759, 5], [3759, 6], [3759, 7], [3759, 8], [3759, 9], [3759, 10], [3759, 11], [3759, 12], [3759, 13], [3759, 14], [3759, 15], [3759, 16], [3759, 17], [3759, 18], [3759, 19], [3759, 20], [3759, 21], [3759, 22], [3759, 23], [3759, 24], [3759, 25], [3759, 26], [3759, 27], [3759, 29], [3759, 30], [3759, 31], [3759, 32], [3759, 33], [3759, 34], [3759, 35], [3759, 36], [3759, 37], [3759, 38], [3759, 39], [3759, 40], [3759, 41], [3759, 42], [3759, 43], [3759, 44], [3759, 45], [3759, 46], [3759, 47], [3759, 48], [3759, 49], [3759, 50], [3759, 51], [3759, 52], [3759, 53], [3759, 54], [3759, 55], [3759, 56], [3759, 57], [3759, 58], [3759, 59], [3759, 60], [3759, 61], [3759, 62], [3759, 63], [3759, 64], [3759, 65], [3759, 66], [3759, 67], [3759, 68], [3759, 69], [3759, 70], [3759, 71], [3759, 72], [3759, 73], [3759, 74], [3759, 75], [3759, 76], [3759, 77], [3759, 78], [3759, 79], [3759, 80], [3759, 81], [3759, 82], [3759, 84], [3759, 85], [3759, 86], [3759, 87], [3759, 88], [3759, 89], [3759, 90], [3759, 91], [3759, 92], [3759, 93], [3759, 94], [3759, 95], [3759, 96], [3759, 97], [3759, 98], [3759, 99], [3759, 100], [3759, 101], [3759, 102], [3759, 103], [3759, 104], [3759, 105], [3759, 106], [3759, 107], [3759, 108], [3759, 109], [3759, 110], [3759, 112], [3759, 113], [3759, 114], [3759, 115], [3759, 116], [3759, 117], [3759, 118], [3759, 119], [3759, 120], [3759, 121], [3759, 122], [3759, 123], [3759, 124], [3759, 125], [3759, 126], [3759, 127], [3759, 128], [3759, 129], [3759, 130], [3759, 131], [3759, 132], [3759, 133], [3759, 134], [3759, 135], [3759, 136], [3759, 137], [3759, 138], [3759, 139], [3759, 140], [3759, 141], [3759, 142], [3759, 143], [3759, 144], [3759, 145], [3759, 146], [3759, 147], [3759, 148], [3759, 149], [3759, 150], [3759, 151], [3759, 152], [3759, 153], [3759, 154], [3759, 155], [3759, 156], [3759, 157], [3759, 158], [3759, 159], [3759, 160], [3759, 161], [3759, 162], [3759, 163], [3759, 164], [3759, 165], [3759, 167], [3759, 168], [3759, 169], [3759, 170], [3759, 171], [3759, 172], [3759, 173], [3759, 174], [3759, 175], [3759, 176], [3759, 177], [3759, 178], [3759, 179], [3759, 180], [3759, 181], [3759, 182], [3759, 183], [3759, 184], [3759, 185], [3759, 186], [3759, 187], [3759, 188], [3759, 189], [3759, 190], [3759, 191], [3759, 192], [3759, 193], [3759, 195], [3759, 196], [3759, 197], [3759, 198], [3759, 199], [3759, 200], [3759, 201], [3759, 202], [3759, 203], [3759, 205], [3759, 206], [3759, 207], [3759, 208], [3759, 209], [3759, 210], [3759, 211], [3759, 212], [3759, 213], [3759, 214], [3759, 215], [3759, 216], [3759, 217], [3759, 218], [3759, 219], [3759, 220], [3759, 221], [3759, 222], [3759, 223], [3759, 224], [3759, 225], [3759, 226], [3759, 227], [3759, 228], [3759, 229], [3759, 230], [3759, 231], [3759, 232], [3759, 233], [3759, 234], [3759, 235], [3759, 236], [3759, 237], [3759, 238], [3759, 239], [3759, 240], [3759, 241], [3759, 242], [3759, 243], [3759, 244], [3759, 245], [3759, 246], [3759, 247], [3759, 248]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=1, paths=[[3759, 204]]), one_qubit=852, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3763], [3764], [3765], [3766], [3767], [3768], [3769], [3770], [3771], [3772], [3773], [3774], [3775], [3776], [3777], [3778], [3779], [3780], [3781], [3782], [3783], [3784], [3785], [3786], [3787], [3788], [3789], [3790], [3791], [3792], [3793], [3794], [3795], [3796], [3797], [3798], [3799], [3800], [3801], [3802], [3803], [3804], [3805], [3806], [3807], [3808], [3809], [3810], [3811], [3812], [3813], [3814], [3815], [3816], [3817, 1], [3817, 2], [3817, 3], [3817, 4], [3817, 5], [3817, 6], [3817, 7], [3817, 8], [3817, 9], [3817, 10], [3817, 11], [3817, 12], [3817, 13], [3817, 14], [3817, 15], [3817, 16], [3817, 17], [3817, 18], [3817, 19], [3817, 20], [3817, 21], [3817, 22], [3817, 23], [3817, 24], [3817, 25], [3817, 26], [3817, 27], [3817, 29], [3817, 30], [3817, 31], [3817, 32], [3817, 33], [3817, 34], [3817, 35], [3817, 36], [3817, 37], [3817, 38], [3817, 39], [3817, 40], [3817, 41], [3817, 42], [3817, 43], [3817, 44], [3817, 45], [3817, 46], [3817, 47], [3817, 48], [3817, 49], [3817, 50], [3817, 51], [3817, 52], [3817, 53], [3817, 54], [3817, 55], [3817, 56], [3817, 57], [3817, 58], [3817, 59], [3817, 60], [3817, 61], [3817, 62], [3817, 63], [3817, 64], [3817, 65], [3817, 66], [3817, 67], [3817, 68], [3817, 69], [3817, 70], [3817, 71], [3817, 72], [3817, 73], [3817, 74], [3817, 75], [3817, 76], [3817, 77], [3817, 78], [3817, 79], [3817, 80], [3817, 81], [3817, 82], [3817, 84], [3817, 85], [3817, 86], [3817, 87], [3817, 88], [3817, 89], [3817, 90], [3817, 91], [3817, 92], [3817, 93], [3817, 94], [3817, 95], [3817, 96], [3817, 97], [3817, 98], [3817, 99], [3817, 100], [3817, 101], [3817, 102], [3817, 103], [3817, 104], [3817, 105], [3817, 106], [3817, 107], [3817, 108], [3817, 109], [3817, 110], [3817, 112], [3817, 113], [3817, 114], [3817, 115], [3817, 116], [3817, 117], [3817, 118], [3817, 119], [3817, 120], [3817, 121], [3817, 122], [3817, 123], [3817, 124], [3817, 125], [3817, 126], [3817, 127], [3817, 128], [3817, 129], [3817, 130], [3817, 131], [3817, 132], [3817, 133], [3817, 134], [3817, 135], [3817, 136], [3817, 137], [3817, 138], [3817, 139], [3817, 140], [3817, 141], [3817, 142], [3817, 143], [3817, 144], [3817, 145], [3817, 146], [3817, 147], [3817, 148], [3817, 149], [3817, 150], [3817, 151], [3817, 152], [3817, 153], [3817, 154], [3817, 155], [3817, 156], [3817, 157], [3817, 158], [3817, 159], [3817, 160], [3817, 161], [3817, 162], [3817, 163], [3817, 164], [3817, 165], [3817, 167], [3817, 168], [3817, 169], [3817, 170], [3817, 171], [3817, 172], [3817, 173], [3817, 174], [3817, 175], [3817, 176], [3817, 177], [3817, 178], [3817, 179], [3817, 180], [3817, 181], [3817, 182], [3817, 183], [3817, 184], [3817, 185], [3817, 186], [3817, 187], [3817, 188], [3817, 189], [3817, 190], [3817, 191], [3817, 192], [3817, 193], [3817, 194], [3817, 195], [3817, 196], [3817, 197], [3817, 198], [3817, 199], [3817, 200], [3817, 201], [3817, 202], [3817, 203], [3817, 204], [3817, 205], [3817, 206], [3817, 207], [3817, 208], [3817, 209], [3817, 210], [3817, 211], [3817, 212], [3817, 213], [3817, 215], [3817, 216], [3817, 217], [3817, 218], [3817, 219], [3817, 220], [3817, 221], [3817, 222], [3817, 223], [3817, 224], [3817, 225], [3817, 226], [3817, 227], [3817, 228], [3817, 229], [3817, 230], [3817, 231], [3817, 232], [3817, 233], [3817, 234], [3817, 235], [3817, 236], [3817, 237], [3817, 238], [3817, 239], [3817, 240], [3817, 241], [3817, 242], [3817, 243], [3817, 244], [3817, 245], [3817, 246], [3817, 247], [3817, 248], [3817, 249], [3817, 250], [3817, 251], [3817, 252], [3817, 253], [3817, 254], [3817, 255], [3817, 256], [3817, 257], [3817, 258], [3817, 259], [3817, 260], [3817, 261], [3817, 262], [3817, 263], [3817, 264], [3817, 265], [3817, 266], [3817, 267], [3817, 268], [3817, 270], [3817, 271], [3817, 272], [3817, 273], [3817, 274], [3817, 275], [3817, 276], [3817, 277], [3817, 278], [3817, 279], [3817, 280], [3817, 281], [3817, 282], [3817, 283], [3817, 284], [3817, 285], [3817, 286], [3817, 287], [3817, 288], [3817, 289], [3817, 290], [3817, 291], [3817, 292], [3817, 293], [3817, 294], [3817, 295], [3817, 296], [3817, 297], [3817, 298], [3817, 299], [3817, 300], [3817, 301], [3817, 302], [3817, 303], [3817, 304], [3817, 305], [3817, 306], [3817, 307], [3817, 308], [3817, 309], [3817, 310], [3817, 311], [3817, 312], [3817, 313], [3817, 314], [3817, 315], [3817, 316], [3817, 318], [3817, 319], [3817, 320], [3817, 321], [3817, 322], [3817, 323], [3817, 324], [3817, 325], [3817, 326], [3817, 327], [3817, 328], [3817, 329], [3817, 330], [3817, 331], [3817, 332], [3817, 333], [3817, 334], [3817, 335], [3817, 336], [3817, 337], [3817, 338], [3817, 339], [3817, 340], [3817, 341], [3817, 342], [3817, 343], [3817, 344], [3817, 345], [3817, 346], [3817, 347], [3817, 348], [3817, 349], [3817, 350], [3817, 351], [3817, 352], [3817, 353], [3817, 354], [3817, 355], [3817, 356], [3817, 357], [3817, 358], [3817, 359], [3817, 360], [3817, 361], [3817, 362], [3817, 363], [3817, 364], [3817, 365], [3817, 366], [3817, 367], [3817, 368], [3817, 369], [3817, 370], [3817, 371], [3817, 373], [3817, 374], [3817, 375], [3817, 376], [3817, 377], [3817, 378], [3817, 379], [3817, 380], [3817, 381], [3817, 382], [3817, 383], [3817, 384], [3817, 385], [3817, 386], [3817, 387], [3817, 388], [3817, 389], [3817, 390], [3817, 391], [3817, 392], [3817, 393], [3817, 394], [3817, 395], [3817, 396], [3817, 397], [3817, 398], [3817, 399], [3817, 400], [3817, 401], [3817, 402], [3817, 403], [3817, 404], [3817, 405], [3817, 406], [3817, 407], [3817, 408], [3817, 409], [3817, 410], [3817, 411], [3817, 412], [3817, 413], [3817, 414], [3817, 415], [3817, 416], [3817, 417], [3817, 418], [3817, 419], [3817, 421], [3817, 422], [3817, 423], [3817, 424], [3817, 425], [3817, 426], [3817, 427], [3817, 428], [3817, 429], [3817, 430], [3817, 431], [3817, 432], [3817, 433], [3817, 434], [3817, 435], [3817, 436], [3817, 437], [3817, 438], [3817, 439], [3817, 440], [3817, 441], [3817, 442], [3817, 443], [3817, 444], [3817, 445], [3817, 446], [3817, 447], [3817, 448], [3817, 449], [3817, 450], [3817, 451], [3817, 452], [3817, 453], [3817, 454], [3817, 455], [3817, 456], [3817, 457], [3817, 458], [3817, 459], [3817, 460], [3817, 461], [3817, 462], [3817, 463], [3817, 464], [3817, 465], [3817, 466], [3817, 467], [3817, 468], [3817, 469], [3817, 470], [3817, 471], [3817, 472], [3817, 473], [3817, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3821], [3822], [3823], [3824], [3825], [3826], [3827], [3828], [3829], [3830], [3831], [3832], [3833], [3834], [3835], [3836], [3837], [3838], [3839], [3840], [3841], [3842], [3843], [3844], [3845], [3846], [3847], [3848], [3849], [3850], [3851], [3852], [3853], [3854], [3855], [3856], [3857], [3858], [3859], [3860], [3861], [3862], [3863], [3864], [3865], [3866], [3867], [3868], [3869], [3870], [3871], [3872], [3873], [3874], [3875, 1], [3875, 2], [3875, 3], [3875, 4], [3875, 5], [3875, 6], [3875, 7], [3875, 8], [3875, 9], [3875, 10], [3875, 11], [3875, 12], [3875, 13], [3875, 14], [3875, 15], [3875, 16], [3875, 17], [3875, 18], [3875, 19], [3875, 20], [3875, 21], [3875, 22], [3875, 23], [3875, 24], [3875, 25], [3875, 26], [3875, 27], [3875, 29], [3875, 30], [3875, 31], [3875, 32], [3875, 33], [3875, 34], [3875, 35], [3875, 36], [3875, 37], [3875, 38], [3875, 39], [3875, 40], [3875, 41], [3875, 42], [3875, 43], [3875, 44], [3875, 45], [3875, 46], [3875, 47], [3875, 48], [3875, 49], [3875, 50], [3875, 51], [3875, 52], [3875, 53], [3875, 54], [3875, 55], [3875, 56], [3875, 57], [3875, 58], [3875, 59], [3875, 60], [3875, 61], [3875, 62], [3875, 63], [3875, 64], [3875, 65], [3875, 66], [3875, 67], [3875, 68], [3875, 69], [3875, 70], [3875, 71], [3875, 72], [3875, 73], [3875, 74], [3875, 75], [3875, 76], [3875, 77], [3875, 78], [3875, 79], [3875, 80], [3875, 81], [3875, 82], [3875, 84], [3875, 85], [3875, 86], [3875, 87], [3875, 88], [3875, 89], [3875, 90], [3875, 91], [3875, 92], [3875, 93], [3875, 94], [3875, 95], [3875, 96], [3875, 97], [3875, 98], [3875, 99], [3875, 100], [3875, 101], [3875, 102], [3875, 103], [3875, 104], [3875, 105], [3875, 106], [3875, 107], [3875, 108], [3875, 109], [3875, 110], [3875, 112], [3875, 113], [3875, 114], [3875, 115], [3875, 116], [3875, 117], [3875, 118], [3875, 119], [3875, 120], [3875, 121], [3875, 122], [3875, 123], [3875, 124], [3875, 125], [3875, 126], [3875, 127], [3875, 128], [3875, 129], [3875, 130], [3875, 131], [3875, 132], [3875, 133], [3875, 134], [3875, 135], [3875, 136], [3875, 137], [3875, 138], [3875, 139], [3875, 140], [3875, 141], [3875, 142], [3875, 143], [3875, 144], [3875, 145], [3875, 146], [3875, 147], [3875, 148], [3875, 149], [3875, 150], [3875, 151], [3875, 152], [3875, 153], [3875, 154], [3875, 155], [3875, 156], [3875, 157], [3875, 158], [3875, 159], [3875, 160], [3875, 161], [3875, 162], [3875, 163], [3875, 164], [3875, 165], [3875, 167], [3875, 168], [3875, 169], [3875, 170], [3875, 171], [3875, 172], [3875, 173], [3875, 174], [3875, 175], [3875, 176], [3875, 177], [3875, 178], [3875, 179], [3875, 180], [3875, 181], [3875, 182], [3875, 183], [3875, 184], [3875, 185], [3875, 186], [3875, 187], [3875, 188], [3875, 189], [3875, 190], [3875, 191], [3875, 192], [3875, 193], [3875, 194], [3875, 195], [3875, 196], [3875, 197], [3875, 198], [3875, 199], [3875, 200], [3875, 201], [3875, 202], [3875, 203], [3875, 204], [3875, 205], [3875, 206], [3875, 207], [3875, 208], [3875, 209], [3875, 210], [3875, 211], [3875, 212], [3875, 213], [3875, 215], [3875, 216], [3875, 217], [3875, 218], [3875, 219], [3875, 220], [3875, 221], [3875, 222], [3875, 223], [3875, 224], [3875, 225], [3875, 226], [3875, 227], [3875, 228], [3875, 229], [3875, 230], [3875, 231], [3875, 232], [3875, 233], [3875, 234], [3875, 235], [3875, 236], [3875, 237], [3875, 238], [3875, 239], [3875, 240], [3875, 241], [3875, 242], [3875, 243], [3875, 244], [3875, 245], [3875, 246], [3875, 247], [3875, 248], [3875, 249], [3875, 250], [3875, 251], [3875, 252], [3875, 253], [3875, 254], [3875, 255], [3875, 256], [3875, 257], [3875, 258], [3875, 259], [3875, 260], [3875, 261], [3875, 262], [3875, 263], [3875, 264], [3875, 265], [3875, 266], [3875, 267], [3875, 268], [3875, 270], [3875, 271], [3875, 272], [3875, 273], [3875, 274], [3875, 275], [3875, 276], [3875, 277], [3875, 278], [3875, 279], [3875, 280], [3875, 281], [3875, 282], [3875, 283], [3875, 284], [3875, 285], [3875, 286], [3875, 287], [3875, 288], [3875, 289], [3875, 290], [3875, 291], [3875, 292], [3875, 293], [3875, 294], [3875, 295], [3875, 296], [3875, 297], [3875, 298], [3875, 299], [3875, 300], [3875, 301], [3875, 302], [3875, 303], [3875, 304], [3875, 305], [3875, 306], [3875, 307], [3875, 308], [3875, 309], [3875, 310], [3875, 311], [3875, 312], [3875, 313], [3875, 314], [3875, 315], [3875, 316], [3875, 318], [3875, 319], [3875, 320], [3875, 321], [3875, 322], [3875, 323], [3875, 324], [3875, 325], [3875, 326], [3875, 327], [3875, 328], [3875, 329], [3875, 330], [3875, 331], [3875, 332], [3875, 333], [3875, 334], [3875, 335], [3875, 336], [3875, 337], [3875, 338], [3875, 339], [3875, 340], [3875, 341], [3875, 342], [3875, 343], [3875, 344], [3875, 345], [3875, 346], [3875, 347], [3875, 348], [3875, 349], [3875, 350], [3875, 351], [3875, 352], [3875, 353], [3875, 354], [3875, 355], [3875, 356], [3875, 357], [3875, 358], [3875, 359], [3875, 360], [3875, 361], [3875, 362], [3875, 363], [3875, 364], [3875, 365], [3875, 366], [3875, 367], [3875, 368], [3875, 369], [3875, 370], [3875, 371], [3875, 373], [3875, 374], [3875, 375], [3875, 376], [3875, 377], [3875, 378], [3875, 379], [3875, 380], [3875, 381], [3875, 382], [3875, 383], [3875, 384], [3875, 385], [3875, 386], [3875, 387], [3875, 388], [3875, 389], [3875, 390], [3875, 391], [3875, 392], [3875, 393], [3875, 394], [3875, 395], [3875, 396], [3875, 397], [3875, 398], [3875, 399], [3875, 400], [3875, 401], [3875, 402], [3875, 403], [3875, 404], [3875, 405], [3875, 406], [3875, 407], [3875, 408], [3875, 409], [3875, 410], [3875, 411], [3875, 412], [3875, 413], [3875, 414], [3875, 415], [3875, 416], [3875, 417], [3875, 418], [3875, 419], [3875, 421], [3875, 422], [3875, 423], [3875, 424], [3875, 425], [3875, 426], [3875, 427], [3875, 428], [3875, 429], [3875, 430], [3875, 431], [3875, 432], [3875, 433], [3875, 434], [3875, 435], [3875, 436], [3875, 437], [3875, 438], [3875, 439], [3875, 440], [3875, 441], [3875, 442], [3875, 443], [3875, 444], [3875, 445], [3875, 446], [3875, 447], [3875, 448], [3875, 449], [3875, 450], [3875, 451], [3875, 452], [3875, 453], [3875, 454], [3875, 455], [3875, 456], [3875, 457], [3875, 458], [3875, 459], [3875, 460], [3875, 461], [3875, 462], [3875, 463], [3875, 464], [3875, 465], [3875, 466], [3875, 467], [3875, 468], [3875, 469], [3875, 470], [3875, 471], [3875, 472], [3875, 473], [3875, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3879], [3880], [3881], [3882], [3883], [3884], [3885], [3886], [3887], [3888], [3889], [3890], [3891], [3892], [3893], [3894], [3895], [3896], [3897], [3898], [3899], [3900], [3901], [3902], [3903], [3904], [3905], [3906], [3907], [3908], [3909], [3910], [3911], [3912], [3913], [3914], [3915], [3916], [3917], [3918], [3919], [3920], [3921], [3922], [3923], [3924], [3925], [3926], [3927], [3928], [3929], [3930], [3931], [3932], [3933, 1], [3933, 2], [3933, 3], [3933, 4], [3933, 5], [3933, 6], [3933, 7], [3933, 8], [3933, 9], [3933, 10], [3933, 11], [3933, 12], [3933, 13], [3933, 14], [3933, 15], [3933, 16], [3933, 17], [3933, 18], [3933, 19], [3933, 20], [3933, 21], [3933, 22], [3933, 23], [3933, 24], [3933, 25], [3933, 26], [3933, 27], [3933, 29], [3933, 30], [3933, 31], [3933, 32], [3933, 33], [3933, 34], [3933, 35], [3933, 36], [3933, 37], [3933, 38], [3933, 39], [3933, 40], [3933, 41], [3933, 42], [3933, 43], [3933, 44], [3933, 45], [3933, 46], [3933, 47], [3933, 48], [3933, 49], [3933, 50], [3933, 51], [3933, 52], [3933, 53], [3933, 54], [3933, 55], [3933, 56], [3933, 57], [3933, 58], [3933, 59], [3933, 60], [3933, 61], [3933, 62], [3933, 63], [3933, 64], [3933, 65], [3933, 66], [3933, 67], [3933, 68], [3933, 69], [3933, 70], [3933, 71], [3933, 72], [3933, 73], [3933, 74], [3933, 75], [3933, 76], [3933, 77], [3933, 78], [3933, 79], [3933, 80], [3933, 81], [3933, 82], [3933, 84], [3933, 85], [3933, 86], [3933, 87], [3933, 88], [3933, 89], [3933, 90], [3933, 91], [3933, 92], [3933, 93], [3933, 94], [3933, 95], [3933, 96], [3933, 97], [3933, 98], [3933, 99], [3933, 100], [3933, 101], [3933, 102], [3933, 103], [3933, 104], [3933, 105], [3933, 106], [3933, 107], [3933, 108], [3933, 109], [3933, 110], [3933, 112], [3933, 113], [3933, 114], [3933, 115], [3933, 116], [3933, 117], [3933, 118], [3933, 119], [3933, 120], [3933, 121], [3933, 122], [3933, 123], [3933, 124], [3933, 125], [3933, 126], [3933, 127], [3933, 128], [3933, 129], [3933, 130], [3933, 131], [3933, 132], [3933, 133], [3933, 134], [3933, 135], [3933, 136], [3933, 137], [3933, 138], [3933, 139], [3933, 140], [3933, 141], [3933, 142], [3933, 143], [3933, 144], [3933, 145], [3933, 146], [3933, 147], [3933, 148], [3933, 149], [3933, 150], [3933, 151], [3933, 152], [3933, 153], [3933, 154], [3933, 155], [3933, 156], [3933, 157], [3933, 158], [3933, 159], [3933, 160], [3933, 161], [3933, 162], [3933, 163], [3933, 164], [3933, 165], [3933, 167], [3933, 168], [3933, 169], [3933, 170], [3933, 171], [3933, 172], [3933, 173], [3933, 174], [3933, 175], [3933, 176], [3933, 177], [3933, 178], [3933, 179], [3933, 180], [3933, 181], [3933, 182], [3933, 183], [3933, 184], [3933, 185], [3933, 186], [3933, 187], [3933, 188], [3933, 189], [3933, 190], [3933, 191], [3933, 192], [3933, 193], [3933, 194], [3933, 195], [3933, 196], [3933, 197], [3933, 198], [3933, 199], [3933, 200], [3933, 201], [3933, 202], [3933, 203], [3933, 204], [3933, 205], [3933, 206], [3933, 207], [3933, 208], [3933, 209], [3933, 210], [3933, 211], [3933, 212], [3933, 213], [3933, 215], [3933, 216], [3933, 217], [3933, 218], [3933, 219], [3933, 220], [3933, 221], [3933, 222], [3933, 223], [3933, 224], [3933, 225], [3933, 226], [3933, 227], [3933, 228], [3933, 229], [3933, 230], [3933, 231], [3933, 232], [3933, 233], [3933, 234], [3933, 235], [3933, 236], [3933, 237], [3933, 238], [3933, 239], [3933, 240], [3933, 241], [3933, 242], [3933, 243], [3933, 244], [3933, 245], [3933, 246], [3933, 247], [3933, 248], [3933, 249], [3933, 250], [3933, 251], [3933, 252], [3933, 253], [3933, 254], [3933, 255], [3933, 256], [3933, 257], [3933, 258], [3933, 259], [3933, 260], [3933, 261], [3933, 262], [3933, 263], [3933, 264], [3933, 265], [3933, 266], [3933, 267], [3933, 268], [3933, 270], [3933, 271], [3933, 272], [3933, 273], [3933, 274], [3933, 275], [3933, 276], [3933, 277], [3933, 278], [3933, 279], [3933, 280], [3933, 281], [3933, 282], [3933, 283], [3933, 284], [3933, 285], [3933, 286], [3933, 287], [3933, 288], [3933, 289], [3933, 290], [3933, 291], [3933, 292], [3933, 293], [3933, 294], [3933, 295], [3933, 296], [3933, 297], [3933, 298], [3933, 299], [3933, 300], [3933, 301], [3933, 302], [3933, 303], [3933, 304], [3933, 305], [3933, 306], [3933, 307], [3933, 308], [3933, 309], [3933, 310], [3933, 311], [3933, 312], [3933, 313], [3933, 314], [3933, 315], [3933, 316], [3933, 318], [3933, 319], [3933, 320], [3933, 321], [3933, 322], [3933, 323], [3933, 324], [3933, 325], [3933, 326], [3933, 327], [3933, 328], [3933, 329], [3933, 330], [3933, 331], [3933, 332], [3933, 333], [3933, 334], [3933, 335], [3933, 336], [3933, 337], [3933, 338], [3933, 339], [3933, 340], [3933, 341], [3933, 342], [3933, 343], [3933, 344], [3933, 345], [3933, 346], [3933, 347], [3933, 348], [3933, 349], [3933, 350], [3933, 351], [3933, 352], [3933, 353], [3933, 354], [3933, 355], [3933, 356], [3933, 357], [3933, 358], [3933, 359], [3933, 360], [3933, 361], [3933, 362], [3933, 363], [3933, 364], [3933, 365], [3933, 366], [3933, 367], [3933, 368], [3933, 369], [3933, 370], [3933, 371], [3933, 373], [3933, 374], [3933, 375], [3933, 376], [3933, 377], [3933, 378], [3933, 379], [3933, 380], [3933, 381], [3933, 382], [3933, 383], [3933, 384], [3933, 385], [3933, 386], [3933, 387], [3933, 388], [3933, 389], [3933, 390], [3933, 391], [3933, 392], [3933, 393], [3933, 394], [3933, 395], [3933, 396], [3933, 397], [3933, 398], [3933, 399], [3933, 400], [3933, 401], [3933, 402], [3933, 403], [3933, 404], [3933, 405], [3933, 406], [3933, 407], [3933, 408], [3933, 409], [3933, 410], [3933, 411], [3933, 412], [3933, 413], [3933, 414], [3933, 415], [3933, 416], [3933, 417], [3933, 418], [3933, 419], [3933, 421], [3933, 422], [3933, 423], [3933, 424], [3933, 425], [3933, 426], [3933, 427], [3933, 428], [3933, 429], [3933, 430], [3933, 431], [3933, 432], [3933, 433], [3933, 434], [3933, 435], [3933, 436], [3933, 437], [3933, 438], [3933, 439], [3933, 440], [3933, 441], [3933, 442], [3933, 443], [3933, 444], [3933, 445], [3933, 446], [3933, 447], [3933, 448], [3933, 449], [3933, 450], [3933, 451], [3933, 452], [3933, 453], [3933, 454], [3933, 455], [3933, 456], [3933, 457], [3933, 458], [3933, 459], [3933, 460], [3933, 461], [3933, 462], [3933, 463], [3933, 464], [3933, 465], [3933, 466], [3933, 467], [3933, 468], [3933, 469], [3933, 470], [3933, 471], [3933, 472], [3933, 473], [3933, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3937], [3938], [3939], [3940], [3941], [3942], [3943], [3944], [3945], [3946], [3947], [3948], [3949], [3950], [3951], [3952], [3953], [3954], [3955], [3956], [3957], [3958], [3959], [3960], [3961], [3962], [3963], [3964], [3965], [3966], [3967], [3968], [3969], [3970], [3971], [3972], [3973], [3974], [3975], [3976], [3977], [3978], [3979], [3980], [3981], [3982], [3983], [3984], [3985], [3986], [3987], [3988], [3989], [3990], [3991, 1], [3991, 2], [3991, 3], [3991, 4], [3991, 5], [3991, 6], [3991, 7], [3991, 8], [3991, 9], [3991, 10], [3991, 11], [3991, 12], [3991, 13], [3991, 14], [3991, 15], [3991, 16], [3991, 17], [3991, 18], [3991, 19], [3991, 20], [3991, 21], [3991, 22], [3991, 23], [3991, 24], [3991, 25], [3991, 26], [3991, 27], [3991, 29], [3991, 30], [3991, 31], [3991, 32], [3991, 33], [3991, 34], [3991, 35], [3991, 36], [3991, 37], [3991, 38], [3991, 39], [3991, 40], [3991, 41], [3991, 42], [3991, 43], [3991, 44], [3991, 45], [3991, 46], [3991, 47], [3991, 48], [3991, 49], [3991, 50], [3991, 51], [3991, 52], [3991, 53], [3991, 54], [3991, 55], [3991, 56], [3991, 57], [3991, 58], [3991, 59], [3991, 60], [3991, 61], [3991, 62], [3991, 63], [3991, 64], [3991, 65], [3991, 66], [3991, 67], [3991, 68], [3991, 69], [3991, 70], [3991, 71], [3991, 72], [3991, 73], [3991, 74], [3991, 75], [3991, 76], [3991, 77], [3991, 78], [3991, 79], [3991, 80], [3991, 81], [3991, 82], [3991, 84], [3991, 85], [3991, 86], [3991, 87], [3991, 88], [3991, 89], [3991, 90], [3991, 91], [3991, 92], [3991, 93], [3991, 94], [3991, 95], [3991, 96], [3991, 97], [3991, 98], [3991, 99], [3991, 100], [3991, 101], [3991, 102], [3991, 103], [3991, 104], [3991, 105], [3991, 106], [3991, 107], [3991, 108], [3991, 109], [3991, 110], [3991, 112], [3991, 113], [3991, 114], [3991, 115], [3991, 116], [3991, 117], [3991, 118], [3991, 119], [3991, 120], [3991, 121], [3991, 122], [3991, 123], [3991, 124], [3991, 125], [3991, 126], [3991, 127], [3991, 128], [3991, 129], [3991, 130], [3991, 131], [3991, 132], [3991, 133], [3991, 134], [3991, 135], [3991, 136], [3991, 137], [3991, 138], [3991, 139], [3991, 140], [3991, 141], [3991, 142], [3991, 143], [3991, 144], [3991, 145], [3991, 146], [3991, 147], [3991, 148], [3991, 149], [3991, 150], [3991, 151], [3991, 152], [3991, 153], [3991, 154], [3991, 155], [3991, 156], [3991, 157], [3991, 158], [3991, 159], [3991, 160], [3991, 161], [3991, 162], [3991, 163], [3991, 164], [3991, 165], [3991, 167], [3991, 168], [3991, 169], [3991, 170], [3991, 171], [3991, 172], [3991, 173], [3991, 174], [3991, 175], [3991, 176], [3991, 177], [3991, 178], [3991, 179], [3991, 180], [3991, 181], [3991, 182], [3991, 183], [3991, 184], [3991, 185], [3991, 186], [3991, 187], [3991, 188], [3991, 189], [3991, 190], [3991, 191], [3991, 192], [3991, 193], [3991, 194], [3991, 195], [3991, 196], [3991, 197], [3991, 198], [3991, 199], [3991, 200], [3991, 201], [3991, 202], [3991, 203], [3991, 204], [3991, 205], [3991, 206], [3991, 207], [3991, 208], [3991, 209], [3991, 210], [3991, 211], [3991, 212], [3991, 213], [3991, 215], [3991, 216], [3991, 217], [3991, 218], [3991, 219], [3991, 220], [3991, 221], [3991, 222], [3991, 223], [3991, 224], [3991, 225], [3991, 226], [3991, 227], [3991, 228], [3991, 229], [3991, 230], [3991, 231], [3991, 232], [3991, 233], [3991, 234], [3991, 235], [3991, 236], [3991, 237], [3991, 238], [3991, 239], [3991, 240], [3991, 241], [3991, 242], [3991, 243], [3991, 244], [3991, 245], [3991, 246], [3991, 247], [3991, 248], [3991, 249], [3991, 250], [3991, 251], [3991, 252], [3991, 253], [3991, 254], [3991, 255], [3991, 256], [3991, 257], [3991, 258], [3991, 259], [3991, 260], [3991, 261], [3991, 262], [3991, 263], [3991, 264], [3991, 265], [3991, 266], [3991, 267], [3991, 268], [3991, 270], [3991, 271], [3991, 272], [3991, 273], [3991, 274], [3991, 275], [3991, 276], [3991, 277], [3991, 278], [3991, 279], [3991, 280], [3991, 281], [3991, 282], [3991, 283], [3991, 284], [3991, 285], [3991, 286], [3991, 287], [3991, 288], [3991, 289], [3991, 290], [3991, 291], [3991, 292], [3991, 293], [3991, 294], [3991, 295], [3991, 296], [3991, 297], [3991, 298], [3991, 299], [3991, 300], [3991, 301], [3991, 302], [3991, 303], [3991, 304], [3991, 305], [3991, 306], [3991, 307], [3991, 308], [3991, 309], [3991, 310], [3991, 311], [3991, 312], [3991, 313], [3991, 314], [3991, 315], [3991, 316], [3991, 318], [3991, 319], [3991, 320], [3991, 321], [3991, 322], [3991, 323], [3991, 324], [3991, 325], [3991, 326], [3991, 327], [3991, 328], [3991, 329], [3991, 330], [3991, 331], [3991, 332], [3991, 333], [3991, 334], [3991, 335], [3991, 336], [3991, 337], [3991, 338], [3991, 339], [3991, 340], [3991, 341], [3991, 342], [3991, 343], [3991, 344], [3991, 345], [3991, 346], [3991, 347], [3991, 348], [3991, 349], [3991, 350], [3991, 351], [3991, 352], [3991, 353], [3991, 354], [3991, 355], [3991, 356], [3991, 357], [3991, 358], [3991, 359], [3991, 360], [3991, 361], [3991, 362], [3991, 363], [3991, 364], [3991, 365], [3991, 366], [3991, 367], [3991, 368], [3991, 369], [3991, 370], [3991, 371], [3991, 373], [3991, 374], [3991, 375], [3991, 376], [3991, 377], [3991, 378], [3991, 379], [3991, 380], [3991, 381], [3991, 382], [3991, 383], [3991, 384], [3991, 385], [3991, 386], [3991, 387], [3991, 388], [3991, 389], [3991, 390], [3991, 391], [3991, 392], [3991, 393], [3991, 394], [3991, 395], [3991, 396], [3991, 397], [3991, 398], [3991, 399], [3991, 400], [3991, 401], [3991, 402], [3991, 403], [3991, 404], [3991, 405], [3991, 406], [3991, 407], [3991, 408], [3991, 409], [3991, 410], [3991, 411], [3991, 412], [3991, 413], [3991, 414], [3991, 415], [3991, 416], [3991, 417], [3991, 418], [3991, 419], [3991, 421], [3991, 422], [3991, 423], [3991, 424], [3991, 425], [3991, 426], [3991, 427], [3991, 428], [3991, 429], [3991, 430], [3991, 431], [3991, 432], [3991, 433], [3991, 434], [3991, 435], [3991, 436], [3991, 437], [3991, 438], [3991, 439], [3991, 440], [3991, 441], [3991, 442], [3991, 443], [3991, 444], [3991, 445], [3991, 446], [3991, 447], [3991, 448], [3991, 449], [3991, 450], [3991, 451], [3991, 452], [3991, 453], [3991, 454], [3991, 455], [3991, 456], [3991, 457], [3991, 458], [3991, 459], [3991, 460], [3991, 461], [3991, 462], [3991, 463], [3991, 464], [3991, 465], [3991, 466], [3991, 467], [3991, 468], [3991, 469], [3991, 470], [3991, 471], [3991, 472], [3991, 473], [3991, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[3995], [3996], [3997], [3998], [3999], [4000], [4001], [4002], [4003], [4004], [4005], [4006], [4007], [4008], [4009], [4010], [4011], [4012], [4013], [4014], [4015], [4016], [4017], [4018], [4019], [4020], [4021], [4022], [4023], [4024], [4025], [4026], [4027], [4028], [4029], [4030], [4031], [4032], [4033], [4034], [4035], [4036], [4037], [4038], [4039], [4040], [4041], [4042], [4043], [4044], [4045], [4046], [4047], [4048], [4049, 1], [4049, 2], [4049, 3], [4049, 4], [4049, 5], [4049, 6], [4049, 7], [4049, 8], [4049, 9], [4049, 10], [4049, 11], [4049, 12], [4049, 13], [4049, 14], [4049, 15], [4049, 16], [4049, 17], [4049, 18], [4049, 19], [4049, 20], [4049, 21], [4049, 22], [4049, 23], [4049, 24], [4049, 25], [4049, 26], [4049, 27], [4049, 29], [4049, 30], [4049, 31], [4049, 32], [4049, 33], [4049, 34], [4049, 35], [4049, 36], [4049, 37], [4049, 38], [4049, 39], [4049, 40], [4049, 41], [4049, 42], [4049, 43], [4049, 44], [4049, 45], [4049, 46], [4049, 47], [4049, 48], [4049, 49], [4049, 50], [4049, 51], [4049, 52], [4049, 53], [4049, 54], [4049, 55], [4049, 56], [4049, 57], [4049, 58], [4049, 59], [4049, 60], [4049, 61], [4049, 62], [4049, 63], [4049, 64], [4049, 65], [4049, 66], [4049, 67], [4049, 68], [4049, 69], [4049, 70], [4049, 71], [4049, 72], [4049, 73], [4049, 74], [4049, 75], [4049, 76], [4049, 77], [4049, 78], [4049, 79], [4049, 80], [4049, 81], [4049, 82], [4049, 84], [4049, 85], [4049, 86], [4049, 87], [4049, 88], [4049, 89], [4049, 90], [4049, 91], [4049, 92], [4049, 93], [4049, 94], [4049, 95], [4049, 96], [4049, 97], [4049, 98], [4049, 99], [4049, 100], [4049, 101], [4049, 102], [4049, 103], [4049, 104], [4049, 105], [4049, 106], [4049, 107], [4049, 108], [4049, 109], [4049, 110], [4049, 112], [4049, 113], [4049, 114], [4049, 115], [4049, 116], [4049, 117], [4049, 118], [4049, 119], [4049, 120], [4049, 121], [4049, 122], [4049, 123], [4049, 124], [4049, 125], [4049, 126], [4049, 127], [4049, 128], [4049, 129], [4049, 130], [4049, 131], [4049, 132], [4049, 133], [4049, 134], [4049, 135], [4049, 136], [4049, 137], [4049, 138], [4049, 139], [4049, 140], [4049, 141], [4049, 142], [4049, 143], [4049, 144], [4049, 145], [4049, 146], [4049, 147], [4049, 148], [4049, 149], [4049, 150], [4049, 151], [4049, 152], [4049, 153], [4049, 154], [4049, 155], [4049, 156], [4049, 157], [4049, 158], [4049, 159], [4049, 160], [4049, 161], [4049, 162], [4049, 163], [4049, 164], [4049, 165], [4049, 167], [4049, 168], [4049, 169], [4049, 170], [4049, 171], [4049, 172], [4049, 173], [4049, 174], [4049, 175], [4049, 176], [4049, 177], [4049, 178], [4049, 179], [4049, 180], [4049, 181], [4049, 182], [4049, 183], [4049, 184], [4049, 185], [4049, 186], [4049, 187], [4049, 188], [4049, 189], [4049, 190], [4049, 191], [4049, 192], [4049, 193], [4049, 194], [4049, 195], [4049, 196], [4049, 197], [4049, 198], [4049, 199], [4049, 200], [4049, 201], [4049, 202], [4049, 203], [4049, 204], [4049, 205], [4049, 206], [4049, 207], [4049, 208], [4049, 209], [4049, 210], [4049, 211], [4049, 212], [4049, 213], [4049, 215], [4049, 216], [4049, 217], [4049, 218], [4049, 219], [4049, 220], [4049, 221], [4049, 222], [4049, 223], [4049, 224], [4049, 225], [4049, 226], [4049, 227], [4049, 228], [4049, 229], [4049, 230], [4049, 231], [4049, 232], [4049, 233], [4049, 234], [4049, 235], [4049, 236], [4049, 237], [4049, 238], [4049, 239], [4049, 240], [4049, 241], [4049, 242], [4049, 243], [4049, 244], [4049, 245], [4049, 246], [4049, 247], [4049, 248], [4049, 249], [4049, 250], [4049, 251], [4049, 252], [4049, 253], [4049, 254], [4049, 255], [4049, 256], [4049, 257], [4049, 258], [4049, 259], [4049, 260], [4049, 261], [4049, 262], [4049, 263], [4049, 264], [4049, 265], [4049, 266], [4049, 267], [4049, 268], [4049, 270], [4049, 271], [4049, 272], [4049, 273], [4049, 274], [4049, 275], [4049, 276], [4049, 277], [4049, 278], [4049, 279], [4049, 280], [4049, 281], [4049, 282], [4049, 283], [4049, 284], [4049, 285], [4049, 286], [4049, 287], [4049, 288], [4049, 289], [4049, 290], [4049, 291], [4049, 292], [4049, 293], [4049, 294], [4049, 295], [4049, 296], [4049, 297], [4049, 298], [4049, 299], [4049, 300], [4049, 301], [4049, 302], [4049, 303], [4049, 304], [4049, 305], [4049, 306], [4049, 307], [4049, 308], [4049, 309], [4049, 310], [4049, 311], [4049, 312], [4049, 313], [4049, 314], [4049, 315], [4049, 316], [4049, 318], [4049, 319], [4049, 320], [4049, 321], [4049, 322], [4049, 323], [4049, 324], [4049, 325], [4049, 326], [4049, 327], [4049, 328], [4049, 329], [4049, 330], [4049, 331], [4049, 332], [4049, 333], [4049, 334], [4049, 335], [4049, 336], [4049, 337], [4049, 338], [4049, 339], [4049, 340], [4049, 341], [4049, 342], [4049, 343], [4049, 344], [4049, 345], [4049, 346], [4049, 347], [4049, 348], [4049, 349], [4049, 350], [4049, 351], [4049, 352], [4049, 353], [4049, 354], [4049, 355], [4049, 356], [4049, 357], [4049, 358], [4049, 359], [4049, 360], [4049, 361], [4049, 362], [4049, 363], [4049, 364], [4049, 365], [4049, 366], [4049, 367], [4049, 368], [4049, 369], [4049, 370], [4049, 371], [4049, 373], [4049, 374], [4049, 375], [4049, 376], [4049, 377], [4049, 378], [4049, 379], [4049, 380], [4049, 381], [4049, 382], [4049, 383], [4049, 384], [4049, 385], [4049, 386], [4049, 387], [4049, 388], [4049, 389], [4049, 390], [4049, 391], [4049, 392], [4049, 393], [4049, 394], [4049, 395], [4049, 396], [4049, 397], [4049, 398], [4049, 399], [4049, 400], [4049, 401], [4049, 402], [4049, 403], [4049, 404], [4049, 405], [4049, 406], [4049, 407], [4049, 408], [4049, 409], [4049, 410], [4049, 411], [4049, 412], [4049, 413], [4049, 414], [4049, 415], [4049, 416], [4049, 417], [4049, 418], [4049, 419], [4049, 421], [4049, 422], [4049, 423], [4049, 424], [4049, 425], [4049, 426], [4049, 427], [4049, 428], [4049, 429], [4049, 430], [4049, 431], [4049, 432], [4049, 433], [4049, 434], [4049, 435], [4049, 436], [4049, 437], [4049, 438], [4049, 439], [4049, 440], [4049, 441], [4049, 442], [4049, 443], [4049, 444], [4049, 445], [4049, 446], [4049, 447], [4049, 448], [4049, 449], [4049, 450], [4049, 451], [4049, 452], [4049, 453], [4049, 454], [4049, 455], [4049, 456], [4049, 457], [4049, 458], [4049, 459], [4049, 460], [4049, 461], [4049, 462], [4049, 463], [4049, 464], [4049, 465], [4049, 466], [4049, 467], [4049, 468], [4049, 469], [4049, 470], [4049, 471], [4049, 472], [4049, 473], [4049, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[4053], [4054], [4055], [4056], [4057], [4058], [4059], [4060], [4061], [4062], [4063], [4064], [4065], [4066], [4067], [4068], [4069], [4070], [4071], [4072], [4073], [4074], [4075], [4076], [4077], [4078], [4079], [4080], [4081], [4082], [4083], [4084], [4085], [4086], [4087], [4088], [4089], [4090], [4091], [4092], [4093], [4094], [4095], [4096], [4097], [4098], [4099], [4100], [4101], [4102], [4103], [4104], [4105], [4106], [4107, 1], [4107, 2], [4107, 3], [4107, 4], [4107, 5], [4107, 6], [4107, 7], [4107, 8], [4107, 9], [4107, 10], [4107, 11], [4107, 12], [4107, 13], [4107, 14], [4107, 15], [4107, 16], [4107, 17], [4107, 18], [4107, 19], [4107, 20], [4107, 21], [4107, 22], [4107, 23], [4107, 24], [4107, 25], [4107, 26], [4107, 27], [4107, 29], [4107, 30], [4107, 31], [4107, 32], [4107, 33], [4107, 34], [4107, 35], [4107, 36], [4107, 37], [4107, 38], [4107, 39], [4107, 40], [4107, 41], [4107, 42], [4107, 43], [4107, 44], [4107, 45], [4107, 46], [4107, 47], [4107, 48], [4107, 49], [4107, 50], [4107, 51], [4107, 52], [4107, 53], [4107, 54], [4107, 55], [4107, 56], [4107, 57], [4107, 58], [4107, 59], [4107, 60], [4107, 61], [4107, 62], [4107, 63], [4107, 64], [4107, 65], [4107, 66], [4107, 67], [4107, 68], [4107, 69], [4107, 70], [4107, 71], [4107, 72], [4107, 73], [4107, 74], [4107, 75], [4107, 76], [4107, 77], [4107, 78], [4107, 79], [4107, 80], [4107, 81], [4107, 82], [4107, 84], [4107, 85], [4107, 86], [4107, 87], [4107, 88], [4107, 89], [4107, 90], [4107, 91], [4107, 92], [4107, 93], [4107, 94], [4107, 95], [4107, 96], [4107, 97], [4107, 98], [4107, 99], [4107, 100], [4107, 101], [4107, 102], [4107, 103], [4107, 104], [4107, 105], [4107, 106], [4107, 107], [4107, 108], [4107, 109], [4107, 110], [4107, 112], [4107, 113], [4107, 114], [4107, 115], [4107, 116], [4107, 117], [4107, 118], [4107, 119], [4107, 120], [4107, 121], [4107, 122], [4107, 123], [4107, 124], [4107, 125], [4107, 126], [4107, 127], [4107, 128], [4107, 129], [4107, 130], [4107, 131], [4107, 132], [4107, 133], [4107, 134], [4107, 135], [4107, 136], [4107, 137], [4107, 138], [4107, 139], [4107, 140], [4107, 141], [4107, 142], [4107, 143], [4107, 144], [4107, 145], [4107, 146], [4107, 147], [4107, 148], [4107, 149], [4107, 150], [4107, 151], [4107, 152], [4107, 153], [4107, 154], [4107, 155], [4107, 156], [4107, 157], [4107, 158], [4107, 159], [4107, 160], [4107, 161], [4107, 162], [4107, 163], [4107, 164], [4107, 165], [4107, 167], [4107, 168], [4107, 169], [4107, 170], [4107, 171], [4107, 172], [4107, 173], [4107, 174], [4107, 175], [4107, 176], [4107, 177], [4107, 178], [4107, 179], [4107, 180], [4107, 181], [4107, 182], [4107, 183], [4107, 184], [4107, 185], [4107, 186], [4107, 187], [4107, 188], [4107, 189], [4107, 190], [4107, 191], [4107, 192], [4107, 193], [4107, 194], [4107, 195], [4107, 196], [4107, 197], [4107, 198], [4107, 199], [4107, 200], [4107, 201], [4107, 202], [4107, 203], [4107, 204], [4107, 205], [4107, 206], [4107, 207], [4107, 208], [4107, 209], [4107, 210], [4107, 211], [4107, 212], [4107, 213], [4107, 215], [4107, 216], [4107, 217], [4107, 218], [4107, 219], [4107, 220], [4107, 221], [4107, 222], [4107, 223], [4107, 224], [4107, 225], [4107, 226], [4107, 227], [4107, 228], [4107, 229], [4107, 230], [4107, 231], [4107, 232], [4107, 233], [4107, 234], [4107, 235], [4107, 236], [4107, 237], [4107, 238], [4107, 239], [4107, 240], [4107, 241], [4107, 242], [4107, 243], [4107, 244], [4107, 245], [4107, 246], [4107, 247], [4107, 248], [4107, 249], [4107, 250], [4107, 251], [4107, 252], [4107, 253], [4107, 254], [4107, 255], [4107, 256], [4107, 257], [4107, 258], [4107, 259], [4107, 260], [4107, 261], [4107, 262], [4107, 263], [4107, 264], [4107, 265], [4107, 266], [4107, 267], [4107, 268], [4107, 270], [4107, 271], [4107, 272], [4107, 273], [4107, 274], [4107, 275], [4107, 276], [4107, 277], [4107, 278], [4107, 279], [4107, 280], [4107, 281], [4107, 282], [4107, 283], [4107, 284], [4107, 285], [4107, 286], [4107, 287], [4107, 288], [4107, 289], [4107, 290], [4107, 291], [4107, 292], [4107, 293], [4107, 294], [4107, 295], [4107, 296], [4107, 297], [4107, 298], [4107, 299], [4107, 300], [4107, 301], [4107, 302], [4107, 303], [4107, 304], [4107, 305], [4107, 306], [4107, 307], [4107, 308], [4107, 309], [4107, 310], [4107, 311], [4107, 312], [4107, 313], [4107, 314], [4107, 315], [4107, 316], [4107, 318], [4107, 319], [4107, 320], [4107, 321], [4107, 322], [4107, 323], [4107, 324], [4107, 325], [4107, 326], [4107, 327], [4107, 328], [4107, 329], [4107, 330], [4107, 331], [4107, 332], [4107, 333], [4107, 334], [4107, 335], [4107, 336], [4107, 337], [4107, 338], [4107, 339], [4107, 340], [4107, 341], [4107, 342], [4107, 343], [4107, 344], [4107, 345], [4107, 346], [4107, 347], [4107, 348], [4107, 349], [4107, 350], [4107, 351], [4107, 352], [4107, 353], [4107, 354], [4107, 355], [4107, 356], [4107, 357], [4107, 358], [4107, 359], [4107, 360], [4107, 361], [4107, 362], [4107, 363], [4107, 364], [4107, 365], [4107, 366], [4107, 367], [4107, 368], [4107, 369], [4107, 370], [4107, 371], [4107, 373], [4107, 374], [4107, 375], [4107, 376], [4107, 377], [4107, 378], [4107, 379], [4107, 380], [4107, 381], [4107, 382], [4107, 383], [4107, 384], [4107, 385], [4107, 386], [4107, 387], [4107, 388], [4107, 389], [4107, 390], [4107, 391], [4107, 392], [4107, 393], [4107, 394], [4107, 395], [4107, 396], [4107, 397], [4107, 398], [4107, 399], [4107, 400], [4107, 401], [4107, 402], [4107, 403], [4107, 404], [4107, 405], [4107, 406], [4107, 407], [4107, 408], [4107, 409], [4107, 410], [4107, 411], [4107, 412], [4107, 413], [4107, 414], [4107, 415], [4107, 416], [4107, 417], [4107, 418], [4107, 419], [4107, 421], [4107, 422], [4107, 423], [4107, 424], [4107, 425], [4107, 426], [4107, 427], [4107, 428], [4107, 429], [4107, 430], [4107, 431], [4107, 432], [4107, 433], [4107, 434], [4107, 435], [4107, 436], [4107, 437], [4107, 438], [4107, 439], [4107, 440], [4107, 441], [4107, 442], [4107, 443], [4107, 444], [4107, 445], [4107, 446], [4107, 447], [4107, 448], [4107, 449], [4107, 450], [4107, 451], [4107, 452], [4107, 453], [4107, 454], [4107, 455], [4107, 456], [4107, 457], [4107, 458], [4107, 459], [4107, 460], [4107, 461], [4107, 462], [4107, 463], [4107, 464], [4107, 465], [4107, 466], [4107, 467], [4107, 468], [4107, 469], [4107, 470], [4107, 471], [4107, 472], [4107, 473], [4107, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=208, paths=[[4109], [4110], [4111], [4112], [4113], [4114], [4115], [4116], [4117], [4118], [4119], [4120], [4121], [4122], [4123], [4124], [4125], [4126], [4127], [4128], [4129], [4130], [4131], [4132], [4133], [4134], [4135], [4136], [4137], [4138], [4139], [4140], [4141], [4142], [4143], [4144], [4145], [4146], [4147], [4148], [4149], [4150], [4151], [4152], [4153], [4154], [4155, 1], [4155, 2], [4155, 3], [4155, 4], [4155, 5], [4155, 6], [4155, 7], [4155, 8], [4155, 9], [4155, 10], [4155, 11], [4155, 12], [4155, 13], [4155, 14], [4155, 15], [4155, 16], [4155, 17], [4155, 18], [4155, 19], [4155, 20], [4155, 21], [4155, 22], [4155, 23], [4155, 24], [4155, 25], [4155, 26], [4155, 27], [4155, 29], [4155, 30], [4155, 31], [4155, 32], [4155, 33], [4155, 34], [4155, 35], [4155, 36], [4155, 37], [4155, 38], [4155, 39], [4155, 40], [4155, 41], [4155, 42], [4155, 43], [4155, 44], [4155, 45], [4155, 46], [4155, 47], [4155, 48], [4155, 49], [4155, 50], [4155, 51], [4155, 52], [4155, 53], [4155, 54], [4155, 55], [4155, 56], [4155, 57], [4155, 58], [4155, 59], [4155, 60], [4155, 61], [4155, 62], [4155, 63], [4155, 64], [4155, 65], [4155, 66], [4155, 67], [4155, 68], [4155, 69], [4155, 70], [4155, 71], [4155, 72], [4155, 73], [4155, 74], [4155, 75], [4155, 76], [4155, 77], [4155, 78], [4155, 79], [4155, 80], [4155, 81], [4155, 82], [4155, 84], [4155, 85], [4155, 86], [4155, 87], [4155, 88], [4155, 89], [4155, 90], [4155, 91], [4155, 92], [4155, 93], [4155, 94], [4155, 95], [4155, 96], [4155, 97], [4155, 98], [4155, 99], [4155, 100], [4155, 101], [4155, 102], [4155, 103], [4155, 104], [4155, 105], [4155, 106], [4155, 107], [4155, 108], [4155, 109], [4155, 110], [4155, 112], [4155, 113], [4155, 114], [4155, 115], [4155, 116], [4155, 117], [4155, 118], [4155, 119], [4155, 120], [4155, 121], [4155, 122], [4155, 123], [4155, 124], [4155, 125], [4155, 126], [4155, 127], [4155, 128], [4155, 129], [4155, 130], [4155, 131], [4155, 132], [4155, 133], [4155, 134], [4155, 135], [4155, 136], [4155, 137], [4155, 138], [4155, 139], [4155, 140], [4155, 141], [4155, 142], [4155, 143], [4155, 144], [4155, 145], [4155, 146], [4155, 147], [4155, 148], [4155, 149], [4155, 150], [4155, 151], [4155, 152], [4155, 153], [4155, 154], [4155, 155], [4155, 156], [4155, 157], [4155, 158], [4155, 159], [4155, 160], [4155, 161], [4155, 162], [4155, 163], [4155, 164], [4155, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=208, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=263, paths=[[4157], [4158], [4159], [4160], [4161], [4162], [4163], [4164], [4165], [4166], [4167], [4168], [4169], [4170], [4171], [4172], [4173], [4174], [4175], [4176], [4177], [4178], [4179], [4180], [4181], [4182], [4183], [4184], [4185], [4186], [4187], [4188], [4189], [4190], [4191], [4192], [4193], [4194], [4195], [4196], [4197], [4198], [4199], [4200], [4201], [4202], [4203], [4204], [4205], [4206], [4207], [4209], [4210], [4211], [4212], [4213], [4214], [4215], [4216], [4217], [4218], [4219], [4220], [4221], [4222], [4223], [4224], [4225], [4226], [4227], [4228], [4229], [4230], [4231], [4232], [4233], [4234], [4236], [4237], [4238], [4239], [4240], [4241], [4242], [4243], [4244], [4245], [4246], [4247], [4248], [4249], [4250], [4251], [4252], [4253], [4254], [4255], [4256], [4257], [4258], [4259], [4260, 1], [4260, 2], [4260, 3], [4260, 4], [4260, 5], [4260, 6], [4260, 7], [4260, 8], [4260, 9], [4260, 10], [4260, 11], [4260, 12], [4260, 13], [4260, 14], [4260, 15], [4260, 16], [4260, 17], [4260, 18], [4260, 19], [4260, 20], [4260, 21], [4260, 22], [4260, 23], [4260, 24], [4260, 25], [4260, 26], [4260, 27], [4260, 29], [4260, 30], [4260, 31], [4260, 32], [4260, 33], [4260, 34], [4260, 35], [4260, 36], [4260, 37], [4260, 38], [4260, 39], [4260, 40], [4260, 41], [4260, 42], [4260, 43], [4260, 44], [4260, 45], [4260, 46], [4260, 47], [4260, 48], [4260, 49], [4260, 50], [4260, 51], [4260, 52], [4260, 53], [4260, 54], [4260, 55], [4260, 56], [4260, 57], [4260, 58], [4260, 59], [4260, 60], [4260, 61], [4260, 62], [4260, 63], [4260, 64], [4260, 65], [4260, 66], [4260, 67], [4260, 68], [4260, 69], [4260, 70], [4260, 71], [4260, 72], [4260, 73], [4260, 74], [4260, 75], [4260, 76], [4260, 77], [4260, 78], [4260, 79], [4260, 80], [4260, 81], [4260, 82], [4260, 84], [4260, 85], [4260, 86], [4260, 87], [4260, 88], [4260, 89], [4260, 90], [4260, 91], [4260, 92], [4260, 93], [4260, 94], [4260, 95], [4260, 96], [4260, 97], [4260, 98], [4260, 99], [4260, 100], [4260, 101], [4260, 102], [4260, 103], [4260, 104], [4260, 105], [4260, 106], [4260, 107], [4260, 108], [4260, 109], [4260, 110], [4260, 112], [4260, 113], [4260, 114], [4260, 115], [4260, 116], [4260, 117], [4260, 118], [4260, 119], [4260, 120], [4260, 121], [4260, 122], [4260, 123], [4260, 124], [4260, 125], [4260, 126], [4260, 127], [4260, 128], [4260, 129], [4260, 130], [4260, 131], [4260, 132], [4260, 133], [4260, 134], [4260, 135], [4260, 136], [4260, 137], [4260, 138], [4260, 139], [4260, 140], [4260, 141], [4260, 142], [4260, 143], [4260, 144], [4260, 145], [4260, 146], [4260, 147], [4260, 148], [4260, 149], [4260, 150], [4260, 151], [4260, 152], [4260, 153], [4260, 154], [4260, 155], [4260, 156], [4260, 157], [4260, 158], [4260, 159], [4260, 160], [4260, 161], [4260, 162], [4260, 163], [4260, 164], [4260, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[[4235]]), z_errors=NoisyOperationsCount(count=1, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=264, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=519, paths=[[4264], [4265], [4266], [4267], [4268], [4269], [4270], [4271], [4272], [4273], [4274], [4275], [4276], [4277], [4278], [4279], [4280], [4281], [4282], [4283], [4284], [4285], [4286], [4287], [4288], [4289], [4290], [4291], [4292], [4293], [4294], [4295], [4296], [4297], [4298], [4299], [4300], [4301], [4302], [4303], [4304], [4305], [4306], [4307], [4308], [4309], [4310], [4311], [4312], [4313], [4314], [4315], [4316], [4317], [4318, 1], [4318, 2], [4318, 3], [4318, 4], [4318, 5], [4318, 6], [4318, 7], [4318, 8], [4318, 9], [4318, 10], [4318, 11], [4318, 12], [4318, 13], [4318, 14], [4318, 15], [4318, 16], [4318, 17], [4318, 18], [4318, 19], [4318, 20], [4318, 21], [4318, 22], [4318, 23], [4318, 24], [4318, 25], [4318, 26], [4318, 27], [4318, 29], [4318, 30], [4318, 31], [4318, 32], [4318, 33], [4318, 34], [4318, 35], [4318, 36], [4318, 37], [4318, 38], [4318, 39], [4318, 40], [4318, 41], [4318, 42], [4318, 43], [4318, 44], [4318, 45], [4318, 46], [4318, 47], [4318, 48], [4318, 49], [4318, 50], [4318, 51], [4318, 52], [4318, 53], [4318, 54], [4318, 55], [4318, 56], [4318, 57], [4318, 58], [4318, 59], [4318, 60], [4318, 61], [4318, 62], [4318, 63], [4318, 64], [4318, 65], [4318, 66], [4318, 67], [4318, 68], [4318, 69], [4318, 70], [4318, 71], [4318, 72], [4318, 73], [4318, 74], [4318, 75], [4318, 76], [4318, 77], [4318, 78], [4318, 79], [4318, 80], [4318, 81], [4318, 82], [4318, 84], [4318, 85], [4318, 86], [4318, 87], [4318, 88], [4318, 89], [4318, 90], [4318, 91], [4318, 92], [4318, 93], [4318, 94], [4318, 95], [4318, 96], [4318, 97], [4318, 98], [4318, 99], [4318, 100], [4318, 101], [4318, 102], [4318, 103], [4318, 104], [4318, 105], [4318, 106], [4318, 107], [4318, 108], [4318, 109], [4318, 110], [4318, 112], [4318, 113], [4318, 114], [4318, 115], [4318, 116], [4318, 117], [4318, 118], [4318, 119], [4318, 120], [4318, 121], [4318, 122], [4318, 123], [4318, 124], [4318, 125], [4318, 126], [4318, 127], [4318, 128], [4318, 129], [4318, 130], [4318, 131], [4318, 132], [4318, 133], [4318, 134], [4318, 135], [4318, 136], [4318, 137], [4318, 138], [4318, 139], [4318, 140], [4318, 141], [4318, 142], [4318, 143], [4318, 144], [4318, 145], [4318, 146], [4318, 147], [4318, 148], [4318, 149], [4318, 150], [4318, 151], [4318, 152], [4318, 153], [4318, 154], [4318, 155], [4318, 156], [4318, 157], [4318, 158], [4318, 159], [4318, 160], [4318, 161], [4318, 162], [4318, 163], [4318, 164], [4318, 165], [4318, 167], [4318, 168], [4318, 169], [4318, 170], [4318, 171], [4318, 172], [4318, 173], [4318, 174], [4318, 175], [4318, 176], [4318, 177], [4318, 178], [4318, 179], [4318, 180], [4318, 181], [4318, 182], [4318, 183], [4318, 184], [4318, 185], [4318, 186], [4318, 187], [4318, 188], [4318, 189], [4318, 190], [4318, 191], [4318, 192], [4318, 193], [4318, 194], [4318, 195], [4318, 196], [4318, 197], [4318, 198], [4318, 199], [4318, 200], [4318, 201], [4318, 202], [4318, 203], [4318, 204], [4318, 205], [4318, 206], [4318, 207], [4318, 208], [4318, 209], [4318, 210], [4318, 211], [4318, 212], [4318, 213], [4318, 215], [4318, 216], [4318, 217], [4318, 218], [4318, 219], [4318, 220], [4318, 221], [4318, 222], [4318, 223], [4318, 224], [4318, 225], [4318, 226], [4318, 227], [4318, 228], [4318, 229], [4318, 230], [4318, 231], [4318, 232], [4318, 233], [4318, 234], [4318, 235], [4318, 236], [4318, 237], [4318, 238], [4318, 239], [4318, 240], [4318, 241], [4318, 242], [4318, 243], [4318, 244], [4318, 245], [4318, 246], [4318, 247], [4318, 248], [4318, 249], [4318, 250], [4318, 251], [4318, 252], [4318, 253], [4318, 254], [4318, 255], [4318, 256], [4318, 257], [4318, 258], [4318, 259], [4318, 260], [4318, 261], [4318, 262], [4318, 263], [4318, 264], [4318, 265], [4318, 266], [4318, 267], [4318, 268], [4318, 270], [4318, 271], [4318, 272], [4318, 273], [4318, 274], [4318, 275], [4318, 276], [4318, 277], [4318, 278], [4318, 279], [4318, 280], [4318, 281], [4318, 282], [4318, 283], [4318, 284], [4318, 285], [4318, 286], [4318, 287], [4318, 288], [4318, 289], [4318, 290], [4318, 291], [4318, 292], [4318, 293], [4318, 294], [4318, 295], [4318, 296], [4318, 297], [4318, 298], [4318, 299], [4318, 300], [4318, 301], [4318, 302], [4318, 303], [4318, 304], [4318, 305], [4318, 306], [4318, 307], [4318, 308], [4318, 309], [4318, 310], [4318, 311], [4318, 312], [4318, 313], [4318, 314], [4318, 315], [4318, 316], [4318, 318], [4318, 319], [4318, 320], [4318, 321], [4318, 322], [4318, 323], [4318, 324], [4318, 325], [4318, 326], [4318, 327], [4318, 328], [4318, 329], [4318, 330], [4318, 331], [4318, 332], [4318, 333], [4318, 334], [4318, 335], [4318, 336], [4318, 337], [4318, 338], [4318, 339], [4318, 340], [4318, 341], [4318, 342], [4318, 343], [4318, 344], [4318, 345], [4318, 346], [4318, 347], [4318, 348], [4318, 349], [4318, 350], [4318, 351], [4318, 352], [4318, 353], [4318, 354], [4318, 355], [4318, 356], [4318, 357], [4318, 358], [4318, 359], [4318, 360], [4318, 361], [4318, 362], [4318, 363], [4318, 364], [4318, 365], [4318, 366], [4318, 367], [4318, 368], [4318, 369], [4318, 370], [4318, 371], [4318, 373], [4318, 374], [4318, 375], [4318, 376], [4318, 377], [4318, 378], [4318, 379], [4318, 380], [4318, 381], [4318, 382], [4318, 383], [4318, 384], [4318, 385], [4318, 386], [4318, 387], [4318, 388], [4318, 389], [4318, 390], [4318, 391], [4318, 392], [4318, 393], [4318, 394], [4318, 395], [4318, 396], [4318, 397], [4318, 398], [4318, 399], [4318, 400], [4318, 401], [4318, 402], [4318, 403], [4318, 404], [4318, 405], [4318, 406], [4318, 407], [4318, 408], [4318, 409], [4318, 410], [4318, 411], [4318, 412], [4318, 413], [4318, 414], [4318, 415], [4318, 416], [4318, 417], [4318, 418], [4318, 419], [4318, 421], [4318, 422], [4318, 423], [4318, 424], [4318, 425], [4318, 426], [4318, 427], [4318, 428], [4318, 429], [4318, 430], [4318, 431], [4318, 432], [4318, 433], [4318, 434], [4318, 435], [4318, 436], [4318, 437], [4318, 438], [4318, 439], [4318, 440], [4318, 441], [4318, 442], [4318, 443], [4318, 444], [4318, 445], [4318, 446], [4318, 447], [4318, 448], [4318, 449], [4318, 450], [4318, 451], [4318, 452], [4318, 453], [4318, 454], [4318, 455], [4318, 456], [4318, 457], [4318, 458], [4318, 459], [4318, 460], [4318, 461], [4318, 462], [4318, 463], [4318, 464], [4318, 465], [4318, 466], [4318, 467], [4318, 468], [4318, 469], [4318, 470], [4318, 471], [4318, 472], [4318, 473], [4318, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=513, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=591, paths=[[4320], [4321], [4322], [4323], [4324], [4325], [4326], [4327], [4328], [4329], [4330], [4331], [4332], [4333], [4334], [4335], [4336], [4337], [4339], [4340], [4341], [4342], [4343], [4344], [4345], [4346], [4347], [4348], [4349], [4350], [4351], [4352], [4353], [4354], [4355], [4356], [4357], [4358], [4359], [4360], [4361], [4362], [4363], [4364], [4365], [4366], [4367], [4368], [4369], [4370], [4371], [4372], [4373], [4374], [4375], [4376], [4377], [4378], [4379], [4380], [4381], [4382], [4383], [4384], [4385], [4386], [4387], [4388], [4389], [4390], [4391], [4392], [4396], [4397], [4398], [4399], [4400], [4401], [4402], [4403], [4404], [4405], [4406], [4407], [4408], [4409], [4410], [4411], [4412], [4413], [4414], [4415], [4416], [4417], [4418], [4419], [4420], [4421], [4422], [4423], [4424], [4425], [4426], [4427], [4428], [4429], [4430], [4431], [4432], [4433], [4434], [4435], [4436], [4437], [4438], [4439], [4440], [4441], [4442], [4443], [4444], [4445], [4446], [4447], [4448], [4449], [4450, 1], [4450, 2], [4450, 3], [4450, 4], [4450, 5], [4450, 6], [4450, 7], [4450, 8], [4450, 9], [4450, 10], [4450, 11], [4450, 12], [4450, 13], [4450, 14], [4450, 15], [4450, 16], [4450, 17], [4450, 18], [4450, 19], [4450, 20], [4450, 21], [4450, 22], [4450, 23], [4450, 24], [4450, 25], [4450, 26], [4450, 27], [4450, 29], [4450, 30], [4450, 31], [4450, 32], [4450, 33], [4450, 34], [4450, 35], [4450, 36], [4450, 37], [4450, 38], [4450, 39], [4450, 40], [4450, 41], [4450, 42], [4450, 43], [4450, 44], [4450, 45], [4450, 46], [4450, 47], [4450, 48], [4450, 49], [4450, 50], [4450, 51], [4450, 52], [4450, 53], [4450, 54], [4450, 55], [4450, 56], [4450, 57], [4450, 58], [4450, 59], [4450, 60], [4450, 61], [4450, 62], [4450, 63], [4450, 64], [4450, 65], [4450, 66], [4450, 67], [4450, 68], [4450, 69], [4450, 70], [4450, 71], [4450, 72], [4450, 73], [4450, 74], [4450, 75], [4450, 76], [4450, 77], [4450, 78], [4450, 79], [4450, 80], [4450, 81], [4450, 82], [4450, 84], [4450, 85], [4450, 86], [4450, 87], [4450, 88], [4450, 89], [4450, 90], [4450, 91], [4450, 92], [4450, 93], [4450, 94], [4450, 95], [4450, 96], [4450, 97], [4450, 98], [4450, 99], [4450, 100], [4450, 101], [4450, 102], [4450, 103], [4450, 104], [4450, 105], [4450, 106], [4450, 107], [4450, 108], [4450, 109], [4450, 110], [4450, 112], [4450, 113], [4450, 114], [4450, 115], [4450, 116], [4450, 117], [4450, 118], [4450, 119], [4450, 120], [4450, 121], [4450, 122], [4450, 123], [4450, 124], [4450, 125], [4450, 126], [4450, 127], [4450, 128], [4450, 129], [4450, 130], [4450, 131], [4450, 132], [4450, 133], [4450, 134], [4450, 135], [4450, 136], [4450, 137], [4450, 138], [4450, 139], [4450, 140], [4450, 141], [4450, 142], [4450, 143], [4450, 144], [4450, 145], [4450, 146], [4450, 147], [4450, 148], [4450, 149], [4450, 150], [4450, 151], [4450, 152], [4450, 153], [4450, 154], [4450, 155], [4450, 156], [4450, 157], [4450, 158], [4450, 159], [4450, 160], [4450, 161], [4450, 162], [4450, 163], [4450, 164], [4450, 165], [4450, 167], [4450, 168], [4450, 169], [4450, 170], [4450, 171], [4450, 172], [4450, 173], [4450, 174], [4450, 175], [4450, 176], [4450, 177], [4450, 178], [4450, 179], [4450, 180], [4450, 181], [4450, 182], [4450, 183], [4450, 184], [4450, 185], [4450, 186], [4450, 187], [4450, 188], [4450, 189], [4450, 190], [4450, 191], [4450, 192], [4450, 193], [4450, 194], [4450, 195], [4450, 196], [4450, 197], [4450, 198], [4450, 199], [4450, 200], [4450, 201], [4450, 202], [4450, 203], [4450, 204], [4450, 205], [4450, 206], [4450, 207], [4450, 208], [4450, 209], [4450, 210], [4450, 211], [4450, 212], [4450, 213], [4450, 215], [4450, 216], [4450, 217], [4450, 218], [4450, 219], [4450, 220], [4450, 221], [4450, 222], [4450, 223], [4450, 224], [4450, 225], [4450, 226], [4450, 227], [4450, 228], [4450, 229], [4450, 230], [4450, 231], [4450, 232], [4450, 233], [4450, 234], [4450, 235], [4450, 236], [4450, 237], [4450, 238], [4450, 239], [4450, 240], [4450, 241], [4450, 242], [4450, 243], [4450, 244], [4450, 245], [4450, 246], [4450, 247], [4450, 248], [4450, 249], [4450, 250], [4450, 251], [4450, 252], [4450, 253], [4450, 254], [4450, 255], [4450, 256], [4450, 257], [4450, 258], [4450, 259], [4450, 260], [4450, 261], [4450, 262], [4450, 263], [4450, 264], [4450, 265], [4450, 266], [4450, 267], [4450, 268], [4450, 270], [4450, 271], [4450, 272], [4450, 273], [4450, 274], [4450, 275], [4450, 276], [4450, 277], [4450, 278], [4450, 279], [4450, 280], [4450, 281], [4450, 282], [4450, 283], [4450, 284], [4450, 285], [4450, 286], [4450, 287], [4450, 288], [4450, 289], [4450, 290], [4450, 291], [4450, 292], [4450, 293], [4450, 294], [4450, 295], [4450, 296], [4450, 297], [4450, 298], [4450, 299], [4450, 300], [4450, 301], [4450, 302], [4450, 303], [4450, 304], [4450, 305], [4450, 306], [4450, 307], [4450, 308], [4450, 309], [4450, 310], [4450, 311], [4450, 312], [4450, 313], [4450, 314], [4450, 315], [4450, 316], [4450, 318], [4450, 319], [4450, 320], [4450, 321], [4450, 322], [4450, 323], [4450, 324], [4450, 325], [4450, 326], [4450, 327], [4450, 328], [4450, 329], [4450, 330], [4450, 331], [4450, 332], [4450, 333], [4450, 334], [4450, 335], [4450, 336], [4450, 337], [4450, 338], [4450, 339], [4450, 340], [4450, 341], [4450, 342], [4450, 343], [4450, 344], [4450, 345], [4450, 346], [4450, 347], [4450, 348], [4450, 349], [4450, 350], [4450, 351], [4450, 352], [4450, 353], [4450, 354], [4450, 355], [4450, 356], [4450, 357], [4450, 358], [4450, 359], [4450, 360], [4450, 361], [4450, 362], [4450, 363], [4450, 364], [4450, 365], [4450, 366], [4450, 367], [4450, 368], [4450, 369], [4450, 370], [4450, 371], [4450, 373], [4450, 374], [4450, 375], [4450, 376], [4450, 377], [4450, 378], [4450, 379], [4450, 380], [4450, 381], [4450, 382], [4450, 383], [4450, 384], [4450, 385], [4450, 386], [4450, 387], [4450, 388], [4450, 389], [4450, 390], [4450, 391], [4450, 392], [4450, 393], [4450, 394], [4450, 395], [4450, 396], [4450, 397], [4450, 398], [4450, 399], [4450, 400], [4450, 401], [4450, 402], [4450, 403], [4450, 404], [4450, 405], [4450, 406], [4450, 407], [4450, 408], [4450, 409], [4450, 410], [4450, 411], [4450, 412], [4450, 413], [4450, 414], [4450, 415], [4450, 416], [4450, 417], [4450, 418], [4450, 419], [4450, 421], [4450, 422], [4450, 423], [4450, 424], [4450, 425], [4450, 426], [4450, 427], [4450, 428], [4450, 429], [4450, 430], [4450, 431], [4450, 432], [4450, 433], [4450, 434], [4450, 435], [4450, 436], [4450, 437], [4450, 438], [4450, 439], [4450, 440], [4450, 441], [4450, 442], [4450, 443], [4450, 444], [4450, 445], [4450, 446], [4450, 447], [4450, 448], [4450, 449], [4450, 450], [4450, 451], [4450, 452], [4450, 453], [4450, 454], [4450, 455], [4450, 456], [4450, 457], [4450, 458], [4450, 459], [4450, 460], [4450, 461], [4450, 462], [4450, 463], [4450, 464], [4450, 465], [4450, 466], [4450, 467], [4450, 468], [4450, 469], [4450, 470], [4450, 471], [4450, 472], [4450, 473], [4450, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=585, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=591, paths=[[4452], [4453], [4454], [4455], [4456], [4457], [4458], [4459], [4460], [4461], [4462], [4463], [4464], [4465], [4466], [4467], [4468], [4469], [4471], [4472], [4473], [4474], [4475], [4476], [4477], [4478], [4479], [4480], [4481], [4482], [4483], [4484], [4485], [4486], [4487], [4488], [4489], [4490], [4491], [4492], [4493], [4494], [4495], [4496], [4497], [4498], [4499], [4500], [4501], [4502], [4503], [4504], [4505], [4506], [4507], [4508], [4509], [4510], [4511], [4512], [4513], [4514], [4515], [4516], [4517], [4518], [4519], [4520], [4521], [4522], [4523], [4524], [4528], [4529], [4530], [4531], [4532], [4533], [4534], [4535], [4536], [4537], [4538], [4539], [4540], [4541], [4542], [4543], [4544], [4545], [4546], [4547], [4548], [4549], [4550], [4551], [4552], [4553], [4554], [4555], [4556], [4557], [4558], [4559], [4560], [4561], [4562], [4563], [4564], [4565], [4566], [4567], [4568], [4569], [4570], [4571], [4572], [4573], [4574], [4575], [4576], [4577], [4578], [4579], [4580], [4581], [4582, 1], [4582, 2], [4582, 3], [4582, 4], [4582, 5], [4582, 6], [4582, 7], [4582, 8], [4582, 9], [4582, 10], [4582, 11], [4582, 12], [4582, 13], [4582, 14], [4582, 15], [4582, 16], [4582, 17], [4582, 18], [4582, 19], [4582, 20], [4582, 21], [4582, 22], [4582, 23], [4582, 24], [4582, 25], [4582, 26], [4582, 27], [4582, 29], [4582, 30], [4582, 31], [4582, 32], [4582, 33], [4582, 34], [4582, 35], [4582, 36], [4582, 37], [4582, 38], [4582, 39], [4582, 40], [4582, 41], [4582, 42], [4582, 43], [4582, 44], [4582, 45], [4582, 46], [4582, 47], [4582, 48], [4582, 49], [4582, 50], [4582, 51], [4582, 52], [4582, 53], [4582, 54], [4582, 55], [4582, 56], [4582, 57], [4582, 58], [4582, 59], [4582, 60], [4582, 61], [4582, 62], [4582, 63], [4582, 64], [4582, 65], [4582, 66], [4582, 67], [4582, 68], [4582, 69], [4582, 70], [4582, 71], [4582, 72], [4582, 73], [4582, 74], [4582, 75], [4582, 76], [4582, 77], [4582, 78], [4582, 79], [4582, 80], [4582, 81], [4582, 82], [4582, 84], [4582, 85], [4582, 86], [4582, 87], [4582, 88], [4582, 89], [4582, 90], [4582, 91], [4582, 92], [4582, 93], [4582, 94], [4582, 95], [4582, 96], [4582, 97], [4582, 98], [4582, 99], [4582, 100], [4582, 101], [4582, 102], [4582, 103], [4582, 104], [4582, 105], [4582, 106], [4582, 107], [4582, 108], [4582, 109], [4582, 110], [4582, 112], [4582, 113], [4582, 114], [4582, 115], [4582, 116], [4582, 117], [4582, 118], [4582, 119], [4582, 120], [4582, 121], [4582, 122], [4582, 123], [4582, 124], [4582, 125], [4582, 126], [4582, 127], [4582, 128], [4582, 129], [4582, 130], [4582, 131], [4582, 132], [4582, 133], [4582, 134], [4582, 135], [4582, 136], [4582, 137], [4582, 138], [4582, 139], [4582, 140], [4582, 141], [4582, 142], [4582, 143], [4582, 144], [4582, 145], [4582, 146], [4582, 147], [4582, 148], [4582, 149], [4582, 150], [4582, 151], [4582, 152], [4582, 153], [4582, 154], [4582, 155], [4582, 156], [4582, 157], [4582, 158], [4582, 159], [4582, 160], [4582, 161], [4582, 162], [4582, 163], [4582, 164], [4582, 165], [4582, 167], [4582, 168], [4582, 169], [4582, 170], [4582, 171], [4582, 172], [4582, 173], [4582, 174], [4582, 175], [4582, 176], [4582, 177], [4582, 178], [4582, 179], [4582, 180], [4582, 181], [4582, 182], [4582, 183], [4582, 184], [4582, 185], [4582, 186], [4582, 187], [4582, 188], [4582, 189], [4582, 190], [4582, 191], [4582, 192], [4582, 193], [4582, 194], [4582, 195], [4582, 196], [4582, 197], [4582, 198], [4582, 199], [4582, 200], [4582, 201], [4582, 202], [4582, 203], [4582, 204], [4582, 205], [4582, 206], [4582, 207], [4582, 208], [4582, 209], [4582, 210], [4582, 211], [4582, 212], [4582, 213], [4582, 215], [4582, 216], [4582, 217], [4582, 218], [4582, 219], [4582, 220], [4582, 221], [4582, 222], [4582, 223], [4582, 224], [4582, 225], [4582, 226], [4582, 227], [4582, 228], [4582, 229], [4582, 230], [4582, 231], [4582, 232], [4582, 233], [4582, 234], [4582, 235], [4582, 236], [4582, 237], [4582, 238], [4582, 239], [4582, 240], [4582, 241], [4582, 242], [4582, 243], [4582, 244], [4582, 245], [4582, 246], [4582, 247], [4582, 248], [4582, 249], [4582, 250], [4582, 251], [4582, 252], [4582, 253], [4582, 254], [4582, 255], [4582, 256], [4582, 257], [4582, 258], [4582, 259], [4582, 260], [4582, 261], [4582, 262], [4582, 263], [4582, 264], [4582, 265], [4582, 266], [4582, 267], [4582, 268], [4582, 270], [4582, 271], [4582, 272], [4582, 273], [4582, 274], [4582, 275], [4582, 276], [4582, 277], [4582, 278], [4582, 279], [4582, 280], [4582, 281], [4582, 282], [4582, 283], [4582, 284], [4582, 285], [4582, 286], [4582, 287], [4582, 288], [4582, 289], [4582, 290], [4582, 291], [4582, 292], [4582, 293], [4582, 294], [4582, 295], [4582, 296], [4582, 297], [4582, 298], [4582, 299], [4582, 300], [4582, 301], [4582, 302], [4582, 303], [4582, 304], [4582, 305], [4582, 306], [4582, 307], [4582, 308], [4582, 309], [4582, 310], [4582, 311], [4582, 312], [4582, 313], [4582, 314], [4582, 315], [4582, 316], [4582, 318], [4582, 319], [4582, 320], [4582, 321], [4582, 322], [4582, 323], [4582, 324], [4582, 325], [4582, 326], [4582, 327], [4582, 328], [4582, 329], [4582, 330], [4582, 331], [4582, 332], [4582, 333], [4582, 334], [4582, 335], [4582, 336], [4582, 337], [4582, 338], [4582, 339], [4582, 340], [4582, 341], [4582, 342], [4582, 343], [4582, 344], [4582, 345], [4582, 346], [4582, 347], [4582, 348], [4582, 349], [4582, 350], [4582, 351], [4582, 352], [4582, 353], [4582, 354], [4582, 355], [4582, 356], [4582, 357], [4582, 358], [4582, 359], [4582, 360], [4582, 361], [4582, 362], [4582, 363], [4582, 364], [4582, 365], [4582, 366], [4582, 367], [4582, 368], [4582, 369], [4582, 370], [4582, 371], [4582, 373], [4582, 374], [4582, 375], [4582, 376], [4582, 377], [4582, 378], [4582, 379], [4582, 380], [4582, 381], [4582, 382], [4582, 383], [4582, 384], [4582, 385], [4582, 386], [4582, 387], [4582, 388], [4582, 389], [4582, 390], [4582, 391], [4582, 392], [4582, 393], [4582, 394], [4582, 395], [4582, 396], [4582, 397], [4582, 398], [4582, 399], [4582, 400], [4582, 401], [4582, 402], [4582, 403], [4582, 404], [4582, 405], [4582, 406], [4582, 407], [4582, 408], [4582, 409], [4582, 410], [4582, 411], [4582, 412], [4582, 413], [4582, 414], [4582, 415], [4582, 416], [4582, 417], [4582, 418], [4582, 419], [4582, 421], [4582, 422], [4582, 423], [4582, 424], [4582, 425], [4582, 426], [4582, 427], [4582, 428], [4582, 429], [4582, 430], [4582, 431], [4582, 432], [4582, 433], [4582, 434], [4582, 435], [4582, 436], [4582, 437], [4582, 438], [4582, 439], [4582, 440], [4582, 441], [4582, 442], [4582, 443], [4582, 444], [4582, 445], [4582, 446], [4582, 447], [4582, 448], [4582, 449], [4582, 450], [4582, 451], [4582, 452], [4582, 453], [4582, 454], [4582, 455], [4582, 456], [4582, 457], [4582, 458], [4582, 459], [4582, 460], [4582, 461], [4582, 462], [4582, 463], [4582, 464], [4582, 465], [4582, 466], [4582, 467], [4582, 468], [4582, 469], [4582, 470], [4582, 471], [4582, 472], [4582, 473], [4582, 474]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=585, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=289, paths=[[4584], [4585], [4586], [4587], [4588], [4589], [4590], [4591], [4592], [4593], [4594], [4595], [4596], [4597], [4598], [4599], [4600], [4601], [4602], [4603], [4604], [4605], [4606], [4607], [4608], [4609], [4610], [4612], [4613], [4614], [4615], [4616], [4617], [4618], [4619], [4620], [4621], [4622], [4623], [4624], [4625], [4626], [4627], [4628], [4629], [4630], [4631], [4632], [4633], [4634], [4635], [4636], [4637], [4638], [4639], [4640], [4641], [4642], [4643], [4644], [4645], [4646], [4647], [4648], [4649], [4650], [4651], [4652], [4653], [4654], [4655], [4656], [4657], [4658], [4659], [4660], [4661], [4662], [4663], [4664], [4665], [4667], [4668], [4669], [4670], [4671], [4672], [4673], [4674], [4675], [4676], [4677], [4678], [4679], [4680], [4681], [4682], [4683], [4684], [4685], [4686], [4687], [4688], [4689], [4690], [4691], [4692], [4693], [4694], [4695], [4696], [4697], [4698], [4699], [4700], [4701], [4702], [4703], [4704], [4705], [4706], [4707], [4708], [4709], [4710], [4711], [4712], [4713, 1], [4713, 2], [4713, 3], [4713, 4], [4713, 5], [4713, 6], [4713, 7], [4713, 8], [4713, 9], [4713, 10], [4713, 11], [4713, 12], [4713, 13], [4713, 14], [4713, 15], [4713, 16], [4713, 17], [4713, 18], [4713, 19], [4713, 20], [4713, 21], [4713, 22], [4713, 23], [4713, 24], [4713, 25], [4713, 26], [4713, 27], [4713, 29], [4713, 30], [4713, 31], [4713, 32], [4713, 33], [4713, 34], [4713, 35], [4713, 36], [4713, 37], [4713, 38], [4713, 39], [4713, 40], [4713, 41], [4713, 42], [4713, 43], [4713, 44], [4713, 45], [4713, 46], [4713, 47], [4713, 48], [4713, 49], [4713, 50], [4713, 51], [4713, 52], [4713, 53], [4713, 54], [4713, 55], [4713, 56], [4713, 57], [4713, 58], [4713, 59], [4713, 60], [4713, 61], [4713, 62], [4713, 63], [4713, 64], [4713, 65], [4713, 66], [4713, 67], [4713, 68], [4713, 69], [4713, 70], [4713, 71], [4713, 72], [4713, 73], [4713, 74], [4713, 75], [4713, 76], [4713, 77], [4713, 78], [4713, 79], [4713, 80], [4713, 81], [4713, 82], [4713, 84], [4713, 85], [4713, 86], [4713, 87], [4713, 88], [4713, 89], [4713, 90], [4713, 91], [4713, 92], [4713, 93], [4713, 94], [4713, 95], [4713, 96], [4713, 97], [4713, 98], [4713, 99], [4713, 100], [4713, 101], [4713, 102], [4713, 103], [4713, 104], [4713, 105], [4713, 106], [4713, 107], [4713, 108], [4713, 109], [4713, 110], [4713, 112], [4713, 113], [4713, 114], [4713, 115], [4713, 116], [4713, 117], [4713, 118], [4713, 119], [4713, 120], [4713, 121], [4713, 122], [4713, 123], [4713, 124], [4713, 125], [4713, 126], [4713, 127], [4713, 128], [4713, 129], [4713, 130], [4713, 131], [4713, 132], [4713, 133], [4713, 134], [4713, 135], [4713, 136], [4713, 137], [4713, 138], [4713, 139], [4713, 140], [4713, 141], [4713, 142], [4713, 143], [4713, 144], [4713, 145], [4713, 146], [4713, 147], [4713, 148], [4713, 149], [4713, 150], [4713, 151], [4713, 152], [4713, 153], [4713, 154], [4713, 155], [4713, 156], [4713, 157], [4713, 158], [4713, 159], [4713, 160], [4713, 161], [4713, 162], [4713, 163], [4713, 164], [4713, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=289, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=213, paths=[[4715], [4716], [4717], [4718], [4719], [4720], [4721], [4722], [4723], [4724], [4725], [4726], [4727], [4728], [4729], [4730], [4731], [4732], [4733], [4734], [4735], [4736], [4737], [4738], [4739], [4740], [4741], [4742], [4743], [4744], [4745], [4746], [4747], [4748], [4749], [4750], [4751], [4752], [4753], [4754], [4755], [4756], [4757], [4758], [4759], [4760], [4761], [4762], [4763], [4764], [4765], [4766, 1], [4766, 2], [4766, 3], [4766, 4], [4766, 5], [4766, 6], [4766, 7], [4766, 8], [4766, 9], [4766, 10], [4766, 11], [4766, 12], [4766, 13], [4766, 14], [4766, 15], [4766, 16], [4766, 17], [4766, 18], [4766, 19], [4766, 20], [4766, 21], [4766, 22], [4766, 23], [4766, 24], [4766, 25], [4766, 26], [4766, 27], [4766, 29], [4766, 30], [4766, 31], [4766, 32], [4766, 33], [4766, 34], [4766, 35], [4766, 36], [4766, 37], [4766, 38], [4766, 39], [4766, 40], [4766, 41], [4766, 42], [4766, 43], [4766, 44], [4766, 45], [4766, 46], [4766, 47], [4766, 48], [4766, 49], [4766, 50], [4766, 51], [4766, 52], [4766, 53], [4766, 54], [4766, 55], [4766, 56], [4766, 57], [4766, 58], [4766, 59], [4766, 60], [4766, 61], [4766, 62], [4766, 63], [4766, 64], [4766, 65], [4766, 66], [4766, 67], [4766, 68], [4766, 69], [4766, 70], [4766, 71], [4766, 72], [4766, 73], [4766, 74], [4766, 75], [4766, 76], [4766, 77], [4766, 78], [4766, 79], [4766, 80], [4766, 81], [4766, 82], [4766, 84], [4766, 85], [4766, 86], [4766, 87], [4766, 88], [4766, 89], [4766, 90], [4766, 91], [4766, 92], [4766, 93], [4766, 94], [4766, 95], [4766, 96], [4766, 97], [4766, 98], [4766, 99], [4766, 100], [4766, 101], [4766, 102], [4766, 103], [4766, 104], [4766, 105], [4766, 106], [4766, 107], [4766, 108], [4766, 109], [4766, 110], [4766, 112], [4766, 113], [4766, 114], [4766, 115], [4766, 116], [4766, 117], [4766, 118], [4766, 119], [4766, 120], [4766, 121], [4766, 122], [4766, 123], [4766, 124], [4766, 125], [4766, 126], [4766, 127], [4766, 128], [4766, 129], [4766, 130], [4766, 131], [4766, 132], [4766, 133], [4766, 134], [4766, 135], [4766, 136], [4766, 137], [4766, 138], [4766, 139], [4766, 140], [4766, 141], [4766, 142], [4766, 143], [4766, 144], [4766, 145], [4766, 146], [4766, 147], [4766, 148], [4766, 149], [4766, 150], [4766, 151], [4766, 152], [4766, 153], [4766, 154], [4766, 155], [4766, 156], [4766, 157], [4766, 158], [4766, 159], [4766, 160], [4766, 161], [4766, 162], [4766, 163], [4766, 164], [4766, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=213, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=162, paths=[[4767, 1], [4767, 2], [4767, 3], [4767, 4], [4767, 5], [4767, 6], [4767, 7], [4767, 8], [4767, 9], [4767, 10], [4767, 11], [4767, 12], [4767, 13], [4767, 14], [4767, 15], [4767, 16], [4767, 17], [4767, 18], [4767, 19], [4767, 20], [4767, 21], [4767, 22], [4767, 23], [4767, 24], [4767, 25], [4767, 26], [4767, 27], [4767, 29], [4767, 30], [4767, 31], [4767, 32], [4767, 33], [4767, 34], [4767, 35], [4767, 36], [4767, 37], [4767, 38], [4767, 39], [4767, 40], [4767, 41], [4767, 42], [4767, 43], [4767, 44], [4767, 45], [4767, 46], [4767, 47], [4767, 48], [4767, 49], [4767, 50], [4767, 51], [4767, 52], [4767, 53], [4767, 54], [4767, 55], [4767, 56], [4767, 57], [4767, 58], [4767, 59], [4767, 60], [4767, 61], [4767, 62], [4767, 63], [4767, 64], [4767, 65], [4767, 66], [4767, 67], [4767, 68], [4767, 69], [4767, 70], [4767, 71], [4767, 72], [4767, 73], [4767, 74], [4767, 75], [4767, 76], [4767, 77], [4767, 78], [4767, 79], [4767, 80], [4767, 81], [4767, 82], [4767, 84], [4767, 85], [4767, 86], [4767, 87], [4767, 88], [4767, 89], [4767, 90], [4767, 91], [4767, 92], [4767, 93], [4767, 94], [4767, 95], [4767, 96], [4767, 97], [4767, 98], [4767, 99], [4767, 100], [4767, 101], [4767, 102], [4767, 103], [4767, 104], [4767, 105], [4767, 106], [4767, 107], [4767, 108], [4767, 109], [4767, 110], [4767, 112], [4767, 113], [4767, 114], [4767, 115], [4767, 116], [4767, 117], [4767, 118], [4767, 119], [4767, 120], [4767, 121], [4767, 122], [4767, 123], [4767, 124], [4767, 125], [4767, 126], [4767, 127], [4767, 128], [4767, 129], [4767, 130], [4767, 131], [4767, 132], [4767, 133], [4767, 134], [4767, 135], [4767, 136], [4767, 137], [4767, 138], [4767, 139], [4767, 140], [4767, 141], [4767, 142], [4767, 143], [4767, 144], [4767, 145], [4767, 146], [4767, 147], [4767, 148], [4767, 149], [4767, 150], [4767, 151], [4767, 152], [4767, 153], [4767, 154], [4767, 155], [4767, 156], [4767, 157], [4767, 158], [4767, 159], [4767, 160], [4767, 161], [4767, 162], [4767, 163], [4767, 164], [4767, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=162, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=208, paths=[[4768, 1], [4768, 2], [4768, 3], [4768, 4], [4768, 5], [4768, 6], [4768, 7], [4768, 8], [4768, 9], [4768, 10], [4768, 11], [4768, 12], [4768, 13], [4768, 14], [4768, 15], [4768, 16], [4768, 17], [4768, 18], [4768, 19], [4768, 20], [4768, 21], [4768, 22], [4768, 23], [4768, 24], [4768, 25], [4768, 26], [4768, 27], [4768, 28], [4768, 29], [4768, 30], [4768, 31], [4768, 32], [4768, 33], [4768, 34], [4768, 35], [4768, 36], [4768, 37], [4768, 38], [4768, 39], [4768, 40], [4768, 41], [4768, 42], [4768, 43], [4768, 44], [4768, 45], [4768, 46], [4768, 47, 1], [4768, 47, 2], [4768, 47, 3], [4768, 47, 4], [4768, 47, 5], [4768, 47, 6], [4768, 47, 7], [4768, 47, 8], [4768, 47, 9], [4768, 47, 10], [4768, 47, 11], [4768, 47, 12], [4768, 47, 13], [4768, 47, 14], [4768, 47, 15], [4768, 47, 16], [4768, 47, 17], [4768, 47, 18], [4768, 47, 19], [4768, 47, 20], [4768, 47, 21], [4768, 47, 22], [4768, 47, 23], [4768, 47, 24], [4768, 47, 25], [4768, 47, 26], [4768, 47, 27], [4768, 47, 29], [4768, 47, 30], [4768, 47, 31], [4768, 47, 32], [4768, 47, 33], [4768, 47, 34], [4768, 47, 35], [4768, 47, 36], [4768, 47, 37], [4768, 47, 38], [4768, 47, 39], [4768, 47, 40], [4768, 47, 41], [4768, 47, 42], [4768, 47, 43], [4768, 47, 44], [4768, 47, 45], [4768, 47, 46], [4768, 47, 47], [4768, 47, 48], [4768, 47, 49], [4768, 47, 50], [4768, 47, 51], [4768, 47, 52], [4768, 47, 53], [4768, 47, 54], [4768, 47, 55], [4768, 47, 56], [4768, 47, 57], [4768, 47, 58], [4768, 47, 59], [4768, 47, 60], [4768, 47, 61], [4768, 47, 62], [4768, 47, 63], [4768, 47, 64], [4768, 47, 65], [4768, 47, 66], [4768, 47, 67], [4768, 47, 68], [4768, 47, 69], [4768, 47, 70], [4768, 47, 71], [4768, 47, 72], [4768, 47, 73], [4768, 47, 74], [4768, 47, 75], [4768, 47, 76], [4768, 47, 77], [4768, 47, 78], [4768, 47, 79], [4768, 47, 80], [4768, 47, 81], [4768, 47, 82], [4768, 47, 84], [4768, 47, 85], [4768, 47, 86], [4768, 47, 87], [4768, 47, 88], [4768, 47, 89], [4768, 47, 90], [4768, 47, 91], [4768, 47, 92], [4768, 47, 93], [4768, 47, 94], [4768, 47, 95], [4768, 47, 96], [4768, 47, 97], [4768, 47, 98], [4768, 47, 99], [4768, 47, 100], [4768, 47, 101], [4768, 47, 102], [4768, 47, 103], [4768, 47, 104], [4768, 47, 105], [4768, 47, 106], [4768, 47, 107], [4768, 47, 108], [4768, 47, 109], [4768, 47, 110], [4768, 47, 112], [4768, 47, 113], [4768, 47, 114], [4768, 47, 115], [4768, 47, 116], [4768, 47, 117], [4768, 47, 118], [4768, 47, 119], [4768, 47, 120], [4768, 47, 121], [4768, 47, 122], [4768, 47, 123], [4768, 47, 124], [4768, 47, 125], [4768, 47, 126], [4768, 47, 127], [4768, 47, 128], [4768, 47, 129], [4768, 47, 130], [4768, 47, 131], [4768, 47, 132], [4768, 47, 133], [4768, 47, 134], [4768, 47, 135], [4768, 47, 136], [4768, 47, 137], [4768, 47, 138], [4768, 47, 139], [4768, 47, 140], [4768, 47, 141], [4768, 47, 142], [4768, 47, 143], [4768, 47, 144], [4768, 47, 145], [4768, 47, 146], [4768, 47, 147], [4768, 47, 148], [4768, 47, 149], [4768, 47, 150], [4768, 47, 151], [4768, 47, 152], [4768, 47, 153], [4768, 47, 154], [4768, 47, 155], [4768, 47, 156], [4768, 47, 157], [4768, 47, 158], [4768, 47, 159], [4768, 47, 160], [4768, 47, 161], [4768, 47, 162], [4768, 47, 163], [4768, 47, 164], [4768, 47, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=208, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=162, paths=[[4769, 1], [4769, 2], [4769, 3], [4769, 4], [4769, 5], [4769, 6], [4769, 7], [4769, 8], [4769, 9], [4769, 10], [4769, 11], [4769, 12], [4769, 13], [4769, 14], [4769, 15], [4769, 16], [4769, 17], [4769, 18], [4769, 19], [4769, 20], [4769, 21], [4769, 22], [4769, 23], [4769, 24], [4769, 25], [4769, 26], [4769, 27], [4769, 29], [4769, 30], [4769, 31], [4769, 32], [4769, 33], [4769, 34], [4769, 35], [4769, 36], [4769, 37], [4769, 38], [4769, 39], [4769, 40], [4769, 41], [4769, 42], [4769, 43], [4769, 44], [4769, 45], [4769, 46], [4769, 47], [4769, 48], [4769, 49], [4769, 50], [4769, 51], [4769, 52], [4769, 53], [4769, 54], [4769, 55], [4769, 56], [4769, 57], [4769, 58], [4769, 59], [4769, 60], [4769, 61], [4769, 62], [4769, 63], [4769, 64], [4769, 65], [4769, 66], [4769, 67], [4769, 68], [4769, 69], [4769, 70], [4769, 71], [4769, 72], [4769, 73], [4769, 74], [4769, 75], [4769, 76], [4769, 77], [4769, 78], [4769, 79], [4769, 80], [4769, 81], [4769, 82], [4769, 84], [4769, 85], [4769, 86], [4769, 87], [4769, 88], [4769, 89], [4769, 90], [4769, 91], [4769, 92], [4769, 93], [4769, 94], [4769, 95], [4769, 96], [4769, 97], [4769, 98], [4769, 99], [4769, 100], [4769, 101], [4769, 102], [4769, 103], [4769, 104], [4769, 105], [4769, 106], [4769, 107], [4769, 108], [4769, 109], [4769, 110], [4769, 112], [4769, 113], [4769, 114], [4769, 115], [4769, 116], [4769, 117], [4769, 118], [4769, 119], [4769, 120], [4769, 121], [4769, 122], [4769, 123], [4769, 124], [4769, 125], [4769, 126], [4769, 127], [4769, 128], [4769, 129], [4769, 130], [4769, 131], [4769, 132], [4769, 133], [4769, 134], [4769, 135], [4769, 136], [4769, 137], [4769, 138], [4769, 139], [4769, 140], [4769, 141], [4769, 142], [4769, 143], [4769, 144], [4769, 145], [4769, 146], [4769, 147], [4769, 148], [4769, 149], [4769, 150], [4769, 151], [4769, 152], [4769, 153], [4769, 154], [4769, 155], [4769, 156], [4769, 157], [4769, 158], [4769, 159], [4769, 160], [4769, 161], [4769, 162], [4769, 163], [4769, 164], [4769, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=162, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=208, paths=[[4770, 1], [4770, 2], [4770, 3], [4770, 4], [4770, 5], [4770, 6], [4770, 7], [4770, 8], [4770, 9], [4770, 10], [4770, 11], [4770, 12], [4770, 13], [4770, 14], [4770, 15], [4770, 16], [4770, 17], [4770, 18], [4770, 19], [4770, 20], [4770, 21], [4770, 22], [4770, 23], [4770, 24], [4770, 25], [4770, 26], [4770, 27], [4770, 28], [4770, 29], [4770, 30], [4770, 31], [4770, 32], [4770, 33], [4770, 34], [4770, 35], [4770, 36], [4770, 37], [4770, 38], [4770, 39], [4770, 40], [4770, 41], [4770, 42], [4770, 43], [4770, 44], [4770, 45], [4770, 46], [4770, 47, 1], [4770, 47, 2], [4770, 47, 3], [4770, 47, 4], [4770, 47, 5], [4770, 47, 6], [4770, 47, 7], [4770, 47, 8], [4770, 47, 9], [4770, 47, 10], [4770, 47, 11], [4770, 47, 12], [4770, 47, 13], [4770, 47, 14], [4770, 47, 15], [4770, 47, 16], [4770, 47, 17], [4770, 47, 18], [4770, 47, 19], [4770, 47, 20], [4770, 47, 21], [4770, 47, 22], [4770, 47, 23], [4770, 47, 24], [4770, 47, 25], [4770, 47, 26], [4770, 47, 27], [4770, 47, 29], [4770, 47, 30], [4770, 47, 31], [4770, 47, 32], [4770, 47, 33], [4770, 47, 34], [4770, 47, 35], [4770, 47, 36], [4770, 47, 37], [4770, 47, 38], [4770, 47, 39], [4770, 47, 40], [4770, 47, 41], [4770, 47, 42], [4770, 47, 43], [4770, 47, 44], [4770, 47, 45], [4770, 47, 46], [4770, 47, 47], [4770, 47, 48], [4770, 47, 49], [4770, 47, 50], [4770, 47, 51], [4770, 47, 52], [4770, 47, 53], [4770, 47, 54], [4770, 47, 55], [4770, 47, 56], [4770, 47, 57], [4770, 47, 58], [4770, 47, 59], [4770, 47, 60], [4770, 47, 61], [4770, 47, 62], [4770, 47, 63], [4770, 47, 64], [4770, 47, 65], [4770, 47, 66], [4770, 47, 67], [4770, 47, 68], [4770, 47, 69], [4770, 47, 70], [4770, 47, 71], [4770, 47, 72], [4770, 47, 73], [4770, 47, 74], [4770, 47, 75], [4770, 47, 76], [4770, 47, 77], [4770, 47, 78], [4770, 47, 79], [4770, 47, 80], [4770, 47, 81], [4770, 47, 82], [4770, 47, 84], [4770, 47, 85], [4770, 47, 86], [4770, 47, 87], [4770, 47, 88], [4770, 47, 89], [4770, 47, 90], [4770, 47, 91], [4770, 47, 92], [4770, 47, 93], [4770, 47, 94], [4770, 47, 95], [4770, 47, 96], [4770, 47, 97], [4770, 47, 98], [4770, 47, 99], [4770, 47, 100], [4770, 47, 101], [4770, 47, 102], [4770, 47, 103], [4770, 47, 104], [4770, 47, 105], [4770, 47, 106], [4770, 47, 107], [4770, 47, 108], [4770, 47, 109], [4770, 47, 110], [4770, 47, 112], [4770, 47, 113], [4770, 47, 114], [4770, 47, 115], [4770, 47, 116], [4770, 47, 117], [4770, 47, 118], [4770, 47, 119], [4770, 47, 120], [4770, 47, 121], [4770, 47, 122], [4770, 47, 123], [4770, 47, 124], [4770, 47, 125], [4770, 47, 126], [4770, 47, 127], [4770, 47, 128], [4770, 47, 129], [4770, 47, 130], [4770, 47, 131], [4770, 47, 132], [4770, 47, 133], [4770, 47, 134], [4770, 47, 135], [4770, 47, 136], [4770, 47, 137], [4770, 47, 138], [4770, 47, 139], [4770, 47, 140], [4770, 47, 141], [4770, 47, 142], [4770, 47, 143], [4770, 47, 144], [4770, 47, 145], [4770, 47, 146], [4770, 47, 147], [4770, 47, 148], [4770, 47, 149], [4770, 47, 150], [4770, 47, 151], [4770, 47, 152], [4770, 47, 153], [4770, 47, 154], [4770, 47, 155], [4770, 47, 156], [4770, 47, 157], [4770, 47, 158], [4770, 47, 159], [4770, 47, 160], [4770, 47, 161], [4770, 47, 162], [4770, 47, 163], [4770, 47, 164], [4770, 47, 165]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=208, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=0, paths=[]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=0, two_qubit=0)])

if __name__ == "__main__":
    c = 0
