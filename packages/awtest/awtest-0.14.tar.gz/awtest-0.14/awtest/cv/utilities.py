import numpy as np
import datetime

def checkpoint(end, begin):
    seconds_all = (end - begin).seconds
    hours = int(seconds_all / 3600)
    minutes = int((seconds_all - hours * 3600) / 60)
    seconds = seconds_all - hours * 3600 - minutes * 60
    print('{:,} hours, {:,} minutes, and {:,} seconds'.format(hours, minutes, seconds))

def unique_array(iterable):
    return np.unique(np.array([x for x in iterable if str(x) != 'nan' and str(x) != 'None' and str(x).lower() != 'nat']))