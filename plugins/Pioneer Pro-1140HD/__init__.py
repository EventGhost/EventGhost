#
# Pioneer Serial
# ================
# Public Domain
#
#  Modified from Onkyo Serial by prostetnic, Bartman and Fiasco
#  I know a little about python programming, but honestly I don't
#  understand classes or how this plugin works :) J. T. Willhoite
#
# Revision history:
# -----------------
# 0.1 - initial

help = """\
Plugin to control Pioneer Elite Plasma Display PRO-1140HD via RS-232. 
Note: Pioneer PRO-1140HD cannot receive RS232 commands if the TV is in SR+ mode.  
Also keep in mind the Pioneer TV requires about a 2.5 second delay between commands or it will ignore the next command."""

import eg

eg.RegisterPlugin(
    name="Pioneer Pro-1140HD tv Serial",
    guid='{21442C6F-27B1-4EA1-9127-67C82BCBBC98}',
    author="J T Willhoite",
    version="0.1." + "$LastChangedRevision: 1181 $".split()[1],
    kind="external",
    description="Control Pioneer Pro-1140HD TV via RS232",
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

cmdList = (
    ('Power', None, None, None),  # Folder name
    #         ?                         Command name that appears in eventghost                      RS232 Code           Range
    ('PowerOff', 'Power Standby', 'POF', None),
    ('PowerOn', 'Power On', 'PON', None),
    ('Master Volume', None, None, None),
    ('VolumeUp10', 'Master Volume Up by 10', 'VOLUP0', None),
    ('VolumeDown10', 'Master Volume Down by 10', 'VOLDW0', None),
    ('VolumeSet', 'Set Master Volume (00-60)', 'VOL0', '00-60'),
    ('MuteOn', 'Mute Off', 'AMTS00', None),
    ('MuteOff', 'Mute On', 'AMTS01', None),
    ('Input Select Command', None, None, None),
    ('Input1', 'Input 1', 'INPS01', None),
    ('Input2', 'Input 2', 'INPS02', None),
    ('Input3', 'Input 3', 'INPS03', None),
    ('Input4', 'Input 4', 'INPS04', None),
    ('Input5', 'Input 5 HDMI', 'INPS05', None),
    ('Input6', 'Input 6 HDMI', 'INPS06', None),
    ('Input7', 'Input PC (VGA)', 'INPS07', None),
    ('Av Selection', None, None, None),
    ('AVStandard', 'Standard', 'AVSS01', None),
    ('AVDynamic', 'Dynamic', 'AVSS02', None),
    ('AVMovie', 'Movie', 'AVSS03', None),
    ('AVGame', 'Game', 'AVSS04', None),
    ('AVPure', 'Pure', 'AVSS06', None),
    ('AVUser', 'User', 'AVSS07', None),
    ('AVISF-Day', 'ISF-Day (after Calibration)', 'AVSS08', None),
    ('AVISF-Night', 'ISF-Night (after Calibration)', 'AVSS09', None),
    ('Screen Size', None, None, None),
    ('ScreenDot', 'Dot by Dot/Partial (PC Only)', 'SZMS00', None),
    ('Screen43', '4:3', 'SZMS01', None),
    ('ScreenFull', 'Full/Full 1080i', 'SZMS02', None),
    ('ScreenZoom', 'Zoom', 'SZMS03', None),
    ('ScreenWide', 'Wide', 'SZMS05', None),
    (None, None, None, None),

)


class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        self.plugin.serialThread.Write(self.cmd + "\x03")


class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(self.cmd + str(data) + "\x03")
        self.plugin.serialThread.ResumeReadEvents()


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write("\x02**" + str(data) + "\x03")
        self.plugin.serialThread.ResumeReadEvents()


class PioneerSerial(eg.PluginClass):

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
                    cmd = "\x02**" + cmd_cmd
                    parameterDescription = "Value: (%s)" % paramDescr

                Action.__name__ = cmd_name
                group.AddAction(Action)
            else:
                # Argumentless command
                class Action(CmdAction):
                    name = cmd_text
                    cmd = "\x02**" + cmd_cmd

                Action.__name__ = cmd_name
                group.AddAction(Action)

        group.AddAction(Raw)

        onOffDict = {
            'F': 'Off',
            'N': 'On',
        }

        muteDict = {
            'S00': 'Off',
            'S01': 'On',
        }

        inputDict = {
            'S01': 'Input1',
            'S02': 'Input2',
            'S03': 'Input3',
            'S04': 'Input4',
            'S05': 'Input5 HDMI',
            'S06': 'Input6 HDMI',
            'S07': 'PC (VGA)',
        }

        avselection = {
            'S01': 'Standard',
            'S02': 'Dynamic',
            'S03': 'Movie',
            'S04': 'Game',
            'S06': 'Pure',
            'S07': 'User',
            'S08': 'ISF Day',
            'S09': 'ISF Night',
        }

        self.commandDict = {
            'PO': ('Power', onOffDict),
            'AMT': ('Muting', muteDict),
            'AVS': ('AV Selection', avselection),
            'INP': ('Input', inputDict)
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

    def OnReceive(self, serial):
        buffer = ""
        while True:
            b = serial.Read(1, 0.1)
            if b == "\x1a":
                if not buffer.startswith("\x02**"):
                    return
                command = buffer[3:6]
                value = buffer[6:]

                # Generic
                if self.commandDict.has_key(command):
                    eventNameDict = self.commandDict[command][1]
                    if eventNameDict.has_key(value):
                        value = eventNameDict[value]
                    self.TriggerEvent(self.commandDict[command][0] + '.' + value)
                    return

                # This is left over from onkyo template, don't know if I need it or how to modify it
                # MasterVolume
                if command == "MVL":
                    self.TriggerEvent("MasterVolume", int(value, 16))
                    return

                # This is left over from onkyo template, don't know if I need it or how to modify it
                # Sleep Timer
                if command == "SLP":
                    payload = -1
                    if value == "OFF":
                        payload = 0
                    if len(value) == 2:
                        payload = int(value, 16)
                    self.TriggerEvent("SleepTimer", payload)
                    return

                self.TriggerEvent(command + "." + value, )
                return
            elif b == "":
                # nothing received inside timeout, possibly indicates erroneous data
                return
            buffer += b
