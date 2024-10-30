# %% Import libraries and ecg_class
import os
from ecg_gudb_database import GUDb
import numpy as np
import matplotlib.pyplot as plt
import neurokit2 as nk
import pandas as pd
from jf_ecg_benchmark.jf_analysis import evaluate as jf
import utils

# %% Load Data
SAVE_PATH = 'results/rr_detection_example'
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

SUBJECT_NUMBER = 0  # 0 - 24

experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
ecg_class = GUDb(SUBJECT_NUMBER, experiments[0])

# Anotated R-peaks and data

annotated_peaks = ecg_class.anno_cs
data = ecg_class.cs_V2_V1

time = ecg_class.t
FS = ecg_class.fs

ecg_clean = nk.ecg_clean(data, sampling_rate=FS, method='neurokit')

# tolerance window in samples
W = FS / 10

# %% Detect peaks
detected_peaks, info = nk.ecg_peaks(ecg_clean, sampling_rate=FS,
                                    method='neurokit')
detected_peaks = np.where(detected_peaks.to_numpy()[:, 0])[0]

artifacts, corrected_peaks = nk.signal_fixpeaks(
    detected_peaks, sampling_rate=FS, iterative=True,
    method='Kubios', show=True)

JF = jf(detected_peaks, annotated_peaks, FS, 100)

hrv_indices = nk.hrv(corrected_peaks, sampling_rate=FS, show=True)

# %%
hrv_indices['HRV_MeanNN'][0]
