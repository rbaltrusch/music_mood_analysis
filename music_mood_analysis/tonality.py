# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:51:14 2021

@author: Korean_Crimson
"""
from dataclasses import dataclass
from typing import List, Tuple

import numpy
from music_mood_analysis import consts
from music_mood_analysis.math_util import compute_Yss
from music_mood_analysis.math_util import get_index_of
from music_mood_analysis.math_util import normalise

# pylint: disable=invalid-name


@dataclass
class TonalityAnalyser:
    """Analyses data using spectral analysis (fft) to extract its tonality."""

    samplerate: int
    MUSICAL_NOTE_FREQUENCIES: Tuple[float, ...] = consts.MUSICAL_NOTE_FREQUENCIES
    MUSICAL_NOTE_NAMES: Tuple[str, ...] = consts.MUSICAL_NOTE_NAMES
    MUSICAL_NOTE_LOWER_BOUND: float = consts.MUSICAL_NOTE_LOWER_BOUND

    def __post_init__(self):
        self.musical_root_index = None
        self.normalised_note_counts: List[int] = []

    def analyse(self, data: numpy.ndarray) -> str:
        """ "Tonality analysis using weighted note occurence. Returns tonality (e.g. A minor)"""
        adjusted_note_counts = self._compute_weighted_note_counts(data)
        self.musical_root_index = get_index_of(max, adjusted_note_counts)
        self._set_normalised_note_counts(adjusted_note_counts)
        return self._determine_tonality()

    def _compute_weighted_note_counts(self, data: numpy.ndarray) -> List[int]:
        """Returns note counts weighted by sum of amplitudes of those notes"""
        weighted_note_counts = [0] * 12
        amplitudes, frequencies = compute_Yss(self.samplerate, data)
        for amplitude, freq in zip(amplitudes, frequencies):
            normalised_frequency = normalise(
                freq,
                lower_bound=self.MUSICAL_NOTE_LOWER_BOUND,
                higher_bound=self.MUSICAL_NOTE_LOWER_BOUND * 2,
            )
            freq_diffs = [
                abs(normalised_frequency - f) for f in self.MUSICAL_NOTE_FREQUENCIES
            ]
            min_index: int = get_index_of(min, freq_diffs)
            weighted_note_counts[min_index] += abs(amplitude)
        return weighted_note_counts

    def _set_normalised_note_counts(self, note_counts: List[int]) -> None:
        """Sets normalised_note_counts such that the first element is the root"""
        self.normalised_note_counts = []
        for i in range(self.musical_root_index - 12, self.musical_root_index):
            self.normalised_note_counts.append(note_counts[i])

    def _determine_tonality(self) -> str:
        tonality = self._get_tonality(self.normalised_note_counts)
        key = self.MUSICAL_NOTE_NAMES[self.musical_root_index]
        return f"{key} {tonality}"

    @staticmethod
    def _get_tonality(note_counts: List[int]):
        """returns 'minor' if amplitude of third semitone (minor third) is higher than the
        amplitude of fourth semitone (major third), else returns 'major'.
        """
        return "minor" if note_counts[3] > note_counts[4] else "major"
