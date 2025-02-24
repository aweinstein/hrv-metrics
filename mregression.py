import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import save_figs_as_pdf


def get_data_method(df, method, metric):
    dfr = df[(df['method'] == method) | (df['method']=='Annotated')]
    # Only keep the metric at hand
    drop_cols = [m for m in metrics if m != metric]
    dfr = dfr.drop(columns=drop_cols)
    dfr['annotated'] = np.nan

    for idx in dfr['subject_idx'].unique():
        for experiment in experiments:
            try:
                annotated = dfr[(dfr['subject_idx']==idx) &
                                (dfr['method'] == 'Annotated') &
                                (dfr['experiment'] == experiment)][metric].iloc[0]
            except IndexError:
                print(f'Subject {idx}, Annotated, experiment {experiment}, metric {metric} is missing')
            else:
                dfr.loc[(dfr['subject_idx']==idx) &
                         (dfr['method'] == method) &
                         (dfr['experiment'] == experiment), ['annotated']] = annotated

    # We don't need the annotated rows anymore
    dfr = dfr[dfr['method']!='Annotated']
    return dfr


def plot_regression(df, df_ccc, metric, method, ax=None, skip_exp=[], lfontsize='medium'):
    if ax is None:
        fig, ax = plt.subplots(layout='constrained')
    dfr = get_data_method(df, method, metric)
    df_ccc = df_ccc.query('method == @method and metric == @metric')
    for experiment in experiments:
        if experiment in skip_exp: continue
        ccc = df_ccc.query('experiment == @experiment')['ccc'].iloc[0]
        ccc =  (int(ccc*100) % 100) / 100 # Get two decimal point without rounding
        data = dfr[dfr['experiment']==experiment]
        label = f'{experiment} ({ccc:.2f})'
        sns.regplot(data=data, x='annotated', y=metric, ci=None, ax=ax,
                    label=label, scatter_kws={"s": 10})

    x = [dfr['annotated'].min(), dfr['annotated'].max()]
    ax.plot(x, x, linestyle=':')
    ax.set_title(method)
    ax.legend(loc='best', fontsize=lfontsize)
    return ax


def plot_regressions(df, df_ccc, metric, skip_exp=[]):
    rows, cols = 2, 4
    fig, axs = plt.subplots(rows, cols, layout='constrained', figsize=(19.2, 9.8))

    for method, ax in zip(methods, axs.flat):
        plot_regression(df, df_ccc, metric, method, ax, skip_exp)

    for i in range(rows):
        for j in range(cols):
            if j == 0:
                axs[i,j].set_ylabel(metric.split('_')[1])
            else:
                axs[i,j].set_ylabel('')
            if (i == 0) and (j < 3):
                axs[i,j].set_xlabel('')

    legend_panel = axs[-1,-1]
    legend_panel.axis('off')
    return fig


def plot_setup_regressions(df, df_ccc, fn, skip_exp=[]):
    figs = []
    for metric in metrics:
        print('Plotting ', metric)
        fig = plot_regressions(df, df_ccc, metric, skip_exp)
        figs.append(fig)
        plt.close(fig)

    print('Saving everything in one PDF file...')
    save_figs_as_pdf(figs, fn)


def plot_all_regressions():
    plt.close('all')

    df = pd.read_csv('datahrv/chest_strap_setup_subset_HRV_notEngzee.csv')
    df = df.drop(columns=['index'] + ['HRV_SDRMSSD.1']) # data cleaning
    df_ccc = pd.read_csv('datahrv/ccc_chest_strap_df.csv')
    plot_setup_regressions(df, df_ccc, 'figures/regressions_chest_strap.pdf')

    df = pd.read_csv('datahrv/einthoven_subset_HRV_not_jogging_with_Engzee.csv')
    df_ccc = pd.read_csv('datahrv/ccc_einthoven_df.csv')
    plot_setup_regressions(df, df_ccc, 'figures/regressions_einthoven.pdf', skip_exp=['jogging'])


def plot_paper_regression_one_fig():
    plt.close('all')
    df = pd.read_csv('datahrv/chest_strap_setup_subset_HRV_notEngzee.csv')
    df = df.drop(columns=['index'] + ['HRV_SDRMSSD.1']) # data cleaning
    df_ccc = pd.read_csv('datahrv/ccc_chest_strap_df.csv')
    rows, cols = 3, 7
    _, axs = plt.subplots(rows, cols, layout='constrained', figsize=(24, 8))
    metrics = ['HRV_MeanNN', 'HRV_TINN', 'HRV_LFHF']
    # Que metodos mostramos?
    # methods = ['Matched_filter', 'Wavelet_transform', 'Christov']

    for i, metric in enumerate(metrics):
        for method, ax in zip(methods, axs[i,:].flat):
            plot_regression(df, df_ccc, metric, method, ax, lfontsize='xx-small')
        for j in range(cols):
            axs[i,j].set_ylabel(metric.split('_')[1])
            axs[i,j].set_xlabel('annotated ' + metric.split('_')[1])

    fn ='figures/regression.pdf'
    plt.savefig(fn)
    print('Figure saved as', fn)


def plot_paper_regression():
    plt.close('all')
    df = pd.read_csv('datahrv/chest_strap_setup_subset_HRV_notEngzee.csv')
    df = df.drop(columns=['index'] + ['HRV_SDRMSSD.1']) # data cleaning
    df_ccc = pd.read_csv('datahrv/ccc_chest_strap_df.csv')
    rows, cols = 2, 4
    metrics = ['HRV_MeanNN', 'HRV_TINN', 'HRV_LFHF']

    for metric in metrics:
        _, axs = plt.subplots(rows, cols, layout='constrained', figsize=(12.2, 6))
        for method, ax in zip(methods, axs.flat):
            plot_regression(df, df_ccc, metric, method, ax, lfontsize='small')
            ax.set_ylabel(metric.split('_')[1])
            ax.set_xlabel('annotated ' + metric.split('_')[1])
        axs[-1,-1].axis('off')

        fn =f'figures/regression_{metric}.pdf'
        plt.savefig(fn)
        print('Figure saved as', fn)


pd.options.mode.copy_on_write = True
methods = ['Elgendi_et_al', 'Matched_filter', 'Wavelet_transform', 'Christov',
           'Hamilton', 'Pan_Tompkins', 'WQRS']
metrics = ['HRV_MeanNN', 'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVSD',
           'HRV_CVNN', 'HRV_TINN', 'HRV_HTI', 'HRV_SDRMSSD', 'HRV_pNN20',
           'HRV_pNN50', 'HRV_IQRNN', 'HRV_LF', 'HRV_HF', 'HRV_LFHF',
           'HRV_LFn', 'HRV_HFn', 'HRV_LnHF', 'HRV_SD1', 'HRV_SD2',
           'HRV_SD1SD2', 'HRV_SampEn', 'HRV_TP']
experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']


if __name__ == '__main__':
    # plot_all_regressions()
    plot_paper_regression()
