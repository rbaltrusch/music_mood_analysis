'''author: Richard Baltrusch
real-time analysis of mood in music'''

import time
import math
import numpy
import operator
import scipy.io.wavfile as siw
import matplotlib.pyplot as plt

def timeit(func):
    def wrapper(*args, **kwargs):
        time0 = time.time()
        result = func(*args, **kwargs)
        print(f'time elapsed in {func.__name__}: {time.time() - time0}')
        return result
    return wrapper

def zerolist(sampleamount):
  sampleamount=int(sampleamount)
  listofzeros = [0] * sampleamount
  return listofzeros

@timeit
def downconvert(samplerate,conversion_ratio, data, stereostatus):
    '''samplerate downconversion algorithm'''
    samplerate = math.ceil(samplerate/conversion_ratio)
    converted_data = []
    for i, data_point in enumerate(data):
        if not i % conversion_ratio:
            converted_data.append(stereotomono(data_point))
    return samplerate, converted_data

@timeit
def downconvertfast(samplerate, data, conversion_ratio, chunksize, chunknumber):
    samplerate = math.ceil(samplerate/conversion_ratio)
    chunklen =int(chunksize*samplerate)
    converted_data = []
    index = chunklen * chunknumber
    data_slice = data[index:index + chunklen]
    for i, data_point in enumerate(data_slice):
        if not i % conversion_ratio:
            converted_data.append(stereotomono(data_point))
    return samplerate, converted_data

def avg(list_):
    return sum(list_) / len(list_)

def getYss(samplerate, timelength, data):
  Yss = numpy.fft.fft(data)
  Yss_f = numpy.fft.fftfreq(Yss.size, 0.000025)
  return Yss, Yss_f

def get_local_maximum_values(samplerate, data):
    '''Beat detection algorithm '''
    data = list(filter(lambda a: a > 0, data))
    beat_constant_min, beat_constant_max = get_beat_constants(samplerate)
    print(beat_constant_min, beat_constant_max, samplerate)
    local_maximum_values = zerolist(len(data))
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

    plt.figure(6)
    plt.subplot(211)
    plt.plot(local_maximum_values)
    plt.subplot(212)
    plt.plot(data)
    plt.ylabel('lmv')
    plt.show()
    return local_maximum_values

def getdbb(samplerate, data):
    beat_constant_min, beat_constant_max = get_beat_constants(samplerate)
    local_maximum_values = get_local_maximum_values(samplerate, data)
    dbbsize = math.ceil(len(data) / beat_constant_min) #bpsmax*time is the maximum amount of possible beats we could have, so this is our array size for the dbb array below
    dbb=zerolist(dbbsize)
    dbbm=zerolist(dbbsize)
    k=0 #counter for dbb array
    for i, local_maximum_value in enumerate(local_maximum_values):
        if k >= len(dbb):
            break
        #if the lmv element is zero, keep counting until we reach a nonzero element
        if not local_maximum_value:
            dbb[k] += 1 
        else:
            dbbm[k] = i
            k += 1

    dbbm = list(filter(lambda a: a != 0, dbbm))
    plt.figure(5)
    plt.plot(dbb)
    plt.ylabel('duration between beats')
    plt.show()
    return dbb, k, dbbm

def getbpmnrta(samplerate, dbb):
    beatconstantmin, beatconstantmax = get_beat_constants(samplerate)
    dbbnz = list(filter(lambda a: a != 0, dbb)) #remove all zeros from dbb list
    dbbnrtma = [sum(dbbnz[:i]) / i for i in range(1, len(dbbnz)-2)]
    bpmnrta = [samplerate*60/dbbnrtm for dbbnrtm in dbbnrtma]
    return bpmnrta, dbbnrtma

def firstdbbhypo(samplerate, durations_between_beats):
    '''This formulates our first dbb (duration between beats hypothesis)'''
    beat_constant_min, beat_constant_max = get_beat_constants(samplerate)
    for duration_between_beats in durations_between_beats:
        if beat_constant_min <= duration_between_beats <= beat_constant_max:
            hypothesis = duration_between_beats
            break
    else:
        hypothesis = 0
    return hypothesis

def setdbbparams(dbbhypo):
  dbbsum=dbbhypo 
  dbbc=1 
  dbbflag, dbbflaggedvalue=resetdbbflag()
  return dbbsum, dbbc, dbbflag, dbbflaggedvalue

def resetdbbflag():
  dbbflag=0 #reset dbb flag counter
  dbbflaggedvalue=[0,0] #reset dbb flagged values array
  return dbbflag, dbbflaggedvalue

def getbpm(samplerate, dbb, k, dbbnrtma):
  beatconstantmin, beatconstantmax=get_beat_constants(samplerate)
  dbbhypo=firstdbbhypo(samplerate, dbb)
  dbbsum=0 
  #This section finds the tempo of the piece
  dbbhypo_ap=0.1 #dbb hypothesis allowance percentage 
  dbbc=1 # dbb counter
  dbbflag=0 #count how often current hypothesis was wrong 
  dbbflaggedvalue=zerolist(2) # the flagged dbb that didnt agree with current hypothesis goes here 
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
    #this else clause was rendered essentially useless by the previous while loop 
    else: 
      if L<10: 
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
  dbbavg=dbbsum/(dbbc+1) #average of duration between beats 
  if dbbavg>0:
    bpm=samplerate*60/(dbbavg)
  else:
    bpm=0
  print('Bpm is: ', bpm)
  return bpm, dbbavg

@timeit
def fullbpmfunct(samplerate, data):
    dbb, k, dbbm=getdbb(samplerate, data)
    bpmnrta, dbbnrtma=getbpmnrta(samplerate, dbb)
    bpm, dbbavg=getbpm(samplerate, dbb, k, dbbnrtma)
    beatarray, samplerate=getbeatarray(dbbm, dbbavg, bpm, samplerate, data)
    return bpmnrta, bpm

def getbeatarray(dbbm, dbbavg, bpm, samplerate, data):
  timelength = len(data)/samplerate
  dbbap=0.1
  dbbh=dbbavg*(1+dbbap)
  dbbl=dbbavg*(1-dbbap)
  beatarraylength=int(math.ceil(bpm*timelength/60))
  beatarray=zerolist(beatarraylength)
  bd=zerolist(beatarraylength)
  dbbmcounter=1
  for beatcounter in range (1, beatarraylength-1):
    if dbbmcounter<len(dbbm)-1:
      if beatarray[beatcounter]==0:
        dbbdiff=dbbm[dbbmcounter]-dbbm[dbbmcounter-1]
        if dbbdiff>=dbbl and dbbdiff <=dbbh:
          beatarray[beatcounter]=dbbm[dbbmcounter]
        else: 
          if (dbbdiff/2>=dbbl and dbbdiff/2<=dbbh):
            beatarray[beatcounter]=dbbm[dbbmcounter-1]+(dbbdiff/2)
            beatarray[beatcounter+1]=dbbm[dbbmcounter]
          else:
            beatarray[beatcounter]=dbbavg+beatarray[beatcounter-1]
        dbbmcounter+=1
    else:
      beatarray[beatcounter]=dbbavg+beatarray[beatcounter-1]
  
  for counter in range(1, len(beatarray)-1):
    bd[counter]=beatarray[counter]-beatarray[counter-1]
  return beatarray, samplerate

def normalise(Yss_f, lower, upper):
    while not 440 < Yss_f < 881:
        Yss_f *= 2 if Yss_f < 440 else 0.5
    return Yss_f
    
def getmnf_cm(samplerate, timelength, data):
    #This section counts the frequency of appearance of each musical note and applies modifiers to predict tonality 
    #construct a one-sided amplitude spectrum of Y(t)
    mnf_base=[440, 466.16, 493.88, 523.25, 554.37, 587.33, 622.25, 659.25, 698.46, 739.99, 783.99, 830.61]
    mnf_cm=zerolist(12); #frequency of notes multiplied by Yss amplitude
    mnf_ca=zerolist(12); #adjusted frequency of notes 
    Yss_list, Yss_f_list = getYss(samplerate, timelength, data)
    for Yss, Yss_f in zip(Yss_list, Yss_f_list):
        Yss_f = normalise(Yss_f, 440, 881)
        mnf_d = [abs(Yss_f - frequency) for frequency in mnf_base]
        mnf_dmi = mnf_d.index(min(mnf_d))
        mnf_cm[mnf_dmi] += Yss
    
    #add root, fourth and fifth together 
    mnf_ca[mnf_dmi] = mnf_cm[mnf_dmi] + mnf_cm[mnf_dmi-7] + mnf_cm[mnf_dmi-5]

    plt.figure(1)
    plt.plot(mnf_ca)
    plt.ylabel('mnf_ca')
    plt.show()
    return mnf_ca

@timeit
def gettonality(samplerate, data):
    mnf_base_name=['A ','A#','B ','C ','C#','D ','D#','E ','F ','F#','G ','G#']
    timelength = len(data)/samplerate
    mnf_ca = getmnf_cm(samplerate, timelength, data)
    mnf_cai, mnf_cam = max(enumerate(mnf_ca), key=operator.itemgetter(1))
    #this section finds whether the tonality is minor or major
    mnf_ca_changed=zerolist(12)
    for mnf_cac in range(11):
        if (mnf_cai-1+mnf_cac)<=11:
            mnf_ca_changed[mnf_cac]=mnf_ca[mnf_cai-1+mnf_cac]
        else:
            mnf_ca_changed[mnf_cac]=mnf_ca[mnf_cai-13+mnf_cac]

    tonality = 'minor' if mnf_ca_changed[3]>mnf_ca_changed[4] else 'major'
    print('Key is: ', mnf_base_name[mnf_cai], tonality)
    return tonality

def set_dummy_data(samplerate=44100):
    return [math.sin(x) for x in range(samplerate)]

def get_beat_constants(samplerate):
    '''returns min and max distances between beats'''
    bpsmax = 3 #how many beats per second we detect at most
    bpsmin = 1.5 #how many beats per second we detect at least
    beatconstantmin=samplerate/bpsmax
    beatconstantmax=samplerate/bpsmin
    return beatconstantmin, beatconstantmax

def stereotomono(stereo_data_point, disabled=False):
    if isinstance(stereo_data_point, numpy.int16):
        mono_data_point = int(stereo_data_point)
    else:
        disabled = True if stereo_data_point.size > 1 else False
        mono_data_point = stereo_data_point if disabled else int(sum(stereo_data_point[0:2]))
    return mono_data_point

def analyse(samplerate, data):
  bpmnrta, bpm = fullbpmfunct(samplerate, data)
  tonality = gettonality(samplerate, data) 
  return bpm, tonality
  
def main():
    '''main function'''
    filename = r'D:\Alle Dateien\Code\Python\Music\Mood analysis\2020May10_015321_interesting.wav'
    samplerate, data = siw.read(filename)
    chunksamplerate, chunkdata = downconvertfast(samplerate, data, conversion_ratio=32, chunksize=100, chunknumber=0)
    return analyse(chunksamplerate,chunkdata)

if __name__ == '__main__':
    bpm, tonality = main()
