# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:46:38 2021

@author: Korean_Crimson
"""

from music_mood_analysis import util

def test_timeit_returns_function():
    assert callable(util.timeit(lambda: None)), 'timeit decorator must return a function'
