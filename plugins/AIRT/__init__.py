
import eg

eg.RegisterPlugin(
    name = "Advanced IR-Transceiver",
    author = "Bitmonster",
    version = "1.0.1093",
    kind = "remote",
    guid = "{9BE52B40-66A0-46D4-B88B-A8C1B6B42CAA}",
    description = 'Hardware plugin for the "Advanced IR-Transceiver".',
    canMultiLoad = True,
)

import wx
import threading

COMSPEED = 115200

ATI_REMOTE_TABLE = {
    0x00: "A",
    0x01: "B",
    0x02: "Power",
    0x03: "TV",
    0x04: "DVD",
    0x05: "WEB",
    0x06: "Book",
    0x07: "Hand",
    0x08: "VolUp",
    0x09: "VolDown",
    0x0A: "Mute",
    0x0B: "ChannelUp",
    0x0C: "ChannelDown",
    0x0D: "Num1",
    0x0E: "Num2",
    0x0F: "Num3",
    0x10: "Num4",
    0x11: "Num5",
    0x12: "Num6",
    0x13: "Num7",
    0x14: "Num8",
    0x15: "Num9",
    0x16: "Menu",
    0x17: "Num0",
    0x18: "Check",
    0x19: "C",
    0x1A: "Up",
    0x1B: "D",
    0x1C: "Watch",
    0x1D: "Left",
    0x1E: "Ok",
    0x1F: "Right",
    0x20: "Resize",
    0x21: "E",
    0x22: "Down",
    0x23: "F",
    0x24: "Rewind",
    0x25: "Play",
    0x26: "Forward",
    0x27: "Record",
    0x28: "Stop",
    0x29: "Pause",
    0x70: "Mouse270",
    0x71: "Mouse090",
    0x72: "Mouse000",
    0x73: "Mouse180",
    0x74: "Mouse315",
    0x75: "Mouse045",
    0x76: "Mouse135",
    0x77: "Mouse225",
    0x78: "LButtonDown",
    0x79: "LButtonDown2",
    0x7A: "LButtonDoubleClick",
    0x7C: "RButtonDown",
    0x7D: "RButtonDown2",
    0x7E: "RButtonDoubleClick",
    }

MEDION_REMOTE_TABLE = {
    0x00: "Mute",
    0x02: "Power",
    0x04: "DVD",
    0x05: "Photo",
    0x06: "Music",
    0x07: "Hand",
    0x08: "VolDown",
    0x09: "VolUp",
    0x0A: "Mute",
    0x0B: "ChannelUp",
    0x0C: "ChannelDown",
    0x0D: "Num1",
    0x0E: "Num2",
    0x0F: "Num3",
    0x10: "Num4",
    0x11: "Num5",
    0x12: "Num6",
    0x13: "Num7",
    0x14: "Num8",
    0x15: "Num9",
    0x16: "TXT",
    0x17: "Num0",
    0x18: "Snapshot",
    0x19: "DVDMenu",
    0x1A: "Up",
    0x1B: "Setup",
    0x1C: "ChSearch",
    0x1D: "Left",
    0x1E: "Ok",
    0x1F: "Right",
    0x20: "Delete",
    0x21: "PreviousTrack",
    0x22: "Down",
    0x23: "NextTrack",
    0x24: "Rewind",
    0x25: "Play",
    0x26: "Forward",
    0x27: "Record",
    0x28: "Stop",
    0x29: "Pause",
    0x2C: "TV",
    0x2D: "VCR",
    0x2E: "Radio",
    0x2F: "TVPreview",
    0x30: "ChannelList",
    0x31: "VideoDesktop",
    0x32: "Red",
    0x33: "Green",
    0x34: "Yellow",
    0x35: "Blue",
    0x36: "Rename",
    0x37: "AcquireImage",
    0x38: "EditImage",
    0x39: "Fullscreen",
    0x3A: "DVDAudio",
    }


def bin2hexstring(data):
    return " ".join(["%02X" % ord(x) for x in data])


def hexstring2bin(str):
    val = 0
    count = 0
    str2=''
    str = str.upper()
    for ch in str:
        if ch >= '0' and ch <= '9':
            val = val * 16 + (ord(ch) - ord('0'))
            count = count + 1
        elif ch >= 'A' and ch <= 'F':
            val = val * 16 + (ord(ch) - ord('A')) + 10
            count = count + 1
        if count == 2:
            str2 = str2 + chr(val)
            val = 0
            count = 0
    return str2



class AIRT(eg.PluginClass):

    def __init__(self):
        self.devicename = 'AIRT'
        self.thread = None
        self.AddEvents()
        self.AddAction(SendIR)


    @eg.LogIt
    def __start__(self, port=0, remotes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
        self.remotes = remotes
        self.port = port
        self.lastActionEvent = None
        self.serialThread = eg.SerialThread()
        self.serialThread.Open(port, COMSPEED)
        self.serialThread.SetReadEventCallback(self.HandleReceive)
        self.serialThread.Start()
        self.serialThread.Write("\x00\x00\x00")


    def __stop__(self):
        self.serialThread.Close()


    def HandleReceive(self, serial):
        byte = ord(serial.Read(1))
        if byte == 6:
            if self.lastActionEvent:
                self.lastActionEvent.set()
                self.lastActionEvent = None
            else:
                self.TriggerEvent('Received', ['<ACK>'])
        elif byte == 21:
            self.TriggerEvent('Received', ['<NAK>'])
        elif byte == 255:
            # receive X10 code
            data = serial.Read(6, 0.2)
            if len(data) < 6:
                return
            x10Id = ord(data[4])
            remoteType = self.remotes[x10Id]
            if remoteType == 2:
                table = ATI_REMOTE_TABLE
            elif remoteType == 1:
                table = MEDION_REMOTE_TABLE
            elif remoteType == 3:
                eventString = bin2hexstring(data[4])
                table = None
            else:
                return
            eventString = str(x10Id + 1) + "."
            if (
                (ord(data[5]) == 0x79 and ord(data[1]) == 1)
                or (ord(data[5]) == 0x7D and ord(data[1]) == 1)
                or (ord(data[1]) == 0)
            ):
                self.EndLastEvent()
                return
            else:
                if table is not None and ord(data[5]) in table:
                    eventString += table[ord(data[5])]
                else:
                    eventString += bin2hexstring(data[5])
                self.TriggerEnduringEvent(eventString)
        elif byte > 127:
            # receive other IR code
            data = serial.Read(6, 0.2)
            eventString = bin2hexstring(chr(byte) + data)
            self.TriggerEnduringEvent(eventString)
        else:
            # received something unknown
            data = serial.Read()
            self.TriggerEvent('Received', [bin2hexstring(byte + data)])


    def Configure(self, port=0, remotes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
        panel = eg.ConfigPanel()
        portCtrl = panel.SerialPortChoice(port)
        remoteCtrl = eg.RadioButtonGrid(
            panel,
            rows=["None", "Medion", "ATI", "X10"],
            columns=[str(i) for i in range(1, 17)]
        )
        remoteCtrl.SetValue(remotes)
        panel.sizer.Add(wx.StaticText(panel, -1, 'Port:'))
        panel.sizer.Add(portCtrl)
        panel.sizer.Add((10, 10))
        panel.sizer.Add(wx.StaticText(panel, -1, 'RF Remotes:'))
        panel.sizer.Add(remoteCtrl)

        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue(), remoteCtrl.GetValue())



class SendIR(eg.ActionClass):
    name = "Send IR"

    def __call__(self, data, repeats=1, block=True):
        if len(data) > 7:
            repeats = ord(data[7])
        event = threading.Event()
        event.data = data[:7] + chr(repeats)
        sp = self.plugin.serialThread
        self.plugin.lastActionEvent = event
        sp.SuspendReadEvents()
        sp.Write(event.data)
        sp.ResumeReadEvents()
        if repeats == 0:
            eg.event.AddUpFunc(sp.Write, '\xAB')
        if block and repeats != 0:
            event.wait(2.0)
            #print "block done"


    def GetLabel(self, data, repeats=1, block=True):
        return bin2hexstring(data)


    def Configure(
        self,
        data='\x00\x00\x00\x00\x00\x00\x00\x00',
        repeats=1,
        block=False
    ):
        panel = eg.ConfigPanel()
        dataCtrl = panel.TextCtrl(bin2hexstring(data))
        panel.sizer.Add(dataCtrl, 0, wx.EXPAND)

        while panel.Affirmed():
            datastr = dataCtrl.GetValue()
            data = hexstring2bin(datastr)
            panel.SetResult(data, 1, True)

