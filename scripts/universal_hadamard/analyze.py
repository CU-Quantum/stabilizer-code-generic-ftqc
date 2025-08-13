/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
Running with arguments: Namespace(num_shots=20, surface_code_distance=3, num_measurement_rounds=3, prob_one_qubit_error=0.001, prob_two_qubit_error=0.002, num_processes=3)
2025-08-13 01:41:51.626340: Start runner
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
----NUMBER OF NOISY CIRCUITS----: 9
    Time since last timestamp: 0:00:41.135734
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
/Applications/PyCharm.app/Contents/plugins/python-ce/helpers/pydev/pydevd_plugins/__init__.py:2: UserWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html. The pkg_resources package is slated for removal as early as 2025-11-30. Refrain from using this package or pin to Setuptools<81.
  __import__('pkg_resources').declare_namespace(__name__)
    Time since last timestamp: 0:00:54.179769

----NUMBER OF ERRORED CIRCUITS----: 2

----SUCCESS RATE----: 90.0%

----ERROR----: 2 circuits that failed should have been corrected. Printing first one.

    1st ERRORED CIRCUIT NOISY OPERATIONS WITH MOMENT INDICES: [([cirq.TaggedOperation(cirq.CircuitOperation(
    circuit=cirq.FrozenCircuit([
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_b3a153ec163a4b76a84d719f14e6db39')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_b3a153ec163a4b76a84d719f14e6db39')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(0)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(1)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_2aefb7cc6529495fa1d199f2f7f79c27')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_2aefb7cc6529495fa1d199f2f7f79c27')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(1)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(2)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_c8cadbb063a14bbab1cbadb41fc499a6')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_c8cadbb063a14bbab1cbadb41fc499a6')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(3)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(4)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(20), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(21), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(21), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_087d21c2c1114b20a467882c05922596')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_087d21c2c1114b20a467882c05922596')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(21), cirq.LineQubit(4)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(5)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(21), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(21)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(22)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(22)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(22), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(22), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_816b1cd1d5c64874a98e0b8c8c4cd4e0')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_816b1cd1d5c64874a98e0b8c8c4cd4e0')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(22), cirq.LineQubit(6)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(7)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(22), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(22)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(23)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(23)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(23), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(23), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_d463d6ba0c6a4b7cbf4956f93530d741')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_d463d6ba0c6a4b7cbf4956f93530d741')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(23), cirq.LineQubit(7)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(8)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(23), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(23)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(24)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                    cirq.ResetChannel()(cirq.LineQubit(28)),
                                    cirq.ResetChannel()(cirq.LineQubit(29)),
                                    cirq.ResetChannel()(cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(24)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(28)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(29)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(31)),
                                    cirq.ResetChannel()(cirq.LineQubit(32)),
                                    cirq.ResetChannel()(cirq.LineQubit(33)),
                                    cirq.ResetChannel()(cirq.LineQubit(34)),
                                    cirq.ResetChannel()(cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(31), key=cirq.MeasurementKey(name='VERIFICATION_0d39908e316c444da2b4fc84cb7194fa')),
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(32), key=cirq.MeasurementKey(name='VERIFICATION_0d39908e316c444da2b4fc84cb7194fa')),
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(33), key=cirq.MeasurementKey(name='VERIFICATION_0d39908e316c444da2b4fc84cb7194fa')),
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(34), key=cirq.MeasurementKey(name='VERIFICATION_0d39908e316c444da2b4fc84cb7194fa')),
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(35), key=cirq.MeasurementKey(name='VERIFICATION_0d39908e316c444da2b4fc84cb7194fa')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_0d39908e316c444da2b4fc84cb7194fa')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(0)),
                        cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(1)),
                        cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(2)),
                        cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(3)),
                        cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(4)),
                        cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(5)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(30)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(29)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(28)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(27)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(24)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(25)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                    cirq.ResetChannel()(cirq.LineQubit(28)),
                                    cirq.ResetChannel()(cirq.LineQubit(29)),
                                    cirq.ResetChannel()(cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(25)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(28)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(29)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(31)),
                                    cirq.ResetChannel()(cirq.LineQubit(32)),
                                    cirq.ResetChannel()(cirq.LineQubit(33)),
                                    cirq.ResetChannel()(cirq.LineQubit(34)),
                                    cirq.ResetChannel()(cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(31), key=cirq.MeasurementKey(name='VERIFICATION_4dd0335dc25149b984ead7ccb3ef03b8')),
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(32), key=cirq.MeasurementKey(name='VERIFICATION_4dd0335dc25149b984ead7ccb3ef03b8')),
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(33), key=cirq.MeasurementKey(name='VERIFICATION_4dd0335dc25149b984ead7ccb3ef03b8')),
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(34), key=cirq.MeasurementKey(name='VERIFICATION_4dd0335dc25149b984ead7ccb3ef03b8')),
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(35), key=cirq.MeasurementKey(name='VERIFICATION_4dd0335dc25149b984ead7ccb3ef03b8')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_4dd0335dc25149b984ead7ccb3ef03b8')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(3)),
                        cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(4)),
                        cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(5)),
                        cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(6)),
                        cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(7)),
                        cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(8)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(30)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(29)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(28)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(27)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(25)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_77d5eaad82b442dfaadde1d10659b171')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_bb348f3844bc47ccb404c03f87418e63')),
                        cirq.measure(cirq.LineQubit(20), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_ca1790de10d244889f559a1506193c77')),
                        cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_b04dde8f8fb24cf69f895756c6952e89')),
                        cirq.measure(cirq.LineQubit(22), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_bf46cc3464ef4888bbf3b65013b7436b')),
                        cirq.measure(cirq.LineQubit(23), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_e10ef576d3fc44c28f67bcd7f4f081dc')),
                        cirq.measure(cirq.LineQubit(24), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_35fcea2bc2ff4ed293175a46257fde12')),
                        cirq.measure(cirq.LineQubit(25), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_8701ee96ad0f46d4b0f177717cad2cc7')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_77d5eaad82b442dfaadde1d10659b171'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_bb348f3844bc47ccb404c03f87418e63'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_ca1790de10d244889f559a1506193c77'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_b04dde8f8fb24cf69f895756c6952e89'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_bf46cc3464ef4888bbf3b65013b7436b'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_e10ef576d3fc44c28f67bcd7f4f081dc'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_35fcea2bc2ff4ed293175a46257fde12'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_8701ee96ad0f46d4b0f177717cad2cc7'))),
            ), 'FAULT_TOLERANT_MEASURER'),
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
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 0, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 1, 0, 0])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 1, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 1, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 1, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_913a020f148943dea161b859976b9668'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
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
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_501daa70ebbf46c69d79f85b78d3c443')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_501daa70ebbf46c69d79f85b78d3c443')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(9)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(10)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_9a3c23116ed142088f8dec0dab8c50a4')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_9a3c23116ed142088f8dec0dab8c50a4')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(10)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(11)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_96431c89d4ca493cbd4bf97984d1d880')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_ee9a36740fa04978835b361388bfa8ff')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_96431c89d4ca493cbd4bf97984d1d880'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_ee9a36740fa04978835b361388bfa8ff'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(9)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_9c3408ff6d314ac3ac5a29db74a1bf93'), symptom=[1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(10)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_9c3408ff6d314ac3ac5a29db74a1bf93'), symptom=[1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_9c3408ff6d314ac3ac5a29db74a1bf93'), symptom=[0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
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
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_b9de73f143a348e9baa37f9e129681fc')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_b9de73f143a348e9baa37f9e129681fc')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(12)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(13)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_6c8773dc9b1b43b3811b7e5f2f789961')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_6c8773dc9b1b43b3811b7e5f2f789961')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(13)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(14)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_8df2db3245034a5b80272737df90f382')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_cfe45dead8f749a29dff2108f6995894')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_8df2db3245034a5b80272737df90f382'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_cfe45dead8f749a29dff2108f6995894'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.Y(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(12)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8eb92b210b4d4941b1bfaaef182fa416'), symptom=[1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(13)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8eb92b210b4d4941b1bfaaef182fa416'), symptom=[1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8eb92b210b4d4941b1bfaaef182fa416'), symptom=[0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
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
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_a45f3be71050457b8bb0ad1a28bca619')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_a45f3be71050457b8bb0ad1a28bca619')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(15)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(16)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_40e9d4282734421984f3753779885ce6')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_40e9d4282734421984f3753779885ce6')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(16)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(17)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_035433294da54c548f90d4ed96b33df4')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_9663a3f1f43246ab8b7cfe306f8a7f26')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_035433294da54c548f90d4ed96b33df4'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_9663a3f1f43246ab8b7cfe306f8a7f26'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(15)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_ff84fb4fe7ab49b09842d86bc5d186ad'), symptom=[1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(16)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_ff84fb4fe7ab49b09842d86bc5d186ad'), symptom=[1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_ff84fb4fe7ab49b09842d86bc5d186ad'), symptom=[0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
    ]),
), 'CORRECTION_ROUND'), cirq.TaggedOperation(cirq.Y(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit')], [111, 9]), ([cirq.TaggedOperation(cirq.CircuitOperation(
    circuit=cirq.FrozenCircuit([
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_571d31c4b1e545a9aec73c6e6331af7a')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_571d31c4b1e545a9aec73c6e6331af7a')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(0)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(1)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_0a12304ad39e4eed90d74f0c6eac2a5c')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_0a12304ad39e4eed90d74f0c6eac2a5c')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(1)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(2)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_6a5516add2e54c6d96497cab3cf96532')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_6a5516add2e54c6d96497cab3cf96532')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(3)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(4)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(20), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(21), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(21), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_1d176151de9e41ebbfe9cfc6327ad178')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_1d176151de9e41ebbfe9cfc6327ad178')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(21), cirq.LineQubit(4)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(5)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(21), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(21)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(22)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(22)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(22), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(22), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_5a91f9620e644583a22760cc5d908316')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_5a91f9620e644583a22760cc5d908316')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(22), cirq.LineQubit(6)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(7)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(22), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(22)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(23)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(23)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(23), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(23), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(27), key=cirq.MeasurementKey(name='VERIFICATION_2873a0fce03c49de88006990655f5855')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_2873a0fce03c49de88006990655f5855')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(23), cirq.LineQubit(7)),
                        cirq.CZ(cirq.LineQubit(26), cirq.LineQubit(8)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(23), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(23)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(24)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                    cirq.ResetChannel()(cirq.LineQubit(28)),
                                    cirq.ResetChannel()(cirq.LineQubit(29)),
                                    cirq.ResetChannel()(cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(24)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(28)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(29)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(31)),
                                    cirq.ResetChannel()(cirq.LineQubit(32)),
                                    cirq.ResetChannel()(cirq.LineQubit(33)),
                                    cirq.ResetChannel()(cirq.LineQubit(34)),
                                    cirq.ResetChannel()(cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(31), key=cirq.MeasurementKey(name='VERIFICATION_5edf7dc8e23b49889acc0c9a17c45c6a')),
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(32), key=cirq.MeasurementKey(name='VERIFICATION_5edf7dc8e23b49889acc0c9a17c45c6a')),
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(33), key=cirq.MeasurementKey(name='VERIFICATION_5edf7dc8e23b49889acc0c9a17c45c6a')),
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(34), key=cirq.MeasurementKey(name='VERIFICATION_5edf7dc8e23b49889acc0c9a17c45c6a')),
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(35), key=cirq.MeasurementKey(name='VERIFICATION_5edf7dc8e23b49889acc0c9a17c45c6a')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_5edf7dc8e23b49889acc0c9a17c45c6a')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(24), cirq.LineQubit(0)),
                        cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(1)),
                        cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(2)),
                        cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(3)),
                        cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(4)),
                        cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(5)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(30)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(29)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(28)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(27)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(24), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(24)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(25)),
                                    cirq.ResetChannel()(cirq.LineQubit(26)),
                                    cirq.ResetChannel()(cirq.LineQubit(27)),
                                    cirq.ResetChannel()(cirq.LineQubit(28)),
                                    cirq.ResetChannel()(cirq.LineQubit(29)),
                                    cirq.ResetChannel()(cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(25)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(26)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(27)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(28)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(29)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(30)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(31)),
                                    cirq.ResetChannel()(cirq.LineQubit(32)),
                                    cirq.ResetChannel()(cirq.LineQubit(33)),
                                    cirq.ResetChannel()(cirq.LineQubit(34)),
                                    cirq.ResetChannel()(cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(31)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(31), key=cirq.MeasurementKey(name='VERIFICATION_7fb5e46091de4997a7e6bd3d1e47b755')),
                                    cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(32)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(32), key=cirq.MeasurementKey(name='VERIFICATION_7fb5e46091de4997a7e6bd3d1e47b755')),
                                    cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(33)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(33), key=cirq.MeasurementKey(name='VERIFICATION_7fb5e46091de4997a7e6bd3d1e47b755')),
                                    cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(34)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(34), key=cirq.MeasurementKey(name='VERIFICATION_7fb5e46091de4997a7e6bd3d1e47b755')),
                                    cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(35)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(35), key=cirq.MeasurementKey(name='VERIFICATION_7fb5e46091de4997a7e6bd3d1e47b755')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_7fb5e46091de4997a7e6bd3d1e47b755')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CNOT(cirq.LineQubit(25), cirq.LineQubit(3)),
                        cirq.CNOT(cirq.LineQubit(26), cirq.LineQubit(4)),
                        cirq.CNOT(cirq.LineQubit(27), cirq.LineQubit(5)),
                        cirq.CNOT(cirq.LineQubit(28), cirq.LineQubit(6)),
                        cirq.CNOT(cirq.LineQubit(29), cirq.LineQubit(7)),
                        cirq.CNOT(cirq.LineQubit(30), cirq.LineQubit(8)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(30)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(29)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(28)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(27)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(25), cirq.LineQubit(26)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(25)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_3c08303e223541eead069c5ee54bee56')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d3a33e0ad0344e9cb78dde32a9baa024')),
                        cirq.measure(cirq.LineQubit(20), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d57effbea8eb46a5bb673fec8d681e1f')),
                        cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_a5998973350b44309de5393b456a6509')),
                        cirq.measure(cirq.LineQubit(22), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_45839ec0ec394c6ba86e3e7f4c0bfde3')),
                        cirq.measure(cirq.LineQubit(23), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_7299e85575f54606bc047f7f0669913d')),
                        cirq.measure(cirq.LineQubit(24), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_ee400e39df5d4ac5aeff4f55db318406')),
                        cirq.measure(cirq.LineQubit(25), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_5c5e7956eb9841a280e7d2c790dddf4b')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_3c08303e223541eead069c5ee54bee56'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d3a33e0ad0344e9cb78dde32a9baa024'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d57effbea8eb46a5bb673fec8d681e1f'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_a5998973350b44309de5393b456a6509'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_45839ec0ec394c6ba86e3e7f4c0bfde3'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_7299e85575f54606bc047f7f0669913d'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_ee400e39df5d4ac5aeff4f55db318406'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_5c5e7956eb9841a280e7d2c790dddf4b'))),
            ), 'FAULT_TOLERANT_MEASURER'),
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
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 0, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 1, 0, 0])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 1, 0, 0, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 1, 0, 0, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 1, 0, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 0, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 1, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 1, 0, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 1, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Y(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 1, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 0, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(6)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(7)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(0)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(1)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(3)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(4)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 0, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 1, 0, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 0, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 0, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[1, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 1, 1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 1, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 0, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 1, 0, 0, 0, 0, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 0, 0, 1, 1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 1, 1, 0, 0, 0, 1])]),
                    ),
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(2)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 1, 0, 0, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.Z(cirq.LineQubit(8)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(5)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_8e5dcbc226df4ac08bac0986f7d73fab'), symptom=[0, 0, 0, 1, 0, 0, 0, 1])]),
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
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_f068def8be2a4f71ab61cb243351cab5')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_f068def8be2a4f71ab61cb243351cab5')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(9)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(10)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_ff8c2bcdd96746989de52a252e2b9df1')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_ff8c2bcdd96746989de52a252e2b9df1')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(10)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(11)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_c874d51ee0af4532b15e3958dcfb0095')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_67168a88f6084244883d2a20bda8b7e0')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_c874d51ee0af4532b15e3958dcfb0095'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_67168a88f6084244883d2a20bda8b7e0'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(9)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_7aa4208afd07490eb8aeeb30d27420f2'), symptom=[1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(10)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_7aa4208afd07490eb8aeeb30d27420f2'), symptom=[1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(11)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_7aa4208afd07490eb8aeeb30d27420f2'), symptom=[0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
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
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_d5fe74b513d148ad9ac413893e3a95d7')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_d5fe74b513d148ad9ac413893e3a95d7')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(12)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(13)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_b8f0279c629f49f9931d952bc81fe0db')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_b8f0279c629f49f9931d952bc81fe0db')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(13)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(14)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_e7f6089b4af84324b735f11dd4f950be')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d70cb84b2930468db1baff1f51a3f042')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_e7f6089b4af84324b735f11dd4f950be'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_d70cb84b2930468db1baff1f51a3f042'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(12)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_c44f65c9116942858b879b8d3e4983fd'), symptom=[1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(13)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_c44f65c9116942858b879b8d3e4983fd'), symptom=[1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(14)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_c44f65c9116942858b879b8d3e4983fd'), symptom=[0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.X(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
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
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(18)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(18)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(18), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_7c3b694b68be45b7bf184c3ac08dd632')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_7c3b694b68be45b7bf184c3ac08dd632')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(18), cirq.LineQubit(15)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(16)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(18), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(18)),
                    ),
                    cirq.Moment(
                        cirq.TaggedOperation(cirq.CircuitOperation(
                            circuit=cirq.FrozenCircuit([
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(19)),
                                    cirq.ResetChannel()(cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.H(cirq.LineQubit(19)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(20)),
                                ),
                                cirq.Moment(
                                    cirq.ResetChannel()(cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(19), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.CNOT(cirq.LineQubit(20), cirq.LineQubit(21)),
                                ),
                                cirq.Moment(
                                    cirq.measure(cirq.LineQubit(21), key=cirq.MeasurementKey(name='VERIFICATION_5a83f6ee5e70472d955da3eeddfae260')),
                                ),
                            ]),
                            use_repetition_ids=False,
                            repeat_until=VerificationIsZero(cirq.MeasurementKey(name='VERIFICATION_5a83f6ee5e70472d955da3eeddfae260')),
                        ), 'CAT_STATE_CREATOR_BASIC_NONDETERMINISTIC'),
                    ),
                    cirq.Moment(
                        cirq.CZ(cirq.LineQubit(19), cirq.LineQubit(16)),
                        cirq.CZ(cirq.LineQubit(20), cirq.LineQubit(17)),
                    ),
                    cirq.Moment(
                        (cirq.CNOT**-1.0).on(cirq.LineQubit(19), cirq.LineQubit(20)),
                    ),
                    cirq.Moment(
                        (cirq.H**-1.0).on(cirq.LineQubit(19)),
                    ),
                    cirq.Moment(
                        cirq.measure(cirq.LineQubit(18), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_b0663035f8f94204a8d52586b2de497e')),
                        cirq.measure(cirq.LineQubit(19), key=cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_551fe8327860411bbd3b1a9eb71763c5')),
                    ),
                ]),
                use_repetition_ids=False,
                repeat_until=MultipleConditions((cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_b0663035f8f94204a8d52586b2de497e'), cirq.MeasurementKey(name='FAULT_TOLERANT_MEASUREMENT_551fe8327860411bbd3b1a9eb71763c5'))),
            ), 'FAULT_TOLERANT_MEASURER'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.CircuitOperation(
                circuit=cirq.FrozenCircuit([
                    cirq.Moment(
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(15)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_11e12447665c4f5ebafafafd52608fdb'), symptom=[1, 0])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(16)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_11e12447665c4f5ebafafafd52608fdb'), symptom=[1, 1])]),
                        cirq.ClassicallyControlledOperation(cirq.X(cirq.LineQubit(17)), [RecoveryCondition(key=cirq.MeasurementKey(name='ERROR_RECOVERY_11e12447665c4f5ebafafafd52608fdb'), symptom=[0, 1])]),
                    ),
                ]),
            ), 'NO_NOISE_TAG'),
        ),
        cirq.Moment(
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(16)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(17)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(15)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(22)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(9)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(0)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(33)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(2)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(24)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(13)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(35)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(26)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(6)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(4)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(28)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(19)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(8)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(30)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(10)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(32)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(1)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(21)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(12)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(23)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(34)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(3)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(14)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(5)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(27)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(29)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(31)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(25)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(7)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(18)), 'NoisyChannel','NoisyChannel_OneQubit'),
            cirq.TaggedOperation(cirq.I(cirq.LineQubit(20)), 'NoisyChannel','NoisyChannel_OneQubit'),
        ),
    ]),
), 'CORRECTION_ROUND'), cirq.TaggedOperation(cirq.X(cirq.LineQubit(11)), 'NoisyChannel','NoisyChannel_OneQubit')], [114, 11])]

    1st ERRORED CIRCUIT COUNTS: NoisyOperationsCountPerCorrectionRound(counts=[NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=459, paths=[[1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11], [12], [13], [14], [15], [16], [17], [18], [19], [20], [21], [22], [23], [24], [25], [26], [27], [28], [29], [30], [31], [32], [33], [34], [35], [36], [38], [39], [40], [41], [42], [43], [44], [45], [46], [47], [48], [49], [50], [51], [52], [53], [54], [55], [56], [57], [58], [59], [60], [61], [62], [63], [64], [65], [66], [67], [68], [69], [70], [71], [72], [73], [75], [76], [77], [78], [79], [80], [81], [82], [83], [84], [85], [86], [87], [88], [89], [90], [91], [92], [93], [94], [95], [96], [97], [98], [99], [100], [101], [102], [103], [104], [105], [106], [107], [108], [109], [110], [112], [113], [114], [115], [116], [117], [118], [119], [120], [121], [122], [123], [124], [125], [126], [127], [128], [129], [130], [131], [132], [133], [134], [135], [136], [137], [138], [139], [140], [141], [142], [143], [144], [145], [146], [147], [149], [150], [151], [152], [153], [154], [155], [156], [157], [158], [159], [160], [161], [162], [163], [164], [165], [166], [167], [168], [169], [170], [171], [172], [173], [174], [175], [176], [177], [178], [179], [180], [181], [182], [183], [184], [186], [187], [188], [189], [190], [191], [192], [193], [194], [195], [196], [197], [198], [199], [200], [201], [202], [203], [204], [205], [206], [207], [208], [209], [210], [211], [212], [213], [214], [215], [216], [217], [218], [219], [220], [221], [223], [224], [225], [226], [227], [228], [229], [230], [231], [232], [233], [234], [235], [236], [237], [238], [239], [240], [241], [242], [243], [244], [245], [246], [247], [248], [249], [250], [251], [252], [253], [254], [255], [256], [257], [258], [260], [261], [262], [263], [264], [265], [266], [267], [268], [269], [270], [271], [272], [273], [274], [275], [276], [277], [278], [279], [280], [281], [282], [283], [284], [285], [286], [287], [288], [289], [290], [291], [292], [293], [294], [295], [297], [298], [299], [300], [301], [302], [303], [304], [305], [306], [307], [308], [309], [310], [311], [312], [313], [314], [315], [316], [317], [318], [319], [320], [321], [322], [323], [324], [325], [326], [327], [328], [329], [330], [331], [332], [334], [335], [336], [337], [338], [339], [340], [341], [342], [344], [345], [346], [347], [348], [349], [350], [351], [352], [353], [354], [355], [356], [357], [358], [359], [360], [361], [362], [363], [364], [365], [366], [367], [368], [369], [370], [371], [372], [373], [374], [375], [376], [377], [378], [379], [380, 1], [380, 2], [380, 3], [380, 4], [380, 5], [380, 6], [380, 7], [380, 8], [380, 9], [380, 11], [380, 12], [380, 13], [380, 14], [380, 15], [380, 16], [380, 17], [380, 18], [380, 19], [380, 20], [380, 21], [380, 22], [380, 23], [380, 24], [380, 25], [380, 26], [380, 27], [380, 28], [380, 29], [380, 30], [380, 31], [380, 32], [380, 33], [380, 34], [380, 35], [380, 36], [380, 37], [380, 38], [380, 39], [380, 40], [380, 41], [380, 42], [380, 43], [380, 44], [380, 45], [380, 46], [380, 48], [380, 49], [380, 50], [380, 51], [380, 52], [380, 53], [380, 54], [380, 55], [380, 56], [380, 58], [380, 59], [380, 60], [380, 61], [380, 62], [380, 63], [380, 64], [380, 65], [380, 66], [380, 67], [380, 68], [380, 69], [380, 70], [380, 71], [380, 72], [380, 73], [380, 74], [380, 75], [380, 76], [380, 77], [380, 78], [380, 79], [380, 80], [380, 81], [380, 82], [380, 83], [380, 84], [380, 85], [380, 86], [380, 87], [380, 88], [380, 89], [380, 90], [380, 91], [380, 92], [380, 93]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=447, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=495, paths=[[390], [391], [392], [393], [394], [395], [396], [397], [398], [399], [400], [401], [402], [403], [404], [405], [406], [407], [408], [409], [410], [411], [412], [413], [414], [415], [416], [417], [418], [419], [420], [421], [422], [423], [424], [425], [427], [428], [429], [430], [431], [432], [433], [434], [435], [436], [437], [438], [439], [440], [441], [442], [443], [444], [445], [446], [447], [448], [449], [450], [451], [452], [453], [454], [455], [456], [457], [458], [459], [460], [461], [462], [464], [465], [466], [467], [468], [469], [470], [471], [472], [473], [474], [475], [476], [477], [478], [479], [480], [481], [482], [483], [484], [485], [486], [487], [488], [489], [490], [491], [492], [493], [494], [495], [496], [497], [498], [499], [501], [502], [503], [504], [505], [506], [507], [508], [509], [510], [511], [512], [513], [514], [515], [516], [517], [518], [519], [520], [521], [522], [523], [524], [525], [526], [527], [528], [529], [530], [531], [532], [533], [534], [535], [536], [538], [539], [540], [541], [542], [543], [544], [545], [546], [547], [548], [549], [550], [551], [552], [553], [554], [555], [556], [557], [558], [559], [560], [561], [562], [563], [564], [565], [566], [567], [568], [569], [570], [571], [572], [573], [575], [576], [577], [578], [579], [580], [581], [582], [583], [584], [585], [586], [587], [588], [589], [590], [591], [592], [593], [594], [595], [596], [597], [598], [599], [600], [601], [602], [603], [604], [605], [606], [607], [608], [609], [610], [612], [613], [614], [615], [616], [617], [618], [619], [620], [621], [622], [623], [624], [625], [626], [627], [628], [629], [630], [631], [632], [633], [634], [635], [636], [637], [638], [639], [640], [641], [642], [643], [644], [645], [646], [647], [649], [650], [651], [652], [653], [654], [655], [656], [657], [658], [659], [660], [661], [662], [663], [664], [665], [666], [667], [668], [669], [670], [671], [672], [673], [674], [675], [676], [677], [678], [679], [680], [681], [682], [683], [684], [686], [687], [688], [689], [690], [691], [692], [693], [694], [695], [696], [697], [698], [699], [700], [701], [702], [703], [704], [705], [706], [707], [708], [709], [710], [711], [712], [713], [714], [715], [716], [717], [718], [719], [720], [721], [723], [724], [725], [726], [727], [728], [729], [730], [731], [732], [733], [734], [735], [736], [737], [738], [739], [740], [741], [742], [743], [744], [745], [746], [747], [748], [749], [750], [751], [752], [753], [754], [755], [756], [757], [758], [760], [761], [762], [763], [764], [765], [766], [767], [768], [770], [771], [772], [773], [774], [775], [776], [777], [778], [779], [780], [781], [782], [783], [784], [785], [786], [787], [788], [789], [790], [791], [792], [793], [794], [795], [796], [797], [798], [799], [800], [801], [802], [803], [804], [805], [806, 1], [806, 2], [806, 3], [806, 4], [806, 5], [806, 6], [806, 7], [806, 8], [806, 9], [806, 11], [806, 12], [806, 13], [806, 14], [806, 15], [806, 16], [806, 17], [806, 18], [806, 19], [806, 20], [806, 21], [806, 22], [806, 23], [806, 24], [806, 25], [806, 26], [806, 27], [806, 28], [806, 29], [806, 30], [806, 31], [806, 32], [806, 33], [806, 34], [806, 35], [806, 36], [806, 37], [806, 38], [806, 39], [806, 40], [806, 41], [806, 42], [806, 43], [806, 44], [806, 45], [806, 46], [806, 48], [806, 49], [806, 50], [806, 51], [806, 52], [806, 53], [806, 54], [806, 55], [806, 56], [806, 58], [806, 59], [806, 60], [806, 61], [806, 62], [806, 63], [806, 64], [806, 65], [806, 66], [806, 67], [806, 68], [806, 69], [806, 70], [806, 71], [806, 72], [806, 73], [806, 74], [806, 75], [806, 76], [806, 77], [806, 78], [806, 79], [806, 80], [806, 81], [806, 82], [806, 83], [806, 84], [806, 85], [806, 86], [806, 87], [806, 88], [806, 89], [806, 90], [806, 91], [806, 92], [806, 93]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=483, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[810], [811], [812], [813], [814], [815], [816], [817], [818], [819], [820], [821], [822], [823], [824], [825], [826], [827], [828], [829], [830], [831], [832], [833], [834], [835], [836], [837], [838], [839], [840], [841], [842], [843], [844], [845], [846, 1], [846, 2], [846, 3], [846, 4], [846, 5], [846, 6], [846, 7], [846, 8], [846, 9], [846, 11], [846, 12], [846, 13], [846, 14], [846, 15], [846, 16], [846, 17], [846, 18], [846, 19], [846, 20], [846, 21], [846, 22], [846, 23], [846, 24], [846, 25], [846, 26], [846, 27], [846, 28], [846, 29], [846, 30], [846, 31], [846, 32], [846, 33], [846, 34], [846, 35], [846, 36], [846, 37], [846, 38], [846, 39], [846, 40], [846, 41], [846, 42], [846, 43], [846, 44], [846, 45], [846, 46], [846, 48], [846, 49], [846, 50], [846, 51], [846, 52], [846, 53], [846, 54], [846, 55], [846, 56], [846, 57], [846, 58], [846, 59], [846, 60], [846, 61], [846, 62], [846, 63], [846, 64], [846, 65], [846, 66], [846, 67], [846, 68], [846, 69], [846, 70], [846, 71], [846, 72], [846, 73], [846, 74], [846, 75], [846, 76], [846, 78], [846, 79], [846, 80], [846, 81], [846, 82], [846, 83], [846, 84], [846, 85], [846, 86], [846, 87], [846, 88], [846, 89], [846, 90], [846, 91], [846, 92], [846, 93], [846, 94], [846, 95], [846, 96], [846, 97], [846, 98], [846, 99], [846, 100], [846, 101], [846, 102], [846, 103], [846, 104], [846, 105], [846, 106], [846, 107], [846, 108], [846, 109], [846, 110], [846, 111], [846, 112], [846, 113], [846, 115], [846, 116], [846, 117], [846, 118], [846, 119], [846, 120], [846, 121], [846, 122], [846, 123], [846, 124], [846, 125], [846, 126], [846, 127], [846, 128], [846, 129], [846, 130], [846, 131], [846, 132], [846, 133], [846, 134], [846, 135], [846, 136], [846, 137], [846, 138], [846, 139], [846, 140], [846, 141], [846, 142], [846, 143], [846, 145], [846, 146], [846, 147], [846, 148], [846, 149], [846, 150], [846, 151], [846, 152], [846, 153], [846, 154], [846, 155], [846, 156], [846, 157], [846, 158], [846, 159], [846, 160], [846, 161], [846, 162], [846, 163], [846, 164], [846, 165], [846, 166], [846, 167], [846, 168], [846, 169], [846, 170], [846, 171], [846, 172], [846, 173], [846, 174], [846, 175], [846, 176], [846, 177], [846, 178], [846, 179], [846, 180], [846, 182], [846, 183], [846, 184], [846, 185], [846, 186], [846, 187], [846, 188], [846, 189], [846, 190], [846, 191], [846, 192], [846, 193], [846, 194], [846, 195], [846, 196], [846, 197], [846, 198], [846, 199], [846, 200], [846, 201], [846, 202], [846, 203], [846, 204], [846, 205], [846, 206], [846, 207], [846, 208], [846, 209], [846, 210], [846, 212], [846, 213], [846, 214], [846, 215], [846, 216], [846, 217], [846, 218], [846, 219], [846, 220], [846, 221], [846, 222], [846, 223], [846, 224], [846, 225], [846, 226], [846, 227], [846, 228], [846, 229], [846, 230], [846, 231], [846, 232], [846, 233], [846, 234], [846, 235], [846, 236], [846, 237], [846, 238], [846, 239], [846, 240], [846, 241], [846, 242], [846, 243], [846, 244], [846, 245], [846, 246], [846, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[850], [851], [852], [853], [854], [855], [856], [857], [858], [859], [860], [861], [862], [863], [864], [865], [866], [867], [868], [869], [870], [871], [872], [873], [874], [875], [876], [877], [878], [879], [880], [881], [882], [883], [884], [885], [886, 1], [886, 2], [886, 3], [886, 4], [886, 5], [886, 6], [886, 7], [886, 8], [886, 9], [886, 11], [886, 12], [886, 13], [886, 14], [886, 15], [886, 16], [886, 17], [886, 18], [886, 19], [886, 20], [886, 21], [886, 22], [886, 23], [886, 24], [886, 25], [886, 26], [886, 27], [886, 28], [886, 29], [886, 30], [886, 31], [886, 32], [886, 33], [886, 34], [886, 35], [886, 36], [886, 37], [886, 38], [886, 39], [886, 40], [886, 41], [886, 42], [886, 43], [886, 44], [886, 45], [886, 46], [886, 48], [886, 49], [886, 50], [886, 51], [886, 52], [886, 53], [886, 54], [886, 55], [886, 56], [886, 57], [886, 58], [886, 59], [886, 60], [886, 61], [886, 62], [886, 63], [886, 64], [886, 65], [886, 66], [886, 67], [886, 68], [886, 69], [886, 70], [886, 71], [886, 72], [886, 73], [886, 74], [886, 75], [886, 76], [886, 78], [886, 79], [886, 80], [886, 81], [886, 82], [886, 83], [886, 84], [886, 85], [886, 86], [886, 87], [886, 88], [886, 89], [886, 90], [886, 91], [886, 92], [886, 93], [886, 94], [886, 95], [886, 96], [886, 97], [886, 98], [886, 99], [886, 100], [886, 101], [886, 102], [886, 103], [886, 104], [886, 105], [886, 106], [886, 107], [886, 108], [886, 109], [886, 110], [886, 111], [886, 112], [886, 113], [886, 115], [886, 116], [886, 117], [886, 118], [886, 119], [886, 120], [886, 121], [886, 122], [886, 123], [886, 124], [886, 125], [886, 126], [886, 127], [886, 128], [886, 129], [886, 130], [886, 131], [886, 132], [886, 133], [886, 134], [886, 135], [886, 136], [886, 137], [886, 138], [886, 139], [886, 140], [886, 141], [886, 142], [886, 143], [886, 145], [886, 146], [886, 147], [886, 148], [886, 149], [886, 150], [886, 151], [886, 152], [886, 153], [886, 154], [886, 155], [886, 156], [886, 157], [886, 158], [886, 159], [886, 160], [886, 161], [886, 162], [886, 163], [886, 164], [886, 165], [886, 166], [886, 167], [886, 168], [886, 169], [886, 170], [886, 171], [886, 172], [886, 173], [886, 174], [886, 175], [886, 176], [886, 177], [886, 178], [886, 179], [886, 180], [886, 182], [886, 183], [886, 184], [886, 185], [886, 186], [886, 187], [886, 188], [886, 189], [886, 190], [886, 191], [886, 192], [886, 193], [886, 194], [886, 195], [886, 196], [886, 197], [886, 198], [886, 199], [886, 200], [886, 201], [886, 202], [886, 203], [886, 204], [886, 205], [886, 206], [886, 207], [886, 208], [886, 209], [886, 210], [886, 212], [886, 213], [886, 214], [886, 215], [886, 216], [886, 217], [886, 218], [886, 219], [886, 220], [886, 221], [886, 222], [886, 223], [886, 224], [886, 225], [886, 226], [886, 227], [886, 228], [886, 229], [886, 230], [886, 231], [886, 232], [886, 233], [886, 234], [886, 235], [886, 236], [886, 237], [886, 238], [886, 239], [886, 240], [886, 241], [886, 242], [886, 243], [886, 244], [886, 245], [886, 246], [886, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[890], [891], [892], [893], [894], [895], [896], [897], [898], [899], [900], [901], [902], [903], [904], [905], [906], [907], [908], [909], [910], [911], [912], [913], [914], [915], [916], [917], [918], [919], [920], [921], [922], [923], [924], [925], [926, 1], [926, 2], [926, 3], [926, 4], [926, 5], [926, 6], [926, 7], [926, 8], [926, 9], [926, 11], [926, 12], [926, 13], [926, 14], [926, 15], [926, 16], [926, 17], [926, 18], [926, 19], [926, 20], [926, 21], [926, 22], [926, 23], [926, 24], [926, 25], [926, 26], [926, 27], [926, 28], [926, 29], [926, 30], [926, 31], [926, 32], [926, 33], [926, 34], [926, 35], [926, 36], [926, 37], [926, 38], [926, 39], [926, 40], [926, 41], [926, 42], [926, 43], [926, 44], [926, 45], [926, 46], [926, 48], [926, 49], [926, 50], [926, 51], [926, 52], [926, 53], [926, 54], [926, 55], [926, 56], [926, 57], [926, 58], [926, 59], [926, 60], [926, 61], [926, 62], [926, 63], [926, 64], [926, 65], [926, 66], [926, 67], [926, 68], [926, 69], [926, 70], [926, 71], [926, 72], [926, 73], [926, 74], [926, 75], [926, 76], [926, 78], [926, 79], [926, 80], [926, 81], [926, 82], [926, 83], [926, 84], [926, 85], [926, 86], [926, 87], [926, 88], [926, 89], [926, 90], [926, 91], [926, 92], [926, 93], [926, 94], [926, 95], [926, 96], [926, 97], [926, 98], [926, 99], [926, 100], [926, 101], [926, 102], [926, 103], [926, 104], [926, 105], [926, 106], [926, 107], [926, 108], [926, 109], [926, 110], [926, 111], [926, 112], [926, 113], [926, 115], [926, 116], [926, 117], [926, 118], [926, 119], [926, 120], [926, 121], [926, 122], [926, 123], [926, 124], [926, 125], [926, 126], [926, 127], [926, 128], [926, 129], [926, 130], [926, 131], [926, 132], [926, 133], [926, 134], [926, 135], [926, 136], [926, 137], [926, 138], [926, 139], [926, 140], [926, 141], [926, 142], [926, 143], [926, 145], [926, 146], [926, 147], [926, 148], [926, 149], [926, 150], [926, 151], [926, 152], [926, 153], [926, 154], [926, 155], [926, 156], [926, 157], [926, 158], [926, 159], [926, 160], [926, 161], [926, 162], [926, 163], [926, 164], [926, 165], [926, 166], [926, 167], [926, 168], [926, 169], [926, 170], [926, 171], [926, 172], [926, 173], [926, 174], [926, 175], [926, 176], [926, 177], [926, 178], [926, 179], [926, 180], [926, 182], [926, 183], [926, 184], [926, 185], [926, 186], [926, 187], [926, 188], [926, 189], [926, 190], [926, 191], [926, 192], [926, 193], [926, 194], [926, 195], [926, 196], [926, 197], [926, 198], [926, 199], [926, 200], [926, 201], [926, 202], [926, 203], [926, 204], [926, 205], [926, 206], [926, 207], [926, 208], [926, 209], [926, 210], [926, 212], [926, 213], [926, 214], [926, 215], [926, 216], [926, 217], [926, 218], [926, 219], [926, 220], [926, 221], [926, 222], [926, 223], [926, 224], [926, 225], [926, 226], [926, 227], [926, 228], [926, 229], [926, 230], [926, 231], [926, 232], [926, 233], [926, 234], [926, 235], [926, 236], [926, 237], [926, 238], [926, 239], [926, 240], [926, 241], [926, 242], [926, 243], [926, 244], [926, 245], [926, 246], [926, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[930], [931], [932], [933], [934], [935], [936], [937], [938], [939], [940], [941], [942], [943], [944], [945], [946], [947], [948], [949], [950], [951], [952], [953], [954], [955], [956], [957], [958], [959], [960], [961], [962], [963], [964], [965], [966, 1], [966, 2], [966, 3], [966, 4], [966, 5], [966, 6], [966, 7], [966, 8], [966, 9], [966, 11], [966, 12], [966, 13], [966, 14], [966, 15], [966, 16], [966, 17], [966, 18], [966, 19], [966, 20], [966, 21], [966, 22], [966, 23], [966, 24], [966, 25], [966, 26], [966, 27], [966, 28], [966, 29], [966, 30], [966, 31], [966, 32], [966, 33], [966, 34], [966, 35], [966, 36], [966, 37], [966, 38], [966, 39], [966, 40], [966, 41], [966, 42], [966, 43], [966, 44], [966, 45], [966, 46], [966, 48], [966, 49], [966, 50], [966, 51], [966, 52], [966, 53], [966, 54], [966, 55], [966, 56], [966, 57], [966, 58], [966, 59], [966, 60], [966, 61], [966, 62], [966, 63], [966, 64], [966, 65], [966, 66], [966, 67], [966, 68], [966, 69], [966, 70], [966, 71], [966, 72], [966, 73], [966, 74], [966, 75], [966, 76], [966, 78], [966, 79], [966, 80], [966, 81], [966, 82], [966, 83], [966, 84], [966, 85], [966, 86], [966, 87], [966, 88], [966, 89], [966, 90], [966, 91], [966, 92], [966, 93], [966, 94], [966, 95], [966, 96], [966, 97], [966, 98], [966, 99], [966, 100], [966, 101], [966, 102], [966, 103], [966, 104], [966, 105], [966, 106], [966, 107], [966, 108], [966, 109], [966, 110], [966, 111], [966, 112], [966, 113], [966, 115], [966, 116], [966, 117], [966, 118], [966, 119], [966, 120], [966, 121], [966, 122], [966, 123], [966, 124], [966, 125], [966, 126], [966, 127], [966, 128], [966, 129], [966, 130], [966, 131], [966, 132], [966, 133], [966, 134], [966, 135], [966, 136], [966, 137], [966, 138], [966, 139], [966, 140], [966, 141], [966, 142], [966, 143], [966, 145], [966, 146], [966, 147], [966, 148], [966, 149], [966, 150], [966, 151], [966, 152], [966, 153], [966, 154], [966, 155], [966, 156], [966, 157], [966, 158], [966, 159], [966, 160], [966, 161], [966, 162], [966, 163], [966, 164], [966, 165], [966, 166], [966, 167], [966, 168], [966, 169], [966, 170], [966, 171], [966, 172], [966, 173], [966, 174], [966, 175], [966, 176], [966, 177], [966, 178], [966, 179], [966, 180], [966, 182], [966, 183], [966, 184], [966, 185], [966, 186], [966, 187], [966, 188], [966, 189], [966, 190], [966, 191], [966, 192], [966, 193], [966, 194], [966, 195], [966, 196], [966, 197], [966, 198], [966, 199], [966, 200], [966, 201], [966, 202], [966, 203], [966, 204], [966, 205], [966, 206], [966, 207], [966, 208], [966, 209], [966, 210], [966, 212], [966, 213], [966, 214], [966, 215], [966, 216], [966, 217], [966, 218], [966, 219], [966, 220], [966, 221], [966, 222], [966, 223], [966, 224], [966, 225], [966, 226], [966, 227], [966, 228], [966, 229], [966, 230], [966, 231], [966, 232], [966, 233], [966, 234], [966, 235], [966, 236], [966, 237], [966, 238], [966, 239], [966, 240], [966, 241], [966, 242], [966, 243], [966, 244], [966, 245], [966, 246], [966, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[970], [971], [972], [973], [974], [975], [976], [977], [978], [979], [980], [981], [982], [983], [984], [985], [986], [987], [988], [989], [990], [991], [992], [993], [994], [995], [996], [997], [998], [999], [1000], [1001], [1002], [1003], [1004], [1005], [1006, 1], [1006, 2], [1006, 3], [1006, 4], [1006, 5], [1006, 6], [1006, 7], [1006, 8], [1006, 9], [1006, 11], [1006, 12], [1006, 13], [1006, 14], [1006, 15], [1006, 16], [1006, 17], [1006, 18], [1006, 19], [1006, 20], [1006, 21], [1006, 22], [1006, 23], [1006, 24], [1006, 25], [1006, 26], [1006, 27], [1006, 28], [1006, 29], [1006, 30], [1006, 31], [1006, 32], [1006, 33], [1006, 34], [1006, 35], [1006, 36], [1006, 37], [1006, 38], [1006, 39], [1006, 40], [1006, 41], [1006, 42], [1006, 43], [1006, 44], [1006, 45], [1006, 46], [1006, 48], [1006, 49], [1006, 50], [1006, 51], [1006, 52], [1006, 53], [1006, 54], [1006, 55], [1006, 56], [1006, 57], [1006, 58], [1006, 59], [1006, 60], [1006, 61], [1006, 62], [1006, 63], [1006, 64], [1006, 65], [1006, 66], [1006, 67], [1006, 68], [1006, 69], [1006, 70], [1006, 71], [1006, 72], [1006, 73], [1006, 74], [1006, 75], [1006, 76], [1006, 78], [1006, 79], [1006, 80], [1006, 81], [1006, 82], [1006, 83], [1006, 84], [1006, 85], [1006, 86], [1006, 87], [1006, 88], [1006, 89], [1006, 90], [1006, 91], [1006, 92], [1006, 93], [1006, 94], [1006, 95], [1006, 96], [1006, 97], [1006, 98], [1006, 99], [1006, 100], [1006, 101], [1006, 102], [1006, 103], [1006, 104], [1006, 105], [1006, 106], [1006, 107], [1006, 108], [1006, 109], [1006, 110], [1006, 111], [1006, 112], [1006, 113], [1006, 115], [1006, 116], [1006, 117], [1006, 118], [1006, 119], [1006, 120], [1006, 121], [1006, 122], [1006, 123], [1006, 124], [1006, 125], [1006, 126], [1006, 127], [1006, 128], [1006, 129], [1006, 130], [1006, 131], [1006, 132], [1006, 133], [1006, 134], [1006, 135], [1006, 136], [1006, 137], [1006, 138], [1006, 139], [1006, 140], [1006, 141], [1006, 142], [1006, 143], [1006, 145], [1006, 146], [1006, 147], [1006, 148], [1006, 149], [1006, 150], [1006, 151], [1006, 152], [1006, 153], [1006, 154], [1006, 155], [1006, 156], [1006, 157], [1006, 158], [1006, 159], [1006, 160], [1006, 161], [1006, 162], [1006, 163], [1006, 164], [1006, 165], [1006, 166], [1006, 167], [1006, 168], [1006, 169], [1006, 170], [1006, 171], [1006, 172], [1006, 173], [1006, 174], [1006, 175], [1006, 176], [1006, 177], [1006, 178], [1006, 179], [1006, 180], [1006, 182], [1006, 183], [1006, 184], [1006, 185], [1006, 186], [1006, 187], [1006, 188], [1006, 189], [1006, 190], [1006, 191], [1006, 192], [1006, 193], [1006, 194], [1006, 195], [1006, 196], [1006, 197], [1006, 198], [1006, 199], [1006, 200], [1006, 201], [1006, 202], [1006, 203], [1006, 204], [1006, 205], [1006, 206], [1006, 207], [1006, 208], [1006, 209], [1006, 210], [1006, 212], [1006, 213], [1006, 214], [1006, 215], [1006, 216], [1006, 217], [1006, 218], [1006, 219], [1006, 220], [1006, 221], [1006, 222], [1006, 223], [1006, 224], [1006, 225], [1006, 226], [1006, 227], [1006, 228], [1006, 229], [1006, 230], [1006, 231], [1006, 232], [1006, 233], [1006, 234], [1006, 235], [1006, 236], [1006, 237], [1006, 238], [1006, 239], [1006, 240], [1006, 241], [1006, 242], [1006, 243], [1006, 244], [1006, 245], [1006, 246], [1006, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[1010], [1011], [1012], [1013], [1014], [1015], [1016], [1017], [1018], [1019], [1020], [1021], [1022], [1023], [1024], [1025], [1026], [1027], [1028], [1029], [1030], [1031], [1032], [1033], [1034], [1035], [1036], [1037], [1038], [1039], [1040], [1041], [1042], [1043], [1044], [1045], [1046, 1], [1046, 2], [1046, 3], [1046, 4], [1046, 5], [1046, 6], [1046, 7], [1046, 8], [1046, 9], [1046, 11], [1046, 12], [1046, 13], [1046, 14], [1046, 15], [1046, 16], [1046, 17], [1046, 18], [1046, 19], [1046, 20], [1046, 21], [1046, 22], [1046, 23], [1046, 24], [1046, 25], [1046, 26], [1046, 27], [1046, 28], [1046, 29], [1046, 30], [1046, 31], [1046, 32], [1046, 33], [1046, 34], [1046, 35], [1046, 36], [1046, 37], [1046, 38], [1046, 39], [1046, 40], [1046, 41], [1046, 42], [1046, 43], [1046, 44], [1046, 45], [1046, 46], [1046, 48], [1046, 49], [1046, 50], [1046, 51], [1046, 52], [1046, 53], [1046, 54], [1046, 55], [1046, 56], [1046, 57], [1046, 58], [1046, 59], [1046, 60], [1046, 61], [1046, 62], [1046, 63], [1046, 64], [1046, 65], [1046, 66], [1046, 67], [1046, 68], [1046, 69], [1046, 70], [1046, 71], [1046, 72], [1046, 73], [1046, 74], [1046, 75], [1046, 76], [1046, 78], [1046, 79], [1046, 80], [1046, 81], [1046, 82], [1046, 83], [1046, 84], [1046, 85], [1046, 86], [1046, 87], [1046, 88], [1046, 89], [1046, 90], [1046, 91], [1046, 92], [1046, 93], [1046, 94], [1046, 95], [1046, 96], [1046, 97], [1046, 98], [1046, 99], [1046, 100], [1046, 101], [1046, 102], [1046, 103], [1046, 104], [1046, 105], [1046, 106], [1046, 107], [1046, 108], [1046, 109], [1046, 110], [1046, 111], [1046, 112], [1046, 113], [1046, 115], [1046, 116], [1046, 117], [1046, 118], [1046, 119], [1046, 120], [1046, 121], [1046, 122], [1046, 123], [1046, 124], [1046, 125], [1046, 126], [1046, 127], [1046, 128], [1046, 129], [1046, 130], [1046, 131], [1046, 132], [1046, 133], [1046, 134], [1046, 135], [1046, 136], [1046, 137], [1046, 138], [1046, 139], [1046, 140], [1046, 141], [1046, 142], [1046, 143], [1046, 145], [1046, 146], [1046, 147], [1046, 148], [1046, 149], [1046, 150], [1046, 151], [1046, 152], [1046, 153], [1046, 154], [1046, 155], [1046, 156], [1046, 157], [1046, 158], [1046, 159], [1046, 160], [1046, 161], [1046, 162], [1046, 163], [1046, 164], [1046, 165], [1046, 166], [1046, 167], [1046, 168], [1046, 169], [1046, 170], [1046, 171], [1046, 172], [1046, 173], [1046, 174], [1046, 175], [1046, 176], [1046, 177], [1046, 178], [1046, 179], [1046, 180], [1046, 182], [1046, 183], [1046, 184], [1046, 185], [1046, 186], [1046, 187], [1046, 188], [1046, 189], [1046, 190], [1046, 191], [1046, 192], [1046, 193], [1046, 194], [1046, 195], [1046, 196], [1046, 197], [1046, 198], [1046, 199], [1046, 200], [1046, 201], [1046, 202], [1046, 203], [1046, 204], [1046, 205], [1046, 206], [1046, 207], [1046, 208], [1046, 209], [1046, 210], [1046, 212], [1046, 213], [1046, 214], [1046, 215], [1046, 216], [1046, 217], [1046, 218], [1046, 219], [1046, 220], [1046, 221], [1046, 222], [1046, 223], [1046, 224], [1046, 225], [1046, 226], [1046, 227], [1046, 228], [1046, 229], [1046, 230], [1046, 231], [1046, 232], [1046, 233], [1046, 234], [1046, 235], [1046, 236], [1046, 237], [1046, 238], [1046, 239], [1046, 240], [1046, 241], [1046, 242], [1046, 243], [1046, 244], [1046, 245], [1046, 246], [1046, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=73, paths=[[1048], [1049], [1050], [1051], [1052], [1053], [1054], [1055], [1056], [1057], [1058], [1059], [1060], [1061], [1062], [1063], [1064], [1065], [1066], [1067], [1068], [1069], [1070], [1071], [1072], [1073], [1074], [1075], [1076, 1], [1076, 2], [1076, 3], [1076, 4], [1076, 5], [1076, 6], [1076, 7], [1076, 8], [1076, 9], [1076, 11], [1076, 12], [1076, 13], [1076, 14], [1076, 15], [1076, 16], [1076, 17], [1076, 18], [1076, 19], [1076, 20], [1076, 21], [1076, 22], [1076, 23], [1076, 24], [1076, 25], [1076, 26], [1076, 27], [1076, 28], [1076, 29], [1076, 30], [1076, 31], [1076, 32], [1076, 33], [1076, 34], [1076, 35], [1076, 36], [1076, 37], [1076, 38], [1076, 39], [1076, 40], [1076, 41], [1076, 42], [1076, 43], [1076, 44], [1076, 45], [1076, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=73, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=111, paths=[[1078], [1079], [1080], [1081], [1082], [1083], [1084], [1085], [1086], [1087], [1088], [1089], [1090], [1091], [1092], [1093], [1094], [1095], [1096], [1097], [1098], [1099], [1100], [1101], [1102], [1103], [1104], [1105], [1106], [1107], [1108], [1109], [1110], [1112], [1113], [1114], [1115], [1116], [1117], [1118], [1119], [1120], [1121], [1122], [1123], [1124], [1125], [1126], [1127], [1128], [1129], [1130], [1131], [1132], [1133], [1134], [1135], [1136], [1137], [1138], [1139], [1140], [1141], [1142], [1143], [1144], [1145, 1], [1145, 2], [1145, 3], [1145, 4], [1145, 5], [1145, 6], [1145, 7], [1145, 8], [1145, 9], [1145, 11], [1145, 12], [1145, 13], [1145, 14], [1145, 15], [1145, 16], [1145, 17], [1145, 18], [1145, 19], [1145, 20], [1145, 21], [1145, 22], [1145, 23], [1145, 24], [1145, 25], [1145, 26], [1145, 27], [1145, 28], [1145, 29], [1145, 30], [1145, 31], [1145, 32], [1145, 33], [1145, 34], [1145, 35], [1145, 36], [1145, 37], [1145, 38], [1145, 39], [1145, 40], [1145, 41], [1145, 42], [1145, 43], [1145, 44], [1145, 45], [1145, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=111, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=45, paths=[[1146, 1], [1146, 2], [1146, 3], [1146, 4], [1146, 5], [1146, 6], [1146, 7], [1146, 8], [1146, 9], [1146, 11], [1146, 12], [1146, 13], [1146, 14], [1146, 15], [1146, 16], [1146, 17], [1146, 18], [1146, 19], [1146, 20], [1146, 21], [1146, 22], [1146, 23], [1146, 24], [1146, 25], [1146, 26], [1146, 27], [1146, 28], [1146, 29], [1146, 30], [1146, 31], [1146, 32], [1146, 33], [1146, 34], [1146, 35], [1146, 36], [1146, 37], [1146, 38], [1146, 39], [1146, 40], [1146, 41], [1146, 42], [1146, 43], [1146, 44], [1146, 45], [1146, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=45, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=81, paths=[[1150], [1151], [1152], [1153], [1154], [1155], [1156], [1157], [1158], [1159], [1160], [1161], [1162], [1163], [1164], [1165], [1166], [1167], [1168], [1169], [1170], [1171], [1172], [1173], [1174], [1175], [1176], [1177], [1178], [1179], [1180], [1181], [1182], [1183], [1184], [1185], [1186, 1], [1186, 2], [1186, 3], [1186, 4], [1186, 5], [1186, 6], [1186, 7], [1186, 8], [1186, 9], [1186, 11], [1186, 12], [1186, 13], [1186, 14], [1186, 15], [1186, 16], [1186, 17], [1186, 18], [1186, 19], [1186, 20], [1186, 21], [1186, 22], [1186, 23], [1186, 24], [1186, 25], [1186, 26], [1186, 27], [1186, 28], [1186, 29], [1186, 30], [1186, 31], [1186, 32], [1186, 33], [1186, 34], [1186, 35], [1186, 36], [1186, 37], [1186, 38], [1186, 39], [1186, 40], [1186, 41], [1186, 42], [1186, 43], [1186, 44], [1186, 45], [1186, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=81, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=495, paths=[[1196], [1197], [1198], [1199], [1200], [1201], [1202], [1203], [1204], [1205], [1206], [1207], [1208], [1209], [1210], [1211], [1212], [1213], [1214], [1215], [1216], [1217], [1218], [1219], [1220], [1221], [1222], [1223], [1224], [1225], [1226], [1227], [1228], [1229], [1230], [1231], [1233], [1234], [1235], [1236], [1237], [1238], [1239], [1240], [1241], [1242], [1243], [1244], [1245], [1246], [1247], [1248], [1249], [1250], [1251], [1252], [1253], [1254], [1255], [1256], [1257], [1258], [1259], [1260], [1261], [1262], [1263], [1264], [1265], [1266], [1267], [1268], [1270], [1271], [1272], [1273], [1274], [1275], [1276], [1277], [1278], [1279], [1280], [1281], [1282], [1283], [1284], [1285], [1286], [1287], [1288], [1289], [1290], [1291], [1292], [1293], [1294], [1295], [1296], [1297], [1298], [1299], [1300], [1301], [1302], [1303], [1304], [1305], [1307], [1308], [1309], [1310], [1311], [1312], [1313], [1314], [1315], [1316], [1317], [1318], [1319], [1320], [1321], [1322], [1323], [1324], [1325], [1326], [1327], [1328], [1329], [1330], [1331], [1332], [1333], [1334], [1335], [1336], [1337], [1338], [1339], [1340], [1341], [1342], [1344], [1345], [1346], [1347], [1348], [1349], [1350], [1351], [1352], [1353], [1354], [1355], [1356], [1357], [1358], [1359], [1360], [1361], [1362], [1363], [1364], [1365], [1366], [1367], [1368], [1369], [1370], [1371], [1372], [1373], [1374], [1375], [1376], [1377], [1378], [1379], [1381], [1382], [1383], [1384], [1385], [1386], [1387], [1388], [1389], [1390], [1391], [1392], [1393], [1394], [1395], [1396], [1397], [1398], [1399], [1400], [1401], [1402], [1403], [1404], [1405], [1406], [1407], [1408], [1409], [1410], [1411], [1412], [1413], [1414], [1415], [1416], [1418], [1419], [1420], [1421], [1422], [1423], [1424], [1425], [1426], [1427], [1428], [1429], [1430], [1431], [1432], [1433], [1434], [1435], [1436], [1437], [1438], [1439], [1440], [1441], [1442], [1443], [1444], [1445], [1446], [1447], [1448], [1449], [1450], [1451], [1452], [1453], [1455], [1456], [1457], [1458], [1459], [1460], [1461], [1462], [1463], [1464], [1465], [1466], [1467], [1468], [1469], [1470], [1471], [1472], [1473], [1474], [1475], [1476], [1477], [1478], [1479], [1480], [1481], [1482], [1483], [1484], [1485], [1486], [1487], [1488], [1489], [1490], [1492], [1493], [1494], [1495], [1496], [1497], [1498], [1499], [1500], [1501], [1502], [1503], [1504], [1505], [1506], [1507], [1508], [1509], [1510], [1511], [1512], [1513], [1514], [1515], [1516], [1517], [1518], [1519], [1520], [1521], [1522], [1523], [1524], [1525], [1526], [1527], [1529], [1530], [1531], [1532], [1533], [1534], [1535], [1536], [1537], [1538], [1539], [1540], [1541], [1542], [1543], [1544], [1545], [1546], [1547], [1548], [1549], [1550], [1551], [1552], [1553], [1554], [1555], [1556], [1557], [1558], [1559], [1560], [1561], [1562], [1563], [1564], [1566], [1567], [1568], [1569], [1570], [1571], [1572], [1573], [1574], [1576], [1577], [1578], [1579], [1580], [1581], [1582], [1583], [1584], [1585], [1586], [1587], [1588], [1589], [1590], [1591], [1592], [1593], [1594], [1595], [1596], [1597], [1598], [1599], [1600], [1601], [1602], [1603], [1604], [1605], [1606], [1607], [1608], [1609], [1610], [1611], [1612, 1], [1612, 2], [1612, 3], [1612, 4], [1612, 5], [1612, 6], [1612, 7], [1612, 8], [1612, 9], [1612, 11], [1612, 12], [1612, 13], [1612, 14], [1612, 15], [1612, 16], [1612, 17], [1612, 18], [1612, 19], [1612, 20], [1612, 21], [1612, 22], [1612, 23], [1612, 24], [1612, 25], [1612, 26], [1612, 27], [1612, 28], [1612, 29], [1612, 30], [1612, 31], [1612, 32], [1612, 33], [1612, 34], [1612, 35], [1612, 36], [1612, 37], [1612, 38], [1612, 39], [1612, 40], [1612, 41], [1612, 42], [1612, 43], [1612, 44], [1612, 45], [1612, 46], [1612, 48], [1612, 49], [1612, 50], [1612, 51], [1612, 52], [1612, 53], [1612, 54], [1612, 55], [1612, 56], [1612, 58], [1612, 59], [1612, 60], [1612, 61], [1612, 62], [1612, 63], [1612, 64], [1612, 65], [1612, 66], [1612, 67], [1612, 68], [1612, 69], [1612, 70], [1612, 71], [1612, 72], [1612, 73], [1612, 74], [1612, 75], [1612, 76], [1612, 77], [1612, 78], [1612, 79], [1612, 80], [1612, 81], [1612, 82], [1612, 83], [1612, 84], [1612, 85], [1612, 86], [1612, 87], [1612, 88], [1612, 89], [1612, 90], [1612, 91], [1612, 92], [1612, 93]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=483, two_qubit=12), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[1616], [1617], [1618], [1619], [1620], [1621], [1622], [1623], [1624], [1625], [1626], [1627], [1628], [1629], [1630], [1631], [1632], [1633], [1634], [1635], [1636], [1637], [1638], [1639], [1640], [1641], [1642], [1643], [1644], [1645], [1646], [1647], [1648], [1649], [1650], [1651], [1652, 1], [1652, 2], [1652, 3], [1652, 4], [1652, 5], [1652, 6], [1652, 7], [1652, 8], [1652, 9], [1652, 11], [1652, 12], [1652, 13], [1652, 14], [1652, 15], [1652, 16], [1652, 17], [1652, 18], [1652, 19], [1652, 20], [1652, 21], [1652, 22], [1652, 23], [1652, 24], [1652, 25], [1652, 26], [1652, 27], [1652, 28], [1652, 29], [1652, 30], [1652, 31], [1652, 32], [1652, 33], [1652, 34], [1652, 35], [1652, 36], [1652, 37], [1652, 38], [1652, 39], [1652, 40], [1652, 41], [1652, 42], [1652, 43], [1652, 44], [1652, 45], [1652, 46], [1652, 48], [1652, 49], [1652, 50], [1652, 51], [1652, 52], [1652, 53], [1652, 54], [1652, 55], [1652, 56], [1652, 57], [1652, 58], [1652, 59], [1652, 60], [1652, 61], [1652, 62], [1652, 63], [1652, 64], [1652, 65], [1652, 66], [1652, 67], [1652, 68], [1652, 69], [1652, 70], [1652, 71], [1652, 72], [1652, 73], [1652, 74], [1652, 75], [1652, 76], [1652, 78], [1652, 79], [1652, 80], [1652, 81], [1652, 82], [1652, 83], [1652, 84], [1652, 85], [1652, 86], [1652, 87], [1652, 88], [1652, 89], [1652, 90], [1652, 91], [1652, 92], [1652, 93], [1652, 94], [1652, 95], [1652, 96], [1652, 97], [1652, 98], [1652, 99], [1652, 100], [1652, 101], [1652, 102], [1652, 103], [1652, 104], [1652, 105], [1652, 106], [1652, 107], [1652, 108], [1652, 109], [1652, 110], [1652, 111], [1652, 112], [1652, 113], [1652, 115], [1652, 116], [1652, 117], [1652, 118], [1652, 119], [1652, 120], [1652, 121], [1652, 122], [1652, 123], [1652, 124], [1652, 125], [1652, 126], [1652, 127], [1652, 128], [1652, 129], [1652, 130], [1652, 131], [1652, 132], [1652, 133], [1652, 134], [1652, 135], [1652, 136], [1652, 137], [1652, 138], [1652, 139], [1652, 140], [1652, 141], [1652, 142], [1652, 143], [1652, 145], [1652, 146], [1652, 147], [1652, 148], [1652, 149], [1652, 150], [1652, 151], [1652, 152], [1652, 153], [1652, 154], [1652, 155], [1652, 156], [1652, 157], [1652, 158], [1652, 159], [1652, 160], [1652, 161], [1652, 162], [1652, 163], [1652, 164], [1652, 165], [1652, 166], [1652, 167], [1652, 168], [1652, 169], [1652, 170], [1652, 171], [1652, 172], [1652, 173], [1652, 174], [1652, 175], [1652, 176], [1652, 177], [1652, 178], [1652, 179], [1652, 180], [1652, 182], [1652, 183], [1652, 184], [1652, 185], [1652, 186], [1652, 187], [1652, 188], [1652, 189], [1652, 190], [1652, 191], [1652, 192], [1652, 193], [1652, 194], [1652, 195], [1652, 196], [1652, 197], [1652, 198], [1652, 199], [1652, 200], [1652, 201], [1652, 202], [1652, 203], [1652, 204], [1652, 205], [1652, 206], [1652, 207], [1652, 208], [1652, 209], [1652, 210], [1652, 212], [1652, 213], [1652, 214], [1652, 215], [1652, 216], [1652, 217], [1652, 218], [1652, 219], [1652, 220], [1652, 221], [1652, 222], [1652, 223], [1652, 224], [1652, 225], [1652, 226], [1652, 227], [1652, 228], [1652, 229], [1652, 230], [1652, 231], [1652, 232], [1652, 233], [1652, 234], [1652, 235], [1652, 236], [1652, 237], [1652, 238], [1652, 239], [1652, 240], [1652, 241], [1652, 242], [1652, 243], [1652, 244], [1652, 245], [1652, 246], [1652, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[1656], [1657], [1658], [1659], [1660], [1661], [1662], [1663], [1664], [1665], [1666], [1667], [1668], [1669], [1670], [1671], [1672], [1673], [1674], [1675], [1676], [1677], [1678], [1679], [1680], [1681], [1682], [1683], [1684], [1685], [1686], [1687], [1688], [1689], [1690], [1691], [1692, 1], [1692, 2], [1692, 3], [1692, 4], [1692, 5], [1692, 6], [1692, 7], [1692, 8], [1692, 9], [1692, 11], [1692, 12], [1692, 13], [1692, 14], [1692, 15], [1692, 16], [1692, 17], [1692, 18], [1692, 19], [1692, 20], [1692, 21], [1692, 22], [1692, 23], [1692, 24], [1692, 25], [1692, 26], [1692, 27], [1692, 28], [1692, 29], [1692, 30], [1692, 31], [1692, 32], [1692, 33], [1692, 34], [1692, 35], [1692, 36], [1692, 37], [1692, 38], [1692, 39], [1692, 40], [1692, 41], [1692, 42], [1692, 43], [1692, 44], [1692, 45], [1692, 46], [1692, 48], [1692, 49], [1692, 50], [1692, 51], [1692, 52], [1692, 53], [1692, 54], [1692, 55], [1692, 56], [1692, 57], [1692, 58], [1692, 59], [1692, 60], [1692, 61], [1692, 62], [1692, 63], [1692, 64], [1692, 65], [1692, 66], [1692, 67], [1692, 68], [1692, 69], [1692, 70], [1692, 71], [1692, 72], [1692, 73], [1692, 74], [1692, 75], [1692, 76], [1692, 78], [1692, 79], [1692, 80], [1692, 81], [1692, 82], [1692, 83], [1692, 84], [1692, 85], [1692, 86], [1692, 87], [1692, 88], [1692, 89], [1692, 90], [1692, 91], [1692, 92], [1692, 93], [1692, 94], [1692, 95], [1692, 96], [1692, 97], [1692, 98], [1692, 99], [1692, 100], [1692, 101], [1692, 102], [1692, 103], [1692, 104], [1692, 105], [1692, 106], [1692, 107], [1692, 108], [1692, 109], [1692, 110], [1692, 111], [1692, 112], [1692, 113], [1692, 115], [1692, 116], [1692, 117], [1692, 118], [1692, 119], [1692, 120], [1692, 121], [1692, 122], [1692, 123], [1692, 124], [1692, 125], [1692, 126], [1692, 127], [1692, 128], [1692, 129], [1692, 130], [1692, 131], [1692, 132], [1692, 133], [1692, 134], [1692, 135], [1692, 136], [1692, 137], [1692, 138], [1692, 139], [1692, 140], [1692, 141], [1692, 142], [1692, 143], [1692, 145], [1692, 146], [1692, 147], [1692, 148], [1692, 149], [1692, 150], [1692, 151], [1692, 152], [1692, 153], [1692, 154], [1692, 155], [1692, 156], [1692, 157], [1692, 158], [1692, 159], [1692, 160], [1692, 161], [1692, 162], [1692, 163], [1692, 164], [1692, 165], [1692, 166], [1692, 167], [1692, 168], [1692, 169], [1692, 170], [1692, 171], [1692, 172], [1692, 173], [1692, 174], [1692, 175], [1692, 176], [1692, 177], [1692, 178], [1692, 179], [1692, 180], [1692, 182], [1692, 183], [1692, 184], [1692, 185], [1692, 186], [1692, 187], [1692, 188], [1692, 189], [1692, 190], [1692, 191], [1692, 192], [1692, 193], [1692, 194], [1692, 195], [1692, 196], [1692, 197], [1692, 198], [1692, 199], [1692, 200], [1692, 201], [1692, 202], [1692, 203], [1692, 204], [1692, 205], [1692, 206], [1692, 207], [1692, 208], [1692, 209], [1692, 210], [1692, 212], [1692, 213], [1692, 214], [1692, 215], [1692, 216], [1692, 217], [1692, 218], [1692, 219], [1692, 220], [1692, 221], [1692, 222], [1692, 223], [1692, 224], [1692, 225], [1692, 226], [1692, 227], [1692, 228], [1692, 229], [1692, 230], [1692, 231], [1692, 232], [1692, 233], [1692, 234], [1692, 235], [1692, 236], [1692, 237], [1692, 238], [1692, 239], [1692, 240], [1692, 241], [1692, 242], [1692, 243], [1692, 244], [1692, 245], [1692, 246], [1692, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=275, paths=[[1696], [1697], [1698], [1699], [1700], [1701], [1702], [1703], [1704], [1705], [1706], [1707], [1708], [1709], [1710], [1711], [1712], [1713], [1714], [1715], [1716], [1717], [1718], [1719], [1720], [1721], [1722], [1723], [1724], [1725], [1726], [1727], [1728], [1729], [1730], [1731], [1732, 1], [1732, 2], [1732, 3], [1732, 4], [1732, 5], [1732, 6], [1732, 7], [1732, 8], [1732, 9], [1732, 11], [1732, 12], [1732, 13], [1732, 14], [1732, 15], [1732, 16], [1732, 17], [1732, 18], [1732, 19], [1732, 20], [1732, 21], [1732, 22], [1732, 23], [1732, 24], [1732, 25], [1732, 26], [1732, 27], [1732, 28], [1732, 29], [1732, 30], [1732, 31], [1732, 32], [1732, 33], [1732, 34], [1732, 35], [1732, 36], [1732, 37], [1732, 38], [1732, 39], [1732, 40], [1732, 41], [1732, 42], [1732, 43], [1732, 44], [1732, 45], [1732, 46], [1732, 48], [1732, 49], [1732, 50], [1732, 51], [1732, 52], [1732, 53], [1732, 54], [1732, 55], [1732, 56], [1732, 57], [1732, 58], [1732, 59], [1732, 60], [1732, 61], [1732, 62], [1732, 63], [1732, 64], [1732, 65], [1732, 66], [1732, 67], [1732, 68], [1732, 69], [1732, 70], [1732, 71], [1732, 72], [1732, 73], [1732, 74], [1732, 75], [1732, 76], [1732, 78], [1732, 79], [1732, 80], [1732, 81], [1732, 82], [1732, 83], [1732, 84], [1732, 85], [1732, 86], [1732, 87], [1732, 88], [1732, 89], [1732, 90], [1732, 91], [1732, 92], [1732, 93], [1732, 94], [1732, 95], [1732, 96], [1732, 97], [1732, 98], [1732, 99], [1732, 100], [1732, 101], [1732, 102], [1732, 103], [1732, 104], [1732, 105], [1732, 106], [1732, 107], [1732, 108], [1732, 109], [1732, 110], [1732, 111], [1732, 112], [1732, 113], [1732, 115], [1732, 116], [1732, 118], [1732, 119], [1732, 120], [1732, 121], [1732, 122], [1732, 123], [1732, 124], [1732, 125], [1732, 126], [1732, 127], [1732, 128], [1732, 129], [1732, 130], [1732, 131], [1732, 132], [1732, 133], [1732, 134], [1732, 135], [1732, 136], [1732, 137], [1732, 138], [1732, 139], [1732, 140], [1732, 141], [1732, 142], [1732, 143], [1732, 145], [1732, 146], [1732, 147], [1732, 148], [1732, 149], [1732, 150], [1732, 151], [1732, 152], [1732, 153], [1732, 154], [1732, 155], [1732, 156], [1732, 157], [1732, 158], [1732, 159], [1732, 160], [1732, 161], [1732, 162], [1732, 163], [1732, 164], [1732, 165], [1732, 166], [1732, 167], [1732, 168], [1732, 169], [1732, 170], [1732, 171], [1732, 172], [1732, 173], [1732, 174], [1732, 175], [1732, 176], [1732, 177], [1732, 178], [1732, 179], [1732, 180], [1732, 182], [1732, 183], [1732, 184], [1732, 185], [1732, 186], [1732, 187], [1732, 188], [1732, 189], [1732, 190], [1732, 191], [1732, 192], [1732, 193], [1732, 194], [1732, 195], [1732, 196], [1732, 197], [1732, 198], [1732, 199], [1732, 200], [1732, 201], [1732, 202], [1732, 203], [1732, 204], [1732, 205], [1732, 206], [1732, 207], [1732, 208], [1732, 209], [1732, 210], [1732, 212], [1732, 213], [1732, 214], [1732, 215], [1732, 216], [1732, 217], [1732, 218], [1732, 219], [1732, 220], [1732, 221], [1732, 222], [1732, 223], [1732, 224], [1732, 225], [1732, 226], [1732, 227], [1732, 228], [1732, 229], [1732, 230], [1732, 231], [1732, 232], [1732, 233], [1732, 234], [1732, 235], [1732, 236], [1732, 237], [1732, 238], [1732, 239], [1732, 240], [1732, 241], [1732, 242], [1732, 243], [1732, 244], [1732, 245], [1732, 246], [1732, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=1, paths=[[1732, 117]]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=275, paths=[[1736], [1737], [1738], [1739], [1740], [1741], [1742], [1743], [1744], [1745], [1746], [1747], [1748], [1749], [1750], [1751], [1752], [1753], [1754], [1755], [1756], [1757], [1758], [1759], [1760], [1761], [1762], [1763], [1764], [1765], [1766], [1767], [1768], [1769], [1770], [1771], [1772, 1], [1772, 2], [1772, 3], [1772, 4], [1772, 5], [1772, 6], [1772, 7], [1772, 8], [1772, 9], [1772, 11], [1772, 12], [1772, 13], [1772, 14], [1772, 15], [1772, 16], [1772, 17], [1772, 18], [1772, 19], [1772, 20], [1772, 21], [1772, 22], [1772, 23], [1772, 24], [1772, 25], [1772, 26], [1772, 27], [1772, 28], [1772, 29], [1772, 30], [1772, 31], [1772, 32], [1772, 33], [1772, 34], [1772, 35], [1772, 36], [1772, 37], [1772, 38], [1772, 39], [1772, 40], [1772, 41], [1772, 42], [1772, 43], [1772, 44], [1772, 45], [1772, 46], [1772, 48], [1772, 49], [1772, 50], [1772, 51], [1772, 52], [1772, 53], [1772, 54], [1772, 55], [1772, 56], [1772, 57], [1772, 58], [1772, 59], [1772, 60], [1772, 61], [1772, 62], [1772, 63], [1772, 64], [1772, 65], [1772, 66], [1772, 67], [1772, 68], [1772, 69], [1772, 70], [1772, 71], [1772, 72], [1772, 73], [1772, 74], [1772, 75], [1772, 76], [1772, 78], [1772, 79], [1772, 80], [1772, 81], [1772, 82], [1772, 83], [1772, 84], [1772, 85], [1772, 86], [1772, 87], [1772, 88], [1772, 89], [1772, 90], [1772, 91], [1772, 92], [1772, 93], [1772, 94], [1772, 95], [1772, 96], [1772, 97], [1772, 98], [1772, 99], [1772, 100], [1772, 101], [1772, 102], [1772, 103], [1772, 104], [1772, 105], [1772, 106], [1772, 107], [1772, 108], [1772, 109], [1772, 110], [1772, 111], [1772, 112], [1772, 113], [1772, 115], [1772, 116], [1772, 117], [1772, 118], [1772, 119], [1772, 120], [1772, 121], [1772, 122], [1772, 123], [1772, 124], [1772, 125], [1772, 126], [1772, 127], [1772, 128], [1772, 129], [1772, 130], [1772, 131], [1772, 132], [1772, 133], [1772, 134], [1772, 135], [1772, 136], [1772, 137], [1772, 138], [1772, 139], [1772, 140], [1772, 141], [1772, 142], [1772, 143], [1772, 145], [1772, 146], [1772, 147], [1772, 148], [1772, 149], [1772, 150], [1772, 152], [1772, 153], [1772, 154], [1772, 155], [1772, 156], [1772, 157], [1772, 158], [1772, 159], [1772, 160], [1772, 161], [1772, 162], [1772, 163], [1772, 164], [1772, 165], [1772, 166], [1772, 167], [1772, 168], [1772, 169], [1772, 170], [1772, 171], [1772, 172], [1772, 173], [1772, 174], [1772, 175], [1772, 176], [1772, 177], [1772, 178], [1772, 179], [1772, 180], [1772, 182], [1772, 183], [1772, 184], [1772, 185], [1772, 186], [1772, 187], [1772, 188], [1772, 189], [1772, 190], [1772, 191], [1772, 192], [1772, 193], [1772, 194], [1772, 195], [1772, 196], [1772, 197], [1772, 198], [1772, 199], [1772, 200], [1772, 201], [1772, 202], [1772, 203], [1772, 204], [1772, 205], [1772, 206], [1772, 207], [1772, 208], [1772, 209], [1772, 210], [1772, 212], [1772, 213], [1772, 214], [1772, 215], [1772, 216], [1772, 217], [1772, 218], [1772, 219], [1772, 220], [1772, 221], [1772, 222], [1772, 223], [1772, 224], [1772, 225], [1772, 226], [1772, 227], [1772, 228], [1772, 229], [1772, 230], [1772, 231], [1772, 232], [1772, 233], [1772, 234], [1772, 235], [1772, 236], [1772, 237], [1772, 238], [1772, 239], [1772, 240], [1772, 241], [1772, 242], [1772, 243], [1772, 244], [1772, 245], [1772, 246], [1772, 247]]), x_errors=NoisyOperationsCount(count=1, paths=[[1772, 151]]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[1776], [1777], [1778], [1779], [1780], [1781], [1782], [1783], [1784], [1785], [1786], [1787], [1788], [1789], [1790], [1791], [1792], [1793], [1794], [1795], [1796], [1797], [1798], [1799], [1800], [1801], [1802], [1803], [1804], [1805], [1806], [1807], [1808], [1809], [1810], [1811], [1812, 1], [1812, 2], [1812, 3], [1812, 4], [1812, 5], [1812, 6], [1812, 7], [1812, 8], [1812, 9], [1812, 11], [1812, 12], [1812, 13], [1812, 14], [1812, 15], [1812, 16], [1812, 17], [1812, 18], [1812, 19], [1812, 20], [1812, 21], [1812, 22], [1812, 23], [1812, 24], [1812, 25], [1812, 26], [1812, 27], [1812, 28], [1812, 29], [1812, 30], [1812, 31], [1812, 32], [1812, 33], [1812, 34], [1812, 35], [1812, 36], [1812, 37], [1812, 38], [1812, 39], [1812, 40], [1812, 41], [1812, 42], [1812, 43], [1812, 44], [1812, 45], [1812, 46], [1812, 48], [1812, 49], [1812, 50], [1812, 51], [1812, 52], [1812, 53], [1812, 54], [1812, 55], [1812, 56], [1812, 57], [1812, 58], [1812, 59], [1812, 60], [1812, 61], [1812, 62], [1812, 63], [1812, 64], [1812, 65], [1812, 66], [1812, 67], [1812, 68], [1812, 69], [1812, 70], [1812, 71], [1812, 72], [1812, 73], [1812, 74], [1812, 75], [1812, 76], [1812, 78], [1812, 79], [1812, 80], [1812, 81], [1812, 82], [1812, 83], [1812, 84], [1812, 85], [1812, 86], [1812, 87], [1812, 88], [1812, 89], [1812, 90], [1812, 91], [1812, 92], [1812, 93], [1812, 94], [1812, 95], [1812, 96], [1812, 97], [1812, 98], [1812, 99], [1812, 100], [1812, 101], [1812, 102], [1812, 103], [1812, 104], [1812, 105], [1812, 106], [1812, 107], [1812, 108], [1812, 109], [1812, 110], [1812, 111], [1812, 112], [1812, 113], [1812, 115], [1812, 116], [1812, 117], [1812, 118], [1812, 119], [1812, 120], [1812, 121], [1812, 122], [1812, 123], [1812, 124], [1812, 125], [1812, 126], [1812, 127], [1812, 128], [1812, 129], [1812, 130], [1812, 131], [1812, 132], [1812, 133], [1812, 134], [1812, 135], [1812, 136], [1812, 137], [1812, 138], [1812, 139], [1812, 140], [1812, 141], [1812, 142], [1812, 143], [1812, 145], [1812, 146], [1812, 147], [1812, 148], [1812, 149], [1812, 150], [1812, 151], [1812, 152], [1812, 153], [1812, 154], [1812, 155], [1812, 156], [1812, 157], [1812, 158], [1812, 159], [1812, 160], [1812, 161], [1812, 162], [1812, 163], [1812, 164], [1812, 165], [1812, 166], [1812, 167], [1812, 168], [1812, 169], [1812, 170], [1812, 171], [1812, 172], [1812, 173], [1812, 174], [1812, 175], [1812, 176], [1812, 177], [1812, 178], [1812, 179], [1812, 180], [1812, 182], [1812, 183], [1812, 184], [1812, 185], [1812, 186], [1812, 187], [1812, 188], [1812, 189], [1812, 190], [1812, 191], [1812, 192], [1812, 193], [1812, 194], [1812, 195], [1812, 196], [1812, 197], [1812, 198], [1812, 199], [1812, 200], [1812, 201], [1812, 202], [1812, 203], [1812, 204], [1812, 205], [1812, 206], [1812, 207], [1812, 208], [1812, 209], [1812, 210], [1812, 212], [1812, 213], [1812, 214], [1812, 215], [1812, 216], [1812, 217], [1812, 218], [1812, 219], [1812, 220], [1812, 221], [1812, 222], [1812, 223], [1812, 224], [1812, 225], [1812, 226], [1812, 227], [1812, 228], [1812, 229], [1812, 230], [1812, 231], [1812, 232], [1812, 233], [1812, 234], [1812, 235], [1812, 236], [1812, 237], [1812, 238], [1812, 239], [1812, 240], [1812, 241], [1812, 242], [1812, 243], [1812, 244], [1812, 245], [1812, 246], [1812, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=276, paths=[[1816], [1817], [1818], [1819], [1820], [1821], [1822], [1823], [1824], [1825], [1826], [1827], [1828], [1829], [1830], [1831], [1832], [1833], [1834], [1835], [1836], [1837], [1838], [1839], [1840], [1841], [1842], [1843], [1844], [1845], [1846], [1847], [1848], [1849], [1850], [1851], [1852, 1], [1852, 2], [1852, 3], [1852, 4], [1852, 5], [1852, 6], [1852, 7], [1852, 8], [1852, 9], [1852, 11], [1852, 12], [1852, 13], [1852, 14], [1852, 15], [1852, 16], [1852, 17], [1852, 18], [1852, 19], [1852, 20], [1852, 21], [1852, 22], [1852, 23], [1852, 24], [1852, 25], [1852, 26], [1852, 27], [1852, 28], [1852, 29], [1852, 30], [1852, 31], [1852, 32], [1852, 33], [1852, 34], [1852, 35], [1852, 36], [1852, 37], [1852, 38], [1852, 39], [1852, 40], [1852, 41], [1852, 42], [1852, 43], [1852, 44], [1852, 45], [1852, 46], [1852, 48], [1852, 49], [1852, 50], [1852, 51], [1852, 52], [1852, 53], [1852, 54], [1852, 55], [1852, 56], [1852, 57], [1852, 58], [1852, 59], [1852, 60], [1852, 61], [1852, 62], [1852, 63], [1852, 64], [1852, 65], [1852, 66], [1852, 67], [1852, 68], [1852, 69], [1852, 70], [1852, 71], [1852, 72], [1852, 73], [1852, 74], [1852, 75], [1852, 76], [1852, 78], [1852, 79], [1852, 80], [1852, 81], [1852, 82], [1852, 83], [1852, 84], [1852, 85], [1852, 86], [1852, 87], [1852, 88], [1852, 89], [1852, 90], [1852, 91], [1852, 92], [1852, 93], [1852, 94], [1852, 95], [1852, 96], [1852, 97], [1852, 98], [1852, 99], [1852, 100], [1852, 101], [1852, 102], [1852, 103], [1852, 104], [1852, 105], [1852, 106], [1852, 107], [1852, 108], [1852, 109], [1852, 110], [1852, 111], [1852, 112], [1852, 113], [1852, 115], [1852, 116], [1852, 117], [1852, 118], [1852, 119], [1852, 120], [1852, 121], [1852, 122], [1852, 123], [1852, 124], [1852, 125], [1852, 126], [1852, 127], [1852, 128], [1852, 129], [1852, 130], [1852, 131], [1852, 132], [1852, 133], [1852, 134], [1852, 135], [1852, 136], [1852, 137], [1852, 138], [1852, 139], [1852, 140], [1852, 141], [1852, 142], [1852, 143], [1852, 145], [1852, 146], [1852, 147], [1852, 148], [1852, 149], [1852, 150], [1852, 151], [1852, 152], [1852, 153], [1852, 154], [1852, 155], [1852, 156], [1852, 157], [1852, 158], [1852, 159], [1852, 160], [1852, 161], [1852, 162], [1852, 163], [1852, 164], [1852, 165], [1852, 166], [1852, 167], [1852, 168], [1852, 169], [1852, 170], [1852, 171], [1852, 172], [1852, 173], [1852, 174], [1852, 175], [1852, 176], [1852, 177], [1852, 178], [1852, 179], [1852, 180], [1852, 182], [1852, 183], [1852, 184], [1852, 185], [1852, 186], [1852, 187], [1852, 188], [1852, 189], [1852, 190], [1852, 191], [1852, 192], [1852, 193], [1852, 194], [1852, 195], [1852, 196], [1852, 197], [1852, 198], [1852, 199], [1852, 200], [1852, 201], [1852, 202], [1852, 203], [1852, 204], [1852, 205], [1852, 206], [1852, 207], [1852, 208], [1852, 209], [1852, 210], [1852, 212], [1852, 213], [1852, 214], [1852, 215], [1852, 216], [1852, 217], [1852, 218], [1852, 219], [1852, 220], [1852, 221], [1852, 222], [1852, 223], [1852, 224], [1852, 225], [1852, 226], [1852, 227], [1852, 228], [1852, 229], [1852, 230], [1852, 231], [1852, 232], [1852, 233], [1852, 234], [1852, 235], [1852, 236], [1852, 237], [1852, 238], [1852, 239], [1852, 240], [1852, 241], [1852, 242], [1852, 243], [1852, 244], [1852, 245], [1852, 246], [1852, 247]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=270, two_qubit=6), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=73, paths=[[1854], [1855], [1856], [1857], [1858], [1859], [1860], [1861], [1862], [1863], [1864], [1865], [1866], [1867], [1868], [1869], [1870], [1871], [1872], [1873], [1874], [1875], [1876], [1877], [1878], [1879], [1880], [1881], [1882, 1], [1882, 2], [1882, 3], [1882, 4], [1882, 5], [1882, 6], [1882, 7], [1882, 8], [1882, 9], [1882, 11], [1882, 12], [1882, 13], [1882, 14], [1882, 15], [1882, 16], [1882, 17], [1882, 18], [1882, 19], [1882, 20], [1882, 21], [1882, 22], [1882, 23], [1882, 24], [1882, 25], [1882, 26], [1882, 27], [1882, 28], [1882, 29], [1882, 30], [1882, 31], [1882, 32], [1882, 33], [1882, 34], [1882, 35], [1882, 36], [1882, 37], [1882, 38], [1882, 39], [1882, 40], [1882, 41], [1882, 42], [1882, 43], [1882, 44], [1882, 45], [1882, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=73, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=111, paths=[[1884], [1885], [1886], [1887], [1888], [1889], [1890], [1891], [1892], [1893], [1894], [1895], [1896], [1897], [1898], [1899], [1900], [1901], [1902], [1903], [1904], [1905], [1906], [1907], [1908], [1909], [1910], [1911], [1912], [1913], [1914], [1915], [1916], [1918], [1919], [1920], [1921], [1922], [1923], [1924], [1925], [1926], [1927], [1928], [1929], [1930], [1931], [1932], [1933], [1934], [1935], [1936], [1937], [1938], [1939], [1940], [1941], [1942], [1943], [1944], [1945], [1946], [1947], [1948], [1949], [1950], [1951, 1], [1951, 2], [1951, 3], [1951, 4], [1951, 5], [1951, 6], [1951, 7], [1951, 8], [1951, 9], [1951, 11], [1951, 12], [1951, 13], [1951, 14], [1951, 15], [1951, 16], [1951, 17], [1951, 18], [1951, 19], [1951, 20], [1951, 21], [1951, 22], [1951, 23], [1951, 24], [1951, 25], [1951, 26], [1951, 27], [1951, 28], [1951, 29], [1951, 30], [1951, 31], [1951, 32], [1951, 33], [1951, 34], [1951, 35], [1951, 36], [1951, 37], [1951, 38], [1951, 39], [1951, 40], [1951, 41], [1951, 42], [1951, 43], [1951, 44], [1951, 45], [1951, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=111, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=45, paths=[[1952, 1], [1952, 2], [1952, 3], [1952, 4], [1952, 5], [1952, 6], [1952, 7], [1952, 8], [1952, 9], [1952, 11], [1952, 12], [1952, 13], [1952, 14], [1952, 15], [1952, 16], [1952, 17], [1952, 18], [1952, 19], [1952, 20], [1952, 21], [1952, 22], [1952, 23], [1952, 24], [1952, 25], [1952, 26], [1952, 27], [1952, 28], [1952, 29], [1952, 30], [1952, 31], [1952, 32], [1952, 33], [1952, 34], [1952, 35], [1952, 36], [1952, 37], [1952, 38], [1952, 39], [1952, 40], [1952, 41], [1952, 42], [1952, 43], [1952, 44], [1952, 45], [1952, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=45, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=73, paths=[[1953, 1], [1953, 2], [1953, 3], [1953, 4], [1953, 5], [1953, 6], [1953, 7], [1953, 8], [1953, 9], [1953, 10], [1953, 11], [1953, 12], [1953, 13], [1953, 14], [1953, 15], [1953, 16], [1953, 17], [1953, 18], [1953, 19], [1953, 20], [1953, 21], [1953, 22], [1953, 23], [1953, 24], [1953, 25], [1953, 26], [1953, 27], [1953, 28], [1953, 29, 1], [1953, 29, 2], [1953, 29, 3], [1953, 29, 4], [1953, 29, 5], [1953, 29, 6], [1953, 29, 7], [1953, 29, 8], [1953, 29, 9], [1953, 29, 11], [1953, 29, 12], [1953, 29, 13], [1953, 29, 14], [1953, 29, 15], [1953, 29, 16], [1953, 29, 17], [1953, 29, 18], [1953, 29, 19], [1953, 29, 20], [1953, 29, 21], [1953, 29, 22], [1953, 29, 23], [1953, 29, 24], [1953, 29, 25], [1953, 29, 26], [1953, 29, 27], [1953, 29, 28], [1953, 29, 29], [1953, 29, 30], [1953, 29, 31], [1953, 29, 32], [1953, 29, 33], [1953, 29, 34], [1953, 29, 35], [1953, 29, 36], [1953, 29, 37], [1953, 29, 38], [1953, 29, 39], [1953, 29, 40], [1953, 29, 41], [1953, 29, 42], [1953, 29, 43], [1953, 29, 44], [1953, 29, 45], [1953, 29, 46]]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=73, two_qubit=0), NoisyOperationsCountPerShot(i_errors=NoisyOperationsCount(count=0, paths=[]), x_errors=NoisyOperationsCount(count=0, paths=[]), z_errors=NoisyOperationsCount(count=0, paths=[]), y_errors=NoisyOperationsCount(count=0, paths=[]), one_qubit=0, two_qubit=0)])
