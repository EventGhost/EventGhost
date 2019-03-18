# -*- coding: utf-8 -*-
#
# plugins/Webserver - Z-Way/__init__.py
#
# This file is a plugin for EventGhost.

import eg
import wx
import json
import socket
import requests
from urllib import quote
from time import sleep

eg.RegisterPlugin(
    name = "Webserver - Z-Way",
    author = "Sem;colon",
    version = "0.40.1",
    kind = "external",
    description = u"""Plugin to control Z-WAVE devices.\n Prerequisites: Raspberry PI with RaZberry module (UZB on Raspberry PI or PC should work as well, but is not tested)""",
    createMacrosOnAdd = True,
    canMultiLoad = False,
    guid = '{9E8E217D-8596-4934-8C9B-2332449635AB}',
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t=6867",
)


class WebZWay(eg.PluginBase):
            
    class Text:
        file  = "File on your Webserver that should be requested when doing a post request from Z-Way (you can leave it empty to request the index):"
        switchGroupName = "SwitchBinary"
        switchGroupDescription = "Actions for CommandClass 37: SwitchBinary (Binary/Normal Switches)"
        dimGroupName = "SwitchMultilevel"
        dimGroupDescription = "Actions for CommandClass 38: SwitchMultilevel (Dimmer)"
        thermostatGroupName = "Thermostat"
        thermostatGroupDescription = "Actions for CommandClass 67: ThermostatSetPoint (Thermostates)"
        colorGroupName = "SwitchColor"
        colorGroupDescription = "Actions for CommandClass 51: SwitchColor"
        port    = "TCP/IP port:"
        webAuthUsername = "Username:"
        webAuthPassword = "Password:"
        webCertfile = "SSL certificate"
        webKeyfile = "SSL private key"
        sslTool = "Select the appropriate file if you want to use a secure "\
            "protocol (https).\n If this field remains blank, the server will use an "\
            "unsecure protocol (http). "
        cMask = (
            "crt files (*.crt)|*.crt"
            "|pem files (*.pem)|*.pem"
            "|All files (*.*)|*.*"
        )
        kMask = (
            "key files (*.key)|*.key"
            "|pem files (*.pem)|*.pem"
            "|All files (*.*)|*.*"
        )
        webBox = "Webserver parameters"
    
    def __init__(self):
        self.hosts={}
        self.AddAction(AddHost)
        self.AddAction(RemoveHost)
        self.AddAction(GetDeviceData)
        self.AddAction(GetAllDeviceData)
        self.AddAction(CustomCommand)
        
        switchGroup = self.AddGroup(
            self.Text.switchGroupName,
            self.Text.switchGroupDescription
        )
        switchGroup.AddAction(SwitchBinarySet)
        
        dimGroup = self.AddGroup(
            self.Text.dimGroupName,
            self.Text.dimGroupDescription
        )
        dimGroup.AddAction(SwitchMultilevelOnOff)
        dimGroup.AddAction(SwitchMultilevelSet)
        dimGroup.AddAction(SwitchMultilevelStartLevelChange)
        
        thermostatGroup = self.AddGroup(
            self.Text.thermostatGroupName,
            self.Text.thermostatGroupDescription
        )
        thermostatGroup.AddAction(ThermostatSetPointSet)
        thermostatGroup.AddAction(ThermostatModeSet)
        
        colorGroup = self.AddGroup(
            self.Text.colorGroupName,
            self.Text.colorGroupDescription
        )
        colorGroup.AddAction(SwitchColorSet)
        colorGroup.AddAction(SwitchColorSetMultiple)
        colorGroup.AddAction(SwitchColorStartLevelChange)
        
        self.thisPcName=socket.gethostname()
        tmp = [a for a in socket.gethostbyname_ex(self.thisPcName)[2]]
        addresses = []
        for a in tmp:
            if a.startswith("127.") or a.startswith("169."):
                continue
            addresses.append(a)
        self.thisPcIPs=addresses
        webPlug = eg.pluginManager.OpenPlugin('{E4305D8E-A3D3-4672-B06E-4EA1F0F6C673}', None, ())
        self.webServer = webPlug.instance


    def __stop__(self):
        self.webServer.__stop__()
        
             
    def __start__(self, file="", webPort=80, webAuthUsername="", webAuthPassword="", webCertfile = "", webKeyfile = ""):
        self.callFile = ""#file
        self.webPort = webPort
        self.webAuthUsername = webAuthUsername
        self.webAuthPassword = webAuthPassword
        self.webCertfile = webCertfile
        self.webKeyfile = webKeyfile
        self.webServer.__start__("Z-Way",webPort,"","EventGhost Z-Way Plugin",webAuthUsername,webAuthPassword,{},False,",",";;",webCertfile,webKeyfile)
      
      
    def OnComputerSuspend(self,type=None):
        self.__stop__()
    
    
    def OnComputerResume(self,type=None):
        self.__start__(*self.info.args)
        
        
    def Configure(self, file="", webPort=80, webAuthUsername="", webAuthPassword="", webCertfile = "", webKeyfile = ""):
        text = self.Text
        panel = eg.ConfigPanel(self)
        ACV = wx.ALIGN_CENTER_VERTICAL
        webPortCtrl = panel.SpinIntCtrl(webPort, min=1, max=65535)
        webCertfileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = text.sslTool,
            dialogTitle = text.webCertfile,
            buttonText = eg.text.General.browse,
            startDirectory = "",
            initialValue = webCertfile,
            fileMask = text.cMask,
        )
        webKeyfileCtrl = eg.FileBrowseButton(
            panel,
            -1,
            toolTip = text.sslTool,
            dialogTitle = text.webKeyfile,
            buttonText = eg.text.General.browse,
            startDirectory = "",
            initialValue = webKeyfile,
            fileMask = text.kMask,
        )
        webAuthUsernameCtrl = panel.TextCtrl(webAuthUsername)
        webAuthPasswordCtrl = panel.TextCtrl(webAuthPassword)
        labels = (
            panel.StaticText(text.port),
            panel.StaticText(text.webAuthUsername),
            panel.StaticText(text.webAuthPassword),
            panel.StaticText(text.webCertfile + ":"),
            panel.StaticText(text.webKeyfile + ":")
        )
        eg.EqualizeWidths(labels)
        sizer = wx.FlexGridSizer(5, 2, 5, 5)
        sizer.AddGrowableCol(1)
        sizer.Add(labels[0], 0, ACV)
        sizer.Add(webPortCtrl)
        sizer.Add(labels[3], 0, ACV)
        sizer.Add(webCertfileCtrl, 0, wx.EXPAND)
        sizer.Add(labels[4], 0, ACV)
        sizer.Add(webKeyfileCtrl, 0, wx.EXPAND)
        sizer.Add(labels[1], 0, ACV)
        sizer.Add(webAuthUsernameCtrl)
        sizer.Add(labels[2], 0, ACV)
        sizer.Add(webAuthPasswordCtrl)
        webBox = wx.StaticBox(panel, label=text.webBox)
        webBoxSizer = wx.StaticBoxSizer(webBox, wx.VERTICAL)
        webBoxSizer.Add(sizer, 0, wx.LEFT|wx.RIGHT|wx.BOTTOM|wx.EXPAND, 5)
        panel.sizer.Add(webBoxSizer, 0, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(
                "",
                webPortCtrl.GetValue(),
                webAuthUsernameCtrl.GetValue(),
                webAuthPasswordCtrl.GetValue(),
                webCertfileCtrl.GetValue(),
                webKeyfileCtrl.GetValue(),
            )
            
            
    def Request(self,ip,port,command,user,password):
        topLevelUrl = 'http://'+ip+':'+str(port)
        DevicesUrl= topLevelUrl +'/'+ command
        LoginUrl = topLevelUrl + '/ZAutomation/api/v1/login'
        LoginHeader = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'application/json'}
        Formlogin = '{"form": true, "login": "'+user+'", "password": "'+password+'", "keepme": false, "default_ui": 1}'

        session = requests.Session()
        session.post(LoginUrl,headers=LoginHeader, data=Formlogin)

        response = session.get(DevicesUrl)
        try:
            return response.json()
        except:
            eg.PrintError("Z-Way ERROR: "+str(response))
    
        

class AddHost(eg.ActionBase):
    name = "Add a Z-Way host"
    
    class Text:
        ip = 'IP Addess:'
        user = 'Username:'
        alias  = "Unique identifier for this host:"
        file  = "File that should be requested when doing post request from Z-Way:"
        port    = "Network Port:"
        password= "Password:"
    
    def __call__(self,alias,ip, port=8083, user="", password=""):
        protocol="http"
        if self.plugin.webCertfile!="":
            protocol="https"
        params=quote(json.dumps([alias,self.plugin.thisPcIPs,self.plugin.webPort,self.plugin.callFile.replace("/","~fs~").replace("\\","~bs~"),self.plugin.webAuthUsername,self.plugin.webAuthPassword,protocol]))
        try:
            devices=self.plugin.Request(ip,port,'JS/Run/initEG(\''+params+'\')', user, password)
        except:
            sleep(8)
            try:
                devices=self.plugin.Request(ip,port,'JS/Run/initEG(\''+params+'\')', user, password)
            except:
                eg.PrintError('Z-Way ERROR: Host "'+alias+'" can\'t be added!(connection not possible)')
                raise
                return False
        self.plugin.hosts[alias]={}
        self.plugin.hosts[alias]["ip"]=ip
        self.plugin.hosts[alias]["port"]=str(port)
        self.plugin.hosts[alias]["user"]=user
        self.plugin.hosts[alias]["password"]=password
        self.plugin.hosts[alias]["devices"]={}
        self.plugin.hosts[alias]["devicesPerClass"]={}#37:SwitchBinary,38:SwitchMultilevel,48:SensorBinary,49:SensorMultilevel,50:Meter,51:SwitchColor,64:ThermostatMode,67:ThermostatSetPoint
        for device in devices:
            if device[0] not in self.plugin.hosts[alias]["devices"]:
                self.plugin.hosts[alias]["devices"][device[0]]={}
            if device[1] not in self.plugin.hosts[alias]["devices"][device[0]]:
                self.plugin.hosts[alias]["devices"][device[0]][device[1]]=[]
            if device[2] not in self.plugin.hosts[alias]["devices"][device[0]][device[1]]:
                self.plugin.hosts[alias]["devices"][device[0]][device[1]].append(device[2])
            if device[2] not in self.plugin.hosts[alias]["devicesPerClass"]:
                self.plugin.hosts[alias]["devicesPerClass"][device[2]]={}
            if device[0] not in self.plugin.hosts[alias]["devicesPerClass"][device[2]]:
                self.plugin.hosts[alias]["devicesPerClass"][device[2]][device[0]]={}
            if device[1] not in self.plugin.hosts[alias]["devicesPerClass"][device[2]][device[0]]:
                self.plugin.hosts[alias]["devicesPerClass"][device[2]][device[0]][device[1]]={}
            if len(device)>3 and device[3] not in self.plugin.hosts[alias]["devicesPerClass"][device[2]][device[0]][device[1]]:
                self.plugin.hosts[alias]["devicesPerClass"][device[2]][device[0]][device[1]][device[3]]={}
        self.plugin.Request(ip,port,'JS/Run/getAllStates(\''+alias+'\')', user, password)
            
    def Configure(self,alias="Z-Way1", ip="", port=8083, user="", password=""):
        text = self.Text
        panel = eg.ConfigPanel(self)
        ipCtrl = panel.TextCtrl(ip)
        st1 = panel.StaticText(text.ip)
        portCtrl = panel.SpinIntCtrl(port, min=0, max=65535)
        st2 = panel.StaticText(text.port)
        aliasCtrl = panel.TextCtrl(alias)
        st3 = panel.StaticText(text.alias)
        userCtrl = panel.TextCtrl(user)
        st4 = panel.StaticText(text.user)
        passwordCtrl = panel.TextCtrl(password)
        st5 = panel.StaticText(text.password)
        eg.EqualizeWidths((st1,st2,st3,st4,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, ipCtrl)
        panel.AddLine(st2, portCtrl)
        panel.AddLine(st4, userCtrl)
        panel.AddLine(st5, passwordCtrl)
        while panel.Affirmed():
            panel.SetResult(
                aliasCtrl.GetValue(),
                ipCtrl.GetValue(),
                portCtrl.GetValue(),
                userCtrl.GetValue(),
                passwordCtrl.GetValue(),
            )

            
class RemoveHost(eg.ActionBase):
    name = "Remove a Z-Way host"
    
    class Text:
        alias  = "Unique identifier for this host:"
    
    def __call__(self,alias):
        result= self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'JS/Run/removeHost(\''+alias+'\')', self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        del self.plugin.hosts[alias]
        return result
            
    def Configure(self, alias=""):
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        st1 = panel.StaticText(text.alias)
        panel.AddLine(st1, aliasCtrl)
        while panel.Affirmed():
            panel.SetResult(
                aliasCtrl.GetStringSelection(),
            )
            

class SwitchBinarySet(eg.ActionBase):
    name = "ON/OFF"
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        targetState  = "Target State:"
        
    def __call__(self,deviceid,instanceid,alias,targetState):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        if targetState=="ON":
            targetState="255"
        else:
            targetState="0"
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[37].Set("+targetState+")"
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
            
    def GetLabel(self,deviceid="???",instanceid="???",alias="???",targetState=""):
        return "SwitchBinary "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+" "+targetState
    
    def Configure(self,deviceid="",instanceid="",alias="",targetState="ON"):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["37"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["37"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        statesList=["ON","OFF"]
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["37"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["37"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        targetStateCtrl = wx.Choice(panel, -1, choices=statesList)
        targetStateCtrl.SetSelection(statesList.index(targetState))
        st4 = panel.StaticText(text.targetState)
        eg.EqualizeWidths((st1,st2,st3,st4))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st4, targetStateCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
                targetStateCtrl.GetStringSelection(),
            )
            
            
class SwitchMultilevelSet(eg.ActionBase):
    name = "Set Level"
    description = u"""Meaning of the "Duration Value" field:  0 instantly.  1-127 in seconds.  128-254 in minutes mapped to 1-127 (value 128 is 1 minute).  255 use device factory default."""
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        targetLevel  = "Target Level:"
        duration  = "Duration Value:"
        
    def __call__(self,deviceid,instanceid,alias,targetLevel,duration=255):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[38].Set("+str(targetLevel)+","+str(duration)+")"
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
            
    def GetLabel(self,deviceid="???",instanceid="???",alias="???",targetLevel="",duration=""):
        return "SwitchMultilevel Set "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+" to "+str(targetLevel)
    
    def Configure(self,deviceid="",instanceid="",alias="",targetLevel=99,duration=255):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        targetLevelCtrl = panel.SpinIntCtrl(targetLevel, min=0, max=99)
        st4 = panel.StaticText(text.targetLevel)
        durationCtrl = panel.SpinIntCtrl(duration, min=0, max=255)
        st5 = panel.StaticText(text.duration)
        eg.EqualizeWidths((st1,st2,st3,st4,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st4, targetLevelCtrl)
        panel.AddLine(st5, durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
                targetLevelCtrl.GetValue(),
                durationCtrl.GetValue(),
            )

            
class SwitchMultilevelOnOff(eg.ActionBase):
    name = "ON/OFF (Previous Value)"
    description = u"""Meaning of the "Duration Value" field:  0 instantly.  1-127 in seconds.  128-254 in minutes mapped to 1-127 (value 128 is 1 minute).  255 use device factory default."""
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        targetState  = "Target State:"
        duration  = "Duration Value:"
        
    def __call__(self,deviceid,instanceid,alias,targetState,duration=255):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        if targetState=="ON":
            targetState="100"
        else:
            targetState="0"
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[38].Set("+targetState+","+str(duration)+")"
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
    
    def GetLabel(self,deviceid="???",instanceid="???",alias="???",targetState="",duration=""):
        return "SwitchMultilevel "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+" "+targetState
    
    def Configure(self,deviceid="",instanceid="",alias="",targetState="ON",duration=255):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        statesList=["ON","OFF"]
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        targetStateCtrl = wx.Choice(panel, -1, choices=statesList)
        targetStateCtrl.SetSelection(statesList.index(targetState))
        st4 = panel.StaticText(text.targetState)
        durationCtrl = panel.SpinIntCtrl(duration, min=0, max=255)
        st5 = panel.StaticText(text.duration)
        eg.EqualizeWidths((st1,st2,st3,st4,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st4, targetStateCtrl)
        panel.AddLine(st5, durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
                targetStateCtrl.GetStringSelection(),
                durationCtrl.GetValue(),
            )


class SwitchMultilevelStartLevelChange(eg.ActionBase):
    name = "Change Level UP/DOWN"
    description = u"""Meaning of the "Duration Value" field:  0 instantly.  1-127 in seconds.  128-254 in minutes mapped to 1-127 (value 128 is 1 minute).  255 use device factory default."""
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        direction = "Direction:"
        duration = "Duration Value:"
        ignoreStartLevel = "Ignore Start Level:"
        startLevel = "Start Level:"
        indec = "indec:"
        step = "Step in %:"
        
    def __call__(self,deviceid,instanceid,alias,direction,duration=255,ignoreStartLevel=True,startLevel=50,indec=0,step=255):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        def UpFunc():
            command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[38].StopLevelChange()"
            self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        if direction=="UP":
            direction="0"
        else:
            direction="1"
        if ignoreStartLevel:
            ignoreStartLevel="true"
        else:
            ignoreStartLevel="false"
        step-=1
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[38].StartLevelChange("+direction+","+str(duration)+","+ignoreStartLevel+","+str(startLevel)+","+str(indec)+","+str(step)+")"
        self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        eg.event.AddUpFunc(UpFunc)
    
    def GetLabel(self,deviceid="???",instanceid="???",alias="???",direction="",duration=""):
        return "SwitchMultilevel StartLevelChange "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+" "+direction
    
    def Configure(self,deviceid="",instanceid="",alias="",direction="UP",duration=255):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        directionsList=["UP","DOWN"]
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["38"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        targetStateCtrl = wx.Choice(panel, -1, choices=directionsList)
        targetStateCtrl.SetSelection(directionsList.index(direction))
        st4 = panel.StaticText(text.direction)
        durationCtrl = panel.SpinIntCtrl(duration, min=0, max=255)
        st5 = panel.StaticText(text.duration)
        eg.EqualizeWidths((st1,st2,st3,st4,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st4, targetStateCtrl)
        panel.AddLine(st5, durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
                targetStateCtrl.GetStringSelection(),
                durationCtrl.GetValue(),
            )
            

class ThermostatSetPointSet(eg.ActionBase):
    name = "Set Value"
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        modeid = "Mode ID:"
        targetLevel  = "Target Value:"
        
    def __call__(self,deviceid,instanceid,modeid,alias,targetLevel):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[67].Set("+str(modeid)+","+str(targetLevel)+")"
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
    
    def GetLabel(self,deviceid="???",instanceid="???",modeid="???",alias="???",targetLevel="???"):
        return "ThermostatSetPoint Set "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+"/"+str(modeid)+" to "+str(targetLevel)
    
    def Configure(self,deviceid="",instanceid="",modeid="",alias="",targetLevel=10.0):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            modeid=modeidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["67"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["67"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
            try:
                modeList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["67"][deviceidCtrl.GetStringSelection()][instanceidCtrl.GetStringSelection()].keys())
            except KeyError:
                modeList = list()
            modeidCtrl.Clear()
            modeidCtrl.AppendItems(modeList)
            if modeid in modeList:
                modeidCtrl.SetSelection(modeList.index(modeid))
            else:
                modeidCtrl.SetSelection(0)
        
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["67"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["67"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            modeList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["67"][deviceidCtrl.GetStringSelection()][instanceidCtrl.GetStringSelection()].keys())
        except KeyError:
            modeList = list()
        st2 = panel.StaticText(text.instanceid)
        modeidCtrl = wx.Choice(panel, -1, choices=modeList)
        if modeid in modeList:
            modeidCtrl.SetSelection(modeList.index(modeid))
        else:
            modeidCtrl.SetSelection(0)
        modeidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st5 = panel.StaticText(text.modeid)
        targetLevelCtrl = panel.SpinNumCtrl(targetLevel, min=-99.0, max=99.0)
        st4 = panel.StaticText(text.targetLevel)
        eg.EqualizeWidths((st1,st2,st3,st4,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st5, modeidCtrl)
        panel.AddLine(st4, targetLevelCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                modeidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
                targetLevelCtrl.GetValue(),
            )
            
            
class ThermostatModeSet(eg.ActionBase):
    name = "Set Mode"
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        modeid = "Mode ID:"
        
    def __call__(self,deviceid,instanceid,modeid,alias):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[64].Set("+str(modeid)+")"
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
    
    def GetLabel(self,deviceid="???",instanceid="???",modeid="???",alias="???"):
        return "ThermostatMode Set "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+" to "+str(modeid)
    
    def Configure(self,deviceid="",instanceid="",modeid="",alias=""):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            modeid=modeidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["64"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["64"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
            try:
                modeList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["64"][deviceidCtrl.GetStringSelection()][instanceidCtrl.GetStringSelection()].keys())
            except KeyError:
                modeList = list()
            modeidCtrl.Clear()
            modeidCtrl.AppendItems(modeList)
            if modeid in modeList:
                modeidCtrl.SetSelection(modeList.index(modeid))
            else:
                modeidCtrl.SetSelection(0)
        
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["64"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["64"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            modeList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["64"][deviceidCtrl.GetStringSelection()][instanceidCtrl.GetStringSelection()].keys())
        except KeyError:
            modeList = list()
        st2 = panel.StaticText(text.instanceid)
        modeidCtrl = wx.Choice(panel, -1, choices=modeList)
        if modeid in modeList:
            modeidCtrl.SetSelection(modeList.index(modeid))
        else:
            modeidCtrl.SetSelection(0)
        modeidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st5 = panel.StaticText(text.modeid)
        eg.EqualizeWidths((st1,st2,st3,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st5, modeidCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                modeidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
            )
        

class SwitchColorSet(eg.ActionBase):
    name = "Set Value"
    description = u"""Meaning of the "Duration Value" field:  0 instantly.  1-127 in seconds.  128-254 in minutes mapped to 1-127 (value 128 is 1 minute).  255 use device factory default."""
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        modeid = "Color:"
        targetLevel  = "Target Value:"
        duration = "Duration Value:"
        
    def __call__(self,deviceid,instanceid,modeid,alias,targetLevel,duration=255):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[51].Set("+str(modeid)+","+str(targetLevel)+","+str(duration)+")"
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
    
    def GetLabel(self,deviceid="???",instanceid="???",modeid="???",alias="???",targetLevel="???",duration="???"):
        return "SwitchColor Set "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+"/"+str(modeid)+" to "+str(targetLevel)
    
    def Configure(self,deviceid="",instanceid="",modeid=0,alias="",targetLevel=10.0,duration=255):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            modeid=modeidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        modeList=["Warm White","Cold White","Red","Green","Blue","Amber","Cyan","Purple","Indexed Color"]
        modeidCtrl = wx.Choice(panel, -1, choices=modeList)
        modeidCtrl.SetSelection(modeid)
        st5 = panel.StaticText(text.modeid)
        targetLevelCtrl = panel.SpinIntCtrl(targetLevel, min=0, max=255)
        st4 = panel.StaticText(text.targetLevel)
        durationCtrl = panel.SpinIntCtrl(duration, min=0, max=255)
        st6 = panel.StaticText(text.duration)
        eg.EqualizeWidths((st1,st2,st3,st4,st5,st6))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st5, modeidCtrl)
        panel.AddLine(st4, targetLevelCtrl)
        panel.AddLine(st6, durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                modeList.index(modeidCtrl.GetStringSelection()),
                aliasCtrl.GetStringSelection(),
                targetLevelCtrl.GetValue(),
                durationCtrl.GetValue(),
            )
            
            
class SwitchColorSetMultiple(eg.ActionBase):
    name = "Set Value RGB"
    description = u"""Meaning of the "Duration Value" field:  0 instantly.  1-127 in seconds.  128-254 in minutes mapped to 1-127 (value 128 is 1 minute).  255 use device factory default."""
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        targetLevel  = "Target Color:"
        duration = "Duration Value:"
        
    def __call__(self,deviceid,instanceid,alias,targetLevel,duration=255):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        if len(targetLevel)==7:
            targetLevel=targetLevel[1:]
            red=int(targetLevel[0:2],16)
            green=int(targetLevel[2:4],16)
            blue=int(targetLevel[4:],16)
            command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[51].SetMultiple([2,3,4],["+str(red)+","+str(green)+","+str(blue)+"],"+str(duration)+")"
            return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        return None
    
    def GetLabel(self,deviceid="???",instanceid="???",alias="???",targetLevel="???",duration="???"):
        return "SwitchColor SetMultiple "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+" to "+str(targetLevel)
    
    def Configure(self,deviceid="",instanceid="",alias="",targetLevel="#FFFFFF",duration=255):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        targetLevelCtrl = panel.TextCtrl(targetLevel)
        st4 = panel.StaticText(text.targetLevel)
        durationCtrl = panel.SpinIntCtrl(duration, min=0, max=255)
        st6 = panel.StaticText(text.duration)
        eg.EqualizeWidths((st1,st2,st3,st4,st6))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st4, targetLevelCtrl)
        panel.AddLine(st6, durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
                targetLevelCtrl.GetValue(),
                durationCtrl.GetValue(),
            )
            

class SwitchColorStartLevelChange(eg.ActionBase):
    name = "Change Level UP/DOWN"
    description = u"""Meaning of the "Duration Value" field:  0 instantly.  1-127 in seconds.  128-254 in minutes mapped to 1-127 (value 128 is 1 minute).  255 use device factory default."""
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        instanceid = "Instance ID:"
        modeid = "Color:"
        direction = "Direction:"
        duration = "Duration Value:"
        ignoreStartLevel = "Ignore Start Level:"
        startLevel = "Start Level:"
        indec = "indec:"
        step = "Step in %:"
        
    def __call__(self,deviceid,instanceid,modeid,alias,direction,duration=255,ignoreStartLevel=True,startLevel=50,indec=0,step=255):
        deviceid=str(deviceid)
        instanceid=str(instanceid)
        def UpFunc():
            command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[51].StopStateChange("+str(modeid)+")"
            self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        if direction=="UP":
            direction="0"
        else:
            direction="1"
        if ignoreStartLevel:
            ignoreStartLevel="true"
        else:
            ignoreStartLevel="false"
        step-=1
        command="devices["+deviceid+"].instances["+instanceid+"].commandClasses[51].StartStateChange("+str(modeid)+","+direction+","+str(duration)+","+ignoreStartLevel+","+str(startLevel)+","+str(indec)+","+str(step)+")"
        self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        eg.event.AddUpFunc(UpFunc)
    
    def GetLabel(self,deviceid="???",instanceid="???",modeid="???",alias="???",direction="",duration="",ignoreStartLevel=True,startLevel=50,indec=0,step=255):
        return "Change Level "+str(alias)+"/"+str(deviceid)+"/"+str(instanceid)+"/"+str(modeid)+" "+direction
    
    def Configure(self,deviceid="",instanceid="",modeid=0,alias="",direction="UP",duration=255):
        
        def onChoice(evt):
            deviceid=deviceidCtrl.GetStringSelection()
            instanceid=instanceidCtrl.GetStringSelection()
            try:
                deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"].keys())
            except KeyError:
                deviceList = list()
            deviceidCtrl.Clear()
            deviceidCtrl.AppendItems(deviceList)
            if deviceid in deviceList:
                deviceidCtrl.SetSelection(deviceList.index(deviceid))
            else:
                deviceidCtrl.SetSelection(0)
            try:
                interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"][deviceidCtrl.GetStringSelection()].keys())
            except KeyError:
                interfaceList = list()
            instanceidCtrl.Clear()
            instanceidCtrl.AppendItems(interfaceList)
            if instanceid in interfaceList:
                instanceidCtrl.SetSelection(interfaceList.index(instanceid))
            else:
                instanceidCtrl.SetSelection(0)
        
        text = self.Text
        directionsList=["UP","DOWN"]
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        try:
            deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"].keys())
        except KeyError:
            deviceList = list()
        st3 = panel.StaticText(text.host)
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        deviceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        try:
            interfaceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devicesPerClass"]["51"][deviceidCtrl.GetStringSelection()].keys())
        except KeyError:
            interfaceList = list()
        st1 = panel.StaticText(text.deviceid)
        instanceidCtrl = wx.Choice(panel, -1, choices=interfaceList)
        if instanceid in interfaceList:
            instanceidCtrl.SetSelection(interfaceList.index(instanceid))
        else:
            instanceidCtrl.SetSelection(0)
        instanceidCtrl.Bind(wx.EVT_CHOICE, onChoice)
        st2 = panel.StaticText(text.instanceid)
        modeList=["Warm White","Cold White","Red","Green","Blue","Amber","Cyan","Purple","Indexed Color"]
        modeidCtrl = wx.Choice(panel, -1, choices=modeList)
        modeidCtrl.SetSelection(modeid)
        st5 = panel.StaticText(text.modeid)
        targetStateCtrl = wx.Choice(panel, -1, choices=directionsList)
        targetStateCtrl.SetSelection(directionsList.index(direction))
        st4 = panel.StaticText(text.direction)
        durationCtrl = panel.SpinIntCtrl(duration, min=0, max=255)
        st6 = panel.StaticText(text.duration)
        eg.EqualizeWidths((st1,st2,st3,st4,st5))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        panel.AddLine(st2, instanceidCtrl)
        panel.AddLine(st5, modeidCtrl)
        panel.AddLine(st4, targetStateCtrl)
        panel.AddLine(st6, durationCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                instanceidCtrl.GetStringSelection(),
                modeList.index(modeidCtrl.GetStringSelection()),
                aliasCtrl.GetStringSelection(),
                targetStateCtrl.GetStringSelection(),
                durationCtrl.GetValue(),
            )

    
class GetDeviceData(eg.ActionBase):
    name = "Get data from one device"
    
    class Text:
        host = "Host:"
        deviceid = "Device ID:"
        
    def __call__(self,deviceid,alias):
        deviceid=str(deviceid)
        for instance in self.plugin.hosts[alias]["devices"][deviceid]:
            for commandClass in self.plugin.hosts[alias]["devices"][deviceid][instance]:
                if commandClass == "51":
                    for mode in list(self.plugin.hosts[alias]["devicesPerClass"][commandClass][deviceid][instance].keys()):
                        command="devices["+deviceid+"].instances["+instance+"].commandClasses["+commandClass+"].Get("+mode+")"
                else:
                    command="devices["+deviceid+"].instances["+instance+"].commandClasses["+commandClass+"].Get()"
                self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'ZWaveAPI/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
        return True
    
    def GetLabel(self,deviceid="???",alias="???"):
        return "Get data from device "+str(alias)+"/"+str(deviceid)
    
    def Configure(self,deviceid="",alias=""):
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        st3 = panel.StaticText(text.host)
        deviceList=list(self.plugin.hosts[aliasCtrl.GetStringSelection()]["devices"])
        deviceidCtrl = wx.Choice(panel, -1, choices=deviceList)
        if deviceid in deviceList:
            deviceidCtrl.SetSelection(deviceList.index(deviceid))
        else:
            deviceidCtrl.SetSelection(0)
        st1 = panel.StaticText(text.deviceid)
        eg.EqualizeWidths((st1,st3))
        panel.AddLine(st3, aliasCtrl)
        panel.AddLine(st1, deviceidCtrl)
        while panel.Affirmed():
            panel.SetResult(
                deviceidCtrl.GetStringSelection(),
                aliasCtrl.GetStringSelection(),
            )
            
            
class GetAllDeviceData(eg.ActionBase):
    name = "Get data from all devices"
    
    class Text:
        host = "Host:"
        
    def __call__(self,alias):
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'JS/Run/getAllStates(\''+alias+'\')', self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
            
    def Configure(self,alias=""):
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        else:
            aliasCtrl.SetSelection(0)
        st3 = panel.StaticText(text.host)
        panel.AddLine(st3, aliasCtrl)
        while panel.Affirmed():
            panel.SetResult(
                aliasCtrl.GetStringSelection(),
            )
            
            
class CustomCommand(eg.ActionBase):
    name = "Custom Command (JS)"
    
    class Text:
        host = "Host:"
        command  = "Command to send:"
        
    def __call__(self,command,alias):
        return self.plugin.Request(self.plugin.hosts[alias]["ip"],self.plugin.hosts[alias]["port"],'JS/Run/'+command, self.plugin.hosts[alias]["user"], self.plugin.hosts[alias]["password"])
            
    def GetLabel(self,command="???",alias="???"):
        return "Send Custom Command: "+command+" to host "+str(alias)
    
    def Configure(self,command="",alias=""):
        text = self.Text
        hostList=list(self.plugin.hosts.keys())
        panel = eg.ConfigPanel(self)
        commandCtrl = panel.TextCtrl(command, size=(500,-1))
        st1 = panel.StaticText(text.command)
        aliasCtrl = wx.Choice(panel, -1, choices=hostList)
        if alias in hostList:
            aliasCtrl.SetSelection(hostList.index(alias))
        st2 = panel.StaticText(text.host)
        eg.EqualizeWidths((st1,st2))
        panel.AddLine(st1, commandCtrl)
        panel.AddLine(st2, aliasCtrl)
        while panel.Affirmed():
            panel.SetResult(
                commandCtrl.GetValue(),
                aliasCtrl.GetStringSelection(),
            )
