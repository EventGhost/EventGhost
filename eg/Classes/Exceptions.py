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


class Text(eg.TranslatableStrings):
    DriverNotFound = "Driver not found!"
    DriverNotOpen = "Could not open driver!"
    DeviceNotFound = "Device not found!"
    ProgramNotRunning = "Application is not running!"
    ProgramNotFound = "Application not found!"
    InitFailed = "Initialisation failed!"
    DeviceInitFailed = "Unable to initialise device!"
    DeviceNotReady = "Device is not ready!"
    SerialOpenFailed = "Can't open serial port!"
    PluginNotFound = "Plugin not found!"
    PluginLoadError = "Plugin load error!"


class ProgramError(eg.Exception):
    source = "unknown"

    def __init__(self, *args):
        self.args = args

    def __unicode__(self):
        res = [self.text] + [unicode(arg) for arg in self.args]
        return "\n".join(res)



class Exceptions:

    class DriverNotFound(ProgramError):
        text = Text.DriverNotFound


    class DriverNotOpen(ProgramError):
        text = Text.DriverNotOpen


    class InitFailed(ProgramError):
        text = Text.InitFailed


    class DeviceInitFailed(ProgramError):
        text = Text.DeviceInitFailed


    class DeviceNotFound(ProgramError):
        text = Text.DeviceNotFound


    class DeviceNotReady(ProgramError):
        text = Text.DeviceNotReady


    class ProgramNotRunning(ProgramError):
        text = Text.ProgramNotRunning


    class ProgramNotFound(ProgramError):
        text = Text.ProgramNotFound


    class SerialOpenFailed(ProgramError):
        text = Text.SerialOpenFailed


    class PluginNotFound(ProgramError):
        text = Text.PluginNotFound


    class PluginLoadError(ProgramError):
        text = Text.PluginLoadError

