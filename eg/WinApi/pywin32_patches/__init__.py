# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
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

# Patches to fix pieces of pywin32 220 that do not function properly.

import win32com
import sys

import win32com_client_dynamic
import dde

# patch for > 219
win32com.client.dynamic._GetDescInvokeType = (
    win32com_client_dynamic.GetDescInvokeType
)
sys.modules['win32com'] = win32com

# patch for > 214
sys.modules['dde'] = dde



