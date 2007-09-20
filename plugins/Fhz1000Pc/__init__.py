import eg

eg.RegisterPlugin(
    name="FHZ 1000 PC",
    kind="external",
    author="Bitmonster",
    version = "1.0." + "$LastChangedRevision: 229 $".split()[1],    
)

import time
import wx
import wx.lib.masked as masked


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
        global d2xx
        import d2xx
        self.handle = d2xx.openEx('ELV FHZ 1000 PC', d2xx.OPEN_BY_DESCRIPTION)
        self.handle.setBaudRate(9600)
        self.handle.setDataCharacteristics(8, 0, 0)
        self.handle.setFlowControl(0, 17, 19)
        # set RX/TX timeouts
        self.handle.setTimeouts(1000,1000)
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
        
        self.SetFhzTime()
        
        
    def __stop__(self):
        self.WriteFhz(0x04, 0xc9, 0x01, 0x97)
        self.handle.close()
        self.handle = None
        
        
    def WriteFhz(self, telegramType, *args):
        maxTime = time.clock() + 1.0
        while self.handle.getModemStatus() != 48:
            if time.clock() > maxTime:
                self.PrintError("FHZ timeout error!")
                return
            time.sleep(0.01)
        crc = 0xff & sum(args)
        dataStr = "".join([chr(x) for x in args])
        data = "\x81" + chr(len(dataStr) + 2) + chr(telegramType) + chr(crc) + dataStr
        if eg.debugLevel:
            print "<- " + " ".join(["%02X" % ord(c) for c in data])
        self.handle.write(data)
        
        
    def ReadFhz(self):
        time.sleep(0.2)
        h = self.handle
        startByte = ord(h.read(1))
        if startByte != 0x81:
            raise FhzException("Wrong start byte.")
        length = ord(h.read(1))
        data = [ord(c) for c in h.read(length)]
        telegramType = data[0]
        crc = data[1]
        newCrc = 0xff & sum(data[2:])
        dataStr = " ".join(["%02X" % x for x in data])
        if eg.debugLevel:
            print ("-> %02X %02X " % (startByte, length)) + dataStr
        return telegramType, data[2:]
    
    
    def SetFhzTime(self):
        t = time.localtime()
        year = t.tm_year % 100 
        self.WriteFhz(
            0xc9, 0x02, 0x01, 0x61, 
            year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min
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
        
        if panel.Affirmed():
            address = self.GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            return (address, )
            


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
        
        if panel.Affirmed():
            address = self.GetAddressFromString(maskedCtrl.GetPlainValue())
            ActionBase.defaultAddress = address
            return (
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
    
    
    
    
    
    
        
        
        