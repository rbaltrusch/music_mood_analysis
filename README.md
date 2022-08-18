[![Unit tests](https://github.com/rbaltrusch/music_mood_analysis/actions/workflows/pytest-unit-tests.yml/badge.svg)](https://github.com/rbaltrusch/music_mood_analysis/actions/workflows/pytest-unit-tests.yml)
[![Pylint](https://github.com/rbaltrusch/music_mood_analysis/actions/workflows/pylint.yml/badge.svg)](https://github.com/rbaltrusch/music_mood_analysis/actions/workflows/pylint.yml)
[![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

# Music Mood Analysis

This analysis tool extracts tempo and tonality from music using digital signal processing techniques to analyse the mood of a piece of music.

The tool comes with a graphical user interface, which may be used to select the file to be analysed, configure the analysis parameters, run the analysis and finally inspect the analysis results.

![Screenshot of the analysis GUI](https://github.com/rbaltrusch/music_mood_analysis/blob/master/music_mood_analysis/gui/media/screenshot2.png?raw=true "Screenshot of the analysis GUI")

## Getting started

To run the package, install it using pip, then run it using:

    python -m pip install music_mood_analysis
    python -m music_mood_analysis

## Command line interface

The music analysis tool can also be used directly with its command line interface, bypassing the graphical interface completely:

```
usage: __main__.py [-h] [--tempo-analysis {fft,lmv}] [--chunk-size CHUNK_SIZE]
                   [--downsample DOWNSAMPLE] [--min-bps MIN_BPS]
                   [--max-bps MAX_BPS] [--lmv-decay LMV_DECAY]
                   filepath

positional arguments:
  filepath              The path to the audio file to be analysed

optional arguments:
  -h, --help            show this help message and exit
  --tempo-analysis {fft,lmv}, -t {fft,lmv}
                        The tempo analysis method to be used
  --chunk-size CHUNK_SIZE, -c CHUNK_SIZE
                        The size (in seconds) of audio data chunk to be
                        analysed at once
  --downsample DOWNSAMPLE, -d DOWNSAMPLE
                        The factor by which to downsample audio data during
                        analysis
  --min-bps MIN_BPS     The minimum amount of beats per second to be
                        considered during tempo analysis
  --max-bps MAX_BPS     The maximum amount of beats per second to be
                        considered during tempo analysis
  --lmv-decay LMV_DECAY
                        The amplitude decay of local maxima during lmv tempo
                        analysis
```

To bring up this help message, run:

```
python -m music_mood_analysis -h
```

## Real-time

The tool used to be configured to be used in a real-time analysis setting for analysis of ambient music. In the current configuration of the script, this is currently not possible anymore; however, it should not be too hard to re-instate the real-time functionality if required.

The current configuration uses a .wav file to test the analysis functionality. It streams several data chunks per second from the file, which could be either be read from a file or be provided by a funnel script reading audio data directly from audio hardware. Such a script is not included in this repository, as it is hardware-specific.

## Contributions

To contribute to this repository, please read the [contribution guidelines](https://github.com/rbaltrusch/music_mood_analysis/blob/master/CONTRIBUTING.md).

## Python

Written in Python 3.8.3.

## License

This repository is open-source software available under the [AGPL-3.0 License](https://github.com/rbaltrusch/music_mood_analysis/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
