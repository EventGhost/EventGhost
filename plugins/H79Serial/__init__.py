#
# H79Serial V0.2
# ==============
# Written by Oliver Wagner, <owagner@hometheatersoftware.com>
# Public Domain
#
# Revision history:
# -----------------
# 0.1 - initial
# 0.2 - EventGhost 0.3.1+ compatibility
#

help = """\
Commands are taken straight out of the RS232_H79.pdf document
available from the Optoma website. Please note that, at least
with the documented command set, the serial input is pretty much
just a remote replacement, i.e. most of the serial commands
refer to remote functions, and you need to fiddle with
Up, Down, Left, Right and Enter to actually change values.
Yes, this sucks.

Projector replies are returned to EventGhost as events."""

eg.RegisterPlugin(
    name = "Optoma H79 Serial",
    author = "Oliver Wagner",
    version = "0.2.1093",
    kind = "external",
    description = "Control an Optoma H79 projector via RS232",
    guid = "{776F4F93-93E3-4587-875C-6B3817D44329}",
    help = help,
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARn"
        "QU1BAACxjwv8YQUAAAAgY0hSTQAAeiYAAICEAAD6AAAAgOgAAHUwAADqYAAAOpgAABdw"
        "nLpRPAAAABZ0RVh0U29mdHdhcmUAUGFpbnQuTkVUIDIuNmyodLUAAAJCSURBVDhPpZNb"
        "bxJRFIWtIQVaBmFA7jCUAcr9futQSoFQKIg0sfqs6YMmPumbhsQHr9E02liDiZqmbQoo"
        "tMVL/CU+6K9ZPTMppHFoYuIk83L2Wd9ee2edqd9/fl34r48H/PVLvv8cYvPNJlqPWnj8"
        "/Cn2DnYx4Z6gOyuWfNxpo7l+De5ABJ5QDPOhKFhfEDZ2HuVaHa9ev0Snt8/DFCPgGNDt"
        "7aLWXEN0YQneaAI2lwdmhoXZ7oTDG4DTFwK3XMR2ewuHx/2xozGAp6fzJYSSGegtDJS0"
        "DiatA15DGHaLG3Mev+Bq485tDI6+iAF8gStViF03KLUWCpUGapUeJpqFy+CF3mhFIJZG"
        "oVJDb9AVAxrr14mDImidUehOa+xwmMJgaQYqAqK1BrKPEFK5ZXT7EwArjSYSpHhJo4NR"
        "ZycCC+RKGlL5LKZlM8TVZWEPqVwBnw8njFBavYLF8ioMNh8BeODUBkERgEyugJQANAYz"
        "vOE4cuUqBsOBeIRCeQXF+hpiXBW0MULGsGKGUkE6q4SSuLLMuUhtCaV6A19/DMWAmxu3"
        "EE5lka9eRWrxBsxsFmodAxPjINaDCMTTcPkjuHvvPi/OiHIw/NYX5o9zeXDFChYKdSET"
        "vkgC0UwOvlgKSS6Hvc7kIE3xxAeth2RpFKzErj+aRDidFTqb7C4hjVvvtkfdnSIHpwfK"
        "Jy+egSGXZQoV5JQaFK0HRwL2YefTSHyR3JWcB+CTyc/n3O8c4G37PQbHR7xw+l8e0yjW"
        "44dynujs+Qnye/WIemQx5AAAAABJRU5ErkJggg=="
    ),
)

import thread
import time
import re


cmdList = (
('PowerOn', 'Power On', 'OKOKOKOKOK', None ),
('PowerOff', 'Power Off', '* 0 IR 002', None ),
('Source', 'Source', '* 0 IR 003', None ),
('VKeyStone', 'V. KeyStone', '* 0 IR 004', None ),
('Zoom', 'Zoom', '* 0 IR 005', None ),
('Freeze', 'Freeze', '* 0 IR 007', None ),
('Menu', 'Menu',  '* 0 IR 008', None ),
('Up', 'Up', '* 0 IR 009', None ),
('Down', 'Down', '* 0 IR 010', None ),
('Right', 'Right', '* 0 IR 011', None ),
('Left', 'Left', '* 0 IR 012', None ),
('Enter', 'Enter', '* 0 IR 013', None ),
('ReSync', 'Re-Sync', '* 0 IR 014', None ),
('SourceSVideo', 'Source S-Video', '* 0 IR 018', None ),
('SourceCompositeVideo', 'Source Composite Video', '* 0 IR 019', None ),
('Aspectratio169', 'Aspect ratio 16:9', '* 0 IR 021', None ),
('HKeyStone', 'H. KeyStone', '* 0 IR 023', None ),
('VideoMute', 'Video Mute(Hide)', '* 0 IR 024', None ),
('Brightness', 'Brightness', '* 0 IR 025', None ),
('Contrast', 'Contrast', '* 0 IR 026', None ),
('ColorTemperature', 'Color Temperature', '* 0 IR 027', None ),
('RedContrast', 'Advanced adjustment: Red contrast', '* 0 IR 028', None ),
('GreenContrast', 'Advanced adjustment: Green contrast', '* 0 IR 029', None ),
('BlueContrast', 'Advanced adjustment: Blue contrast', '* 0 IR 030', None ),
('RedBrightness', 'Advanced adjustment: Red Brightness', '* 0 IR 031', None ),
('GreenBrightness', 'Advanced adjustment: Green Brightness', '* 0 IR 032', None ),
('BlueBrightness', 'Advanced adjustment: Blue Brightness', '* 0 IR 033', None ),
('FormatMode', 'Format Mode', '* 0 IR 034', None ),
('Mode', 'Mode', '* 0 IR 035', None ),
('SignalHorizontal', 'Signal: Horizontal', '* 0 IR 036', None ),
('SignalVertical', 'Signal: Vertical', '* 0 IR 037', None ),
('SignalFrequency', 'Signal: Frequency', '* 0 IR 038', None ),
('SignalPhase', 'Signal: Phase', '* 0 IR 039', None ),
('AspectNative', 'Aspect Ratio: Native', '* 0 IR 040', None ),
('AspectWindow', 'Aspect Ratio: Window', '* 0 IR 041', None ),
('AspectLetterBox', 'Aspect Ration : Letter Box', '* 0 IR 042', None ),
('Language', 'Language', '* 0 IR 043', None ),
('Bulb', 'Bulb (Lamp information)', '* 0 IR 044', None ),
('AutoImageOn', 'Auto Image: On', '* 0 IR 045', None ),
('AutoImageOff', 'Auto Image: Off', '* 0 IR 047', None ),
('AutoShutdownOn', 'Auto Shutdown: On', '* 0 IR 047', None ),
('AutoShutdownOff', 'Auto Shutdown: Off', '* 0 IR 048', None ),
('SourceBNC', 'Source: BNC terminal', '* 0 IR 049', None ),
('Sharpness', 'Sharpness', '* 0 IR 050', None ),
('SourceDVI', 'Source: DVI terminal', '* 0 IR 051', None ),
('SourceRCA', 'Source: RCA terminal', '* 0 IR 052', None ),
('Color', 'Color', '* 0 IR 053', None ),
('TINT', 'TINT', '* 0 IR 054', None ),
('ImageMode', 'Image mode', '* 0 IR 055', None ),
('WhitePeaking', 'White peaking', '* 0 IR 056', None ),

('Raw', 'Send Raw command', '', '*'),
)

class H79Serial(eg.PluginClass):

    def __init__(self):
        self.serial = None
        group = topGroup = self

        def createWriter(cmd):
            def write(self):
                self.plugin.serial.write(cmd)
                self.plugin.serial.write(chr(13))
            return write

        for cmd_name, cmd_text, cmd_cmd, cmd_rangespec in cmdList:
            if cmd_text is None:
                # New subgroup, or back up
                if cmd_name is None:
                    group = topGroup
                else:
                    group = topGroup.AddGroup(cmd_name)
            elif cmd_rangespec is not None:
                # Command with argument
                class ArgHandler(eg.ActionWithStringParameter):
                    name = cmd_name
                    description = cmd_text
                    cmd = cmd_cmd
                    def __call__(self,data):
                        self.plugin.serial.write(self.cmd+str(data)+chr(13))
                ArgHandler.__name__ = cmd_name
                group.AddAction(ArgHandler)
            else:
                # Argumentless command
                class Handler(eg.ActionClass):
                    name = cmd_name
                    description = cmd_text
                    __call__ = createWriter(cmd_cmd)
                Handler.__name__ = cmd_name
                group.AddAction(Handler)


    # Serial port reader
    def reader(self):
        line=""
        while self.readerkiller is False:
            ch=self.serial.read()
            if ch=='\n':
                continue;
            if ch=='\r':
                if line != "":
                    self.TriggerEvent(line)
                    line=""
            else:
                line+=ch


    def __start__(self, port):
        try:
            self.serial = eg.SerialPort(port)
        except:
            raise eg.Exception("Can't open serial port.")
        self.serial.baudrate = 9600
        self.serial.timeout = 30.0
        self.serial.setDTR(1)
        self.serial.setRTS(1)
        self.readerkiller = False
        thread.start_new_thread(self.reader,());


    def __stop__(self):
        self.readerkiller = True
        if self.serial is not None:
            self.serial.close()
            self.serial = None


    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue())

