""""
Utilities to detect and calculate HRV measures.
"""
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages


def save_figs_as_pdf(figs, fn):
    if isinstance(figs, list):
        pdf = PdfPages(fn)
        for f in figs:
            pdf.savefig(f)
        pdf.close()
    else:
        figs.savefig(fn, format='pdf')
    print('File saved as', fn)


def confusion_matrix(annotated_peaks,
                     detected_peaks, tolerance_window):
    """
    Computes performance measures for peak detection.

    Parameters
    ----------
    annotated_peaks -> 1D ndarray with the annotated peaks in samples
    detected_peaks -> 1D ndarray with the detected peaks in samples
    tolerance_window -> float with the number of samples to tolerate for the
    detection of a true positive peak.

    References
    ----------
    This function is based on what is described in:
    """

    tp = np.sum(
        np.abs(
            (annotated_peaks[:, None] - detected_peaks[None, :])) < tolerance_window)

    fp = len(detected_peaks) - tp

    fn = len(annotated_peaks) - tp

    sensitivity = tp / (tp + fn)

    positive_predictivity = tp / (tp + fp)

    return sensitivity, positive_predictivity, tp, fp, fn


def read_info():
    """
    Returns dictionary with information about the QRS detection analysis.

    Parameters
    ----------
    file -> string with the name of the info file.
    """
    n_subjects = 25
    info = {}
    info['subject_list'] = [str(n) for n in range(n_subjects)]
    info['experiments'] = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
    info['methods_names'] = ['Elgendi_et_al', 'Matched_filter',
                             'Wavelet_transform', 'Engzee', 'Christov',
                             'Hamilton', 'Pan_Tompkins', 'WQRS']
    return info


def plot_hrv(data, x, y, hue):
    """
    Plot HRV metrics
    """
    fig, ax = plt.subplots(figsize=(7, 4))
    ax = sns.barplot(data, x=x, y=y, hue=hue,
                     ax=ax, errorbar='se')

    plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
             45, ha="left", rotation_mode="anchor")

    plt.legend(ncol=3)
    return fig, ax
