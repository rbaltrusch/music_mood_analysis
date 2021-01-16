# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 13:32:09 2021

@author: Korean_Crimson
"""

import pytest

@pytest.fixture
def samplerate():
    return 44100

@pytest.fixture
def down_samplerate():
    """returns downsampled samplerate"""
    return round(44100 / 32)
