"""EEG reference preparation for source modeling."""

import mne
import numpy as np

from mne_nodes_simple_functions.simple_functions import average_reference_raw


def test_average_reference_raw():
    raw = mne.io.RawArray(
        np.array([[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]]),
        mne.create_info(["EEG001", "EEG002", "MEG001"], 1000, ["eeg", "eeg", "mag"]),
    )
    raw.set_eeg_reference(["EEG001"])
    before = raw.get_data()
    referenced, info = average_reference_raw(raw)
    assert referenced is raw and info is raw.info
    assert not info["custom_ref_applied"]
    assert len(info["projs"]) == 1
    np.testing.assert_array_equal(raw.get_data(), before)
    raw.apply_proj()
    np.testing.assert_allclose(raw.get_data()[:2].mean(axis=0), 0, atol=1e-14)
    np.testing.assert_array_equal(raw.get_data()[2], before[2])
