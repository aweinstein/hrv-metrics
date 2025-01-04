"""
Finds detectors that fails to detect 10 or more R peaks.
"""
from pathlib import Path
from ecg_gudb_database import GUDb
import matplotlib.pyplot as plt
from ecgdetectors import Detectors
from jf.jf_analysis import evaluate as jf
from jf.sensitivity_analysis import evaluate as sens
import pandas as pd
from tqdm import tqdm

save_path = Path(__file__).resolve().parent /  'results'
FS = 250

def plot_single_case():
    experiment = 'sitting'
    subject = 16 # Engzee fails to detect peaks for subjects 16 and 21
    detectors = Detectors(FS)
    methods = detectors.get_detector_list()
    ecg = GUDb(subject, experiment)
    anno_exists = ecg.anno_cables_exists # Get the ECG signal
    annotated_peaks = ecg.anno_cs
    data = ecg.cs_V2_V1 * 1000
    time = ecg.t

    # Get the peaks
    detected_peaks = detectors.engzee_detector(data)
    detected_peaks2 = detectors.two_average_detector(data)

    # Print Sensitivity and JF score
    W = int(FS / 10) # tolerance window in samples
    JF = jf(detected_peaks, annotated_peaks, FS, None)['jf']
    print(f'JF score: {JF:.2f}')
    SENS = sens(detected_peaks, annotated_peaks, FS/10)[0]
    print(f'Sensitivity: {SENS:.2f}')

    plt.close('all')
    plt.figure(figsize=(6, 4))
    plt.plot(time, data, color='black')
    plt.plot(time[annotated_peaks], data[annotated_peaks], 'o', color='blue')
    plt.plot(time[detected_peaks], data[detected_peaks], 'x', color='magenta')
    plt.plot(time[detected_peaks2], data[detected_peaks2], '*', color='green')

    plt.title('Raw ECG signal with annotated and detected peaks')

    # Detail names of detectors
    plt.legend(['ECG signal', 'Annotated peaks', 'Engzee Detector',
                'Two Average Detector'], loc='lower right')
    plt.xlim(0, 5.5)
    plt.xlabel('Time [s]')
    plt.ylabel('ECG [mV]')
    plt.savefig(save_path / 'engzee_fail.pdf')


def check_all(setup):
    """Find detectors unable to detect more than 10 R peaks.
    Returns a dataframe with recordings with less than 10 detections.
    """
    df = []
    count = 0
    experiments = GUDb.experiments
    detectors = Detectors(FS)
    print('Checking all subjects and conditions for setup', setup)
    for experiment in tqdm(experiments, desc='Condition'):
        for subject in tqdm(range(25), desc='Subject', leave=True):
            ecg = GUDb(subject, experiment)

            annotated_peaks = ecg.anno_cs
            if setup == 'chest_strap':
                data = ecg.cs_V2_V1 * 1000
                anno_exists = ecg.anno_cs_exists
                annotated_peaks = ecg.anno_cs
            if setup == 'einthoven':
                 data = ecg.einthoven_II * 1000
                 anno_exists = ecg.anno_cables_exists
                 annotated_peaks = ecg.anno_cables

            if not anno_exists:
                tqdm.write(f'No annotations for setup {setup}, '
                           f'subject {subject}, condition {experiment} '
                           'Skipping it.')
                continue
            else:
                for name, detector in tqdm(detectors.get_detector_list(), desc='Detector', leave=True):
                    detected_peaks = detector(data)
                    df.append({"detected_peaks": len(detected_peaks),
                               "percentage": len(detected_peaks) / len(annotated_peaks) * 100,
                               "subject": subject,
                               "experiment": experiment,
                               "detector": name})

                    if ('engzee' in name.lower()) and len(detected_peaks) < 10:
                        tqdm.write( f'Setup {setup}, subject {subject}, condition {experiment} '
                                    'has less than 10 detected peaks')
                        tqdm.write(f'Total annotated peaks: {len(annotated_peaks)}')
                        count += 1

    df = pd.DataFrame.from_dict(df)
    print(f'Number of recordings without detections: {count}')
    df = df[df['detected_peaks'] < 10]
    df.to_csv(save_path / f'engzee_{setup}_fail_table.csv')
    return df


if __name__ == '__main__':
    plot_single_case()
    df_cheststrap =check_all('chest_strap')
    df_einthoven = check_all('einthoven')
