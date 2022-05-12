# -*- coding: utf-8 -*-
"""
Created on Sun Jan 31 17:57:26 2021

@author: Korean_Crimson
"""
#pylint: disable=import-error
#pylint: disable=line-too-long
import os
import tkinter as tk

from music_mood_analysis.gui import app
from music_mood_analysis.gui import callbacks
from music_mood_analysis.gui import components
from music_mood_analysis.gui import config
from music_mood_analysis.gui import figure
from music_mood_analysis.gui import root

def init():
    """Initializes root and all views of gui app"""
    init_root()
    file_view = init_file_view()
    config_view = init_config_view()
    plot_view = init_plot_view()
    app.views_dict = {'file': file_view, 'config': config_view, 'plot': plot_view}

def init_root():
    """Initialize tkinter root"""
    #configure root
    root.title(config.TITLE)
    root['bg'] = config.BG
    root.focus_force()

    #set trace callbacks
    root.bind_all("<Button-1>", callbacks.focus)
    app.data['data_length'].trace_add('write', callbacks.set_scale)
    app.data['error'].trace_add('write', callbacks.set_error)

    #set window icon
    icon_path = os.path.join(os.path.dirname(__file__), 'media', 'icon.png')
    root.set_icon(icon_path)

def init_file_view():
    """Initializes file select view"""
    view = components.View()
    view.activate()

    frame = tk.Frame(root, bd=0, bg=config.BG)
    component = components.Frame(frame, sticky='NSEW', row=0, column=0, row_span=2, column_span=3, padx=10, pady=10)
    component.add_col(0)
    component.add_col(0)
    component.add_col(0)
    view.add_frame_component(component, 'frame')

    #File disp
    file_label = tk.Label(frame, text='Audio file', **config.LABEL_THEME)
    component = components.Component(file_label, sticky='NSE', row=0, column=0, padx=5)
    view.add_component(component, 'file_label')

    file_entry = tk.Entry(frame, textvariable=app.data['audio_filename'], **config.DYNAMIC_ENTRY_THEME)
    component = components.Component(file_entry, sticky='NSEW', row=0, column=1)
    view.add_component(component, 'file_entry')

    #Choose file button
    file_button = tk.Button(frame, text='Select file', command=callbacks.choose_file, **config.BUTTON_THEME)
    component = components.Component(file_button, sticky='NSEW', row=0, column=2, row_span=2)
    view.add_component(component, 'file_button')

    #Samplerate disp
    samplerate_label = tk.Label(frame, text='Samplerate', **config.LABEL_THEME)
    component = components.Component(samplerate_label, sticky='NSE', row=1, column=0, padx=5)
    view.add_component(component, 'samplerate_label')

    samplerate_entry = tk.Entry(frame, textvariable=app.data['samplerate'], **config.DYNAMIC_ENTRY_THEME)
    component = components.Component(samplerate_entry, sticky='NSEW', row=1, column=1)
    view.add_component(component, 'samplerate_entry')
    return view

def init_config_view():
    """Initializes analysis configuration view"""
    #pylint: disable=too-many-locals
    #pylint: disable=too-many-statements
    view = components.View()
    view.activate()
    callbacks.set_gui_config_defaults()

    frame = tk.Frame(root, bd=0, bg=config.BG)
    component = components.Frame(frame, sticky='NSEW', row=2, column=0, row_span=6, column_span=3, padx=10, pady=10)
    component.add_col(0)
    component.add_col(0)
    component.add_col(110)
    view.add_frame_component(component, 'frame')

    #CHUNK_SIZE
    chunksize_label = tk.Label(frame, text='Chunk size (sec)', **config.LABEL_THEME)
    component = components.Component(chunksize_label, sticky='NSE', row=0, column=0, padx=5)
    view.add_component(component, 'chunksize_label')

    chunksize_scale = tk.Scale(frame, from_=0, to=10, orient='horizontal', variable=app.data['chunksize'], bd=0, **config.SCALE_THEME)
    component = components.Component(chunksize_scale, sticky='NSEW', row=0, column=1)
    view.add_component(component, 'chunksize_scale')

    #CONVERSION_RATIO
    conversion_label = tk.Label(frame, text='Conversion ratio', **config.LABEL_THEME)
    component = components.Component(conversion_label, sticky='NSE', row=1, column=0, padx=5)
    view.add_component(component, 'conversion_label')

    conversion_scale = tk.Scale(frame, from_=1, to=64, orient='horizontal', variable=app.data['conversion_ratio'], bd=0, **config.SCALE_THEME)
    component = components.Component(conversion_scale, sticky='NSEW', row=1, column=1)
    view.add_component(component, 'conversion_scale')

    #BPS_MIN
    bps_min_label = tk.Label(frame, text='Minimum beats/s', **config.LABEL_THEME)
    component = components.Component(bps_min_label, sticky='NSE', row=2, column=0, padx=5)
    view.add_component(component, 'bps_min_label')

    bps_min_scale = tk.Scale(frame, from_=0.5, to=5, orient='horizontal', digits=2, resolution=0.1, variable=app.data['bps_min'], bd=0, **config.SCALE_THEME)
    component = components.Component(bps_min_scale, sticky='NSEW', row=2, column=1)
    view.add_component(component, 'bps_min_scale')

    #BPS_MAX
    bps_max_label = tk.Label(frame, text='Maximum beats/s', **config.LABEL_THEME)
    component = components.Component(bps_max_label, sticky='NSE', row=3, column=0, padx=5)
    view.add_component(component, 'bps_max_label')

    bps_max_scale = tk.Scale(frame, from_=0.5, to=5, orient='horizontal', digits=2, resolution=0.1, variable=app.data['bps_max'], bd=0, **config.SCALE_THEME)
    component = components.Component(bps_max_scale, sticky='NSEW', row=3, column=1)
    view.add_component(component, 'bps_max_scale')

    #DECAY
    decay_label = tk.Label(frame, text='Local maximum decay/sample', **config.LABEL_THEME)
    component = components.Component(decay_label, sticky='NSE', row=4, column=0, padx=5)
    view.add_component(component, 'decay_label')

    decay_scale = tk.Scale(frame, from_=0, to=0.001, orient='horizontal', digits=2, resolution=0.0001, variable=app.data['decay'], bd=0, **config.SCALE_THEME)
    component = components.Component(decay_scale, sticky='NSEW', row=4, column=1)
    view.add_component(component, 'decay_scale')

    #reset defaults button
    reset_button = tk.Button(frame, text='Reset', command=callbacks.set_gui_config_defaults, **config.BUTTON_THEME)
    component = components.Component(reset_button, sticky='NSEW', row=0, row_span=2, column=2)
    view.add_component(component, 'reset_button')

    #run button
    run_button = tk.Button(frame, text='Run', command=callbacks.analyze, **config.BUTTON_THEME)
    component = components.Component(run_button, sticky='NSEW', row=2, row_span=3, column=2)
    view.add_component(component, 'run_button')

    return view

def init_plot_view():
    """Initializes results and plots view"""
    view = components.View()
    view.activate()

    frame = tk.Frame(root, bd=0, bg=config.BG)
    component = components.Frame(frame, sticky='NSEW', row=13, column=0, column_span=3, row_span=4, padx=10, pady=10)
    component.add_col(0)
    component.add_col(0)
    component.add_col(140)
    view.add_frame_component(component, 'frame')

    #tonality disp
    tonality_label = tk.Label(frame, text='Tonality', **config.LABEL_THEME)
    component = components.Component(tonality_label, sticky='NSE', row=0, column=0, padx=5)
    view.add_component(component, 'tonality_label')

    tonality_entry = tk.Entry(frame, textvariable=app.data['tonality'], **config.DYNAMIC_ENTRY_THEME)
    component = components.Component(tonality_entry, sticky='NSEW', row=0, column=1, column_span=2)
    view.add_component(component, 'tonality_entry')

    #tempo disp
    tempo_label = tk.Label(frame, text='Beats per minute', **config.LABEL_THEME)
    component = components.Component(tempo_label, sticky='NSE', row=1, column=0, padx=5)
    view.add_component(component, 'tempo_label')

    tempo_entry = tk.Entry(frame, textvariable=app.data['bpm'], **config.DYNAMIC_ENTRY_THEME)
    component = components.Component(tempo_entry, sticky='NSEW', row=1, column=1, column_span=2)
    view.add_component(component, 'tempo_entry')

    #figures
    lmv_fig = figure.Figure(frame, config.BG, config.FG)
    lmv_fig.set_labels(title='Local maximum values', x_title='Time', y_title='Amplitude')
    component = components.Component(lmv_fig, sticky='NSEW', row=2, column=1)
    view.add_component(component, 'lmv_fig')

    note_fig = figure.Figure(frame, config.BG, config.FG)
    note_fig.set_labels(title='Normalized note counts', x_title='Time', y_title='Amplitude')
    component = components.Component(note_fig, sticky='NSEW', row=2, column=2)
    view.add_component(component, 'note_fig')
    return view
