import eg
import threading, Queue, time, string, binascii
import wx
from eg.WinAPI.SerialPort import SerialPort

ATI_Remote_Table = {
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

Medion_Remote_Table = {
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


def bin2hexstring(str):
    if len(str) > 0:
        str2 = binascii.hexlify(str[0])
        for i in xrange(1, len(str)):
            str2 = str2 + ' ' + binascii.hexlify(str[i])
        return string.upper(str2)
    else:
        return str

def hexstring2bin(str):
    val = 0
    count = 0
    str2=''
    str = string.upper(str)
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



COMSPEED = 115200


class AIRT(eg.PluginClass):
    
    name = "Advanced IR-Transceiver"
    author = "Bitmonster"
    version = "1.0." + "$LastChangedRevision$".split()[1]
    kind = "remote"
    description = 'Hardware plugin for the "Advanced IR-Transceiver".'
    
    def __init__(self):
        self.devicename = 'AIRT'
        self.thread = None
        self.AddAction(SendIR)
        
        
    def __start__(self, port=0, remotes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
        self.remotes = remotes
        self.receiveQueue = Queue.Queue(2048)
        self._want_abort = False
        self.port = port
        self.thread = threading.Thread(target=self.ThreadWorker)
        self.thread.start()


    def __stop__(self):
        self._want_abort = True


    def ThreadWorker(self):
        # This is the code executing in the new thread. 
        lasttime = time.clock()
        event_bytecount = 0
        event_bytes = ""
        self.sp = SerialPort(self.port, COMSPEED)
        self.sp.open()
        self.sp.write("\x00\x00\x00")
        buf = ""
        received_event = None
        while not self._want_abort:
            if not self.receiveQueue.empty():
                received_event = self.receiveQueue.get()
                #print bin2hexstring(received_event.data)
                self.sp.write(received_event.data)
            data = self.sp.read(-1)
            if data:
                buf = buf + data
                lasttime = time.clock()
            elif (time.clock() - lasttime > 0.01) and (buf != ""):
                while len(buf):
                    if ord(buf[0]) >= 128 and len(buf) >= 7:
                        eventString = ''
                        if ord(buf[0]) == 255:
                            x10Id = ord(buf[5])
                            remoteType = self.remotes[x10Id]
                            if remoteType == 2:
                                table = ATI_Remote_Table
                            elif remoteType == 1:
                                table = Medion_Remote_Table
                            elif remoteType == 3:
                                eventString = bin2hexstring(buf[5])
                                table = None
                            else:
                                buf = buf[7:]
                                continue
                            eventString = str(x10Id + 1) + "."
                            if (
                                (ord(buf[6]) == 0x79 and ord(buf[2]) == 1)
                                or (ord(buf[6]) == 0x7D and ord(buf[2]) == 1)
                                or (ord(buf[2]) == 0)
                            ):
                                self.EndLastEvent()
                                buf = buf[7:]
                                continue
                            else:    
                                if table is not None and ord(buf[6]) in table:
                                    eventString += table[ord(buf[6])]
                                else:
                                    eventString += bin2hexstring(buf[6])
                        else:
                            eventString = bin2hexstring(buf[0:7])
                        self.TriggerEnduringEvent(eventString)
                        buf = buf[7:]
                    elif ord(buf[0]) == 6:
                        if received_event <> None:
                            received_event.set()
                            received_event = None
                        else:
                            self.TriggerEvent('Received', ['<ACK>'])
                        buf = buf[1:]
                    elif ord(buf[0]) == 21:
                        self.TriggerEvent('Received', ['<NAK>'])
                        buf = buf[1:]
                    else:
                        self.TriggerEvent('Received', [bin2hexstring(buf)])
                        buf = ''
            else:
                time.sleep(0.02)
        self.sp.close()

    
    def SendRaw(self, data, block=False):
        event = threading.Event()
        event.data = data
        self.receiveQueue.put(event)
        if block:
            event.wait(2.0)


    def Configure(self, port=0, remotes=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]):
        dialog = eg.ConfigurationDialog(self)
        portCtrl = eg.SerialPortChoice(dialog, value=port)
        remoteCtrl = eg.RadioButtonGrid(
            dialog, 
            rows=["None", "Medion", "ATI", "X10"],
            columns=[str(i) for i in range(1, 17)]
        )
        remoteCtrl.SetValue(remotes)
        dialog.sizer.Add(wx.StaticText(dialog, -1, 'Port:'))
        dialog.sizer.Add(portCtrl)
        dialog.sizer.Add((10, 10))
        dialog.sizer.Add(wx.StaticText(dialog, -1, 'RF Remotes:'))
        dialog.sizer.Add(remoteCtrl)
        
        yield dialog
        yield (portCtrl.GetValue(), remoteCtrl.GetValue(), )
                    


class SendIR(eg.ActionClass):
    name = "Send IR"
    
    def __call__(self, data, repeats=1, block=True):
        if len(data) > 7:
            repeats = ord(data[7])
        event = threading.Event()
        event.data = data[:7] + chr(repeats)
        self.plugin.receiveQueue.put(event)
        if repeats == 0:
            eg.event.AddUpFunc(self.plugin.SendRaw, '\xAB')
        if block and repeats != 0:
            event.wait(2.0)
            #print "block done"
            
            
    def GetLabel(self, data, repeats=1, block=True):
        return bin2hexstring(data)
    
    
    def Configure(self, data='\x00\x00\x00\x00\x00\x00\x00\x00', repeats=1, block=False):
        dialog = eg.ConfigurationDialog(self)
        datastr = bin2hexstring(data)
        dataCtrl = wx.TextCtrl(dialog, -1, datastr)
        dialog.sizer.Add(dataCtrl, 0, wx.EXPAND)
        
        yield dialog
        datastr = dataCtrl.GetValue()
        data = hexstring2bin(datastr)
        yield (data, 1, True)
    
