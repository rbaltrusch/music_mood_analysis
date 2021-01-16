# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:47:23 2021

@author: Korean_Crimson
"""

import pytest
import numpy
from music_mood_analysis import dataconversion

@pytest.mark.parametrize('point', [numpy.int16(2),
                                   13,
                                   [2, 3],
                                   (4, 5),
                                   numpy.array([1,2])
                                   ])
def test_stereo_to_mono(point):
    result = dataconversion._mono(point)
    assert isinstance(result, int), 'dataconversion._mono should return an int'
