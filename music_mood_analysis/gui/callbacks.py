# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:17:38 2021

@author: Korean_Crimson
"""

import os
import math
from tkinter.filedialog import askopenfilename
import scipy.io.wavfile as siw

import tonality
import tempo
from dataconversion import downconvert_chunk
import plots
import consts
from gui import app, config, figure

def set_gui_config_defaults(*_):
    """Callback for reset button"""
    app.data['chunksize'].set(consts.CHUNK_SIZE)
    app.data['conversion_ratio'].set(consts.CONVERSION_RATIO)
    app.data['bps_min'].set(consts.BPS_MIN)
    app.data['bps_max'].set(consts.BPS_MAX)
    app.data['allowance'].set(consts.BEAT_DISTANCE_HYPOTHESIS_ALLOWANCE_PERCENTAGE)
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

    #get gui data
    samplerate = int(app.data.get('samplerate').get())
    data = app.data.get('data')

    _set_analysis_constants()
    _analyze(samplerate, data)
    _plot_data()

def _set_analysis_constants():
    plots.PLOTTING_ENABLED = False #disable plots inside analysis
    tempo.BPS_MIN = app.data['bps_min'].get()
    tempo.BPS_MAX = app.data['bps_max'].get()
    tempo.BEAT_DISTANCE_HYPOTHESIS_ALLOWANCE_PERCENTAGE = app.data['allowance'].get()
    tempo.DECAY = app.data['decay'].get()

def _analyze(samplerate, data):
    #get data from gui
    conversion_ratio = app.data['conversion_ratio'].get()
    chunk_size = app.data['chunksize'].get()

    #downconvert
    args = [samplerate, data, conversion_ratio, chunk_size]
    chunk_sample_rate, chunk_data = downconvert_chunk(*args, chunk_index=0)

    #run analysis
    bpm, local_maximum_values, data_ = tempo.analyse(chunk_sample_rate, chunk_data)
    tonality_, key, normalized_note_counts = tonality.analyse(chunk_sample_rate, chunk_data)

    #set data for plots
    app.data['local_maximum_values'] = local_maximum_values
    app.data['normalized_note_counts'] = normalized_note_counts
    app.data['transformed_data'] = data_
    app.data['key'] = key

    #set tk StringVars
    app.data['chunk_samplerate'].set(chunk_sample_rate)
    app.data['bpm'].set(bpm)
    app.data['tonality'].set(f'{key} {tonality_}')

def _plot_data():
    dataset1 = figure.DataSet(y=app.data.get('local_maximum_values'), line_colour=config.PRIM)
    dataset2 = figure.DataSet(y=app.data.get('transformed_data'), line_colour=config.SEC)
    app['plot']['lmv_fig'].tk_component.plot(dataset1, dataset2, normalized=True)

    #get dataset1 annotations from noramlized note names
    root_index = consts.MUSICAL_NOTE_NAMES.index(app.data['key'])
    annotations = [consts.MUSICAL_NOTE_NAMES[i] for i in range(root_index - 12, root_index)]

    dataset1 = figure.DataSet(y=app.data.get('normalized_note_counts'), line_colour=config.SEC)
    dataset1.annotations = annotations
    app['plot']['note_fig'].tk_component.plot(dataset1, normalized=True, annotate=True, bar=True)

    app['plot'].activate()
    app['plot'].pack()
