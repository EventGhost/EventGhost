# This file is a plugin for EventGhost.
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

eg.RegisterPlugin(
    name = "AsteriskAMI",
    author = "TheOgre",
    version = "0.2.0",
    kind = "other",
    description = "Receives events from Asterisk AMI interface",
    guid='{FEC0A1F1-50EE-4E4C-A2EA-290831283521}' ,
    url="http://www.eventghost.net/forum/viewtopic.php?t=3492"    
)

import time
import threading
import telnetlib

class Text:
    hostname = "Hostname or IP:"
    port = "TCP/IP Port:"
    timeout = "Time Out:"
    username = "Username:"
    password = "Password:"
    eventPrefix = "Event Prefix:"
    eventFilter = "Exclude Events:"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    eventGenerationBox = "Event generation"    

class TelnetReader(threading.Thread):
    
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):

        threading.Thread.__init__(self, group=group, target=target, 
            name=name, verbose=verbose)
            
        self.args = args
        self.settings = kwargs
        self.stopEvent = kwargs['stopEvent']
        return
        
    def run(self):
        packet = ""
        self.telnet = None
        while not self.stopEvent.isSet():
            
            if self.telnet == None:
                self.telnet = self.connect()

            strPacket = ""
            
            try:
                strPacket = self.telnet.read_until('\r\n\r\n',self.settings['timeout'])
                
                if strPacket!="":
                    lines = strPacket.rstrip().split('\r\n')
                    packet = self.parsePacket(lines)
                    
                    eventName = ""
                    
                    if 'Event' in packet:
                        eventName = packet['Event']
                    elif 'Message' in packet:
                        eventName = packet['Message']
                    else:
                        eventName = lines[0]
                        
                    if eventName not in self.settings['eventFilter']:
                        self.settings['plugin'].TriggerEvent(eventName, payload = packet)

                    
            except:
                print "Error Parsing Packet"
                self.telnet = None            
            
        return

           
    def connect(self):
        print "Connecting to " + self.settings['hostname'] + ":" + str(self.settings['port']) + " (timeout = " + str(self.settings['timeout']) +")"
        tn= None
        
        try:
            
            tn = telnetlib.Telnet(self.settings['hostname'],self.settings['port'], self.settings['timeout'])
            tn.read_until('\n',self.settings['timeout']).rstrip()
            p = "Action: Login\nUsername: " + self.settings['username'] + "\nSecret: " + self.settings['password'] + "\n\n"
            tn.write(str(p))
        except:
            self.settings['plugin'].PrintError("Error Connecting")
            tn = None
           
        return tn
        
    def parsePacket(self, lines):
    
        packet = dict()
        
        for line in lines:
            if line.count(':') == 1 and line[-1] == ':': 
                key, val = line[:-1], ''
            elif line.count(',') == 1 and line[0] == ' ': 
                key, val = line[1:].split(',', 1)
            else:
                key, val = line.split(': ', 1)            
        
            packet[key]=val
            
        return packet
            
class AsteriskAMI(eg.PluginBase):
    
    text = Text
    
    def __start__(self, hostname, port, timeout, username, password, eventPrefix, eventFilterText):
        
        self.stopEvent=threading.Event()
                
        settings = {
            'plugin':self,
            'stopEvent':self.stopEvent,
            'hostname':hostname,
            'port':port,
            'timeout':timeout,
            'username':username,
            'password':password,
            'eventPrefix':eventPrefix,
            'eventFilter':eventFilterText.split(',')
        }
        
        thread = TelnetReader(kwargs=settings)
        thread.start()
        


    def __stop__(self):
        self.stopEvent.set()
        return

    def Configure(self, hostname="localhost", port=5038, timeout=2, username="eg", password="eg", eventPrefix="AMI", eventFilter="AGIExec" ):
        text = self.text
        panel = eg.ConfigPanel()
        
        hostnameControl = panel.TextCtrl(hostname)
        hostnameText = panel.StaticText(text.hostname)

        portControl = panel.SpinIntCtrl(port, max=65535)
        portText = panel.StaticText(text.port)

        timeoutControl = panel.SpinIntCtrl(timeout, max=10)
        timeoutText = panel.StaticText(text.timeout)

        usernameControl = panel.TextCtrl(username)
        usernameText = panel.StaticText(text.username)

        passwordControl = panel.TextCtrl(password, style=wx.TE_PASSWORD)
        passwordText = panel.StaticText(text.password)
        
        prefixControl = panel.TextCtrl(eventPrefix)
        prefixText = panel.StaticText(text.eventPrefix)

        filterControl = panel.TextCtrl(eventFilter)
        filterText = panel.StaticText(text.eventFilter)
        
        eg.EqualizeWidths((hostnameText, portText, timeoutText, usernameText, passwordText, prefixText, filterText))
        
        box1 = panel.BoxedGroup(text.tcpBox, (hostnameText,hostnameControl),(portText,portControl),(timeoutText,timeoutControl))
        box2 = panel.BoxedGroup(text.securityBox, (usernameText, usernameControl),(passwordText,passwordControl))
        box3 = panel.BoxedGroup(text.eventGenerationBox,(prefixText,prefixControl),(filterText,filterControl))
        
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND|wx.TOP, 10),
            (box3, 0, wx.EXPAND|wx.TOP, 10),
        ])
        
        while panel.Affirmed():
            panel.SetResult(
                hostnameControl.GetValue(),
                portControl.GetValue(),
                timeoutControl.GetValue(),
                usernameControl.GetValue(),
                passwordControl.GetValue(),
                prefixControl.GetValue(),
                filterControl.GetValue()
            )