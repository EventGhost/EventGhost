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

import sys
import os
sys.path.append(os.getcwdu())

if len(sys.argv) > 1:
    mainFilePath = os.path.abspath(sys.argv[1].encode('mbcs'))
    sys.argv = sys.argv[1:]
    sys.argv[0] = mainFilePath
    import imp
    imp.load_source("__main__", mainFilePath)
else:
    if getattr(sys, "frozen", None) == "console_exe":
        from code import InteractiveConsole
        InteractiveConsole().interact()

