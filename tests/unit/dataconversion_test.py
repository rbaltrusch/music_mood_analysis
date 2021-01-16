# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:47:23 2021

@author: Korean_Crimson
"""

import math
import pytest
import numpy
from music_mood_analysis import dataconversion

@pytest.mark.parametrize('point', [numpy.int16(2),
                                   13,
                                   [2, 3],
                                   (4, 5),
                                   numpy.array([1, 2])
                                   ])
def test_stereo_to_mono(point):
    result = dataconversion._mono(point)
    assert isinstance(result, int), 'dataconversion._mono should return an int'


@pytest.mark.usefixture("down_samplerate,random_data")
@pytest.mark.parametrize("chunk_size", [0, 0.1, 1, -1])
def test_extract_data_chunk(down_samplerate, random_data, chunk_size):
    data = random_data #fixture should be of length 2000
    samplerate = down_samplerate #fixture should be 1379
    chunk_index = 0

    data_chunk = dataconversion._extract_data_chunk(samplerate, data, chunk_size, chunk_index)

    expected_length = round(samplerate * chunk_size) if chunk_size > 0 else 0
    if expected_length > len(data):
        expected_length = len(data)

    assert isinstance(data_chunk, type(data)), 'Data chunk should be of the same type as data passed'
    assert len(data_chunk) == expected_length, f'Data chunk expected to be of size {expected_length}'


@pytest.mark.usefixture("samplerate,long_random_data")
@pytest.mark.parametrize("conversion_ratio,chunk_size", [(1, 0),
                                                         (1, 1),
                                                         (10, 1),
                                                         (10, -1),
                                                         (32, 1),
                                                         (32, 0.05)
                                                         ])
def test_downconvert_chunk(samplerate, long_random_data, conversion_ratio, chunk_size):
    data = long_random_data #fixture should be of length 60000
    chunk_index = 0

    downsampled_samplerate, downsampled_data = dataconversion.downconvert_chunk(samplerate,
                                                                                data,
                                                                                conversion_ratio,
                                                                                chunk_size,
                                                                                chunk_index)

    assert isinstance(downsampled_data, list), 'Downsampled data should be of type list'
    assert isinstance(downsampled_samplerate, int), 'Downsampled samplerate should be of type int'

    expected_down_samplerate = math.ceil(samplerate / conversion_ratio)
    message = f'Expected downsampled_samplerate = {expected_down_samplerate}, got {downsampled_samplerate}'
    assert downsampled_samplerate == expected_down_samplerate, message

    expected_length = math.ceil(expected_down_samplerate * chunk_size)
    if expected_length < 0:
        expected_length = 0
    if expected_length > len(data):
        expected_length = math.ceil(len(data) / conversion_ratio)

    assert len(downsampled_data) == expected_length, f'Downsampled data should of length {expected_length}'
