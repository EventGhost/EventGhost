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


def read_file(file_name):
    import os

    base_path = os.path.dirname(__file__)

    try:
        path = os.path.join(base_path, file_name)

        with open(path, 'r') as f:
            return f.read()
    except IOError:
        return ''


__version__ = '0.1.0'
__author__ = 'Kevin Schlosser'
__url__ = 'https://github.com/kdschlosser/pyWinMCERemote'
__description__ = 'An impossibly simple Python binding to the Windows Ehome CIR Remote API'
__author_email__ = 'kevin.g.schlosser@gmail.com'
__long_description__ = read_file('README.md')
__license__ = read_file('LICENSE')

