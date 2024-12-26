"""
Script to compute HRV metrics
"""
# %% Import libraries and ecg_class
from pathlib import Path
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import neurokit2 as nk
from tqdm import tqdm
from utils import read_info, plot_hrv, make_peaks_file_name

# %% Read info file
info = read_info()
core_df = pd.read_csv('results/core_df.csv')
subject_list = np.unique(core_df['subject_idx'])
experiments = info['experiments']
methods_names = np.array(info['methods_names'])
methods_names = methods_names[methods_names != 'Engzee']
setup = 'einthoven'
FS = 250  # This should be inside the info file
read_path = Path('results/rr_detection')
save_path = Path('results/HRV')

# %% Open detected peaks file
df_det_hrv = pd.DataFrame()
df_ann_hrv = pd.DataFrame()

for s in tqdm(subject_list, desc='Subject'):
    for experiment in tqdm(experiments, desc='Condition'):

        ann_file = read_path / make_peaks_file_name(s, setup, experiment, 'annotated')
        try:
            annotated_peaks = np.load(ann_file)
        except FileNotFoundError:
            tqdm.write(f'Skip subject {s}, experiemnt {experiment}.')
            core_df = core_df[np.logical_and(core_df.subject_idx !=
                              s, core_df.experiment != experiment)]
            continue

        # Compute HRV
        ann_hrv = nk.hrv(annotated_peaks, FS)
        ann_hrv['method'] = 'Annotated'
        ann_hrv['experiment'] = experiment
        ann_hrv['subject_idx'] = s

        df_ann_hrv = pd.concat([df_ann_hrv, ann_hrv])

        for method in tqdm(methods_names, desc='Method', leave=False):

            det_file = read_path / make_peaks_file_name(s, setup, experiment, method)
            try:
                detected_peaks = np.load(det_file)
            except FileNotFoundError:
                tqdm.write(f'skip subject {s}: {method}')
                # core_df = core_df[core_df.subject_idx !=
                #                  s and core_df.method != method]
                continue

            det_hrv = nk.hrv(detected_peaks, FS)
            det_hrv['method'] = method
            det_hrv['experiment'] = experiment
            det_hrv['subject_idx'] = s

            df_det_hrv = pd.concat([df_det_hrv, det_hrv])

df_det_hrv = pd.concat([df_det_hrv, df_ann_hrv], axis=0)
df_det_hrv = df_det_hrv.set_index(np.arange(len(df_det_hrv)))
df_det_hrv.to_csv(save_path / f'{setup}_HRV_results.csv')

# %% Compute error

t_df = df_det_hrv[df_det_hrv.method != 'Annotated']
an_df = df_det_hrv[df_det_hrv.method == 'Annotated']

ann_hrv_arr = an_df.to_numpy().repeat(len(methods_names),
                                      axis=0)[:, :-3]
error = abs(t_df[t_df.columns[:-3]] - ann_hrv_arr)

error_df = pd.concat([t_df[t_df.columns[-3:]], error], axis=1)

# %% Plot Mean HRV precission

fig, ax = plt.subplots(figsize=(7, 4))
ax = sns.barplot(df_det_hrv,
                 x='method', y='HRV_MeanNN',
                 hue='experiment', ax=ax)

plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
         45, ha="left", rotation_mode="anchor")

plt.legend(ncol=3)

# plt.show()

# %% Plot SDNN

fig, ax = plt.subplots(figsize=(7, 4))
ax = sns.barplot(df_det_hrv, x='method', y='HRV_SDNN',
                 hue='experiment', ax=ax)

plt.setp(ax.xaxis.get_majorticklabels(), rotation=-
         45, ha="left", rotation_mode="anchor")

plt.legend(ncol=3)

# plt.show()
plt.close('all')

# %%
data = df_det_hrv
for y in det_hrv.columns:
    fig, ax = plot_hrv(data, x='experiment', y=y, hue='method')
    fig.tight_layout()
    fig.savefig(f'results/HRV/plot_{y}.pdf')
    fig.savefig(f'results/HRV/plot_{y}.png')

    fig.clf()
    plt.close()
# %% Save error figures

data = error_df

for y in det_hrv.columns:
    fig, ax = plot_hrv(data, x='experiment', y=y, hue='method')
    fig.tight_layout()
    fig.savefig(f'results/HRV/error_plot_{y}.pdf')
    fig.savefig(f'results/HRV/error_plot_{y}.png')

    fig.clf()
    plt.close()
