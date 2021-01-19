# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 21:54:54 2021

@author: Korean_Crimson
"""

import matplotlib.pyplot as plt

from util import timeit
from math_util import compute_Yss
from consts import BPS_MAX, BPS_MIN
from tonality import _normalise

@timeit
def _test(samplerate, data):
    Yss, Yss_f = compute_Yss(samplerate, data)
    Yss_f = [freq for freq in Yss_f]
    Yss = [abs(x) for x in Yss[:len(Yss_f)]]

    from collections import defaultdict
    freq_dict = defaultdict(int)
    for amplitude, freq in zip(Yss, Yss_f):
        normalised_freq = _normalise(freq, lower_bound=BPS_MIN, higher_bound=BPS_MAX)
        rounded_freq = round(normalised_freq, 2)
        freq_dict[rounded_freq] += abs(amplitude)

    plt.figure()
    plt.plot(list(freq_dict.keys()), list(freq_dict.values()))
    plt.show()
    print(sorted(freq_dict.items(), key=lambda x: x[1], reverse=True))
    print(round(60 * max(freq_dict.items(), key=lambda x: x[1])[0]))
