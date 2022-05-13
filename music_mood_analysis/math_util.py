# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:54:21 2021

@author: Korean_Crimson
"""

from typing import List, Tuple, Union
import numpy

Number = Union[float, int]


def compute_Yss(
    samplerate: Number, data: numpy.ndarray
) -> Tuple[List[Number], List[Number]]:
    """Construct a one-sided amplitude spectrum of Y(t)

    Input args:
        samplerate - int
        data - numpy.array

    Return values:
        Yss: one-dimensional discrete Fourier Transform
        Yss_f: Discrete Fourier Transform sample non-zero positive frequencies
    """
    # pylint: disable=C0103
    Yss = numpy.fft.fft(data)
    time_step = 1 / samplerate
    Yss_f = numpy.fft.fftfreq(Yss.size, time_step)
    Yss, Yss_f = list(
        zip(*[(amplitude, freq) for amplitude, freq in zip(Yss, Yss_f) if freq > 0])
    )
    return list(Yss), list(Yss_f)


def get_index_of(func, data: List[Number]) -> int:
    """Returns index of the data point which func (should be in-built min or max)
    would return if called by itself.

    Input args:
        func: function (should be min/max)
        data: iterable

    Return val:
        index: int

    Example:
        index = get_index_of(max, [3, 5, 2]) #returns 1
    """
    index, _ = func(enumerate(data), key=lambda x: x[1])
    return index


def smooth(data: List[Number], factor=1) -> List[Number]:
    """Used to smooth data, returns list"""
    return [sum(data[i : i + factor]) for i in range(len(data) - factor + 1)]


def normalise(number: Number, lower_bound: Number, higher_bound: Number) -> Number:
    """Returns number normalised to be within the lower or higher bound, or 0 if negative"""
    if number <= 0:
        return 0

    if higher_bound / 2 <= lower_bound:
        higher_bound = lower_bound * 2

    while not lower_bound <= number <= higher_bound:
        number *= 2 if number < lower_bound else 0.5
    return number
