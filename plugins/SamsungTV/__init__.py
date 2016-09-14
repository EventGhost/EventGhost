# -*- coding: utf-8 -*-
#
# plugins/SamsungTV/__init__.py
#
# This file is a plugin for EventGhost.
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
#
# Samsung Serial
# ================
# Public Domain
#
# Revision history:
# -----------------
# 0.1 - initial
# 0.2 - revised by Fiasco for Samsung TV series

help = """\
Plugin to control Samsung TV RS-232."""

eg.RegisterPlugin(
    name = "Samsung TV",
    author = (
        "prostetnic",
        "Bartman",
        "Fiasco",
    ),
    version = "0.2.1181",
    kind = "external",
    guid = "{ADA3F327-DA18-44E0-A712-8C1C90B52DEC}",
    description = "Control Samsung TV via RS232",
    url = "http://www.eventghost.org/forum/viewtopic.php?f=9&t=2059",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
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


import re
import binascii
# command 7 bytes total
# header 2 byte 0x08 0x22
# cmd 1 1 byte
# cmd 2 1 byte
# cmd 3 1 byte
# value 1 byte
# checksum 1 byte (2's complement of sum of all values
# 9600 8bit None 1bit none
# success 030cf1
# fail 030cff

cmdList = (
    ('Power / Sleep', None, None, None),
        ('PowerOff',               'Power Standby',                                              '00000001',             None),
        ('PowerOn',                'Power On',                                                   '00000002',             None),
        ('PowerStatus',            'Get Power Status',                                           '00000000',             None),
    ('Master Volume', None, None, None),
        ('MuteToggle',             'Mute Toggle',                                                '02000000',             None),
        ('VolumeUp',               'Master Volume Up',                                           '01000100',             None),
        ('VolumeDown',             'Master Volume Down',                                         '01000200',             None),
        ('VolumeDirect',           'Set Volume Directly (0-100)',                                '010000',               '0-100'),
    ('Channel', None, None, None),
        ('ChannelDirect',          'Set Channel Directly (0-9999)',                              '04',                   '0-9999'),
        ('ChannelUp',              'Channel Up',                                                 '03000100',             None),
        ('ChannelDn',              'Channel Down',                                               '03000201',             None),
    ('Input', None, None, None),
        ('TV',                     'TV',                                                         '0a000000',           None),
        ('AV1',                    'AV 1',                                                       '0a000100',           None),
        ('AV2',                    'AV 2',                                                       '0a000101',           None),
        ('AV3',                    'AV 3',                                                       '0a000102',           None),
        ('SVideo1',                'S-Video 1',                                                  '0a000200',           None),
        ('SVideo2',                'S-Video 2',                                                  '0a000201',           None),
        ('SVideo3',                'S-Video 3',                                                  '0a000202',           None),
        ('Component1',             'Component 1',                                                '0a000300',           None),
        ('Component2',             'Component 2',                                                '0a000301',           None),
        ('Component3',             'Component 3',                                                '0a000302',           None),
        ('PC1',                    'PC 1',                                                       '0a000400',           None),
        ('PC2',                    'PC 2',                                                       '0a000401',           None),
        ('PC3',                    'PC 3',                                                       '0a000402',           None),
        ('HDMI1',                  'HDMI 1',                                                     '0a000500',           None),
        ('HDMI2',                  'HDMI 2',                                                     '0a000501',           None),
        ('HDMI3',                  'HDMI 3',                                                     '0a000502',           None),
        ('HDMI4',                  'HDMI 4',                                                     '0a000503',           None),
        ('DVI1',                   'DVI 1',                                                      '0a000600',           None),
        ('DVI2',                   'DVI 2',                                                      '0a000601',           None),
        ('DVI3',                   'DVI 3',                                                      '0a000602',           None),
    ('Picture', None, None, None),
        ('Dynamic',                'Dynamic',                                                    '0b000000',           None),
        ('Standard',               'Standard',                                                   '0b000001',           None),
        ('Wide',                   'Wide',                                                       '0b000002',           None),
        ('Contrast',               'Set Contrast (0-100)',                                       '0b0200',             '0-100'),
        ('Brightness',             'Set Brightness (0-100)',                                     '0b0300',             '0-100'),
        ('Sharpness',              'Set Sharpness (0-100)',                                      '0b0400',             '0-100'),
        ('Color',                  'Set Color (0-10)',                                           '0b0500',             '0-10'),
        ('Tint',                   'Set Tint (0-100)',                                           '0b0700',             '0-100'),
        ('DetailBlackOff',         'Black Adjust Off',                                           '0b090000',           None),
        ('DetailBlackLow',         'Black Adjust Low',                                           '0b090001',           None),
        ('DetailBlackMed',         'Black Adjust Medium',                                        '0b090002',           None),
        ('DetailBlackHigh',        'Black Adjust High',                                          '0b090003',           None),
        ('DynamicContrastOff',     'Dynamic Contrast Off',                                       '0b090100',           None),
        ('DynamicContrastLow',     'Dynamic Contrast Low',                                       '0b090101',           None),
        ('DynamicContrastMed',     'Dynamic Contrast Medium',                                    '0b090102',           None),
        ('DynamicContrastHigh',    'Dynamic Contrast High',                                      '0b090103',           None),
        ('ColorSpaceAuto',         'Color Space Auto',                                           '0b090300',           None),
        ('ColorSpaceWide',         'Color Space Wide',                                           '0b090301',           None),
    ('Sound', None, None, None),
        ('Standard',               'Standard',                                                   '0c000000',           None),
        ('Music',                  'Music',                                                      '0c000001',           None),
        ('Movie',                  'Movie',                                                      '0c000002',           None),
        ('Speech',                 'Speech',                                                     '0c000003',           None),
        ('Custom',                 'Custom',                                                     '0c000004',           None),
        ('EQStandard',             'EQ Standard',                                                '0c010000',           None),
        ('EQMusic',                'EQ Music',                                                   '0c010001',           None),
        ('EQMovie',                'EQ Movie',                                                   '0c010002',           None),
        ('EQSpeech',               'EQ Speech',                                                  '0c010003',           None),
        ('EQCustom',               'EQ Custom',                                                  '0c010004',           None),
        ('SRSTruSurroundOn',       'SRS Tru Surround On',                                        '0c020000',           None),
        ('SRSTruSurroundOff',      'SRS Tru Surround Off',                                       '0c020001',           None),
        ('MultiTrackMono',         'Multi-Track Mono',                                           '0c040000',           None),
        ('MultiTrackStereo',       'Multi-Track Stereo',                                         '0c040001',           None),
        ('MultiTrackSAP',          'Multi-Track SAP',                                            '0c040002',           None),
    (None, None, None, None),
)


def generatechecksum(value):
    print value
    data = value.decode("hex")
    sum = 0
    for byte in data:
        sum += ord(byte)
    # data += chr((sum & 0xFF) ^ 0xFF)

    # Here's how to get the one's complement of the low byte of the sum
    # print "Sum:", sum, "=", hex(sum)
    # print "Low byte:", hex(sum & 0xFF)
    print "Two's complement:", hex((~sum + 1) & 0xFF)
    data = hex((~sum + 1) & 0xFF)
    data = str(data)[2:]
    if ( len(data) < 2 ):
       data = '0' + data
    print "checksum " + data
    return data

class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        value = generatechecksum(self.cmd)
        value = binascii.a2b_hex(self.cmd + value)
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()



class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        value = generatechecksum(self.cmd + data)
        value = binascii.a2b_hex(self.cmd + data + value)
        self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        value = generatechecksum(data)
        value = binascii.a2b_hex(data + value)
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()

class SamsungSerial(eg.PluginClass):
    def __init__(self):
        self.serial = None
        group = self

        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_name)
            elif cmd_rangespec is not None:
                # Command with argument
                actionName, paramDescr = cmd_text.split("(")
                actionName = actionName.strip()
                paramDescr = paramDescr[:-1]
                minValue, maxValue = cmd_rangespec.split("-")

                class Action(ValueAction):
                    name = actionName
                    cmd = "0822" + cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr
                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd =  "0822" + cmd_cmd
                Action.__name__ = cmd_name
                group.AddAction(Action)

        group.AddAction(Raw)


    def __start__(self, port):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 9600, '8N1')
        self.serialThread.SetRts()
        self.serialThread.Start()

    def __stop__(self):
        self.serialThread.Close()

    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())

    def OnReceive(self, serial):
        buffer = ""
        while True:
            b = serial.Read(1, 0.1)
            b = binascii.hexlify(b)
            if b == '':
               return
            print b

# fail 030cff
# success 030cf1

            if buffer == '030cff':
               self.TriggerEvent("Command", "Failed")
               return
            if buffer == '030cf1':
               self.TriggerEvent("Command", "Success")
               return
            buffer += b

