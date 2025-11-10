"""
Show the duration of the ECGs for all subjects, setups, and conditions.
"""
from pathlib import Path
import numpy as np
from tqdm import tqdm
from ecg_gudb_database import GUDb
import pandas as pd


def duration_single_case(s, experiment, setup):
    ecg = GUDb(s, experiment)

    if setup == 'Einthoven':
        # annotated = ecg.anno_cables_exists
        # annotated_peaks = ecg.anno_cables
        data = ecg.einthoven_II

    elif setup == 'Chest strap':
        # annotated = ecg.anno_cs_exists
        # annotated_peaks = ecg.anno_cs
        data = ecg.cs_V2_V1

    fs = 250
    duration = len(data) / fs

    d = {'subject': s, 'condition': experiment, 'setup': setup,
         'duration': duration}
    return d


def duration_all_ecg(setup):
    rows = []
    for s in tqdm(subjects, desc='Subject'):
        for experiment in tqdm(experiments, desc='Condition', leave=False):
            rows.append(duration_single_case(s, experiment, setup))
    return pd.DataFrame(rows)

if __name__ == '__main__':
    save_path = Path(__file__).resolve().parent /  'results'
    subjects = np.arange(0, 24)
    experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
    figs_annotated, figs_nonannotated = [], []
    df_einthoven = duration_all_ecg('Einthoven')
    df_chest_strap = duration_all_ecg('Chest strap')
    df = pd.concat([df_einthoven, df_chest_strap], ignore_index=True)

    fn = save_path / 'duration_ecg.csv'
    df.to_csv(fn, index=False)
    print('Durations saved into', fn)
