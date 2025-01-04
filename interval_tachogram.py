"""
Plot interval tachogram for each subject, method, and condition.
"""
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utils import read_info, save_figs_as_pdf, make_peaks_file_name, subjects
from tqdm import tqdm

results_path = Path(__file__).resolve().parent /  'results'
info = read_info()
experiments = info['experiments']
methods_names = info['methods_names']

FS = 250  # This should be inside the info file
read_path = results_path / 'rr_detection'


def plot_tachograms(setup):
    figs = []
    for s in tqdm(subjects, desc='Subject'):
        for experiment in tqdm(experiments, desc='Condition'):
            # Load annotated peaks
            ann_file = read_path / make_peaks_file_name(s, setup, experiment, 'annotated')
            try:
                annotated_peaks = np.load(ann_file)
            except FileNotFoundError:
                tqdm.write(f'Skip subject {s}, experiemnt {experiment}.')
                continue

            # Compute tachogram of annotated peaks
            ann_tachogram = np.diff(annotated_peaks) / FS

            for method in tqdm(methods_names, desc='Method', leave=False):
                det_file = read_path / make_peaks_file_name(s, setup, experiment, method)
                try:
                    detected_peaks = np.load(det_file)
                except FileNotFoundError:
                    tqdm.write(f'skip subject {s}: {method}')
                    continue
                det_tachogram = np.diff(detected_peaks) / FS
                bins = np.linspace(np.amin(ann_tachogram),
                                   np.amax(ann_tachogram), 50)

                fig, axs = plt.subplots(2, 1, sharex=True, sharey=True)
                axs[0].hist(det_tachogram, bins=bins, color='purple')
                title = f'Setup {setup}, subject {s}, condition {experiment}, ' \
                    f'method {method}'
                axs[0].set_title(title)

                axs[1].hist(ann_tachogram, bins=bins, color='teal')
                axs[1].set_title('Annotated Tachogram')
                axs[1].set_xlabel('RR interval (s)')
                plt.close(fig)
                figs.append(fig)

    save_figs_as_pdf(figs, results_path /f'tachogram_{setup}.pdf')


if __name__ == '__main__':
    plot_tachograms('einthoven')
    plot_tachograms('chest_strap')
