"""
Contains common test fixtures to run Amazon DynamoDB tests
"""

import sys

sys.path.append('../..')

from test_tools.fixtures.common import *

from os.path import dirname as d
from os.path import abspath, join

root_dir = d(d(abspath(__file__)))
sys.path.append(root_dir)

