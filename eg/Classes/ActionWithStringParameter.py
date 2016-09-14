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

import wx

# Local imports
import eg

class ActionWithStringParameter(eg.ActionBase):
    """
    Simple action class, that only has a single string parameter.
    """
    #: Set parameterDescription to a descriptive string of the one and only
    #: parameter this action has.
    parameterDescription = None
    defaultParameter = ""

    def Configure(self, parameter=None):
        """
        Simple configuration dialog with a single TextCtrl to edit the
        the string parameter of this action.
        """
        if parameter is None:
            parameter = self.defaultParameter
        panel = eg.ConfigPanel(resizable=True)

        parameterDescription = None
        if self.parameterDescription:
            parameterDescription = self.parameterDescription
        elif (
            hasattr(self, "text") and
            hasattr(self.text, "parameterDescription")
        ):
            parameterDescription = self.text.parameterDescription

        if parameterDescription:
            labelCtrl = panel.StaticText(parameterDescription)
            panel.sizer.Add(labelCtrl, 0, wx.EXPAND)
            panel.sizer.Add((5, 5))
        parameterCtrl = panel.TextCtrl(parameter)
        panel.sizer.Add(parameterCtrl, 0, wx.EXPAND)
        parameterCtrl.SetFocus()
        wx.CallAfter(parameterCtrl.SetInsertionPointEnd)

        while panel.Affirmed():
            panel.SetResult(parameterCtrl.GetValue())
