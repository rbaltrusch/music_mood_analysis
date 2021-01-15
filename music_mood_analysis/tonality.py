# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:51:14 2021

@author: Korean_Crimson
"""

import plots
from consts import MUSICAL_NOTE_FREQUENCIES, MUSICAL_NOTE_NAMES
from consts import MUSICAL_NOTE_LOWER_BOUND, MUSICAL_NOTE_HIGHER_BOUND
from math_util import init_zero_list, compute_Yss, get_index_of
from util import timeit

def _normalise(Yss_f):
    while not MUSICAL_NOTE_LOWER_BOUND < Yss_f < MUSICAL_NOTE_HIGHER_BOUND:
        Yss_f *= 2 if Yss_f < MUSICAL_NOTE_LOWER_BOUND else 0.5
    return Yss_f

@timeit
def analyse(samplerate, data):
    '''
    Tonality analysis using weighted note occurence.

    Input args:
        samplerate: int
        data: numpy.array

    Return values:
        tonality: string ('minor' or 'major')
        key: string (see consts.MUSICAL_NOTE_NAMES)
    '''
    adjusted_note_counts = count_musical_notes(samplerate, data)
    musical_root_index = get_index_of(max, adjusted_note_counts)
    normalised_note_counts = [adjusted_note_counts[i] for i in range(musical_root_index - 12, musical_root_index)]
    plots.plot(normalised_note_counts, title='Adjusted musical note frequency')
    tonality = _get_tonality(normalised_note_counts)
    key = MUSICAL_NOTE_NAMES[musical_root_index]
    return tonality, key

def count_musical_notes(samplerate, data):
    '''Counts note occurence weighted by amplitude of each musical note and applies
    the following modifier to predict tonality:
        Counts of root, fourth and fifth notes are summed, for each semitone.

    Input args:
        samplerate: int
        data: numpy.array

    Return values:
        adjusted_note_counts: list ()
    '''
    weighted_note_counts = compute_weighted_note_counts(samplerate, data)
    adjusted_note_counts = [_adjust(weighted_note_counts, i) for i in range(12)]
    plots.plot(adjusted_note_counts, weighted_note_counts, title='Adjusted musical note frequency', normalised=True)
    return adjusted_note_counts

def compute_weighted_note_counts(samplerate, data):
    '''Returns note counts weighted by sum of amplitudes of those notes
    '''
    weighted_note_counts = init_zero_list(12)
    amplitudes, frequencies = compute_Yss(samplerate, data)
    for amplitude, freq in zip(amplitudes, frequencies):
        frequency_differences = [abs(_normalise(freq) - frequency) for frequency in MUSICAL_NOTE_FREQUENCIES]
        min_index = frequency_differences.index(min(frequency_differences))
        weighted_note_counts[min_index] += abs(amplitude)
    return weighted_note_counts

def _adjust(note_counts, index):
    '''add root note, fourth (5 semitones higher) and fifth (7 semitones higher) together'''
    return note_counts[index] + note_counts[index-7] + note_counts[index-5]

def _get_tonality(note_counts):
    '''returns 'minor' if weighted amplitude of third semitone (minor third) is
    higher than the weighted amplitude of fourth semitone (major third), else
    returns 'major'.
    '''
    return 'minor' if note_counts[3] > note_counts[4] else 'major'
