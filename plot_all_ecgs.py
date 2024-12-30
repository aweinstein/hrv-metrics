"""
Plot the ECGs for all subjects, setups, and conditions.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from ecg_gudb_database import GUDb
from utils import save_figs_as_pdf


def plot_single_case(s, experiment, setup):
    ecg = GUDb(s, experiment)

    if setup == 'Einthoven':
        annotated = ecg.anno_cables_exists
        annotated_peaks = ecg.anno_cables
        data = ecg.einthoven_II

    elif setup == 'Chest strap':
        annotated = ecg.anno_cs_exists
        annotated_peaks = ecg.anno_cs
        data = ecg.cs_V2_V1

    data *= 1000 # Convert to mV
    fig = plt.figure(figsize=(12, 6.3))
    plt.plot(ecg.t, data)
    plt.scatter(ecg.t[annotated_peaks], data[annotated_peaks],
                color='red', label='Annotated Peaks', marker='o', s=50)

    if annotated:
        title = f'Subject {s}, condition {experiment}, setup: {setup}'
    else:
        title = (f'Subject {s}, condition {experiment}, setup: {setup} '
                 'No annotation')

    plt.title(title)
    plt.xlabel('Time [s]')
    plt.xlim([10, 20])
    plt.ylabel('ECG [mV]')
    plt.close(fig)
    return annotated, fig


def plot_all_ecg(setup, figs_annotated, figs_nonannotated):
    for s in tqdm(subjects, desc='Subject'):
        for experiment in tqdm(experiments, desc='Condition', leave=False):
            annotated, fig = plot_single_case(s, experiment, setup)
            if annotated:
                figs_annotated.append(fig)
            else:
                figs_nonannotated.append(fig)

if __name__ == '__main__':
    save_path = Path(__file__).resolve().parent /  Path('results')
    subjects = np.arange(0, 24)
    experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
    figs_annotated, figs_nonannotated = [], []
    plt.close('all')
    plot_all_ecg('Einthoven', figs_annotated, figs_nonannotated)
    plot_all_ecg('Chest strap', figs_annotated, figs_nonannotated)

    fn = save_path / 'ecgs_annotated.pdf'
    save_figs_as_pdf(figs_annotated, fn)
    fn = save_path / 'ecgs_nonannotated.pdf'
    save_figs_as_pdf(figs_nonannotated, fn)
