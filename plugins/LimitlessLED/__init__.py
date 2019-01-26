# Change Log --- CURRENT VERSION 1.4.0

# ==================\
# 1.4.0 - 2015/11/25\
# ==================\
# Features:
# - The user is now able to optionally specify the global variable they'd like to use for the VARIABLE COMMAND option.
#
# Added:
# - Added an icon! :)
#
# Changed:
# - Some ConfigPanels have been updated; this is part of a larger wxPython project I am working on.
#
# Bugfixes:
# - Fixed a small number of notify-errors.
# ==================\

# ==================\
# 1.3.1 - 2015/11/18\
# ==================\
# Added:
# - Version checker will initialize on every startup and notify the user if an update is necessary.
#
# Bugfixes:
# - There is now a maximum brightness of 100% on all lights commands.
# ==================\

# ==================\
# 1.3.0 - 2015/10/31\
# ==================\
# Features:
# - Added NAME GROUPS Action
# = You can now name your groups in a human-friendly way.
#
# - Added SHOW GROUPS STATUS Action
# = You can now view the theoretical status of your groups.
# 
# - Added VARIABLE COMMAND Action
# = You can now perform any action based on an EventGhost payload.
# ==================\

# ==================\
# 1.2.2 - 2015/10/24\
# ==================\
# Bugfixes:
# - Commands can be edited properly now.
# ==================\

# ==================\
# 1.2.1 - 2015/09/14\
# ==================\
# Bugfixes:
# - Groups will now brighten and darken correctly if group1 is dark, and only one group is on.
#
# ***DEV SPECIFIC CHANGES***
# - FILLER GROUP BV changed from 000 to 999.
# ==================\

# ==================\
# 1.2.0 - 2015/08/16\
# ==================\
# Features:
# - All actions are named appropriately and can be re-configured now.
#
# Optimization:
# - All commands are slightly faster (likely unnoticable), but have more built-in redundancy.
# - Cleaned up some UI elements from showing if they didn't need to be (controls for groups 5 - 8 if no second bridge present)
#
# Removed:
# - UI elements that are now-defunct like the "RESET GROUPS" button and all such associations.
#
# ***DEV SPECIFIC CHANGES***
# - Full code is now ~150 lines shorter.
# = Cleaned up "IF WHITE" condition to only be 2-4 lines
# = Removed defunct UI elements
# ==================\

# ==================\
# 1.1.1 - 2015/08/13\
# ==================\
# Added:
# - All actions are named appropriately and can be re-configured now.
#
# Bugfixes:
# - Lights will now properly dim or brighten if two complementary commands are sent back-to-back.

# ==================\
# 1.1.0 - 2015/08/12\
# ==================\
# Features:
# - Added DIMMER Action
# == You can now set brightness levels directly, or step up/down by a level (includes a 2x multiplier) 
#
# Bugfixes:
# - Lights will now turn off correctly if some lights are WHITE and some are COLOR. BV of 0 was not recorded for WHITE; causing lights which were OFF to ON->DIM->OFF if "ALL OFF" command was run.
#
# Optimization:
# - Fine tuned TURN ON commands to work in most cases for bridges connected via WiFi (Commands were being sent to bridge too frequently with FOR LOOP, dumbed it down so RF could catch up)
# == Bulbs should turn on correctly the first time, color+brightness
#
# Added:
# - version indicator in CONFIG PANEL
#
# ***DEV SPECIFIC CHANGES*** 
# - all relevant commands now adhere to the logic: "IF all GROUP BV/CV values are equal, then use the broadcast option (255.255.255.255), otherwise, use the rotate method."
# == See fn "CheckIfSame", supports BV or CV as these are set to arg "iterator", while the list itself is the second argument. Call the function result, return logic boolean.

# ==================\
# 1.0.0 - 2015/07/21\
# ==================\
# Initial Release!
# Features:
# - Up to 2 bridges, up to 9 total groups (8 individual, 1 for ALL) .. all features herein support any configuration of all/specific groups
# - ON @ specific brightness, specific color
# - OFF
# - All tertiary colors in RGB color pie!

# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

"""<rst>
**Notice:**
This plugin supports LimitlessLED / MiLight bulbs.

The goal of this plugin is to give the user complete control and customization over their LED RGBW bulbs. The plugin
supports up to two bridges, for a maximum of eight (nine, if you count the "broadcast all" option) groupings of
lights which should give even large homes good control over their investment.
"""

import eg

eg.RegisterPlugin(
    name="LimitlessLED",
    author="SupahNoob",
    version="1.4.0",
    kind="external",
    description=__doc__,
    url="https://www.reddit.com/message/compose/?to=SupahNoob",
    icon=(
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAABGdBTUEAALGPC/xhBQAA"
        "ACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAC1lBMVEVb"
        "hQFahQFahQFahQFahQFahQFahQFahQFahQFahQFbhQFahQFahQFahQFahQFahQFahQFa"
        "hQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFbhQJbhQFa"
        "hQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFahQFbhgJbhgJahQFa"
        "hQFahQFahQFahQFahQFZhAFYhAFZhAFahQFahQFahQFahQFahQFbhQJZhABahQFahQFb"
        "hgNbhgNbhgNZhANgiQNjiwJfiAFbhgRchgRchgRchgNchgRchgReiAhYgwBYgwBTgABU"
        "gABRfgBpkABvlQBpkAB2mQFWggBQfgBRfwBSfwBRfgBSfwCnvntjjBBkjBGEpEN6nDia"
        "tEuguUmKqU1njh52mQCbtVeNq1WRrleOq1KSrliNq1GZtGKkvHGZtGKWsV+btWCrwV96"
        "nTN2mjCctlOfuECswX2kvHWrwX2ov3irwX6nvndgiQBiiwBjjABgigBiiwB5nABylgB3"
        "mgB/oABpkAJeiABhigBgigBgigBgigBgiQB0mQRzmANzmAN0mANymAN4nAN8nwJ6nQJy"
        "lwJxlwF0mQNzmAJzmAN0mAN0mANzmAN+oAJ9oAF+oAF9oAF+oAF8nwF8nwF8nwF+oAF+"
        "oAF9oAF+oAF+oAF9oAF+oAF9oAGJqQKJqQGJqQGJqQGJqQGJqQGJqQGJqQGJqQGJqQGJ"
        "qQGJqQGJqQGJqQGJqQGIqQGTsQKTsQGTsQGTsQGTsQGTsQGTsQGTsQGTsQGTsQGTsQGT"
        "sQGTsQGTsQGTsQGSsQGeuQKduQGduQGduQGduQGduQGduQGduQGduQGduQGduQGduQGd"
        "uQGduQGduQGduQGnwAOnwAKnwAKnwAKnwAKnwAKnwAKmwAKmwAKmwAKmvwGmwAKmwAGm"
        "wAGmwAGlvwL////eOiK1AAAAAWJLR0TxQr/fwgAAAAd0SU1FB98LEwQtOBXhh5cAAAEZ"
        "SURBVBjTY2BgZGJmYWVjB2MOTi4Gbh5ePn4BQSEwFhYRZRATl5CUkpaRBWM5eQUGRSVl"
        "FVU1dQ1NLW0dXT19AwZDI2MTUzNzC0sraxtbO3sHBkcnZxdXN3cPTy9vH18//wCGwKDg"
        "kNCw8IjIqOiY2Lj4BIbEpOSU1LT0jMys7JzcvPwChsKi4pLSsvKKyqrqmtq6+gaGxqbm"
        "lta29o7Oru6e3r7+CQwTJ02eMnXa9BkzZ82eM3fe/AUMCxctXrJ02fIVK1etXrN23foN"
        "DBs3bd6yddv2HTt37d6zd9/+AwwHDx0+cvTY8RMnT50+c/bc+QsMFy9dvnL12vUbN2/d"
        "vnP33v0HDA8fPX7y9NnzFy9fvX7z9t37DwCIInHsRYJMPAAAACV0RVh0ZGF0ZTpjcmVh"
        "dGUAMjAxNS0xMS0xOVQwNDo0NTo1NiswMTowMNxtWOcAAAAldEVYdGRhdGU6bW9kaWZ5"
        "ADIwMTUtMTEtMTlUMDQ6NDU6NTYrMDE6MDCtMOBbAAAAAElFTkSuQmCC"
    ),
)

import socket
import os
import os.path
import wx
import time
import binascii
import random
import copy
import re
import sys
import requests
from threading import Thread


def versiontuple(v):
    return tuple(map(int, (v.split("."))))


def CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl, group5Ctrl,
                     group6Ctrl, group7Ctrl, group8Ctrl):
    printgroups = []
    specifygroups = []

    if groupallCtrl == True:
        specifygroups = "\x42\x00\x55"

    if groupspecifyCtrl == True:
        if group1Ctrl or group5Ctrl == True:
            specifygroups.append("\x45\x00\x55")  # == self.plugin.groupsONcode[1]
            if group1Ctrl == True:
                printgroups.append(1)
            if group5Ctrl == True:
                printgroups.append(5)
        if group2Ctrl or group6Ctrl == True:
            specifygroups.append("\x47\x00\x55")  # == self.plugin.groupsONcode[2]
            if group2Ctrl == True:
                printgroups.append(2)
            if group6Ctrl == True:
                printgroups.append(6)
        if group3Ctrl or group7Ctrl == True:
            specifygroups.append("\x49\x00\x55")  # == self.plugin.groupsONcode[3]
            if group3Ctrl == True:
                printgroups.append(3)
            if group7Ctrl == True:
                printgroups.append(7)
        if group4Ctrl or group8Ctrl == True:
            specifygroups.append("\x4B\x00\x55")  # == self.plugin.groupsONcode[4]
            if group4Ctrl == True:
                printgroups.append(4)
            if group8Ctrl == True:
                printgroups.append(8)

    printgroups.sort()
    return (specifygroups, printgroups)


def CreateBrightnessCode(brightness):
    brightness = int(brightness * .27)
    if brightness < 2:
        brightness = 2

    b = str(format(78, '02x'))
    b += str(format(brightness, '02x'))
    b += str(format(85, '02x'))

    brightnessCode = binascii.unhexlify(b)
    return brightnessCode


def CheckIfSame(iterator, list_items):
    if (list_items.count(iterator) == (len(list_items) - 1)):
        return True
    else:
        return False


class LimitlessLED(eg.PluginBase):
    def UpgradePlugin(self):
        re_version = re.compile(ur'<em>v([^\"]+)</em>')
        eg_post = 'http://www.eventghost.org/forum/viewtopic.php?f=9&t=7311&sid=d40efb73fbd7aa654cbaf01af88a32cc'
        r = requests.get(eg_post)
        remoteVersion = re_version.search(r.text)
        if not remoteVersion:
            print "Could not retrieve available version."
            return
        remoteVersion = remoteVersion.groups(1)[0]

        if versiontuple(self.info.version) >= versiontuple(remoteVersion):
            print "LimitlessLED Plugin is up to date!"
        else:
            print "There is a new version (v" + remoteVersion + ") of this plugin available!"
            print "Please copy and paste the link below into your browser."
            print eg_post
            print "Once downloaded and replaced, please restart EventGhost."

    def __init__(self):
        Thread(target=self.UpgradePlugin).start()

        self.ip = "255.255.255.255"  # This is the IP of the bridge, default is 255.255.255.255 (all bridges).
        self.ip2 = ""  # This is the IP of a second bridge, if you have more than 4 groups to use.
        self.port = 8899  # This is the port that the bridge operates on, default is 8899.

        self.AddAction(ShowLightsStatus)
        self.AddAction(NameGroups)
        self.AddAction(TurnOn)
        self.AddAction(TurnOff)
        self.AddAction(Dimmer)  # Action "Dim/Brighten lights"
        self.AddAction(SetColor)
        self.AddAction(
            VariableCMD)  # Action Influence group and/or brightness and/or color value based on a global EG variable.

        # These values are recorded globally more for record keeping purposes than anything else
        self.specifygroups = []  # this is where we will actually define the groups we want to have an effect on.

        self.groupnames = [
            'FILLER',
            '*NOT SET*',
            '*NOT SET*',
            '*NOT SET*',
            '*NOT SET*',
            '*NOT SET*',
            '*NOT SET*',
            '*NOT SET*',
            '*NOT SET*',
        ]

        self.groupsBV = [
            999,  # FILLER group
            00,  # group 1
            00,  # group 2
            00,  # group 3
            00,  # group 4
            00,  # group 5
            00,  # group 6
            00,  # group 7
            00,  # group 8
        ]

        self.groupsCV = [
            "FILLER",  # FILLER group
            "Color",  # group 1
            "Color",  # group 2
            "Color",  # group 3
            "Color",  # group 4
            "Color",  # group 5
            "Color",  # group 6
            "Color",  # group 7
            "Color",  # group 8
        ]

        self.groupsWhiteCode = (
            "\xC2\x00\x55",  # all groups
            "\xC5\x00\x55",  # group 1 or 5
            "\xC7\x00\x55",  # group 2 or 6
            "\xC9\x00\x55",  # group 3 or 7
            "\xCB\x00\x55",  # group 4 or 8
        )

        self.color = (
            ("White"),
            ("Cyan"),
            ("Azure"),
            ("Blue"),
            ("Violet"),
            ("Magenta"),
            ("Rose"),
            ("Red"),
            ("Orange"),
            ("Yellow"),
            ("Chartreuse"),
            ("Green"),
            ("Spring Green"),
        )

        self.colorCodes = (
            ("\xC2\x00\x55"),  # White
            ("\x40\x35\x55"),  # Cyan
            ("\x40\x20\x55"),  # Azure
            ("\x40\xFF\x55"),  # Blue
            ("\x40\xF0\x55"),  # Violet
            ("\x40\xD0\x55"),  # Magenta
            ("\x40\xB5\x55"),  # Rose
            ("\x40\xB1\x55"),  # Red
            ("\x40\xA0\x55"),  # Orange
            ("\x40\x80\x55"),  # Yellow
            ("\x40\x72\x55"),  # Chartreuse
            ("\x40\x62\x55"),  # Green
            ("\x40\x51\x55"),  # Spring Green
        )

        self.groupsONcode = (
            ("\x42\x00\x55"),  # all groups
            ("\x45\x00\x55"),  # group 1 or 5
            ("\x47\x00\x55"),  # group 2 or 6
            ("\x49\x00\x55"),  # group 3 or 7
            ("\x4B\x00\x55"),  # group 4 or 8
        )

        self.groupsOFFcode = (
            ("\x41\x00\x55"),  # all groups
            ("\x46\x00\x55"),  # group 1 or 5
            ("\x48\x00\x55"),  # group 2 or 6
            ("\x4A\x00\x55"),  # group 3 or 7
            ("\x4C\x00\x55"),  # group 4 or 8
        )

    def Configure(self, ip=0, ip2=0, port=0, secondBridge=0):
        ip = self.ip
        ip2 = self.ip2
        port = self.port

        panel = eg.ConfigPanel()
        ipCtrl = wx.TextCtrl(panel, value=ip, name="IP Control: ")
        portCtrl = panel.SpinIntCtrl(port, min=1, max=65535)
        # Displays a box that ONLY registers an INTEGER for Port Number (important!!!)
        secondBridge = panel.CheckBox(0, "I have a second bridge ")
        secondBridgeCtrl = panel.TextCtrl(ip2)

        ipCtrl_label = panel.StaticText('IP Address: ')
        ip2Ctrl_label = panel.StaticText('IP Address: ')

        if ip2 == "":
            secondBridgeCtrl.Enable(False)
        else:
            secondBridgeCtrl.Enable(True)
            secondBridge.SetValue(True)

        plg_title = panel.StaticText('Please define the IP address and port number that your WiFi Bridge operates on.')

        if ip == '':
            ipCtrl_text = panel.StaticText('Please set the IP Address of the bridge (DEFAULT VALUE = 255.255.255.255).')
        elif ip == '255.255.255.255':
            ipCtrl_text = panel.StaticText(
                'This is the IP address that broadcasts commands to all bridges on your WiFi.')
        else:
            ipCtrl_text = panel.StaticText('This is the IP address of the bridge.')

        # wx.LAYOUT options
        ipBorder = wx.StaticBox(panel, -1)
        ipBox = wx.StaticBoxSizer(ipBorder, wx.VERTICAL)
        ipLayout = wx.BoxSizer(wx.HORIZONTAL)
        ipLayout.AddMany([
            (ipCtrl_label, 0, wx.ALIGN_CENTER),
            (ipCtrl, 0, wx.ALIGN_CENTER)
        ])
        ipBox.AddMany([
            (ipCtrl_text, 1, wx.ALIGN_CENTER_HORIZONTAL),
            (ipLayout, 1, wx.ALIGN_CENTER_HORIZONTAL)
        ])

        ip2Border = wx.StaticBox(panel, -1)
        ip2Box = wx.StaticBoxSizer(ip2Border, wx.VERTICAL)
        ip2Layout = wx.BoxSizer(wx.HORIZONTAL)
        ip2Layout.AddMany([
            (ip2Ctrl_label, 0, wx.ALIGN_CENTER),
            (secondBridgeCtrl, 0, wx.ALIGN_CENTER)
        ])
        ip2Box.AddMany([
            (secondBridge, 1, wx.ALIGN_CENTER),
            (ip2Layout, 1, wx.ALIGN_CENTER_HORIZONTAL)
        ])

        if port == '':
            portCtrl_text = panel.StaticText('Please set Port Number of the bridge (DEFAULT VALUE = 8899).')
        elif ip == 8899:
            portCtrl_text = panel.StaticText('This is the default port number.')
        else:
            portCtrl_text = panel.StaticText('This is the Port Number of the bridge.')

        portCtrl_label = panel.StaticText('Port Number: ')

        # wx.LAYOUT options
        portBorder = wx.StaticBox(panel, -1)
        portBox = wx.StaticBoxSizer(portBorder, wx.VERTICAL)
        portLayout = wx.BoxSizer(wx.HORIZONTAL)
        portLayout.AddMany([
            (portCtrl_label, 0, wx.ALIGN_CENTER),
            (portCtrl, 0, wx.ALIGN_CENTER)
        ])
        portBox.AddMany([
            (portCtrl_text, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (portLayout, 0, wx.ALIGN_CENTER_HORIZONTAL)
        ])

        panel.sizer.Add(plg_title, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.sizer.Add(ipBox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.sizer.Add(portBox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.sizer.Add(ip2Box, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM)

        def OnCheckBox(event):
            flag = secondBridge.GetValue()
            secondBridgeCtrl.Enable(flag)

        secondBridge.Bind(wx.EVT_CHECKBOX, OnCheckBox)

        while panel.Affirmed():  # This bit is mandatory, it is what helps to save/store/cancel the values
            panel.SetResult(  # the user sets on initial plugin configuration
                ipCtrl.GetValue(),
                secondBridgeCtrl.GetValue(),
                portCtrl.GetValue(),
                secondBridge.GetValue()
            )

    def __start__(self, ip, ip2, port, secondBridge):
        self.ip = ip
        self.ip2 = ip2
        self.port = port
        if secondBridge == 0:
            self.ip2 = ""

        print u''
        print "IP Address of Bridge 1: ", self.ip
        if self.ip2 == "":
            pass
        else:
            print "IP Address of Bridge 2: ", self.ip2
        print "Port: ", self.port


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class ShowLightsStatus(eg.ActionBase):
    name = "Lights Status"
    description = "Show the theoretical status of your lights!"

    def GetLabel(self):
        return "Lights Status: Execute to see names!"

    def __call__(self):
        for x in xrange(0, 9):
            if self.plugin.groupnames[x] == "*NOT SET*":
                continue
            print ''
            if x == 0:
                continue
            elif x < 5:
                print "Group Name: " + str(self.plugin.groupnames[x])
                print "Brightness Level: " + str(self.plugin.groupsBV[x]) + "       Color: " + str(
                    self.plugin.groupsCV[x])
            elif x > 4 and self.plugin.ip2 != "":
                print "Group Name: " + str(self.plugin.groupnames[x])
                print "Brightness Level: " + str(self.plugin.groupsBV[x]) + "       Color: " + str(
                    self.plugin.groupsCV[x])


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class NameGroups(eg.ActionBase):
    name = "Name Groups"
    description = "Enter your group names!"

    def Configure(self, one=1, two=2, three=3, four=4, five=5, six=6, seven=7, eight=8):
        panel = eg.ConfigPanel(self)

        one = self.plugin.groupnames[1]
        two = self.plugin.groupnames[2]
        three = self.plugin.groupnames[3]
        four = self.plugin.groupnames[4]
        five = self.plugin.groupnames[5]
        six = self.plugin.groupnames[6]
        seven = self.plugin.groupnames[7]
        eight = self.plugin.groupnames[8]

        group1Name = panel.TextCtrl(one)
        group2Name = panel.TextCtrl(two)
        group3Name = panel.TextCtrl(three)
        group4Name = panel.TextCtrl(four)
        group5Name = panel.TextCtrl(five)
        group6Name = panel.TextCtrl(six)
        group7Name = panel.TextCtrl(seven)
        group8Name = panel.TextCtrl(eight)

        if self.plugin.ip2 == "":
            group5Name.Show(False)
            group6Name.Show(False)
            group7Name.Show(False)
            group8Name.Show(False)

        panel.AddLine(u'', u'For changes to go through, you must press "TEST" button.')
        panel.AddLine(
            u'Use normal-language, one-word identifiers like "Bedroom" or "Living" (instead of "Living Room").')

        if self.plugin.ip2 == "":
            panel.AddLine(u'')
            panel.AddLine(u'Group 1: ', group1Name, 'Group 3: ', group3Name)
            panel.AddLine(u'Group 2: ', group2Name, 'Group 4: ', group4Name)
        else:
            panel.AddLine(u'Group 1: ', group1Name, 'Group 5: ', group5Name)
            panel.AddLine(u'Group 2: ', group2Name, 'Group 6: ', group6Name)
            panel.AddLine(u'Group 3: ', group3Name, 'Group 7: ', group7Name)
            panel.AddLine(u'Group 4: ', group4Name, 'Group 8: ', group8Name)

        while panel.Affirmed():
            panel.SetResult(
                group1Name.GetValue(),
                group2Name.GetValue(),
                group3Name.GetValue(),
                group4Name.GetValue(),
                group5Name.GetValue(),
                group6Name.GetValue(),
                group7Name.GetValue(),
                group8Name.GetValue(),
            )

    def GetLabel(self, one, two, three, four, five, six, seven, eight):
        return "GROUP NAMES: Execute to see names!"

    def __call__(self, one, two, three, four, five, six, seven, eight):
        self.plugin.groupnames[1] = one
        self.plugin.groupnames[2] = two
        self.plugin.groupnames[3] = three
        self.plugin.groupnames[4] = four
        self.plugin.groupnames[5] = five
        self.plugin.groupnames[6] = six
        self.plugin.groupnames[7] = seven
        self.plugin.groupnames[8] = eight

        print "Below are your group names, associated to their numbers."

        for x in xrange(0, 9):
            if x == 0:
                continue
            elif x < 5:
                print "Group " + str(x) + ": " + str(self.plugin.groupnames[x])
            elif x > 4 and self.plugin.ip2 != "":
                print "Group " + str(x) + ": " + str(self.plugin.groupnames[x])


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class TurnOn(eg.ActionBase):
    name = "Turn Lights ON"
    description = "Turn the light group(s) ON"

    def Configure(self, brightness=100, color=0, *args):
        del self.plugin.specifygroups[:]

        panel = eg.ConfigPanel(self)
        groupallCtrl = panel.RadioButton(-1, " ALL GROUPS")
        groupspecifyCtrl = panel.RadioButton(0, " SPECIFY GROUPS")
        group1Ctrl = panel.CheckBox(-1, " 1")
        group2Ctrl = panel.CheckBox(-1, " 2")
        group3Ctrl = panel.CheckBox(-1, " 3")
        group4Ctrl = panel.CheckBox(-1, " 4")
        group5Ctrl = panel.CheckBox(-1, " 5")
        group6Ctrl = panel.CheckBox(-1, " 6")
        group7Ctrl = panel.CheckBox(-1, " 7")
        group8Ctrl = panel.CheckBox(-1, " 8")
        brightnessCtrl = panel.SpinIntCtrl(brightness, min=1, max=100)
        colorCtrl = panel.Choice(color, self.plugin.color)

        group1Ctrl.Enable(False)
        group2Ctrl.Enable(False)
        group3Ctrl.Enable(False)
        group4Ctrl.Enable(False)
        group5Ctrl.Enable(False)
        group6Ctrl.Enable(False)
        group7Ctrl.Enable(False)
        group8Ctrl.Enable(False)

        if self.plugin.ip2 == "":
            group5Ctrl.SetValue(False)
            group6Ctrl.SetValue(False)
            group7Ctrl.SetValue(False)
            group8Ctrl.SetValue(False)
            group5Ctrl.Show(False)
            group6Ctrl.Show(False)
            group7Ctrl.Show(False)
            group8Ctrl.Show(False)

        def OnSpecifyRadioButton(event):
            all_state = groupallCtrl.GetValue()
            specify_state = groupspecifyCtrl.GetValue()
            if specify_state == True:
                group1Ctrl.SetValue(False)
                group2Ctrl.SetValue(False)
                group3Ctrl.SetValue(False)
                group4Ctrl.SetValue(False)
                group5Ctrl.SetValue(False)
                group6Ctrl.SetValue(False)
                group7Ctrl.SetValue(False)
                group8Ctrl.SetValue(False)
                group1Ctrl.Enable(True)
                group2Ctrl.Enable(True)
                group3Ctrl.Enable(True)
                group4Ctrl.Enable(True)
                if self.plugin.ip2 != "":
                    group5Ctrl.Enable(True)
                    group6Ctrl.Enable(True)
                    group7Ctrl.Enable(True)
                    group8Ctrl.Enable(True)
            if all_state == True:
                group1Ctrl.SetValue(True)
                group2Ctrl.SetValue(True)
                group3Ctrl.SetValue(True)
                group4Ctrl.SetValue(True)
                group1Ctrl.Enable(False)
                group2Ctrl.Enable(False)
                group3Ctrl.Enable(False)
                group4Ctrl.Enable(False)
                if self.plugin.ip2 != "":
                    group5Ctrl.SetValue(True)
                    group6Ctrl.SetValue(True)
                    group7Ctrl.SetValue(True)
                    group8Ctrl.SetValue(True)
                    group5Ctrl.Enable(False)
                    group6Ctrl.Enable(False)
                    group7Ctrl.Enable(False)
                    group8Ctrl.Enable(False)

        groupallCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)
        groupspecifyCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)

        panel.AddLine(u'')
        panel.AddLine(u'Select group(s):', groupallCtrl, u'          ', groupspecifyCtrl)
        panel.AddLine(u'', u'', u'', group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl)
        panel.AddLine(u'', u'', u'', group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl)
        panel.AddLine(u'Brightness (1 - 100%):', brightnessCtrl)
        panel.AddLine(u'')
        panel.AddLine(u'Select a Color:', colorCtrl)

        while panel.Affirmed():
            panel.SetResult(
                brightnessCtrl.GetValue(),
                colorCtrl.GetValue(),
                groupallCtrl.GetValue(),
                groupspecifyCtrl.GetValue(),
                group1Ctrl.GetValue(),
                group2Ctrl.GetValue(),
                group3Ctrl.GetValue(),
                group4Ctrl.GetValue(),
                group5Ctrl.GetValue(),
                group6Ctrl.GetValue(),
                group7Ctrl.GetValue(),
                group8Ctrl.GetValue(),
            )

    def GetLabel(self, brightness, color, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl,
                 group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl):
        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)
        if groupallCtrl:
            return "Turn [ALL] ON in " + str(self.plugin.color[color]) + " at " + str(brightness) + "%"
        elif not groupallCtrl:
            return "Turn " + str(printgroups) + " ON in " + str(self.plugin.color[color]) + " at " + str(
                brightness) + "%"

    def __call__(self, brightness, color, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl,
                 group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl):
        ip = self.plugin.ip
        ip2 = self.plugin.ip2
        port = self.plugin.port

        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)
        brightnessCode = CreateBrightnessCode(brightness)

        print "=== Values Set ==="
        if groupallCtrl == True:
            print "Group(s): ALL"
        else:
            print "Group(s): ", printgroups
        print "Brightness: " + str(brightness) + "%"
        print "Color: ", self.plugin.color[color]
        print "=== Values Set ==="

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if groupallCtrl:
            for c in xrange(0, 3):
                sock.sendto(specifygroups, ("255.255.255.255", port))
                time.sleep(.1)
                if self.plugin.color[color] == "White":
                    sock.sendto(self.plugin.groupsWhiteCode[0], ("255.255.255.255", port))
                    time.sleep(.1)
                else:
                    sock.sendto(self.plugin.colorCodes[color], ("255.255.255.255", port))
                    time.sleep(.1)
                sock.sendto(brightnessCode, ("255.255.255.255", port))
                if c == 0:
                    time.sleep(.2)
                    for y in xrange(0, 9):
                        if y == 0:
                            continue
                        else:
                            self.plugin.groupsBV[y] = brightness
                            self.plugin.groupsCV[y] = self.plugin.color[color]
                elif c == 1:
                    time.sleep(.3)

        else:
            for x in printgroups:
                if x < 5:
                    ipval = ip
                    if x == 1:
                        y = 1
                    if x == 2:
                        y = 2
                    if x == 3:
                        y = 3
                    if x == 4:
                        y = 4
                else:
                    ipval = ip2
                    if x == 5:
                        y = 1
                    if x == 6:
                        y = 2
                    if x == 7:
                        y = 3
                    if x == 8:
                        y = 4

                self.plugin.groupsBV[x] = brightness
                self.plugin.groupsCV[x] = self.plugin.color[color]

                for c in xrange(0, 3):
                    sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                    time.sleep(.05)
                    if self.plugin.color[color] == "White":
                        sock.sendto(self.plugin.groupsWhiteCode[y], (ipval, port))
                        time.sleep(.05)
                    else:
                        sock.sendto(self.plugin.colorCodes[color], (ipval, port))
                        time.sleep(.05)
                    sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                    time.sleep(.05)
                    sock.sendto(brightnessCode, (ipval, port))
                    time.sleep(.05)


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class TurnOff(eg.ActionBase):
    name = "Turn Lights OFF"
    description = "Turn the light group(s) OFF"

    def Configure(self, *args):
        del self.plugin.specifygroups[:]

        panel = eg.ConfigPanel(self)
        groupallCtrl = panel.RadioButton(-1, " ALL GROUPS")
        groupspecifyCtrl = panel.RadioButton(0, " SPECIFY GROUPS")
        group1Ctrl = panel.CheckBox(-1, " 1")
        group2Ctrl = panel.CheckBox(-1, " 2")
        group3Ctrl = panel.CheckBox(-1, " 3")
        group4Ctrl = panel.CheckBox(-1, " 4")
        group5Ctrl = panel.CheckBox(-1, " 5")
        group6Ctrl = panel.CheckBox(-1, " 6")
        group7Ctrl = panel.CheckBox(-1, " 7")
        group8Ctrl = panel.CheckBox(-1, " 8")

        group1Ctrl.Enable(False)
        group2Ctrl.Enable(False)
        group3Ctrl.Enable(False)
        group4Ctrl.Enable(False)
        group5Ctrl.Enable(False)
        group6Ctrl.Enable(False)
        group7Ctrl.Enable(False)
        group8Ctrl.Enable(False)

        if self.plugin.ip2 == "":
            group5Ctrl.SetValue(False)
            group6Ctrl.SetValue(False)
            group7Ctrl.SetValue(False)
            group8Ctrl.SetValue(False)
            group5Ctrl.Show(False)
            group6Ctrl.Show(False)
            group7Ctrl.Show(False)
            group8Ctrl.Show(False)

        def OnSpecifyRadioButton(event):
            all_state = groupallCtrl.GetValue()
            specify_state = groupspecifyCtrl.GetValue()
            if specify_state == True:
                group1Ctrl.SetValue(False)
                group2Ctrl.SetValue(False)
                group3Ctrl.SetValue(False)
                group4Ctrl.SetValue(False)
                group5Ctrl.SetValue(False)
                group6Ctrl.SetValue(False)
                group7Ctrl.SetValue(False)
                group8Ctrl.SetValue(False)
                group1Ctrl.Enable(True)
                group2Ctrl.Enable(True)
                group3Ctrl.Enable(True)
                group4Ctrl.Enable(True)
                if self.plugin.ip2 != "":
                    group5Ctrl.Enable(True)
                    group6Ctrl.Enable(True)
                    group7Ctrl.Enable(True)
                    group8Ctrl.Enable(True)
            if all_state == True:
                group1Ctrl.SetValue(True)
                group2Ctrl.SetValue(True)
                group3Ctrl.SetValue(True)
                group4Ctrl.SetValue(True)
                group1Ctrl.Enable(False)
                group2Ctrl.Enable(False)
                group3Ctrl.Enable(False)
                group4Ctrl.Enable(False)
                if self.plugin.ip2 != "":
                    group5Ctrl.SetValue(True)
                    group6Ctrl.SetValue(True)
                    group7Ctrl.SetValue(True)
                    group8Ctrl.SetValue(True)
                    group5Ctrl.Enable(False)
                    group6Ctrl.Enable(False)
                    group7Ctrl.Enable(False)
                    group8Ctrl.Enable(False)

        groupallCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)
        groupspecifyCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)

        panel.AddLine(u'')
        panel.AddLine(u'Select group(s):', groupallCtrl, u'          ', groupspecifyCtrl)
        panel.AddLine(u'')
        panel.AddLine(u'')
        panel.AddLine(u'', u'', u'', group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl)
        panel.AddLine(u'')
        panel.AddLine(u'', u'', u'', group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl)

        while panel.Affirmed():
            panel.SetResult(
                groupallCtrl.GetValue(),
                groupspecifyCtrl.GetValue(),
                group1Ctrl.GetValue(),
                group2Ctrl.GetValue(),
                group3Ctrl.GetValue(),
                group4Ctrl.GetValue(),
                group5Ctrl.GetValue(),
                group6Ctrl.GetValue(),
                group7Ctrl.GetValue(),
                group8Ctrl.GetValue(),
            )

    def GetLabel(self, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl, group5Ctrl,
                 group6Ctrl, group7Ctrl, group8Ctrl):
        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)
        if groupallCtrl:
            return "Turn [ALL] OFF"
        elif not groupallCtrl:
            return "Turn " + str(printgroups) + " OFF"

    def __call__(self, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl, group5Ctrl,
                 group6Ctrl, group7Ctrl, group8Ctrl):
        ip = self.plugin.ip
        ip2 = self.plugin.ip2
        port = self.plugin.port

        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)

        print "=== Values Set ==="
        if groupallCtrl == True:
            print "Turning off ALL groups."
        else:
            print "Group(s) turning OFF: ", printgroups
        print "=== Values Set ==="

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if groupallCtrl and CheckIfSame(self.plugin.groupsBV[1], self.plugin.groupsBV):
            brightness = self.plugin.groupsBV[1]
            for i in xrange(brightness, -1, -2):
                brightness = i
                brightnessCode = CreateBrightnessCode(brightness)

                if brightness < 6:
                    for c in xrange(0, 2):
                        time.sleep(0.5)
                        sock.sendto(self.plugin.groupsOFFcode[0], ("255.255.255.255", port))

                    for x in xrange(0, 9):
                        if x == 0:
                            continue
                        self.plugin.groupsBV[x] = 0
                else:
                    sock.sendto(self.plugin.groupsONcode[0], ("255.255.255.255", port))
                    time.sleep(.015)
                    sock.sendto(brightnessCode, ("255.255.255.255", port))

        else:
            if groupallCtrl == True:
                printgroups = [1, 2, 3, 4, 5, 6, 7, 8]

            for n in printgroups:
                if self.plugin.groupsBV[
                    n] == 0:  # Essentially, "Don't waste your resources if the bulb is already recorded to be in the OFF state"
                    continue

                if n < 5:
                    ipval = ip
                    if n == 1:
                        y = 1
                    if n == 2:
                        y = 2
                    if n == 3:
                        y = 3
                    if n == 4:
                        y = 4
                else:
                    ipval = ip2
                    if n == 5:
                        y = 1
                    if n == 6:
                        y = 2
                    if n == 7:
                        y = 3
                    if n == 8:
                        y = 4

                brightness = self.plugin.groupsBV[n]  # Grab brightness level of bulb.
                for i in xrange(brightness, -1,
                                -2):  # Decrement by 1 (lines 714-716 & 724-727), until it is 0, then set it off (lines 718-720). Set the final value of the bulb (line 721).
                    brightness = i
                    brightnessCode = CreateBrightnessCode(brightness)

                    if brightness < 6:
                        for c in xrange(0, 2):
                            time.sleep(.05)
                            sock.sendto(self.plugin.groupsOFFcode[y], (ipval, port))
                        self.plugin.groupsBV[n] = 0
                        break
                    else:
                        sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                        time.sleep(.015)
                        sock.sendto(brightnessCode, (ipval, port))


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class Dimmer(eg.ActionBase):
    name = "Dimmer"
    description = "Set a specific brightness, or step up / down in increments."

    def Configure(self, brightness=100, *args):
        del self.plugin.specifygroups[:]

        panel = eg.ConfigPanel(self)
        groupallCtrl = panel.RadioButton(-1, " ALL GROUPS")
        groupspecifyCtrl = panel.RadioButton(0, " SPECIFY GROUPS")
        group1Ctrl = panel.CheckBox(-1, " 1")
        group2Ctrl = panel.CheckBox(-1, " 2")
        group3Ctrl = panel.CheckBox(-1, " 3")
        group4Ctrl = panel.CheckBox(-1, " 4")
        group5Ctrl = panel.CheckBox(-1, " 5")
        group6Ctrl = panel.CheckBox(-1, " 6")
        group7Ctrl = panel.CheckBox(-1, " 7")
        group8Ctrl = panel.CheckBox(-1, " 8")
        brightnessCtrl = panel.SpinIntCtrl(brightness, min=1, max=100)
        specifyCtrl = panel.CheckBox(-1, "")
        upCtrl = panel.CheckBox(0, " Up")
        downCtrl = panel.CheckBox(0, " Dn")
        stepCtrl = panel.SpinIntCtrl(1, min=1, max=2)

        group1Ctrl.Enable(False)
        group2Ctrl.Enable(False)
        group3Ctrl.Enable(False)
        group4Ctrl.Enable(False)
        group5Ctrl.Enable(False)
        group6Ctrl.Enable(False)
        group7Ctrl.Enable(False)
        group8Ctrl.Enable(False)
        upCtrl.Enable(False)
        downCtrl.Enable(False)
        stepCtrl.Enable(False)

        if self.plugin.ip2 == "":
            group5Ctrl.SetValue(False)
            group6Ctrl.SetValue(False)
            group7Ctrl.SetValue(False)
            group8Ctrl.SetValue(False)
            group5Ctrl.Show(False)
            group6Ctrl.Show(False)
            group7Ctrl.Show(False)
            group8Ctrl.Show(False)

        def OnSpecifyRadioButton(event):
            all_state = groupallCtrl.GetValue()
            specify_state = groupspecifyCtrl.GetValue()
            if specify_state == True:
                group1Ctrl.SetValue(False)
                group2Ctrl.SetValue(False)
                group3Ctrl.SetValue(False)
                group4Ctrl.SetValue(False)
                group5Ctrl.SetValue(False)
                group6Ctrl.SetValue(False)
                group7Ctrl.SetValue(False)
                group8Ctrl.SetValue(False)
                group1Ctrl.Enable(True)
                group2Ctrl.Enable(True)
                group3Ctrl.Enable(True)
                group4Ctrl.Enable(True)
                if self.plugin.ip2 != "":
                    group5Ctrl.Enable(True)
                    group6Ctrl.Enable(True)
                    group7Ctrl.Enable(True)
                    group8Ctrl.Enable(True)
            if all_state == True:
                group1Ctrl.SetValue(True)
                group2Ctrl.SetValue(True)
                group3Ctrl.SetValue(True)
                group4Ctrl.SetValue(True)
                group1Ctrl.Enable(False)
                group2Ctrl.Enable(False)
                group3Ctrl.Enable(False)
                group4Ctrl.Enable(False)
                if self.plugin.ip2 != "":
                    group5Ctrl.SetValue(True)
                    group6Ctrl.SetValue(True)
                    group7Ctrl.SetValue(True)
                    group8Ctrl.SetValue(True)
                    group5Ctrl.Enable(False)
                    group6Ctrl.Enable(False)
                    group7Ctrl.Enable(False)
                    group8Ctrl.Enable(False)

        def OnBrightnessButton(event):
            specific_state = specifyCtrl.GetValue()
            up_state = upCtrl.GetValue()
            down_state = downCtrl.GetValue()
            if specific_state == True:
                upCtrl.SetValue(False)
                upCtrl.Enable(False)
                downCtrl.SetValue(False)
                downCtrl.Enable(False)
                stepCtrl.Enable(False)
                brightnessCtrl.Enable(True)
            else:
                brightnessCtrl.Enable(False)
                upCtrl.Enable(True)
                downCtrl.Enable(True)
                stepCtrl.Enable(True)

        def StepUpBox(event):
            up_state = upCtrl.GetValue()
            down_state = downCtrl.GetValue()
            if up_state == True:
                downCtrl.SetValue(False)
                upCtrl.SetValue(True)

        def StepDownBox(event):
            up_state = upCtrl.GetValue()
            down_state = downCtrl.GetValue()
            if down_state == True:
                upCtrl.SetValue(False)
                downCtrl.SetValue(True)

        groupallCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)
        groupspecifyCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)
        specifyCtrl.Bind(wx.EVT_CHECKBOX, OnBrightnessButton)
        upCtrl.Bind(wx.EVT_CHECKBOX, StepUpBox)
        downCtrl.Bind(wx.EVT_CHECKBOX, StepDownBox)

        panel.AddLine(u'')
        panel.AddLine(u'Select group(s):', groupallCtrl, u'          ', groupspecifyCtrl)
        panel.AddLine(u'', u'', u'', group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl)
        panel.AddLine(u'', u'', u'', group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl)
        panel.AddLine(u'')
        panel.AddLine(u'        Set brightness?', specifyCtrl, brightnessCtrl, u'', u'', u'2x Step = 2')
        panel.AddLine(u'', u'Step Brightness?', upCtrl, downCtrl, u'       ', stepCtrl)

        while panel.Affirmed():
            panel.SetResult(
                brightnessCtrl.GetValue(),
                groupallCtrl.GetValue(),
                groupspecifyCtrl.GetValue(),
                group1Ctrl.GetValue(),
                group2Ctrl.GetValue(),
                group3Ctrl.GetValue(),
                group4Ctrl.GetValue(),
                group5Ctrl.GetValue(),
                group6Ctrl.GetValue(),
                group7Ctrl.GetValue(),
                group8Ctrl.GetValue(),
                stepCtrl.GetValue(),
                upCtrl.GetValue(),
                downCtrl.GetValue(),
            )

    def GetLabel(self, brightness, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl,
                 group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl, step, upCtrl, downCtrl):
        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)
        if upCtrl:
            if groupallCtrl:
                return "Brighten [ALL] by " + str(15 * step) + "%"
            elif not groupallCtrl:
                return "Brighten " + str(printgroups) + " by " + str(15 * step) + "%"
        elif downCtrl:
            if groupallCtrl:
                return "Dim [ALL] by " + str(15 * step) + "%"
            elif not groupallCtrl:
                return "Dim " + str(printgroups) + " by " + str(15 * step) + "%"
        else:
            if groupallCtrl:
                return "Set [ALL] to " + str(brightness) + "%"
            elif not groupallCtrl:
                return "Set " + str(printgroups) + " to " + str(brightness) + "%"

    def __call__(self, brightness, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl,
                 group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl, step, upCtrl, downCtrl):
        ip = self.plugin.ip
        ip2 = self.plugin.ip2
        port = self.plugin.port

        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)

        for c in xrange(0, 3):
            print ""
        print "=== Values Set ==="
        if groupallCtrl == True:
            print "Group(s): ALL"
        else:
            print "Group(s): ", printgroups

        if upCtrl == True:
            print "The lights are getting brighter.."
        elif downCtrl == True:
            print "The lights are getting dimmer.."
        else:
            print "Brightness: " + str(brightness) + "%"
        print "=== Values Set ==="
        for c in xrange(0, 3):
            print ""

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if groupallCtrl and CheckIfSame(self.plugin.groupsBV[1], self.plugin.groupsBV):
            getBrightness = self.plugin.groupsBV[1]
            if upCtrl:
                brightness = getBrightness + (15 * step)
                if brightness > 100:
                    print "..but wait! It can't get any brighter!"
                    return
                brightnessCode = CreateBrightnessCode(brightness)
            elif downCtrl:
                brightness = getBrightness - (15 * step)
                if brightness < 10:
                    print "..but wait! It can't get any dimmer!"
                    return
                brightnessCode = CreateBrightnessCode(brightness)
            else:
                brightnessCode = CreateBrightnessCode(brightness)

            for c in xrange(0, 3):
                sock.sendto(specifygroups, ("255.255.255.255", port))
                time.sleep(.1)
                sock.sendto(brightnessCode, ("255.255.255.255", port))
                time.sleep(.1)

            for x in xrange(0, 9):
                if x == 0:
                    continue
                else:
                    self.plugin.groupsBV[x] = brightness

        elif groupallCtrl and not CheckIfSame(self.plugin.groupsBV[1], self.plugin.groupsBV):
            for x in xrange(0, 9):
                if x == 0:
                    continue
                else:
                    if upCtrl:
                        getBrightness = self.plugin.groupsBV[x]
                        if getBrightness == 0:
                            continue
                        elif getBrightness == 100:
                            continue
                        else:
                            brightness = getBrightness + (15 * step)
                            if brightness > 100:
                                brightness = 100
                            brightnessCode = CreateBrightnessCode(brightness)
                    elif downCtrl:
                        getBrightness = self.plugin.groupsBV[x]
                        if getBrightness == 0:
                            continue
                        brightness = getBrightness - (15 * step)
                        if brightness < 10:
                            brightness = 10
                        brightnessCode = CreateBrightnessCode(brightness)
                    else:
                        brightnessCode = CreateBrightnessCode(brightness)

                    if x < 5:
                        ipval = ip
                        if x == 1:
                            y = 1
                        if x == 2:
                            y = 2
                        if x == 3:
                            y = 3
                        if x == 4:
                            y = 4
                    else:
                        ipval = ip2
                        if x == 5:
                            y = 1
                        if x == 6:
                            y = 2
                        if x == 7:
                            y = 3
                        if x == 8:
                            y = 4

                    self.plugin.groupsBV[x] = brightness

                    for c in xrange(0, 3):
                        sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                        time.sleep(.05)
                        sock.sendto(brightnessCode, (ipval, port))
                        time.sleep(.05)

        # if select group...
        else:
            for x in printgroups:
                if upCtrl:
                    getBrightness = self.plugin.groupsBV[x]
                    if getBrightness == 100:
                        continue
                    else:
                        brightness = getBrightness + (15 * step)
                        if brightness > 100:
                            brightness = 100
                        brightnessCode = CreateBrightnessCode(brightness)
                elif downCtrl:
                    getBrightness = self.plugin.groupsBV[x]
                    if getBrightness == 0:
                        continue
                    else:
                        brightness = getBrightness - (15 * step)
                        if brightness < 10:
                            brightness = 10
                        brightnessCode = CreateBrightnessCode(brightness)
                else:
                    brightnessCode = CreateBrightnessCode(brightness)

                if x < 5:
                    ipval = ip
                    if x == 1:
                        y = 1
                    if x == 2:
                        y = 2
                    if x == 3:
                        y = 3
                    if x == 4:
                        y = 4
                else:
                    ipval = ip2
                    if x == 5:
                        y = 1
                    if x == 6:
                        y = 2
                    if x == 7:
                        y = 3
                    if x == 8:
                        y = 4

                self.plugin.groupsBV[x] = brightness

                for c in xrange(0, 3):
                    sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                    time.sleep(.05)
                    sock.sendto(brightnessCode, (ipval, port))
                    time.sleep(.05)


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class SetColor(eg.ActionBase):
    name = "Set Color"
    description = "Set a specific color."

    def Configure(self, color=0, *args):
        del self.plugin.specifygroups[:]

        panel = eg.ConfigPanel(self)
        groupallCtrl = panel.RadioButton(-1, " ALL GROUPS")
        groupspecifyCtrl = panel.RadioButton(0, " SPECIFY GROUPS")
        group1Ctrl = panel.CheckBox(-1, " 1")
        group2Ctrl = panel.CheckBox(-1, " 2")
        group3Ctrl = panel.CheckBox(-1, " 3")
        group4Ctrl = panel.CheckBox(-1, " 4")
        group5Ctrl = panel.CheckBox(-1, " 5")
        group6Ctrl = panel.CheckBox(-1, " 6")
        group7Ctrl = panel.CheckBox(-1, " 7")
        group8Ctrl = panel.CheckBox(-1, " 8")
        colorCtrl = panel.Choice(color, self.plugin.color)

        group1Ctrl.Enable(False)
        group2Ctrl.Enable(False)
        group3Ctrl.Enable(False)
        group4Ctrl.Enable(False)
        group5Ctrl.Enable(False)
        group6Ctrl.Enable(False)
        group7Ctrl.Enable(False)
        group8Ctrl.Enable(False)

        if self.plugin.ip2 == "":
            group5Ctrl.SetValue(False)
            group6Ctrl.SetValue(False)
            group7Ctrl.SetValue(False)
            group8Ctrl.SetValue(False)
            group5Ctrl.Show(False)
            group6Ctrl.Show(False)
            group7Ctrl.Show(False)
            group8Ctrl.Show(False)

        def OnSpecifyRadioButton(event):
            all_state = groupallCtrl.GetValue()
            specify_state = groupspecifyCtrl.GetValue()
            if specify_state == True:
                group1Ctrl.SetValue(False)
                group2Ctrl.SetValue(False)
                group3Ctrl.SetValue(False)
                group4Ctrl.SetValue(False)
                group5Ctrl.SetValue(False)
                group6Ctrl.SetValue(False)
                group7Ctrl.SetValue(False)
                group8Ctrl.SetValue(False)
                group1Ctrl.Enable(True)
                group2Ctrl.Enable(True)
                group3Ctrl.Enable(True)
                group4Ctrl.Enable(True)
                if self.plugin.ip2 != "":
                    group5Ctrl.Enable(True)
                    group6Ctrl.Enable(True)
                    group7Ctrl.Enable(True)
                    group8Ctrl.Enable(True)
            if all_state == True:
                group1Ctrl.SetValue(True)
                group2Ctrl.SetValue(True)
                group3Ctrl.SetValue(True)
                group4Ctrl.SetValue(True)
                group1Ctrl.Enable(False)
                group2Ctrl.Enable(False)
                group3Ctrl.Enable(False)
                group4Ctrl.Enable(False)
                if self.plugin.ip2 != "":
                    group5Ctrl.SetValue(True)
                    group6Ctrl.SetValue(True)
                    group7Ctrl.SetValue(True)
                    group8Ctrl.SetValue(True)
                    group5Ctrl.Enable(False)
                    group6Ctrl.Enable(False)
                    group7Ctrl.Enable(False)
                    group8Ctrl.Enable(False)

        groupallCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)
        groupspecifyCtrl.Bind(wx.EVT_RADIOBUTTON, OnSpecifyRadioButton)

        panel.AddLine(u'')
        panel.AddLine(u'Select group(s):', groupallCtrl, u'          ', groupspecifyCtrl)
        panel.AddLine(u'', u'', u'', group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl)
        panel.AddLine(u'', u'', u'', group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl)
        panel.AddLine(u'')
        panel.AddLine(u'', u'        Set Color?', colorCtrl)

        while panel.Affirmed():
            panel.SetResult(
                colorCtrl.GetValue(),
                groupallCtrl.GetValue(),
                groupspecifyCtrl.GetValue(),
                group1Ctrl.GetValue(),
                group2Ctrl.GetValue(),
                group3Ctrl.GetValue(),
                group4Ctrl.GetValue(),
                group5Ctrl.GetValue(),
                group6Ctrl.GetValue(),
                group7Ctrl.GetValue(),
                group8Ctrl.GetValue(),
            )

    def GetLabel(self, color, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl,
                 group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl):
        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)
        if groupallCtrl:
            return "Set the color of [ALL] to " + str(self.plugin.color[color])
        elif not groupallCtrl:
            return "Set the color of " + str(printgroups) + " to " + str(self.plugin.color[color])

    def __call__(self, color, groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl, group3Ctrl, group4Ctrl,
                 group5Ctrl, group6Ctrl, group7Ctrl, group8Ctrl):
        ip = self.plugin.ip
        ip2 = self.plugin.ip2
        port = self.plugin.port
        groupsWhiteCode = self.plugin.groupsWhiteCode

        specifygroups, printgroups = CreateGroupCodes(groupallCtrl, groupspecifyCtrl, group1Ctrl, group2Ctrl,
                                                      group3Ctrl, group4Ctrl, group5Ctrl, group6Ctrl, group7Ctrl,
                                                      group8Ctrl)

        for c in xrange(0, 3):
            print ""
        print "=== Values Set ==="
        if groupallCtrl == True:
            print "Group(s): ALL"
        else:
            print "Group(s): ", printgroups

        if groupallCtrl:
            print "All groups turned to " + str(self.plugin.color[color])
        elif not groupallCtrl:
            print "Groups " + str(printgroups) + " turned to " + str(self.plugin.color[color])
        print "=== Values Set ==="
        for c in xrange(0, 3):
            print ""

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        if groupallCtrl:
            if CheckIfSame(self.plugin.groupsBV[1], self.plugin.groupsBV):
                if self.plugin.groupsBV[1] == 0:
                    print "But the lights are off!"
                    return
                elif self.plugin.groupsBV[1] > 0:
                    for c in xrange(0, 3):
                        sock.sendto(specifygroups, ("255.255.255.255", port))
                        time.sleep(.1)
                        if self.plugin.color[color] == "White":
                            sock.sendto(groupsWhiteCode[0], ("255.255.255.255", port))
                            time.sleep(.1)
                        else:
                            sock.sendto(self.plugin.colorCodes[color], ("255.255.255.255", port))
                            time.sleep(.1)

                        if c == 0:
                            for x in xrange(0, 9):
                                if x == 0:
                                    continue
                                else:
                                    self.plugin.groupsCV[x] = self.plugin.color[color]

            else:
                for x in xrange(0, 9):
                    if x == 0:
                        continue
                    else:
                        if self.plugin.groupsBV[x] == 0:
                            continue
                        else:
                            if x < 5:
                                ipval = ip
                                if x == 1:
                                    y = 1
                                if x == 2:
                                    y = 2
                                if x == 3:
                                    y = 3
                                if x == 4:
                                    y = 4
                            else:
                                ipval = ip2
                                if x == 5:
                                    y = 1
                                if x == 6:
                                    y = 2
                                if x == 7:
                                    y = 3
                                if x == 8:
                                    y = 4

                            self.plugin.groupsCV[x] = self.plugin.color[color]

                            for c in xrange(0, 3):
                                sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                                time.sleep(.1)
                                if self.plugin.color[color] == "White":
                                    sock.sendto(self.plugin.groupsWhiteCode[y], (ipval, port))
                                    time.sleep(.1)
                                else:
                                    sock.sendto(self.plugin.colorCodes[color], (ipval, port))
                                    time.sleep(.1)

        # if select group...
        else:
            for x in printgroups:
                if self.plugin.groupsBV[x] == 0:
                    continue
                else:
                    if x < 5:
                        ipval = ip
                        if x == 1:
                            y = 1
                        if x == 2:
                            y = 2
                        if x == 3:
                            y = 3
                        if x == 4:
                            y = 4
                    else:
                        ipval = ip2
                        if x == 5:
                            y = 1
                        if x == 6:
                            y = 2
                        if x == 7:
                            y = 3
                        if x == 8:
                            y = 4

                    self.plugin.groupsCV[x] = self.plugin.color[color]

                    for c in xrange(0, 3):
                        sock.sendto(self.plugin.groupsONcode[y], (ipval, port))
                        time.sleep(.1)
                        if self.plugin.color[color] == "White":
                            sock.sendto(self.plugin.groupsWhiteCode[y], (ipval, port))
                            time.sleep(.1)
                        else:
                            sock.sendto(self.plugin.colorCodes[color], (ipval, port))
                            time.sleep(.1)


# =======================================================================================================================================================================================================#
# =======================================================================================================================================================================================================#

class VariableCMD(eg.ActionBase):
    name = "Variable Command"
    description = "Change the state of the lights based on a spoken, typed, or read command generated from eg.event.payload."

    def Configure(self, global_var=''):
        panel = eg.ConfigPanel(self)

        img = wx.Image(
            os.path.join(
                os.path.dirname(__file__),
                'example_pic.png'
            ),
            wx.BITMAP_TYPE_ANY
        )
        png = img.ConvertToBitmap()
        example_pic = wx.StaticBitmap(panel, -1, png, (10, 5), (png.GetWidth(), png.GetHeight()))
        exampleBox = panel.BoxedGroup(
            "Example", example_pic)

        vc_spacer = panel.StaticText(' ')
        vc_spacer2 = panel.StaticText(' ')
        example_text = panel.StaticText(
            'For example .. you can use "AutoRemote.Message.*" ... As you can see above, I use')
        example_text2 = panel.StaticText(
            'the AutoRemote plugin in conjunction with this one, in order to speak commands')
        example_text3 = panel.StaticText('into a microphone/mobile phone and LimitlessLED plugin reacts accordingly.')

        vc_cmd_title = panel.StaticText(
            "If you'd like to specify a variable, do so below - otherwise eg.event.payload is used.")

        global_var = panel.TextCtrl('eg.event.payload')

        panel.sizer.AddMany([
            (exampleBox, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (vc_spacer, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (example_text, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (example_text2, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (example_text3, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (vc_spacer2, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (vc_cmd_title, 0, wx.ALIGN_CENTER_HORIZONTAL),
            (global_var, 0, wx.ALIGN_CENTER_HORIZONTAL)
        ])

        def OnTextEnter(event):
            field = global_var.GetValue()
            if ' ' in field:
                panel.EnableButtons(False)
            elif not field.startswith('eg.globals.'):
                panel.EnableButtons(False)
            else:
                panel.EnableButtons(True)

        global_var.Bind(wx.EVT_TEXT, OnTextEnter)

        while panel.Affirmed():
            panel.SetResult(
                global_var.GetValue())

    def GetLabel(self, global_var):
        return "Variable Command"

    def __call__(self, global_var):
        i = re.compile('u\'(.*)\'')
        j = re.compile('u\"(.*)\"')

        cmd = ''
        sub_cmd = ''
        groups = ['all']
        colors = [name.lower() for name in self.plugin.color]

        # Define our Default Values
        brightness = 40
        color_val = ['white']
        brightness_counter = 0  # if counter == 0, no command is given. Since we have default values, logic
        color_counter = 0  # checks will always trigger -- this acts as a counter-trigger.

        if global_var == 'eg.event.payload':
            if eg.event.payload is None:
                print "No command was given!"
            input_data = str(eg.event.payload)
        else:
            if global_var is None:
                print "No command was given!"
            input_data = str(global_var)

        try:
            input_data = re.search(i, input_data)
            words = input_data.group(1).split(' ')
        except AttributeError:
            input_data = re.search(j, input_data)
            words = input_data.group(1).split(' ')

        for y in xrange(0, 9):
            if y == 0:
                continue
            groups.append(self.plugin.groupnames[y].lower())

        for x in words:
            if x in ['on', 'off', 'remaining', 'lights', 'light', 'rest', 'of', 'the',
                     'everything', 'too']:
                cmd += x + ' '
                continue
            if '%' in x:
                cmd += x[:-1] + ' '
                continue
            if x in colors:
                if 'spring green' in ' '.join(words):
                    cmd += 'spring green '
                    continue
                cmd += x + ' '
                continue
            if x in groups:
                cmd += x + ' '
                continue
            if x in ['dim', 'dimmer', 'brighter', 'brighten', 'down', 'up', 'bright',
                     'dark', 'darker', 'little', 'bit', 'tad', 'touch', 'wink', 'wee']:
                cmd += x + ' '
                brightness_counter += 1
                continue

        if cmd == '':
            "No command found, please try again."
        else:
            cmd = cmd.split(' ')

            # find color_val
            if 'spring green' in ' '.join(cmd):
                color_val = ['spring green']
                color_counter += 1
            else:
                color_val = [i for i in colors if i in cmd]
                if color_val == []:
                    color_val = ['white']
                else:
                    color_counter += 1

            # find brightness
            for word in cmd:
                try:
                    brightness = int(round(int(word)))
                    brightness_counter += 1
                except ValueError:
                    try:
                        int(round(float(word)))
                        brightness_counter += 1
                    except ValueError:
                        continue

            if brightness == 0:
                print "Brightness can't be less than the minimum brightness! Setting brightness to 5%."
                brightness = 5

            if brightness > 100:
                print "Brightness can't be greater than the max brightness! Setting brightness to 100%."
                brightness = 100

            # test for awkwardly worded "all" command
            if 'lights' in cmd:
                try:
                    prev_word_the = cmd[cmd.index('lights') - 1]
                    if prev_word_the == 'the':
                        groups_present = [i for i in groups if i in cmd]
                        if groups_present == []:
                            groups_present = False
                except ValueError:
                    pass
            else:
                prev_word_the, groups_present = False, False

            # build the lights command, be it ON, OFF, DIM, or COLOR
            if 'on' in cmd:
                if (all(i in cmd for i in ['remaining', 'lights'])
                    or all(i in cmd for i in ['remaining', 'light'])
                    or all(i in cmd for i in ['rest', 'of'])
                    or any(i in cmd for i in ['all', 'everything', 'too'])
                    or (bool(prev_word_the) and not bool(groups_present))
                ):
                    if self.plugin.ip2 == "":
                        eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), True, False, True, True,
                                                       True, True, False, False, False, False)
                    else:
                        eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), True, False, True, True,
                                                       True, True, False, False, False, False)
                else:
                    for word in cmd:
                        if word == 'on':
                            continue
                        elif word in groups:
                            if groups.index(word) == 1:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               True, False, False, False, False, False, False, False)
                            elif groups.index(word) == 2:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, True, False, False, False, False, False, False)
                            elif groups.index(word) == 3:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, False, True, False, False, False, False, False)
                            elif groups.index(word) == 4:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, False, False, True, False, False, False, False)
                            elif groups.index(word) == 5:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, False, False, False, True, False, False, False)
                            elif groups.index(word) == 6:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, False, False, False, False, True, False, False)
                            elif groups.index(word) == 7:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, False, False, False, False, False, True, False)
                            elif groups.index(word) == 8:
                                eg.plugins.LimitlessLED.TurnOn(brightness, colors.index(color_val[0]), False, True,
                                                               False, False, False, False, False, False, False, True)
            elif 'off' in cmd:
                if (all(i in cmd for i in ['remaining', 'lights'])
                    or all(i in cmd for i in ['remaining', 'light'])
                    or all(i in cmd for i in ['rest', 'of'])
                    or any(i in cmd for i in ['all', 'everything', 'too'])
                    or (bool(prev_word_the) and not bool(groups_present))
                ):
                    if self.plugin.ip2 == "":
                        eg.plugins.LimitlessLED.TurnOff(True, False, True, True, True, True, False, False, False, False)
                    else:
                        eg.plugins.LimitlessLED.TurnOff(True, False, True, True, True, True, True, True, True, True)
                else:
                    for word in cmd:
                        if word in groups:
                            if groups.index(word) == 1:
                                eg.plugins.LimitlessLED.TurnOff(False, True, True, False, False, False, False, False,
                                                                False, False)
                            elif groups.index(word) == 2:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, True, False, False, False, False,
                                                                False, False)
                            elif groups.index(word) == 3:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, False, True, False, False, False,
                                                                False, False)
                            elif groups.index(word) == 4:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, False, False, True, False, False,
                                                                False, False)
                            elif groups.index(word) == 5:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, False, False, False, True, False,
                                                                False, False)
                            elif groups.index(word) == 6:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, False, False, False, False, True,
                                                                False, False)
                            elif groups.index(word) == 7:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, False, False, False, False, False,
                                                                True, False)
                            elif groups.index(word) == 8:
                                eg.plugins.LimitlessLED.TurnOff(False, True, False, False, False, False, False, False,
                                                                False, True)
            else:
                if color_counter != 0:
                    if (all(i in cmd for i in ['remaining', 'lights'])
                        or all(i in cmd for i in ['remaining', 'light'])
                        or all(i in cmd for i in ['rest', 'of'])
                        or any(i in cmd for i in ['all', 'everything', 'too'])
                        or (bool(prev_word_the) and not bool(groups_present))
                    ):
                        if self.plugin.ip2 == "":
                            eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), True, False, True, True, True,
                                                             True, False, False, False, False)
                        else:
                            eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), True, False, True, True, True,
                                                             True, True, True, True, True)
                    else:
                        for word in cmd:
                            if word in groups:
                                if groups.index(word) == 1:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, True,
                                                                     False, False, False, False, False, False, False)
                                elif groups.index(word) == 2:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     True, False, False, False, False, False, False)
                                elif groups.index(word) == 3:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     False, True, False, False, False, False, False)
                                elif groups.index(word) == 4:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     False, False, True, False, False, False, False)
                                elif groups.index(word) == 5:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     False, False, False, True, False, False, False)
                                elif groups.index(word) == 6:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     False, False, False, False, True, False, False)
                                elif groups.index(word) == 7:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     False, False, False, False, False, True, False)
                                elif groups.index(word) == 8:
                                    eg.plugins.LimitlessLED.SetColor(colors.index(color_val[0]), False, True, False,
                                                                     False, False, False, False, False, False, True)
                elif brightness_counter != 0:
                    brighter = [i for i in ['brighten', 'brighter', 'up', 'dark'] if i in cmd]
                    dimmer = [i for i in ['darker', 'dimmer', 'dim', 'down', 'bright'] if i in cmd]
                    modifier = [i for i in ['little', 'bit', 'tad', 'touch', 'wink', 'wee'] if i in cmd]

                    if modifier:
                        step = 1
                    else:
                        step = 2

                    if (all(i in cmd for i in ['remaining', 'lights'])
                        or all(i in cmd for i in ['remaining', 'light'])
                        or all(i in cmd for i in ['rest', 'of'])
                        or any(i in cmd for i in ['all', 'everything', 'too'])
                        or (bool(prev_word_the) and not bool(groups_present))
                    ):
                        if self.plugin.ip2 == "":
                            eg.plugins.LimitlessLED.Dimmer(brightness, True, False, True, True, True, True, False,
                                                           False, False, False, step, any(brighter), any(dimmer))
                        else:
                            eg.plugins.LimitlessLED.Dimmer(brightness, True, False, True, True, True, True, True, True,
                                                           True, True, step, any(brighter), any(dimmer))
                    else:
                        for word in cmd:
                            if word in groups:
                                if groups.index(word) == 1:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, True, False, False, False,
                                                                   False, False, False, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 2:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, True, False, False,
                                                                   False, False, False, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 3:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, False, True, False,
                                                                   False, False, False, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 4:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, False, False, True,
                                                                   False, False, False, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 5:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, False, False, False,
                                                                   True, False, False, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 6:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, False, False, False,
                                                                   False, True, False, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 7:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, False, False, False,
                                                                   False, False, True, False, step, any(brighter),
                                                                   any(dimmer))
                                elif groups.index(word) == 8:
                                    eg.plugins.LimitlessLED.Dimmer(brightness, False, True, False, False, False, False,
                                                                   False, False, False, True, step, any(brighter),
                                                                   any(dimmer))
                else:
                    print " "
                    print "This was a command that SupahNoob did not account for. If you would like it added, please contact me!"
                    print "Below are the words recognized on a separate new line."
                    for word in cmd:
                        print word
                    else:
                        print "And this was the full command that was given.."
                        print " ".join(words)

        # eg.plugins.LimitlessLED.Dimmer(100, True, False, True, True, True, True, False, False, False, False, 1, False, False)
        # eg.plugins.LimitlessLED.Dimmer(100, True, False, True, True, True, True, True, True, True, True, 1, True, False)
        # eg.plugins.LimitlessLED.Dimmer(100, True, False, True, True, True, True, True, True, True, True, 1, False, True)
