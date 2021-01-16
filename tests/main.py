# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 23:39:42 2021

@author: Korean_Crimson
"""

import os
import sys
import datetime
import subprocess
import py

PACKAGE_NAME = 'music_mood_analysis'
REPORTS_PATH = 'reports'

def main(open_in_browser=False):
    """Add package under test to PYTHONPATH, run pytest to generate html report
    and open the report in the browser.
    """
    package_path = os.path.join('..', PACKAGE_NAME)
    sys.path.append(package_path)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f'{timestamp}_report.html'
    report_filepath = os.path.join(REPORTS_PATH, report_filename)

    #pylint: disable=E1101
    py.test.cmdline.main(args=[f'--html={report_filepath}',
                               '--self-contained-html',
                               f'--cov={package_path}'
                               ])

    if open_in_browser:
        subprocess.call('start report.html', shell=True)

if __name__ == '__main__':
    main()
