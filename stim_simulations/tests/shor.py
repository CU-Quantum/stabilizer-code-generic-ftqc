import numpy as np
import pytest

from stim_simulations.shor import (
    run_shor_round_with_recovery,
    build_shor_one_round_circuit,
    decode_shor_syndrome,
    BLOCKS,
)


def test_no_error_no_syndrome_and_no_corrections():
    res = run_shor_round_with_recovery(shots=10, injected_error=None, seed=1)
    dets = res["detections"]
    x_corr = res["x_corrections"]
    z_corr = res["z_corrections"]

    # With no errors, all syndromes are zero and no corrections suggested
    assert dets.shape[1] == 8
    assert np.all(dets == 0)
    assert np.all(x_corr == 0)
    assert np.all(z_corr == 0)


@pytest.mark.parametrize("q", list(range(9)))
def test_single_x_error_is_corrected_on_same_qubit(q):
    # Inject an X on qubit q
    res = run_shor_round_with_recovery(shots=1, injected_error=("X", q), seed=2)
    dets = res["detections"][0]
    x_corr = res["x_corrections"][0]
    z_corr = res["z_corrections"][0]

    # X errors flip Z-pair checks in their block, not the cross-block X checks
    assert dets[6] == 0 and dets[7] == 0

    # Decoder should propose an X on exactly the error location
    assert x_corr[q] is True
    assert int(np.sum(x_corr)) == 1
    # No Z corrections for a pure X error
    assert not np.any(z_corr)


@pytest.mark.parametrize("q", list(range(9)))
def test_single_z_error_is_corrected_on_block_representative(q):
    # Inject a Z on qubit q
    res = run_shor_round_with_recovery(shots=1, injected_error=("Z", q), seed=3)
    dets = res["detections"][0]
    x_corr = res["x_corrections"][0]
    z_corr = res["z_corrections"][0]

    # Z errors flip cross-block X checks depending on which block the qubit is in
    # And shouldn't trigger within-block Z-pair checks
    assert np.all(dets[:6] == 0)

    # Determine expected block
    if q in BLOCKS[0]:
        expected = BLOCKS[0][0]
        assert dets[6] == 1 and dets[7] == 0
    elif q in BLOCKS[1]:
        expected = BLOCKS[1][0]
        assert dets[6] == 1 and dets[7] == 1
    else:
        expected = BLOCKS[2][0]
        assert dets[6] == 0 and dets[7] == 1

    # Decoder should propose a Z on the first qubit of the correct block (representative)
    assert z_corr[expected] is True
    assert int(np.sum(z_corr)) == 1
    # No X corrections for a pure Z error
    assert not np.any(x_corr)
