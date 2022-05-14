# -*- coding: utf-8 -*-
"""This module tests the command line interface"""

import pytest

from music_mood_analysis import cli


def test_filepath_missing():
    parser = cli.construct_parser()
    with pytest.raises(SystemExit):
        parser.parse_args([])


def test_filepath():
    parser = cli.construct_parser()
    args = parser.parse_args(["a.wav"])
    assert args.filepath == "a.wav"


@pytest.mark.parametrize(
    "arguments, expected",
    [
        ("a --tempo-analysis fft", "fft"),
        ("a -t lmv", "lmv"),
    ],
)
def test_tempo_analysis(arguments, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(arguments.split())
    assert args.tempo_analysis == expected


@pytest.mark.parametrize("arguments", ["a --tempo-analysis", "a -t", "a -t abc"])
def test_tempo_analysis_fail(arguments):
    parser = cli.construct_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(arguments.split())


@pytest.mark.parametrize(
    "arguments, expected",
    [
        ("a --downsample 3", 3),
        ("a -d 15", 15),
    ],
)
def test_downsample(arguments, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(arguments.split())
    assert args.downsample == expected


@pytest.mark.parametrize(
    "arguments",
    [
        ("a --downsample 3.2"),
        ("a -d 15.5"),
    ],
)
def test_downsample_fail(arguments):
    parser = cli.construct_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(arguments.split())


@pytest.mark.parametrize(
    "arguments, expected",
    [
        ("a --min-bps 2.6", 2.6),
    ],
)
def test_min_bps(arguments, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(arguments.split())
    assert args.min_bps == expected


@pytest.mark.parametrize(
    "arguments, expected",
    [
        ("a --max-bps 8.5", 8.5),
    ],
)
def test_max_bps(arguments, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(arguments.split())
    assert args.max_bps == expected


@pytest.mark.parametrize(
    "arguments, expected",
    [
        ("a --lmv-decay 23.4", 23.4),
    ],
)
def test_lmv_decay(arguments, expected):
    parser = cli.construct_parser()
    args = parser.parse_args(arguments.split())
    assert args.lmv_decay == expected


@pytest.mark.parametrize(
    "arguments",
    [
        "a.wav -d 5",
        "abc.wav",
        "test.wav -d 15 --chunk-size 12",
        "a.wav -t fft",
    ],
)
def test_display_args(arguments):
    parser = cli.construct_parser()
    args = parser.parse_args(arguments.split())
    cli.display_args(args)
