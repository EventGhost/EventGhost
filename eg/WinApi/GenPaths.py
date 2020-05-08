# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2020 EventGhost Project <http://www.eventghost.net/>
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


import os
import sys
import comtypes.client
import win32com.client
import pythoncom
import eg

# Patch win32com and comtypes to use the gen_py directory in the programs
# application data directory instead of its package directory.
# When the program runs "frozen" it would not be able to modify
# the package directory
win32com_gen_path = (
    os.path.join(eg.configDir, "win32com_gen_py").encode('mbcs')
)
if not os.path.exists(win32com_gen_path):
    os.makedirs(win32com_gen_path)

win32com.__gen_path__ = win32com_gen_path
sys.modules["win32com.gen_py"].__path__ = [win32com_gen_path]
win32com.client.gencache.is_readonly = False


comtypes_gen_path = (
    os.path.join(eg.configDir, "comtypes_gen_py").encode('mbcs')
)
if not os.path.exists(comtypes_gen_path):
    os.makedirs(comtypes_gen_path)

comtypes.client.gen_dir = comtypes_gen_path
sys.modules['comtypes.gen'].__path__ = [comtypes_gen_path]


# Flag for puythoncom to know this is not an installed
# python but instead it is a packaged version
if hasattr(sys, "frozen"):
    pythoncom.frozen = 1

sys.coinit_flags = 2
