# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:54:21 2021

@author: Korean_Crimson
"""

import numpy

def compute_Yss(samplerate, data):
    '''construct a one-sided amplitude spectrum of Y(t)

    Input args:
        samplerate - int
        data - numpy.array

    Return values:
        Yss: numpy.array (one-dimensional discrete Fourier Transform)
        Yss_f: list (Discrete Fourier Transform sample non-zero positive frequencies)
    '''
    #pylint: disable=C0103
    Yss = numpy.fft.fft(data)
    time_step = 1 / samplerate
    Yss_f = numpy.fft.fftfreq(Yss.size, time_step)
    Yss, Yss_f = list(zip(*[(amplitude, freq) for amplitude, freq in zip(Yss, Yss_f) if freq > 0]))
    return list(Yss), list(Yss_f)

def get_index_of(func, data):
    """returns index of the data point which func (should be in-built min or max)
    would return if called by itself.

    Input args:
        func: function (should be min/max)
        data: iterable

    Return val:
        index: int

    Example:
        index = get_index_of(max, [3, 5, 2]) #returns 1
    """
    index, _ = func(enumerate(data), key=lambda x: x[1])
    return index

def smooth(data, factor=1):
    """Used to smooth data, returns list"""
    return [sum(data[i:i+factor]) for i in range(len(data) - factor + 1)]
