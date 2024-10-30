"""Plot cases where the ECG peak detection method:
Engzee fails to detect peaks."""
# %% Import libraries and ecg_class
import os
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
from ecgdetectors import Detectors
from jf_ecg_benchmark.jf_analysis import evaluate as jf
from jf_ecg_benchmark.sensitivity_analysis import evaluate as sens
import pandas as pd
from tqdm import tqdm

os.chdir(os.path.dirname(os.path.abspath(__file__)))
# %%
PLOT = True
SAVE_PATH = 'results/rr_detection'
if not os.path.exists(SAVE_PATH):
    os.mkdir(SAVE_PATH)

FS = 250
DETECTOR = 'Einhoven'
EXPERIMENT = 'sitting'

# %% Engzee fails to detect peaks
# Subjects 16 and 21
SUBJECT = 16
detectors = Detectors(FS)
methods = detectors.get_detector_list()

ecg_class = GUDb(SUBJECT, EXPERIMENT)

# Get the ECG signal
anno_exists = ecg_class.anno_cables_exists
annotated_peaks = ecg_class.anno_cs
data = ecg_class.cs_V2_V1 * 1000
time = ecg_class.t

# Get the peaks
detected_peaks = detectors.engzee_detector(data)

detected_peaks2 = detectors.two_average_detector(data)


JF = jf(annotated_peaks, detected_peaks, FS,
        trim=False)['jf']
print(f'JF score: {JF}')

SENS = sens(annotated_peaks, detected_peaks, FS)[0]
print(f'Sensitivity: {SENS}')

# Print Sensitivity and JF score

# %% Plot the ECG signal

plt.figure(figsize=(6, 4))
plt.plot(time, data, color='black')
plt.plot(time[annotated_peaks], data[annotated_peaks], 'o', color='blue')
plt.plot(time[detected_peaks], data[detected_peaks], 'x', color='magenta')
plt.plot(time[detected_peaks2], data[detected_peaks2], '*', color='green')

plt.title('Raw ECG signal with annotated and detected peaks')

# Detail names of detectors
plt.legend(['ECG signal', 'Annotated peaks', 'Engzee Detector',
            'Elgendi Detector'], loc='lower right')

plt.xlim(0, 5.5)

plt.xlabel('Time [s]')
plt.ylabel('Amplitude [mV]')

plt.savefig(f'{SAVE_PATH}/engzee_fail.pdf')

# %% Check for every subject and experiment condition
# when the Engzee detector fails

df = []
count = 0
experiments = GUDb.experiments
for experiment in experiments:
    for subject in tqdm(range(0, 25)):
        ecg_class = GUDb(subject, experiment)
        anno_exists = ecg_class.anno_cs_exists
        annotated_peaks = ecg_class.anno_cs
        data = ecg_class.cs_V2_V1 * 1000
        # anno_exists = ecg_class.anno_cables_exists
        # annotated_peaks = ecg_class.anno_cables
        # data = ecg_class.einthoven_II * 1000
        time = ecg_class.t

        if anno_exists is False:
            print('Skipping subject... No annotations')
            continue
        else:
            for name, detector in detectors.get_detector_list():
                detected_peaks = detector(data)
                df.append({"detected_peaks": len(detected_peaks),
                           "percentage": len(detected_peaks) / len(annotated_peaks)*100,
                           "subject": subject,
                           "experiment": experiment,
                           "detector": name})

                if ('engzee' in name.lower()) and len(detected_peaks) < 10:
                    print(
                        f'Subject {subject}, condition {experiment} has less than 10 detected peaks')
                    print(f'Eigendi detected {len(detected_peaks2)} peaks')
                    print(f'Total Annotated Peaks: {len(annotated_peaks)}')
                    count += 1

df = pd.DataFrame.from_dict(df)
df.to_latex(f'{SAVE_PATH}/engzee_fail_table.tex')
print(f'Total of recordings lost: {count}')

# %%

df[df['detected_peaks'] < 10]
