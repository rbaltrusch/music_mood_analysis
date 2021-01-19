# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:07:35 2021

@author: Korean_Crimson
"""

import plots
from consts import get_beat_distance_constants, DECAY
from consts import BEAT_DISTANCE_HYPOTHESIS_ALLOWANCE_PERCENTAGE as allowance_percentage
from math_util import init_zero_list, smooth
from util import timeit

@timeit
def analyse(samplerate, data):
    beat_distances = compute_beat_distances(samplerate, data)
    bpm = compute_bpm(samplerate, beat_distances)
    return bpm

def compute_local_maximum_values(samplerate, data):
    '''Beat detection algorithm '''
    data = [x for x in data if x > 0]
    data = smooth(data, factor=100)
    beat_constant_min, beat_constant_max = get_beat_distance_constants(samplerate)
    local_maximum_values = init_zero_list(len(data))
    current_local_maximum_value = 0
    local_maximum_value_counter = 0
    previous_max_i = 0
    for i, data_point in enumerate(data):
        remove_previous_max_flag = False
        if data_point >= current_local_maximum_value:
            if local_maximum_value_counter < beat_constant_min:
                remove_previous_max_flag = True
            set_max_flag = True
        elif local_maximum_value_counter > beat_constant_max:
            set_max_flag = True
        else:
            set_max_flag = False
            local_maximum_value_counter += 1

        if set_max_flag:
            if remove_previous_max_flag:
                local_maximum_values[previous_max_i] = 0
            previous_max_i = i
            local_maximum_value_counter = 0
            local_maximum_values[i] = data_point
            current_local_maximum_value = data_point

        if local_maximum_value_counter < beat_constant_min:
            current_local_maximum_value *= (1 - DECAY)

    plots.plot(data, local_maximum_values, ylabel='Local maximum values', normalised=True)
    return local_maximum_values

def compute_beat_distances(samplerate, data):
    local_maximum_values = compute_local_maximum_values(samplerate, data)
    indices = [i for i, x in enumerate(local_maximum_values) if x > 0] #non zero indices
    beat_distances = [indices[i + 1] - indices[i] for i in range(len(indices) - 1)]
    plots.plot(beat_distances, ylabel='duration between beats')
    return beat_distances

def find_first_hypothesis(samplerate, durations_between_beats):
    '''This formulates our first dbb (duration between beats hypothesis)'''
    beat_constant_min, beat_constant_max = get_beat_distance_constants(samplerate)
    for duration_between_beats in durations_between_beats:
        if beat_constant_min <= duration_between_beats <= beat_constant_max:
            hypothesis = duration_between_beats
            break
    else:
        hypothesis = 0
    return hypothesis

def compute_bpm(samplerate, beat_distances):
    '''This section finds the tempo of the piece'''
    beatconstantmin, beatconstantmax = get_beat_distance_constants(samplerate)
    hypothesis = find_first_hypothesis(samplerate, beat_distances)
    selected_distances = []
    flagged_values = [] #beat distances that didnt agree with current hypothesis
    flag = ''
    for beat_distance in beat_distances:
        if flag == 'next':
            hypothesis = beat_distance
            flag = ''

        #current hypothesis stays if less than two flagged values
        if len(flagged_values) < 2:
            if beatconstantmax <= hypothesis <= beatconstantmin and _is_in_bounds(beat_distance, hypothesis):
                flagged_values = []
                selected_distances.append(beat_distance)
                hypothesis = sum(selected_distances) / len(selected_distances)
            else:
                flagged_values.append(beat_distance)
        elif _are_closely_matching(flagged_values):
            hypothesis = sum(flagged_values) / 2
            selected_distances, flagged_values = [hypothesis], []
        else:
            flag = 'next'
            selected_distances, flagged_values = [hypothesis], []

    selected_distances = selected_distances if selected_distances else [hypothesis]
    if selected_distances:
        avg_beat_distance = sum(selected_distances) / len(selected_distances)
        bpm = (samplerate / avg_beat_distance) * 60 if avg_beat_distance else 0
    else:
        bpm = 0
    return round(bpm)

def _are_closely_matching(values):
    a, b = values
    result = abs(a - b)/ (a + b) <= allowance_percentage if a + b else False
    return result

def _is_in_bounds(value, boundary):
    """Only works for positive values"""
    lower_bound = boundary * (1 - allowance_percentage)
    higher_bound = boundary * (1 + allowance_percentage)
    return lower_bound <= value <= higher_bound
