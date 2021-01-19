# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:47:09 2021

@author: Korean_Crimson
"""

SAMPLE_RATE = 44100

CONVERSION_RATIO = 32
CHUNK_SIZE = 5

BPS_MAX = 3 #how many beats per second we detect at most
BPS_MIN = 1.5 #how many beats per second we detect at least

#12 frequencies starting from middle A440, up a semitone each.
MUSICAL_NOTES = {'A': 440,
                 'A#': 466.16,
                 'B': 493.88,
                 'C': 523.25,
                 'C#': 554.37,
                 'D': 587.33,
                 'D#': 622.25,
                 'E': 659.25,
                 'F': 698.46,
                 'F#': 739.99,
                 'G': 783.99,
                 'G#': 830.61}
MUSICAL_NOTE_FREQUENCIES = list(MUSICAL_NOTES.values())
MUSICAL_NOTE_NAMES = list(MUSICAL_NOTES.keys())
MUSICAL_NOTE_LOWER_BOUND = MUSICAL_NOTES['A']
                      
BEAT_DISTANCE_HYPOTHESIS_ALLOWANCE_PERCENTAGE = 0.1

PLOTTING_ENABLED = True

def get_beat_distance_constants(samplerate):
    '''returns min and max distances between beats (int, int)'''
    beat_distance_min = round(samplerate / BPS_MAX)
    beat_distance_max = round(samplerate / BPS_MIN)
    return beat_distance_min, beat_distance_max
