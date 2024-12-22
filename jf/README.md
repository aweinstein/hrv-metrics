# JF Benchmark Analysis for heartbeat detectors

A benchmarking analysis method that generates an overall benchmark for
ECG detector algorithms, based on measurements of temporal jitter (J)
and (F) score

The Glasgow University GUDB ECG recordings database ([Howell and Porr,
2018](http://dx.doi.org/10.5525/gla.researchdata.716)) is used for
testing as it has annotated R-peaks for reference. The detector
algorithms are tested using recordings for all subjects, all
exercises, and Einthoven II and chest strap leads (Einthoven I and
Einthoven III can additionally be used if desired).

The benchmark gives a score between 0-100 where 100 is defined as the
ideal detector. The ideal detector has
a median absolute deviation (MAD) of zero for temporal jitter
and an F-score of 100%.

[![DOI](https://www.zenodo.org/badge/362771491.svg)](https://www.zenodo.org/badge/latestdoi/362771491)

## Prerequisites

Install `py-ecg-detectors` ([Howell and Porr, 2019](https://doi.org/10.5281/zenodo.3353396)).

via PIP:
```
pip install py-ecg-detectors [--user]
```

From source:
```
python setup.py install [--user]
```
*Use the option --user if you don't have system-wise write permission.*

---
Install ecg_gudb_database ([Howell and Porr, 2018](https://pypi.org/project/ecg-gudb-database/)) via the package manager [pip](https://pip.pypa.io/en/stable/).

```bash
pip install ecg_gudb_database
```

## Usage

### jf_analysis.py

Module which performs the JF analysis. It has no main program.

JF analysis of interval variation and F1 (FP, FN, TP):

```
evaluate(det_posn, anno_R, fs, nSamples, trim=True)
```

Arguments:

    - det_posn: the timestamps of the detector in sample positions
    - anno_R: the ground truth in samples
    - fs: sampling rate of the ECG file
    - nSamples: number of samples in the ECG file
    - trim: trims 2 detections from start/end of det_posn/anno_R


Returns:

    - jf[key_jitter]   : jitter in s
    - jf[key_tp]       : true positive beats
    - jf[key_fp]       : false positive beats
    - jf[key_fn]       : false negative beats
    - jf[key_f1]       : F1 score
    - jf[key_jf]       : JF Score


### jf_evaluate_all_detectors.py

The code evaluates all ECG detectors with all subjects, all leads, and all
experiments. It outputs separate json files for every detector and stores
them in the `results` directory.

Only needs to be run once and then can be analysed by the script below.

### jf_stats_detectors.py

The overall JF Benchmark values of all detectors for Einthoven
II and chest strap results are shown together on a bar graph for
comparison for sitting and jogging.

![alt tag](jf_einth.png)
![alt tag](jf_chest.png)

### jf_stats_activities.py

This analysis focusses how different noise levels affect performance from
sitting to jogging.

![alt tag](jf_activities.png)

## jf_stats_detectors_sitting.py

Prints out the stats for all detectors for Einthoven and sitting. It also
counts the number of QRS complexes used.

# Traditional sensitivity analysis

For a sensitivity analysis on an `fs/10` samples temporal window run:

```
python sensitivity_evaluate_all_detectors.py
python sensitivity_stats_plots.py
```

![alt tag](sensitivity.png)

Note that a pure sensitivity analysis on a wide temporal window
yields mostly 99-100% sensitivity.

# Credit

 - Bernd Porr <bernd.porr@glasgow.ac.uk>
 - Eleanor Forsyth
