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
# $LastChangedDate: 2009-05-15 12:00:002 +0800 $
# $LastChangedRevision: 500 $
# $LastChangedBy: kingtd $


eg.RegisterPlugin(
    name="WMC Controller",
    guid='{06B84539-F011-470A-A427-73BB814A63CF}',
    description="Receives events from a Windows Media Center PC and all extenders with the controller installed from http://www.codeplex.com/WMCController or https://github.com/gjniewenhuijse/MceController",
    kind="external",
    version="0.7.1" + "$LastChangedRevision: 348 $".split()[1],
    canMultiLoad=True,
    author="Dragon470 , from kingtd (based off original code from Bitmonster)",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABmJLR0QAAAAAAAD5Q7t/"
        "AAAACXBIWXMAAAsSAAALEgHS3X78AAAAB3RJTUUH1gIQFgQb1MiCRwAAAVVJREFUOMud"
        "kjFLw2AQhp8vif0fUlPoIgVx6+AgopNI3fwBViiIoOAgFaugIDhUtP4BxWDs4CI4d3MR"
        "cSyIQ1tDbcHWtjFI4tAWG5pE8ca7997vnrtP4BOZvW0dSBAcZ0pAMTEzPUs4GvMsVkvP"
        "6HktGWRAOBpjIXVNKOSWWdYXN7lFAAINhBCEQgqxyTHAAQQAD/dFbLurUYJYT7P7TI2C"
        "VavwIiZodyyaH6ZLo/RZVTXiOYVhGOh5jcpbq5eRAXAc5wdBVSPMLR16GtxdbgJgN95d"
        "OxicACG6bPH4uIu1UHjE7sFqR/NDVxhaoixLvFYbtDufNFtu1tzxgdeAaZfBU7ECTvd1"
        "WRlxsa4sp1ydkiRxkstmlEFRrWT4nrRer3vmlf6mb883fK8AoF1d+Bqc6Xkt+cufT6e3"
        "dnb9DJJrq+uYpunZ2WcFfA0ol8v8N5Qgvr/EN8Lzfbs+L0goAAAAAElFTkSuQmCC"
    ),
)

import asynchat
import socket
import time
import urllib


class Info:
    mcxUserList = [0]
    prefixList = ["WMC"]
    host = "127.0.0.1"
    port = 40400
    controlport = 40510  # using http instead of Telnet, more reliable as it can't disconnect
    pluginREF = ""


class Text:
    host = "Hostname/IP Address:"
    mcxusers = "list Mcx# (0 is PC):"
    eventPrefix = "Event Prefix:"
    tcpBox = "TCP/IP Settings"
    securityBox = "Security"
    eventGenerationBox = "Event generation"
    UniGen = "Show events(if unchecked, no events will generate)"
    KeyGen = "Show KeyPress events"
    TimeGen = "Show time events"

    class Send:
        name = "Send"


class WMCstatus(asynchat.async_chat):
    """Telnet engine class. Implements command line user interface."""

    def __init__(self, host, port, prefix, plugin):

        asynchat.async_chat.__init__(self)

        self.set_terminator("\n")

        self.data = ""
        self.host = host
        self.port = port
        self.plugin = plugin
        self.prefix = prefix

        # connect to WMC Status Engine
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)

        eg.RestartAsyncore()
        self.settimeout(1.0)
        self.connect((host, port))

    def handle_connect(self):
        # connection succeeded
        setattr(self.plugin, self.prefix + "_Status", "On")
        eg.TriggerEvent("Status Session Connected", str(self.host) + ":" + str(self.port), prefix=self.prefix)
        pass

    def handle_close(self):
        setattr(self.plugin, self.prefix + "_Status", "Off")
        eg.TriggerEvent("Status Session Closed", str(self.host) + ":" + str(self.port), prefix=self.prefix)
        self.close()

    def handle_expt(self):
        # connection failed
        setattr(self.plugin, self.prefix + "_Status", "Off")
        eg.TriggerEvent("Status Session Could Not Connect", str(self.host) + ":" + str(self.port), prefix=self.prefix)
        self.close()

    def collect_incoming_data(self, data):
        # received a chunk of incoming data
        self.data = self.data + data

    def found_terminator(self):
        # got a response line
        data = self.data
        if data.endswith("\r"):
            data = data[:-1]
        self.data = ""
        if (data.find("=") > -1):
            dcmd = data[:data.find("=")]
            dpay = data[data.find("=") + 1:]
            # this is events to eventghost
            if Info.UniversalLogs:
                if dcmd == "TrackTime" and Info.TimeLogs:
                    eg.TriggerEvent(dcmd, dpay, prefix=self.prefix)
                elif dcmd == "KeyPress" and Info.KeyLogs:
                    eg.TriggerEvent(dcmd, dpay, prefix=self.prefix)
                elif dcmd != "TrackTime" and dcmd != "KeyPress":
                    eg.TriggerEvent(dcmd, dpay, prefix=self.prefix)
            # internal variable data collection and storage
            # variables are assigned by the dcmd and name of mxc   variable format prefix.dcmd
            if dcmd == "StreamingContentAudio" or dcmd == "StreamingContentVideo" or dcmd == "PVR" or dcmd == "TVTuner" or dcmd == "CD" or dcmd == "DVD":
                # Type
                setattr(self.plugin, self.prefix + "_Type", dcmd)
            elif dcmd == "FS_DVD" or dcmd == "FS_Guide" or dcmd == "FS_Home" or dcmd == "FS_Music" or dcmd == "FS_Photos" or dcmd == "FS_Radio" or dcmd == "FS_RecordedShows" or dcmd == "FS_TV" or dcmd == "FS_Unknown" or dcmd == "FS_Videos":
                # Location
                setattr(self.plugin, self.prefix + "_Location", dcmd)
            elif dcmd == "Play" or dcmd == "Stop" or dcmd == "Pause" or dcmd == "FF1" or dcmd == "FF2" or dcmd == "FF3" or dcmd == "Rewind1" or dcmd == "Rewind2" or dcmd == "Rewind3" or dcmd == "SlowMotion1" or dcmd == "SlowMotion2" or dcmd == "SlowMotion3":
                # state
                setattr(self.plugin, self.prefix + "_State", dcmd)
            elif dcmd == "EndSession":
                # Set State
                setattr(self.plugin, self.prefix + "_State", "Stop")
                setattr(self.plugin, self.prefix + "_" + dcmd, dpay)
            else:
                setattr(self.plugin, self.prefix + "_" + dcmd, dpay)
        elif (data.find("204 Connected") > -1):
            dcmd = "204 Connected"
            dpay = data[data.find("204 Connected") + 14:]
            eg.TriggerEvent(dcmd, dpay, prefix=self.prefix)
        else:
            eg.TriggerEvent(data, prefix=self.prefix)


class WMCControl(eg.PluginClass):
    text = Text

    def __init__(self):
        self.AddAction(self.SendStock)
        self.AddAction(self.Send)
        self.AddAction(self.Connect)
        self.AddAction(self.GetInfo)

    def __start__(self, host, mcxUsers, prefixs, UniGen, TimeGen, KeyGen):
        Info.prefixList = prefixs.split()
        Info.mcxUserList = mcxUsers.split()
        Info.host = host
        Info.pluginREF = self
        Info.UniversalLogs = UniGen
        Info.TimeLogs = TimeGen
        Info.KeyLogs = KeyGen

        for x in Info.mcxUserList:
            try:
                self.status = WMCstatus(Info.host, int(Info.port) + int(x), Info.prefixList[Info.mcxUserList.index(x)],
                                        self)
            except socket.error, exc:
                raise self.Exception(exc[1])
            time.sleep(0.1)  # slight delay to help prevent asyncore errors

        SessionChangeNotifier(self)

    def __stop__(self):
        if self.status:
            self.status.close()
        self.status = None

    def Configure(self, host="127.0.0.1", mcxUsers="0", prefixs="WMC-PC", UniGen=True, TimeGen=True, KeyGen=True):
        text = self.text
        panel = eg.ConfigPanel(self)

        hostCtrl = panel.TextCtrl(host)
        mcxUsersCtrl = panel.TextCtrl(mcxUsers)
        eventPrefixsCtrl = panel.TextCtrl(prefixs)
        eventUniGenCtrl = wx.CheckBox(panel, -1, text.UniGen)
        eventUniGenCtrl.SetValue(UniGen)
        eventTimeGenCtrl = wx.CheckBox(panel, -1, text.TimeGen)
        eventTimeGenCtrl.SetValue(TimeGen)
        eventKeyGenCtrl = wx.CheckBox(panel, -1, text.KeyGen)
        eventKeyGenCtrl.SetValue(KeyGen)

        st1 = panel.StaticText(text.host)
        st2 = panel.StaticText(text.mcxusers)
        st4 = panel.StaticText(text.eventPrefix)
        eg.EqualizeWidths((st1, st4))

        box1 = panel.BoxedGroup(text.tcpBox, (st1, hostCtrl), (st2, mcxUsersCtrl))
        box2 = panel.BoxedGroup(text.eventGenerationBox, (st4, eventPrefixsCtrl), eventUniGenCtrl, eventTimeGenCtrl,
                                eventKeyGenCtrl)
        panel.sizer.AddMany([
            (box1, 0, wx.EXPAND),
            (box2, 0, wx.EXPAND | wx.TOP, 10),
        ])

        while panel.Affirmed():
            panel.SetResult(
                hostCtrl.GetValue(),
                mcxUsersCtrl.GetValue(),
                eventPrefixsCtrl.GetValue(),
                eventUniGenCtrl.GetValue(),
                eventTimeGenCtrl.GetValue(),
                eventKeyGenCtrl.GetValue(),
            )

    class Send(eg.ActionWithStringParameter):
        description = ("Sends any command to WMC Controller.")

        class Text:
            action = "WMC Command:"

        def __call__(self, action, mcx):
            url = "http://" + Info.host + ":" + str(40510 + int(mcx)) + "/" + str(eg.ParseString(action))
            send = urllib.urlopen(url)
            resonse = send.read()
            send.close()
            return True

        def Configure(self, action="", mcx=0):
            text = self.text
            panel = eg.ConfigPanel(self)

            actionCtrl = panel.TextCtrl(action)
            mcxCtrl = wx.Choice(panel, -1, (10, 80), choices=Info.prefixList)
            if str(mcx) in Info.mcxUserList:
                mcxCtrl.SetStringSelection(Info.prefixList[Info.mcxUserList.index(str(mcx))])
            st1 = panel.StaticText("Command:")
            st2 = panel.StaticText("Device:")
            box1 = panel.BoxedGroup("Command", (st1, actionCtrl), (st2, mcxCtrl))
            panel.sizer.AddMany([
                (box1, 0, wx.EXPAND)
            ])

            while panel.Affirmed():
                print mcxCtrl.GetCurrentSelection()
                panel.SetResult(
                    actionCtrl.GetValue(),
                    mcxCtrl.GetCurrentSelection()
                )

    class SendStock(eg.ActionBase):
        description = ("Sends a pre-set command to WMC Controller.")

        class Text:
            action = "WMC Command:"

        def __call__(self, action, mcx):
            print action
            url = "http://" + Info.host + ":" + str(40510 + int(mcx)) + "/" + str(action)
            send = urllib.urlopen(url)
            resonse = send.read()
            send.close()
            return True

        def Configure(self, action="button-ok", mcx=0):
            text = self.text
            panel = eg.ConfigPanel(self)

            actions = ["button-rec", "button-left", "button-right", "button-up", "button-down", "button-ok",
                       "button-enter", "button-clear", "button-back", "button-info", "button-ch-plus",
                       "button-ch-minus",
                       "button-dvdmenu", "button-dvdaudio", "button-dvdsubtitle", "button-cc", "button-pause",
                       "button-play", "button-stop", "button-skipback", "button-skipfwd", "button-rew", "button-fwd",
                       "button-zoom", "button-num-0", "button-num-1", "button-num-2", "button-num-3", "button-num-4",
                       "button-num-5", "button-num-6", "button-num-7", "button-num-8", "button-num-9", "type .",
                       "goto FMRadio", "goto InternetRadio", "goto LiveTV", "goto ManageDisks", "goto MovieLibrary",
                       "goto MorePrograms", "goto MusicAlbums", "goto MusicArtists", "goto MusicSongs", "goto MyMusic",
                       "goto MyPictures", "goto MYTV", "goto MYVideos", "goto PhotoDetails", "goto RecordedTV",
                       "goto RecorderStorageSettings", "goto ScheduledTVRecordings", "goto Slideshow",
                       "goto SlideshowSettings",
                       "goto Start", "goto TVGuide", "goto Visualizations"
                       ]

            wx.StaticText(panel, label="Command: ", pos=(10, 10))
            choice_action = wx.Choice(panel, -1, (10, 30), choices=actions)
            wx.StaticText(panel, label="Device: ", pos=(10, 60))
            mcxCtrl = wx.Choice(panel, -1, (10, 80), choices=Info.prefixList)
            if action in actions:
                choice_action.SetStringSelection(action)
            if str(mcx) in Info.mcxUserList:
                mcxCtrl.SetStringSelection(Info.prefixList[Info.mcxUserList.index(str(mcx))])

            while panel.Affirmed():
                panel.SetResult(
                    actions[choice_action.GetCurrentSelection()],
                    mcxCtrl.GetCurrentSelection()
                )

    class Connect(eg.ActionBase):
        description = ("Force a WMC Controller (re)connect.  Best Used for reconnecting to other pc WMC instances.")

        def __call__(self, mcx=Info.prefixList[0]):
            try:
                self.status = WMCstatus(Info.host, int(Info.port) + int(Info.mcxUserList[Info.prefixList.index(mcx)]),
                                        mcx, self.plugin)
            except socket.error, exc:
                raise self.Exception(exc[1])

        def Configure(self, mcx=Info.prefixList[0]):
            text = self.text
            panel = eg.ConfigPanel(self)

            wx.StaticText(panel, label="Device: ", pos=(10, 10))
            mcxCtrl = wx.Choice(panel, -1, (10, 30), choices=Info.prefixList)
            if str(mcx) in Info.prefixList:
                mcxCtrl.SetStringSelection(mcx)

            while panel.Affirmed():
                panel.SetResult(
                    mcxCtrl.GetStringSelection()
                )

    class GetInfo(eg.ActionBase):

        def __call__(self, object, mcx):
            if str(mcx) in Info.prefixList:
                try:
                    return getattr(self.plugin, mcx + "_" + object)
                except:
                    return None
            else:
                try:
                    return getattr(self.plugin, str(Info.prefixList[Info.mcxUserList.index(str(mcx))]) + "_" + object)
                except:
                    return None

        def Configure(self, object="TrackTime", mcx=0):
            text = self.text
            panel = eg.ConfigPanel(self)

            objects = ["Status", "MediaName", "TrackNumber", "TrackTime", "Volume", "Mute", "Location", "State",
                       "Recording", "Type", "KeyPress"
                       ]

            wx.StaticText(panel, label="Command: ", pos=(10, 10))
            choice_object = wx.Choice(panel, -1, (10, 30), choices=objects)
            wx.StaticText(panel, label="Device: ", pos=(10, 60))
            mcxCtrl = wx.Choice(panel, -1, (10, 80), choices=Info.prefixList)
            if object in objects:
                choice_object.SetStringSelection(object)
            if str(mcx) in Info.mcxUserList:
                mcxCtrl.SetStringSelection(Info.prefixList[Info.mcxUserList.index(str(mcx))])

            while panel.Affirmed():
                panel.SetResult(
                    objects[choice_object.GetCurrentSelection()],
                    mcxCtrl.GetCurrentSelection()
                )


import eg

from ctypes import WinDLL, POINTER, c_void_p, c_int, byref, GetLastError
from ctypes.wintypes import BOOL, HWND, DWORD, HANDLE, LPWSTR

PVOID = c_void_p
LPTSTR = LPWSTR

_WtsApi32 = WinDLL("WtsApi32")

WTSRegisterSessionNotification = _WtsApi32.WTSRegisterSessionNotification
WTSRegisterSessionNotification.restype = BOOL
WTSRegisterSessionNotification.argtypes = [HWND, DWORD]
WTSUserName = 5
WTSFreeMemory = _WtsApi32.WTSFreeMemory
WTSFreeMemory.restype = None
WTSFreeMemory.argtypes = [PVOID]
WTSUnRegisterSessionNotification = _WtsApi32.WTSUnRegisterSessionNotification
WTSUnRegisterSessionNotification.restype = BOOL
WTSUnRegisterSessionNotification.argtypes = [HWND]
WTS_CURRENT_SERVER_HANDLE = 0  # Variable c_void_p
NOTIFY_FOR_ALL_SESSIONS = 1  # Variable c_int

# values for enumeration '_WTS_INFO_CLASS'
WTSInitialProgram = 0
WTSApplicationName = 1
WTSWorkingDirectory = 2
WTSOEMId = 3
WTSSessionId = 4
WTSWinStationName = 6
WTSDomainName = 7
WTSConnectState = 8
WTSClientBuildNumber = 9
WTSClientName = 10
WTSClientDirectory = 11
WTSClientProductId = 12
WTSClientHardwareId = 13
WTSClientAddress = 14
WTSClientDisplay = 15
WTSClientProtocolType = 16
_WTS_INFO_CLASS = c_int  # enum
WTS_INFO_CLASS = _WTS_INFO_CLASS
WTSQuerySessionInformationW = _WtsApi32.WTSQuerySessionInformationW
WTSQuerySessionInformationW.restype = BOOL
WTSQuerySessionInformationW.argtypes = [
    HANDLE, DWORD, WTS_INFO_CLASS, POINTER(LPWSTR), POINTER(DWORD)
]
WTSQuerySessionInformation = WTSQuerySessionInformationW  # alias

WM_WTSSESSION_CHANGE = 0x02B1

WTS_WPARAM_DICT = {
    1: "ConsoleConnect",
    2: "ConsoleDisconnect",
    3: "RemoteConnect",
    4: "RemoteDisconnect",
    5: "SessionLogon",
    6: "SessionLogoff",
    7: "SessionLock",
    8: "SessionUnlock",
    9: "SessionRemoteControl"
}


class SessionChangeNotifier:
    inited = False

    def __init__(self, plugin):
        self.TriggerEvent = plugin.TriggerEvent
        self.retryCount = 0
        eg.messageReceiver.AddHandler(
            WM_WTSSESSION_CHANGE,
            self.OnSessionChange
        )
        eg.scheduler.AddTask(0, self.Register)

    @eg.LogIt
    def Register(self):
        success = WTSRegisterSessionNotification(
            eg.messageReceiver.hwnd,
            NOTIFY_FOR_ALL_SESSIONS
        )
        if success:
            self.inited = True
            return
        errorNum = GetLastError()
        # if we get the error RPC_S_INVALID_BINDING (1702), the system
        # hasn't started all needed services. For this reason we wait some
        # time and try it again.
        if errorNum == 1702:
            self.retryCount += 1
            if self.retryCount > 60:
                # if we tried it to often, give up
                eg.PrintError("WTSRegisterSessionNotification timeout")
                return
            eg.scheduler.AddTask(2.0, self.Register)
            return
        # some other error has happened
        raise SystemError("WTSRegisterSessionNotification", errorNum)

    def Close(self):
        if self.inited:
            WTSUnRegisterSessionNotification(eg.messageReceiver.hwnd)
        eg.messageReceiver.RemoveHandler(
            WM_WTSSESSION_CHANGE,
            self.OnSessionChange
        )

    @eg.LogIt
    def OnSessionChange(self, hwnd, msg, wparam, lparam):
        eventstring = WTS_WPARAM_DICT.get(wparam, None)
        if eventstring is not None:
            pBuffer = LPTSTR()
            bytesReturned = DWORD()
            WTSQuerySessionInformation(
                WTS_CURRENT_SERVER_HANDLE,
                lparam,
                WTSUserName,
                byref(pBuffer),
                byref(bytesReturned)
            )
            userName = pBuffer.value
            WTSFreeMemory(pBuffer)
            if eventstring == "SessionLogon":
                if userName[:3] == "Mcx":
                    try:
                        self.status = WMCstatus(Info.host, int(Info.port) + int(userName[3:5].replace("-", "")),
                                                Info.prefixList[Info.mcxUserList.index(userName[3:5].replace("-", ""))],
                                                Info.pluginREF)
                    except socket.error, exc:
                        raise self.Exception(exc[1])

        return 1
