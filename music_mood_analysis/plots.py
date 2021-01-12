# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:57:06 2021

@author: Korean_Crimson
"""

from consts import PLOTTING_ENABLED
import matplotlib.pyplot as plt

def plot(*datasets, xlabel='x', ylabel='y', title='Plot'):
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
        for data in datasets:
            plt.subplot()
            plt.plot(data)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        plt.title(title)
        plt.show()
