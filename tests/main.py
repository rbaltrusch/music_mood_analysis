# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 23:39:42 2021

@author: Korean_Crimson
"""

import os
import sys
import time
import datetime
import subprocess
import py

PACKAGE_NAME = 'music_mood_analysis'
REPORTS_PATH = 'reports'

def main(open_in_browser=True, keep=False, include_slow=True, include_unreliable=True):
    """Add package under test to PYTHONPATH, run pytest to generate html report
    and open the report in the browser.
    """
    package_path = os.path.join('..', PACKAGE_NAME)
    sys.path.append(package_path)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    report_filename = f'{timestamp}_report.html'
    report_filepath = os.path.join(REPORTS_PATH, report_filename)

    command_line_args = [f'--html={report_filepath}',
                         '--self-contained-html',
                         f'--cov={package_path}',
                         f'--cov-report=html']

    if not include_slow:
        command_line_args.append('-m not slow')

    if not include_unreliable:
        command_line_args.append('m not unreliable')

    #pylint: disable=E1101
    py.test.cmdline.main(args=command_line_args)

    if open_in_browser:
        subprocess.call(f'start {report_filepath}', shell=True) #open test report
        subprocess.call(f'start htmlcov/index.html', shell=True) #open coverage report

    if not keep:
        #wait 1 second until test report is open, then delete it
        time.sleep(1)
        os.remove(report_filepath)

if __name__ == '__main__':
    main()
