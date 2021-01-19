# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 18:27:08 2021

@author: Korean_Crimson
"""

import random
import pytest
import numpy

from music_mood_analysis import plots

@pytest.mark.slow
@pytest.mark.parametrize('datasets,kwargs', [
        ([[random.randint(0, 100000) for _ in range(13)]], {}),
        ([[1, 2, 3], [2, 3, 4]], {'normalised': False}),
        ([[1, 2, 3], [2, 3, 4]], {'normalised': True}),
        ([[2, -53, 400, 12000, 3]],
         {'title': 'my title', 'xlabel': 'label x', 'ylabel': 'label y'}),
        ([numpy.random.rand(100)], {})
        ])
def test_plot(datasets, kwargs):
    plots.plot(*datasets, **kwargs)

def test_plot_disabled():
    plots.PLOTTING_ENABLED = False
    plots.plot([1, 2, 3])
