# Music mood analysis

Real-time analysis of music, extracting tempo and tonality.

The current configuration uses a .wav file to test the analysis functionality. However, it does this using a stream of around 14 data chunks per second, which could be either be read from a file or be provided by a funnel script reading audio data directly from audio hardware. Such a script is not included in this repository, as it is hardware-specific.

The analysis tool comes with a minimalistic graphical user interface, which may be used to select the file to be analysed, configure the analysis parameters, run the analysis and finally inspect the analysis results.

![Screenshot of the analysis GUI](music_mood_analysis/gui/media/screenshot.png?raw=true "Screenshot of the analysis GUI")
*Screenshot of the analysis GUI*

Written in Python 3.8.3
