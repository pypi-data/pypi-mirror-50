"""Truncate file given as argument by one character."""

from __future__ import print_function
import sys

with open(sys.argv[1]) as f:
    print(f.read()[:-1], end='')
