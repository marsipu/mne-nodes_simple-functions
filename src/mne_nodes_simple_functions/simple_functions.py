def average_reference_raw(raw):
    """Add an EEG average-reference projector and return raw data and its info.

    The raw object is updated in place. Apply projections during epoching or
    inverse modeling so data, covariance and inverse use the same reference.
    """
    raw.set_eeg_reference(ref_channels="average", projection=True)
    info = raw.info
    return raw, info


def filter_raw(raw, l_freq=None, h_freq=None):
    """Filter raw data.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw data to filter.
    l_freq : float | None
        The low cutoff frequency. If None, no high-pass filtering is applied.
    h_freq : float | None
        The high cutoff frequency. If None, no low-pass filtering is applied.

    Returns
    -------
    raw : mne.io.Raw
        The filtered raw data.
    """
    raw = raw.filter(l_freq=l_freq, h_freq=h_freq, n_jobs=-1)
    return raw

def get_events(raw):
    """Find events in raw data.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw data to find events from.

    Returns
    -------
    events : array-like
        The found events.
    """
    from mne import find_events
    events = find_events(raw)
    return events

find_events = get_events

def make_epochs(raw, events=None, event_id=None, tmin=-0.5, tmax=1, baseline=None):
    """Create epochs from raw data.

    Parameters
    ----------
    raw : mne.io.Raw
        The raw data to create epochs from.
    events : array-like | None
        The events array. If None, events will be automatically detected from the annotations in raw data.
    event_id : dict | None
        The event ID mapping. If None, it will be automatically determined from the annotations in raw data.
    tmin : float
        The start time before each event.
    tmax : float
        The end time after each event.
    baseline : tuple | None
        The time interval to use for baseline correction.

    Returns
    -------
    epochs : mne.Epochs
        The created epochs.
    """
    from mne import Epochs, events_from_annotations
    if events is None or event_id is None:
        events, event_id = events_from_annotations(raw)
    epochs = Epochs(raw, events, event_id, tmin=tmin, tmax=tmax, baseline=baseline)
    return epochs

def compute_evoked(epochs, condition: str | None = None):
    """Compute the evoked response for a specific condition.

    Parameters
    ----------
    epochs : mne.Epochs
        The epochs to compute the evoked response from.
    condition : str | None
        The condition to compute the evoked response for. If None, the first condition will be used.

    Returns
    -------
    evoked : mne.Evoked
        The computed evoked response.
    """
    if condition is None:
        evoked = epochs.average()
    else:
        evoked = epochs[condition].average()
    return evoked

def plot_evokeds(evoked):
    fig = evoked.plot()
    return fig

def make_noise_covariance_raw(raw):
    from mne import compute_raw_covariance
    noise_cov = compute_raw_covariance(raw, n_jobs=-1)
    return noise_cov

def make_noise_covariance_epochs(epochs):
    from mne import compute_covariance
    noise_cov = compute_covariance(epochs, n_jobs=-1)
    return noise_cov

def get_forward_solution(info, trans, subject):
    """Compute a forward model, reusing existing watershed BEM surfaces."""
    from mne import (
        make_bem_model,
        make_bem_solution,
        make_forward_solution,
        setup_source_space,
    )

    src = setup_source_space(subject, n_jobs=-1)
    bem_model = make_bem_model(subject)
    bem_solution = make_bem_solution(bem_model)
    fwd = make_forward_solution(info, trans, src, bem_solution)
    return fwd

def get_inverse_operator(info, fwd, noise_cov):
    from mne.minimum_norm import make_inverse_operator
    inv = make_inverse_operator(info, fwd, noise_cov)
    return inv

def make_source_estimate(evoked, inv, method='dSPM'):
    from mne.minimum_norm import apply_inverse
    stc = apply_inverse(evoked, inv, lambda2=1.0 / 9.0, method=method)
    return stc

def plot_source_estimate(stc):
    fig = stc.plot()
    return fig