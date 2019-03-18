# -*- coding: utf-8 -*-
#
# plugins/Samsung TV Network Control/__init__.py
# 
# This file is a plugin for EventGhost.
# Copyright (C) 2012 Guy Moreau <gmyx -at- gmpws.ca>
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
#
# Samsung Samsung TV Network Control
# ================
# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
# 
# Structure taken from SamsungTV PlugIn 
# Control code taken from {insert url here when I get it} 
# 
# Possible Future Items:
# * Ping the supplied IP / port (to be tested if this does anything)
# * Bind button on configure screen (to trigger the TV's allow / deny screen)
# * Detect all available IPs and MAC addresses
# * Make TV model a drop down with avialable models

help = """\
Plugin to control Samsung TV via it's Network interface. Your Samsung TV must have this function enabled and connected to the network."""

import eg

eg.RegisterPlugin(
    name="Samsung TV Network Control",
    guid='{2098C4C1-2D8B-4D87-8736-5F8C8B535E32}',
    author="Guy Moreau (gmyx)",
    version="0.1",
    kind="external",
    description="Control Samsung TV via it's Network interface",
    url="http://www.eventghost.net/forum/viewtopic.php?f=9&t={TBD}",
    help=help,
    canMultiLoad=False,
    createMacrosOnAdd=True,
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABGdBTUEAALGPC/xhBQAA"
        "AAd0SU1FB9YDBAsPCqtpoiUAAAAWdEVYdFNvZnR3YXJlAFBhaW50Lk5FVCAyLjZsqHS1"
        "AAADe0lEQVQ4T02TXVCUZRSAPyZsxpnqoovum+miq+6qFUJYQP7cogS2VpGFAAlKpyAC"
        "EVh+4k80WGADQWlxZRfZACH5ECVY5TdHiEbAIQVkHRzUCZK/ZWGXp10SxjPzXrzvvM9z"
        "zpw5xwUQXg7ndX1jw3VkYmrzycK/gusrgrB3z17hvXfffv2tN99YcXHEi///g07Bznkw"
        "+9i1yvAbqvJKolRJhJ2KQp4ZQWTWd5wsV9Ni6sWybn3tZWYXvjt531V1tgJF8lcEZbij"
        "MLgRbTpAVHcgyk5/QnSefHrmc7QdV1hbX9+VbAvuTk67ZpfVIDsWgu/ZfURfD+TElVBy"
        "m4+TooshvDaAL697EPOHLzK1L9prbayuWbYlwsLzFZfCql+Qx8XhqfoAZUsIhsEGLGsW"
        "Nm12FlZtTM0/w2DSEmn0dEgclRSFcFG8wcamTRAqtO0kpRficdQLpV5Gr7mf3qFHzC1u"
        "YF61MvrIztD0OsP3F6m/ZUDZ7klosxfxJZn0j04hpJ+uIvZ4EpJvJKhvFWOzW1lc2qT/"
        "zznuzdnoGnlG+8BDWnvMDE7M8q1eQcygN6GFkWj0nQgp+WUcilTyUaIHzRPtWKx2rLYt"
        "5hfXHBnMNIjDtHbfY3RmmcdLdkrEfKIHDyDLPYS6vhnhh9wSgiPCcYvbT+3gNQbGluib"
        "WOTG8EOaTGOY/nrKwPgynXdm+H3gCZkNeQ6BP0GnZGgMRoTUnDMcSfgaiUJKWuPP6MRx"
        "LhjvUN3Qh671NnVNQ1y9Oe2YgUmaeqY4WnMEpSgl5ORhzhmaEFRFpSTnOpool+GXFoa6"
        "sQNNXReVupucv9zHeWM3Gl0HNY0mci7VEtF2EJ+8fSTkpSP23EaYmpl1ySgowk8ehiTc"
        "i6iiExRcNKC+0IlG20m5XqRCK5J9qYxoMZSgail+scEUn6vn+bJFImxtbQkl5dWoCkvx"
        "Cg3k/Uh3grKCSahJJln3E8n1BSQ2JhArHuSTUgneET6kFWno6h3GyW5P4sqqRUhMLSCn"
        "uJQA+cdIFYF8GC3F/Xs3vDM8kaZ4sP+YD/4RX5B+Wk1l3SXnkG2zu7uwZrHuqa1rILuw"
        "hNSsfOSxsQQoPkN2WI4iPp7EzBx+dPRLb7zK0orl1Z2FEmwvTM4HZ0kzZvM7hqZfMbaJ"
        "jEw8YHh8kvrGFmr1euaf/iPZAW12uzD2t1n4DwtSpLoLWTYZAAAAAElFTkSuQmCC"
    ),
)

import socket
import base64
from netbios import *
import re

# insert command structure here as notes

# Known Key Codes
# Allow for a custom KEY_
# mlKeys = list()
cmdKEYs = (
    "KEY_1",
    "KEY_2",
    "{Custom}",
    "KEY_MENU",
    "KEY_UP",
    "KEY_DOWN",
    "KEY_LEFT",
    "KEY_RIGHT",
    "KEY_3",
    "KEY_VOLUP",
    "KEY_4",
    "KEY_5",
    "KEY_6",
    "KEY_VOLDOWN",
    "KEY_7",
    "KEY_8",
    "KEY_9",
    "KEY_MUTE",
    "KEY_CHDOWN",
    "KEY_0",
    "KEY_CHUP",
    "KEY_PRECH",
    "KEY_GREEN",
    "KEY_YELLOW",
    "KEY_CYAN",
    "KEY_ADDDEL",
    "KEY_SOURCE",
    "KEY_INFO",
    "KEY_PIP_ONOFF",
    "KEY_PIP_SWAP",
    "KEY_PLUS100",
    "KEY_CAPTION",
    "KEY_PMODE",
    "KEY_TTX_MIX",
    "KEY_TV",
    "KEY_PICTURE_SIZE",
    "KEY_AD",
    "KEY_PIP_SIZE",
    "KEY_MAGIC_CHANNEL",
    "KEY_PIP_SCAN",
    "KEY_PIP_CHUP",
    "KEY_PIP_CHDOWN",
    "KEY_DEVICE_CONNECT",
    "KEY_HELP",
    "KEY_ANTENA",
    "KEY_CONVERGENCE",
    "KEY_11",
    "KEY_12",
    "KEY_AUTO_PROGRAM",
    "KEY_FACTORY",
    "KEY_3SPEED",
    "KEY_RSURF",
    "KEY_ASPECT",
    "KEY_TOPMENU",
    "KEY_GAME",
    "KEY_QUICK_REPLAY",
    "KEY_STILL_PICTURE",
    "KEY_DTV",
    "KEY_FAVCH",
    "KEY_REWIND",
    "KEY_STOP",
    "KEY_PLAY",
    "KEY_FF",
    "KEY_REC",
    "KEY_PAUSE",
    "KEY_TOOLS",
    "KEY_INSTANT_REPLAY",
    "KEY_LINK",
    "KEY_FF_",
    "KEY_GUIDE",
    "KEY_REWIND_",
    "KEY_ANGLE",
    "KEY_RESERVED1",
    "KEY_ZOOM1",
    "KEY_PROGRAM",
    "KEY_BOOKMARK",
    "KEY_DISC_MENU",
    "KEY_PRINT",
    "KEY_RETURN",
    "KEY_SUB_TITLE",
    "KEY_CLEAR",
    "KEY_VCHIP",
    "KEY_REPEAT",
    "KEY_DOOR",
    "KEY_OPEN",
    "KEY_WHEEL_LEFT",
    "KEY_POWER",
    "KEY_SLEEP",
    "KEY_2",
    "KEY_DMA",
    "KEY_TURBO",
    "KEY_1",
    "KEY_FM_RADIO",
    "KEY_DVR_MENU",
    "KEY_MTS",
    "KEY_PCMODE",
    "KEY_TTX_SUBFACE",
    "KEY_CH_LIST",
    "KEY_RED",
    "KEY_DNIe",
    "KEY_SRS",
    "KEY_CONVERT_AUDIO_MAINSUB",
    "KEY_MDC",
    "KEY_SEFFECT",
    "KEY_DVR",
    "KEY_DTV_SIGNAL",
    "KEY_LIVE",
    "KEY_PERPECT_FOCUS",
    "KEY_HOME",
    "KEY_ESAVING",
    "KEY_WHEEL_RIGHT",
    "KEY_CONTENTS",
    "KEY_VCR_MODE",
    "KEY_CATV_MODE",
    "KEY_DSS_MODE",
    "KEY_TV_MODE",
    "KEY_DVD_MODE",
    "KEY_STB_MODE",
    "KEY_CALLER_ID",
    "KEY_SCALE",
    "KEY_ZOOM_MOVE",
    "KEY_CLOCK_DISPLAY",
    "KEY_AV1",
    "KEY_SVIDEO1",
    "KEY_COMPONENT1",
    "KEY_SETUP_CLOCK_TIMER",
    "KEY_COMPONENT2",
    "KEY_MAGIC_BRIGHT",
    "KEY_DVI",
    "KEY_HDMI",
    "KEY_W_LINK",
    "KEY_DTV_LINK",
    "KEY_APP_LIST",
    "KEY_BACK_MHP",
    "KEY_ALT_MHP",
    "KEY_DNSe",
    "KEY_RSS",
    "KEY_ENTERTAINMENT",
    "KEY_ID_INPUT",
    "KEY_ID_SETUP",
    "KEY_ANYNET",
    "KEY_POWEROFF",
    "KEY_POWERON",
    "KEY_ANYVIEW",
    "KEY_MS",
    "KEY_MORE",
    "KEY_PANNEL_POWER",
    "KEY_PANNEL_CHUP",
    "KEY_PANNEL_CHDOWN",
    "KEY_PANNEL_VOLUP",
    "KEY_PANNEL_VOLDOW",
    "KEY_PANNEL_ENTER",
    "KEY_PANNEL_MENU",
    "KEY_PANNEL_SOURCE",
    "KEY_AV2",
    "KEY_AV3",
    "KEY_SVIDEO2",
    "KEY_SVIDEO3",
    "KEY_ZOOM2",
    "KEY_PANORAMA",
    "KEY_4_3",
    "KEY_16_9",
    "KEY_DYNAMIC",
    "KEY_STANDARD",
    "KEY_MOVIE1",
    "KEY_CUSTOM",
    "KEY_AUTO_ARC_RESET",
    "KEY_AUTO_ARC_LNA_ON",
    "KEY_AUTO_ARC_LNA_OFF",
    "KEY_AUTO_ARC_ANYNET_MODE_OK",
    "KEY_AUTO_ARC_ANYNET_AUTO_START",
    "KEY_AUTO_FORMAT",
    "KEY_DNET",
    "KEY_HDMI1",
    "KEY_AUTO_ARC_CAPTION_ON",
    "KEY_AUTO_ARC_CAPTION_OFF",
    "KEY_AUTO_ARC_PIP_DOUBLE",
    "KEY_AUTO_ARC_PIP_LARGE",
    "KEY_AUTO_ARC_PIP_SMALL",
    "KEY_AUTO_ARC_PIP_WIDE",
    "KEY_AUTO_ARC_PIP_LEFT_TOP",
    "KEY_AUTO_ARC_PIP_RIGHT_TOP",
    "KEY_AUTO_ARC_PIP_LEFT_BOTTOM",
    "KEY_AUTO_ARC_PIP_RIGHT_BOTTOM",
    "KEY_AUTO_ARC_PIP_CH_CHANGE",
    "KEY_AUTO_ARC_AUTOCOLOR_SUCCESS",
    "KEY_AUTO_ARC_AUTOCOLOR_FAIL",
    "KEY_AUTO_ARC_C_FORCE_AGING",
    "KEY_AUTO_ARC_USBJACK_INSPECT",
    "KEY_AUTO_ARC_JACK_IDENT",
    "KEY_NINE_SEPERATE",
    "KEY_ZOOM_IN",
    "KEY_ZOOM_OUT",
    "KEY_MIC",
    "KEY_HDMI2",
    "KEY_HDMI3",
    "KEY_AUTO_ARC_CAPTION_KOR",
    "KEY_AUTO_ARC_CAPTION_ENG",
    "KEY_AUTO_ARC_PIP_SOURCE_CHANGE",
    "KEY_HDMI4",
    "KEY_AUTO_ARC_ANTENNA_AIR",
    "KEY_AUTO_ARC_ANTENNA_CABLE",
    "KEY_AUTO_ARC_ANTENNA_SATELLITE",
    "KEY_EXT1",
    "KEY_EXT2",
    "KEY_EXT3",
    "KEY_EXT4",
    "KEY_EXT5",
    "KEY_EXT6",
    "KEY_EXT7",
    "KEY_EXT8",
    "KEY_EXT9",
    "KEY_EXT10",
    "KEY_EXT11",
    "KEY_EXT12",
    "KEY_EXT13",
    "KEY_EXT14",
    "KEY_EXT15",
    "KEY_EXT16",
    "KEY_EXT17",
    "KEY_EXT18",
    "KEY_EXT19",
    "KEY_EXT20",
    "KEY_EXT21",
    "KEY_EXT22",
    "KEY_EXT23",
    "KEY_EXT24",
    "KEY_EXT25",
    "KEY_EXT26",
    "KEY_EXT27",
    "KEY_EXT28",
    "KEY_EXT29",
    "KEY_EXT30",
    "KEY_EXT31",
    "KEY_EXT32",
    "KEY_EXT33",
    "KEY_EXT34",
    "KEY_EXT35",
    "KEY_EXT36",
    "KEY_EXT37",
    "KEY_EXT38",
    "KEY_EXT39",
    "KEY_EXT40",
    "KEY_EXT41"
)

# fixed global vars
gsAppString = "iphone..iapp.samsung"  # What the iPhone app reports - I don't know if this matters much


# helper class
class GetMac:
    def GetMac(self):
        # Code taken from: http://groups.google.com/group/comp.lang.python/msg/fd2e7437d72c1c21
        # code ported from "HOWTO: Get the MAC Address for an Ethernet Adapter"
        # MS KB ID: Q118623
        lOut = ""
        print "GetMac"
        ncb = NCB()
        ncb.Command = NCBENUM
        la_enum = LANA_ENUM()
        ncb.Buffer = la_enum
        rc = Netbios(ncb)
        if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)
        for i in range(la_enum.length):
            ncb.Reset()
            ncb.Command = NCBRESET
            ncb.Lana_num = ord(la_enum.lana[i])
            rc = Netbios(ncb)
            if rc != 0: raise RuntimeError, "Unexpected result %d" % (rc,)

            ncb.Reset()
            ncb.Command = NCBASTAT
            ncb.Lana_num = ord(la_enum.lana[i])
            ncb.Callname = "*               "
            adapter = ADAPTER_STATUS()
            ncb.Buffer = adapter
            Netbios(ncb)
            print "Adapter address:",
            for ch in adapter.adapter_address:
                lOut = lOut + "%02x" % (ord(ch),) + "-"
            lOut = re.findall(r".*(?=-)", lOut)[0]
            print lOut
            return lOut


# the one and only action
class SendCommand(eg.ActionWithStringParameter):
    name = 'Send Command'

    def __call__(self, msCommand, msCustom):
        print "Sendign command: " + msCommand + msCustom

        # encode as base 64
        encodedIP = base64.b64encode(self.plugin.msPCIP)
        encodedMAC = base64.b64encode(self.plugin.msPCMAC)
        encodedRemoteName = base64.b64encode(self.plugin.msRemoteName)

        messagepart1 = chr(100) + chr(0) + chr(len(encodedIP)) + chr(0) + encodedIP + chr(len(encodedMAC)) + chr(
            0) + encodedMAC + chr(len(encodedRemoteName)) + chr(0) + encodedRemoteName
        part1 = chr(0) + chr(len(gsAppString)) + chr(0) + gsAppString + chr(len(messagepart1)) + chr(0) + messagepart1

        messagepart2 = chr(200) + chr(0);
        part2 = chr(0) + chr(len(gsAppString)) + chr(0) + gsAppString + chr(len(messagepart2)) + chr(0) + messagepart2

        # Send remote key
        if msCommand == "{Custom}":
            key = msCustom
        else:
            key = msCommand

        print key

        encodedKey = base64.b64encode(key)
        messagepart3 = chr(0) + chr(0) + chr(0) + chr(len(encodedKey)) + chr(0) + encodedKey
        tvappstring = "iphone." + self.plugin.msTV + ".iapp.samsung"
        part3 = chr(0) + chr(len(tvappstring)) + chr(0) + tvappstring + chr(len(messagepart3)) + chr(0) + messagepart3

        # open socket and send
        lSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print self.plugin.msTVport
        print int(self.plugin.msTVport)
        lSocket.connect((self.plugin.msTVIP, int(self.plugin.msTVport)))
        lSocket.sendall(part1)
        lSocket.sendall(part2)
        lSocket.sendall(part3)
        lData = lSocket.recv(65535)
        lSocket.close()
        print 'Received', repr(lData)

    def cmdCommand_click(self, event):
        """get the selected color choice"""
        # if {custom} selected, activate the text box else deactive it
        if self.cmdCommand.GetStringSelection() <> "{Custom}":
            self.txtCustom.Disable()
        else:
            self.txtCustom.Enable()

    def Configure(self, msCommand="", msCustomCode=""):
        panel = eg.ConfigPanel()
        # cmdCommand of the available KEY Codes
        self.cmdCommand = wx.Choice(
            panel,
            -1,
            choices=sorted(cmdKEYs)
        )
        panel.AddLine("Command:", self.cmdCommand)
        self.cmdCommand.SetStringSelection(msCommand)
        # event handler for the choice box click
        self.cmdCommand.Bind(wx.EVT_CHOICE, self.cmdCommand_click)
        # txtCustomCode
        self.txtCustom = wx.TextCtrl(panel, -1, msCustomCode)
        panel.AddLine("Custom Code:", self.txtCustom)
        # check if test box needs to be disabled
        if msCommand <> "{Custom}":
            self.txtCustom.Disable()
        while panel.Affirmed():
            panel.SetResult(self.cmdCommand.GetStringSelection(), self.txtCustom.GetValue())


class SamsungTVNetworkControl(eg.PluginBase):
    def __init__(self):
        print "Samsung TV Network Control is inited."

        # for lsKey, liID in cmdKEYs:
        #  mlKeys.append(lsKey)
        self.AddAction(SendCommand)

    def __start__(self, asTVIP, asTVPort, asPCIP, asPCMAC, asTV, asRemoteName):
        self.msTVIP = asTVIP
        self.msTVport = asTVPort
        self.msPCIP = asPCIP
        self.msPCMAC = asPCMAC
        self.msTV = asTV
        self.msRemoteName = asRemoteName

    def Configure(self, msTVIP="", msTVport="55000", \
                  msPCIP=socket.gethostbyname(socket.gethostname()), \
                  msPCMac=GetMac().GetMac(), msTV="",
                  msRemoteName="EventGhost Samsung Remote"):
        panel = eg.ConfigPanel()
        # txtTVIP: TV's IP Address
        txtTVIP = wx.TextCtrl(panel, -1, msTVIP)
        panel.AddLine("IP:", txtTVIP)
        # txtTVport: TV's Port Address, should be 55000
        txtTVport = wx.TextCtrl(panel, -1, msTVport)
        panel.AddLine("Port:", txtTVport)
        # txtPCIP: This computer's IP Address
        txtPCIP = wx.TextCtrl(panel, -1, msPCIP)
        panel.AddLine("PC IP:", txtPCIP)
        # txtPCMAC: This computer's IP Address
        txtPCMAC = wx.TextCtrl(panel, -1, msPCMac)
        panel.AddLine("PC MAC:", txtPCMAC)
        # txtTV: This is the TV's Model Number
        txtTV = wx.TextCtrl(panel, -1, msTV)
        panel.AddLine("TV Model Name:", txtTV)
        # txtRemoteName: This is the name shown on the TV when pairing
        txtRemoteName = wx.TextCtrl(panel, -1, msRemoteName)
        panel.AddLine("Pairing with TV Name:", txtRemoteName)
        while panel.Affirmed():
            panel.SetResult(txtTVIP.GetValue(), txtTVport.GetValue(), \
                            txtPCIP.GetValue(), txtPCMAC.GetValue(), \
                            txtTV.GetValue(), txtRemoteName.GetValue())
