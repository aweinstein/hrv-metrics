"""
Plots an example of the ECGs for Einthoven and the Chest Strap setup to
demonstrate the difference of noise level between the setups.
"""
from pathlib import Path
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
from ecgdetectors import Detectors
from tqdm import tqdm

save_path = save_path = Path(__file__).resolve().parent /  Path('results')
FS = 250
subject = 9
experiment = 'jogging'
ecg = GUDb(subject, experiment) #
annotated_peaks = ecg.anno_cables
time = ecg.t

# Plot the ECG signal
plt.close('all')
fig, axs = plt.subplots(2, 1, figsize=(6, 4), sharex=True)
fig.suptitle(f'Subject {subject} ECG for jogging condition')

data = ecg.einthoven_II * 1000
annotated_peaks = ecg.anno_cables
axs[0].plot(time, data, color='black')
axs[0].plot(time[annotated_peaks], data[annotated_peaks], 'o', color='blue')
axs[0].set_title('Loose Cables')
axs[0].set_ylabel('ECG [mV]')
axs[0].set_ylim([-25, -15])

data = ecg.cs_V2_V1 * 1000
annotated_peaks = ecg.anno_cs
axs[1].plot(time, data, color='black')
axs[1].plot(time[annotated_peaks], data[annotated_peaks], 'o', color='blue')
axs[1].set_title('Chest Strap')
axs[1].set_ylabel('ECG [mV]')
axs[1].set_xlabel('Time [s]')

plt.xlim(0, 5.5)
plt.tight_layout()
plt.savefig(f'{save_path}/jogging_example.pdf')
plt.show()
