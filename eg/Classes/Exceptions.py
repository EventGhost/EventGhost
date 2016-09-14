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

# Local imports
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
    PluginNotFound = "Plugin start error!"
    PluginLoadError = "Plugin load error!"


class ProgramError(eg.Exception):
    source = "unknown"

    def __init__(self, *args):
        self.args = args

    def __unicode__(self):
        res = [self.text] + [unicode(arg) for arg in self.args]
        return "\n".join(res)


class Exceptions:
    class DeviceInitFailed(ProgramError):
        text = Text.DeviceInitFailed

    class DeviceNotFound(ProgramError):
        text = Text.DeviceNotFound

    class DeviceNotReady(ProgramError):
        text = Text.DeviceNotReady

    class DriverNotFound(ProgramError):
        text = Text.DriverNotFound

    class DriverNotOpen(ProgramError):
        text = Text.DriverNotOpen

    class InitFailed(ProgramError):
        text = Text.InitFailed

    class PluginLoadError(ProgramError):
        text = Text.PluginLoadError

    class PluginNotFound(ProgramError):
        text = Text.PluginNotFound

    class ProgramNotFound(ProgramError):
        text = Text.ProgramNotFound

    class ProgramNotRunning(ProgramError):
        text = Text.ProgramNotRunning

    class SerialOpenFailed(ProgramError):
        text = Text.SerialOpenFailed
