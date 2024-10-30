# %% Import libraries and ecg_class
import os
import ecgdetectors
import matplotlib.pyplot as plt
import neurokit2 as nk
from ecg_gudb_database import GUDb
from jf_ecg_benchmark.sensitivity_analysis import evaluate as sensitivity


PLOT = False
SAVE_PATH = 'results/rr_detection_example'
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)


experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']

# Methods from the ecg_peaks function in neurokit2 webpage
methods = ['neurokit', 'pantompkins1985', 'hamilton2002',
           'zong2003', 'christov2004', 'elgendi2010',
           'engzeemod2012', 'kalidas2017',
           'nabian2018', 'rodrigues2021']


ecg_class = GUDb(0, experiments[-1])

# Anotated R-peaks and data

annotated_peaks = ecg_class.anno_cs
time = ecg_class.t
data = ecg_class.einthoven_II
FS = ecg_class.fs

plt.figure()
plt.xlim([0, 5])
plt.plot(time, data)

# %%

detectors = ecgdetectors.Detectors()
detector_list = detectors.get_detector_list()

detectors.fs = FS
detected_peaks1 = detectors.engzee_detector(data)

_, info = nk.ecg_peaks(data, sampling_rate=FS,
                       method=methods[6])
detected_peaks2 = info['ECG_R_Peaks']

# %% Compare

plt.plot(time, data, label='Raw ECG', color='teal')
plt.scatter(time[detected_peaks1], data[detected_peaks1],
            color='purple', label='Porr Implementation', marker='x')
plt.scatter(time[detected_peaks2], data[detected_peaks2],
            color='blue', label='Neurokit Implementation')
plt.title(methods[1])
plt.legend()
plt.xlim([50, 55])
plt.ylim([-0.015, -0.009])

# %% Compare sensitivity
TOL = FS/10

porr_sensitivity = sensitivity(detected_peaks1, annotated_peaks, TOL)

neurokit_sensitivity = sensitivity(detected_peaks2, annotated_peaks, TOL)

print(f'Porr\'s implementation: {porr_sensitivity}')
print(f'Neurokit Implementation: {neurokit_sensitivity}')

# %% Preprocess for Neurokit

cleaned_data = nk.ecg_clean(data, FS, method=methods[1])
_, info = nk.ecg_peaks(cleaned_data, sampling_rate=FS,
                       method=methods[1],
                       correct_artifacts=False,
                       )
detected_peaks2 = info['ECG_R_Peaks']

neurokit_sensitivity = sensitivity(detected_peaks2, annotated_peaks, TOL)
print(f'Neurokit w preprocessing: {neurokit_sensitivity}')

# %% Compare again

plt.plot(time, data)
plt.scatter(time[detected_peaks1], data[detected_peaks1],
            color='purple', label='Porr Implementation', marker='x')
plt.scatter(time[detected_peaks2], data[detected_peaks2],
            color='blue', label='Neurokit Implementation')
plt.title('Engzee Detector')
plt.legend()
plt.xlim([50, 60])
