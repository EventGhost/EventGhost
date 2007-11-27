import eg

eg.RegisterPlugin(
    name = "Barco CRT Projector",
    kind = "external",
    author = "Bitmonster",
    version = "1.0.0",
    canMultiLoad = True,
    createMacrosOnAdd = True,
    icon = (
        "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAIAAACQkWg2AAAABnRSTlMA/wD/AP83WBt9"
        "AAAACXBIWXMAAAsTAAALEwEAmpwYAAABTElEQVR4nJWRO0sDQRSFz53Z7GNWo0VMYgiI"
        "D9BERJSAP8PCyl9g5T8QC/HniI3Y2qnYZyEoeYAYo8YgaFbzmBmLXdYUksepprjfnHPP"
        "Ja01JpEBwD85lV5p5ChfXxPHRwxAv+jp9idfXZS1KlteUI0nnlvSsgtS5Fo042LK7l3f"
        "yqIXOhCIFzZJOM7hgayWrf09isf56oosVaClUdgCZ2w2Lh+fQ0BDq9YHs0xZrvZu7ozt"
        "DVV/o2mXzSVUsyUrNUB1zi5iO4UQANA9v4yySu9hyCYsiDROPzoCNMZqliJgIk0cyQBw"
        "lcvXFQEgoiGHz+TzuwFQTqXvv/yRDt/JVOgwmMh1hSsEAFeI1+a7ktI0Y1ojcjb+0gEA"
        "lFSZZAKMc86FbfWlchw7ZpqNxkvwrwEgm0kPNtv+6QQPIgLQ9n34vm1b2fk0gGFb/qtf"
        "bUt6K1gxHQUAAAAASUVORK5CYII="
    ),
)



ACTIONS = (
    ("Enter", "Enter", None, (0x07, )),
    ("Exit", "Exit", None, (0x08, )),
    ("Up", "Cursor Up", None, (0x21, )),
    ("Down", "Cursor Down", None, (0x22, )),
    ("Left", "Cursor Left", None, (0x24, )),
    ("Right", "Cursor Right", None, (0x23, )),
    ("AdjustToggle", "Adjust Toggle", None, (0x09, )),
    ("AdjustOn", "Adjust On", None, (0x51, 0x09, 0x00, 0x00, 0x01)),
    ("AdjustOff", "Adjust Off", None, (0x51, 0x09, 0x00, 0x00, 0x00)),
    ("TextToggle", "Text Toggle", None, (0x0d, )),
    ("TextOn", "Text On", None, (0x51, 0x06, 0x00, 0x00, 0x01)),
    ("TextOff", "Text Off", None, (0x51, 0x06, 0x00, 0x00, 0x00)),
    ("PauseToggle", "Pause Toggle", None, (0x0f, )),
    ("PauseOff", "Pause Off", None, (0x51, 0x01, 0x00, 0x00, 0x00)),
    ("PauseOn", "Pause On", None, (0x51, 0x01, 0x00, 0x00, 0x01)),
    ("PowerToggle", "Power Toggle", None, (0x0e, )),
    ("PowerOff", "Power Off (Standby)", None, (0x51, 0x0a, 0x00, 0x00, 0x00)),
    ("PowerOn", "Power On", None, (0x51, 0x0a, 0x00, 0x00, 0x01)),
    ("Numpad0", "Numpad 0", None, (0x10, )),
    ("Numpad1", "Numpad 1", None, (0x11, )),
    ("Numpad2", "Numpad 2", None, (0x12, )),
    ("Numpad3", "Numpad 3", None, (0x13, )),
    ("Numpad4", "Numpad 4", None, (0x14, )),
    ("Numpad5", "Numpad 5", None, (0x15, )),
    ("Numpad6", "Numpad 6", None, (0x16, )),
    ("Numpad7", "Numpad 7", None, (0x17, )),
    ("Numpad8", "Numpad 8", None, (0x18, )),
    ("Numpad9", "Numpad 9", None, (0x19, )),
    ("ContrastUp", "Contrast Up", None, (0x28, )),
    ("ContrastDown", "Contrast Down", None, (0x29, )),
    ("BrightnessUp", "Brightness Up", None, (0x2a, )),
    ("BrightnessDown", "Brightness Down", None, (0x2b, )),
    ("SaturationUp", "Colour Saturation Up", None, (0x2c, )),
    ("SaturationDown", "Colour Saturation Down", None, (0x2d, )),
    ("TintUp", "Colour Tint Up", None, (0x22, )),
    ("TintDown", "Colour Tint Down", None, (0x2f, )),
    ("SharpnessUp", "Sharpness Up", None, (0x36, )),
    ("SharpnessDown", "Sharpness Down", None, (0x37, )),
)

import wx

STX = 0x02
ACK = chr(0x06)
NAK = chr(0x15)
BAUDRATES = [110, 150, 300, 600, 1200, 2400, 4800, 9600]
ALL_BYTE_VALUES = frozenset(range(256))


class ActionBase(eg.ActionClass):
    
    def __call__(self):
        self.plugin.DoCommand(self, *self.value)



class SetText(eg.ActionWithStringParameter):
    
    def __call__(self, s):
        s = s + (chr(0) * (208 - len(s)))
        self.plugin.DoCommand(self, 0x70, 0x02, 0x02, 0x01, 0x0c, s)
    
    
    
class ReadTime(eg.ActionClass):
    
    def __call__(self):
        self.plugin.DoCommand(self, 0x60)
        
        
        
class RequestShape(eg.ActionClass):
    
    def __call__(self, shape=0, x=0, y=0, colours=0x07):
        self.plugin.DoCommand(self, 0x78, shape, x * 16 + y, colours)
        
        
    def Configure(self, shape=0, x=0, y=0, colours=0x07):
        choices = [
            ("Internal convergence pattern", 0x00),
            ("Horizontal line in center of zones", 0x01),
            ("Vertical line in center of zones", 0x02),
            ("Crosshatch in zone XY", 0x05),
            ("Convergence contour around zone XY", 0x06),
            ("Erase shape, switch colour", 0x07),
            ("Vertical bars, switch colour", 0x08),
            ("Horizontal bars, switch colour", 0x09),
        ]
        panel = eg.ConfigPanel(self)
        shapeCtrl = panel.SpinIntCtrl(shape)
        xCtrl = panel.SpinIntCtrl(x)
        yCtrl = panel.SpinIntCtrl(y)
        redCtrl = panel.CheckBox(colours & 0x01, "Red")
        greenCtrl = panel.CheckBox(colours & 0x02, "Green")
        blueCtrl = panel.CheckBox(colours & 0x04, "Blue")
        panel.AddLine("Shape:", shapeCtrl)
        panel.AddLine("X coordinate:", xCtrl)
        panel.AddLine("Y coordinate:", yCtrl)
        panel.AddLine("Colours:", redCtrl)
        panel.AddLine(None, greenCtrl)
        panel.AddLine(None, blueCtrl)
        while panel.Affirmed():
            colours = int(redCtrl.GetValue()) * 0x01
            colours |= int(redCtrl.GetValue()) * 0x02
            colours |= int(redCtrl.GetValue()) * 0x04
            panel.SetResult(
                shapeCtrl.GetValue(),
                xCtrl.GetValue(),
                yCtrl.GetValue(),
                colours,
            )
        


class LockIr(eg.ActionClass):
    name = "Lock IR"
    description = (
        "Programs the projector to filter out certain infra red commands."
    )
    
    def __call__(self, flags=0x7f):
        self.plugin.DoCommand(self, 0x50, flags)
        
        
    def Configure(self, flags=0x7f):
        panel = eg.ConfigPanel(self)
        choices = [
            "Stand by", 
            "Pause", 
            "Text", 
            "Adjust keys (Adj, Enter, Exit, cursors)",
            "Numeric keys",
            "Picture control keys",
            "Sound control keys",
        ]
        panel.AddLine("Allowed IR-commands:")
        ctrls = []
        for i, choice in enumerate(choices):
            ctrl = panel.CheckBox(flags & (1 << i), choice)
            ctrls.append(ctrl)
            panel.AddLine(None, ctrl)
        while panel.Affirmed():
            flags = 0
            for i, ctrl in enumerate(ctrls):
                flags |= (1 << i) * int(ctrl.GetValue())
            panel.SetResult(flags)
        
        
        
class Barco(eg.PluginClass):
    
    def __init__(self):
        for evalName, tmpName, tmpDescription, tmpValue in ACTIONS:
            class TmpAction(ActionBase):
                name = tmpName
                description = tmpDescription
                value = tmpValue
            TmpAction.__name__ = evalName
            self.AddAction(TmpAction)
        self.AddAction(SetText)
        self.AddAction(ReadTime)
        self.AddAction(RequestShape)
        self.AddAction(LockIr)
    
    
    @eg.LogIt
    def __start__(self, port=0, address=0, baudrate=9600):
        self.port = port
        self.address = 0
        self.serialThread = eg.SerialThread()
        self.serialThread.SetReadEventCallback(self.OnReceive)
        self.serialThread.Open(port, baudrate)
        self.serialThread.Start()
        
        
    def __stop__(self):
        self.serialThread.Close()
        
        
    def OnReceive(self, serial):
        data = serial.Read(512)
        print "Barco: " + " ".join(["%02X" % ord(c) for c in data])
        
    
    def DoCommand(self, action, cmd, dat1=0, dat2=0, dat3=0, dat4=0, block=None):
        data = [self.address, cmd, dat1, dat2, dat3, dat4]
        checksum = sum(data) % 256
        data.append(checksum)
        
        if block is not None:
            data2 = [ord(x) for x in block]
            checksum2 = sum(data2) % 256
            data += data2
            data.append(checksum2)
            
        offset = 1
        while offset in data:
            offset += 1
        offset = (STX - offset) % 256
    
        data = [STX, offset] + [(x + offset) % 256 for x in data]
        s = "".join([chr(x) for x in data])
        self.serialThread.SuspendReadEvents()
        try:
            self.serialThread.Write(s)
            res = self.serialThread.Read(1, 0.5)
            if res != ACK:
                raise action.Exceptions.DeviceNotFound("Got no ACK!")
        finally:
            self.serialThread.ResumeReadEvents()

    
    def Configure(self, port=0, address=0, baudrate=9600):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        choices = [str(baudrate) for baudrate in BAUDRATES]
        baudrateCtrl = panel.Choice(BAUDRATES.index(baudrate), choices=choices)
        addrCtrl = panel.SpinIntCtrl(address, min=0, max=255)
        panel.AddLine("Serial port:", portCtrl)
        panel.AddLine("Baudrate:", baudrateCtrl)
        panel.AddLine("Projector address:", addrCtrl)
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(), 
                addrCtrl.GetValue(),
                BAUDRATES[baudrateCtrl.GetValue()],
            )
            
    
    
        
