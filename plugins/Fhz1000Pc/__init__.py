import eg

eg.RegisterPlugin(
    name="FHZ 1000 PC",
    kind="external",
    author="Bitmonster",
    version = "1.0." + "$LastChangedRevision: 229 $".split()[1],    
)

import time
import os
import ctypes
from ctypes import byref, c_char_p, Structure, POINTER
from ctypes.wintypes import DWORD
import win32file
import win32con
import wx
import wx.lib.masked as masked

FT_OPEN_BY_DESCRIPTION = 2




class Fhz1000Pc(eg.PluginClass):
    
    def __init__(self):
        self.AddAction(Off)
        self.AddAction(On)
        self.AddAction(Dim)
        self.AddAction(ToggleDim)
        self.AddAction(DimDown)
        self.AddAction(DimUp)
        self.AddAction(Toggle)
        self.AddAction(StartProgramTimer)
        self.AddAction(ResetToFactoryDefaults)
        
        
    def __start__(self):
        self.timeTask = None
        self.readBuffer = ""
        
        global d2xx
        try:
            d2xx = ctypes.windll.LoadLibrary("ftd2xx.dll")
        except:
            raise self.Exception(
                "FHZ PC DLL not found (ftd2xx.dll).\n"
                "Make sure you have installed the driver for the device!"
            )
        self.ftHandle = d2xx.FT_W32_CreateFile(
            'ELV FHZ 1000 PC',
            win32con.GENERIC_READ|win32con.GENERIC_WRITE,
            0, # exclusive access
            0, # no security
            win32con.OPEN_EXISTING,
            win32con.FILE_ATTRIBUTE_NORMAL|win32con.FILE_FLAG_OVERLAPPED|FT_OPEN_BY_DESCRIPTION,
            0
        )
        self.receiveThread = eg.SerialThread(self.ftHandle)
        self.receiveThread.WriteFile = d2xx.FT_W32_WriteFile
        self.receiveThread.ReadFile = d2xx.FT_W32_ReadFile
        self.receiveThread.ClearCommError = d2xx.FT_W32_ClearCommError
        self.receiveThread.CloseHandle = d2xx.FT_W32_CloseHandle
        
        d2xx.FT_SetLatencyTimer(self.ftHandle, 2)
        d2xx.FT_SetBaudRate(self.ftHandle, 9600)
        d2xx.FT_SetDataCharacteristics(self.ftHandle, 8, 0, 0)
        d2xx.FT_SetFlowControl(self.ftHandle, 0, 17, 19)
        d2xx.FT_SetTimeouts(self.ftHandle, 1000, 1000)
        
        self.receiveThread.SuspendReadEvents()
        self.receiveThread.SetReadEventCallback(self.HandleReceive)
        self.receiveThread.Start()
        # Say hello
        self.WriteFhz(0xC9, 0x02, 0x01, 0x1f, 0x42)
        self.ReadFhz()

        # Request Status/Serial
        self.WriteFhz(0x04, 0xc9, 0x01, 0x84, 0x57, 0x02, 0x08)
        self.ReadFhz()

        # HMS Init (if required)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x86)
        
        # FS20 Init (if required)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x96)
        
        # calculate the time of the current minute
        t = list(time.localtime())
        t[5] = 0
        self.nextTaskTime = time.mktime(t)
        self.WriteFhz(*self.GetTimeData())
        self.nextTaskTime += 60.0
        self.timeTask = eg.scheduler.AddTaskAbsolute(
            self.nextTaskTime, 
            self.TimeScheduleTask
        )
        self.receiveThread.ResumeReadEvents()
        
        
        
    def __stop__(self):
        if self.timeTask is not None:
            eg.scheduler.CancelTask(self.timeTask)
        self.WriteFhz(0x04, 0xc9, 0x01, 0x97)
        if self.receiveThread:
            self.receiveThread.Close()
        
        
    def HandleReceive(self, serial):
        data = serial.Read(512)
        print "HR: " + " ".join(["%02X" % ord(c) for c in data])
        
        
    def WriteFhzNoWait(self, telegramType, *args):
        crc = 0xff & sum(args)
        dataStr = "".join([chr(x) for x in args])
        data = "\x81" + chr(len(dataStr) + 2) + chr(telegramType) + chr(crc) + dataStr
        if eg.debugLevel:
            print "W: " + " ".join(["%02X" % ord(c) for c in data])
        self.receiveThread.Write(data)
        time.sleep(0.01)

        
    def WriteFhz(self, telegramType, *args):
        maxTime = time.clock() + 1.0
        dwStatus = DWORD()
        while True:
            d2xx.FT_GetModemStatus(self.ftHandle, byref(dwStatus))
            if dwStatus.value == 48:
                break
            if time.clock() > maxTime:
                self.PrintError("FHZ timeout error!")
                return
            time.sleep(0.01)
            #print "write sleep"
        self.WriteFhzNoWait(telegramType, *args)
        
        
    def ReadFhz(self):
        startByte = ord(self.Read(1))
        if startByte != 0x81:
            raise FhzException("Wrong start byte.")
        length = ord(self.Read(1))
        data = [ord(c) for c in self.Read(length)]
        telegramType = data[0]
        crc = data[1]
        newCrc = 0xff & sum(data[2:])
        if eg.debugLevel:
            dataStr = " ".join(["%02X" % x for x in data])
            print ("-> %02X %02X " % (startByte, length)) + dataStr
        return telegramType, data[2:]
    
    
    def Read(self, numBytes):
        data = self.receiveThread.Read(numBytes, 1.0)
        if len(data) < numBytes:
            self.PrintError("FHZ read timeout error!")
        return data
        
    
        
    def GetTimeData(self):
        t_struct = time.localtime(self.nextTaskTime)
        year = t_struct.tm_year % 100 
        return(
            0xc9, 0x02, 0x01, 0x61, 
            year, t_struct.tm_mon, t_struct.tm_mday, 
            t_struct.tm_hour, t_struct.tm_min
        )
        
        
    def TimeScheduleTask(self, repeats=1):
        """
        Send the current time 50 times and schedule the next execution at the
        next minute.
        """
        data = self.GetTimeData()
        for i in range(repeats):
            eg.actionThread.CallWait(self.WriteFhzNoWait, *data)
        self.nextTaskTime += 60.0
        self.timeTask = eg.scheduler.AddTaskAbsolute(
            self.nextTaskTime, 
            self.TimeScheduleTask
        )

        
    
class ActionBase(eg.ActionClass):
    defaultAddress = 0x094001
    
    def __call__(self, address):
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        self.plugin.WriteFhz(0x04, 0x02, 0x01, 0x01, a2, a1, a0, self.funccode)


    def GetLabel(self, address):
        return self.name
    
    
    def GetStringFromAddress(self, address):
        valueStr = ""
        for i in range(11, -1, -1):
            x = (address >> i*2) & 0x03
            valueStr += str(x + 1)
        return valueStr
        
        
    def GetAddressFromString(self, addressString):
        address = 0
        for i in range(12):
            address <<= 2
            address += (int(addressString[i], 4) - 1)
        return address
        
    
    def Configure(self, address=None):       
        if address is None:
            address = self.defaultAddress
            
        panel = eg.ConfigPanel(self)
            
        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(self.GetStringFromAddress(address))

        panel.AddLine("Address:", maskedCtrl)
        
        while panel.Affirmed():
            address = self.GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(address)
            


class Dim(ActionBase):
    name = "Set dim-level"
    
    def __call__(self, address, level):
        x, a0 = divmod(address, 256)
        a2, a1 = divmod(x, 256)
        self.plugin.WriteFhz(0x04, 0x02, 0x01, 0x01, a2, a1, a0, level)
    
    
    def GetLabel(self, address, level):
        return "Set dim-level to %.02f %%" % (level * 100.00 / 16)
    
    
    def Configure(self, address=None, level=1):       
        if address is None:
            address = self.defaultAddress
        panel = eg.ConfigPanel(self)
            
        maskedCtrl = masked.TextCtrl(
            parent=panel,
            mask="#### #### - ####",
            defaultValue="1111 1111 - 1111",
            excludeChars="056789",
            formatcodes="F",
            validRequired=False,
        )
        maskedCtrl.SetValue(self.GetStringFromAddress(address))
        
        def LevelCallback(value):
            return "%.02f %%" % (value * 100.00 / 16)
        
        levelCtrl = eg.Slider(
            panel, 
            value=level, 
            min=1, 
            max=16, 
            minLabel="6.25 %",
            maxLabel="100.00 %",
            style = wx.SL_AUTOTICKS|wx.SL_TOP,
            size=(300,-1),
            levelCallback=LevelCallback
        )
        levelCtrl.SetMinSize((300, -1))
        
        panel.AddLine("Address:", maskedCtrl)
        panel.AddLine("Level:", levelCtrl)
        
        while panel.Affirmed():
            address = self.GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            panel.SetResult(
                address, 
                levelCtrl.GetValue(),
            )
            
            
            
class Off(ActionBase):
    funccode = 0x00
    
    
    
class On(ActionBase):
    funccode = 0x11
        
        
        
class ToggleDim(ActionBase):
    name = "Toggle dimming"
    funccode = 0x12
    
    

class DimUp(ActionBase):
    name = "Dim up"
    funccode = 0x13
    


class DimDown(ActionBase):
    name = "Dim down"
    funccode = 0x14
    
    

class Toggle(ActionBase):
    funccode = 0x15
    
    

class StartProgramTimer(ActionBase):
    name = "Start/stop programming timer"
    funccode = 0x16
    
    

class ResetToFactoryDefaults(ActionBase):
    name = "Reset to factory defaults"
    funccode = 0x1b
    
    
    
    
    
    
        
        
        