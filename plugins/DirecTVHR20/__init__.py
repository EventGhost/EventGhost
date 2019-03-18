#
# DirecTV HR20
# ================
#
# Revision history:
# -----------------
# 0.1 - initial
#

import eg

help = """\
Plugin to control the DirecTV HR20 Receiver via RS232 through a USB->Serial adapter.
<ul>
<li>The following USB->Serial adapters are compatable with the HR20 Receiver</li>
<li>IOGear GUC232A</li>
<li>Aten UC-232A</li>
<li>Bafo BF-810</li>
</ul>
<UL>
<li>Additonally you will need a null modem cable adapter. (null modem cable if you are using
a serial port on your computer or a null modem adapter if you are using USB on your computer)
<li>Data Format is: 9600 baud, 1 start bit, 8 data bits, no parity, no flow control</li>
</ul>
</ul>
"""

eg.RegisterPlugin(
    name="DirecTV HR20 Serial",
    guid='{0351B118-417C-489D-A650-F832F1C75ADD}',
    author="",
    version="0.1." + "$LastChangedRevision: 809 $".split()[1],
    kind="external",
    description="Control DirecTV HR20 via RS232",
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

import binascii
import eg

cmdList = (
    ('Power', None, None, None),
    ('Standby', 'Standby', '81', None),
    ('Active', 'Power On', '82', None),
    ('Reboot', 'Reboot', '96', None),
    ('Actions', None, None, None),
    ('Enter', 'Enter', 'A50001A0', None),
    ('Info', 'Information', 'A50001A1', None),
    ('Active', 'Active', 'A50001A2', None),
    ('List', 'List', 'A50001A3', None),
    ('Back', 'Back', 'A50001A4', None),
    ('Minus', 'Minus', 'A50001A5', None),
    ('Select', 'Select', 'A50001C3', None),
    ('PowerOn', 'Power On', 'A50001C5', None),
    ('Right', 'Right', 'A500019A', None),
    ('Left', 'Left', 'A500019B', None),
    ('Up', 'Up', 'A500019C', None),
    ('Down', 'Down', 'A500019D', None),
    ('PowerOff', 'Power Off', 'A50001D0', None),
    ('CHUp', 'Channel Up', 'A50001D1', None),
    ('CHDown', 'Channel Down', 'A50001D2', None),
    ('Guide', 'Guide', 'A50001D3', None),
    ('Exit', 'Exit', 'A50001D4', None),
    ('PreviousCH', 'Prev Channel', 'A50001D6', None),
    ('Pause', 'Pause', 'A50001B0', None),
    ('Rewind', 'Rewind', 'A50001B1', None),
    ('Play', 'Play', 'A50001B2', None),
    ('Stop', 'Stop', 'A50001B3', None),
    ('FastForward', 'Fast Forward', 'A50001B4', None),
    ('Record', 'Record', 'A50001B5', None),
    ('Replay', 'Replay', 'A50001B6', None),
    ('Advance', 'Advance', 'A50001B7', None),
    ('0', '0', 'A50001E0', None),
    ('1', '1', 'A50001E1', None),
    ('2', '2', 'A50001E2', None),
    ('3', '3', 'A50001E3', None),
    ('4', '4', 'A50001E4', None),
    ('5', '5', 'A50001E5', None),
    ('6', '6', 'A50001E6', None),
    ('7', '7', 'A50001E7', None),
    ('8', '8', 'A50001E8', None),
    ('9', '9', 'A50001E9', None),
    ('Green', 'Green', 'A50001EC', None),
    ('Red', 'Red', 'A50001EA', None),
    ('Yellow', 'Yellow', 'A50001EB', None),
    ('Blue', 'Blue', 'A50001ED', None),
    ('Menu', 'Menu', 'A50001F7', None),
    ('Format', 'Format', 'A50001F8', None),
    ('Queries', None, None, None),
    ('GetPrimaryStatus', 'Get Status Information On Current Channel', '83', None),
    ('GetCurrentChannel', 'Get Major and Minor Numbers Of Tunned Channel', '87', None),
    ('GetSignalQuality', 'Get Signal Level For Tuned Channel', '90', None),
    ('GetCurrentTime', 'Get Current Time', '91', None),
    ('GetUserCommand', 'Get Remote Or front Panel Command Input', '92', None),
    ('EnableUserEntry', 'Allow Remote Or Front Panel Control', '93', None),
    ('DisableUserEntry', 'Disable Remote Or Front Panel Control', '94', None),
    ('GetReturnValue', 'Return Last Return Value', '95', None),
    ('SendUserCommand', 'Send Remote Control Command', 'A5', None),
    ('OpenUserChannel', 'Tune To Channel Directly (0-9999)', 'A6', '0-9999'),
    ('GetTuner', 'Get Number Of Tuners And Designations', '9A', None),
    ('GetPrimaryStatusMT', 'Get Status Information On Current Channel', '8A', None),
    ('GetCurrentChannelMT', 'Get Major And Minor Numbers Ot Tuned Channel', '8B', None),
    ('GetSignalQualityMT', 'Get Signal Quality MT', '9D', None),
    (None, None, None, None),

)


class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        print "command sent " + self.cmd
        # push command onto the list
        self.plugin.lastCommand.append(self.cmd)
        self.plugin.serialThread.Write(binascii.a2b_hex('FA' + self.cmd + 'F4'))


class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        data = eg.ParseString(data);
        data = str(hex(int(data)))
        data = data[2:len(data)]
        while len(data) < 4:
            data = "0" + data
        print ('FA' + data + 'FFFFF4')
        print("ValueAction " + data)
        # push command onto the list        
        self.plugin.lastCommand.append(self.cmd)
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(binascii.a2b_hex('FAA6' + data + 'FFFFF4'))
        self.plugin.serialThread.ResumeReadEvents()


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        print(str(data))
        # push command onto the list               
        self.plugin.lastCommand.append(data)
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(binascii.a2b_hex('FA' + str(data) + 'F4'))
        self.plugin.serialThread.ResumeReadEvents()


class DirecTVSerial(eg.PluginClass):
    def __init__(self):
        self.serial = None
        self.lastCommand = []
        self.buffer = []
        self.errorState = False
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
                    cmd = cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr

                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd = cmd_cmd

                Action.__name__ = cmd_name
                group.AddAction(Action)

        group.AddAction(Raw)

        self.audioDict = {
            '00': 'MPEG In / PCM Out',
            '09': 'AC3 In / AC3 Out',
            'FF': 'None'
        }
        self.primaryDict = {
            '0B': 'Data',
            '0C': 'Audio',
            '0E': 'Retired',
            '0F': 'Video - TV',
            '10': 'Video - HDTV',
            'FF': 'None'
        }
        self.dataDict = {
            '0B': 'Retired',
            '0C': 'Retired',
            '0D': 'Retired',
            'FF': 'None'
        }
        self.successDict = {
            'F0': 'Command Acknowledge',
            'F2': 'Correct Number Of Arguments',
            'F4': 'Success: Service Command'
        }
        self.errorDict = {
            'F1': 'Error: Command Unkown',
            'F3': 'Error: Timed Out Receiving Parameters',
            'F5': 'Error: Service Command',
            'F6': 'Error: Parser Break',
            'F7': 'Error: Service Command Pending',
            'F9': 'Error: Command Parser In Use',
            'FB': 'Error: Prefix Not Sent',
            'FD': 'Error: Parser Data Error',
            'FF': 'Error: Parser Buffer'
        }

    def __start__(self, port):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 9600)
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

    def ChannelNumber(self, data):
        return int(data, 16)

    def OnReceive(self, serial):
        buffer = []
        while True:

            currentCommand = self.lastCommand[0]
            b = serial.Read(1, 0.1)
            if b == "":
                return
            b = binascii.b2a_hex(b)
            buffer.append(b.upper())
            print("STB Response: " + b)
            command = buffer[0]

            if command == 81:
                a = 1
            if command == 82:
                a = 1
            if command == 83:
                a = 1
            if command == 84:
                a = 1
            if command == 85:
                a = 1
            if command == 86:
                a = 1
            if command == 87:
                # Possible Responses Success
                # [F0][0000][0000][F4]
                if self.successDict.has_key(command):
                    print(self.successDict[command])
                    errorState = false
                    buffer.pop(0)
                    # if acknowledged
                    if command == 'F4':
                        self.lastCommand.pop(0)
                    continue
                if not errorState:
                    channel += buffer.pop(0)
                    if (len(channel) == 4):
                        self.TriggerEvent("Channel1" + str(self.ChannelNumber(channel)))
                        eg.globals.directvchannel1 = str(self.ChannelNumber(channel))
                    continue
                    # Possible Response Failed
                # [F1]
                # [F0][F5]
                if self.errorDict.has_key(command) | errorState == True:
                    errorState = True
                    print(self.errorDict[command])
                    buffer.pop(0)
                    if command == 'F5':
                        currentCommand.pop(0)
                        errorState = False
                        continue

            if self.lastCommand == "9D":
                print(buffer[2:4])
                print(str(self.ChannelNumber(buffer[2:4])))
