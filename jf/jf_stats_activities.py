#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats
from ecgdetectors import Detectors
import json
import sys

experiment_names = ['sitting','maths','walking','hand_bike','jogging']

einth = 'einthoven_ii'
cs = 'chest_strap_V2_V1'

detectors = Detectors()
det_names = [i[1].__name__ for i in detectors.get_detector_list()]

resultsdir = "results"

alpha = 0.05

minjf = 90 # %

def get_jf(detector_name, leads, experiment):
    f = open(resultsdir+"/jf_"+detector_name+".json","r")
    js = f.read()
    data = json.loads(js)
    s = []
    for i in data[leads][experiment]:
        if i["jf"]:
            s.append(i["jf"]*100)
    return np.array(s)


def get_result(det, leads):
    
    m = []
    s = []
    for e in experiment_names:
        m.append(np.mean(get_jf(det, leads, e)))
        s.append(np.std(get_jf(det, leads, e)))

    return m,s


def print_stat(p):
    if p == None:
        print('--- & ',end='')
        return
    s = ""
    if p < alpha:
        s = "*"
    print('{:03.2f}{} & '.format(p,s),end='')

    
def calc_stats(det,leads):
    print("Stats:",det, leads)
    print("      & ",end='')
    for e in experiment_names:
        print(e," & ",end='')
    print("\\\\")
    for e in experiment_names:
        r1 = get_jf(det, leads, e)
        t,p = stats.ttest_1samp(r1,minjf,alternative='greater')
        print_stat(p)
    print()


def multi_plot(data, std, y_label, legend, title=None):
    fig, ax = plt.subplots()
    x_pos = np.arange(len(experiment_names))

    fig.set_size_inches(10, 7)
    width = 1.0 / (len(data)+1)
    rects = []
    for i in range(len(data)):
        rects.append(ax.bar(x_pos+width*i, data[i], width, yerr=std[i], alpha=0.5, ecolor='black', capsize=10))
    ax.set_ylim([0,150])
    ax.set_ylabel(y_label)
    ax.set_xlabel('Experiment')
    ax.set_xticks(x_pos + width / 2)
    ax.set_xticklabels(experiment_names)
    ax.legend(rects, legend)

    if title!=None:
        ax.set_title(title)

    plt.tight_layout()

dets = []
dets.append(det_names[3])
dets.append(det_names[0])
dets.append(det_names[7])
dets.append(det_names[6])

helpstr = "Valid arguments are 'einth' for Einthoven or 'cs' for Chest Strap."

leads = einth
if len(sys.argv) > 1:
    if ('einth' in sys.argv[1]):
        leads = einth
    elif ('cs' in sys.argv[1]):
        leads = cs
    else:
        print(helpstr)
        print("Exiting...")
        quit()
else:
    print(helpstr)

print("Leads:",leads)
print("Dets:",dets)

avg = []
std = []
for d in dets:
    a,s = get_result(d, leads)
    avg.append(a)
    std.append(s)

multi_plot(avg,std,
        'JF (%)', dets, leads)


for d in dets:
    calc_stats(d, leads)

plt.show()
