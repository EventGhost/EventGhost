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


class ProgramError(eg.Exception):
    source = "unknown"

    def __init__(self, *args):
        self.text = getattr(eg.text.Exceptions, self.__class__.__name__)
        self.args = args

    def __unicode__(self):
        res = [self.text] + [unicode(arg) for arg in self.args]
        return "\n".join(res)


class Exceptions:
    class DeviceInitFailed(ProgramError):
        pass

    class DeviceNotFound(ProgramError):
        pass

    class DeviceNotReady(ProgramError):
        pass

    class DriverNotFound(ProgramError):
        pass

    class DriverNotOpen(ProgramError):
        pass

    class InitFailed(ProgramError):
        pass

    class PluginLoadError(ProgramError):
        pass

    class PluginNotFound(ProgramError):
        pass

    class ProgramNotFound(ProgramError):
        pass

    class ProgramNotRunning(ProgramError):
        pass

    class SerialOpenFailed(ProgramError):
        pass
