"""
Functions to visualize the ECG and the annotations.
"""
from itertools import product
from pathlib import Path
import pandas as pd
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
from cycler import cycler
from ecgdetectors import Detectors
from jf.jf_analysis import evaluate as jf
from jf.sensitivity_analysis import evaluate as sens
from utils import experiments


save_path = Path(__file__).resolve().parent /  'results'
FS = 250
detectors = Detectors(FS)
detectors_d = {
    'pan_tompkins': detectors.pan_tompkins_detector,
    'two_average': detectors.two_average_detector,
    'swt': detectors.swt_detector,
    'christov': detectors.christov_detector,
    'hamilton': detectors.hamilton_detector,
    'matched_filter': detectors.matched_filter_detector,
    'engzee': detectors.engzee_detector,
    'wqrs': detectors.wqrs_detector
}

def auto_ylim(ax, margin=0.1):
    """Automatically adjust ylim based on current xlim"""
    xlim = ax.get_xlim()

    # Collect all y-values within xlim
    y_values = []
    for line in ax.get_lines():
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        mask = (xdata >= xlim[0]) & (xdata <= xlim[1])
        if mask.any():
            y_values.extend(ydata[mask])

    if y_values:
        y_min, y_max = min(y_values), max(y_values)
        y_range = y_max - y_min
        ax.set_ylim(y_min - margin * y_range, y_max + margin * y_range)


def load_data(subject, experiment, setup):
    ecg = GUDb(subject, experiment)

    if setup == 'chest_strap':
        data = ecg.cs_V2_V1 * 1000
        anno_exists = ecg.anno_cs_exists
        annotated_peaks = ecg.anno_cs
    elif setup == 'einthoven':
        data = ecg.einthoven_II * 1000
        anno_exists = ecg.anno_cables_exists
        annotated_peaks = ecg.anno_cables
    else:
        print(f'Error: Unkwnon setup {setup}')

    time = ecg.t
    return (time, data, anno_exists, annotated_peaks)


def plot_single_case(subject, experiment, setup, methods):
    time, data, anno_exists, annotated_peaks = load_data(subject, experiment,
                                                         setup)
    _, ax = plt.subplots(figsize=(6, 4))
    ax.plot(time, data, color='black', lw=0.5, label='ECG')
    ax.set_prop_cycle(marker=['+', 'o', 'x', 'D', '1', '2', '3'],
                      color=['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
                             '#e377c2', '#7f7f7f'])
    ms = 7
    if anno_exists:
        ax.plot(time[annotated_peaks], data[annotated_peaks], ls='None',
                label='Annotated', ms=ms)
    else:
        print('No annotations.')

    jfs, sensibilities = {}, {}
    for detector in methods:
        detected_peaks = detectors_d[detector](data)
        jfs[detector] = jf(detected_peaks,
                           annotated_peaks, FS, None)['jf']
        sensibilities[detector] = sens(detected_peaks, annotated_peaks, FS/10)[0]
        ax.plot(time[detected_peaks], data[detected_peaks], ls='None',
                label=detector, ms=ms)

    ax.set_title('Raw ECG signal with annotated and detected peaks')
    ax.legend(loc='lower right')
    ax.set_xlim(0, 5.5)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('ECG [mV]')
    fn = save_path / 'engzee_fail.pdf'
    plt.savefig(fn)
    print('Figure saved as', fn)

    return jfs, sensibilities


def get_top_bottom_by_jf(setup):
    jf_path = Path(__file__).resolve().parent / 'results' / 'rr_detection'
    fn = jf_path / f'sensitivity_jf_{setup}.csv'
    df = pd.read_csv(fn)
    # Remove repeated combination of experiment and subject
    dftop = df.loc[df.groupby(['experiment', 'subject_idx'])['JF'].idxmax()]

    top3 = dftop.nlargest(3, ['JF', 'sensitivity'])
    top3['rank'] = 'top'
    bot3 = df.nsmallest(3, 'JF')
    bot3['rank'] = 'bot'
    topbot = pd.concat([top3, bot3])
    topbot['setup'] = setup
    print(top3)
    print(bot3)
    return topbot


def plot_best_worst():
    """Plot the top three and the botton three detections by JF."""

    rows, cols = 4, 3
    _, axs = plt.subplots(rows, cols, layout='constrained', figsize=(19.2, 9.8))
    topbot_df = pd.concat([get_top_bottom_by_jf('chest_strap'),
                           get_top_bottom_by_jf('einthoven')])

    for i, row in enumerate(topbot_df.itertuples()):
        print('Plotting', row.method, row.experiment, row.subject_idx)
        subject, experiment, setup = row.subject_idx, row.experiment, row.setup
        time, data, anno_exists, annotated_peaks = load_data(subject, experiment,
                                                             setup)
        ax = axs.flat[i]
        ax.plot(time, data, color='black', lw=0.5, label='ECG')
        ax.set_prop_cycle(marker=['+', 'o', 'x', 'D', '1', '2', '3'],
                          color=['#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b',
                                 '#e377c2', '#7f7f7f'])

        detector = row.method.lower()
        if detector == 'elgendi_et_al':
            detector = 'two_average'
        elif detector == 'wavelet_transform':
            detector = 'swt'
        detected_peaks = detectors_d[detector](data)

        ms_annotated = 10
        ms_detector = 5
        if anno_exists:
            ax.plot(time[annotated_peaks], data[annotated_peaks], ls='None',
                    label='Annotated', ms=ms_annotated)
        else:
            print('No annotations.')
        ax.plot(time[detected_peaks], data[detected_peaks], ls='None',
                label=detector, ms=ms_detector)

        ax.set_xlim(0, 5.5)
        auto_ylim(ax)
        txt = (f'({chr(ord('a') + i)}) Subject {row.subject_idx}, '
               f'{row.experiment}, JF={row.JF:.1f}')
        ax.text(0.01, 0.02, txt, fontsize=12,
                transform=ax.transAxes)


    for r, c in product(range(rows), range(cols)):
        if r < 3:
            axs[r, c].set_xticks([])
        else:
            axs[r, c].set_xlabel('Time [s]')
        if c == 0:
            axs[r, c].set_ylabel('ECG [mV]')

        axs[r, c].tick_params(labelsize=14)
        axs[r, c].xaxis.label.set_size(16)
        axs[r, c].yaxis.label.set_size(16)


    fn = save_path / 'ecg_best_worst.pdf'
    plt.savefig(fn)
    print('Figure saved as', fn)

if __name__ == '__main__':
    plt.close('all')
    setup = 'chest_strap'
    subject = 16  # Engzee fails to detect peaks for subjects 16 and 21
    experiment = 'sitting'
    methods = ['two_average', 'engzee']
    jf_vals, sens = plot_single_case(subject, experiment, setup, methods)
    for method in methods:
        print(f'Setup {setup}, subject {subject}, experiment {experiment} '
              f'method {method}: sensitivity = {sens[method]:.2f} JF = {jf_vals[method]:.2f}')

    plot_best_worst()

    plt.show()
