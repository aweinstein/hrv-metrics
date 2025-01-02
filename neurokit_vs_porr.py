# %% Import libraries and ecg_class
import os
import ecgdetectors
import matplotlib.pyplot as plt
import neurokit2 as nk
from ecg_gudb_database import GUDb
from jf.sensitivity_analysis import evaluate as sensitivity
from jf.jf_analysis import evaluate as jf


experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']

# Methods from the ecg_peaks function in neurokit2 webpage
methods = ['neurokit', 'pantompkins1985', 'hamilton2002', 'zong2003',
           'christov2004', 'elgendi2010', 'engzeemod2012', 'kalidas2017',
           'nabian2018', 'rodrigues2021']
ecg_class = GUDb(0, experiments[-1])

# Anotated R-peaks and data
annotated_peaks = ecg_class.anno_cs
time = ecg_class.t
data = ecg_class.einthoven_II
fs = ecg_class.fs

# Peaks detected by Porr
detectors = ecgdetectors.Detectors()
detector_list = detectors.get_detector_list()
detectors.fs = fs
detected_peaks_porr = detectors.engzee_detector(data)

# Peaks detected by neurokit
_, info = nk.ecg_peaks(data, sampling_rate=fs, method=methods[6])
detected_peaks_nk = info['ECG_R_Peaks']

# Peaks detected by neurokit after preprocessing
cleaned_data = nk.ecg_clean(data, fs, method=methods[1])
_, info = nk.ecg_peaks(cleaned_data, sampling_rate=fs,
                       method=methods[1],
                       correct_artifacts=False,
                       )
detected_peaks_nk_clean = info['ECG_R_Peaks']

# Compare sensitivity
tol = fs / 10
sensitivity_porr = sensitivity(detected_peaks_porr, annotated_peaks, tol)
sensitivity_nk = sensitivity(detected_peaks_nk, annotated_peaks, tol)
sensitivity_nk_clean = sensitivity(detected_peaks_nk_clean,
                                         annotated_peaks, tol)

jf_porr = jf(detected_peaks_porr, annotated_peaks, fs, None)['jf']
jf_nk = jf(detected_peaks_nk, annotated_peaks, fs, None)['jf']
jf_nk_clean = jf(detected_peaks_nk_clean, annotated_peaks, fs, None)['jf']

print('Sensitivity')
print(f'Porr\'s implementation: {sensitivity_porr}')
print(f'Neurokit Implementation: {sensitivity_nk}')
print(f'Neurokit with preprocessing: {sensitivity_nk_clean}')
print('JF')
print(f'Porr\'s implementation: {jf_porr}')
print(f'Neurokit Implementation: {jf_nk}')
print(f'Neurokit with preprocessing: {jf_nk_clean}')

plt.close('all')
plt.figure()
plt.plot(time, data, label='Raw ECG', color='teal')
plt.scatter(time[detected_peaks_porr], data[detected_peaks_porr],
            color='purple', label='Porr Implementation', marker='x')
plt.scatter(time[detected_peaks_nk], data[detected_peaks_nk],
            color='blue', label='Neurokit Implementation')
plt.title('Engzee')
plt.legend()
plt.xlim([50, 60])
plt.ylim([-0.015, -0.009])

plt.figure()
plt.plot(time, data)
plt.scatter(time[detected_peaks_porr], data[detected_peaks_porr],
            color='purple', label='Porr Implementation', marker='x')
plt.scatter(time[detected_peaks_nk_clean], data[detected_peaks_nk_clean],
            color='blue', label='Neurokit with preprocessing Implementation')
plt.title('Engzee')
plt.legend()
plt.xlim([50, 60])
plt.ylim([-0.015, -0.009])
