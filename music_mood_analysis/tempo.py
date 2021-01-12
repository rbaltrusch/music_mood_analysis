# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:07:35 2021

@author: Korean_Crimson
"""

import math

import plots
from consts import get_beat_distance_constants
from math_util import init_zero_list
from util import timeit

@timeit
def analyse(samplerate, data):
    dbb, k = get_beat_distances(samplerate, data)
    dbbnrtma = getbpmnrta(samplerate, dbb)
    bpm = getbpm(samplerate, dbb, k, dbbnrtma)
    return bpm

def get_local_maximum_values(samplerate, data):
    '''Beat detection algorithm '''
    data = [x for x in data if x > 0]
    beat_constant_min, beat_constant_max = get_beat_distance_constants(samplerate)
    local_maximum_values = init_zero_list(len(data))
    current_local_maximum_value = 0
    local_maximum_value_counter = 0
    for i, data_point in enumerate(data):
        if data_point >= current_local_maximum_value and beat_constant_min < local_maximum_value_counter < beat_constant_max:
            local_maximum_values[i - 1] = 0
            local_maximum_value_counter = 0
            local_maximum_values[i] = data_point
            current_local_maximum_value = local_maximum_values[i]
        else:
            local_maximum_value_counter += 1

    plots.plot(local_maximum_values, data, ylabel='Local maximum values')
    return local_maximum_values

def get_beat_distances(samplerate, data):
    beat_constant_min, _ = get_beat_distance_constants(samplerate)
    local_maximum_values = get_local_maximum_values(samplerate, data)
    dbbsize = math.ceil(len(data) / beat_constant_min) #bpsmax*time is the maximum amount of possible beats we could have, so this is our array size for the dbb array below
    dbb = init_zero_list(dbbsize)
    k = 0 #counter for dbb array
    for i, local_maximum_value in enumerate(local_maximum_values):
        if k >= len(dbb):
            break
        #if the lmv element is zero, keep counting until we reach a nonzero element
        if local_maximum_value:
            k += 1
        else:
            dbb[k] += 1

    plots.plot(dbb, ylabel='duration between beats')
    return dbb, k

def getbpmnrta(samplerate, dbb):
    beatconstantmin, beatconstantmax = get_beat_distance_constants(samplerate)
    dbbnz = [x for x in dbb if x != 0]
    dbbnrtma = [sum(dbbnz[:i]) / i for i in range(1, len(dbbnz)-2)]
    return dbbnrtma

def firstdbbhypo(samplerate, durations_between_beats):
    '''This formulates our first dbb (duration between beats hypothesis)'''
    beat_constant_min, beat_constant_max = get_beat_distance_constants(samplerate)
    for duration_between_beats in durations_between_beats:
        if beat_constant_min <= duration_between_beats <= beat_constant_max:
            hypothesis = duration_between_beats
            break
    else:
        hypothesis = 0
    return hypothesis

def setdbbparams(dbbhypo):
    dbbsum = dbbhypo 
    dbbc = 1 
    dbbflag, dbbflaggedvalue = resetdbbflag()
    return dbbsum, dbbc, dbbflag, dbbflaggedvalue

def resetdbbflag():
    dbbflag = 0
    dbbflaggedvalue = [0,0]
    return dbbflag, dbbflaggedvalue

def getbpm(samplerate, dbb, k, dbbnrtma):
    '''This section finds the tempo of the piece'''
    beatconstantmin, beatconstantmax = get_beat_distance_constants(samplerate)
    dbbhypo=firstdbbhypo(samplerate, dbb)
    dbbsum=0
    dbbhypo_ap=0.1 #dbb hypothesis allowance percentage 
    dbbc=1 # dbb counter
    dbbflag=0 #count how often current hypothesis was wrong 
    dbbflaggedvalue=init_zero_list(2) # the flagged dbb that didnt agree with current hypothesis goes here 
    L=0
    for o in range(L,int(k-1)):
        if dbbflag<2:
            #current hypothesis stays 
            if dbbhypo<=beatconstantmin and dbbhypo>=beatconstantmax:
                dbbhypo_lb=dbbhypo*(1-dbbhypo_ap) #dbb hypothesis lower bound
                dbbhypo_hb=dbbhypo*(1+dbbhypo_ap) #dbb hypothesis higher bound
                if dbb[L]>=dbbhypo_lb and dbb[L]<=dbbhypo_hb:
                    dbbflag, dbbflaggedvalue=resetdbbflag()
                    dbbsum+=dbb[L]
                    dbbavg=dbbsum/dbbc
                    dbbhypo=dbbavg
                    dbbc+=1
                else:
                    dbbflaggedvalue[dbbflag]=dbb[L]
                    dbbflag+=1
        elif L<10: 
            if abs(dbbflaggedvalue[0]-dbbflaggedvalue[1])/int(sum(dbbflaggedvalue)/2)<0.1:
                dbbhypo=sum(dbbflaggedvalue)/2 #set a new hypothesis 
                dbbsum, dbbc, dbbflag, dbbflaggedvalue=setdbbparams(dbbhypo)
            else: 
                dbbhypo=dbb[L+1]
                dbbsum, dbbc, dbbflag, dbbflaggedvalue=setdbbparams(dbbhypo)
        else:
            if dbbhypo<=dbbnrtma[L]*(1+dbbhypo_ap) and dbbhypo>=dbbnrtma[L]*(1-dbbhypo_ap):
                dbbflag, dbbflaggedvalue=resetdbbflag()
            else:
                dbbhypo=dbbnrtma[L]
                dbbsum, dbbc, dbbflag, dbbflaggedvalue=setdbbparams(dbbhypo)
        L+=1

    dbbavg = dbbsum / (dbbc + 1) #average of duration between beats
    bpm = samplerate * 60 / dbbavg if dbbavg > 0 else 0
    return bpm
