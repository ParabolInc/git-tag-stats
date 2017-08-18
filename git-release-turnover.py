#!/usr/bin/env python3
"""
Emit CSV file for LoC turned over in GitHub repository between all tags
"""
from argparse import ArgumentParser
import logging
import os
import sys

from grt import main

__author__ = 'Jordan Husney'
__version__ = '0.1'

epilog = 'system (default) encoding: {}'.format(sys.getdefaultencoding())
parser = ArgumentParser(
    usage='%(prog)s [options] [FILE ...]',
    description=__doc__, epilog=epilog,
    prog=os.path.basename(sys.argv[0])
)

parser.add_argument('-o', '--output',
                    help='name of CSV file to output')
parser.add_argument('--repo',
                    help='directory containing repository to analyze')
parser.add_argument('--version', action='version', version=__version__)
args = parser.parse_args()

try:
    main(args.repo, args.output)
except:
    logging.exception("unexpected program error")
