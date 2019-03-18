#
# Lumagen Vision
# ================


r"""<rst>
Plugin to control the Lumagen Vision DVI/HDP via RS-232.

|

.. image:: picture.gif
   :align: center
"""

import eg

eg.RegisterPlugin(
    name="Lumagen Vision DVI/HDP",
    description=__doc__,
    author="FoLLgoTT",
    version="1.0.0",
    kind="external",
    guid="{f36bdbd0-5e7c-4793-8294-6288011a7d6d}",
    canMultiLoad=True,
    createMacrosOnAdd=True,
)

cmdList = (
    ('Power', None, None, None),
    ('PowerOn', 'Power On', '%', None),
    ('PowerOff', 'Power Standby', '$', None),
    ('Control', None, None, None),
    ('Menu', 'Activates Menu', 'M', None),
    ('Exit', 'Exit or Cancel', 'X', None),
    ('ForceMenuOff', 'Force Menu Off', '!', None),
    ('OK', 'Accept Command', 'k', None),
    ('Left', 'Cursor Left', '<', None),
    ('Right', 'Cursor Right', '>', None),
    ('Down', 'Cursor Down', 'v', None),
    ('Up', 'Cursor Up', '^', None),
    ('Digit0', 'Digit 0', '0', None),
    ('Digit1', 'Digit 1', '1', None),
    ('Digit2', 'Digit 2', '2', None),
    ('Digit3', 'Digit 3', '3', None),
    ('Digit4', 'Digit 4', '4', None),
    ('Digit5', 'Digit 5', '5', None),
    ('Digit6', 'Digit 6', '6', None),
    ('Digit7', 'Digit 7', '7', None),
    ('Digit8', 'Digit 8', '8', None),
    ('Digit9', 'Digit 9', '9', None),
    ('OSDOn', 'On Screen Display On', 'g', None),
    ('OSDOff', 'On Screen Display Off', 's', None),
    ('Freeze', 'Freezes Frame', 'z', None),
    ('Input', None, None, None),
    ('Input', 'Selects Input (n = 1-8)', 'i', '1-8'),
    ('PrevInput', 'Selects previous Input', 'P', None),
    ('Input43', 'Input is 4:3', 'n', None),
    ('Input43NZ', 'Input is 4:3, no Zoom', '[', None),
    ('Input43LB', 'Input is 4:3, Letter Box', 'l', None),
    ('Input43LBNZ', 'Input is 4:3, Letter Box, no Zoom', ']', None),
    ('Input169', 'Input is 16:9', 'w', None),
    ('Input169NZ', 'Input is 16:9, no Zoom', '*', None),
    ('Input185', 'Input is 1.85:1', 'j', None),
    ('Input185NZ', 'Input is 1.85:1, no Zoom', '/', None),
    ('Input235', 'Input is 2.35:1', 'W', None),
    ('Memory', None, None, None),
    ('MemA', 'Selects Memory A', 'a', None),
    ('MemB', 'Selects Memory B', 'b', None),
    ('MemC', 'Selects Memory C', 'c', None),
    ('MemD', 'Selects Memory D', 'd', None),
    ('Output', None, None, None),
    ('OutputYPbPr', 'Sets Output to YPbPr', 'Y', None),
    ('OutputRGBHV', 'Sets Output to RGBHV', 'R', None),
    ('OutputRGBS', 'Sets Output to RGBS', 'S', None),
    ('OutputRGsB', 'Sets Output to RGsB', 'T', None),
    ('OutputVRes480p', 'Sets Vertical Output Resolution to 480p', 'A', None),
    ('OutputVRes540p', 'Sets Vertical Output Resolution to 540p', 'B', None),
    ('OutputVRes600p', 'Sets Vertical Output Resolution to 600p', 'C', None),
    ('OutputVRes720p', 'Sets Vertical Output Resolution to 720p', 'D', None),
    ('OutputVRes768p', 'Sets Vertical Output Resolution to 768p', 'E', None),
    ('OutputVRes840p', 'Sets Vertical Output Resolution to 840p', 'F', None),
    ('OutputVRes1080p', 'Sets Vertical Output Resolution to 1080p', 'G', None),
    ('OutputVRes1080i', 'Sets Vertical Output Resolution to 1080i', 'I', None),
    ('OutputVRes', 'Sets Vertical Output Resolution (1080 = 1080p)', 'V', '480-1080'),
    ('OutputVRate', 'Sets Vertical Output Frequency (2400 = 24.00Hz)', '~', '2397-7500'),
    ('OutputHRate', 'Sets Horizontal Output Frequency (45000 = 45000Hz)', 'H', '10000-60000'),
    ('OutputAspect1', 'Sets Output Aspect Ratio (220 = 2.2:1)', '=', '110-250'),
    ('OutputAspect2', 'Sets Output Aspect Ratio (220 = 2.2:1)', 'ZY1', '110-250'),
    ('OutputZoom', 'Sets Output Zoom Factor (n = 0-7)', 'ZY0', '0-7'),
    ('Test Patterns', None, None, None),
    ('TestPattern01', 'Shows Test Pattern 01 with given IRE Level (01 = 10IRE)', 'ta', '00-10'),
    ('TestPattern02', 'Shows Test Pattern 02 with given IRE Level (01 = 10IRE)', 'tb', '00-10'),
    ('TestPattern03', 'Shows Test Pattern 03 with given IRE Level (01 = 10IRE)', 'tc', '00-10'),
    ('TestPattern04', 'Shows Test Pattern 04 with given IRE Level (01 = 10IRE)', 'td', '00-10'),
    ('TestPattern05', 'Shows Test Pattern 05 with given IRE Level (01 = 10IRE)', 'te', '00-10'),
    ('TestPattern06', 'Shows Test Pattern 06 with given IRE Level (01 = 10IRE)', 'tf', '00-10'),
    ('TestPattern07', 'Shows Test Pattern 07 with given IRE Level (01 = 10IRE)', 'tg', '00-10'),
    ('TestPattern08', 'Shows Test Pattern 08 with given IRE Level (01 = 10IRE)', 'th', '00-10'),
    ('TestPattern09', 'Shows Test Pattern 09 with given IRE Level (01 = 10IRE)', 'ti', '00-10'),
    ('TestPattern10', 'Shows Test Pattern 10 with given IRE Level (01 = 10IRE)', 'tj', '00-10'),
    ('TestPattern11', 'Shows Test Pattern 11 with given IRE Level (01 = 10IRE)', 'tk', '00-10'),
    ('TestPattern12', 'Shows Test Pattern 12 with given IRE Level (01 = 10IRE)', 'tl', '00-10'),
    ('TestPattern13', 'Shows Test Pattern 13 with given IRE Level (01 = 10IRE)', 'tm', '00-10'),
    ('TestPattern14', 'Shows Test Pattern 14 with given IRE Level (01 = 10IRE)', 'tn', '00-10'),
    ('TestPattern15', 'Shows Test Pattern 15 with given IRE Level (01 = 10IRE)', 'to', '00-10'),
    ('TestPattern16', 'Shows Test Pattern 16 with given IRE Level (01 = 10IRE)', 'tp', '00-10'),
    (None, None, None, None),
)


class CmdAction(eg.ActionClass):
    """Base class for all argumentless actions"""

    def __call__(self):
        self.plugin.serialThread.Write(self.cmd + '\r')


class ValueAction(eg.ActionWithStringParameter):
    """Base class for all actions with adjustable argument"""

    def __call__(self, data):
        self.plugin.serialThread.Write(self.cmd + str(data) + '\r')


class LumagenVision(eg.PluginClass):

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
        return
