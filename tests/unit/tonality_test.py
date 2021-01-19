# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:29:38 2021

@author: Korean_Crimson
"""

import random
import pytest
from music_mood_analysis import tonality

@pytest.mark.parametrize("note_counts,expected", [
        ([0, 1, 2, 3, 4], "major"),
        ([50, 230, 4, 25, -5], "minor"),
        ([-50, -3, -35, -45, -60], "minor")
        ])
def test_get_tonality(note_counts, expected):
    tonality_ = tonality._get_tonality(note_counts)
    assert tonality_ == expected, f'Expected tonality = {expected}, but got {tonality_}'

@pytest.mark.xfail()
@pytest.mark.parametrize("note_counts", [
        [random.randint(0, 100) for _ in range(4)],
        [random.randint(0, 100) for _ in range(4)],
        [random.randint(0, 100) for _ in range(4)],
        ])
def test_get_tonality_bad_args(note_counts):
    tonality._get_tonality(note_counts)


@pytest.mark.parametrize("note_counts,index,expected", [
        ([x for x in range(12)], 0, 12), #no wrap
        ([x for x in range(12)], 4, 24), #no wrap
        ([x for x in range(12)], 5, 15), #wrap around once (5th)
        ([x for x in range(12)], 7, 9), #wrap around twice (5th and 7th)
        ])
def test_adjust(note_counts, index, expected):
    result = tonality._adjust(note_counts, index)
    assert isinstance(result, int), '_adjust should return an int'
    assert result == expected, f'Expected result={expected}, but got {result}'

@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("data_a")
def test_compute_weighted_note_counts(samplerate, data_a):
    weighted_note_counts = tonality.compute_weighted_note_counts(samplerate, data_a)
    assert isinstance(weighted_note_counts, list), 'Weighted note counts should be list'
    assert max(weighted_note_counts) > 0, 'Maximum should be above zero'
    assert max(weighted_note_counts) == weighted_note_counts[0], 'Maximum should be A (index 0)'

@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("data_a_minor_chord")
def test_compute_weighted_note_counts2(samplerate, data_a_minor_chord):
    weighted_note_counts = tonality.compute_weighted_note_counts(samplerate, data_a_minor_chord)
    assert isinstance(weighted_note_counts, list), 'Weighted note counts should be list'
    assert max(weighted_note_counts) > 0, 'Maximum should be above zero'
    assert weighted_note_counts[0] in sorted(weighted_note_counts, reverse=True)[:3], 'A (index 10) should be in the top three note counts'

@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("data_g_major_chord")
def test_compute_weighted_note_counts3(samplerate, data_g_major_chord):
    weighted_note_counts = tonality.compute_weighted_note_counts(samplerate, data_g_major_chord)
    assert isinstance(weighted_note_counts, list), 'Weighted note counts should be list'
    assert max(weighted_note_counts) > 0, 'Maximum should be above zero'
    assert weighted_note_counts[10] in sorted(weighted_note_counts, reverse=True)[:3], 'G (index 10) should be in the top three note counts'

@pytest.mark.slow
@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("random_data")
def test_count_musical_notes(samplerate, random_data):
    note_counts = tonality.count_musical_notes(samplerate, random_data)
    weighted_note_counts = tonality.compute_weighted_note_counts(samplerate, random_data)
    assert isinstance(note_counts, list), 'Note counts should be of type list'
    assert len(note_counts) == 12, 'Note counts should be of length 12'
    assert note_counts == weighted_note_counts, 'count_musical_notes should return the same result as compute_weighted_note_counts'

@pytest.mark.parametrize("frequency,expected", [
        (-1, 0),
        (0, 0),
        (220, 440),
        (440, 440),
        (880, 880),
        (1000, 500)
        ])
def test_normalise(frequency, expected):
    normalised_frequency = tonality._normalise(frequency)
    assert isinstance(normalised_frequency, (int, float)), 'tonality._normalise should return an int or float'
    assert normalised_frequency == expected, f'Expected {expected}, but got {normalised_frequency}'

@pytest.mark.slow
@pytest.mark.usefixtures("data_g_major_scale")
def test_analyse(samplerate, data_g_major_scale):
    tonality_, key = tonality.analyse(samplerate, data_g_major_scale)
    assert tonality_ == 'major', 'Should return G major for a G major scale'
    assert key == 'G', 'Should return key == G for a G major scale'
