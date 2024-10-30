""""Example script to load database"""
# %% Import libraries and ecg_class
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt

SUBJECT_NUMBER = 0  # 0 - 24
EXPERIMENT = 'sitting'  # sitting, maths, walking, hand_bike, jogging

ecg_class = GUDb(SUBJECT_NUMBER, EXPERIMENT)

# %% Anotated R-peaks and data

r_peaks = ecg_class.anno_cs

data = ecg_class.data

# %% Plot anotated peaks and data
IDX = 0
plt.plot(data[:, IDX], color='teal')

plt.scatter(r_peaks, data[r_peaks, IDX], color='purple')
plt.xlabel('Samples')
plt.ylabel('Voltage')

plt.title(f'Subject: {SUBJECT_NUMBER}\nExperiment: {EXPERIMENT}')

plt.xlim([0, 1000])

plt.show()
