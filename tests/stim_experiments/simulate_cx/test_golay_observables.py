import numpy as np

from stim_experiments.simulate_cx.support.stabilizer_code_utilities import get_golay_code_utilities


def _make_weight7_utils():
    utils = get_golay_code_utilities(balanced=True)
    n = len(utils.data_indices)
    x_support = [0, 2, 4, 5, 6, 10, 11]
    z_support = [0, 1, 3, 6, 8, 10, 13]
    ox = np.zeros(2 * n, dtype=int)
    oz = np.zeros(2 * n, dtype=int)
    for i in x_support:
        ox[i] = 1
    for i in z_support:
        oz[n + i] = 1
    utils.x_observable = ox
    utils.z_observable = oz
    return utils


def _commutes_with_all_stabilizers(utils, observable):
    S = utils.symplectic_matrix
    n = S.shape[1] // 2
    ox = observable[:n]
    oz = observable[n:]
    sx = S[:, :n]
    sz = S[:, n:]
    return np.all((ox @ sz.T + oz @ sx.T) % 2 == 0)


def test_default_observables_are_valid_logical_operators():
    utils = get_golay_code_utilities(balanced=True)
    n = len(utils.data_indices)
    assert _commutes_with_all_stabilizers(utils, utils.x_observable)
    assert _commutes_with_all_stabilizers(utils, utils.z_observable)
    assert (utils.x_observable[:n] @ utils.z_observable[n:]) % 2 == 1


def test_weight7_observables_are_valid_logical_operators():
    utils = _make_weight7_utils()
    n = len(utils.data_indices)
    assert _commutes_with_all_stabilizers(utils, utils.x_observable)
    assert _commutes_with_all_stabilizers(utils, utils.z_observable)
    assert int(utils.x_observable.sum()) == 7
    assert int(utils.z_observable.sum()) == 7
    assert (utils.x_observable[:n] @ utils.z_observable[n:]) % 2 == 1
