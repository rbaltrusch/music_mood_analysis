# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 14:47:09 2021

@author: Korean_Crimson
"""

import functools
import sys
import logging
from typing import Dict, Type
import scipy.io.wavfile as siw

from music_mood_analysis.gui import app, init
from music_mood_analysis import cli, dataconversion, tempo, tonality


def run_gui():
    """Runs the music analysis graphical interface"""
    init.init()
    app.pack_all()
    app.mainloop()


def _construct_tempo_analyser(args, samplerate):
    tempo_analyser_types: Dict[str, Type[tempo.AbstractTempoAnalyser]] = {
        "fft": tempo.FFTTempoAnalyser,
        "lmv": functools.partial(tempo.TempoAnalyser, DECAY=args.lmv_decay),
    }
    tempo_analyser_type = tempo_analyser_types[args.tempo_analysis]
    tempo_analyser = tempo_analyser_type(
        samplerate,
        BPS_MIN=args.min_bps,
        BPS_MAX=args.max_bps,
    )
    return tempo_analyser


def run_cli():
    """Runs the command line interface"""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    parser = cli.construct_parser()
    args = parser.parse_args()
    cli.display_args(args)

    samplerate, data = siw.read(args.filepath)
    down_converter = dataconversion.DownConverter(
        samplerate, conversion_ratio=args.downsample, chunk_size=args.chunk_size
    )
    down_sampled_data = (
        down_converter.downconvert(data)
        if args.chunk_size is None
        else down_converter.downconvert_chunk(data, chunk_index=0)
    )

    tonality_analyser = tonality.TonalityAnalyser(
        samplerate=down_converter.down_samplerate
    )
    tonality_ = tonality_analyser.analyse(down_sampled_data)

    tempo_analyser = _construct_tempo_analyser(
        args, samplerate=down_converter.down_samplerate
    )
    tempo_ = tempo_analyser.analyse(down_sampled_data)

    logging.info("Tonality: %s", tonality_)
    logging.info("Tempo: %s", tempo_)


def main():
    """Main function"""
    entry_point = run_gui if len(sys.argv) <= 1 else run_cli
    entry_point()


main()
