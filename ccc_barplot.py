"""
Plot the CCC for all HRV metrics and R-peak detector methods.
Plot based on grouped bar chart example
https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from utils import save_figs_as_pdf


Metrics = ['HRV_MeanNN', 'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVSD',
           'HRV_CVNN', 'HRV_TINN', 'HRV_HTI', 'HRV_SDRMSSD', 'HRV_pNN20',
           'HRV_pNN50', 'HRV_IQRNN', 'HRV_LF', 'HRV_HF', 'HRV_LFHF',
           'HRV_LFn', 'HRV_HFn', 'HRV_LnHF', 'HRV_SD1', 'HRV_SD2',
           'HRV_SD1SD2', 'HRV_SampEn', 'HRV_TP']


def make_barplot(df, methods, experiments, axs, metrics=None, ytitle=0.89):
    if metrics is None:
        metrics = Metrics
    if len(methods) < 8:
        width = 0.12 # the width of the bars
    else:
        width = 0.1

    x = np.arange(len(experiments))  # the label locations
    for metric, ax in zip(metrics, axs.flat):
        dfm = df[df['metric'] == metric]
        # TODO: Sort the rows of `dfm` to match `experiments`
        multiplier = 0
        for method in methods:
            data = dfm[dfm['method'] == method]['ccc'].values
            offset = width * multiplier
            ax.bar(x + offset, data, width, label=method)
            multiplier += 1

        ax.set_xticks(x + 3*width, experiments)
        ax.set_ylim(0, 1.1)
        ax.set_title(metric.split('_')[1], y=ytitle)
        # See https://pmc.ncbi.nlm.nih.gov/articles/PMC6107969/, which recommend
        # the values from
        # Chan, Y. H. "Biostatistics 104: correlational analysis." Singapore Med
        # J 44.12 (2003): 614-619.
        ax.axhline(0.8, color='black', linestyle=':', alpha=0.5)
        ax.axhline(0.5, color='black', linestyle=':', alpha=0.5)
        ax.axhline(0.3, color='black', linestyle=':', alpha=0.5)

    return x, width


def make_barplots(fn, methods, experiments):
    df = pd.read_csv(fn)
    rows, cols = 4, 6
    fig, axs = plt.subplots(rows, cols, layout='constrained', figsize=(19.2, 9.8))
    x, width = make_barplot(df, methods, experiments, axs)

    for i in range(rows):
        for j in range(cols):
            if j == 0:
                axs[i,j].set_ylabel('CCC')
            if j > 0:
                axs[i,j].set_yticks([])
            if i < (rows - 1):
                axs[i,j].set_xticks([])

    axs[rows-2, cols-1].set_xticks(x + 3*width, experiments)

    legend_panel = axs[-1,-1]
    legend_panel.axis('off')
    legend_panel.legend(handles=axs[0, 0].get_legend_handles_labels()[0],
                       labels=axs[0, 0].get_legend_handles_labels()[1],
                       loc="center")

    return fig


def make_all_plots():
    plt.close('all')

    methods = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform', 'Christov',
           'Hamilton', 'Pan_Tompkins', 'WQRS']
    experiments = ['sitting', 'maths', 'walking', 'handbk', 'jogging']

    figs = []
    fig = make_barplots('datahrv/ccc_chest_strap_df.csv', methods, experiments)
    figs.append(fig)


    methods = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform', 'Engzee',
               'Christov', 'Hamilton', 'Pan_Tompkins', 'WQRS']
    experiments = ['sitting', 'maths', 'walking', 'handbk']
    fig = make_barplots('datahrv/ccc_einhoven_df.csv', methods, experiments)
    figs.append(fig)

    plt.show()

    save_figs_as_pdf(figs, 'figures/ccc_barplots.pdf')


def make_paper_plot():
    fn = 'datahrv/ccc_chest_strap_df.csv'
    df = pd.read_csv(fn)
    plt.close('all')
    _, axs = plt.subplots(4, 1, layout='constrained', figsize=(5.38, 7),
                          height_ratios= [1, 1, 1, 0.5])
    methods = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform', 'Christov',
               'Hamilton', 'Pan_Tompkins', 'WQRS']
    experiments = ['sitting', 'maths', 'walking', 'handbk', 'jogging']

    metrics = ['HRV_MeanNN', 'HRV_TINN', 'HRV_LFHF']
    _, _ = make_barplot(df, methods, experiments, axs, metrics, ytitle=1)
    for ax in axs:
        ax.set_ylabel('CCC')

    legend_panel = axs[-1]
    legend_panel.axis('off')
    legend_panel.legend(handles=axs[0].get_legend_handles_labels()[0],
                       labels=axs[0].get_legend_handles_labels()[1],
                        loc="center", ncols=len(methods)//2)
    fn = 'figures/ccc_barplot.pdf'
    plt.savefig(fn)
    print('Figure saved as', fn)
    plt.show()


if __name__ == '__main__':
    make_paper_plot() # Figure with three metrics for chest strap.
    # make_all_plots()  # Figure with all metrics and the two setups.
