# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:57:06 2021

@author: Korean_Crimson
"""

import matplotlib.pyplot as plt
from consts import PLOTTING_ENABLED

def plot(*datasets, xlabel='x', ylabel='y', title='Plot', normalised=False):
    '''Plots a number of datasets on subplots. If only one dataset is specified,
    a single plot is created. Does nothing if consts.PLOTTING_ENABLED = False.

    Input args:
        *datasets: list of lists
        xlabel: string
        ylabel: string
        title: string

    Return values:
        None
    '''
    if PLOTTING_ENABLED:
        plt.figure()
        _, subplot = plt.subplots(1)
        for data in datasets:
            if normalised:
                data = _normalise(data)
            subplot.plot(data)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.show()

def _normalise(data):
    max_val = max(data)
    data = [val / max_val for val in data]
    return data
