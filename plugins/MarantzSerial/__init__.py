eg.RegisterPlugin(
    name = "Marantz AV Receiver",
    author = "Dexter",
    version = "1.0.1093",
    kind = "external",
    guid = "{2189A326-0BAC-4D81-B69A-DCCD19060BAB}",
    url = "http://www.eventghost.org/forum/viewtopic.php?t=747",
    description = ('This plugin allows you to control your <a href="http://www.marantz.com">Marantz</a> \
                    SR-series receiver through it\'s serial port.\n\n\
                    <p>The plugin can send the commands directly to the serial port as well as to \
                    the <a href="http://daniel.vvtp.tudelft.nl/marantzcontrol/">MarantzControl</a> application.</p>\n\
                    <br><br>\
                    <p><b>Error messages:</b></p>\
                    <p><i>Unable to open serial port</i><br>The serial port could not be opened. Make sure the port is not used by another application.</p>\
                    <p><i>No response</i><br>The command was sent succesfully, but no response was received. Check if the serial cable is connected, \
                    if the correct serial port is selected and if the receiver is switched on.</p>\
                    <p><i>Bad response</i><br>An incorrect response was received. Make sure you connect to a Marantz SR-series receiver.</p>\
                    <p><i>Command not available in this mode</i><br>The command is not supported by this method (via MarantzSerial or directly to serial port.</p>\
                    <p><i>MarantzSerial application not found</i><br>The MarantzSerial application was not found. Make sure the application is started.</p>\
                    <p><i>Unable to send command to MarantzSerial</i><br>The MarantzSerial application is located, but an error occured while sending a message.</p>\
                    <br><br>\
                    <p>Note: Only the most important commands are implemented and no events are currently available</p>'),
)


# Now we import some other things we will need later
import math
import sys
import time
from ctypes import WinDLL
from ctypes.wintypes import ATOM,LPCSTR
from win32gui import FindWindow, SendMessageTimeout, GetWindowText
from win32con import WM_APP, WM_USER, SMTO_BLOCK, SMTO_ABORTIFHUNG
import new


# Export GlobalAddAtom function
_kernel32 = WinDLL("kernel32")
GlobalAddAtomA = _kernel32.GlobalAddAtomA
GlobalAddAtomA.restype = ATOM
GlobalAddAtomA.argtypes = [LPCSTR]
GlobalAddAtom = GlobalAddAtomA # alias


# Define commands
# (name, title, description (same as title if None), command)
commandsList = (
('Power',
(('PowerOn', 'Power on', None, '/power on', '@PWR:2'),
('PowerOff', 'Power off', None, '/power off', '@PWR:1'),
('PowerToggle', 'Power toggle', None, '/power toggle', '@PWR:0'))),

('Input',
(('InputTV', 'Select TV input', None, '/input tv', '@SRC:1'),
('InputDVD', 'Select DVD input', None, '/input dvd', '@SRC:2'),
('InputVCR1', 'Select VCR1 input', None, '/input vcr1', '@SRC:3'),
('InputVCR2', 'Select VCR2 input', None, '/input vcr2', '@SRC:4'),
('InputDSS', 'Select DSS input', None, '/input dss', '@SRC:5'),
('InputLD', 'Select LD input', None, '/input ld', '@SRC:6'),
('InputAux1', 'Select Aux 1 input', None, '/input aux1', '@SRC:9'),
('InputAux2', 'Select Aux 2 input', None, '/input aux2', '@SRC:A'),
('InputCD', 'Select CD input', None, '/input cd', '@SRC:C'),
('InputCD-R', 'Select CD-R input', None, '/input cd-r', '@SRC:D'),
('InputTape', 'Select Tape input', None, '/input tape', '@SRC:E'),
('InputTuner1', 'Select Tuner 1 input', None, '/input tuner1', '@SRC:F'),
('InputTuner1FM', 'Select Tuner 1 FM input', None, '/input tuner1', '@SRC:G'),
('InputTuner1AM', 'Select Tuner 1 AM input', None, '/input tuner1', '@SRC:H'),
('InputTuner2', 'Select Tuner 2 input', None, '/input tuner2', '@SRC:J'),
('InputTuner2FM', 'Select Tuner 2 FM input', None, '/input tuner2', '@SRC:K'),
('InputTuner2AM', 'Select Tuner 2 AM input', None, '/input tuner2', '@SRC:L'))),

('Input mode',
(('InputmodeAuto', 'Inputmode auto', 'Sets inputmode to auto', '/inputmode auto', '@INP:0'),
('InputmodeAnalog', 'Inputmode analog', 'Sets inputmode to analog', '/inputmode analog', '@INP:1'),
('InputmodeDigital', 'Inputmode digital', 'Sets inputmode to digital', '/inputmode digital', '@INP:2'))),

('7.1 Channel Input',
(('ChannelInput71On', '7.1 channel input on', 'Sets the 7.1 channel input on', None, '@71C:2'),
('ChannelInput71Off', '7.1 channel input off', 'Sets the 7.1 channel input off', None, '@71C:1'),
('ChannelInput71Toggle', '7.1 channel input toggle', 'Toggles the 7.1 channel input', None, '@71C:0'))),

('Surround mode',
(('SurroundAuto', 'Select Auto surround mode', None, '/surround auto', '@SUR:00'),
('SurroundStereo', 'Select Stereo surround mode', None, '/surround stereo', '@SUR:01'),
('SurroundMulti', 'Select Multi Channel Stereo surround mode', None, '/surround multi', '@SUR:0H'),
('SurroundVirtual', 'Select Virtual surround mode', None, '/surround virtual', '@SUR:0L'),
('SurroundDirect', 'Select Pure Direct surround mode', None, '/surround direct', '@SUR:0T'),
('SurroundDolby', 'Select Dolby surround mode', None, '/surround dolby', '@SUR:02'),
('SurroundDolbyDigitalEx', 'Select Dolby Digital EX surround mode', None, '/surround ddex', '@SUR:0A'),
('SurroundDolbyProLogic', 'Select Dolby ProLogic surround mode', None, '/surround dpl', '@SUR:09'),
('SurroundDolbyProLogic2Movie', 'Select Dolby ProLogic II Movie surround mode', None, '/surround dpl2mv', '@SUR:04'),
('SurroundDolbyProLogic2Music', 'Select Dolby ProLogic II Music surround mode', None, '/surround dpl2ms', '@SUR:06'),
('SurroundDolbyProLogic2Game', 'Select Dolby ProLogic II Game surround mode', None, '/surround dpl2gm', '@SUR:08'),
('SurroundDTS', 'Select DTS surround mode', None, '/surround dts', '@SUR:0M'),
('SurroundDTSES', 'Select DTS ES surround mode', None, '/surround dtses', '@SUR:0E'),
('SurroundDTSNeo6Cinema', 'Select DTS Neo6 Cinema surround mode', None, '/surround neo6cinema', '@SUR:0F'),
('SurroundDTSNeo6Music', 'Select DTS Neo6 Music surround mode', None, '/surround neo6music', '@SUR:0G'),
('SurroundCS2Cinema', 'Select CircleSurround II Cinema surround mode', None, '/surround cs2cinema', '@SUR:0I'),
('SurroundCS2Music', 'Select CircleSurround II Music surround mode', None, '/surround cs2music', '@SUR:0J'),
('SurroundCS2Mono', 'Select CircleSurround II Mono surround mode', None, '/surround cs2mono', '@SUR:0K'))),

('Night mode',
(('NightModeOn', 'Nighmode on', 'Sets nightmode (dynamic range compression) on', None, '@NGT:2'),
('NightModeOff', 'Nightmode off', 'Sets nightmode (dynamic range compression) off', None, '@NGT:1'),
('NightModeToggle', 'Nightmode toggle', 'Toggles nightmode (dynamic range compression)', None, '@NGT:0'))),

('Hometheater equalizer (HT-EQ)',
(('HometheaterEqualizerOn', 'Hometheater equalizer (HT-EQ) on', 'Sets the Hometheater equalizer (HT-EQ) on', None, '@REQ:2'),
('HometheaterEqualizerOff', 'Hometheater equalizer (HT-EQ) off', 'Sets the Hometheater equalizer (HT-EQ) off', None, '@REQ:1'),
('HometheaterEqualizerToggle', 'Hometheater equalizer (HT-EQ) toggle', 'Toggles the Hometheater equalizer (HT-EQ)', None, '@REQ:0'))),

('Audio Attenuation (ATT)',
(('AudioAttenuationOn', 'Audio attenuation (ATT) on', 'Sets the audio attenuation (ATT) on', None, '@ATT:2'),
('AudioAttenuationOff', 'Audio attenuation (ATT) off', 'Sets the audio attenuation (ATT) off', None, '@ATT:1'),
('AudioAttenuationToggle', 'Audio attenuation (ATT) toggle', 'Toggles the audio attenuation (ATT)', None, '@ATT:0'))),

('Mute',
(('MuteOn', 'Mute on', None, '/mute on', '@AMT:2'),
('MuteOff', 'Mute off', None, '/mute off', '@AMT:1'),
('MuteToggle', 'Mute toggle', None, '/mute toggle', '@AMT:0'))),

)



class MarantzSerialAction(eg.ActionClass):

    def __call__(self):
        self.plugin.SendCommand(self.appcmd, self.serialcmd)



class MarantzSerialSetVolumeAbsolute(eg.ActionWithStringParameter):
    name='Set absolute volume'
    description='Sets the absolute volume'

    def __call__(self, volume):
        return self.plugin.SetVolume(volume, False)

    def GetLabel(self, volume):
        return "Set Absolute Volume to %d" % volume

    def Configure(self, volume=-40):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(volume, min=-70, max=10)
        panel.AddLine("Set absolute volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



class MarantzSerialSetVolumeRelative(eg.ActionWithStringParameter):
    name='Set relative volume'
    description='Sets the relative volume'

    def __call__(self, volume):
        return self.plugin.SetVolume(volume, True)

    def GetLabel(self, volume):
        return "Set Relative Volume to %d" % volume

    def Configure(self, volume=0):
        panel = eg.ConfigPanel(self)
        valueCtrl = panel.SpinIntCtrl(volume, min=-100, max=100)
        panel.AddLine("Set relative volume to", valueCtrl)
        while panel.Affirmed():
            panel.SetResult(valueCtrl.GetValue())



class MarantzSerial(eg.PluginClass):

    def __init__(self):
        self.serial = None
        self.response = None
        self.method = 0
        self.hwndMarantzControl = None

        for groupname, list in commandsList:
            group = self.AddGroup(groupname)
            for classname, title, desc, app, serial in list:
                if desc is None:
                    desc = title
                clsAttributes = dict(name=title, description=desc, appcmd=app, serialcmd=serial)
                cls = new.classobj(classname, (MarantzSerialAction,), clsAttributes)
                group.AddAction(cls)

        group = self.AddGroup('Volume')
        group.AddAction(MarantzSerialSetVolumeAbsolute)
        group.AddAction(MarantzSerialSetVolumeRelative)


    def FindMarantzWindow(self):
        # Old handle still valid?
        if self.hwndMarantzControl is not None:
            if GetWindowText(self.hwndMarantzControl) == 'MarantzControl':
                return True

        # Search for window
        self.hwndMarantzControl = FindWindow(None, 'MarantzControl')
        if self.hwndMarantzControl != 0:
            return True

        # Nothing found
        return False


    def SendCommandApp(self, cmd):
        try:
            if self.FindMarantzWindow():
                hAtom = GlobalAddAtom(cmd)
                SendMessageTimeout(
                    self.hwndMarantzControl,
                    WM_APP+102,
                    hAtom,
                    0,
                    SMTO_BLOCK|SMTO_ABORTIFHUNG,
                    500 # Wait at most 500ms
                )
                time.sleep(0.1) # Wait 100ms for command to be processed by MarantzSerial
                return False

            else:
                self.PrintError("MarantzControl application not found")
                return True

        except:
            self.PrintError("Unable to send command to MarantzControl")
            return True


    def SendCommandSerial(self, cmd):
        if self.serial is None:
            return True

        # Send command
        cmd += '\r'
        self.serial.write(cmd)

        # Wait for response (if any)
        self.response = ""
        while True:

            # Wait for next char
            ch = self.serial.read(1)

            # Timeout occured?
            if ch == '':
                self.response = None
                self.PrintError("No response")
                return True

            # End-of-response?
            elif ch == '\r':
                break

            # Add received char
            self.response += ch

        # Seperator found?
        seppos = self.response.find(':')
        if seppos == -1:
            self.PrintError("Bad response")
            return True

        # Is this response a response on the sent command?
        seppos += 1 # (include ':')
        if cmd[0:seppos] != self.response[0:seppos]:
            self.PrintError("Bad response")
            return True

        # Strip anything before seperator and return ok
        self.response = self.response[seppos:].strip()
        return False


    def GetResponseInt(self):
        if (self.response[0] == '-' or self.response[0] == '+'):
            if not self.response[1:].isdigit():
                self.PrintError("Bad response")
                return None

        elif not self.response.isdigit():
            self.PrintError("Bad response")
            return None

        return int(self.response)


    def SendCommand(self, appcmd, serialcmd):
        if self.method == 0:
            if appcmd is None:
                self.PrintError("Command not available in this mode")
                return True
            result = self.SendCommandApp(appcmd)

        elif self.method == 1:
            if serialcmd is None:
                self.PrintError("Command not available in this mode")
                return True
            result = self.SendCommandSerial(serialcmd)

        return result


    def SetVolume(self, volume, relative):
        if self.method == 0:
            if relative:
                self.SendCommandApp("/volume %d" % volume)

        elif self.method == 1:
            if relative:
                if self.SendCommandSerial("@VOL:?"):
                    return
                current = self.GetResponseInt()
                if current is None:
                    return
                volume += current

            if volume > 10:
                volume = 10
            elif volume < -70:
                volume = -70

            self.SendCommandSerial("@VOL:0%+.2d" % (volume))
            return volume


    def __start__(self, method=0, port=0):
        self.method = method
        if method == 1:
            try:
                self.serial = eg.SerialPort(port)
                self.serial.baudrate = 9600
                self.serial.timeout = 0.5
                self.serial.setDTR(1)
                self.serial.setRTS(1)
            except:
                self.PrintError("Unable to open serial port")


    def __stop__(self):
        if self.serial is not None:
            self.serial.close()
            self.serial = None


    def Configure(self, method=0, port=0):
        methodCtrl = None
        portCtrl = None

        def OnMethodChange(self):
            if methodCtrl.GetValue() == 1:
                portCtrl.Enable()
            else:
                portCtrl.Disable()

        panel = eg.ConfigPanel(self)
        methodCtrl = panel.Choice(method, choices=("Via MarantzControl", "Directly to serial port"))
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Method:", methodCtrl)
        panel.AddLine("Port:", portCtrl)

        methodCtrl.Bind(wx.EVT_CHOICE, OnMethodChange)
        OnMethodChange(self)

        while panel.Affirmed():
            panel.SetResult(methodCtrl.GetValue(), portCtrl.GetValue())

