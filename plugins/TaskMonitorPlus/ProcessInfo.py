# -*- coding: utf-8 -*-
#
# This file is a plugin for EventGhost.
# Copyright © 2005-2016 EventGhost Project <http://www.eventghost.org/>
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

from os.path import splitext
from eg.WinApi.Utils import GetProcessName

class ProcessInfo(object):
    """
    Class representing an individual process, and keeping a list of
    its open windows.
    """
    def __init__(self, pid):
        self.pid = pid
        self.name = splitext(GetProcessName(pid))[0]
        self.hwnds = dict()     # key=hwnd, val=WindowInfo(hwnd)

    def __str__(self):
        return self.name
        # return self.name+"."+str(self.pid)

    def __add__(self, other):
        # Allow string concatenation without extra syntax
        if isinstance(other, basestring):
            return str(self)+other
        # Intentionally raise TypeError
        return self+other

    def __radd__(self, other):
        # Allow string concatenation without extra syntax
        if isinstance(other, basestring):
            return other+str(self)
        # Intentionally raise TypeError
        return self+other

#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf-8
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf-8:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf-8:
