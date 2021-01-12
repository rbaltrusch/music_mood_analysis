'''author: Richard Baltrusch
real-time analysis of mood in music'''

import scipy.io.wavfile as siw

import tonality
import tempo
from dataconversion import downconvert_chunk

def analyse(samplerate, data):
    '''Main analysis function.

    Input args:
        samplerate: int
        data: numpy.array

    Return values:
        bpm: int (beats per minute)
        tonality: string (see consts.MUSICAL_NOTE_NAMES)
    '''
    bpm = tempo.analyse(samplerate, data)
    tonality_, _ = tonality.analyse(samplerate, data)
    return bpm, tonality_

def _test():
    samplerate_, data_ = siw.read(r'test.wav')
    chunk_sample_rate, chunk_data = downconvert_chunk(samplerate_, data_, chunk_index=0)
    bpm, tonality_ = analyse(chunk_sample_rate, chunk_data)
    return bpm, tonality_

if __name__ == '__main__':
    _test()
