"""
Functions to visualize the ECG and the annotations.
"""
from pathlib import Path
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
from cycler import cycler
from ecgdetectors import Detectors
from jf.jf_analysis import evaluate as jf
from jf.sensitivity_analysis import evaluate as sens


save_path = Path(__file__).resolve().parent /  'results'
FS = 250

def plot_single_case(subject, experiment, setup, methods):
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

    # methods = detectors.get_detector_list()
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

    plt.close('all')
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


if __name__ == '__main__':
    setup = 'chest_strap'
    subject = 16  # Engzee fails to detect peaks for subjects 16 and 21
    experiment = 'sitting'
    methods = ['two_average', 'engzee']
    jf, sens = plot_single_case(subject, experiment, setup, methods)
    for method in methods:
        print(f'Setup {setup}, subject {subject}, experiment {experiment} '
              f'method {method}: sensitivity = {sens[method]:.2f} JF = {jf[method]:.2f}')
