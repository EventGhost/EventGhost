#
# LG Plasma
# ================

# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
#

help = """\
Plugin to control LG  Receiver via RS-232
Small plugin to control 

LG 42PQ10, 50PQ10, 50PS11, 60PS11, 42PQ12, 50PQ12

plasma televisions
By Fiasco
<ul>
</ul>
"""

import eg

eg.RegisterPlugin(
    name="LG PS/PQ Plasma TV Serial",
    guid='{FC3E24B0-5BE1-4E77-91AF-4F3E29E376B1}',
    author="Revised by Fiasco for LG plasmas on 07/26/09",
    version="0.1." + "$LastChangedRevision: 809 $".split()[1],
    kind="external",
    description="Control LG plasma TV's via RS232",
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

import eg
import time

cmdList = (
    ('Power / Sleep', None, None, None),
    ('PowerOff', 'Power Standby', 'ka 00 00', None),
    ('PowerOn', 'Power On', 'ka 00 01', None),
    ('PowerState', 'Returns Power State', 'ka 00 ff', None),
    ('LowPower0', 'Power/Energy Savings Off', 'jq 00 00', None),
    ('LowPower1', 'Power/Energy Savings Minimum', 'jq 00 01', None),
    ('LowPower2', 'Power/Energy Savings Medium', 'jq 00 02', None),
    ('LowPower3', 'Power/Energy Savings Maximum', 'jq 00 03', None),
    ('GetLowPower', 'Get Power/Energy Mode', 'jq 00 ff', None),
    ('Sensor1', 'Intelligent Sensor Low', 'jq 00 10', None),
    ('Sensor2', 'Intelligent Sensor Medium', 'jq 00 11', None),
    ('Sensor3', 'Intelligent Sensor Maximum', 'jq 00 12', None),
    ('Input Select Command', None, None, None),
    ('DTVAntenna', 'DTV (Antenna)', 'xb 00 00', None),
    ('DTVCable', 'DTV (Cable)', 'xb 00 01', None),
    ('Analog Antenna', 'Analog (Antenna)', 'xb 00 10', None),
    ('Analog Cable', 'Analog (Cable)', 'xb 00 11', None),
    ('AV1', 'A/V 1', 'xb 00 20', None),
    ('AV2', 'A/V 2', 'xb 00 21', None),
    ('Component1', 'Component 1', 'xb 00 40', None),
    ('Component2', 'Component 2', 'xb 00 41', None),
    ('RGB-PC', 'RGB PC', 'xb 00 60', None),
    ('HDMI1', 'HDMI 1', 'xb 00 90', None),
    ('HDMI2', 'HDMI 2', 'xb 00 91', None),
    ('HDMI3', 'HDMI 3', 'xb 00 92', None),
    ('HDMI4', 'HDMI 4', 'xb 00 93', None),
    ('InputState', 'Returns Current Input', 'xb 00 ff', None),
    ('Channel Tuning', None, None, None),
    ('TuneChannel', 'Tune Channel (0-64, 0-100 in Hex, 0=---/MIN)', 'ma 00', '0-64'),
    ('TuneDTVChannel', 'Tune Channel DTV (0-999, 0-10000 in Hex, 0=---/MIN)', 'ma 00', '0-999'),
    ('ChannelAdd', 'Add Channel', 'mb 00 01', None),
    ('ChannelDel', 'Delete Channel', 'mb 00 00', None),
    ('IR Key Code', None, None, None),
    ('SendIR', 'Send IR Keycode(0-64, 0-100 in Hex, 0=---/MIN)', 'mc 00', '0-64'),
    ('Master Volume', None, None, None),
    ('VolumeSet', 'Set Master Volume (0-64, 0-100 in Hex, 0=---/MIN)', 'kf 00', '0-64'),
    ('VolumeGet', 'Get Volume', 'kf 00 ff', None),
    ('MuteOn', 'Mute On', 'kd 00 00', None),
    ('MuteOff', 'Mute Off', 'kd 00 01', None),
    ('MuteState', 'Returns Mute Status', 'kd 00 ff', None),
    ('Treble', 'Set Treble (0-64, 0-100 in Hex, 0=---/MIN)', 'kr 00', '0-64'),
    ('GetTreble', 'Get Treble', 'kr 00 ff', None),
    ('Bass', 'Set Bass (0-64, 0-100 in Hex, 0=---/MIN)', 'ks 00', '0-64'),
    ('GetBass', 'Get Bass', 'ks 00 ff', None),
    ('Balance', 'Set Balance (0-64, 0-100 in Hex, 0=---/MIN)', 'kt 00', '0-64'),
    ('GetBalance', 'Get Balance', 'kt 00 ff', None),
    ('Picture', None, None, None),
    ('AutoConfig', 'Auto Configuration', 'ju 0', None),
    ('Contrast', 'Set Contrast (0-64, 0-100 in Hex, 0=---/MIN)', 'kg 0', '0-64'),
    ('GetContrast', 'Get Contrast', 'kg 01 ff', None),
    ('Brightness', 'Set Brightness (0-64, 0-100 in Hex, 0=---/MIN)', 'kh 01', '0-64'),
    ('GetBrightness', 'Get Brightness', 'kh 01 ff', None),
    ('Color', 'Set Color (0-64, 0-100 in Hex, 0=---/MIN)', 'ki 01', '0-64'),
    ('GetColor', 'Get Color', 'ki 01 ff', None),
    ('Tint', 'Set Tint (0-64, 0-100 in Hex, 0=---/MIN)', 'kj 01', '0-64'),
    ('GetTint', 'Get Tint', 'kj 01 ff', None),
    ('Sharpness', 'Set Sharpness (0-64, 0-100 in Hex, 0=---/MIN)', 'kk 01', '0-64'),
    ('GetSharpness', 'Get Sharpness', 'kk 01 ff', None),
    ('ColorTemperature1', 'Set Color Tempeature 1', 'ku 01 00', None),
    ('ColorTemperature1', 'Set Color Tempeature 2', 'ku 01 01', None),
    ('ColorTemperature1', 'Set Color Tempeature 3', 'ku 01 02', None),
    ('GetColorTemperature', 'Get Color Temperature', 'ku 01 ff', None),
    ('Aspect Ratio', None, None, None),
    ('Aspect43', 'Aspect Ratio 4:3', 'kc 00 01', None),
    ('Aspect169', 'Aspect Ratio 16:9', 'kc 00 02', None),
    ('AspectZoom', 'Aspect Ratio Zoom', 'kc 00 04', None),
    ('AspectProgram', 'Aspect Ratio Set By Program', 'kc 00 06', None),
    ('AspectScan', 'Aspect Ratio Just Scan', 'kc 00 09', None),
    ('AspectCinema1', 'Aspect Ratio Cinema Zoom 1', 'kc 00 10', None),
    ('AspectCinema2', 'Aspect Ratio Cinema Zoom 2', 'kc 00 1f', None),
    ('AspectState', 'Return Aspect Ratio', 'kc 00 ff', None),
    ('Screen Mute', None, None, None),
    ('ScreenMuteOff', 'Screen Mute On TV Will show OSD', 'kd 00 01', None),
    ('ScreenMuteOn', 'Screen Mute On TV Will not show OSD', 'kd 00 01', None),
    ('ScreenMuteVideo', 'Video Out Mute', 'kd 00 10', None),
    ('ScreenMuteStatus', 'Get Screen Mute State', 'kd 00 ff', None),
    ('OSDSelectOn', 'OSD On', 'kl 00 01', None),
    ('OSDSelectOff', 'OSD Off', 'kl 00 00', None),
    ('GetOSDSelect', 'Get OSD Select State', 'kl 00 ff', None),
    ('ISMMethod1', 'Screen Saver Orbiter', 'jp 00 02', None),
    ('ISMMethod2', 'Screen Saver Normal', 'jp 00 08', None),
    ('ISMMethod3', 'Screen Saver White Wash', 'jp 00 04', None),
    ('ISMMethod4', 'Screen Saver Color Wash', 'jp 00 20', None),
    ('GetISMMethod', 'Get Screen Saver Method', 'jp 00 ff', None),
    ('Remote Control Lock', None, None, None),
    ('RemoteLockOn', 'Remote Lock On', 'km 00 01', None),
    ('RemoteLockOff', 'Remote Lock Off', 'km 00 00', None),
    ('GetRemoteLock', 'Get Remote Lock State', 'km 00 ff', None),
    (None, None, None, None),
)


class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        print (self.cmd)
        # value = binascii.a2b_hex(self.cmd)

        self.plugin.serialThread.SuspendReadEvents()

        self.plugin.serialThread.Write(self.cmd + chr(13))
        # self.plugin.serialThread.Write(value)
        self.plugin.serialThread.ResumeReadEvents()


class PowerOnAction(eg.ActionClass):
    name = 'Power On Synchronously'

    def __call__(self):
        print ('ka 00 ff')

        self.plugin.serialThread.SuspendReadEvents()

        self.plugin.serialThread.Write('ka 00 ff' + chr(13))
        # b = self.plugin.serialThread.Read(11, 0.1)
        b = ""
        cha = self.plugin.serialThread.Read(1, 0.2)
        while cha != '':
            b = b + cha
            cha = self.plugin.serialThread.Read(1, 0.2)
        print(b)

        self.plugin.serialThread.Write('ka 00 ff' + chr(13))
        # b = self.plugin.serialThread.Read(11, 0.1)
        b = ""
        cha = self.plugin.serialThread.Read(1, 0.2)
        while cha != '':
            b = b + cha
            cha = self.plugin.serialThread.Read(1, 0.2)
        print(b)

        # If TV not on 
        if b[5:9] != 'OK01':
            print ('Turning On:' + b[5:9])
            self.plugin.serialThread.Write('ka 00 01' + chr(13))
            b = ""
            cha = self.plugin.serialThread.Read(1, 0.2)
            while cha != '':
                b = b + cha
                cha = self.plugin.serialThread.Read(1, 0.2)
            # b = self.plugin.serialThread.Read(11, 0.1)
            print(b)

            TimeoutCounter = 0
            # b[5:9] != 'OK01'
            while TimeoutCounter < 17:
                print ('Checking state:' + b[5:9])
                self.plugin.serialThread.Write('ka 00 ff' + chr(13))
                b = ""
                cha = self.plugin.serialThread.Read(1, 0.5)
                while cha != '':
                    b = b + cha
                    cha = self.plugin.serialThread.Read(1, 0.5)
                # b = self.plugin.serialThread.Read(11, 0.1)
                print(b)
                time.sleep(1)
                TimeoutCounter = TimeoutCounter + 1

        print ('Turned On')

        self.plugin.serialThread.ResumeReadEvents()


class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        data = eg.ParseString(data)
        data = data.upper()
        print (self.cmd + str(data))
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(self.cmd + chr(13))
        self.plugin.serialThread.ResumeReadEvents()


class TuneDTVAction(eg.ActionWithStringParameter):
    name = 'Tune DTV channel'

    def __call__(self, data):
        data = eg.ParseString(data)
        data = data.upper()
        ChannelNo = hex(int(data))[2:].zfill(4)
        self.plugin.serialThread.SuspendReadEvents()
        print(elf.cmd + ' ' + ChannelNo[0:2] + ' ' + ChannelNo[2:4] + ' 10')
        self.plugin.serialThread.Write(self.cmd + ' ' + ChannelNo[0:2] + ' ' + ChannelNo[2:4] + ' 10' + chr(13))
        self.plugin.serialThread.ResumeReadEvents()


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()

        self.plugin.serialThread.Write(data + chr(13))
        self.plugin.serialThread.ResumeReadEvents()


class lgSerial(eg.PluginClass):

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

                if cmd_name == 'TuneDTVChannel':
                    class Action(TuneDTVAction):
                        name = actionName
                        cmd = cmd_cmd
                        parameterDescription = "Value: (%s)" % paramDescr
                else:
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
        group.AddAction(PowerOnAction)

        self.onOffDict = {
            '00': 'Off',
            '01': 'On',
        }

        self.inputDict = {
            '00': 'DTV Antenna',
            '01': 'DTV Cable',
            '10': 'Analog Antenna',
            '11': 'Analog Cable',
            '20': 'AV1',
            '21': 'AV2',
            '40': 'Component 1',
            '41': 'Component 2',
            '60': 'RGB-PC',
            '90': 'HDMI 1',
            '91': 'HDMI 2',
            '92': 'HDMI 3',
            '93': 'HDMI 4'
        }

        self.aspectDict = {
            '01': '4:3',
            '02': '16:9',
            '04': 'Zoom',
            '06': 'Set By Program',
            '09': 'Just Scan',
            '10': 'Cinema Zoom 1',
            '11': 'Cinema Zoom 2'
        }

        self.ISMModes = {
            '02': 'Orbiter',
            '04': 'White Wash',
            '08': 'Normal',
            '20': 'Color Wash'
        }

    def __start__(self, port):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 9600, '8N1')
        # self.serialThread.SetRts()
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
            # b = binascii.hexlify(b)
            if b == '':
                return
            print b
