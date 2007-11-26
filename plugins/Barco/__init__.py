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


FB = """\
PARK 0FH toggle
MONO 1DH toggle mono / stereo \
EXPAND 1EH toggle expand / normal | Only on local command
MUTE 1FH mute sound / of Retro projectors.
TOGG_A 27H Toggle for sound / picture
SAT_UP 2CH Color saturation up
SAT_DN 2DH Color saturation down
HUE_UP 2EH Color tint up
HUE_DN 2FH Color tint down
SHA_UP 36H Color sharpness up
SHA_DN 37H Color sharpness down
VOL_UP 38H Analog sound controls volume up
VOL_DN 39H " volume down
BAS_UP 3AH " bass up
BAS_DN 3BH " bass down
TRE_UP 3CH " treble up
TRE_DN 3DH " treble down
BAL_UP 3EH " balance up
BAL_DN 3FH " balance down
"""

ACTIONS = (
    ("Enter", "Enter", None, 0x07),
    ("Exit", "Exit", None, 0x08),
    ("Up", "Cursor Up", None, 0x21),
    ("Down", "Cursor Down", None, 0x22),
    ("Left", "Cursor Left", None, 0x24),
    ("Right", "Cursor Right", None, 0x23),
    ("Home", "Cursor Home", None, 0x25),
    ("Adjust", "Adjust", None, 0x09),
    ("ToggleText", "Toggle Text", None, 0x0d),
    ("ToggleStandby", "Toggle Standby", None, 0x0e),
    ("Numpad0", "Numpad 0", None, 0x10),
    ("Numpad1", "Numpad 1", None, 0x11),
    ("Numpad2", "Numpad 2", None, 0x12),
    ("Numpad3", "Numpad 3", None, 0x13),
    ("Numpad4", "Numpad 4", None, 0x14),
    ("Numpad5", "Numpad 5", None, 0x15),
    ("Numpad6", "Numpad 6", None, 0x16),
    ("Numpad7", "Numpad 7", None, 0x17),
    ("Numpad8", "Numpad 8", None, 0x18),
    ("Numpad9", "Numpad 9", None, 0x19),
    ("ContrastUp", "Contrast Up", None, 0x28),
    ("ContrastDown", "Contrast Down", None, 0x29),
    ("BrightnessUp", "Brightness Up", None, 0x2a),
    ("BrightnessDown", "Brightness Down", None, 0x2b),
)

STX = 0x02

class Barco(eg.PluginClass):
    
    def __init__(self):
        for evalName, tmpName, tmpDescription, tmpValue in ACTIONS:
            class TmpAction(ActionBase):
                name = tmpName
                description = tmpDescription
                value = tmpValue
            TmpAction.__name__ = evalName
            self.AddAction(TmpAction)
    
    
    @eg.LogIt
    def __start__(self, port=0, address=0):
        self.port = port
        self.address = 0
        self.serialThread = eg.SerialThread()
        self.serialThread.Open(port)
        self.serialThread.Start()
        
        
    def __stop__(self):
        self.serialThread.Close()
        
        
    def DoCommand(self, cmd, data1=0, data2=0, data3=0, data4=0):
        data = [self.address, cmd, data1, data2, data3, data4]
        used = {}
        checksum = 0
        for x in data:
            used[x] = True
            checksum += x
        checksum %= 256
        used[checksum] = True
        data.append(checksum % 256)
    
        offset = 1
        while offset in data:
            offset += 1
        offset = (STX - offset) % 256
    
        data = [STX, offset] + [(x + offset) % 256 for x in data]
        s = "".join([chr(x) for x in data])
        self.serialThread.Write(s)

    
    def Configure(self, port=0, address=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        addrCtrl = panel.SpinIntCtrl(address, min=0, max=16)
        panel.AddLine("Serial port:", portCtrl)
        panel.AddLine("Projector address:", addrCtrl)
        while panel.Affirmed():
            panel.SetResult(portCtrl.GetValue(), addrCtrl.GetValue())
            
    
    
class ActionBase(eg.ActionClass):
    
    def __call__(self):
        self.plugin.DoCommand(self.value)
        
