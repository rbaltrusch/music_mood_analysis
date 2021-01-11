# Music mood analysis

Real-time analysis of music, extracting tempo and tonality.

The current configuration uses a .wav file to test the analysis functionality. However, it does this using a stream of around 14 data chunks per second, which could be either be read from a file or be provided by a funnel script reading audio data directly from audio hardware. Such a script is not included in this repository, as it is hardware-specific.

Written in Python 3.8.3
