import eg
import socket
import re
import time
import sys
import wx
import urllib2
from xml.dom import minidom

eg.RegisterPlugin(
    name = "DenonTCPIP",
    guid='{DCFAC924-7CB5-4CBF-A5AA-118E2F035BA2}',
    author = "Mikael Arneborn",
    version = "0.2",
    kind = "other",
    canMultiLoad=True,
    description = "A Plugin to Control Denon/Marantz Receivers via TCP/IP"
)

class Volume:
    def __init__(self):
        self.value   = 50.0
        self.max     = 90.0
        self.min     = 0.0
        self.startedStep = None
        self.steps   = ((0,0.5),(0.5,1),(2,2),(3,4))
    def set (self, value):
        if (self.value > self.max):
            self.value = self.max
        elif (self.value < self.min):
            self.value = self.min
        else:  
            self.value = value
    def resetStep(self):
        self.startedStep = None
    def pickStep(self):
        if (self.startedStep is None):
            self.startedStep = time.clock()
            deltaT = 0
        else:
            deltaT = time.clock()-self.startedStep
        step = 0
        for (t,s) in self.steps:
            if (t > deltaT):
                break
            step = s
        return step

    def step(self,mult):
        self.set(self.value + mult*self.pickStep())
        
class DenonVolume(Volume):
    def toSend(self):
        s = "";
        if (self.value < 10):
            s = "0"
        s = s+str(int(self.value))
        if (int(s) != int(round(self.value+0.001,0))):
            s = s+"5"
        return s
    def set(self, value):
        if (type(value) == int or type(value) == float):
            Volume.set(self, value)
        elif (type(value) != str):
            pass
        elif (len(value) == 3):
            Volume.set(self, float(value)/10)
        elif (len(value) == 2):
            Volume.set(self, float(value))
        
class DenonTCPIP(eg.PluginBase):
    """ A plugin to control my Denon Receiver via TCP/IP """
    
    def __init__(self):
        self.host = "192.168.1.2"
        self.port = 23
        self.things = []
        self.connected = False
        self.volume = DenonVolume()
        self.volume.plugin = self
        self.mute = False
        self.muteZ2 = False
        self.state = False
        self.stateZ2 = False

        mainZone = self.AddGroup(
            "Zone 1",
            "Actions for Zone 1"
        )

        mainZoneInfo = mainZone.AddGroup(
            "Information Retrieval",
            "Zone 1 Information Retrieval"
        )
        mainZoneInfo.AddAction(GetMainZoneVolume)
        mainZoneInfo.AddAction(GetMainZoneSource)
        mainZoneInfo.AddAction(GetMainZoneState)
        mainZoneInfo.AddAction(GetMainZoneMute)

        mainZone.AddAction(ToggleMainZoneMute)
        mainZone.AddAction(ToggleMainZonePower)
        mainZone.AddAction(SetMainZonePowerOn)
        mainZone.AddAction(SetMainZonePowerOff)
        mainZone.AddAction(SetMainZoneSource)
        mainZone.AddAction(SetMainZoneAudioSource)
        mainZone.AddAction(SetMainZoneVolumeLevel)
        mainZone.AddAction(VolumeMainZoneUp)
        mainZone.AddAction(VolumeMainZoneDn)

        Zone2 = self.AddGroup(
            "Zone 2",
            "Actions for Zone 2"
        )

        Zone2Info = Zone2.AddGroup(
            "Information Retrieval",
            "Zone 2 Information Retrieval"
        )
        Zone2Info.AddAction(GetZone2State)
        Zone2Info.AddAction(GetZone2Mute)

        Zone2.AddAction(ToggleZone2Mute)
        Zone2.AddAction(ToggleZone2Power)
        Zone2.AddAction(SetZone2Source)
        Zone2.AddAction(SetZone2VolumeLevel)

        OSM = self.AddGroup(
            "On Screen Menu",
            "Actions for remote OSM button press'"
        )
        OSM.AddAction(osmUp)
        OSM.AddAction(osmDown)
        OSM.AddAction(osmLeft)
        OSM.AddAction(osmRight)
        OSM.AddAction(osmSelect)
        OSM.AddAction(osmOption)
        OSM.AddAction(osmInfo)
                
        self.AddAction(GenericSend)

    def Configure(self,
                  host="192.168.1.104",
                  port=23
                  ):

        panel    = eg.ConfigPanel()
        hostCtrl = panel.TextCtrl(host)
        portCtrl = panel.SpinIntCtrl(port, max=65535)
        
        st1 = panel.StaticText("Host:")
        st2 = panel.StaticText("Port:")

        eg.EqualizeWidths((st1, st2))
        IPBox = panel.BoxedGroup(
            "TCPIP/IP Settings",
            (st1, hostCtrl),
            (st2, portCtrl),
        )

        panel.sizer.Add(IPBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                portCtrl.GetValue(),
            )
            
    def __start__ (self, host, port):
        self.host = host
        self.port = port
        self.initValues()
        

    def __stop__ (self):
        pass

    def initValues (self):
        zmDict = {}
        url = 'http://' + str(self.host) + ':80/goform/formMainZone_MainZoneXml.xml'

        try:
            r = urllib2.urlopen(url, timeout = 1).read()
        except urllib2.HTTPError, e:
            eg.PrintNotice("Connection error, wrong IP or AVR not accessible")
            return False
        except urllib2.URLError, e:
            eg.PrintNotice("Connection error, wrong IP or AVR not accessible")
            return False

        j = minidom.parseString(r)

        po = j.getElementsByTagName('ZonePower')[0]
        Power = po.getElementsByTagName('value')[0].firstChild.nodeValue
        friend = j.getElementsByTagName('FriendlyName')[0]
        Name = friend.getElementsByTagName('value')[0].firstChild.nodeValue
        put = j.getElementsByTagName('InputFuncSelect')[0]
        Input = put.getElementsByTagName('value')[0].firstChild.nodeValue
        mut = j.getElementsByTagName('Mute')[0]
        Mute = mut.getElementsByTagName('value')[0].firstChild.nodeValue
        vol = j.getElementsByTagName('MasterVolume')[0]
        volu = vol.getElementsByTagName('value')[0].firstChild.nodeValue
        Volume = str((float(volu)+80))

        zmDict = {"Power":Power, "Input":Input, "Volume":Volume, "Mute":Mute}
        self.TriggerEvent(Name, zmDict)

        z2Dict = {}
        url2 = 'http://' + str(self.host) + ':80/goform/formMainZone_MainZoneXml.xml?=&ZoneName=ZONE2'

        try:
            q = urllib2.urlopen(url2, timeout = 1).read()
        except urllib2.HTTPError, e:
            return False
        except urllib2.URLError, e:
            return False

        q = urllib2.urlopen(url2).read()
        y = minidom.parseString(q)

        po2 = y.getElementsByTagName('ZonePower')[0]
        Power2 = po2.getElementsByTagName('value')[0].firstChild.nodeValue
        friend2 = y.getElementsByTagName('FriendlyName')[0]
        Name2 = friend2.getElementsByTagName('value')[0].firstChild.nodeValue + "Z2"
        put2 = y.getElementsByTagName('InputFuncSelect')[0]
        Input2 = put2.getElementsByTagName('value')[0].firstChild.nodeValue
        mut2 = y.getElementsByTagName('Mute')[0]
        Mute2 = mut2.getElementsByTagName('value')[0].firstChild.nodeValue
        vol2 = y.getElementsByTagName('MasterVolume')[0]
        volu2 = vol2.getElementsByTagName('value')[0].firstChild.nodeValue
        Volume2 = str((float(volu2)+80))

        z2Dict = {"Power":Power2, "Input":Input2, "Volume":Volume2, "Mute":Mute2}
        self.TriggerEvent(Name2, z2Dict) 
    
    def connect (self):
        if (self.connected):
            self.socket.close()
            
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.settimeout(1.0)
        try:
            x = self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except:
            if eg.debugLevel:
                eg.PrintTraceback()
            self.PrintError("DenonTCPIP - Couldn't connect to receiver")
            self.disconnect()
            return False

    def disconnect(self):
        if (self.connected):
            self.socket.close()
            del self.socket
        self.connected = False
        return True

    def send(self, str):
        if (not self.connected):
            self.connect()
        cmd = str+"\r"
        if (sys.version_info[0] < 3):
            self.socket.sendall(cmd)
        else:
            self.socket.sendall(cmd.encode("utf-8"))
        
    def recv(self):
        if (not self.connected):
            self.PrintError("DenonTCPIP - Tried to receive, but there is no connection")
        r = self.socket.recv(1024)
        if (sys.version_info[0] < 3):
            return r
        else:
            return r.decode("utf-8")
        
    def getMute (self):
        self.send("MU?")
        m = self.recv()
        if (m == "MUOFF\r"):
            return False
        elif (m == "MUON\r"):
            return True
        else:
            return m

    def getState (self):
        self.send("ZM?")
        state = self.recv()
        if (state == "ZMON\r"):
            return True
        elif (state == "ZMOFF\r"):
            return False
        else:  
            return state

    def getsource (self):
        self.send("SI?")
        self.si = self.recv()
        return self.si

    def getVolume(self):
        self.send("MV?")
        v = self.recv()
        vg = re.match("MV(\d+)", v)
        if (vg is None):
            return v
        else:
            self.volume.set(vg.group(1))
            return vg.group(1)

    def getMuteZ2 (self):
        self.send("Z2MU?")
        m = self.recv()
        if (m == "Z2MUOFF\r"):
            return False
        elif (m == "Z2MUON\r"):
            return True
        else:
            return m

    def getStateZ2 (self):
        self.send("Z2?")
        stateZ2 = self.recv()
        if (stateZ2 == "Z2ON\r"):
            return True
        elif (state == "Z2OFF\r"):
            return False
        else:  
            return stateZ2

    def fade(self, mult):
        firstDelay = 0.3
        startDelay = 0.3
        endDelay   = 0.3
        sweepTime  = 5.0

        while(True):
            self.volume.step(mult)
            self.send("MV"+self.volume.toSend())
            event = eg.event
            if event.shouldEnd.isSet():
                break
            elapsed = time.clock() - event.time
            if elapsed < firstDelay * 0.90:
                delay = firstDelay
            elif sweepTime > 0.0:
                sweepDelay = (
                    (startDelay - endDelay)
                    * (sweepTime - (elapsed + firstDelay))
                    / sweepTime
                )
                if sweepDelay < 0:
                    sweepDelay = 0
                delay = sweepDelay + endDelay
            else:
                delay = endDelay
            event.shouldEnd.wait(delay)

class GenericSend(eg.ActionBase):
    name = "Send Generic Command"
    description = "Send Command, Example: MU?, MUON, MUOFF"

    def Configure(self, cmd="MU?"):

        panel       = eg.ConfigPanel()
        cmdCtrl     = panel.TextCtrl(cmd)
        
        st1 = panel.StaticText("Command:")

        cmdBox = panel.BoxedGroup(
            "Command to send",
            (st1, cmdCtrl),
        )

        panel.sizer.Add(cmdBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                cmdCtrl.GetValue(),
            )

    def __call__(self, cmd):
        self.plugin.send(cmd)
        si = self.plugin.recv()
        return si

class osmUp(eg.ActionBase):
    name = "OSM Up"
    description = "Triggers Up button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCUP")
        self.plugin.disconnect()

class osmDown(eg.ActionBase):
    name = "OSM Down"
    description = "Triggers Down button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCDN")
        self.plugin.disconnect()

class osmLeft(eg.ActionBase):
    name = "OSM Left"
    description = "Triggers Left button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCLT")
        self.plugin.disconnect()

class osmRight(eg.ActionBase):
    name = "OSM Right"
    description = "Triggers Right button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCUP")
        self.plugin.disconnect()

class osmSelect(eg.ActionBase):
    name = "OSM Select"
    description = "Triggers Select button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCENT")
        self.plugin.disconnect()
                        
class osmOption(eg.ActionBase):
    name = "OSM Option"
    description = "Triggers Option button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCOPT")
        self.plugin.disconnect()

class osmInfo(eg.ActionBase):
    name = "OSM Info"
    description = "Triggers Info button for On Screen Menu"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("MNCINF")
        self.plugin.disconnect()
  
class GetMainZoneVolume(eg.ActionBase):
    name = "Get Volume  (Zone 1)"
    description = "Query Zone 1 Volume State"
    
    def __call__(self):
        self.plugin.connect()
        vol = str(self.plugin.getVolume())
        self.plugin.volume.resetStep()
        self.plugin.disconnect()
        return vol

class VolumeMainZoneUp(eg.ActionBase):
    name = "Volume + 5 (Zone 1)"
    description = " Raises Zone 1 volume points"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.fade(1)
        self.plugin.disconnect()
        
class VolumeMainZoneDn(eg.ActionBase):
    name = "Volume - 5 (Zone 1)"
    description = "Lowers Zone 1 volume 5 points"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.fade(-1)
        self.plugin.disconnect()

class ToggleMainZoneMute(eg.ActionBase):
    name = "Toggle Mute  (Zone 1)"
    description = "Toggle Zone 1 Mute State"
    
    def __call__(self):
        self.plugin.connect()
        if self.plugin.getMute() == True:
            self.plugin.send("MUOFF")
        else:
            self.plugin.send("MUON")
        self.plugin.disconnect()

class ToggleMainZonePower(eg.ActionBase):
    name = "Toggle Power (Zone 1)"
    description = "Toggle Zone 1 Power State"
    
    def __call__(self):
        self.plugin.connect()
        if (self.plugin.getState() == True):
            self.plugin.send("ZMOFF")
        else:
            self.plugin.send("ZMON")
        self.plugin.disconnect()

class SetMainZonePowerOn(eg.ActionBase):
    name = "Set Power On  (Zone 1)"
    description = "Set Zone 1 Power State to On"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("ZMON")
        self.plugin.disconnect()

class SetMainZonePowerOff(eg.ActionBase):
    name = "Set Power Off  (Zone 1)"
    description = "Set Zone 1 Power State to Off"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("ZMOFF")
        self.plugin.disconnect()
        
class SetMainZoneSource(eg.ActionBase):
    name = "Set Input (Zone 1)"
    description = "Set Zone 1 Input to Selected Value"
    
    def Configure(self, source=""):
        panel       = eg.ConfigPanel()
	choices = ['NET', 'MPLAY', 'PHONO', 'CD', 'TUNER', 'DVD', 'HDP', 'TV/CBL', 'SAT', 'VCR', 'DVR', '.AUX', 'NET/USB', 'XM', 'IPOD', 'SAT/CBL', 'GAME']

	sourceCtrl = wx.ComboBox(panel, choices=choices)
        st2 = panel.StaticText("Source:")
        st3 = panel.StaticText("Other:")
        cmdBox = panel.BoxedGroup(
            "Source to change to",
            (st2, sourceCtrl),
        )

        panel.sizer.Add(cmdBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                sourceCtrl.GetValue(),
            )

    def __call__(self, source):
        self.plugin.connect()
        self.plugin.send("SI"+source)
        self.plugin.disconnect()

class SetMainZoneAudioSource(eg.ActionBase):
    name = "Set Audio Source (Zone 1)"
    description = "Set Zone 1 Audio Output to Selected Value"
    
    def Configure(self, source=""):
        panel       = eg.ConfigPanel()
	choices = ['AUTO', 'HDMI', 'DIGITAL', 'ANALOG', 'EXT.IN', '7.1IN', 'NO']

	sourceCtrl = wx.ComboBox(panel, choices=choices)
        st2 = panel.StaticText("Source:")
        st3 = panel.StaticText("Other:")
        cmdBox = panel.BoxedGroup(
            "Source to change to",
            (st2, sourceCtrl),
        )

        panel.sizer.Add(cmdBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                sourceCtrl.GetValue(),
            )

    def __call__(self, source):
        self.plugin.connect()
        self.plugin.send("SD"+source)
        self.plugin.disconnect()

class SetMainZoneVolumeLevel(eg.ActionBase):
    name = "Set Volume Level (Zone 1)"
    description = "Set Zone 1 Volume Selected Value"
    
    def Configure(self, vol=55):
        panel = eg.ConfigPanel()
        spaceString = panel.StaticText("")
        volumeCtrl = panel.SpinIntCtrl(vol, max=80)
	ctrlBox = panel.BoxedGroup(
            "Set Volume Level",
            ("Volume", volumeCtrl)
        )
	
        panel.sizer.Add(spaceString, 0, wx.EXPAND)
        panel.sizer.Add(ctrlBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                volumeCtrl.GetValue(),
            )

    def __call__(self, vol):
        self.plugin.connect()
        self.plugin.send("MV"+str(vol))
        self.plugin.disconnect()
        
class GetMainZoneSource(eg.ActionBase):
    name = "Get Input Source (Zone 1)"
    description = "Get Zone 1 Input Source"
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("SI?")
        sour = self.plugin.recv()
        sourc = re.match("SI(.*?)\r", sour)
        source = sourc.group(1)
        self.plugin.disconnect()
	return source

class GetMainZoneState(eg.ActionBase):
    name = "Get Power (Zone 1)"
    description = "Get Zone 1 Power State"
    
    def __call__(self):
        self.plugin.connect()
        state = self.plugin.getState()
	return state

class GetMainZoneMute(eg.ActionBase):
    name = "Get Mute (Zone 1)"
    description = "Get Zone 1 Mute State"
    
    def __call__(self):
        self.plugin.connect()
        state = self.plugin.getMute()
	return state

class ToggleZone2Mute(eg.ActionBase):
    name = "Toggle Mute (Zone 2)"
    description = "Toggle Zone 2 Mute State"
    
    def __call__(self):
        self.plugin.connect()
        if (self.plugin.getMuteZ2() == True):
            self.plugin.send("Z2MUOFF")
        else:
            self.plugin.send("Z2MUON")
        self.plugin.disconnect()

class ToggleZone2Power(eg.ActionBase):
    name = "Toggle Power (Zone 2)"
    description = "Toggle Zone 2 Power State"
    
    def __call__(self):
        self.plugin.connect()
        if (self.plugin.getStateZ2() == "Z2ON\r"):
            self.plugin.send("Z2OFF")
        else:
            self.plugin.send("Z2ON")
        self.plugin.disconnect()

class SetZone2PowerOn(eg.ActionBase):
    name = "Set Power On (Zone 2)"
    description = "Set Zone 2 Power State to On"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("Z2ON")
        self.plugin.disconnect()

class SetZone2PowerOff(eg.ActionBase):
    name = "Set Power Off  (Zone 2)"
    description = "Set Zone 2 Power State to Off"
    
    def __call__(self):
        self.plugin.connect()
        self.plugin.send("Z2OFF")
        self.plugin.disconnect()

class SetZone2VolumeLevel(eg.ActionBase):
    name = "Set Volume Level (Zone 2)"
    description = "Set Zone 2 Volume Selected Value"
    
    def Configure(self, vol=55):
        panel = eg.ConfigPanel()
        spaceString = panel.StaticText("")
        volumeCtrl = panel.SpinIntCtrl(vol, max=80)
	ctrlBox = panel.BoxedGroup(
            "Set Volume Level",
            ("Volume", volumeCtrl)
        )
	
        panel.sizer.Add(spaceString, 0, wx.EXPAND)
        panel.sizer.Add(ctrlBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                volumeCtrl.GetValue(),
            )

    def __call__(self, vol):
        self.plugin.connect()
        self.plugin.send("Z2"+str(vol))
        self.plugin.disconnect()
        

class SetZone2Source(eg.ActionBase):
    name = "Set Input (Zone 2)"
    description = "Set Zone 2 Input to Selected Value"
    
    def Configure(self, source=""):
        panel       = eg.ConfigPanel()
	choices = ['NET', 'MPLAY', 'PHONO', 'CD', 'TUNER', 'DVD', 'HDP', 'TV/CBL', 'SAT', 'VCR', 'DVR', '.AUX', 'NET/USB', 'XM', 'IPOD', 'SAT/CBL', 'GAME']

	sourceCtrl = wx.ComboBox(panel, choices=choices)
        st2 = panel.StaticText("Source:")
        st3 = panel.StaticText("Other:")
        cmdBox = panel.BoxedGroup(
            "Source to change to",
            (st2, sourceCtrl),
        )

        panel.sizer.Add(cmdBox, 0, wx.EXPAND)

        while panel.Affirmed():
            panel.SetResult(
                sourceCtrl.GetValue(),
            )

    def __call__(self, source):
        self.plugin.connect()
        self.plugin.send("Z2"+source)
        self.plugin.disconnect()

class GetZone2State(eg.ActionBase):
    name = "Get Power (Zone 2)"
    description = "Get Zone 2 Power State"
    def __call__(self):
        self.plugin.connect()
        state = self.plugin.getStateZ2()
	return state

class GetZone2Mute(eg.ActionBase):
    name = "Get Mute (Zone 2)"
    description = "Get Zone 2 Mute State"
    def __call__(self):
        self.plugin.connect()
        mute = self.plugin.getMuteZ2()
	return mute
