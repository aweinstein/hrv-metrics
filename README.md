# HRV-paper
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15213192.svg)](https://doi.org/10.5281/zenodo.15213192)

This is the repository for the paper "Effects of Detection Algorithms of the Electrocardiograms R wave in Heart Rate Variability Metrics." It contains all the necessary code to reproduce the paper's results.

## Requirements

You can install the dependencies with `pip install -r requirements.txt`. This code also depends on the code from the [jf_ecg_benchmark repository](https://github.com/berndporr/JF-ECG-Benchmark). Since this code can not be installed using `pip` at the moment, it is included in the repository.

## Instructions

To reproduce the paper's results run the following scripts:

- Figure 2: ```jogging_example.py```.
- Figure 3: ```vis_eeg.py```.
- Figure 4: ```ccc_barplot.py```. 
- Figure 5: ```mregression.py```.
- Figure 6: ```ccc_and_jf.py```.

## Scripts

The following is a description of all the scripts in the repository:

- ```ccc_and_jf.py```: Shows the relationship between CCC and JF.
- ```ccc_barplot.py```: Makes CCC plots.
- ```check_annotation.py```: Print subject, setup, and condition for which there are no annotations.
- ```compute_hrv.py```:  Compute HRV for all subjects, conditions, methods, and setups.
- ```export_HRV.py```: Exports a valid subset of HRV metrics. It also shows which rows in the dataframe contains null values.
- ```find_failed_detectors.py```: Finds detectors that fails to detect 10 or more R peaks.
- ```interval_tachogram.py```: Plots histogram of RR intervals using np.diff
- ```jogging_example.py```: Plots an example of the ECGs for Einthoven and the Chest Strap setup to demonstrate the difference of noise level between the setups.
- ```mregression.py```: Makes multiple regression plots.
- ```neurokit_vs_Porr.py```: Compare Porr, Neurokit, and Neurokit with clean data.
- ```plot_all_ecgs.py```: Plot the ECGs for all subjects, setups, and conditions.
- ```rr_peak_detection.py```: Detects QRS peaks for all subjects, conditions, and setups.
- ```utils.py```: Utility functions.
- ```vis_eeg.py```: Functions to visualize the ECG and the annotations.


## Databases

This work uses the database [Howell, L. and Porr, B. (2018) High precision ECG Database with annotated R peaks, recorded and filmed under realistic conditions.](https://doi.org/DOI:10.5525/gla.researchdata.716). It can be accesed through a [Python API.](https://github.com/berndporr/ECG-GUDB).
