# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 15:08:31 2021

@author: Korean_Crimson
"""

#pylint: disable=line-too-long

import os
import sys
import ctypes
import tkinter as tk

class Tk(tk.Tk):
    """Extends tk.Tk as root of the app for better row, col and icon API"""

    def __init__(self):
        super().__init__()
        self.col_num = 0
        self.row_num = 0

    def add_row(self, minsize, weight=1):
        """Extends rowconfigure with handy defaults"""
        self.rowconfigure(self.row_num, minsize=minsize, weight=weight)
        self.row_num += 1

    def add_col(self, minsize, weight=1):
        """Extends columnconfigure with handy defaults"""
        self.columnconfigure(self.col_num, minsize=minsize, weight=weight)
        self.col_num += 1

    def add_frames(self):
        """Adds empty frames to each row and column so that tk doesnt collapse
        empty grid cells.
        """
        for row in range(self.row_num):
            for col in range(self.col_num):
                frame = tk.Frame(self)
                frame.grid(row=row, column=col)

    def set_icon(self, icon_path):
        """Sets window icon, and taskbar icon (only on Windows)"""
        if not os.path.isfile(icon_path):
            return
        photo = tk.PhotoImage(file=icon_path)
        self.iconphoto(False, photo)
        self._set_taskbar_icon()

    @staticmethod
    def _set_taskbar_icon():
        """Required to set taskbar icon for windows, otherwise the tkinter window
        is recognized by windows as being grouped together with python.exe.
        See: https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105
        """
        if sys.platform.startswith('win32'):
            myappid = 'mycompany.myproduct.subproduct.version' # arbitrary string
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class Gui:
    """Main gui class to hold references to all components, data and tk Vars used
    in the gui
    """

    def __init__(self, window):
        self.window = window
        self.views_dict = {}
        self.data = {}
        self.focused_widget_name = None

    def __getitem__(self, view_name):
        return self.views_dict[view_name]

    def mainloop(self):
        """Calls tk.root.mainloop"""
        self.window.mainloop()

    def pack_all(self):
        """Adds all active views to gui (via View.pack)"""
        for view in self.views_dict.values():
            if view.active:
                view.pack()
            else:
                view.unpack()

    def deactivate_all(self):
        """Deactivates all views"""
        for view in self.views_dict.values():
            view.deactivate()

    def switch_to(self, *keys):
        """Switches to a particular view by activating it and deactivating all others"""
        self.deactivate_all()
        for key in keys:
            self.views_dict[key].activate()
        self.pack_all()

class View():
    """View class to group together conceptually related tk widgets, which then
    can be collectively shown or hidden
    """

    def __init__(self):
        self.active = False
        self._components = {}
        self._frame_components = {}

    def __getitem__(self, component_name):
        return self._all_components[component_name]

    def get_frames(self):
        """returns all frame_components stored in the view"""
        return self._frame_components.values()

    def clear(self):
        """unpack the view and remove all its components and frame_components"""
        self.unpack()
        self._components = {}
        self._frame_components = {}

    def activate(self):
        """activate the view.

        This will not show the view right away, but the view will instead be
        packed next time that the components.Gui.pack_all method is called.
        """
        self.active = True

    def deactivate(self):
        """deactivate the view.

        This will not hide the view right away, but the view will instead not be
        packed next time that the components.Gui.pack_all method is called
        """
        self.active = False

    def add_component(self, component, name):
        """add components.Component and its name (needs to be unique)"""
        self._components[name] = component

    def add_frame_component(self, component, name):
        """add frame component. This MUST be used for gui components whose type
        is tk.Frame, as the frames must be added to grid before their contents

        name needs to be unique.
        """
        self._frame_components[name] = component

    def pack(self):
        """calls gridpack for all components in the view"""
        for component in self._all_components.values():
            component.gridpack()

    def repack(self):
        """unpacks, then packs the view (for refresh purposes)"""
        self.unpack()
        self.pack()

    def unpack(self):
        """calls unpack for all components in the view"""
        for component in self._all_components.values():
            component.unpack()

    def hide_component(self, component_name):
        """hides the component specified by its name"""
        self._all_components[component_name].hide()

    def unhide_component(self, component_name):
        """unhides the component specified by its name"""
        component = self._all_components[component_name]
        component.unhide()
        component.gridpack()

    @property
    def _all_components(self):
        return {**self._components, **self._frame_components}


#pylint: disable=R0902,R0913
class Component():
    """Wrapper class around tk widgets that holds all information required
    for grid manager, which allows adding or removing widgets from grid easily
    """

    def __init__(self, tk_component, row=0, column=0, sticky='n', padx=0, pady=0, column_span=1, row_span=1, var=None):
        self.tk_component = tk_component
        self.row = row
        self.column = column
        self.sticky = sticky
        self.padx = padx
        self.pady = pady
        self.column_span = column_span
        self.row_span = row_span
        self.hidden = False
        self.var = var
        self.data = None

    def hide(self):
        """hides the component"""
        self.hidden = True
        self.unpack()

    def unhide(self):
        """unhides the component"""
        self.hidden = False

    def gridpack(self):
        """places tk widget on the grid if not hidden"""
        if not self.hidden:
            self.tk_component.grid(row=self.row,
                                   column=self.column,
                                   sticky=self.sticky,
                                   padx=self.padx,
                                   pady=self.padx,
                                   rowspan=self.row_span,
                                   columnspan=self.column_span
                                   )

    def unpack(self):
        """wraps tk widget grid_forget method"""
        self.tk_component.grid_forget()

    def config(self, *args, **kwargs):
        """Wraps tk widget config method"""
        self.tk_component.config(*args, **kwargs)

class Frame(Component):
    """Wrapper class around tk frame widgets that holds all information required
    for grid manager, which allows adding or removing widgets from grid easily.

    Inherits all attributes and methods from Component class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.col_num = 0
        self.row_num = 0

    def add_row(self, minsize, weight=1):
        """Extends tk.Frame.rowconfigure with handy defaults"""
        self.tk_component.rowconfigure(self.row_num, minsize=minsize, weight=weight)
        self.row_num += 1

    def add_col(self, minsize, weight=1):
        """Extends tk.Frame.columnconfigure with handy defaults"""
        self.tk_component.columnconfigure(self.col_num, minsize=minsize, weight=weight)
        self.col_num += 1
