# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:17:38 2021

@author: Korean_Crimson
"""
import math
import os
from tkinter.filedialog import askopenfilename

import scipy.io.wavfile as siw
from music_mood_analysis import consts
from music_mood_analysis import plots
from music_mood_analysis import tempo
from music_mood_analysis import tonality
from music_mood_analysis.dataconversion import DownConverter
from music_mood_analysis.gui import app
from music_mood_analysis.gui import config
from music_mood_analysis.gui import figure

def set_gui_config_defaults(*_):
    """Callback for reset button"""
    app.data['chunksize'].set(consts.CHUNK_SIZE)
    app.data['conversion_ratio'].set(consts.CONVERSION_RATIO)
    app.data['bps_min'].set(consts.BPS_MIN)
    app.data['bps_max'].set(consts.BPS_MAX)
    app.data['decay'].set(consts.DECAY)

def set_scale(*_):
    """Callback for data_length StringVar write trace"""
    length = app.data['data_length'].get()
    app['config']['chunksize_scale'].config(to=length)

def set_error(*_):
    """Callback for error StringVar write trace"""
    background = config.ERR if app.data['error'].get() else config.BG2
    app['file']['file_button'].config(bg=background)

def choose_file():
    """Callback for select file button"""
    filepath = askopenfilename(filetypes=[("Audio files (*.wav)", "*.wav")])
    if filepath:
        samplerate, data = siw.read(filepath)
        app.data['data'] = data

        #tk StringVars
        filename = os.path.basename(filepath)
        app.data['audio_filename'].set(filename)
        app.data['samplerate'].set(samplerate)
        app.data['error'].set(False)

        seconds = math.floor(len(data) / samplerate)
        app.data['data_length'].set(seconds)

def focus(event):
    """Callback for left-click -- stores the selected widget"""
    app.focused_widget_name = str(event.widget)

def analyze():
    """Callback for run button"""
    if not app.data['audio_filename'].get():
        app.data['error'].set(True)
        return

    plots.PLOTTING_ENABLED = False #disable plots during analysis
    chunk_data, chunk_sample_rate = _downconvert()
    tempo_analyser = _analyse_tempo(chunk_data, chunk_sample_rate)
    tonality_analyser = _analyse_tonality(chunk_data, chunk_sample_rate)
    _plot_data(tempo_analyser, tonality_analyser)

def _downconvert():
    #get data from gui
    samplerate = int(app.data.get('samplerate').get())
    data = app.data.get('data')
    conversion_ratio = app.data['conversion_ratio'].get()
    chunk_size = app.data['chunksize'].get()

    #downconvert
    down_converter = DownConverter(samplerate, conversion_ratio, chunk_size)
    chunk_data = down_converter.downconvert_chunk(data, chunk_index=0)
    return chunk_data, down_converter.down_samplerate

def _analyse_tempo(chunk_data, chunk_sample_rate):
    tempo_analyser = tempo.TempoAnalyser(chunk_sample_rate)
    tempo_analyser.BPS_MIN = app.data['bps_min'].get()
    tempo_analyser.BPS_MAX = app.data['bps_max'].get()
    tempo_analyser.DECAY = app.data['decay'].get()
    bpm = tempo_analyser.analyse(chunk_data)
    app.data['bpm'].set(bpm)
    return tempo_analyser

def _analyse_tonality(chunk_data, chunk_sample_rate):
    tonality_analyser = tonality.TonalityAnalyser(chunk_sample_rate)
    tonality_ = tonality_analyser.analyse(chunk_data)
    app.data['tonality'].set(tonality_)
    return tonality_analyser

def _plot_data(tempo_analyser, tonality_analyser):
    dataset1 = figure.DataSet(y=tempo_analyser.local_maximum_data, line_colour=config.PRIM)
    dataset2 = figure.DataSet(y=tempo_analyser.processed_data, line_colour=config.SEC)
    app['plot']['lmv_fig'].tk_component.plot(dataset1, dataset2, normalized=True)

    #get dataset1 annotations from normalized note names
    root_index = tonality_analyser.musical_root_index
    annotations = [consts.MUSICAL_NOTE_NAMES[i] for i in range(root_index - 12, root_index)]

    dataset1 = figure.DataSet(y=tonality_analyser.normalised_note_counts, line_colour=config.SEC)
    dataset1.annotations = annotations
    app['plot']['note_fig'].tk_component.plot(dataset1, normalized=True, annotate=True, bar=True)

    app['plot'].activate()
    app['plot'].pack()
