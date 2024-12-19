"""Plot cases where the ECG peak detection method:
Engzee fails to detect peaks."""
# %% Import libraries and ecg_class
import os
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
from ecgdetectors import Detectors
from tqdm import tqdm

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# %%
PLOT = True
SAVE_PATH = 'results/rr_detection'
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)
FS = 250

# %% Check if the annotated peaks exist

EXPERIMENT = 'jogging'
for subject in tqdm(range(0, 25)):
    ecg_class = GUDb(subject, EXPERIMENT)
    # Get the ECG signal
    anno_exists = ecg_class.anno_cables_exists
    annotated_peaks = ecg_class.anno_cables
    if not ecg_class.anno_cs_exists:
        print(f'{subject}')
        print('CS Annotated peaks doesnt exist')
    if not ecg_class.anno_cables_exists:
        print(f'{subject}')
        print('Einhoven Annotated peaks doesnt exist')

# %% Jogging missing annotations
SUBJECT = 9
detectors = Detectors(FS)
methods = detectors.get_detector_list()

ecg_class = GUDb(SUBJECT, EXPERIMENT)

# Get the ECG signal
anno_exists = ecg_class.anno_cables_exists
annotated_peaks = ecg_class.anno_cables

time = ecg_class.t

# Plot the ECG signal
fig, axs = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
fig.suptitle('Raw ECG signal during jogging condition')

data = ecg_class.einthoven_II * 1000
annotated_peaks = ecg_class.anno_cables
axs[0].plot(time, data, color='black')
# axs[0].plot(time[annotated_peaks], data[annotated_peaks], 'o', color='blue')
axs[0].set_title('Setup: Loose Cables')
axs[0].set_ylabel('Amplitude [mV]')
axs[0].set_ylim([-25, -15])

data = ecg_class.cs_V2_V1 * 1000
annotated_peaks = ecg_class.anno_cs
axs[1].plot(time, data, color='black')
axs[1].plot(time[annotated_peaks], data[annotated_peaks], 'o', color='blue')
axs[1].set_title('Setup: Chest Strap')
axs[1].set_ylabel('Amplitude [mV]')
axs[1].set_xlabel('Time [s]')
# axs[1].set_ylim([-5, 0])


plt.xlim(0, 5.5)
plt.tight_layout()

plt.savefig(f'{SAVE_PATH}/jogging_example.pdf')

# %%
