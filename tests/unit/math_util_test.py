# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:31:03 2021

@author: Korean_Crimson
"""

import pytest
import numpy
from music_mood_analysis import math_util

@pytest.mark.parametrize('sampleamount', [-1, 0, 1, 10, 1000])
def test_init_zero_list(sampleamount):
    result = math_util.init_zero_list(sampleamount)

    expected_length = sampleamount if sampleamount > 0 else 0
    message = f'init_zero_list should return a list of length {expected_length}'
    assert len(result) == expected_length, message

    all_zeros = all(x == 0 for x in result)
    assert all_zeros, 'init_zero_list should return a list filled with zeros'

@pytest.mark.xfail()
@pytest.mark.parametrize('sampleamount', [[], 'test', {'a': 2}, {'b'}])
def test_init_zero_list_bad_args(sampleamount):
    math_util.init_zero_list(sampleamount)


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

@pytest.mark.xfail()
@pytest.mark.usefixtures('samplerate')
@pytest.mark.parametrize('data', [[]])
def test_compute_Yss_bad_args(samplerate, data):
    #pylint: disable=C0103
    math_util.compute_Yss(samplerate, data)

@pytest.mark.xfail()
@pytest.mark.usefixtures('samplerate')
@pytest.mark.parametrize('data', [[1], [1, -1]])
def test_compute_Yss_empty_Yss_f(samplerate, data):
    _, Yss_f = math_util.compute_Yss(samplerate, data)
    assert Yss_f, 'Yss_f should not be empty'


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

@pytest.mark.xfail()
@pytest.mark.parametrize('func,data', [
        (min, []),
        (max, []),
        (lambda *args: 1, [1, 2, 3])
        ])
def test_get_index_of_bad_args(func, data):
    math_util.get_index_of(func, data)
