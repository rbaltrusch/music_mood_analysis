# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:43:43 2021

@author: Korean_Crimson
"""

import math
import numpy

from consts import CONVERSION_RATIO, CHUNK_SIZE
from util import timeit

@timeit
def downconvert(samplerate, data, conversion_ratio=CONVERSION_RATIO):
    '''downsampling algorithm, returns the downsampled samplerate and data.

    Inputs args:
        samplerate: int
        data: numpy.array
        conversion_ratio: int

    Return values:
        downsampled_samplerate: int
        downsampled_data: list
    '''
    downsampled_samplerate = math.ceil(samplerate/conversion_ratio)
    downsampled_data = [_mono(data_point) for i, data_point in enumerate(data) if not i % conversion_ratio]
    return downsampled_samplerate, downsampled_data

@timeit
def downconvert_chunk(samplerate, data, conversion_ratio=CONVERSION_RATIO, chunk_size=CHUNK_SIZE, chunk_index=0):
    '''downsampling algorithm, returns the downsampled samplerate and data for
    a specified data chunk.
    This is useful to analyse data in a data stream (real-time) rather than all at once.

    Inputs args:
        samplerate: int
        data: numpy.array
        conversion_ratio: int
        chunk_size: double (amount of data, specified in seconds)
        chunk_index: int (specifies extracted chunk of data, starts at 0)

    Return values:
        downsampled_samplerate: int
        downsampled_data: numpy.array

    Example: _extract_data_chunk(samplerate, data, 1, 0) #returns the first second of data
    '''
    data_chunk = _extract_data_chunk(samplerate, data, chunk_size, chunk_index)
    return downconvert(samplerate, data_chunk, conversion_ratio)

def _extract_data_chunk(samplerate, data, chunk_size, chunk_index):
    chunk_length = round(chunk_size * samplerate)
    if chunk_length < 0:
        chunk_length = 0

    index = chunk_length * chunk_index
    data_chunk = data[index:index + chunk_length]
    return data_chunk

def _mono(stereo_data_point):
    '''Converts one stereo data point to one mono data point'''
    if isinstance(stereo_data_point, (numpy.int16, int)):
        mono_data_point = int(stereo_data_point)
    else:
        mono_data_point = int(sum(stereo_data_point))
    return mono_data_point
