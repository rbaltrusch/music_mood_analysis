# -*- coding: utf-8 -*-
"""Module to construct the cli parser"""

import logging
import argparse


def construct_parser() -> argparse.ArgumentParser:
    """Constructs the cli argument parser"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "filepath",
        type=str,
        help="The path to the audio file to be analysed",
    )

    parser.add_argument(
        "--tempo-analysis",
        "-t",
        choices=["fft", "lmv"],
        default="fft",
        help="The tempo analysis method to be used",
    )

    parser.add_argument(
        "--chunk-size",
        "-c",
        type=int,
        help="The size (in seconds) of audio data chunk to be analysed at once",
    )

    parser.add_argument(
        "--downsample",
        "-d",
        default=32,
        type=int,
        help="The factor by which to downsample audio data during analysis",
    )

    parser.add_argument(
        "--min-bps",
        default=1.5,
        type=float,
        help="The minimum amount of beats per second to be considered during tempo analysis",
    )

    parser.add_argument(
        "--max-bps",
        default=3.0,
        type=float,
        help="The maximum amount of beats per second to be considered during tempo analysis",
    )

    parser.add_argument(
        "--lmv-decay",
        default=0.000_1,
        type=float,
        help="The amplitude decay of local maxima during lmv tempo analysis",
    )

    return parser


def display_args(args):
    """Logs all attributes of the arguments namespace passed"""
    for name, value in vars(args).items():
        logging.info("Using setting %s: %s", name, value)
