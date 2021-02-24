# Music mood analysis

This analysis tool extracts tempo and tonality from music using digital signal processing techniques.

The tool comes with a graphical user interface, which may be used to select the file to be analysed, configure the analysis parameters, run the analysis and finally inspect the analysis results.

![Screenshot of the analysis GUI](music_mood_analysis/gui/media/screenshot2.png?raw=true "Screenshot of the analysis GUI")
*Screenshot of the analysis GUI*

## Real-time

The tool used to be configured to be used in a real-time analysis setting for analysis of ambient music. In the current configuration of the script, this is currently not possible anymore; however, it should not be too hard to re-instate the real-time functionality if required.

The current configuration uses a .wav file to test the analysis functionality. It streams several data chunks per second from the file, which could be either be read from a file or be provided by a funnel script reading audio data directly from audio hardware. Such a script is not included in this repository, as it is hardware-specific.

## Getting started

To get a copy of this repository, simply open up git bash in an empty folder and use the command:

    $ git clone https://github.com/rbaltrusch/music_mood_analysis

To install all python dependencies, run the following in your command line:

    python -m pip install -r requirements.txt

## Documentation

More documentation is planned to be included in the [wiki](https://github.com/rbaltrusch/music_mood_analysis/wiki).

## Python

Written in Python 3.8.3

## License

This repository is open-source software available under the [AGPL-3.0 License](https://github.com/rbaltrusch/music_mood_analysis/blob/master/LICENSE).

## Contact

Please raise an issue for code changes. To reach out, please send an email to richard@baltrusch.net.
