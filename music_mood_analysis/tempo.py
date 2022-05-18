# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:07:35 2021

@author: Korean_Crimson
"""
from abc import ABC, abstractmethod
import collections
from dataclasses import dataclass
from typing import DefaultDict, Iterable, List

import numpy
from music_mood_analysis import consts
from music_mood_analysis.math_util import compute_Yss
from music_mood_analysis.math_util import normalise
from music_mood_analysis.math_util import smooth

# pylint: disable=invalid-name


@dataclass
class DataPoint:
    """Stores index, value and decayed_value attributes for local maximum value algorithm"""

    index: int
    value: float
    decayed_value: float


@dataclass
class AbstractTempoAnalyser(ABC):
    """Analyses tempo"""

    samplerate: float
    BPS_MIN: float = consts.BPS_MIN
    BPS_MAX: float = consts.BPS_MAX

    @abstractmethod
    def analyse(self, data: numpy.ndarray) -> int:
        """Analyses the input data and returns the computed bpm"""


# pylint: disable=too-many-instance-attributes
@dataclass
class TempoAnalyser(AbstractTempoAnalyser):
    """Analyses tempo of data by determining distance between local amplitude maxima"""

    DECAY: float = consts.DECAY

    def __post_init__(self):
        self.local_maximum_data: List[int] = []
        self._local_maximum_values: List[DataPoint] = []
        self.processed_data: List[float] = []

    def analyse(self, data: numpy.ndarray) -> int:
        """Analyses the input data and returns the computed bpm"""
        self._process_data(data)
        self._compute_local_maximum_values()
        self._set_local_maximum_data()
        return self._compute_bpm()

    def _process_data(self, data: Iterable[float]) -> None:
        non_zero_data = [x for x in data if x > 0]
        self.processed_data = smooth(non_zero_data, factor=100)

    def _compute_local_maximum_values(self) -> None:
        """Beat detection algorithm"""
        self._local_maximum_values = [DataPoint(0, 0, 0)]
        for i, x in enumerate(self.processed_data):
            under_min = i - self._local_maximum_values[-1].index < self.beat_min_dist
            over_max = i - self._local_maximum_values[-1].index > self.beat_max_dist
            if x >= self._local_maximum_values[-1].decayed_value or over_max:
                if under_min:
                    self._local_maximum_values.pop()
                self._local_maximum_values.append(DataPoint(i, x, x))
            self._local_maximum_values[-1].decayed_value *= 1 - consts.DECAY

    def _compute_beat_distances(self) -> List[int]:
        indices = [data_point.index for data_point in self._local_maximum_values]
        return [indices[i + 1] - indices[i] for i in range(len(indices) - 1)]

    def _set_local_maximum_data(self) -> None:
        self.local_maximum_data = [0] * len(self.processed_data)
        for data_point in self._local_maximum_values:
            self.local_maximum_data[data_point.index] = data_point.value

    def _compute_bpm(self) -> int:
        """This section finds the tempo of the piece"""
        beat_dists = self._compute_beat_distances()
        filtered_dists = [
            d for d in beat_dists if self.beat_min_dist <= d <= self.beat_max_dist
        ]
        if not filtered_dists:
            return 0

        middle_index = len(filtered_dists) // 2
        median_dist = sorted(filtered_dists)[middle_index]
        return round((60 * self.samplerate) / median_dist)

    @property
    def beat_min_dist(self) -> float:
        """Beat constant min getter, minimum distance between beats"""
        return round(self.samplerate / self.BPS_MAX)

    @property
    def beat_max_dist(self) -> float:
        """Beat constant max getter, maximum distance between beats"""
        return round(self.samplerate / self.BPS_MIN)


class FFTTempoAnalyser(AbstractTempoAnalyser):  # pylint: disable=too-few-public-methods
    """Analyses tempo of data using spectral analysis (fft)"""

    def analyse(self, data: numpy.ndarray) -> int:
        """Analyses the input data and returns the computed bpm"""
        Yss, Yss_f = compute_Yss(self.samplerate, data)
        freq_dict: DefaultDict[float, int] = collections.defaultdict(int)
        for amplitude, freq in zip(map(abs, Yss), Yss_f):
            normalised_freq = normalise(
                freq, lower_bound=self.BPS_MIN, higher_bound=self.BPS_MAX
            )
            rounded_freq = round(normalised_freq, 2)
            freq_dict[rounded_freq] += amplitude
        bpm = round(60 * max(freq_dict.items(), key=lambda x: x[1])[0])
        return bpm
