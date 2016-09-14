#
# JVC HD-1 Serial V0.1
# ====================
# Written by Oliver Wagner, <owagner@hometheatersoftware.com>
# Public Domain
#
# This plugin is for controlling an JVC HD-1 projector via RS-232
#
# Except for the power and menu commands, the HD-1 only offers remote control
# emulation (at least, only those are documented). There are two commands which
# yield a reply:
# - Get Power returns the current power status
# - Get Input returns the current input status
# The replies from each command are returned as events.
#

from __future__ import with_statement

eg.RegisterPlugin(
    name = "JVC HD-1 Projector",
    description = "This plugin is for controlling an JVC HD-1 projector via RS-232",
    kind = "external",
    author = "Oliver Wagner",
    version = "1.0.0",
    guid = "{A35CC4DC-BC72-4EF8-BC8E-27F88A2686D4}",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=650",
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


ACK = chr(0x06)
OP = chr(0x21)
REF = chr(0x3f)
UNITID1 = chr(0x89)
UNITID2 = chr(0x01)
END = chr(0x0a)
RESP = chr(0x40)

ACTIONS = (
    ("GetPower", "Get Power Status", REF, (0x50, 0x57)),
    ("GetInput", "Get Input Status", REF, (0x49, 0x50)),

    ("PowerOn", "Turn On Power", OP, (0x50, 0x57, 0x31)),
    ("PowerOff", "Turn Off Power", OP, (0x50, 0x57, 0x30)),

    ("InputSVideo", "Input S-Video", OP, (0x49, 0x50, 0x30)),
    ("InputVideo", "Input Video", OP, (0x49, 0x50, 0x31)),
    ("InputComp", "Input Composite", OP, (0x49, 0x50, 0x32)),
    ("InputHDMI1", "Input HDMI1", OP, (0x49, 0x50, 0x36)),
    ("InputHDMI2", "Input HDMI1", OP, (0x49, 0x50, 0x37)),

    ("RemoteUp", "Remote UP", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x31)),
    ("RemoteDown", "Remote DOWN", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x32)),
    ("RemoteLeft", "Remote LEFT", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x34)),
    ("RemoteRight", "Remote RIGHT", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x36)),
    ("RemoteExit", "Remote EXIT", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x33)),
    ("RemoteOn", "Remote OPERATE ON", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x35)),
    ("RemoteOff", "Remote OPERATE OFF", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x36)),
    ("RemoteHide", "Remote HIDE", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x44)),
    ("RemoteMenu", "Remote MENU", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x45)),
    ("RemoteEnter", "Remote ENTER", OP, (0x52, 0x43, 0x37, 0x33, 0x30, 0x46)),


    ("CheckConnection", "Check connection", OP, (0x00, 0x00)),
)

class ActionBase(eg.ActionClass):

    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, self.cmd, self.data)


    def SendCommand(self, serial, cmd, data):
        serial.Write(cmd)
        serial.Write(UNITID1)
        serial.Write(UNITID2)
        serial.Write("".join([chr(x) for x in data]))
        serial.Write(END)
        res = serial.Read(1, 1.0)
        if res != ACK:
            raise self.Exceptions.DeviceNotFound("Got no ACK!")
        while res != END:
            res = serial.Read(1, 0.5)


    def GetResponse(self, serial, cmde):
        answer = serial.Read(7, 1.0)
        if len(answer) < 7:
            raise self.Exceptions.DeviceNotFound("Not enough bytes received!")




class JVCHD1Serial(eg.PluginClass):

    def __init__(self):
        self.info.eventPrefix = "JVC-HD1"
        for evalName, tmpDescription, tmpCmd, tmpData in ACTIONS:
            class TmpAction(ActionBase):
                name = evalName
                description = tmpDescription
                cmd = tmpCmd
                data = tmpData
            TmpAction.__name__ = evalName
            self.AddAction(TmpAction)


    @eg.LogIt
    def __start__(self, port=0):
        self.port = port
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, 19200)
        self.serialThread.SetRts()
        self.serialThread.Start()


    def __stop__(self):
        self.serialThread.Close()


    def OnReceive(self, serial):
        data = serial.Read(1)
        if data != RESP:
            return
        serial.Read(2, 1.0) # Skip unit ID
        c1 = serial.Read(1, 1.0)
        c2 = serial.Read(1, 1.0)
        state = serial.Read(1, 1.0)
        serial.Read(1, 1.0) # Skip 0x0a
        if c1 == chr(0x50) and c2 == chr(0x57):
            if state == chr(0x30):
                sid =" Standby"
            elif state == chr(0x31):
                sid = "PowerOn"
            elif state == chr(0x32):
                sid = "CoolingDown"
            elif state == chr(0x34):
                sid = "Warning"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("PowerState." + sid)
        elif c1 == chr(0x49) and c2 == chr(0x50):
            if state == chr(0x30):
                sid = "SVideo"
            elif state == chr(0x31):
                sid = "Video"
            elif state == chr(0x32):
                sid = "Composite"
            elif state == chr(0x36):
                sid = "HDMI1"
            elif state == chr(0x37):
                sid = "HDMI2"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("Input." + sid)
        else:
            raise self.Exceptions.DeviceNotReady("Unexpected response %02X%02X" %(ord(c1), ord(c2)))



    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Serial port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(),
            )




