# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:47:23 2021

@author: Korean_Crimson
"""

import math
import pytest
import numpy
from music_mood_analysis.dataconversion import DownConverter

@pytest.mark.parametrize('point', [
        numpy.int16(2),
        13,
        [2, 3],
        (4, 5),
        numpy.array([1, 2])
        ])
def test_stereo_to_mono(point):
    result = DownConverter._mono(point)
    assert isinstance(result, int), 'dataconversion._mono should return an int'


@pytest.mark.usefixtures("down_samplerate", "random_data")
@pytest.mark.parametrize("chunk_size", [0, 0.1, 1, -1])
def test_extract_data_chunk(down_samplerate, random_data, chunk_size):
    data = random_data #fixture should be of length 2000
    samplerate = down_samplerate #fixture should be 1379
    chunk_index = 0

    data_converter = DownConverter(samplerate, chunk_size=chunk_size)
    data_chunk = data_converter._extract_data_chunk(data, chunk_index)

    expected_length = round(samplerate * chunk_size) if chunk_size > 0 else 0
    if expected_length > len(data):
        expected_length = len(data)

    assert isinstance(data_chunk, type(data)), 'Data chunk should be of the same type as data passed'
    assert len(data_chunk) == expected_length, f'Data chunk expected to be of size {expected_length}'


@pytest.mark.usefixtures("samplerate", "long_random_data")
@pytest.mark.parametrize("conversion_ratio,chunk_size", [
        (1, 0),
        (1, 1),
        (10, 1),
        (10, -1),
        (32, 1),
        (32, 0.05)
        ])
def test_downconvert_chunk(samplerate, long_random_data, conversion_ratio, chunk_size):
    data = long_random_data #fixture should be of length 60000
    chunk_index = 0

    data_converter = DownConverter(samplerate, conversion_ratio, chunk_size)
    downsampled_data = data_converter.downconvert_chunk(data, chunk_index)

    assert isinstance(downsampled_data, list), 'Downsampled data should be of type list'

    samplerate = math.ceil(samplerate / conversion_ratio)
    expected_length = max(math.ceil(samplerate * chunk_size), 0)
    if expected_length > len(data):
        expected_length = math.ceil(len(data) / conversion_ratio)

    assert len(downsampled_data) == expected_length, f'Downsampled data should of length {expected_length}'

@pytest.mark.parametrize("samplerate, expected", [
    (2, 1),
    (3, 1),
    (4, 2),
    (5, 2),
])
def test_down_samplerate(samplerate, expected):
    data_converter = DownConverter(samplerate, conversion_ratio=3)
    assert data_converter.down_samplerate == expected
