"""
Exploration for different methods to extract RR-interval times.
"""

# %% Import libraries and ecg_class
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


SAVE_PATH = Path('results/rr_detection')
n_subjects = 24
FS = 250
DETECTOR = 'chest_strap'
experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
subjects = np.arange(0, n_subjects + 1)


methods_names = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform',
                 'Engzee', 'Christov', 'Hamilton', 'Pan_Tompkins',
                 'WQRS']

# %% Initialize Porr detectors
detectors = Detectors(FS)
methods = detectors.get_detector_list()

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
        if DETECTOR == 'Einhoven':
            anno_exists = ecg_class.anno_cables_exists
            annotated_peaks = ecg_class.anno_cables
            data = ecg_class.einthoven_II

        elif DETECTOR == 'chest_strap':
            anno_exists = ecg_class.anno_cs_exists
            annotated_peaks = ecg_class.anno_cs
            data = ecg_class.cs_V2_V1

        if not anno_exists:
            tqdm.write(f'No annotation for subject {s}, condition {experiment}. '
                       'Skipping it.')
            continue

        time = ecg_class.t
        FS = ecg_class.fs

        # tolerance window in samples
        W = int(FS / 10)

        fn = SAVE_PATH / f'{s:02d}_{DETECTOR}_{experiment}_annotated_peaks.npy'
        np.save(fn, annotated_peaks)

        figs = []
        for i, method in enumerate(tqdm(methods, desc='Method', leave=False)):

            # Find peaks
            detected_peaks = np.array(method[1](data))

            fn = f'{s:02d}_{DETECTOR}_{experiment}_{methods_names[i]}_peaks.npy'
            fn = SAVE_PATH / fn

            # Save detected peaks
            np.save(fn, detected_peaks)

            # Compute sensitivity
            if len(detected_peaks) > 10:

                experiments_name.append(experiment)
                methods_name.append(methods_names[i])
                subject_idx.append(s)

                results = sens(detected_peaks, annotated_peaks, W)
                sensitivity.append(results[0])

                JF.append(jf(detected_peaks, annotated_peaks, FS, None)['jf'])

# Arrange into pandas array
data_dict = {'sensitivity': np.array(sensitivity),
             'JF': np.array(JF)*100,
             'method': np.array(methods_name),
             'experiment': np.array(experiments_name),
             'subject_idx': np.array(subject_idx)}
data = pd.DataFrame.from_dict(data_dict)
core_df = data.to_csv('results/core_df.csv')
data.to_csv(SAVE_PATH / 'sensitivity_jf.csv')

# Sensitivity Plot
plt.close('all')
fig, ax = plt.subplots(figsize=(7, 4))
sns.barplot(data=data, x='method', y='sensitivity',
            hue='experiment', errorbar='sd', ax=ax)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
         45, ha="left", rotation_mode="anchor")
plt.ylabel('Sensitivity [%]')
plt.xlabel('Method')

plt.tight_layout()

fig.savefig(SAVE_PATH / 'sensitivity.pdf')

# %% JF Plot
fig, ax = plt.subplots(figsize=(7, 4))

sns.barplot(data=data, x='method', y='JF', hue='experiment', errorbar='sd',
            ax=ax)
plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
         45, ha="left", rotation_mode="anchor")
plt.ylabel('JF [%]')
plt.xlabel('Method')

plt.tight_layout()

fig.savefig(SAVE_PATH / 'JF.pdf')
