# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:29:33 2021

@author: Korean_Crimson
"""

from music_mood_analysis import tempo
import pytest

@pytest.mark.slow
@pytest.mark.parametrize("indexes,expected", [
        ([10, 100], [90]),
        ([0, 2], [2]),
        ([0, 1], [1])
        ])
def test_compute_beat_distances(indexes, expected):
    tempo_analyser = tempo.TempoAnalyser(None)
    tempo_analyser._local_maximum_values = [tempo.DataPoint(i, 0, 0) for i in indexes]
    beat_distances = tempo_analyser._compute_beat_distances()
    assert isinstance(beat_distances, list), 'beat_distances should be of type list'
    assert beat_distances == expected, f'Expected {expected}, but got {beat_distances}'

@pytest.mark.slow
@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.usefixtures("random_rhythmic_data")
def test_compute_local_maximum_values(down_samplerate, random_rhythmic_data):
    tempo_analyser = tempo.TempoAnalyser(down_samplerate)

    tempo_analyser.processed_data = random_rhythmic_data
    tempo_analyser._compute_local_maximum_values()
    local_maximum_values = tempo_analyser._local_maximum_values
    assert isinstance(local_maximum_values, list), 'local_maximum_values should be of type list'

    non_zero_vals = [x.value for x in local_maximum_values]
    lower, upper = 6, 12
    assert lower < len(non_zero_vals) < upper, f'Expected total of values in range {lower}:{upper}, got {len(non_zero_vals)}'

@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.parametrize("beat_distances,expected", [
        ([690, 690], 120),
        ([230, 0, 500, 560], 148),
        ([230, 0, 500, 549], 151),
        ([], 0),
        ([500, 300, 200, 800, 798], 104),
        ([600, 500, 498], 165)
        ])
def test_compute_bpm_random(down_samplerate, beat_distances, expected):
    tempo_analyser = tempo.TempoAnalyser(down_samplerate)
    tempo_analyser._compute_beat_distances = lambda: beat_distances
    bpm = tempo_analyser._compute_bpm()
    assert isinstance(bpm, int), 'Bpm should be int'
    assert bpm == expected, f'Expected value to be {expected}, but got {bpm}'

@pytest.mark.unreliable
@pytest.mark.slow
@pytest.mark.usefixtures("down_samplerate")
@pytest.mark.usefixtures("random_rhythmic_data")
@pytest.mark.parametrize("tempo_analyser_type", [tempo.TempoAnalyser, tempo.FFTTempoAnalyser])
def test_analyse(tempo_analyser_type, down_samplerate, random_rhythmic_data):
    """This test very rarely fails, due to the random input data"""
    data = random_rhythmic_data
    tempo_analyser = tempo_analyser_type(down_samplerate)
    bpm = tempo_analyser.analyse(data)
    assert isinstance(bpm, int), 'Bpm should be int'

    lower, upper = 110, 130
    assert lower < bpm < upper, f'Expected result to be in range {lower}:{upper}, but got {bpm}'

@pytest.mark.usefixtures("samplerate")
def test_beat_distance_constants(samplerate):
    tempo_analyser = tempo.TempoAnalyser(samplerate)
    min_distance = tempo_analyser.beat_min_dist
    max_distance = tempo_analyser.beat_max_dist
    assert min_distance < max_distance, "Minimum distance should be smaller than maximum distance"
