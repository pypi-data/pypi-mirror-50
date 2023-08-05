"""Reverse file content given as argument."""

from __future__ import print_function
import sys

with open(sys.argv[1]) as f:
    print(f.read()[::-1], end='')
