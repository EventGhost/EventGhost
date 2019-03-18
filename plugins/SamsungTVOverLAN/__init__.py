# -*- coding: utf-8 -*-
#
# plugins/SamsungTVOVerLAN/__init__.py
# 
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
#
# Samsung Serial
# ================
# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
import eg
import samsungremote

help = """\
Plugin to control Samsung TVs over LAN."""
eg.RegisterPlugin(
    name = "Samsung TV over LAN",
    author = "dredkin",
    version = "0.1",
    kind = "external",
    guid = "{2432E1D6-1566-11E2-BEB7-2F216288709B}",
    description = "Control Samsung TVs (Series C and LAter) equipped with LAN or Wi-Fi interface",
    url = "http://www.eventghost.net/forum",
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
cmdList = (
    ('Power', None),
        ('KEY_POWEROFF',               'Power Standby'),
    ('Volume', None),
        ('KEY_MUTE',             'Mute Toggle'),
        ('KEY_VOLUP',               'Master Volume Up'),
        ('KEY_VOLDOWN',             'Master Volume Down'),
    ('Channel', None),
        ('KEY_0',          '0'),
        ('KEY_1',          '1'),
        ('KEY_2',          '2'),
        ('KEY_3',          '3'),
        ('KEY_4',          '4'),
        ('KEY_5',          '5'),
        ('KEY_6',          '6'),
        ('KEY_7',          '7'),
        ('KEY_8',          '8'),
        ('KEY_9',          '9'),
        ('KEY_CHUP',              'Channel Up'),
        ('KEY_CHDOWN',              'Channel Down'),
        ('KEY_CH_LIST',              'Channel List'),
        ('KEY_PRECH',              'Previous Channel'),
        ('KEY_PICTURE_SIZE',                'Picture Size'),
        
    ('Input', None),
        ('KEY_TV',                     'TV'),               
        ('KEY_SOURCE',                     'Source'),               
        ('KEY_W_LINK','Media Player'), 
        ('KEY_RSS','Internet'), 
        ('KEY_CONTENTS','Contents'),
    ('Menu / Nav', None),
        ('KEY_UP',                'Up'),
        ('KEY_DOWN',                'Down'),
        ('KEY_LEFT',                'Left'),
        ('KEY_RIGHT',                'Right'),
        ('KEY_MENU',                'Menu'),
        ('KEY_ENTER',                'Enter'),
        ('KEY_RETURN',                'Return'),
        ('KEY_EXIT',                'Exit'),
        ('KEY_TOOLS',                'Tools'),
        ('KEY_INFO',                'Info'),
        ('KEY_GUIDE',                'Guide'),
    ('Media Player', None),
        ('KEY_PLAY','Play'),
        ('KEY_PAUSE','Pause'),
        ('KEY_REWIND','Rewind'),
        ('KEY_FF','Fast Forward'),
        ('KEY_REC','Record'),
        ('KEY_STOP','Stop'),
        ('KEY_CAPTION','Subtitles'),
        ('KEY_MTS','Dual'),  
        ('KEY_AD','AD'),
    (None, None),       
)
        
class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        sender = self.plugin.sender
        sender.connect(self.plugin.tvip,self.plugin.tvmodel)
        sender.sendKey(self.cmd)
        sender.disconnect

class Raw(eg.ActionWithStringParameter):
    name = 'Send command'
    def __call__(self, data):
        sender = self.plugin.sender
        sender.connect(self.plugin.tvip,self.plugin.tvmodel)
        sender.sendKey(data)
        sender.disconnect

class SamsungOverLAN(eg.PluginBase):     
    def __init__(self):
        self.sender = samsungremote.SamsungTVSender("EventGhost Remote")
        self.tvip = ""
        self.tvmodel = ""
        group = self

        for cmd_cmd, cmd_text in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_cmd is None:
                    group = self
                else:
                    group = self.AddGroup(cmd_cmd)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd =  cmd_cmd
                Action.__name__ = cmd_text
                group.AddAction(Action)

        group.AddAction(Raw)
          

    def __start__(self, tvip, tvmodel):
        self.tvip = tvip
        self.tvmodel = tvmodel

    def __stop__(self):
        self.sender.disconnect()
        
    def Configure(self, tvip="192.168.1.2", tvmodel="LE46C650"):
        panel = eg.ConfigPanel(self)
        tvipControl = wx.TextCtrl(panel, -1, tvip)
        panel.sizer.Add(tvipControl, 1, wx.EXPAND)
        panel.AddLine("Samsung TV IP Adress:", tvipControl)
        tvmodelControl = wx.TextCtrl(panel, -1, tvmodel)
        panel.sizer.Add(tvmodelControl, 1, wx.EXPAND)
        panel.AddLine("TV Model:", tvmodelControl)
        while panel.Affirmed():
            panel.SetResult(tvipControl.GetValue(),tvmodelControl.GetValue())
