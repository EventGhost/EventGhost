# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.net/>
#
# EventGhost is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 2 of the License, or (at your option)
# any later version.
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with EventGhost. If not, see <http://www.gnu.org/licenses/>.

import logging
import sys
from os.path import join

class StdHandler(object):
    indent = 0

    def __init__(self, oldStream, logger):
        self.oldStream = oldStream
        self.encoding = oldStream.encoding
        self.buf = ""
        self.logger = logger

        # the following is a workaround for colorama (0.3.6),
        # which is called by sphinx (build CHM docs).
        self.closed = False

    def write(self, data):
        try:
            self.buf += data
        except UnicodeError:
            self.buf += data.decode('mbcs')
        lines = self.buf.split("\n")
        for line in self.buf.split("\n")[:-1]:
            line = (self.indent * 4 * " ") + line.rstrip()
            self.logger(line)
            self.oldStream.write(line + "\n")
        self.buf = lines[-1]


    def flush(self):
        pass


    def isatty(self):
        return True



def LogToFile(file):
    logging.basicConfig(filename=file, level=logging.DEBUG,)
    logging.getLogger().setLevel(20)
    sys.stdout = StdHandler(sys.stdout, logging.info)
    sys.stderr = StdHandler(sys.stderr, logging.error)


def SetIndent(level):
    StdHandler.indent = level

