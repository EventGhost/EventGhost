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

import eg
import wx
import math


class SpinIntCtrl(eg.SpinNumCtrl):
    """
    A wx.Control that shows a integer value and spin buttons to let
    the easily input an integer value.
    """

    def __init__(
        self,
        parent,
        id=-1,
        value=0,
        min=0,
        max=None,
        size=(-1,-1),
        style=0
    ):
        allowNegative = bool(min < 0)
        if max is None:
            integerWidth = 5
        else:
            integerWidth = int(math.ceil(math.log10(max + 1)))

        eg.SpinNumCtrl.__init__(
            self,
            parent,
            id,
            value,
            min=min,
            max=max,
            size=size,
            allowNegative=allowNegative,
            groupDigits = False,
            fractionWidth=0,
            integerWidth=integerWidth
        )

