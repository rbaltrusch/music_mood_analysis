# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:47:09 2021

@author: Korean_Crimson
"""

SAMPLE_RATE = 44100

CONVERSION_RATIO = 32
CHUNK_SIZE = 100

BPS_MAX = 3 #how many beats per second we detect at most
BPS_MIN = 1.5 #how many beats per second we detect at least

#12 frequencies starting from middle A440, up a semitone each.
MUSICAL_NOTE_FREQUENCIES = [440, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61]
MUSICAL_NOTE_LOWER_BOUND = 440
MUSICAL_NOTE_HIGHER_BOUND = 881
MUSICAL_NOTE_NAMES = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

PLOTTING_ENABLED = True

def get_beat_distance_constants(samplerate):
    '''returns min and max distances between beats (int, int)'''
    beat_distance_min = samplerate / BPS_MAX
    beat_distance_max = samplerate / BPS_MIN
    return beat_distance_min, beat_distance_max
