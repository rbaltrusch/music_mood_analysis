# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:26:16 2021

@author: Korean_Crimson
"""

TITLE = 'Music Mood Analysis'

#colours
FG = '#FFFFFF'
BG = '#121212'
BG2 = '#242424'
BG3 = '#363636'
BG4 = '#484848'
BG5 = '#606060'
PRIM = '#3700B3'
SEC = '#A172E1'
ERR = '#CF6679'

#themes
THEME = {'fg': FG, 'bg': BG2, 'highlightbackground': BG3}
_ACTIVE_THEME0 = {**THEME, 'activebackground': BG3}

DYNAMIC_ENTRY_THEME = {**THEME, 'state': 'disabled', 'disabledbackground': BG2}
LABEL_THEME = {'fg': FG, 'bg': BG, 'highlightbackground': BG2}
BUTTON_THEME = {**_ACTIVE_THEME0, 'activeforeground': FG}
SCALE_THEME = {**_ACTIVE_THEME0, 'troughcolor': BG5}
