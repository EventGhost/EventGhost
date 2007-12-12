# This file is part of EventGhost.
# Copyright (C) 2005 Lars-Peter Voss <bitmonster@eventghost.org>
# 
# EventGhost is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# EventGhost is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# $LastChangedDate: 2007-10-05 02:25:25 +0200 (Fri, 05 Oct 2007) $
# $LastChangedRevision: 242 $
# $LastChangedBy: bitmonster $


class Text(eg.TranslatableStrings):
    DriverNotFound = "Driver not found!"
    DriverNotOpen = "Could not open driver!"
    DeviceNotFound = "Device not found!"
    ProgramNotRunning = "Application is not running!"
    ProgramNotFound = "Application not found!"
    InitFailed = "Initialization failed!"
    DeviceInitFailed = "Unable to initalize device!"
    DeviceNotReady = "Device is not ready!"
    SerialOpenFailed = "Can't open serial port!"
    
    
class Exception(eg.Exception):
    source = "unknow"
    
    def __init__(self, *args):
        self.args = args
        
    def __unicode__(self):
        res = [self.text] + [unicode(arg) for arg in self.args]
        return "\n".join(res)
    
    
    
class Exceptions:
    
    class DriverNotFound(Exception):
        text = Text.DriverNotFound
    
    
    class DriverNotOpen(Exception):
        text = Text.DriverNotOpen
    
    
    class InitFailed(Exception):
        text = Text.InitFailed
    
    
    class DeviceInitFailed(Exception):
        text = Text.DeviceInitFailed
    
    
    class DeviceNotFound(Exception):
        text = Text.DeviceNotFound
    

    class DeviceNotReady(Exception):
        text = Text.DeviceNotReady
    

    class ProgramNotRunning(Exception):
        text = Text.ProgramNotRunning
    

    class ProgramNotFound(Exception):
        text = Text.ProgramNotFound
    

    class SerialOpenFailed(Exception):
        text = Text.SerialOpenFailed
    

