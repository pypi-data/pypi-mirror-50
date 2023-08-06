"""A flask of techela."""

import argparse
import os
import subprocess
import sys
from pkg_resources import get_distribution


__version__ = get_distribution('techela').version

parser = argparse.ArgumentParser(description='Open techela.')
parser.add_argument('course_id', help='The course id')
parser.add_argument('--debug', help='Print debug info', action='store_true')

args = parser.parse_args()

COURSE = args.course_id
COURSEDIR = os.path.expanduser(f'~/.techela/{COURSE}')
COURSEREPO = f'https://github.com/jkitchin/{COURSE}'

if args.debug:
    print(COURSEDIR)
    sys.exit()

if not os.path.isdir(COURSEDIR):
    # We have not cloned before and need to.
    cpe = subprocess.run(['git',
                          'clone',
                          COURSEREPO,
                          COURSEDIR],
                         check=True,
                         stdout=subprocess.PIPE)
