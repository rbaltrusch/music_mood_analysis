# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 12:46:38 2021

@author: Korean_Crimson
"""

import pytest
from music_mood_analysis import util

@pytest.mark.parametrize("function,expected", [(lambda: None, None),
                                      (lambda: 1, 1),
                                      (lambda: [1], [1])
                                      ])
def test_timeit_returns_function(function, expected):
    func = util.timeit(function)
    assert callable(func), 'timeit decorator must return a function'
    result = func()
    assert result == expected, 'timeit decorator should not change result of decorated function'
