# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:29:33 2021

@author: Korean_Crimson
"""

from music_mood_analysis import tempo
import pytest

@pytest.mark.parametrize("value,boundary,allowance_percentage,expected", [
        (0, 0, 0, True),
        (1, 1, 0, True),
        (0, 1, 0, False),
        (440, 441, 0.01, True)
        ])
def test_is_in_bounds(value, boundary, allowance_percentage, expected):
    tempo.allowance_percentage = allowance_percentage
    result = tempo._is_in_bounds(value, boundary)
    assert isinstance(result, bool), 'Result should be bool'
    assert result == expected, f'Expected {expected}, but got {result}'

@pytest.mark.xfail
@pytest.mark.parametrize("value,boundary,allowance_percentage,expected", [
        (-12, -10, 0.3, True)
        ])
def test_is_in_bounds_negative(value, boundary, allowance_percentage, expected):
    tempo.allowance_percentage = allowance_percentage
    result = tempo._is_in_bounds(value, boundary)
    assert result == expected, f'Expected {expected}, but got {result}'

@pytest.mark.parametrize("values,allowance_percentage,expected", [
        ([1, 1], 0, True),
        ([1, 1.00001], 0, False),
        ([1, 1.1], 0.1, True),
        ([1, -1], 0.1, False),
        ([0, 0.01], 0.1, False)
        ])
def test_are_closely_matching(values, allowance_percentage, expected):
    tempo.allowance_percentage = allowance_percentage
    result = tempo._are_closely_matching(values)
    assert isinstance(result, bool), 'Result should be bool'
    assert result == expected, f'Expected {expected}, but got {result}'

@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.parametrize("durations_between_beats,expected", [
        ([], 0),
        ([500], 500),
        ([400, 500, 600], 500),
        ([423, 1099, 568, 793], 1099),
        ])
def test_find_first_hypothesis(down_samplerate, durations_between_beats, expected):
    hypothesis = tempo.find_first_hypothesis(down_samplerate, durations_between_beats)
    assert isinstance(hypothesis, (int, float)), 'Hypothesis should be int or float'
    assert hypothesis == expected, f'Expected {expected}, but got {hypothesis}'

@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.parametrize("data,expected", [])
def test_compute_beat_distances(down_samplerate, data, expected):
    beat_distances = tempo.compute_beat_distances(down_samplerate, data)
    assert isinstance(beat_distances, list), 'beat_distances should be of type list'
    assert beat_distances == expected, f'Expected {expected}, but got {beat_distances}'

@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.parametrize("data, expected", [])
def test_compute_local_maximum_values(down_samplerate, data, expected):
    local_maximum_values = tempo.compute_local_maximum_values(down_samplerate, data)
    assert isinstance(local_maximum_values, list), 'local_maximum_values should be of type list'
    assert local_maximum_values == expected, f'Expected {expected}, but got {local_maximum_values}'

@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.parametrize("beat_distances,expected", [])
def test_compute_bpm(down_samplerate, beat_distances, expected):
    bpm = tempo.compute_bpm(down_samplerate, beat_distances)
    assert isinstance(bpm, int), 'Bpm should be int'
    assert bpm == expected, f'Expected {expected}, but got {bpm}'

@pytest.mark.slow
@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.parametrize("data,expected", [])
def test_analyse(down_samplerate, data, expected):
    bpm = tempo.analyse(down_samplerate, data)
    assert isinstance(bpm, int), 'Bpm should be int'
    assert bpm == expected, f'Expected {expected}, but got {bpm}'
