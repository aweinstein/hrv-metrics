"""Export a subset of HRV measures for statistical analysis.
"""
# %%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__)))

SETUP = 'einhoven'

hrv_metrics = pd.read_csv(f'results/HRV/{SETUP}_HRV_results.csv')

# %%

subset = hrv_metrics[['subject_idx', 'method',
                      'experiment', 'HRV_MeanNN',
                      'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVSD',
                      'HRV_CVNN', 'HRV_TINN', 'HRV_HTI', 'HRV_SDRMSSD',
                      'HRV_pNN20', 'HRV_pNN50', 'HRV_IQRNN',
                      'HRV_LF', 'HRV_HF', 'HRV_LFHF', 'HRV_LFn', 'HRV_HFn',
                      'HRV_LnHF', 'HRV_SD1', 'HRV_SD2', 'HRV_SD1SD2',
                      'HRV_SampEn', 'HRV_TP']]
# subset = subset[subset['method'] != 'Engzee']
subset = subset[subset['experiment'] != 'jogging']
nan_values = subset[subset.isnull().any(axis=1)]
print('Number of Null values:', nan_values.shape[0])
# %% Save to csv
subset.to_csv(f'results/{SETUP}_subset_HRV.csv', index_label='index')

# %%
HRV_RMSSD = subset.HRV_RMSSD[np.logical_and(subset.subject_idx == 11,
                                            subset.experiment == 'walking')]
methods = subset.method[HRV_RMSSD.index]
plt.bar(methods, HRV_RMSSD)
plt.xticks(rotation=45)
plt.ylabel('HRV_RMSSD')
plt.title('Subject 11, Experiment walking')
plt.tight_layout()
plt.show()
# %%
