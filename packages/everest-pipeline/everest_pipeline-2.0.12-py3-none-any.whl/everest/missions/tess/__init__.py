#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:py:mod:`__init__.py` - Initialization
--------------------------------------

'''

from __future__ import division, print_function, absolute_import, unicode_literals
from .tess import *

#: The string that identifies individual targets for this mission
IDSTRING = 'TIC'
#: The character abbreviation of the name given to an observing "season" for this mission
SEASONCHAR = 'S'
#: The string representing the filter/band used in the mission 
MAGSTRING = r'T'
#: The time units for the mission
TIMEUNITS = 'BJD'
#: The currently supported seasons
SEASONS = []
#: Returns :py:obj:`True` if argument is a valid `TESS` target identifier (necessary but not sufficient)
ISTARGET = lambda x: ((type(x) is int))
#: The published light curve CSV file header
CSVHEADER = \
'''TIC %07d
============

'''