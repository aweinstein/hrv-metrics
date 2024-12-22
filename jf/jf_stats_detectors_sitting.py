#!/usr/bin/python3
import numpy as np
import scipy.stats as stats
from ecgdetectors import Detectors
import json
from ecg_gudb_database import GUDb

experiment = 'sitting'

leads = 'einthoven_ii'

detectors = Detectors()
det_names = [i[1].__name__ for i in detectors.get_detector_list()]
plot_names = [i[0] for i in detectors.get_detector_list()]

resultsdir = "results"

alpha = 0.05

minja = 90 # %

def get_jf(detector_name):
    f = open(resultsdir+"/jf_"+detector_name+".json","r")
    js = f.read()
    data = json.loads(js)
    s = []
    for i in data[leads][experiment]:
        if i["jf"]:
            s.append(i["jf"]*100)
    return np.array(s)


def get_result(det):
    m = []
    s = []
    n = 0
    for subject_number in range(0, 25):
        ecg_class = GUDb(subject_number, experiment)
        if ecg_class.anno_cables_exists:
            data_anno = ecg_class.anno_cables
            n = n + len(data_anno)
    for det in det_names:
        print(det,experiment)
        m.append(np.mean(get_jf(det)))
        s.append(np.std(get_jf(det)))

    return n,np.array(m),np.array(s)


def print_result(n,data,std,legend):
    print("JF Score of Einthoven sitting. Stats done on {} QRS complexes:".format(n))
    for i in zip(legend,data,std):
        print("{}: {:1.1f}+/-{:1.1f}".format(i[0],i[1],i[2]))
    print()


n,einthoven_sitting_avg,einthoven_sitting_std = get_result(det_names)

print_result(n,einthoven_sitting_avg,einthoven_sitting_std,det_names)
