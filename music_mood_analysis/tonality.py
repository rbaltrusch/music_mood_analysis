# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:51:14 2021

@author: Korean_Crimson
"""

from dataclasses import dataclass
import numpy

import consts
from math_util import compute_Yss, get_index_of, normalise

#pylint: disable=invalid-name

@dataclass
class TonalityAnalyser:
    """Analyses data using spectral analysis (fft) to extract its tonality."""

    samplerate: int
    normalised_note_counts: list = None
    musical_root_index: int = None
    MUSICAL_NOTE_FREQUENCIES: tuple = consts.MUSICAL_NOTE_FREQUENCIES
    MUSICAL_NOTE_NAMES: tuple = consts.MUSICAL_NOTE_NAMES
    MUSICAL_NOTE_LOWER_BOUND: int = consts.MUSICAL_NOTE_LOWER_BOUND

    def analyse(self, data: numpy.array) -> str:
        """"Tonality analysis using weighted note occurence. Returns tonality (e.g. A minor)"""
        adjusted_note_counts = self._compute_weighted_note_counts(data)
        self.musical_root_index = get_index_of(max, adjusted_note_counts)
        self._set_normalised_note_counts(adjusted_note_counts)
        return self._determine_tonality()

    def _compute_weighted_note_counts(self, data: numpy.array):
        """Returns note counts weighted by sum of amplitudes of those notes"""
        weighted_note_counts = [0] * 12
        amplitudes, frequencies = compute_Yss(self.samplerate, data)
        for amplitude, freq in zip(amplitudes, frequencies):
            normalised_frequency = normalise(freq,
                                             lower_bound=self.MUSICAL_NOTE_LOWER_BOUND,
                                             higher_bound=self.MUSICAL_NOTE_LOWER_BOUND * 2
                                             )
            freq_diffs = [abs(normalised_frequency - f) for f in self.MUSICAL_NOTE_FREQUENCIES]
            min_index = get_index_of(min, freq_diffs)
            weighted_note_counts[min_index] += abs(amplitude)
        return weighted_note_counts

    def _set_normalised_note_counts(self, note_counts):
        """Sets normalised_note_counts such that the first element is the root"""
        self.normalised_note_counts = []
        for i in range(self.musical_root_index - 12, self.musical_root_index):
            self.normalised_note_counts.append(note_counts[i])

    def _determine_tonality(self):
        tonality = self._get_tonality(self.normalised_note_counts)
        key = self.MUSICAL_NOTE_NAMES[self.musical_root_index]
        return f'{key} {tonality}'

    @staticmethod
    def _get_tonality(note_counts):
        """returns 'minor' if amplitude of third semitone (minor third) is higher than the
        amplitude of fourth semitone (major third), else returns 'major'.
        """
        return 'minor' if note_counts[3] > note_counts[4] else 'major'
