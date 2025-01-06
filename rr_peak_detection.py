"""
Detects QRS peaks for all subjects, conditions, and setups.
"""
from pathlib import Path
import seaborn as sns
from ecg_gudb_database import GUDb
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from ecgdetectors import Detectors
from jf.jf_analysis import evaluate as jf
from jf.sensitivity_analysis import evaluate as sens
from utils import subjects, experiments, methods_names, make_peaks_file_name

save_path = Path(__file__).resolve().parent / 'results/rr_detection'
fs = 250
# %% Initialize Porr detectors
detectors = Detectors(fs)
methods = detectors.get_detector_list()


def detect_peaks(setup):
    # Allocate arrays that later compose the DF
    sensitivity = []
    JF = []
    methods_name = []
    experiments_name = []
    subject_idx = []

    for s in tqdm(subjects, desc='Subject'):
        for experiment in tqdm(experiments, desc='Condition'):
            ecg_class = GUDb(s, experiment)

            # Anotated R-peaks and data
            if setup == 'einthoven':
                anno_exists = ecg_class.anno_cables_exists
                annotated_peaks = ecg_class.anno_cables
                data = ecg_class.einthoven_II

            elif setup == 'chest_strap':
                anno_exists = ecg_class.anno_cs_exists
                annotated_peaks = ecg_class.anno_cs
                data = ecg_class.cs_V2_V1

            if not anno_exists:
                tqdm.write(f'No annotation for subject {s}, condition {experiment}. '
                           'Skipping it.')
                continue

            fs = ecg_class.fs

            # tolerance window in samples
            W = int(fs / 10)

            fn = make_peaks_file_name(s, setup, experiment, 'annotated')
            np.save(save_path / fn, annotated_peaks)

            for i, method in enumerate(tqdm(methods, desc='Method', leave=False)):

                # Find peaks
                detected_peaks = np.array(method[1](data))

                fn = make_peaks_file_name(s, setup, experiment, methods_names[i])
                np.save(save_path / fn, detected_peaks)

                # Compute sensitivity
                if len(detected_peaks) > 10:

                    experiments_name.append(experiment)
                    methods_name.append(methods_names[i])
                    subject_idx.append(s)

                    results = sens(detected_peaks, annotated_peaks, W)
                    sensitivity.append(results[0])

                    JF.append(jf(detected_peaks, annotated_peaks, fs, None)['jf'])

    # Arrange into pandas array
    data_dict = {'sensitivity': np.array(sensitivity),
                 'JF': np.array(JF)*100,
                 'method': np.array(methods_name),
                 'experiment': np.array(experiments_name),
                 'subject_idx': np.array(subject_idx)}
    data = pd.DataFrame.from_dict(data_dict)
    data.to_csv(save_path / f'sensitivity_jf_{setup}.csv')

    # Sensitivity and JF plots
    plt.close('all')
    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=data, x='method', y='sensitivity',
                hue='experiment', errorbar='sd', ax=ax)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
             45, ha="left", rotation_mode="anchor")
    plt.ylabel('Sensitivity [%]')
    plt.xlabel('Method')
    plt.title(setup)
    plt.tight_layout()
    fig.savefig(save_path / f'sensitivity_{setup}.pdf')

    fig, ax = plt.subplots(figsize=(7, 4))
    sns.barplot(data=data, x='method', y='JF', hue='experiment', errorbar='sd',
                ax=ax)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
             45, ha="left", rotation_mode="anchor")
    plt.ylabel('JF [%]')
    plt.xlabel('Method')
    plt.title(setup)
    plt.tight_layout()
    fig.savefig(save_path / f'JF_{setup}.pdf')


if __name__ == '__main__':
    detect_peaks('chest_strap')
    detect_peaks('einthoven')
