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
    tonality_analyser = tonality.TonalityAnalyser(None)
    tonality_ = tonality_analyser._get_tonality(note_counts)
    assert tonality_ == expected, f'Expected tonality = {expected}, but got {tonality_}'

@pytest.mark.xfail()
@pytest.mark.parametrize("note_counts", [
        [random.randint(0, 100) for _ in range(4)],
        [random.randint(0, 100) for _ in range(4)],
        [random.randint(0, 100) for _ in range(4)],
        ])
def test_get_tonality_bad_args(note_counts):
    tonality_analyser = tonality.TonalityAnalyser(None)
    tonality_analyser._get_tonality(note_counts)

@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("data_a")
def test_compute_weighted_note_counts(samplerate, data_a):
    tonality_analyser = tonality.TonalityAnalyser(samplerate)
    weighted_note_counts = tonality_analyser._compute_weighted_note_counts(data_a)
    assert isinstance(weighted_note_counts, list), 'Weighted note counts should be list'
    assert max(weighted_note_counts) > 0, 'Maximum should be above zero'
    assert max(weighted_note_counts) == weighted_note_counts[0], 'Maximum should be A (index 0)'

@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("data_a_minor_chord")
def test_compute_weighted_note_counts2(samplerate, data_a_minor_chord):
    tonality_analyser = tonality.TonalityAnalyser(samplerate)
    weighted_note_counts = tonality_analyser._compute_weighted_note_counts(data_a_minor_chord)
    assert isinstance(weighted_note_counts, list), 'Weighted note counts should be list'
    assert max(weighted_note_counts) > 0, 'Maximum should be above zero'
    assert weighted_note_counts[0] in sorted(weighted_note_counts, reverse=True)[:3], 'A (index 10) should be in the top three note counts'

@pytest.mark.usefixtures("samplerate")
@pytest.mark.usefixtures("data_g_major_chord")
def test_compute_weighted_note_counts3(samplerate, data_g_major_chord):
    tonality_analyser = tonality.TonalityAnalyser(samplerate)
    weighted_note_counts = tonality_analyser._compute_weighted_note_counts(data_g_major_chord)
    assert isinstance(weighted_note_counts, list), 'Weighted note counts should be list'
    assert max(weighted_note_counts) > 0, 'Maximum should be above zero'
    assert weighted_note_counts[10] in sorted(weighted_note_counts, reverse=True)[:3], 'G (index 10) should be in the top three note counts'

@pytest.mark.slow
@pytest.mark.usefixtures("data_g_major_scale")
def test_analyse(samplerate, data_g_major_scale):
    tonality_analyser = tonality.TonalityAnalyser(samplerate)
    tonality_ = tonality_analyser.analyse(data_g_major_scale)
    assert tonality_ == 'G major', 'Should return G major for a G major scale'
