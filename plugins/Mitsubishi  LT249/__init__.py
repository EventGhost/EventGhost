#
# Mitsubishi Serial
# ================

# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
# 0.2 - revised by Fiasco for Mitsubishi LT249 LCD TV series

help = """\
Plugin to control Mitsubishi LT249 LCD TV RS-232."""

import eg

eg.RegisterPlugin(
    name="Mitsubishi LT249",
    guid='{DA01DBF3-93A3-4160-8DD1-D7046C157227}',
    author="prostetnic, Bartman and Fiasco",
    version="0.2." + "$LastChangedRevision: 1181 $".split()[1],
    kind="external",
    description="Control Mitsubishi LT249 LCD TV via RS232",
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

cmdList = (
    ('Power / Sleep', None, None, None),
    ('PowerOff', 'Power Standby', '020001', None),
    ('PowerOn', 'Power On', '020000', None),
    ('PowerStatus', 'Get Power Status', '020080', None),
    ('Master Volume', None, None, None),
    ('MuteToggle', 'Mute Toggle', '020800', None),
    ('VolumeUp', 'Master Volume Up', '020801', None),
    ('VolumeDown', 'Master Volume Down', '020802', None),
    ('Input', None, None, None),
    ('InputStatus', 'Get Input Status', '020180', None),
    ('Input1', 'Input 1', '03010001', None),
    ('Input2', 'Input 2', '03010002', None),
    ('Input3', 'Input 3', '03010003', None),
    ('Input4', 'Input 4', '03010004', None),
    ('Input5', 'Input 5', '03010005', None),
    ('Ant-A', 'Antenna A', '03010006', None),
    ('Ant-B', 'Antenna B', '03010007', None),
    ('Ant-DTV', 'Antenna DTV', '03010008', None),
    ('Component1', 'Component 1', '03010009', None),
    ('Component2', 'Component 2', '0301000A', None),
    ('Component3', 'Component 3', '0301000B', None),
    ('Component4HDMI3', 'Component 4 / HDMI 3', '0301000C', None),
    ('Component5HDMI4', 'Component 5 / HDMI 4', '0301000D', None),
    ('Input-DTV', 'Input DTV', '0301000F', None),
    ('VGA1', 'VGA 1', '03010020', None),
    ('VGA2', 'VGA 2', '03010021', None),
    ('VGA3', 'VGA 3', '03010022', None),
    ('MonitorLink', 'Monitor Link', '03010023', None),
    ('InputUp', 'Input Up', '020101', None),
    ('InputDown', 'Input Down', '020102', None),
    ('ChannelUp', 'Channel Up', '020201', None),
    ('ChannelDown', 'Channel Down', '020202', None),
    ('Format', None, None, None),
    ('Standard', 'Standard', '03030001', None),
    ('Expand', 'Expand', '03030002', None),
    ('Zoom', 'Zoom', '03030003', None),
    ('Stretch', 'Stretch', '03030004', None),
    ('StretchPlus', 'Stretch Plus', '03030005', None),
    ('Narrow', 'Narrow', '03030006', None),
    ('FullNative', 'Full Native', '03030007', None),
    (None, None, None, None),
)


def generatechecksum(value):
    #    print "Command " + value
    data = value.decode("hex")
    sum = 0
    for byte in data:
        sum += ord(byte)
    data += chr((sum & 0xFF) ^ 0xFF)

    # Here's how to get the one's complement of the low byte of the sum
    # print "Sum:", sum, "=", hex(sum)
    # print "Low byte:", hex(sum & 0xFF)
    #    print "One's complement:", hex((sum & 0xFF) ^ 0xFF)
    data = hex((sum & 0xFF) ^ 0xFF)
    data = str(data)[2:]
    if (len(data) < 2):
        data = '0' + data
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
        self.plugin.serialThread.Write(self.cmd + str(data))
        self.plugin.serialThread.ResumeReadEvents()


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        value = generatechecksum(data)
        value = binascii.a2b_hex(data + value)
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()


class MitsubishiSerial(eg.PluginClass):
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
                    cmd = "DF8070F8" + cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr

                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd = "DF8070F8" + cmd_cmd

                Action.__name__ = cmd_name
                group.AddAction(Action)

        group.AddAction(Raw)

        self.onOffDict = {
            '02': 'Off',
            '01': 'On',
        }

        self.inputDict = {
            '01': 'Input 1',
            '02': 'Input 2',
            '03': 'Input 3',
            '04': 'Input 4',
            '05': 'Input 5',
            '06': 'Antenna-A',
            '07': 'Antenna-B',
            '08': 'Antenna-DTV',
            '09': 'Component 1',
            '0A': 'Component 2',
            '0B': 'Component 3',
            '0C': 'Component 4 / HDMI 3',
            '0D': 'Component 5 / HDMI 4',
            '0F': 'Input-DTV',
            '20': 'RGB 1',
            '21': 'RGB 2',
            '22': 'RGB 3',
            '23': 'Monitor Link'
        }
        self.formatDict = {
            '01': 'Standard',
            '02': 'Expand',
            '03': 'Zoom',
            '04': 'Stretch',
            '05': 'Stretch Plus',
            '06': 'Narrow',
            '07': 'Full Native'
        }

    def __start__(self, port):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 9600, '8O1')
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
            if len(buffer) > 19:
                return
            if b == generatechecksum(buffer):
                header = buffer[0:8]
                commandlength = buffer[8:10]
                command = buffer[10:14]
                status = buffer[14:16]
                data = buffer[16:]

                # Input Commands
                if command == '0180':
                    self.TriggerEvent("Input", self.inputDict[data])
                if command == '0100':
                    self.TriggerEvent("Input", self.inputDict[data])
                    # Power Commands
                if command == '0080':
                    self.TriggerEvent("Power", self.onOffDict[data])
                if command == '0000' and status == '00':
                    self.TriggerEvent("Power", "On")
                if command == '0001' and status == '00':
                    self.TriggerEvent("Power", "Off")
                if command == '0300':
                    self.TriggerEvent("Format", self.formatDict[data])

                if status == "80":
                    print "Device Busy"
                if status == "81":
                    print "Command Failed"
                if status == '00':
                    print "Command Success"
                return

            buffer += b
