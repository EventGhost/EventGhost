#
# Panasonic Serial
# ================

# Public Domain
#
#
# Revision history:
# -----------------
# 0.1 - initial
#
# Derived from Onkyo Stereo plugin.
#


help = """\
Plugin to control Panasonic Projectors via RS-232.
Developed for PT-AE-3000U, but should work with
different models that use similar control strings
(e.g. the PT-AE4000U)."""

import eg

eg.RegisterPlugin(
    name="Panasonic PT-AE3000U Projector",
    guid='{3FC30075-B17B-4737-A47A-8875D3A4CC27}',
    author="Ben Mathews",
    version="0.1." + "$LastChangedRevision: 0.3.7.r965$".split()[1],
    kind="external",
    description="Control Panasonic PT-AE3000U Projector via RS232",
    help=help,
    canMultiLoad=True,
    createMacrosOnAdd=True
)

STX = chr(0x02)
ETX = chr(0x03)

cmdList = (
    ('Power / Sleep', None, None, None),
    ('PowerOff', 'Power Standby', 'POF', None),
    ('PowerOn', 'Power On', 'PON', None),
    ('PowerState', 'Returns Power State', 'QPW', None),
    ('Freeze', None, None, None),
    ('FreezeOff', 'Freeze Off', 'OFZ:0', None),
    ('FreezeOn', 'Freeze On', 'OFZ:1', None),
    ('FreezeState', 'Returns Freeze State', 'QFZ', None),
    ('Input', None, None, None),
    ('InputComponent1', 'Component Video 1', 'IIS:CP1', None),
    ('InputComponent2', 'Component Video 2', 'IIS:CP2', None),
    ('InputSVideo', 'S Video', 'IIS:SVD', None),
    ('InputVideo', 'Video', 'IIS:VID', None),
    ('InputHDMI1', 'HDMI 1', 'IIS:HD1', None),
    ('InputHDMI2', 'HDMI 2', 'IIS:HD2', None),
    ('InputHDMI3', 'HDMI 3', 'IIS:HD3', None),
    ('InputState', 'Returns Video Input', 'QIN', None),
    ('Sleep Timer', None, None, None),
    ('SleepTimerOff', 'Sleep Timer Off', 'OOT:0', None),
    ('SleepTimer60Min', 'Sleep Timer: 60 Minutes', 'OOT:1', None),
    ('SleepTimer90Min', 'Sleep Timer: 90 Minutes', 'OOT:2', None),
    ('SleepTimer120Min', 'Sleep Timer: 120 Minutes', 'OOT:3', None),
    ('SleepTimer150Min', 'Sleep Timer: 150 Minutes', 'OOT:4', None),
    ('SleepTimer180Min', 'Sleep Timer: 180 Minutes', 'OOT:5', None),
    ('SleepTimer210Min', 'Sleep Timer: 210 Minutes', 'OOT:6', None),
    ('SleepTimer240Min', 'Sleep Timer: 240 Minutes', 'OOT:7', None),
    ('SleepTimerState', 'Returns Sleep Timer State', 'QOT', None),
    ('Picture Mode', None, None, None),
    ('PictureModeNormal', 'Picture Mode: Normal', 'VPM:NOR', None),
    ('PictureModeDynamic', 'Picture Mode: Dynamic', 'VPM:DYN', None),
    ('PictureModeColor1', 'Picture Mode: Color1', 'VPM:CL1', None),
    ('PictureModeColor2', 'Picture Mode: Color2', 'VPM:CL2', None),
    ('PictureModeCinema1', 'Picture Mode: Cinema1', 'VPM:CN1', None),
    ('PictureModeCinema2', 'Picture Mode: Cinema2', 'VPM:CN2', None),
    ('PictureModeCinema3', 'Picture Mode: Cinema3', 'VPM:CN3', None),
    ('PictureModeState', 'Returns Picture Mode State', 'QPM', None),
    ('Picture Blanking', None, None, None),
    ('TogglePictureBlank', 'Toggle Picture Blanking', 'OSH', None),
    ('PictureBlankState', 'Returns Picture Blanking State', 'QSH', None),
    ('Waveform Generator', None, None, None),
    ('WaveformGeneratorOff', 'Waveform Generator Off', 'OWM:0', None),
    ('WaveformGeneratorFullScanY', 'Waveform Generator: Full Scan (Y)', 'OWM:1', None),
    ('WaveformGeneratorFullScanR', 'Waveform Generator: Full Scan (R)', 'OWM:2', None),
    ('WaveformGeneratorFullScanG', 'Waveform Generator: Full Scan (G)', 'OWM:3', None),
    ('WaveformGeneratorFullScanB', 'Waveform Generator: Full Scan (B)', 'OWM:4', None),
    ('WaveformGeneratorSingleLineScanY', 'Waveform Generator: Single Line Scan (Y)', 'OWM:5', None),
    ('WaveformGeneratorSingleLineScanR', 'Waveform Generator: Single Line Scan (R)', 'OWM:6', None),
    ('WaveformGeneratorSingleLineScanG', 'Waveform Generator: Single Line Scan (G)', 'OWM:7', None),
    ('WaveformGeneratorSingleLineScanB', 'Waveform Generator: Single Line Scan (B)', 'OWM:8', None),
    ('Aspect Ratio', None, None, None),
    ('CycleAspectRatio', 'Cycle Through Aspect Ratio Settings', 'VS1', None),
    (None, None, None, None),
)


class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        self.plugin.last_cmd = self.cmd
        self.plugin.serialThread.Write(STX + self.cmd + ETX)


class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(STX + self.cmd + ":" + cstr(data) + ETX)
        self.plugin.last_cmd = self.cmd
        self.plugin.serialThread.ResumeReadEvents()


class Raw(eg.ActionWithStringParameter):
    name = 'Send Raw command'

    def __call__(self, data):
        self.plugin.serialThread.SuspendReadEvents()
        self.plugin.serialThread.Write(STX + str(data) + ETX)
        self.plugin.last_cmd = self.cmd
        self.plugin.serialThread.ResumeReadEvents()


class PanasonicSerial(eg.PluginClass):

    def __init__(self):
        self.serial = None
        self.last_cmd = ""
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

        onOffDict = {
            '000': 'Off',
            '001': 'On'
        }
        freezeDict = {
            '0': 'Off',
            '1': 'On'
        }
        inputSignalStatusDict = {
            'CP1': 'Component 1 In',
            'CP2': 'Component 2 In',
            'SVD': 'S-Video In',
            'VID': 'Video In',
            'HD1': 'HDMI 1 In',
            'HD2': 'HDMI 2 In',
            'HD3': 'HDMI 3 In',
            'RG1': 'Computer In'
        }
        offTimerStatusDict = {
            '0': 'Off',
            '1': '60 Min',
            '2': '90 Min',
            '3': '120 Min',
            '4': '150 Min',
            '5': '180 Min',
            '6': '210 Min',
            '7': '240 Min'
        }
        pictureModeStatusDict = {
            'NOR': 'Normal',
            'DYN': 'Dynamic',
            'CL1': 'Color 1',
            'CL2': 'Color 2',
            'CN1': 'Cinema 1',
            'CN2': 'Cinema 2',
            'CN3': 'Cinema 3'
        }
        blankStatusDict = {
            '0': 'Off',
            '1': 'On'
        }
        waveformStatusDict = {
            '0': 'Off',
            '1': 'Full Scan (Y)',
            '2': 'Full Scan (R)',
            '3': 'Full Scan (G)',
            '4': 'Full Scan (B)',
            '5': 'Single Line Scan (Y)',
            '6': 'Single Line Scan (R)',
            '7': 'Single Line Scan (G)',
            '8': 'Single Line Scan (B)'
        }
        self.commandDict = {
            'QPW': ('Power Status', onOffDict),
            'QFZ': ('Freeze Status', freezeDict),
            'QIN': ('Input Signal Status', inputSignalStatusDict),
            'QOT': ('Off Timer Status', offTimerStatusDict),
            'QPM': ('Picture Mode Status', pictureModeStatusDict),
            'QSH': ('Blank Status', blankStatusDict),
            'QWM': ('Waveform Status', waveformStatusDict)
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
            if b == ETX:
                if not buffer.startswith(STX):
                    return
                command = self.last_cmd
                value = buffer[1:]

                # Generic
                if self.commandDict.has_key(command):
                    eventNameDict = self.commandDict[command][1]
                    if eventNameDict.has_key(value):
                        value = eventNameDict[value]
                    self.TriggerEvent(self.commandDict[command][0] + '.' + value)
                    return

                self.TriggerEvent(command + "." + value, )
                return
            elif b == "":
                # nothing received inside timeout, possibly indicates erroneous data
                return
            buffer += b
