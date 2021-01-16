# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 23:39:42 2021

@author: Korean_Crimson
"""

import sys
import subprocess
import py

def main(open_in_browser=False):
    """Add package under test to PYTHONPATH, run pytest to generate html report
    and open the report in the browser.
    """
    sys.path.append('..\\music_mood_analysis')
    #pylint: disable=E1101
    py.test.cmdline.main(args=['--html=report.html', '--self-contained-html'])

    if open_in_browser:
        subprocess.call('start report.html', shell=True)

if __name__ == '__main__':
    main()
