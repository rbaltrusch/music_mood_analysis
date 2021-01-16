# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 12:30:33 2021

@author: Korean_Crimson
"""

import pytest
from music_mood_analysis import consts

@pytest.mark.usefixtures("samplerate")
def test_beat_distance_constants(samplerate):
    min_distance, max_distance = consts.get_beat_distance_constants(samplerate)
    assert min_distance < max_distance
