# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 14:41:51 2021

@author: Korean_Crimson
"""
#pylint: disable=invalid-name
from dataclasses import dataclass
from dataclasses import field
from typing import Iterable
from typing import Optional

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

@dataclass
class DataSet:
    """Dataset class to be used for plotting using figure.Figure"""

    x: Optional[Iterable[float]] = None
    y: Optional[Iterable[float]] = None
    line_colour: str = '#FFFFFF'
    annotations: Iterable[str] = field(default_factory=list)

    def __iter__(self):
        for item in [self.x, self.y, self.line_colour]:
            if item is not None:
                yield item

    def normalize(self):
        """Normalizes the y dataset by dividing all points in it by its maximum"""
        if isinstance(self.y, list):
            max_ = max(self.y)
            self.y = [point / max_ for point in self.y]
        return self

    @property
    def x_limits(self):
        """returns x axis limits for matplotlib.axes.Axes.set_xlim"""
        return self._get_limits(self.x) if self.x is not None else (0, len(self.y) - 1)

    @property
    def y_limits(self):
        """returns y axis limits for matplotlib.axes.Axes.set_ylim"""
        return self._get_limits(self.y)

    @staticmethod
    def _get_limits(array):
        """returns tuple of min and max of passed array. defaults to (0, 1)"""
        return (0, 1) if array is None else (min(array), max(array))

class Figure:
    """Wrapper class around matplotlib plots for tkinter (FigureCanvasTkAgg)"""

    def __init__(self,  parent, bg_colour, axes_colour):
        self.parent = parent
        self.bg_colour = bg_colour
        self.axes_colour = axes_colour
        self.figure = matplotlib.figure.Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.parent)
        self.tk_widget = self.canvas.get_tk_widget()
        rect = self.figure.patch
        rect.set_facecolor(self.bg_colour)

    #pylint: disable=disallowed-name #bar
    def plot(self, *datasets, normalized=False, annotate=False, bar=False):
        """Plots the passed datasets.
        If normalized=True, the datasets are normalized first.
        If annotate=True, each point in the datasets gets annotated with custom text
            (the annotations must previously have been stored in DataSet.annotations)
        """
        self.axes.clear()

        if normalized:
            datasets = self._normalize(datasets)

        for dataset in datasets:
            if bar:
                self.axes.bar(list(range(len(dataset.y))), dataset.y, color=dataset.line_colour)
            else:
                self.axes.plot(*dataset)

            self.axes.set_xlim(*dataset.x_limits)

            if normalized:
                self.axes.set_yticks([x * 0.2 for x in range(7)]) #0 to 1.2
            else:
                self.axes.set_ylim(*dataset.y_limits)

            if annotate and dataset.annotations:
                #adjust for center alignment of bars
                xticks = list(range(-1, len(dataset.annotations) + 1))
                annotations = [''] + dataset.annotations + ['']

                #set number of ticks and their labels
                self.axes.set_xticks(xticks)
                self.axes.set_xticklabels(annotations)

    def grid(self, *args, **kwargs):
        """Adds the tk widget to the grid"""
        self._colour_axes()
        self.tk_widget.grid(*args, **kwargs)
        self.canvas.draw()

    def grid_forget(self, *args, **kwargs):
        """Removes the tk widget from the grid"""
        self.tk_widget.grid_forget(*args, **kwargs)

    def config(self, *args, **kwargs):
        """Calls config on the tk widget"""
        self.tk_widget.config(*args, **kwargs)

    def _colour_axes(self):
        self.axes.set_facecolor(self.bg_colour)
        self.axes.spines['bottom'].set_color(self.axes_colour)
        self.axes.spines['top'].set_color(self.axes_colour)
        self.axes.spines['right'].set_color(self.axes_colour)
        self.axes.spines['left'].set_color(self.axes_colour)
        self.axes.tick_params(axis='x', colors=self.axes_colour, which='both')
        self.axes.tick_params(axis='y', colors=self.axes_colour, which='both')

    def set_labels(self, title='', x_title='', y_title='', title_fontsize=12, axes_fontsize=10):
        """Sets title and axes titles"""
        #pylint: disable=R0913
        self.axes.set_title (title, fontsize=title_fontsize, color=self.axes_colour)
        self.axes.set_ylabel(y_title, fontsize=axes_fontsize, color=self.axes_colour)
        self.axes.set_xlabel(x_title, fontsize=axes_fontsize, color=self.axes_colour)

    @staticmethod
    def _normalize(datasets):
        return [dataset.normalize() for dataset in datasets]
