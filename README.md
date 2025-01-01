# HRV-paper

This is the repository for the paper "Effects of Detection Algorithms of the Electrocardiograms R wave in Heart Rate Variability Metrics" (tentative title). 

This repository contains all the corresponding code. It also includes other issues associated with the paper.ng code here.It also contains other issues associated with the paper.

## Databases

Howell, L. and Porr, B. (2018); High precision ECG Database with annotated R peaks, recorded and filmed under realistic conditions. University of Glasgow


[Howell, L. and Porr, B. (2018) High precision ECG Database with annotated R peaks, recorded and filmed under realistic conditions.](https://doi.org/DOI:10.5525/gla.researchdata.716)

[Also available through the Python API.](https://github.com/berndporr/ECG-GUDB)

## Scripts

- ```ccc_barplot.py```: Makes CCC plots.
- ```check_annotation.py```: Print subject, setup, and condition for which there are no annotations.
- ```compute_hrv.py```:  Compute HRV for all subjects, conditions, methods, and setups.
- ```export_HRV.py```: Exports a valid subset of HRV metrics. It also shows which rows in the dataframe contains null values.
- ```find_failed_detectors.py```: Finds detectors that fails to detect 10 or more R peaks.
- ```interval_tachogram.py```: Plots histogram of RR intervals using np.diff
- ```jogging_example.py```: Plots an example of the ECGs for Einthoven and the Chest Strap setup to demonstrate the difference of noise level between the setups.
- ```load_database.py```
- ```make_table.py```
- ```mregression.py```: Makes multiple regression plots.
- ```neurokit_vs_Porr.py```
- ```plot_all_ecgs.py```: Plot the ECGs for all subjects, setups, and conditions.
- ```rr_peak_detection.py```: Detects QRS peaks for all subjects, conditions, and setups.
- ```test_peak_detection.py```
- ```utils.py```: Utility functions.

## Notes

When computing the results. Remember to delete the files already in the results folder otherwise the difference between annotated data in Einhoven and CS datasets could produce errors in the results.

## Requirements

You can install the dependencies with `pip install -r requirements.txt`. This code also depends on the code from the [jf_ecg_benchmark repository](https://github.com/berndporr/JF-ECG-Benchmark). Since, at the moment, this code can not be installed using `pip`, we copy it to the repo.

