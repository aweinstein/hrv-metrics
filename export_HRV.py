"""
Export a subset of HRV metrics for statistical analysis.
"""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

save_path = Path(__file__).resolve().parent /  'results/HRV'

def export_hrv(setup):
    hrv_metrics = pd.read_csv(save_path / f'{setup}_HRV_results.csv')
    subset = hrv_metrics[['subject_idx', 'method', 'experiment', 'HRV_MeanNN',
                          'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVSD',
                          'HRV_CVNN', 'HRV_TINN', 'HRV_HTI', 'HRV_SDRMSSD',
                          'HRV_pNN20', 'HRV_pNN50', 'HRV_IQRNN', 'HRV_LF',
                          'HRV_HF', 'HRV_LFHF', 'HRV_LFn', 'HRV_HFn', 'HRV_LnHF',
                          'HRV_SD1', 'HRV_SD2', 'HRV_SD1SD2', 'HRV_SampEn',
                          'HRV_TP']]
    if setup == 'einthoven':
        subset = subset[subset['experiment'] != 'jogging']
    if setup == 'chest_strap':
        subset = subset[subset['method'] != 'Engzee']

    nan_values = subset[subset.isnull().any(axis=1)]
    print('Number of Null values:', nan_values.shape[0])
    fn = save_path / f'{setup}_subset_HRV.csv'
    subset.to_csv(fn, index_label='index')
    print(f'Subset of HRV metrics for setup {setup} written into {fn}')
    print(subset.info())


if __name__ == '__main__':
    export_hrv('einthoven')
    export_hrv('chest_strap')
