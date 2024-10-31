# HRV-paper

This is the repository for the paper "Effects of Detection Algorithms of the Electrocardiograms R wave in Heart Rate Variability Metrics" (tentative title). 

This repository contains all the corresponding code. It also includes other issues associated with the paper.ng code here.It also contains other issues associated with the paper.


## Overleaf 

https://www.overleaf.com/project/65fd77e0eff57b3a35134f8f

## Databases

Howell, L. and Porr, B. (2018) High precision ECG Database with annotated R peaks, recorded and filmed under realistic conditions. [Data Collection] (DOI:10.5525/gla.researchdata.716)

Also available through the python api in: https://github.com/berndporr/ECG-GUDB

## Scripts

1. rr_peak_detection.py - Detects QRS peaks for the dataset. One of the parameters of the script is which setup to use. Options are 'Chest strap' or 'Einhoven'
2. compute_hrv.py - Computes HRV metrics. It will use the files in the results folder. The script has a parameter setup, with options: 'Chest strap' or 'Einhoven'. IMPORTANT: You need to make sure the results in the results folder are from the setup option in this script, otherwise, they will be mislabeled during this step.
3. interval_tachogram.py - plots histogram of RR intervals using np.diff
4. export_HRV.py - exports a valid subset of HRV metrics. It also shows which rows in the dataframe contains null values.
5. CS_Jogging_plot.py - Prints which subjects-experiment doesn't have annotations. Plots a sample of the Einhoven and the Chest Strap conditions to demonstrate the difference of noise level between the setups.
6. engzee_plots.py - Plots a sample of the Chest Strap setup when the Engzee method fails.

## Notes

When computing the results. Remember to delete the files already in the results folder otherwise the difference between annotated data in Einhoven and CS datasets could produce errors in the results.

## Requirements

There is a txt file containing the modules needed to run the scripts. Use `pip install -r requirements.txt` in your new enviorment.
The jf_ecg_benchmark needs to be cloned from the following repository: https://github.com/julioRodino/JF-ECG-Benchmark.git and check out into the 'use_as_package' branch.

## References

This Google Drive directory contains some relevant papers:

https://drive.google.com/drive/folders/1_w_WF6XVycLRbn8CZLLKUAgH0dZ8_93I?usp=drive_link
