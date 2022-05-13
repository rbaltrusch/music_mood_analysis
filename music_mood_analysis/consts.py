# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:47:09 2021

@author: Korean_Crimson
"""

SAMPLE_RATE = 44100
CONVERSION_RATIO = 32
CHUNK_SIZE = 5

BPS_MAX = 3  # how many beats per second we detect at most
BPS_MIN = 1.5  # how many beats per second we detect at least
DECAY = 0.0001  # Amplitude decay of current max val between beat_distance_min and beat_distance_max

# 12 frequencies starting from middle A440, up a semitone each.
MUSICAL_NOTES = {
    "A": 440.0,
    "A#": 466.16,
    "B": 493.88,
    "C": 523.25,
    "C#": 554.37,
    "D": 587.33,
    "D#": 622.25,
    "E": 659.25,
    "F": 698.46,
    "F#": 739.99,
    "G": 783.99,
    "G#": 830.61,
}
MUSICAL_NOTE_FREQUENCIES = tuple(MUSICAL_NOTES.values())
MUSICAL_NOTE_NAMES = tuple(MUSICAL_NOTES.keys())
MUSICAL_NOTE_LOWER_BOUND = MUSICAL_NOTES["A"]

PLOTTING_ENABLED = True
