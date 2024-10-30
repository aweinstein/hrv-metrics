# %% Import libraries and ecg_class
import os
import seaborn as sns
from ecg_gudb_database import GUDb
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from ecgdetectors import Detectors
from jf_ecg_benchmark.jf_analysis import evaluate as jf
from jf_ecg_benchmark.sensitivity_analysis import evaluate as sens
from multipage_pdf import save_figs_as_pdf


os.chdir(os.path.dirname(os.path.abspath(__file__)))

PLOT = False
SAVE_PATH = 'results/rr_detection'
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

NSUBJECTS = 24
FS = 250
DETECTOR = 'Einhoven'
experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
subjects = np.arange(0, NSUBJECTS+1)

# %%

methods_names = np.array(['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform',
                          'Engzee', 'Christov', 'Hamilton', 'Pan_Tompkins',
                          'WQRS'])

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

# First, loop trough subjects
for i, s in enumerate(subjects):

    # Second, loop thorugh experiments
    # Iterate through experiments
    for ii, experiment in enumerate(experiments):

        ecg_class = GUDb(s, experiment)

        # Anotated R-peaks and data
        if DETECTOR == 'Einhoven':
            anno_exists = ecg_class.anno_cables_exists
            annotated_peaks = ecg_class.anno_cables
            data = ecg_class.einthoven_II

        if not anno_exists:
            print(f'Subject: {s} | Experiment: {experiment} | No annotations')
# %%
