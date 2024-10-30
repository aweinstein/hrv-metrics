# %%5 Check einhoven non annotated data

import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from ecg_gudb_database import GUDb

subjects = np.arange(0, 24)
experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
DETECTOR = 'Einhoven'

if not os.path.exists('non_annotated'):
    os.mkdir('non_annotated')

#  %%Load data
# First, loop trough subjects
for i, s in enumerate(tqdm(subjects)):

    # Second, loop thorugh experiments
    # Iterate through experiments
    for ii, experiment in enumerate(experiments):

        ecg_class = GUDb(s, experiment)

        # Anotated R-peaks and data
        if DETECTOR == 'Einhoven':
            anno_exists = ecg_class.anno_cables_exists
            annotated_peaks = ecg_class.anno_cables
            data = ecg_class.einthoven_II

        elif DETECTOR == 'Chest strap':
            anno_exists = ecg_class.anno_cs_exists
            annotated_peaks = ecg_class.anno_cs
            data = ecg_class.cs_V2_V1

        if not anno_exists:

            time = ecg_class.t
            FS = ecg_class.fs

            plt.figure(figsize=(12, 6))
            plt.plot(time, data)
            plt.scatter(time[annotated_peaks], data[annotated_peaks],
                        color='red', label='Annotated Peaks', marker='o', s=50)

            plt.title(f'Subject {s}, {experiment}, DETECTOR: {DETECTOR}')
            plt.xlabel('Time [s]')

            plt.xlim([10, 20])
            plt.savefig(f'non_annotated/Nann_{s}_{experiment}.png')

            # plt.show()
    plt.close('all')

# %% Plot signle subject

s = 1
experiment = 'jogging'

ecg_class = GUDb(s, experiment)

# Anotated R-peaks and data
if DETECTOR == 'Einhoven':
    anno_exists = ecg_class.anno_cables_exists
    annotated_peaks = ecg_class.anno_cables
    data = ecg_class.einthoven_II

elif DETECTOR == 'Chest strap':
    anno_exists = ecg_class.anno_cs_exists
    annotated_peaks = ecg_class.anno_cs
    data = ecg_class.cs_V2_V1

plt.figure(figsize=(12, 6))
plt.plot(ecg_class.t, data)
plt.scatter(ecg_class.t[annotated_peaks], data[annotated_peaks],
            color='red', label='Annotated Peaks', marker='o', s=50)

if anno_exists:
    plt.title(
        f'Subject {s}, {experiment}, DETECTOR: {DETECTOR}\n with annotated peaks')
else:
    plt.title(
        f'Subject {s}: {experiment}, DETECTOR: {DETECTOR},\n No annotated peaks')

plt.xlabel('Time [s]')
plt.xlim([10, 20])
plt.show()
