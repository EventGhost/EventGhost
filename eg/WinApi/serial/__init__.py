#!/usr/bin/env python
#portable serial port access with python
#this is a wrapper module for different platform implementations
#
# (C)2001-2002 Chris Liechti <cliechti@gmx.net>
# this is distributed under a free software license, see license.txt

import sys, os, string
VERSION = string.split("$Revision$")[1]     #extract CVS version

from serialwin32 import *

