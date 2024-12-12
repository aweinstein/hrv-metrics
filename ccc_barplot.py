"""
Plot the CCC for all HRV metrics and R-peak detector methods.
Plot based on grouped bar chart example
https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# TODO: Import from multipage_pdf
from matplotlib.backends.backend_pdf import PdfPages
def save_figs_as_pdf(figs, fn):
    if isinstance(figs, list):
        pdf = PdfPages(fn)
        for f in figs:
            pdf.savefig(f)
        pdf.close()
    else:
        figs.savefig(fn, format='pdf')
    print('File %s created' % fn)

metrics = ['HRV_MeanNN', 'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVSD',
           'HRV_CVNN', 'HRV_TINN', 'HRV_HTI', 'HRV_SDRMSSD', 'HRV_pNN20',
           'HRV_pNN50', 'HRV_IQRNN', 'HRV_LF', 'HRV_HF', 'HRV_LFHF',
           'HRV_LFn', 'HRV_HFn', 'HRV_LnHF', 'HRV_SD1', 'HRV_SD2',
           'HRV_SD1SD2', 'HRV_SampEn', 'HRV_TP']


def make_barplot(fn, methods, experiments):
    df = pd.read_csv(fn)
    x = np.arange(len(experiments))  # the label locations
    if len(methods) < 8:
        width = 0.12 # the width of the bars
    else:
        width = 0.1
    rows, cols = 4, 6
    fig, axs = plt.subplots(rows, cols, layout='constrained', figsize=(19.2, 9.8))

    for metric, ax in zip(metrics, axs.flat):
        dfm = df[df['metric'] == metric]
        # TODO: Sort the rows of `dfm` to match `experiments`
        multiplier = 0
        for method in methods:
            data = dfm[dfm['method'] == method]['ccc'].values
            offset = width * multiplier
            rects = ax.bar(x + offset, data, width, label=method)
            multiplier += 1

        ax.set_xticks(x + 3*width, experiments)
        ax.set_ylim(0, 1.1)
        ax.set_title(metric.split('_')[1], y=0.89)

        # See https://pmc.ncbi.nlm.nih.gov/articles/PMC6107969/
        # https://thedatascientist.com/concordance-correlation-coefficient/
        ax.axhline(0.95, color='red', linestyle=':')
        ax.axhline(0.9, color='red', linestyle=':')
        ax.axhline(0.8, color='green', linestyle=':')
        ax.axhline(0.6, color='green', linestyle=':')
        ax.axhline(0.3, color='green', linestyle=':')
        ax.axhline(0.2, color='green', linestyle=':')

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


if __name__ == '__main__':
    plt.close('all')
    methods = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform', 'Christov',
           'Hamilton', 'Pan_Tompkins', 'WQRS']
    experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
    experiments = ['sitting', 'maths', 'walking', 'handbk', 'jogging']

    figs = []
    fig = make_barplot('datahrv/ccc_chest_strap_df.csv', methods, experiments)
    figs.append(fig)


    methods = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform', 'Engzee',
               'Christov', 'Hamilton', 'Pan_Tompkins', 'WQRS']
    experiments = ['sitting', 'maths', 'walking', 'handbk']
    fig = make_barplot('datahrv/ccc_einhoven_df.csv', methods, experiments)
    figs.append(fig)

    plt.show()

    save_figs_as_pdf(figs, 'figures/ccc_barplot.pdf')
