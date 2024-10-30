"""Plot interval tachogram for each subject and method. Also for each condition."""
# %% Load libraries
import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from utils import read_info
from multipage_pdf import save_figs_as_pdf
from tqdm import tqdm


# %% Read info file
info = read_info('results/info.txt')
core_df = pd.read_csv('results/core_df.csv')
subject_list = np.unique(core_df['subject_idx'])
experiments = info['experiments']
methods_names = info['methods_names']

FS = 250  # This should be inside the info file
READ_PATH = 'results/rr_detection/'
SAVE_PATH = 'results/tachograms'

# %% Iterate through subjects
for i, s in enumerate(tqdm(subject_list)):

    # Iterate through experiments
    for ii, experiment in enumerate(experiments):
        # Load annotated peaks
        ann_file = f'{READ_PATH}/s[{s}]/{experiment}/annotated_peaks.npy'

        # Check if file exists
        if os.path.exists(ann_file):
            annotated_peaks = np.load(ann_file)
        else:
            print(f'skip subject {s}, Exp: {experiment}...')
            core_df = core_df[np.logical_and(core_df.subject_idx !=
                                             s, core_df.experiment != experiment)]
            continue

        # Compute tachogram of annotated peaks
        ann_tachogram = np.diff(annotated_peaks) / FS

        # Iterate through methods
        figs = []
        for iii, method in enumerate(methods_names):

            save_path = f'{SAVE_PATH}/s[{s}]/{experiment}/{method}'

            detected_peaks = np.load(
                f'{READ_PATH}/s[{s}]/{experiment}/{method}/detected_peaks.npy')
            det_tachogram = np.diff(detected_peaks) / FS

            bins = np.linspace(np.amin(ann_tachogram),
                               np.amax(ann_tachogram), 50)

            fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)

            axs[0].hist(det_tachogram, bins=bins, color='purple')

            axs[0].set_title('Subject: ' + str(s) + ' - ' + experiment +
                             ' - ' + method)

            axs[1].hist(ann_tachogram, bins=bins, color='teal')
            axs[1].set_title('Annotated Tachogram')
            axs[1].set_xlabel('RR interval (s)')

            try:
                plt.savefig(f'{save_path}/detected_peaks.png')
            except FileNotFoundError:
                os.makedirs(save_path)
                plt.savefig(f'{save_path}/detected_peaks.png')

            figs.append(fig)

        save_figs_as_pdf(
            figs, f'{SAVE_PATH}/s[{s}]_{experiment}_tachogram.pdf')

        # Clear memory
        del figs
        plt.close('all')

# %% Plot tachogram for a given subject and condition

s = 11
method = 'Engzee'
experiment = 'walking'

ann_file = f'{READ_PATH}/s[{s}]/{experiment}/annotated_peaks.npy'
annotated_peaks = np.load(ann_file)

det_file = f'{READ_PATH}/s[{s}]/{experiment}/{method}/detected_peaks.npy'
detected_peaks = np.load(det_file)

ann_tachogram = np.diff(annotated_peaks) / FS
det_tachogram = np.diff(detected_peaks) / FS

# %% Plot histogram with subplots

fig, axs = plt.subplots(2, 1)

axs[0].hist(det_tachogram, color='purple')
axs[0].set_title('Subject: ' + str(s) + ' - ' + experiment + ' - ' + method)

axs[1].hist(ann_tachogram, color='teal')

axs[1].set_title('Annotated Tachogram')
axs[1].set_xlabel('RR interval (s)')

plt.tight_layout()
plt.show()
