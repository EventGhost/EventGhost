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
# $LastChangedDate$
# $LastChangedRevision$
# $LastChangedBy$


eg.RegisterPlugin(
    name = "d-box2 Remote Emulator",
    author = "Bitmonster",
    version = "1.0." + "$LastChangedRevision$".split()[1],
    kind = "external",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    description = "Control your d-box2 set-top box over Ethernet.",
    help = "<i>(Linux/Neutrino must be installed on the box)</i>",
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACmklEQVR42o2TS0hVYRDH"
        "/3O+c859dX1mvhOzSw+kByZW1ibICIQIxSBqYUUQLdpkoW0Meu3b3AiCFrWqMFoItTGL"
        "wo2UCUrY1V6o3Hx1Pffc1/d9jfQgUcEDM/Od+WZ+35z55hBWfIw8Vh2A3sj2Dks3r5dE"
        "0QrJLPo8qxt/YobYXGbbA6hVA9pNgWat9ZRUVMiONxx+btWAHZWq/UQjTmoL8/e74BuM"
        "EFeBYwzWqwCQqA3pzo5WHPDbmGkPY65/BOvZf5rl4/9VLAOgBV8TQftrq/Daa8N5NYSA"
        "BnWxf5j3F3oT/QtZDrCZ1bWFHjAqslAwBwXYd4aIjrANC8IzofR8YinAEJx4iWWWk8Ms"
        "llKQQZvjNGoNjeKMMiaIdFxpPRhXyCwChEqpiDefjE+j00ngOZ/uYUkyYJ0J7NMZiqVh"
        "zEihpTDUsJOE+w8wGEZNSuGsJ4Cj97oxcPsRrnNyn9QoXSMQMAkbVMqYTQJzOWu5LsLA"
        "eBSSkJ2XBTKDb69GT22p0ldMC6mxSVi3HuDp45e4mEqj2SCQT2DSVBRt2Iv81kZ90G/i"
        "5v42MULIK26CYde1HZqpaal3qnOCyg54tf2iD98uhM2eWZeKBemSXZXyS321jm7fZG4d"
        "jvrV5wnj7sMeo5dQUNYC8u72eUSsIidpVea6gVB+vOjDV1P0fgpOScN0SWuqK5+uLt9m"
        "lvYng2Ojo0iriBtEwmFAVmEZ7OBxCI9lJGMZ7q6CFRAQhhfEcwhtQqZ8kE6IdtoJUYEJ"
        "FUn61btULqQcIvizAX/BYR6+BuiUBTIkrzMw+H8g/nqtJDJuDJmEy8D3sOR3TkwjlZ6H"
        "IOf3LRSESnjE9/BJaU6KQ0mHR4LnhOLQ0uWIBFfE7/onfnxeNDm/ADdeEckvKwEjAAAA"
        "AElFTkSuQmCC"
    ),
)


ACTIONS = (
    ("Left", "Left", "KEY_LEFT"),
    ("Right", "Right", "KEY_RIGHT"),
    ("Up", "Up", "KEY_UP"),             
    ("Down", "Down", "KEY_DOWN"),
    ("Ok", "Ok", "KEY_OK"),            
    ("Mute", "Mute", "KEY_MUTE"),
    ("Power", "Power", "KEY_POWER"),           
    ("Red", "Red", "KEY_RED"),
    ("Green", "Green", "KEY_GREEN"),
    ("Yellow", "Yellow", "KEY_YELLOW"),         
    ("Blue", "Blue", "KEY_BLUE"),           
    ("VolumeUp", "Volume Up", "KEY_VOLUMEUP"),
    ("VolumeDown", "Volume Down", "KEY_VOLUMEDOWN"),     
    ("Help", "Help", "KEY_HELP"),
    ("Setup", "Setup", "KEY_SETUP"),           
    ("TopLeft", "Top Left", "KEY_TOPLEFT"),
    ("TopRight", "Top Right", "KEY_TOPRIGHT"),       
    ("BottomLeft", "Bottom Left", "KEY_BOTTOMLEFT"),
    ("BottomRight", "Bottom Right", "KEY_BOTTOMRIGHT"),     
    ("Home", "Home", "KEY_HOME"),
    ("PageDown", "Page Down", "KEY_PAGEDOWN"),       
    ("PageUp", "Page Up", "KEY_PAGEUP"),
    ("Num0", "Number 0", "KEY_0"),               
    ("Num1", "Number 1", "KEY_1"),
    ("Num2", "Number 2", "KEY_2"),               
    ("Num3", "Number 3", "KEY_3"),
    ("Num4", "Number 4", "KEY_4"),               
    ("Num5", "Number 5", "KEY_5"),
    ("Num6", "Number 6", "KEY_6"),               
    ("Num7", "Number 7", "KEY_7"),
    ("Num8", "Number 8", "KEY_8"),               
    ("Num9", "Number 9", "KEY_9"),
)

TIMEOUT = 1.5

# stolen from the standard library and added a timeout to the socket
import socket
from httplib import HTTPConnection

class MyHTTPConnection(HTTPConnection):
    
    def connect(self):
        """Connect to the host and port specified in __init__."""
        msg = "getaddrinfo returns an empty list"
        for res in socket.getaddrinfo(self.host, self.port, 0,
                                      socket.SOCK_STREAM):
            af, socktype, proto, canonname, sa = res
            try:
                self.sock = socket.socket(af, socktype, proto)
                self.sock.settimeout(TIMEOUT)
                if self.debuglevel > 0:
                    print "connect: (%s, %s)" % (self.host, self.port)
                self.sock.connect(sa)
            except socket.error, msg:
                if self.debuglevel > 0:
                    print 'connect fail:', (self.host, self.port)
                if self.sock:
                    self.sock.close()
                self.sock = None
                continue
            break
        if not self.sock:
            raise socket.error(msg)



class ActionPrototype(eg.ActionClass):
    
    def __call__(self):
        conn = MyHTTPConnection(self.plugin.host)
        try:
            conn.request("GET", self.plugin.connectString % self.value)
        except socket.error, e:
            if isinstance(e.message, socket.timeout):
                raise self.Exceptions.DeviceNotFound
            raise
        conn.getresponse()
        conn.close()
        
        

class DBox2(eg.PluginClass):
    
    def __init__(self):
        self.AddActionsFromList(ACTIONS, ActionPrototype)
        
        
    def __start__(self, host, useRcem=False):
        self.host = host
        if useRcem:
            self.connectString = "/control/rcem?%s"
        else:
            self.connectString = "/control/exec?Y_Tools&rcsim&%s"
            
        
        
    def Configure(self, host="127.0.0.1", useRcem=True):
        panel = eg.ConfigPanel(self)
        hostCtrl = panel.TextCtrl(host)
        useRcemCtrl = panel.CheckBox(useRcem, 'Use "rcem" instead of "rcsim"')
        panel.AddLine("d-box2 Host:", hostCtrl)
        panel.AddLine(useRcemCtrl)        
        while panel.Affirmed():
            panel.SetResult(hostCtrl.GetValue(), useRcemCtrl.GetValue())
    
        
