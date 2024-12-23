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
from utils import save_figs_as_pdf


PLOT = False
SAVE_PATH = Path('results/rr_detection')

NSUBJECTS = 24
FS = 250
DETECTOR = 'chest_strap'
experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
subjects = np.arange(0, NSUBJECTS+1)


methods_names = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform',
                 'Engzee', 'Christov', 'Hamilton', 'Pan_Tompkins',
                 'WQRS']

# Write info file to save variables
lines = [list(subjects.astype(str)), experiments,
         list(methods_names), [str(FS)]]
HEADERS = ['subject_list', 'experiments', 'methods_names']
with open('results/info.txt', '+w', encoding='utf-8') as f:
    for header, line in zip(HEADERS, lines):
        f.write(header+';')
        for item in line:
            f.write(item+',')
        f.write('\n')


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

            # Plot 5s if wanted
            if PLOT:
                # Deffine plotting window
                T1, T2 = 10, 15
                fig = plt.figure()
                data_range = [np.amin(data), np.amax(data)]
                plt.plot(time, data, color='teal')

                plt.scatter(time[annotated_peaks], data[annotated_peaks],
                            color='red', label='Annotated', marker='x', alpha=0.7)
                plt.scatter(time[detected_peaks], data[detected_peaks],
                            color='blue', label='Detected', marker='o', s=50, alpha=0.5)

                line1 = [plt.axvline(x)
                         for x in ((annotated_peaks - W)/FS)]
                line2 = [plt.axvline(x)
                         for x in ((annotated_peaks + W)/FS)]

                # Identify timepoints inside the windows
                no_fill = np.any(
                    np.abs(np.arange(len(time))[:, None] -
                           annotated_peaks[None, :]) < W,
                    axis=1)

                plt.fill_between(time,
                                 data-np.amax(data)*0.1,
                                 data+np.amin(data)*0.1,
                                 where=no_fill,
                                 alpha=0.3,
                                 color='green')

                plt.xlabel('Time [s]')
                plt.ylabel('Voltage')
                plt.legend()

                plt.xlim([T1, T2])
                # y_lim = [np.amin(data[np.argmin(abs(T1-time)):np.argmin(abs(T2-time))])*1.1,
                #         np.amax(data[np.argmin(abs(T1-time)):np.argmin(abs(T2-time))])*0.9]

                plt.title(f'Method: {method[0]}\nExperiment: {experiment}')

                # plt.ylim(y_lim)

                plt.tight_layout()

                fig.savefig(
                    f'{SAVE_PATH}/s[{s}]/{experiment}/{methods_names[i]}/5s.png')  # png
                fig.savefig(
                    f'{SAVE_PATH}/s[{s}]/{experiment}/{methods_names[i]}/5s.pdf')  # pdf
                figs.append(fig)
                # plt.close()

                # Plot Histogram
                fig2 = plt.figure(figsize=(7, 4))

                plt.hist(np.diff(detected_peaks / FS), bins=30, color='purple')
                plt.xlabel('Time [s]')
                plt.title(f'Subject: {s}\n Method: {method}')
                fig2.savefig(
                    f'{SAVE_PATH}/s[{s}]/{experiment}/{methods_names[i]}/histogram.png')  # png
                fig2.savefig(
                    f'{SAVE_PATH}/s[{s}]/{experiment}/{methods_names[i]}/histogram.pdf')  # pdf

            if PLOT:
                save_figs_as_pdf(figs,
                                 f'{SAVE_PATH}/s[{s}]/{experiment}/time_series.pdf')
                plt.close('all')
# %% Arrange in to pandas array

data_dict = {'sensitivity': np.array(sensitivity),
             'JF': np.array(JF)*100,
             'method': np.array(methods_name),
             'experiment': np.array(experiments_name),
             'subject_idx': np.array(subject_idx)}

data = pd.DataFrame.from_dict(data_dict)

core_df = data.to_csv('results/core_df.csv')

data.to_csv(SAVE_PATH / 'sensitivity_jf.csv')

# %% Sensitivity Plot

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
