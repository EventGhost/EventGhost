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

class SerialPortChoice(wx.Choice):
    """
    A wx.Choice control that shows all available serial ports on the system.
    """
    def __init__(
        self,
        parent,
        id=-1,
        pos=wx.DefaultPosition,
        size=wx.DefaultSize,
        style=0,
        validator=wx.DefaultValidator,
        name=wx.ChoiceNameStr,
        value=None
    ):
        """
        :Parameters:
            `value` : int
                The initial port to select (0 = COM1:). The first available
                port will be selected if the given port does not exist or
                no value is given.
        """
        ports = eg.SerialThread.GetAllPorts()
        self.ports = ports
        choices = [("COM%d" % (portnum + 1)) for portnum in ports]
        wx.Choice.__init__(
            self, parent, id, pos, size, choices, style, validator, name
        )
        try:
            portPos = ports.index(value)
        except ValueError:
            portPos = 0
        self.SetSelection(portPos)

    def GetValue(self):
        """
        Return the currently selected serial port.

        :rtype: int
        :returns: The serial port as an integer (0 = COM1:)
        """
        try:
            port = self.ports[self.GetSelection()]
        except:
            port = 0
        return port
