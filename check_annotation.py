"""
Print subject, setup, and condition for which there are no annotations.
"""

from ecg_gudb_database import GUDb
from tqdm import tqdm


nsubjects = 25
experiments = ['sitting', 'maths', 'walking', 'hand_bike', 'jogging']
subjects = range(nsubjects)

for s in tqdm(subjects, desc='Subject'):
    for experiment in tqdm(experiments, desc='Setup', leave=False):
        ecg = GUDb(s, experiment)
        if not ecg.anno_cables_exists:
            tqdm.write(f'Subject {s:2d}, setup Einthoven, condition {experiment}: '
                       'no annotations')
        if not ecg.anno_cs_exists:
            tqdm.write(f'Subject {s:2d}, setup cable strap, condition {experiment}: '
                       'no annotations')
