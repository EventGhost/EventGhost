# -*- coding: utf-8 -*-
#
# This file is part of EventGhost.
# Copyright © 2005-2019 EventGhost Project <http://www.eventghost.org/>
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

"""
This file is part of the **pyWinMCERemote**
project https://github.com/kdschlosser/pyWinMCERemote

:platform: Windows
:license: GPL version 2 or newer
:synopsis: library entry point

.. moduleauthor:: Kevin Schlosser @kdschlosser <kevin.g.schlosser@gmail.com>
"""

import ioctl
import version

get_ir_devices = ioctl.get_ir_devices
load_device_data = ioctl.load_device_data

__version__ = version.__version__
__author__ = version.__author__
__url__ = version.__url__
__description__ = version.__description__
__author_email__ = version.__author_email__
__license__ = version.__license__
__long_description__ = version.__long_description__

__doc__ += '\n ' + __long_description__

