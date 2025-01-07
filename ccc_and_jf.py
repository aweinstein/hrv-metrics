"""
Shows the relationship between CCC and JF.
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

metrics = ['HRV_MeanNN', 'HRV_SDNN', 'HRV_RMSSD', 'HRV_SDSD', 'HRV_CVSD',
           'HRV_CVNN', 'HRV_TINN', 'HRV_HTI', 'HRV_SDRMSSD', 'HRV_pNN20',
           'HRV_pNN50', 'HRV_IQRNN', 'HRV_LF', 'HRV_HF', 'HRV_LFHF',
           'HRV_LFn', 'HRV_HFn', 'HRV_LnHF', 'HRV_SD1', 'HRV_SD2',
           'HRV_SD1SD2', 'HRV_SampEn', 'HRV_TP']

def get_data(setup, metric):
    jf_df = pd.read_csv(f'results/rr_detection/sensitivity_jf_{setup}.csv')
    ccc_df = pd.read_csv(f'datahrv/ccc_{setup}_df.csv')

    if setup == 'chest_strap':
        jf_df = jf_df.query('method != "Engzee"')
    if setup == 'einthoven':
        jf_df = jf_df.query('experiment != "jogging"')

    jf_mean = jf_df.groupby(['method','experiment'])['JF'].mean()
    ccc_metric_df = ccc_df.query('metric == @metric')
    ccc_metric_df = ccc_metric_df.merge(jf_mean.reset_index(),
                                        on=['method', 'experiment'])
    return ccc_metric_df


def compute_rsquared(df):
    Y = df['ccc']
    X = df['JF']
    X = sm.add_constant(X)
    model = sm.OLS(Y, X)
    results = model.fit()
    return results.rsquared


def plot_regressions(setup):
    """
    If `setup` is a string, use the data of the individual setup. If it is a
    list with both setups, concatenate the data.
    """
    print('Regression for', setup)
    rows, cols = 6, 4
    fig, axs = plt.subplots(rows, cols, layout='constrained',
                            figsize=(8.3, 10.2))
    for metric, ax in zip(metrics, axs.flat):
        if isinstance(setup, str):
            df = get_data(setup, metric)
        else:
            df = pd.concat([get_data(setup[0], metric),
                            get_data(setup[1], metric)])
        sns.regplot(data=df, x='JF', y='ccc', ci=None, ax=ax, label=metric,
                    scatter_kws={"s": 10})
        rsquared = compute_rsquared(df)
        title = rf'{metric.split("_")[1]} ($R^2$: {rsquared:.2f})'
        ax.set_title(title)


    for i in range(rows):
        for j in range(cols):
            if j == 0:
                axs[i,j].set_ylabel('CCC')
            else:
                axs[i,j].set_ylabel('')
            if (i < 5):
                axs[i,j].set_xlabel('')
            axs[i,j].set_xlim(df['JF'].min() - 1, 101)
            axs[i,j].set_ylim(- 0.1, 1.1)
    axs[4,3].set_xlabel('JF')
    last_panel = axs[-1,-1]
    last_panel.axis('off')
    return fig


if __name__ == '__main__':
    plt.close('all')
    figs = []
    figs.append(plot_regressions('chest_strap'))
    figs.append(plot_regressions('einthoven'))
    figs.append(plot_regressions(['chest_strap', 'einthoven']))
    save_path = Path(__file__).resolve().parent / 'figures'
    fns = ['ccc_jf_chest_strap.pdf', 'ccc_jf_einthoven.pdf', 'ccc_jf_both.pdf']
    for fn, fig in zip(fns, figs):
        print('Saving figure as', fn)
        fig.savefig(save_path / fn)

    plt.show()
