# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 17:14:44 2021

@author: Korean_Crimson
"""

import math
import random
import numpy
import pytest
from music_mood_analysis.consts import MUSICAL_NOTES as notes

def _musical_note(freq=440, samplerate=44100, time=2):
    amount_of_data_points = round(samplerate * time)
    data_points = numpy.linspace(0, time, amount_of_data_points)
    return numpy.sin(2 * numpy.pi * freq * data_points)

def _combine_notes(frequencies, scalings=None, samplerate=44100, time=2):
    '''frequencies and offsets need to be of the same length if offsets are passed'''
    scalings = [1] * len(frequencies) if scalings is None else scalings
    combined_data = sum(scaling * _musical_note(freq=freq, samplerate=samplerate, time=time) for freq, scaling in zip(frequencies, scalings))
    assert len(combined_data) == len(_musical_note(freq=frequencies[0], samplerate=samplerate))
    return combined_data

def _short(data, length=2000):
    return data if len(data) <= length else data[:length]

def _select_notes(selected_notes):
    return [notes[note] for note in selected_notes]

@pytest.fixture
def random_data():
    return numpy.random.rand(2000)

@pytest.fixture
def long_random_data():
    return numpy.random.rand(60000)

@pytest.fixture
def data_a(samplerate):
    return _short(_musical_note(freq=440, samplerate=samplerate))

@pytest.fixture
def data_a_minor_chord(samplerate):
    frequencies = _select_notes(['A', 'C', 'E'])
    return _short(_combine_notes(frequencies, samplerate=samplerate))

@pytest.fixture
def data_g_major_chord(samplerate):
    frequencies = _select_notes(['G', 'B', 'D'])
    return _short(_combine_notes(frequencies, samplerate=samplerate))

@pytest.fixture
def data_g_major_scale(samplerate):
    frequencies = _select_notes(['G', 'A', 'B', 'C', 'D', 'E', 'F#'])
    scalings = [1, 0.5, 0.8, 0.7, 0.6, 0.4, 0.2] #scalings from experience
    return _short(_combine_notes(frequencies, scalings, samplerate=samplerate))

@pytest.fixture
@pytest.mark.usefixtures("down_samplerate")
def random_rhythmic_data(down_samplerate):
    samplerate = down_samplerate
    frequency = samplerate / 2 #120 bpm
    samples = samplerate * 5

    sine = [math.sin(2 * math.pi * x / frequency) for x in range(samples)]
    noisy = [random.randint(25, 100) * x for x in sine]
    capped = [random.randint(0, 75) if x < 0 else x for x in noisy] #cap negative
    return capped
