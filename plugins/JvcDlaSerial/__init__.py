#
# JVC DLA Serial Control
# ======================
#
# This plug in is for controlling the following JVC HD-1 projector via RS-232
#
# Except for the power and menu commands, the HD-1 only offers remote control
# emulation (at least, only those are documented). There are two commands which
# yield a reply:
# - Get Power returns the current power status
# - Get Input returns the current input status
# The replies from each command are returned as events.
#

from __future__ import with_statement
import binascii

eg.RegisterPlugin(
    name = "JVC DILA Projector",
    description = "This plugin is for controlling a JVC DILA projectors via RS-232",
    kind = "external",
    author = "Bartman",
    version = "0.1." + "$LastChangedRevision: 374 $".split()[1],
    canMultiLoad = True,
    createMacrosOnAdd = True,
    url = "http://www.eventghost.org/forum/viewtopic.php?t=650",
)


ACK = chr(0x06)
OP = chr(0x21)
REF = chr(0x3f)
UNITID1 = chr(0x89)
UNITID2 = chr(0x01)
END = chr(0x0a)
RESP = chr(0x40)

#these are the actions grouped
PowerActions = ('Power', 'Power', 'Actions to control the power state', (0x50, 0x57),
    (
     ("Get", "Get Power Status", REF, ()),
     ("On", "Turn On Power", OP, (0x31, )),
     ("Off", "Turn Off Power", OP, (0x30, )),
    ))

InputActions = ('Input', 'Input', 'Action to control the input', (0x49, 0x50),
    (
     ("Get", "Get Input Status", REF, ()),
     ("SVideo", "Input S-Video", OP, (0x30, )),
     ("Video", "Input Video", OP, (0x31, )),
     ("Comp", "Input Composite", OP, (0x32, )),
     ("PC", "Input PC", OP, (0x33, )),
     ("HDMI1", "Input HDMI1", OP, (0x36, )),
     ("HDMI2", "Input HDMI2", OP, (0x37, )),
     ("Next", "Next Input", OP, (0x2b, )),
     ("Previous", "Previous Input", OP, (0x2d, )),
     ))

PatternsActions = ('Pattern', 'Test Patterns', 'Show Test Patterns', (0x54, 0x53),
    (
     ("Get", "Get Test Pattern", REF, ()),
     ("Off", "Test Pattern - Off", OP, (0x30, )),
     ("ColorBars", "Test Pattern - Color Bars", OP, (0x31, )),
     ("StairStep", "Test Pattern - Stair step (black and white)", OP, (0x36, )),
     ("StairStepRed", "Test Pattern - Stair step (red)", OP, (0x37, )),
     ("StairStepGreen", "Test Pattern - Stair step (green)", OP, (0x38, )),
     ("StairStepBlue", "Test Pattern - Stair step (blue)", OP, (0x39, )),
     ("Crosshatch", "Test Pattern - Crosshatch (green)", OP, (0x41, )),
     ))

GammaTableActions = ('GammaTable', 'Gamma Table', '', (0x47, 0x53),
    (
     ("Get", "Get Gamma Table Value", REF, ()),
     ("Normal", "Gamma - Normal", OP, (0x30, )),
     ("A", "Gamma - A", OP, (0x31, )),
     ("B", "Gamma - B", OP, (0x32, )),
     ("C", "Gamma - C", OP, (0x33, )),
     ("D", "Gamma - D", OP, (0x37, )),
     ("Custom1", "Gamma - Custom1", OP, (0x34, )),
     ("Custom2", "Gamma - Custom2", OP, (0x35, )),
     ("Custom3", "Gamma - Custom3", OP, (0x36, )),
     ))

GammaValueActions = ('GammaValue', 'Gamma Value', '', (0x47, 0x50),
    (
     ("Get", "Get Gamma Correction Value", REF, ()),
     ("18", "Gamma Correction Value - 1.8", OP, (0x30, )),
     ("19", "Gamma Correction Value - 1.9", OP, (0x31, )),
     ("20", "Gamma Correction Value - 2.0", OP, (0x32, )),
     ("21", "Gamma Correction Value - 2.1", OP, (0x33, )),
     ("22", "Gamma Correction Value - 2.2", OP, (0x34, )),
     ("23", "Gamma Correction Value - 2.3", OP, (0x35, )),
     ("24", "Gamma Correction Value - 2.4", OP, (0x36, )),
     ("25", "Gamma Correction Value - 2.5", OP, (0x37, )),
     ("26", "Gamma Correction Value - 2.6", OP, (0x38, )),
     ))

RemoteActions = ('Remote', 'Remote Control Emulation', 'Emulates remote control key presses', (0x52, 0x43, 0x37, 0x33),
    (
     ("Advanced", "Picture Adjust > Advanced", OP, (0x37, 0x33)),
     ("Aspect16_9", "Aspect - 16:9", OP, (0x32, 0x36)),
     ("Aspect4_3", "Aspect - 4:3", OP, (0x32, 0x35)),
     ("AspectZoom", "Aspect - Zoom", OP, (0x32, 0x37)),
     ("AspectCycle", "Aspect - Cycle", OP, (0x37, 0x37)),
     ("Back", "Back", OP, (0x30, 0x33)),
     ("BnrOff", "Block Noise Reduction Off", OP, (0x31, 0x30)),
     ("BnrOn", "Block Noise Reduction On", OP, (0x30, 0x46)),
     ("BrightnessDown", "Brightness Down", OP, (0x37, 0x42)),
     ("BrightnessUp", "BrightnessUp", OP, (0x37, 0x41)),
     ("BrightnessAdjustmentBar", "Brightness Adjustment Bar Toggle", OP, (0x30, 0x39)),
     ("CecOff", "CEC Off", OP, (0x35, 0x37)),
     ("CecOn", "CEC On", OP, (0x35, 0x36)),
     ("ColorDown", "Color Down", OP, (0x37, 0x44)),
     ("ColorUp", "Color Up", OP, (0x37, 0x43)),
     ("ColorAdjustmentBar", "Color Adjustment Bar Toggle", OP, (0x31, 0x35)),
     ("ColorManagementCustom1", "Color Management - Custom1", OP, (0x36, 0x31)),
     ("ColorManagementCustom2", "Color Management - Custom2", OP, (0x36, 0x32)),
     ("ColorManagementCustom3", "Color Management - Custom3", OP, (0x36, 0x33)),
     ("ColorManagementOff", "Color Management - Off", OP, (0x36, 0x30)),
     ("ColorTemp5800K", "Color Temperature - 5800 K", OP, (0x34, 0x45)),
     ("ColorTemp6500K", "Color Temperature - 6500 K", OP, (0x34, 0x46)),
     ("ColorTemp7500K", "Color Temperature - 7500 K", OP, (0x35, 0x30)),
     ("ColorTemp9300K", "Color Temperature - 9300 K", OP, (0x35, 0x31)),
     ("ColorTempCustom1", "Color Temperature - Custom1", OP, (0x35, 0x33)),
     ("ColorTempCustom2", "Color Temperature - Custom2", OP, (0x35, 0x34)),
     ("ColorTempCustom3", "Color Temperature - Custom3", OP, (0x35, 0x35)),
     ("ColorTempHighBright", "Color Temperature - High Bright", OP, (0x35, 0x32)),
     ("ColorTempCycle", "Color Temperature - Cycle", OP, (0x37, 0x36)),
     ("ContrastDown", "Contrast Down", OP, (0x37, 0x39)),
     ("ContrastUp", "Contrast Up", OP, (0x37, 0x38)),
     ("ContrastAdjustmentBar", "Contrast Adjustment Bar Toggle", OP, (0x30, 0x41)),
     ("CtiOff", "Color Transient Improvement - Off", OP, (0x35, 0x43)),
     ("CtiLow", "Color Transient Improvement - Low", OP, (0x35, 0x44)),
     ("CtiMiddle", "Color Transient Improvement - Middle", OP, (0x35, 0x45)),
     ("CtiHigh", "Color Transient Improvement - High", OP, (0x35, 0x46)),
     ("CursorDown", "Cursor Down", OP, (0x30, 0x32)),
     ("CursorUp", "Cursor Up", OP, (0x03, 0x31)),
     ("CursorLeft", "Cursor Left", OP, (0x33, 0x36)),
     ("CursorRight", "Cursor Right", OP, (0x33, 0x34)),
     ("DetailEnhanceDown", "Detail Enhance Down", OP, (0x31, 0x32)),
     ("DetailEnhanceUp", "Detail Enhance Up", OP, (0x31, 0x31)),
     ("GammaA", "Gamma - A", OP, (0x33, 0x39)),
     ("GammaB", "Gamma - B", OP, (0x33, 0x41)),
     ("GammaC", "Gamma - C", OP, (0x33, 0x42)),
     ("GammaD", "Gamma - D", OP, (0x33, 0x46)),
     ("GammaCustom1", "Gamma - Custom1", OP, (0x33, 0x43)),
     ("GammaCustom2", "Gamma - Custom2", OP, (0x33, 0x44)),
     ("GammaCustom3", "Gamma - Custom3", OP, (0x33, 0x45)),
     ("GammaNormal", "Gamma - Normal", OP, (0x33, 0x38)),
     ("GammaCycle", "Gamma - Cycle", OP, (0x37, 0x35)),
     ("Hide", "Hide (Toggle)", OP, (0x31, 0x44)),
     ("Information", "Information", OP, (0x37, 0x34)),
     ("InputComponent", "Input - Component", OP, (0x34, 0x44)),
     ("InputHDMI1", "Input - HDMI-1", OP, (0x37, 0x30)),
     ("InputHDMI2", "Input - HDMI-2", OP, (0x37, 0x31)),
     ("InputPC", "Input - PC", OP, (0x34, 0x36)),
     ("InputSVideo", "Input - S-Video", OP, (0x34, 0x43)),
     ("InputVideo", "Input - Video", OP, (0x34, 0x42)),
     ("InputCycle", "Input - Cycle", OP, (0x30, 0x38)),
     ("IsfOff", "ISF - Off", OP, (0x35, 0x41)),
     ("IsfOn", "ISF - On", OP, (0x35, 0x42)),
     ("KeyStoneHorizontalDown", "Keystone Correction Horizontal Down", OP, (0x34, 0x31)),
     ("KeyStoneHorizontalUp", "Keystone Correction Horizontal Up", OP, (0x34, 0x30)),
     ("KeyStoneVerticalDown", "Keystone Correction Vertical Down", OP, (0x31, 0x43)),
     ("KeyStoneVerticalUp", "Keystone Correction Vertical Up", OP, (0x31, 0x42)),
     ("LensAperture1", "Lens Aperture - 1", OP, (0x32, 0x38)),
     ("LensAperture2", "Lens Aperture - 2", OP, (0x32, 0x39)),
     ("LensAperture3", "Lens Aperture - 3", OP, (0x32, 0x41)),
     ("LensApertureAdjustment", "Lens Aperture - Adjustment", OP, (0x32, 0x30)),
     ("LensFocusDown", "Lens Focus Down", OP, (0x33, 0x32)),
     ("LensFocusUp", "Lens Focus Up", OP, (0x33, 0x21)),
     ("LensShiftDown", "LensShift - Down", OP, (0x32, 0x32)),
     ("LensShiftLeft", "LensShift - Left", OP, (0x334, 0x34)),
     ("LensShiftRight", "LensShift - Right", OP, (0x34, 0x33)),
     ("LensShiftUp", "LensShift - Up", OP, (0x32, 0x31)),
     ("LensZoomIn", "Lens Zoom - In", OP, (0x33, 0x35)),
     ("LensZoomOut", "Lens Zoom - Out", OP, (0x33, 0x37)),
     ("Menu", "Menu Toggle", OP, (0x32, 0x45)),
     ("MenuPosition", "Menu Position", OP, (0x34, 0x32)),
     ("MnrDown", "Mosquito Noise Reduction Down", OP, (0x30, 0x45)),
     ("MnrUp", "Mosquito Noise Reduction Up", OP, (0x30, 0x44)),
     ("NoiseReduction", "Noise Reduction Toggle", OP, (0x31, 0x38)),
     ("OK", "OK", OP, (0x32, 0x46)),
     ("PictureAdjust", "Picture Adjust", OP, (0x37, 0x32)),
     ("PictureModeCinema1", "Picture Mode - Cinema1", OP, (0x36, 0x39)),
     ("PictureModeCinema2", "Picture Mode - Cinema2", OP, (0x36, 0x38)),
     ("PictureModeCinema3", "Picture Mode - Cinema3", OP, (0x36, 0x36)),
     ("PictureModeDynamic", "Picture Mode - Dynamic", OP, (0x36, 0x42)),
     ("PictureModeNatural", "Picture Mode - Natural", OP, (0x36, 0x41)),
     ("PictureModeStage", "Picture Mode - Stage", OP, (0x36, 0x37)),
     ("PictureModeThx", "Picture Mode - THX", OP, (0x36, 0x46)),
     ("PictureModeUser1", "Picture Mode - User1", OP, (0x36, 0x43)),
     ("PictureModeUser2", "Picture Mode - User2", OP, (0x36, 0x44)),
     ("PictureModeUser3", "Picture Mode - User3", OP, (0x36, 0x45)),
     ("PowerOff", "Power - Off", OP, (0x30, 0x36)),
     ("PowerOn", "Power - On", OP, (0x30, 0x35)),
     ("QuickAlign", "Quick Align", OP, (0x31, 0x33)),
     ("RnrDown", "Random Noise Reduction Down", OP, (0x30, 0x43)),
     ("RnrUp", "Random Noise Reduction Up", OP, (0x30, 0x42)),
     ("SharpnessDown", "Sharpness Down", OP, (0x37, 0x46)),
     ("SharpnessUp", "Sharpness Up", OP, (0x37, 0x45)),
     ("SharpnessAdjustmentBar", "Sharpness Adjustment Bar Toggle", OP, (0x31, 0x34)),
     ("ShutterClose", "Shutter - Close", OP, (0x31, 0x39)),
     ("ShutterOpen", "Shutter - Open", OP, (0x31, 0x41)),
     ("ShutterOn", "Shutter - On", OP, (0x32, 0x43)),
     ("ShutterOff", "Shutter - Off", OP, (0x32, 0x44)),
     ("TestPattern", "Test Pattern", OP, (0x35, 0x39)),
     ("TintAdjustmentBar", "Tint Adjustment Bar Toggle", OP, (0x31, 0x36)),
     ("VerticalStretchOff", "Vertical Stretch - Off", OP, (0x32, 0x34)),
     ("VerticalStretchOn", "Vertical Stretch - On", OP, (0x32, 0x33)),
     ))

TestActions = ('', 'Test Command', '', (),
    (
     ("Null", "Check Connection", OP, (0x00, 0x00)),
     ("GetModel", "Get Model", REF, (0x4d, 0x44)),
     ("GetSourceState", "Get Source State", REF, (0x53, 0x43)),
     ))

ACTIONS = (PowerActions, InputActions, PatternsActions, GammaTableActions, GammaValueActions, RemoteActions, TestActions)
            
class ActionBase(eg.ActionClass):
    
    def __call__(self):
        with self.plugin.serialThread as serial:
            self.SendCommand(serial, self.cmd, self.groupData, self.data)


    def SendCommand(self, serial, cmd, groupData, data):
        serial.Write(cmd)
        serial.Write(UNITID1)
        serial.Write(UNITID2)
        serial.Write("".join([chr(x) for x in groupData]))
        serial.Write("".join([chr(x) for x in data]))
        serial.Write(END)
        res = serial.Read(6, 1.0)
        if len(res) != 6 or res[0] != ACK or res[5] != END:
            raise self.Exceptions.DeviceNotFound("Got no ACK!")

class JvcDlaSerial(eg.PluginClass):
    
    def __init__(self):
        self.info.eventPrefix = "JVC-DLA"
        for groupId, groupExternalName, groupDescription, groupTmpData, actions in ACTIONS:
            group = self.AddGroup(groupExternalName, groupDescription)
            for evalName, tmpDescription, tmpCmd, tmpData in actions:
                class TmpAction(ActionBase):
                    name = tmpDescription
                    description = tmpDescription
                    cmd = tmpCmd
                    groupData = groupTmpData
                    data = tmpData
                TmpAction.__name__ = groupId + evalName
                group.AddAction(TmpAction)
    
    
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
        buffer = serial.Read(7, 1.0)
        if len(buffer) == 7:
            code = buffer[3:5]
            if code == "MD":
                buffer += serial.Read(13, 1.0)
            if buffer[0] != RESP or buffer[len(buffer) - 1] != END:
                raise self.Exceptions.DeviceNotReady("Unexpected response " + binascii.hexlify(buffer))
        else:
            raise self.Exceptions.DeviceNotReady("Unexpected response " + binascii.hexlify(buffer))
        
        state = buffer[5:len(buffer) - 1]
        if code == "PW":
            if state == chr(0x30):
                sid ="Standby"
            elif state == chr(0x31):
                sid = "PowerOn"
            elif state == chr(0x32):
                sid = "CoolingDown"
            elif state == chr(0x34):
                sid = "Warning"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("PowerState." + sid)
        elif code == "IP":
            if state == chr(0x30):
                sid = "SVideo"
            elif state == chr(0x31):
                sid = "Video"
            elif state == chr(0x32):
                sid = "Composite"
            elif state == chr(0x33):
                sid = "PC"
            elif state == chr(0x36):
                sid = "HDMI1"
            elif state == chr(0x37):
                sid = "HDMI2"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("Input." + sid)
        elif code == "TS":
            if state == chr(0x30):
                sid = "Off"
            elif state == chr(0x31):
                sid = "ColorBars"
            elif state == chr(0x36):
                sid = "StairStep"
            elif state == chr(0x37):
                sid = "StairStepRed"
            elif state == chr(0x38):
                sid = "StairStepGreen"
            elif state == chr(0x39):
                sid = "StairStepBlue"
            elif state == chr(0x41):
                sid = "Crosshatch"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("TestPattern." + sid)
        elif code == "GS":
            if state == chr(0x30):
                sid = "Normal"
            elif state == chr(0x31):
                sid = "A"
            elif state == chr(0x32):
                sid = "B"
            elif state == chr(0x33):
                sid = "C"
            elif state == chr(0x34):
                sid = "Custom1"
            elif state == chr(0x35):
                sid = "Custom2"
            elif state == chr(0x36):
                sid = "Custom3"
            elif state == chr(0x37):
                sid = "D"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("GammaTable." + sid)
        elif code == "GP":
            if state == chr(0x30):
                sid = "18"
            elif state == chr(0x31):
                sid = "19"
            elif state == chr(0x32):
                sid = "20"
            elif state == chr(0x33):
                sid = "21"
            elif state == chr(0x34):
                sid = "22"
            elif state == chr(0x35):
                sid = "23"
            elif state == chr(0x36):
                sid = "24"
            elif state == chr(0x37):
                sid = "25"
            elif state == chr(0x38):
                sid = "26"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("GammaValue." + sid)
        elif code == "SC":
            if state == chr(0x00):
                sid = "Logo"
            elif state == chr(0x30):
                sid = "NoSignal"
            elif state == chr(0x31):
                sid = "SignalOk"
            else:
                sid = "UNKNOWN%02X" % ord(state)
            self.TriggerEvent("SourceState." + sid)
        elif code == "MD":
            self.TriggerEvent("Model." + state[11:len(state)])
        else:
            raise self.Exceptions.DeviceNotReady("Unexpected response %02X%02X" %(ord(code[0]), ord(code[1])))
        
    
    
    def Configure(self, port=0):
        panel = eg.ConfigPanel(self)
        portCtrl = panel.SerialPortChoice(port)
        panel.AddLine("Serial port:", portCtrl)
        while panel.Affirmed():
            panel.SetResult(
                portCtrl.GetValue(), 
            )
            
    
    
        
