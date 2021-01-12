# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:54:21 2021

@author: Korean_Crimson
"""

import numpy

def init_zero_list(sampleamount):
    '''returns list of length sampleamount (int), containing zeros (int)'''
    return [0] * sampleamount

def compute_Yss(samplerate, data):
    '''construct a one-sided amplitude spectrum of Y(t)

    Input args:
        samplerate - int
        data - numpy.array

    Return values:
        Yss: numpy.array (one-dimensional discrete Fourier Transform)
        Yss_f: list (Discrete Fourier Transform sample non-zero positive frequencies)
    '''
    Yss = numpy.fft.fft(data)
    time_step = 1 / samplerate
    Yss_f = [freq for freq in numpy.fft.fftfreq(Yss.size, time_step) if freq > 0]
    return Yss, Yss_f

def get_index_of(func, data):
    index, _ = func(enumerate(data), key=lambda x: x[1])
    return index
