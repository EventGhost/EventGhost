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
# $LastChangedDate: 2013-Dec-07 $
# $LastChangedRevision: 003 $
# $LastChangedBy: rdgerken $

'''<rst>

**Envisalink Vista TPI Plugin**

`Envisalink <http://www.eyezon.com/?page_id=176>`_ is a internet gateway for Honeywell Vista / ADEMCO security panels.


*Option/Setup*

Enter the TCP/IP address and the listening port of your Envisalink Gateway.  The 
default listening port is 4025.  The default password is \'user\'.

'''

import eg

eg.RegisterPlugin(
    name = 'Envisalink Vista TPI',
    guid='{3579F279-72C6-4A2C-BAE0-77949823B063}',
    description = __doc__,
    author = 'rdgerken',
    version = '1.0.' + '$LastChangedRevision: 002 $'.split()[1],
    kind = 'external',
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
'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'
'YAAAOpgAABdvkl/FRgAABGBJREFUeAEAEgDt/wD///8AOzs7sQH///8Atra2/wAAAP//ABIA7f8B'
'1tbWAAcHBwACCgoK/wEBAY4AAAD//wAiAN3/Af///wDJycm5wcHBRxwcHAACAAAAAMPDw0agoKD/'
'BAQEpgAAAP//AEQAu/8Dzs7OAAoKCi9mZmbpsLCwAAIMDAwABgYG0SgoKLAAAAAABNPT0zfi4uLI'
'Ojo6AP///wACISEhye/v7wAtLS0AAAAAAAAAAP//AIQAe/8B////AN7e3gDs7OwxJycnouHh4Tz9'
'/f3w+fn5ATg4OAACAAAAAAcHBwDT09OAa2trLLKysvAxMTEAAQEBAAAAAAAEAAAAANLS0pnj4+NO'
'YGBgAERERABAQEAANzc3/zc3NwEA////AN3d3QDj4+MAlpaW//Pz8//U1NS14uLiAP///wAACAH3'
'/gD///8Azs7OAMfHxwA/Pz+ma2trRfDw8ADe3t4A////AAH///8A4+PjANHR0f8VFRUfFRUVjNzc'
'3LcNDQ2fOTk5AAIAAAAA+vr6AP39/QDHx8fi1tbWVgYGBp7r6+sAAAAAAAQAAAAACgoKAMXFxQD6'
'+vr/Ozs7AAAAAO4aGhoAAAAAAAIAAAAA6OjotLS0tAAsLCwAYmJiAOLi4hL7+/sDAAAAAAD///8A'
'/////wAAAP/9/f3/1NTU/2FhYf+JiYlz////AAD///8At7e3Y1ZWVv9ISEj/AAAA/7Kysv/AwMAX'
'////AAIAAAAAKioqnUxMTIx2dnYA////AP///wsaGhrpAAAAAAAIAvf9Af///wAAAAAA0tLSAP//'
'/wAODg4AxcXFYuvr651DQ0MA////ANnZ2QABAQGZNTU1aAQEBAD9/f0AHx8fAAAAAAAB////AAAA'
'AADKysoABAQEAOrq6owSEhJz3d3dGP///+kFBQUAKCgoAP////jj4+PgysrKKAsLCwB2dnYAAAAA'
'AAQAAAAAAAAAABwcHAAHBwcAAQEBLMnJyQDW1tZ6HR0dWywsLATy8vKg6+vr0AgICDNhYWEADAwM'
'AAAAAAAAAAAAAP///wD///8AwMDAAK+vrzbGxsb/jY2N/0hISP8QEBD/AAAA/wAAAP+Ghob/////'
'/9vb2znQ0NAA////AP///wAA////AP///wC2traK/////5GRkf8AAAD/tra2////////////zs7O'
'/zc3N/9oaGj/qKio67e3t1b///8A////AAIAAAAAAAAAAPn5+dTGxsbbBwcHAAAAAACOjo4A2tra'
'AAAAAACCgoIAycnJAPr6+gDg4OAR4uLiGAAAAAAAAAAAAf///wAAAAAA4eHhAAUFBQDFxcW0vLy8'
'S/b29gABAQEA5OTkADExMQCNjY0A0dHR8ff39xcSEhL5JiYmAAAAAAAB////AAAAAADd3d0AAwMD'
'APv7+wDV1dUA4uLiUiYmJkEiIiIB1dXVzNnZ2aMuLi79Li4uAPPz8wApKSkAAAAAAAEAAP//zJLX'
'qMGRIWgAAAAASUVORK5CYII='
)
)

import wx
import asynchat
import socket
import asyncore
import threading
import re
from types import ClassType
                
class Text:
    tcpBox = 'TCP/IP Settings'
    hostLabel = 'Host:'
    portLabel = 'Port:'
    userLabel = 'Password:'
    passLabel = 'Keypad Code:'
      
class EnvisalinkSession(asynchat.async_chat):
    '''
    Handles an Envisalink TCP/IP session.
    '''
     
    def __init__ (self, plugin, address):
        self.plugin = plugin
        self.data = ''

        # Call constructor of the parent class
        asynchat.async_chat.__init__(self)

        # Set up input line terminator
        self.set_terminator('\r\n')
        
        # create and connect a socket
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        eg.RestartAsyncore()
        self.settimeout(2.0)
        try:
            self.connect(address)
        except:
            pass

    def handle_connect(self):
        '''
        Called when the active opener's socket actually makes a connection. 
        '''
        self.plugin.TriggerEvent('Connected')

    def handle_expt(self):
        # connection failed
        self.plugin.isSessionRunning = False
        self.plugin.isAuthenticated = False
        self.set_terminator('\r\n')
        self.plugin.TriggerEvent('NoConnection')
        self.close()

    def handle_close(self):
        '''
        Called when the channel is closed.
        '''
        self.plugin.isSessionRunning = False
        self.plugin.isAuthenticated = False
        self.set_terminator('\r\n')
        self.plugin.TriggerEvent('ConnectionLost')
        self.close()

    def collect_incoming_data(self, data):
        '''
        Called with data holding an arbitrary amount of received data.
        '''
        self.data = self.data + data

    def found_terminator(self):
        '''
        Called when the incoming data stream matches the termination 
        condition set by set_terminator.
        '''
        if self.plugin.debug:  
           print 'Envisalink> ' + self.data
        data = re.sub('([^0-9a-zA-Z:\,\.\~\#\>])', '', self.data)
        self.data=''
        arguments = data.rsplit(',')
        command = arguments[0]

        try:   
            if command.upper() == 'LOGIN:':
               print 'Envisalink> Sending Login Password'
               self.plugin.DoCommand( self.plugin.envisalinkuser )
            if not self.plugin.isAuthenticated:
               if command.upper() == 'OK':
                  self.plugin.isAuthenticated = True
                  self.set_terminator('$')
                  self.plugin.TriggerEvent('Authenticated')   

            #Virtual Keypad Update           
            if ( command.upper() == '00' ):
               partition   = arguments[1]
               icons = arguments[2]
               numeric = arguments[3]
               beeps = arguments[4]
               string = arguments[5]
               #Only send new event if there is an update - ignore high frequency duplicate updates from Envisalink TPI
               if (self.plugin.lastupdatevalue != 'VirtualKeypad.Partition' + partition + '.' + string ):
                   self.plugin.lastupdatevalue = 'VirtualKeypad.Partition' + partition + '.' + string
                   self.plugin.TriggerEvent(self.plugin.lastupdatevalue)
               if self.plugin.debug:
                   print 'Envisalink> Icons=' + icons + ' Numeric=' + numeric + ' Beeps=' + beeps + ' String=' + string 
               return

        except:
            print 'Envisalink> Unexpected Response: ' + data

class NvAction(eg.ActionBase):  
    def __call__(self):
        self.plugin.DoCommand(self.plugin.envisalinkpass + self.command)

class Envisalink(eg.PluginBase):        
    text = Text

    def __init__(self):
        self.host = 'localhost'
        self.port = 4025
        self.envisalinkuser = 'user'
        self.envisalinkpass = '0812'
        self.isSessionRunning = False
        self.isAuthenticated = False
        self.waitStr = None
        self.waitFlag = threading.Event()
        self.session = None
        self.debug = False

        group = self.AddGroup('Envisalink Virtual Keypad')
        className = 'ArmStay'
        clsAttributes = dict(name='Arm Stay', command = '3')
        cls = ClassType(className, (NvAction,), clsAttributes)
        group.AddAction(cls)

        className = 'ArmAway'
        clsAttributes = dict(name='Arm Away', command = '2')
        cls = ClassType(className, (NvAction,), clsAttributes)
        group.AddAction(cls)

        className = 'Off'
        clsAttributes = dict(name='Off', command = '1')
        cls = ClassType(className, (NvAction,), clsAttributes)
        group.AddAction(cls)

        self.AddAction(self.MyCommand)
        self.AddEvents()


    def __start__(
        self,
        host='192.168.32.4', 
        port=4025,
        envisalinkuser='user',
        envisalinkpass='0812',
        debug=False,
        lastupdatevalue=''
    ):
        self.host = host
        self.port = port
        self.envisalinkuser = envisalinkuser
        self.envisalinkpass = envisalinkpass
        self.debug = debug
        self.lastupdatevalue = lastupdatevalue
            
        if not self.isSessionRunning:
            self.session = EnvisalinkSession(self, (self.host, self.port))
            self.isSessionRunning = True
            if self.debug:
               print 'Envisalink> Session is Running' 

    def __stop__(self):
        if self.isSessionRunning:
            self.session.close()

    @eg.LogIt

    def DoCommand(self, cmdstr):
        self.waitFlag.clear()
        self.waitStr = cmdstr
        if not self.isSessionRunning:
            self.session = EnvisalinkSession(self, (self.host, self.port))
            self.isSessionRunning = True
            if self.debug:
               print 'Envisalink> Do Command Session is Running'
        try:
            if self.debug:
               print 'Envisalink> Trying: ' + cmdstr 
            if (not self.isAuthenticated and (cmdstr==self.envisalinkuser)) or self.isAuthenticated: 
               self.session.sendall(cmdstr + '\r\n')
            else:
               print 'Envisalink> Can\'t send command - ' + cmdstr + ' - Authenticate first!'
        except:
            self.isSessionRunning = False
            self.TriggerEvent('close')
            self.session.close()
        self.waitFlag.wait(2.0)
        self.waitStr = None
        self.waitFlag.set()

    def Configure(
        self,
        host='192.168.32.4',
        port=4025,
        envisalinkuser='user',
        envisalinkpass='0812',
        debug=False
    ):
        text = self.text
        panel = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)       
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        userCtrl = panel.TextCtrl(envisalinkuser)
        passCtrl = panel.TextCtrl(envisalinkpass)
        debugCtrl = panel.CheckBox(debug, '')
        
        tcpBox = panel.BoxedGroup(
            text.tcpBox,
            (text.hostLabel, hostCtrl),
            (text.portLabel, portCtrl),
            (text.userLabel, userCtrl),
            (text.passLabel, passCtrl),
            ('Debug', debugCtrl),
        )
        eg.EqualizeWidths(tcpBox.GetColumnItems(0))
        panel.sizer.Add(tcpBox, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(), 
                portCtrl.GetValue(), 
                userCtrl.GetValue(),
                passCtrl.GetValue(),
                debugCtrl.GetValue(),
            )

    class MyCommand(eg.ActionWithStringParameter):
        name = 'Raw Command'
        def __call__(self, value):
            value = eg.ParseString(value)  
            self.plugin.DoCommand(value)
