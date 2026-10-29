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
    raw = raw.filter(l_freq=l_freq, h_freq=h_freq)
    return raw

def find_events(raw):
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

def plot_evoked(evoked):
    """Plot the evoked response.

    Parameters
    ----------
    evoked : mne.Evoked
        The evoked response to plot.

    Returns
    -------
    fig : matplotlib.figure.Figure
        The figure containing the plot.
    """
    fig = evoked.plot()
    return fig