# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:43:43 2021

@author: Korean_Crimson
"""

import math
from dataclasses import dataclass

from music_mood_analysis import consts


@dataclass
class DownConverter:
    """Downconverts data from one samplerate to a lower one"""

    samplerate: int
    conversion_ratio: int = consts.CONVERSION_RATIO
    chunk_size: int = consts.CHUNK_SIZE

    def downconvert(self, data: list) -> list:
        """Returns the data downsampled by the conversion_ratio."""
        return [self._mono(d) for d in data[:: self.conversion_ratio]]

    def downconvert_chunk(self, data: list, chunk_index=0) -> list:
        """Returns the downsampled samplerate and data for a specified data chunk.
        This is useful to analyse data in a data stream rather than all at once.

        chunk_index specifies extracted chunk of data, starting at 0.
        """
        data_chunk = self._extract_data_chunk(data, chunk_index)
        return self.downconvert(data_chunk)

    def _extract_data_chunk(self, data, chunk_index):
        index = self.chunk_length * chunk_index
        return data[index : index + self.chunk_length]

    @staticmethod
    def _mono(stereo_data_point):
        """Converts one stereo data point to one mono data point"""
        try:
            return int(sum(stereo_data_point))
        except TypeError:  # not iterable
            return int(stereo_data_point)

    @property
    def chunk_length(self) -> int:
        """Getter for chunk_length, returns chunk_size times samplerate or 0 if negative"""
        return max(round(self.chunk_size * self.samplerate), 0)

    @property
    def down_samplerate(self) -> int:
        """The downsampled samplerate"""
        return math.ceil(self.samplerate / self.conversion_ratio)
