# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright (C) 2005-2009 Lars-Peter Voss <bitmonster@eventghost.org>
#
# EventGhost is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License version 2 as published by the
# Free Software Foundation;
#
# EventGhost is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# this import is needed first, because it applies
# patches to wx.lib.filebrowsebutton
import FileBrowseButton
from wx.lib.filebrowsebutton import DirBrowseButton as _DirBrowseButton


class DirBrowseButton(_DirBrowseButton):
    """
    A control to allow the user to type in a filename or browse with the
    standard file dialog to select a directory.
    """
    pass

