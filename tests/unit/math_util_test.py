# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:31:03 2021

@author: Korean_Crimson
"""

import pytest
import numpy
from music_mood_analysis import math_util


@pytest.mark.usefixtures('samplerate')
@pytest.mark.parametrize('data', [
        [1, -1] * 2,
        [1, -1] * 1000,
        numpy.array([1, -1] * 2),
        numpy.array([1, -1] * 10000),
        numpy.ndarray((2, 2)),
        numpy.ndarray((1000, 2))
        ])
def test_compute_Yss(samplerate, data):
    #pylint: disable=C0103
    Yss, Yss_f = math_util.compute_Yss(samplerate, data)
    assert isinstance(Yss, list), 'Yss should be of type numpy.ndarray'
    assert Yss, 'Yss should not be empty'
    assert isinstance(Yss_f, list), 'Yss_f should be of type list'
    assert Yss_f, 'Yss_f should not be empty'
    assert all(x > 0 for x in Yss_f), 'All elements of Yss_f should be positive and non-zero'

@pytest.mark.usefixtures('samplerate')
@pytest.mark.parametrize('data', [[]])
def test_compute_Yss_bad_args(samplerate, data):
    with pytest.raises(Exception):
        math_util.compute_Yss(samplerate, data)

@pytest.mark.usefixtures('samplerate')
@pytest.mark.parametrize('data', [[1], [1, -1]])
def test_compute_Yss_empty_Yss_f(samplerate, data):
    with pytest.raises(ValueError):
        math_util.compute_Yss(samplerate, data)


@pytest.mark.parametrize('func,data,expected', [
        (min, [1, 5, 3], 0),
        (max, [1, 5, 3], 1),
        (min, [0], 0),
        (max, [0], 0),
        (min, [-1, -1000, 2], 1),
        (max, [-1000, -235, -15034, -234, -539], 3)
        ])
def test_get_index_of(func, data, expected):
    index = math_util.get_index_of(func, data)
    message = f'Expected {expected}, but got {index} from math_util.get_index_of({func}, {data})'
    assert index == expected, message

@pytest.mark.parametrize('func,data,exception_type', [
        (min, [], ValueError),
        (max, [], ValueError),
        (lambda *args: 1, [1, 2, 3], TypeError)
        ])
def test_get_index_of_bad_args(func, data, exception_type):
    with pytest.raises(exception_type):
        math_util.get_index_of(func, data)

@pytest.mark.parametrize("frequency,expected,lower,higher", [
        (-1, 0, 440, 880),
        (0, 0, 440, 880),
        (220, 440, 440, 880),
        (440, 440, 440, 880),
        (880, 880, 440, 880),
        (1000, 500, 440, 880),
        (1000, 500, 440, 440),
        ])
def test_normalise(frequency, expected, lower, higher):
    normalised_frequency = math_util.normalise(frequency, lower_bound=lower, higher_bound=higher)
    assert isinstance(normalised_frequency, (int, float)), 'tonality._normalise should return an int or float'
    assert normalised_frequency == expected, f'Expected {expected}, but got {normalised_frequency}'
