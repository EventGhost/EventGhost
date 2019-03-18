#
# SonyVPLSerial 
# =============
# Written by Silviu Marghescu
#
# This plug-in is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This plug-in is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with EventGhost; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Revision history:
# -----------------
# 0.1 - first revision (only the main commands and responses implemented)
#

help = """\
The plugin controls any Sony VPL front projector via the serial interface.
The protocol was implemented using specifications for the VPL-VW40/VPL-VW60
models, but was tested on a VPL-HW10.  According to Sony support, the protocol
is the same for all models that have a serial interface.

Sony projectors using this protocol send status messages in response to either
explicit commands or status queries.  Status messages trigger events (some with
payload) that can be used in macros."""

import eg

eg.RegisterPlugin(
    name="Sony VPL Front Projector Serial",
    guid='{526DF7E1-7C90-4C43-A226-C5DBBFEC3B33}',
    author="Silviu Marghescu",
    version="0.1." + "$LastChangedRevision: 1 $".split()[1],
    kind="external",
    description="Control Sony VPL front projectors via the serial interface",
    help=help,
    canMultiLoad=True,
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

# command map; 4 elements: id, name, serial code, group
commands = (
    ('PowerOn', 'Power On', '\xA9\x17\x2E\x00\x00\x00\x3F\x9A', "Power"),
    ('PowerStandby', 'Power Standby', '\xA9\x17\x2F\x00\x00\x00\x3F\x9A', "Power"),
    # ('PowerStatus', 'Power Status', '\xA9\x17\x25\x00\x00\x00\x37\x9A', "Power"),
    ('PowerStatus', 'Power Status', '\xA9\x01\x02\x01\x00\x00\x03\x9A', "Power"),

    ('InputVideo', 'Input Video', '\xA9\x00\x01\x00\x00\x00\x01\x9A', "Input"),
    ('InputSVideo', 'Input S-Video', '\xA9\x00\x01\x00\x00\x01\x01\x9A', "Input"),
    ('InputA', 'Input Input-A', '\xA9\x00\x01\x00\x00\x02\x03\x9A', "Input"),
    ('InputComponent', 'Input Component', '\xA9\x00\x01\x00\x00\x03\x03\x9A', "Input"),
    ('InputHDMI1', 'Input HDMI1', '\xA9\x00\x01\x00\x00\x04\x05\x9A', "Input"),
    ('InputHDMI2', 'Input HDMI2', '\xA9\x00\x01\x00\x00\x05\x05\x9A', "Input"),
    ('InputStatus', 'Input Status', '\xA9\x00\x01\x01\x00\x00\x01\x9A', "Input"),

    ('PictureDynamic', 'Picture Mode Dynamic', '\xA9\x00\x02\x00\x00\x00\x02\x9A', "Picture"),
    ('PictureStandard', 'Picture Mode Standard', '\xA9\x00\x02\x00\x00\x01\x03\x9A', "Picture"),
    ('PictureCinema', 'Picture Mode Cinema', '\xA9\x00\x02\x00\x00\x02\x02\x9A', "Picture"),
    ('PictureStatus', 'Picture Mode Status', '\xA9\x00\x02\x01\x00\x00\x03\x9A', "Picture"),

    ('LampLow', 'Lamp Low', '\xA9\x00\x1A\x00\x00\x00\x1a\x9A', "Misc."),
    ('LampHigh', 'Lamp High', '\xA9\x00\x1A\x00\x00\x01\x1B\x9A', "Misc."),
    ('LampTime', 'Get Lamp Time', '\xA9\x01\x13\x01\x00\x00\x13\x9A', "Misc."),
)


class CmdAction(eg.ActionClass):

    def __call__(self):
        self.plugin.serialThread.Write(self.cmd)


class SonyVPLSerial(eg.PluginClass):

    def __init__(self):
        self.groups = {}
        for cmd_name, cmd_text, cmd_cmd, cmd_group in commands:
            if cmd_group is None:
                group = self
            elif self.groups.has_key(cmd_group):
                group = self.groups[cmd_group]
            else:
                group = self.AddGroup(cmd_group)
                self.groups[cmd_group] = group

            class Action(CmdAction):
                name = cmd_text
                cmd = cmd_cmd

            Action.__name__ = cmd_name
            group.AddAction(Action)

        self.nakDict = {
            "\x01": "UndefinedCommand",
            "\x04": "SizeError",
            "\x05": "SelectError",
            "\x06": "RangeOver",
            "\x0a": "NotApplicable",
            "\x10": "ChecksumError",
            "\x20": "FramingError",
            "\x30": "ParityError",
            "\x40": "OverRubError",
            "\x50": "OtherError"
        }

        self.dataDict = {
            "\x00\x01\x00\x00": "Input.Video",
            "\x00\x01\x00\x01": "Input.S-Video",
            "\x00\x01\x00\x02": "Input.Input-A",
            "\x00\x01\x00\x03": "Input.Component",
            "\x00\x01\x00\x04": "Input.HDMI1",
            "\x00\x01\x00\x05": "Input.HDMI2",

            "\x00\x02\x00\x00": "Picture.Dynamic",
            "\x00\x02\x00\x01": "Picture.Standard",
            "\x00\x02\x00\x02": "Picture.Cinema",
            "\x00\x02\x00\x03": "Picture.User1",
            "\x00\x02\x00\x04": "Picture.User2",
            "\x00\x02\x00\x05": "Picture.User3",

            "\x00\x1a\x00\x00": "Lamp.Low",
            "\x00\x1a\x00\x01": "Lamp.High",

            "\x00\x1d\x00\x00": "Iris.Off",
            "\x00\x1d\x00\x01": "Iris.On",
            "\x00\x1d\x00\x02": "Iris.Auto1",
            "\x00\x1d\x00\x03": "Iris.Auto2",

            "\x00\x30\x00\x00": "PictureMute.Off",
            "\x00\x30\x00\x01": "PictureMute.On",

            "\x01\x01\x00\x00": "Error.NoError",
            "\x01\x01\x00\x01": "Error.LampError",
            "\x01\x01\x00\x02": "Error.FanError",
            "\x01\x01\x00\x04": "Error.CoverError",
            "\x01\x01\x00\x08": "Error.TempError",
            "\x01\x01\x00\x10": "Error.D5VError",
            "\x01\x01\x00\x20": "Error.PowerError",
            "\x01\x01\x00\x40": "Error.WarningError",
            "\x01\x01\x00\x80": "Error.NVMDataError",

            "\x01\x02\x00\x00": "Power.Standby",
            "\x01\x02\x00\x01": "Power.StartUp",
            "\x01\x02\x00\x02": "Power.StartUpLamp",
            "\x01\x02\x00\x03": "Power.PowerOn",
            "\x01\x02\x00\x04": "Power.Cooling1",
            "\x01\x02\x00\x05": "Power.Cooling2",
            "\x01\x02\x00\x06": "Power.SavingCooling1",
            "\x01\x02\x00\x07": "Power.SavingCooling2",
            "\x01\x02\x00\x08": "Power.SavingStandby"
        }

    def __start__(self, port):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 38400, "8E1")
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
            # check for end of response frame
            if b == "\x9a":
                if not buffer.startswith("\xa9"):
                    return  # invalid frame
                ###print("Buffer: "+binascii.b2a_hex(buffer).upper(), len(buffer));
                replycode = buffer[1:3]
                replytype = buffer[3]
                replydata = buffer[4:6]

                if replytype == "\x03":
                    # ACK/NAK frame
                    if replycode[0] == "\x00":
                        # ACK
                        self.TriggerEvent("ACK")
                    elif replycode[0] == "\x01":
                        # NAK Command error
                        self.TriggerEvent("NAK.Command." + self.nakDict[replycode[1]])
                    elif replycode[0] == "\xf0":
                        # NAK Communication error
                        self.TriggerEvent("NAK.Communication." + self.nakDict[replycode[1]])
                    return

                if replytype == "\x02":
                    # data frame
                    key = replycode + replydata
                    if self.dataDict.has_key(key):
                        self.TriggerEvent(self.dataDict[key])
                        return
                    elif replycode == "\x01\x13":
                        # lamp hours
                        self.TriggerEvent("LampTime", ord(replydata[0]) * 16 + ord(replydata[1]))
                        return
                    self.TriggerEvent("UNKNOWN")
                    return

            elif b == "":
                return
            buffer += b
