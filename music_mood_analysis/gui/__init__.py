# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:13:17 2021

@author: Korean_Crimson
"""
#pylint: disable=E0611,E0401
import tkinter as tk

from music_mood_analysis.gui.components import Gui
from music_mood_analysis.gui.components import Tk

root = Tk()
app = Gui(root)

#tk variable declarations
app.data['bpm'] = tk.StringVar()
app.data['tonality'] = tk.StringVar()
app.data['audio_filename'] = tk.StringVar()
app.data['samplerate'] = tk.StringVar()
app.data['data_length'] = tk.IntVar()
app.data['chunksize'] = tk.IntVar()
app.data['conversion_ratio'] = tk.IntVar()
app.data['bps_min'] = tk.DoubleVar()
app.data['bps_max'] = tk.DoubleVar()
app.data['decay'] = tk.DoubleVar()
app.data['error'] = tk.BooleanVar()
