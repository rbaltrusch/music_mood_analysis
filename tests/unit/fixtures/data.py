# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 17:14:44 2021

@author: Korean_Crimson
"""

import numpy
import pytest

@pytest.fixture
def random_data():
    return numpy.random.rand(2000)
