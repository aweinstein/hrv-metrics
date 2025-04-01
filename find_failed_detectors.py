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

            if setup == 'chest_strap':
                data = ecg.cs_V2_V1 * 1000
                anno_exists = ecg.anno_cs_exists
                annotated_peaks = ecg.anno_cs
            elif setup == 'einthoven':
                data = ecg.einthoven_II * 1000
                anno_exists = ecg.anno_cables_exists
                annotated_peaks = ecg.anno_cables
            else:
                tqdm.write(f'Error: Unkwnon setup {setup}')
                break

            if not anno_exists:
                tqdm.write(f'No annotations for setup {setup}, '
                           f'subject {subject}, condition {experiment} '
                           'Skipping it.')
                continue
            else:
                for name, detector in tqdm(detectors.get_detector_list(),
                                           desc='Detector', leave=True):
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
    df_cheststrap =check_all('chest_strap')
    df_einthoven = check_all('einthoven')
