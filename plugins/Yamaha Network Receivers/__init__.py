# Python Imports
import wx.lib.agw.floatspin as FS

# Local Imports
import globals
from client import *
from yamaha import *

# expose some information about the plugin through an eg.PluginInfo subclass
eg.RegisterPlugin(
    name = "Yamaha RX-V Network Receiver",
    author = "Anthony Casagrande (BirdAPI), Jason Kloepping (Dragon470)",
    version = "1.1",
    kind = "external",
    # We don't auto load macros because they are not configured yet.
    createMacrosOnAdd = True,
    canMultiLoad = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=3382",
    description = "Control Yamaha RX-V network receivers."
)

class YamahaRX(eg.PluginClass):
    def __init__(self):
        self.AddAction(SmartVolumeUp, name="Smart Volume Up", clsName="SmartVolumeUp", description="Increases the volume by step1 for a specified period of time, and then increases the volume by step2 each time after.")
        self.AddAction(SmartVolumeDown, name="Smart Volume Down", clsName="SmartVolumeDown", description="Decreases the volume by step1 for a specified period of time, and then decreases the volume by step2 each time after.")
        self.AddAction(SmartVolumeFinished, name="Smart Volume Finished", clsName="SmartVolumeFinished", description="This MUST be called after a Smart Volume Up or Smart Volume Down in order to reset them for the next time.")
        self.AddAction(IncreaseVolume, name="Increase Volume", clsName="IncreaseVolume", description="Increase the volume a specified amount on the specified zone.")
        self.AddAction(DecreaseVolume, name="Decrease Volume", clsName="DecreaseVolume", description="Decrease the volume a specified amount on the specified zone.")
        self.AddAction(SetVolume, name="Set Exact Volume", clsName="SetVolume", description="Set the exact volume on the specified zone.")
        self.AddAction(SetInitVolume, name="Set Initial Volume", clsName="SetInitVolume", description="Set the initial volume when the receiver turns on (zone specific).  The mode controls if the initial volume will retain last volume or reset to the given volume.")
        self.AddAction(SetMaxVolume, name="Set Max Volume", clsName="SetMaxVolume", description="Set the max volume the zone can go.")
        self.AddAction(SetScene, name="Set Scene", clsName="SetScene", description="Change the scene number on the specified zone.")
        self.AddAction(SetSourceInput, name="Set Source Input", clsName="SetSourceInput", description="Set the source input on the specified zone.")
        self.AddAction(NextInput, name="Next Input", clsName="NextInput", description="Set the source input on the specified zone to the next input in the specified list of inputs.")
        self.AddAction(PreviousInput, name="Previous Input", clsName="PreviousInput", description="Set the source input on the specified zone to the previous input in the specified list of inputs.")
        self.AddAction(SetBass, name="Set Exact Bass", clsName="SetBass", description="Set the bass tone control.")
        self.AddAction(SetTreble, name="Set Exact Tremble", clsName="SetTreble", description="Set the treble tone control.")
        self.AddAction(SetPattern1, name="Set Speaker Levels", clsName="SetPattern1", description="Sets the individual speaker levels.")
        self.AddAction(SetFeatureVideoOut, name="Feature Input Video Out", clsName="SetFeatureVideoOut", description="Set the source video output from a specified input.  For Main Zone only.")
        self.AddAction(SetAudioIn, name="Set Audio In for Video Source", clsName="SetAudioIn", description="Sets a particular audio feed for a specific video source.")
        self.AddAction(SetPowerStatus, name="Set Power Status", clsName="SetPowerStatus", description="Set the power status for the receiver (Main Zone), or turn on/off additional zones.")
        self.AddAction(SetSurroundMode, name="Set Surround Mode", clsName="SetSurroundMode", description="Choose between Surround Decode and Straight, or toggle between the two.")
        self.AddAction(Set7ChannelMode, name="Set 7 Channel Mode", clsName="Set7ChannelMode", description="Turn 7 Channel Stereo mode on and off. Usually turned 'On' after setting 'Surround Mode' to 'Surround Decode'.")  # McB 1/11/2014 - Turn 7-channel mode on and off
        self.AddAction(CursorAction, name="Cursor Action", clsName="CursorAction", description="Generic cursor action: Up, Down, Left, Right, Enter, Return, Level, On Screen, Option, Top Menu, Pop Up Menu")
        self.AddAction(SetSleepStatus, name="Set Sleep Status", clsName="SetSleepStatus", description= "Set the sleep state for the receiver (Main Zone), or additional zones.")
        self.AddAction(NumCharAction, name="NumChar Action", clsName="NumCharAction", description="Generic NumChar action: 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, +10, ENT")
        self.AddAction(OperationAction, name="Operation Action", clsName="OperationAction", description="Generic Operation action: Play, Stop, Pause, Search-, Search+, Skip-, Skip+, FM, AM")
        self.AddAction(SetActiveZone, name="Set Active Zone", clsName="SetActiveZone", description="Sets which zone is currently active. This affects any action that is based on 'Active Zone'.")
        self.AddAction(ToggleMute, name="Toggle Mute", clsName="ToggleMute", description="Toggles mute state")
        self.AddAction(ToggleEnhancer, name="Toggle Enhancer", clsName="ToggleEnhancer", description="Toggles the enhancer on and off")
        self.AddAction(NextRadioPreset, name="Next Radio Preset", clsName="NextRadioPreset", description="Goes to next radio preset, or if radio is not on, it turns it on. Also wraps when you go past the last preset.")
        self.AddAction(PreviousRadioPreset, name="Previous Radio Preset", clsName="PreviousRadioPreset", description="Goes to previous radio preset, or if radio is not on, it turns it on. Also wraps to the end when you go past the first preset.")
        self.AddAction(ToggleRadioAMFM, name="Toggle Radio AM / FM", clsName="ToggleRadioAMFM", description="Toggles radio between AM and FM")
        self.AddAction(RadioAutoFreqUp, name="Radio Auto Freq Up", clsName="RadioAutoFreqUp", description="Auto increases the radio frequency")
        self.AddAction(RadioAutoFreqDown, name="Radio Auto Freq Down", clsName="RadioAutoFreqDown", description="Auto decreases the radio frequency")
        self.AddAction(RadioFreqUp, name="Radio Freq Up", clsName="RadioFreqUp", description="Increases the radio frequency")
        self.AddAction(RadioFreqDown, name="Radio Freq Down", clsName="RadioFreqDown", description="Decreases the radio frequency")
        self.AddAction(RadioSetExact, name="Radio Set Station", clsName="RadioSetExact", description="Set an exact radio station to go to.")
        self.AddAction(InputVolumeTrim, name="Source Volume Trim", clsName="InputVolumeTrim", description="Each source volume trim (-6.0 dB to 6.0 dB).")
        self.AddAction(SetDisplayDimmer, name="Set Display Brightness", clsName="SetDisplayDimmer", description="Sets the front display brightness level.")
        self.AddAction(SetWallPaper, name="Set Wall Paper", clsName="SetWallPaper", description="Sets the background image for use when no video source is in use as a background.")
        self.AddAction(GetInfo, name="Get Info", clsName="GetInfo", description="Gets various info from the receiver.")
        self.AddAction(GetAvailability, name="Get Availability", clsName="GetAvailability", description="Gets the available input sources.")
        self.AddAction(SendAnyCommand, name="Send Any Command", clsName="SendAnyCommand", description="Sends any command in YNC.")
        self.grp1 = self.AddGroup('Config', 'General configuration actions')
        self.grp1.AddAction(AutoDetectIP, name="Auto Detect IP", clsName="AutoDetectIP", description="Runs the IP Address auto detection in case your receiver's ip address has changed since starting EventGhost.")
        self.grp1.AddAction(VerifyStaticIP, name="Verify Static IP", clsName="VerifyStaticIP", description="Checks whether there is a Yamaha AV Receiver at the other end of the static ip specified in the configuration.")
        #Add all actions again but hidden so they can be exposed for eg python scripts (not sure why adding clsName removes the ability to call the action outside the plugin)
        self.AddAction(SmartVolumeUp, hidden=True)
        self.AddAction(SmartVolumeDown, hidden=True)
        self.AddAction(SmartVolumeFinished, hidden=True)
        self.AddAction(IncreaseVolume, hidden=True)
        self.AddAction(DecreaseVolume, hidden=True)
        self.AddAction(SetVolume, hidden=True)
        self.AddAction(SetInitVolume, hidden=True)
        self.AddAction(SetMaxVolume, hidden=True)
        self.AddAction(SetScene, hidden=True)
        self.AddAction(SetSourceInput, hidden=True)
        self.AddAction(NextInput, hidden=True)
        self.AddAction(SetFeatureVideoOut, hidden=True)
        self.AddAction(SetFeatureVideoOut, hidden=True)
        self.AddAction(SetWallPaper, hidden=True)
        self.AddAction(PreviousInput, hidden=True)
        self.AddAction(SetBass, hidden=True)
        self.AddAction(SetTreble, hidden=True)
        self.AddAction(SetPattern1, hidden=True)
        self.AddAction(SetPowerStatus, hidden=True)
        self.AddAction(SetSurroundMode, hidden=True)
        self.AddAction(Set7ChannelMode, hidden=True) # McB 1/11/2014 - Turn 7-channel mode on and off
        self.AddAction(CursorAction, hidden=True)
        self.AddAction(SetSleepStatus, hidden=True)
        self.AddAction(NumCharAction, hidden=True)
        self.AddAction(OperationAction, hidden=True)
        self.AddAction(SetActiveZone, hidden=True)
        self.AddAction(ToggleMute, hidden=True)
        self.AddAction(ToggleEnhancer, hidden=True)
        self.AddAction(NextRadioPreset, hidden=True)
        self.AddAction(PreviousRadioPreset, hidden=True)
        self.AddAction(ToggleRadioAMFM, hidden=True)
        self.AddAction(RadioAutoFreqUp, hidden=True)
        self.AddAction(RadioAutoFreqDown, hidden=True)
        self.AddAction(RadioFreqUp, hidden=True)
        self.AddAction(RadioFreqDown, hidden=True)
        self.AddAction(RadioSetExact, hidden=True)
        self.AddAction(InputVolumeTrim, hidden=True)
        self.AddAction(GetInfo, hidden=True)
        self.AddAction(SetDisplayDimmer, hidden=True)
        self.AddAction(GetAvailability, hidden=True)
        self.AddAction(SendAnyCommand, hidden=True)
        self.grp1.AddAction(AutoDetectIP, hidden=True)
        self.grp1.AddAction(VerifyStaticIP, hidden=True)
        
        # added again here so legacy configs will be maintained (no future added actions need to be added below)
        self.AddAction(SmartVolumeUp, hidden=True, clsName="Smart Volume Up")
        self.AddAction(SmartVolumeDown, hidden=True, clsName="Smart Volume Down")
        self.AddAction(SmartVolumeFinished, hidden=True, clsName="Smart Volume Finished")
        self.AddAction(IncreaseVolume, hidden=True, clsName="Increase Volume")
        self.AddAction(DecreaseVolume, hidden=True, clsName="Decrease Volume")
        self.AddAction(SetVolume, hidden=True, clsName="Set Exact Volume")
        self.AddAction(SetInitVolume, hidden=True, clsName="Set Initial Volume")
        self.AddAction(SetMaxVolume, hidden=True, clsName="Set Max Volume")
        self.AddAction(SetScene, hidden=True, clsName="Set Scene")
        self.AddAction(SetSourceInput, hidden=True, clsName="Set Source Input")
        self.AddAction(NextInput, hidden=True, clsName="Next Input")
        self.AddAction(PreviousInput, hidden=True, clsName="Previous Input")
        self.AddAction(SetBass, hidden=True, clsName="Set Exact Bass")
        self.AddAction(SetTreble, hidden=True, clsName="Set Exact Tremble")
        self.AddAction(SetPattern1, hidden=True, clsName="Set Speaker Levels")
        self.AddAction(SetFeatureVideoOut, hidden=True, clsName="Feature Input Video Out")
        self.AddAction(SetAudioIn, hidden=True, clsName="Set Audio In for Video Source")
        self.AddAction(SetPowerStatus, hidden=True, clsName="Set Power Status")
        self.AddAction(SetSurroundMode, hidden=True, clsName="Set Surround Mode")
        self.AddAction(Set7ChannelMode, hidden=True, clsName="Set 7 Channel Mode")  # McB 1/11/2014 - Turn 7-channel mode on and off
        self.AddAction(CursorAction, hidden=True, clsName="Cursor Action")
        self.AddAction(SetSleepStatus, hidden=True, clsName="Set Sleep Status")
        self.AddAction(NumCharAction, hidden=True, clsName="NumChar Action")
        self.AddAction(OperationAction, hidden=True, clsName="Operation Action")
        self.AddAction(SetActiveZone, hidden=True, clsName="Set Active Zone")
        self.AddAction(ToggleMute, hidden=True, clsName="Toggle Mute")
        self.AddAction(ToggleEnhancer, hidden=True, clsName="Toggle Enhancer")
        self.AddAction(NextRadioPreset, hidden=True, clsName="Next Radio Preset")
        self.AddAction(PreviousRadioPreset, hidden=True, clsName="Previous Radio Preset")
        self.AddAction(ToggleRadioAMFM, hidden=True, clsName="Toggle Radio AM / FM")
        self.AddAction(RadioAutoFreqUp, hidden=True, clsName="Radio Auto Freq Up")
        self.AddAction(RadioAutoFreqDown, hidden=True, clsName="Radio Auto Freq Down")
        self.AddAction(RadioFreqUp, hidden=True, clsName="Radio Freq Up")
        self.AddAction(RadioFreqDown, hidden=True, clsName="Radio Freq Down")
        self.AddAction(RadioSetExact, hidden=True, clsName="Radio Set Station")
        self.AddAction(InputVolumeTrim, hidden=True, clsName="Source Volume Trim")
        self.AddAction(SetDisplayDimmer, hidden=True, clsName="Set Display Brightness")
        self.AddAction(SetWallPaper, hidden=True, clsName="Set Wall Paper")
        self.AddAction(GetInfo, hidden=True, clsName="Get Info")
        self.AddAction(GetAvailability, hidden=True, clsName="Get Availability")
        self.AddAction(SendAnyCommand, hidden=True, clsName="Send Any Command")
        self.grp1 = self.AddGroup('Config', 'General configuration actions')
        self.grp1.AddAction(AutoDetectIP, hidden=True, clsName="Auto Detect IP")
        self.grp1.AddAction(VerifyStaticIP, hidden=True, clsName="Verify Static IP")
        
    def __start__(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0, default_timeout=3.0):
        self.ip_address = ip_address
        self.port = port
        self.ip_auto_detect = ip_auto_detect
        self.auto_detect_model = auto_detect_model
        self.auto_detect_timeout = auto_detect_timeout
        self.default_timeout = default_timeout
        self.FOUND_IP = None
        self.MODEL = None
        self.active_zone = 0
        self.smart_vol_up_start = None
        self.smart_vol_down_start = None
        ip = setup_ip(self)
        
        #populated by the Setup Availability function
        # Available zones/sources. These are to be generated based on availability
        self.AVAILABLE_ZONES = []
        self.AVAILABLE_SOURCES = []
        self.AVAILABLE_INFO_SOURCES = []
        self.AVAILABLE_FEATURE_SOURCES = []
        self.AVAILABLE_INPUT_SOURCES = []
        self.AVAILABLE_SOURCES_RENAME = []
        
        if ip is not None:
            setup_availability(self)

    def autoDetectChanged(self, event):
        if self.cb.GetValue():
            self.txt_ip.Hide()
            self.lbl_ip.Hide()
            
            self.lbl_model.Show()
            self.combo.Show()
        else:
            self.txt_ip.Show()
            self.lbl_ip.Show()
            
            self.lbl_model.Hide()
            self.combo.Hide()

            self.txt_ip.SetFocus()
            self.txt_ip.SetInsertionPoint(len(self.txt_ip.GetValue()))
        
    def Configure(self, ip_address="", port=80, ip_auto_detect=True, auto_detect_model="ANY", auto_detect_timeout=1.0, default_timeout=3.0):
        x_start = 10
        x_padding = 60
        y_start = 10
        y_padding = 22
        label_padding = 3
        i = 0

        if ip_address == "":
            # Default ip address to network prefix to save typing
            ip_address = get_network_prefix() + '.'
        
        panel = eg.ConfigPanel()

        lbl_net = wx.StaticText(panel, label="Network Settings: ", pos=(0, y_start + label_padding + (i * y_padding)))
        font = lbl_net.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        lbl_net.SetFont(font)
        
        i += 1
        # Auto Detect IP
        self.cb = wx.CheckBox(panel, -1, 'Auto Detect IP Address', (x_start, y_start + (i * y_padding)))
        self.cb.SetValue(ip_auto_detect)
        self.cb.Bind(wx.EVT_CHECKBOX, self.autoDetectChanged)
        
        i += 1
        # IP Address
        self.lbl_ip = wx.StaticText(panel, label="Static IP Address: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.txt_ip = wx.TextCtrl(panel, -1, ip_address, (x_start + (x_padding * 2), y_start + (i * y_padding)), (100, -1))
        
        # Do not add to index, so they go over top each other
        # Models (Auto Detect)
        self.lbl_model = wx.StaticText(panel, label="AV Receiver Model (If you have multiple on network): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.combo = wx.ComboBox(panel, -1, pos=(x_start + (x_padding * 4.5), y_start + (i * y_padding)), size=(100, -1), choices=globals.ALL_MODELS, style=wx.CB_DROPDOWN)
        self.combo.SetValue(auto_detect_model)
        
        i += 1
        lbl_adv = wx.StaticText(panel, label="Advanced Settings: ", pos=(0, y_start + label_padding + (i * y_padding)))
        font = lbl_adv.GetFont()
        font.SetPointSize(10)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        lbl_adv.SetFont(font)
        
        i += 1
        # Port
        wx.StaticText(panel, label="Port: ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.spin = wx.SpinCtrl(panel, -1, "", (x_start + x_padding, y_start + (i * y_padding)), (80, -1))
        self.spin.SetRange(1,65535)
        self.spin.SetValue(int(port))
        
        i += 1
        # Auto Detect Timeout
        wx.StaticText(panel, label="Auto Detect IP Timeout (seconds): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.auto_time = FS.FloatSpin(panel, -1, pos=(x_start + (x_padding * 3), y_start + (i * y_padding)), min_val=0.1, max_val=10.0,
                                 increment=0.1, value=float(auto_detect_timeout), agwStyle=FS.FS_LEFT)
        self.auto_time.SetFormat("%f")
        self.auto_time.SetDigits(1)
        
        i += 1
        # Default Timeout
        wx.StaticText(panel, label="Default Timeout (seconds): ", pos=(x_start, y_start + label_padding + (i * y_padding)))
        self.def_time = FS.FloatSpin(panel, -1, pos=(x_start + (x_padding * 3), y_start + (i * y_padding)), min_val=0.1, max_val=10.0,
                                 increment=0.1, value=float(default_timeout), agwStyle=FS.FS_LEFT)
        self.def_time.SetFormat("%f")
        self.def_time.SetDigits(1)
        
        # Call this once after setting everything up to change the visibility of things
        self.autoDetectChanged(None)

        while panel.Affirmed():
            panel.SetResult(self.txt_ip.GetValue(), self.spin.GetValue(), self.cb.GetValue(), str(self.combo.GetValue()), self.auto_time.GetValue(), self.def_time.GetValue())
        
