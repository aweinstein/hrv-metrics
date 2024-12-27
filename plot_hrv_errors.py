import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
from utils import read_info, plot_hrv, save_figs_as_pdf

# %% Read info file
info = read_info()
experiments = info['experiments']
methods_names = np.array(info['methods_names'])
methods_names = methods_names[methods_names != 'Engzee']
setup = 'einthoven'
df_det_hrv = pd.read_csv(f'results/HRV/{setup}_HRV_results.csv')
t_df = df_det_hrv[df_det_hrv.method != 'Annotated']
an_df = df_det_hrv[df_det_hrv.method == 'Annotated']
ann_hrv_arr = an_df.to_numpy().repeat(len(methods_names), axis=0)[:, :-3]
error = abs(t_df[t_df.columns[:-3]] - ann_hrv_arr)
error_df = pd.concat([t_df[t_df.columns[-3:]], error], axis=1)
hrvs = df_det_hrv.columns.tolist()
hrvs.remove('subject_idx')
hrvs.remove('experiment')
hrvs.remove('method')
hrvs.remove('Unnamed: 0')

plt.close('all')
figs = []
for y in tqdm(hrvs):
    fig, ax = plot_hrv(df_det_hrv, x='experiment', y=y, hue='method')
    fig.tight_layout()
    figs.append(fig)
    plt.close(fig)
fn = f'results/HRV/plot_hrv_{setup}.pdf'
print(f'Saving plots into {fn}...')
save_figs_as_pdf(figs, fn)

figs = []
for y in tqdm(hrvs):
    fig, ax = plot_hrv(error_df, x='experiment', y=y, hue='method')
    fig.tight_layout()
    figs.append(fig)
    plt.close(fig)
fn = f'results/HRV/plot_hrv_error_{setup}.pdf'
print(f'Saving plots into {fn}...')
save_figs_as_pdf(figs, fn)
