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

"""
    eg.Tasklet
    ~~~~~~~~~~

    A wrapper around stackless.tasklet

    :copyright: 2009 by EventGhost team, see AUTHORS.txt for more details.
    :license: GNU GPL v2, see LICENSE.txt for more details.
"""

import stackless


class Tasklet(stackless.tasklet):
    countTasklets = 0

    def __init__(self, func):
        stackless.tasklet.__init__(self)
        self.bind(func)
        Tasklet.countTasklets += 1
        self.taskId = Tasklet.countTasklets


    @classmethod
    def GetCurrentId(cls):
        try:
            return stackless.getcurrent().taskId
        except AttributeError:
            return 0

