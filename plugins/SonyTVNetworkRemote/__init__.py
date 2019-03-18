import urllib2
import json  #This is used to parse any JSON responses.

# Note:  You should configure the TV (or your router) so that the TV always receives the same IP address.

global globalIp #This will store the IP address of the TV.  (The port number is apparently always 80.)
global globalPreSharedKey #This will store the "pre-shared key".
global globalSOAPStrings  #This will store the SOAP strings for the http connection.

#Pre-shared key can be adjusted on your TV by going to:
#Settings
#  Network
#    Home network setup
#      IP Address Control
#       Authentication
#          Set to:  Normal & Preshared Key
#          Preshared Key
#            For example:  1111 <- just choose one>

eg.RegisterPlugin(
    name = "Sony TV Network Remote Plugin",
    guid='{D814F63D-D2BB-4119-8B94-C487A2C4AAD4}',
    author = "Toby Gerenger, paseant, blaher", 
    version = "0.0.3",
    kind = "external",
    createMacrosOnAdd = True,
    url = "http://www.eventghost.net/forum/viewtopic.php?f=9&t=6067",
    descripAddresstion = "This plugin connects to the network control interface for certain Sony TVs.  The included codes are for a Sony Bravia 2015 model KDL65W850C.  These codes seem to be fairly consistent across Sony's TV lines (including 2018 models)."
)

class SonyTVNetworkPlugin(eg.PluginBase):
    def __init__(self):
        group1 = self.AddGroup("RemoteControl","Send commands as if pushing buttons on the remote control.")
        group1.AddActionsFromList(REMOTE_ACTIONS, TVRemoteAction)
        self.AddAction(SendCommand)
        self.AddAction(GetCurrentInput)
        self.AddAction(SetCurrentInput)
        
    def __start__(self, ipAddress, preSharedKey):
        global globalIp
        global globalPreSharedKey
        global globalSOAPStrings

        globalIp = ipAddress
        globalPreSharedKey = preSharedKey
        globalSOAPStrings = SOAPStrings()
        
    def __stop__(self):
        pass

    def Configure(self, ipAddress='192.168.0.115', preSharedKey='1111'):
        panel = eg.ConfigPanel()
        textControlIP = wx.TextCtrl(panel, -1, ipAddress)
        textControlPSK = wx.TextCtrl(panel, -1, preSharedKey)
        panel.sizer.Add(wx.StaticText(panel, -1, "TV's IP Address:"))
        panel.sizer.Add(textControlIP)
        panel.sizer.Add(wx.StaticText(panel, -1, "TV's Pre-shared Key:"))
        panel.sizer.Add(textControlPSK)
        while panel.Affirmed():
            panel.SetResult(textControlIP.GetValue(), textControlPSK.GetValue())

class TVRemoteAction(eg.ActionClass):
    def __call__(self):
        SendIRCC(self.value)

class SendCommand(eg.ActionBase):
    name = "Send Command"
    description = "Sends an IRCC code to the TV.  For example, this code will mute the TV:  AAAAAQAAAAEAAAAUAw=="

    def __call__(self, commandString):
        SendIRCC(commandString)

    def Configure(self, commandString=""):
        panel = eg.ConfigPanel()
        textControlCmd = wx.TextCtrl(panel, -1, commandString)
        panel.sizer.Add(textControlCmd, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControlCmd.GetValue())

class GetCurrentInput(eg.ActionBase):
    name = "Get Current Input"
    description = "Returns the current TV input URI.  For example: extInput:hdmi?port=2"

    def __call__(self):
        try:
            return json.loads(SendAvContent("""{"id":1,"method":"getPlayingContentInfo","version":"1.0","params":["1.0"]}"""))["result"][0]["uri"]
            
        except:
            print("Cannot get current input.  TV may be off, or not set to an external input.")
            return "Exception"

class SetCurrentInput(eg.ActionBase):
    name = "Set Current Input"
    description = "Sets the TV input to an external input URI.  For example: extInput:hdmi?port=2"

    def __call__(self, inputString):
        try:
            return SendAvContent('{"id":101,"method":"setPlayContent","version":"1.0","params":[{"uri":"' + inputString + '"}]}')
            
        except:
            print("Cannot set input.  TV may be off, or invalid input string.")
            return "Exception"
        
    def Configure(self, inputString="extInput:hdmi?port=2"):
        panel = eg.ConfigPanel()
        textControlCmd = wx.TextCtrl(panel, -1, inputString)
        panel.sizer.Add(textControlCmd, 1, wx.EXPAND)
        while panel.Affirmed():
            panel.SetResult(textControlCmd.GetValue())

def SendIRCC(commandString):
    try:
        conn=urllib2.Request('http://' + globalIp + '/sony/IRCC', globalSOAPStrings.contentStart + commandString + globalSOAPStrings.contentEnd, globalSOAPStrings.headers)
        urllib2.urlopen(conn, timeout=.5)
    except:
        print("Generic exception in SendIRCC.  Is the TV on?")
        
def SendAvContent(commandString):
    try:
        conn=urllib2.Request('http://' + globalIp + '/sony/avContent', commandString, globalSOAPStrings.headers)
        response=urllib2.urlopen(conn, timeout=.5)
        return response.read()
    except:
        print("Generic exception in SendAvContent.")
        
class SOAPStrings:
    def __init__(self):
        print "Sony TV's IP set to:" , globalIp
        print "Sony TV's pre-shared key set to:", globalPreSharedKey
                
        self.headers = {
      'X-Auth-psk': globalPreSharedKey,
      'User-Agent': 'TVSideView/2.0.1 CFNetwork/672.0.8 Darwin/14.0.0',
            'Content-Type': 'text/xml; charset=UTF-8',
            'SOAPACTION': '"urn:schemas-sony-com:service:IRCC:1#X_SendIRCC"',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzipAddress, deflate',
            'Host': globalIp,
            'Connection': 'close',}
    
        self.contentStart = """<?xml version="1.0"?>
            <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
            <s:Body>
            <u:X_SendIRCC xmlns:u="urn:schemas-sony-com:service:IRCC:1">
            <IRCCCode>"""
    
        self.contentEnd = """</IRCCCode>
            </u:X_SendIRCC>
            </s:Body>
            </s:Envelope>"""
    
# The action list below consists of the following structure:
# ("class", "Command Name", "Command DescripAddresstion", "parameter"),
REMOTE_ACTIONS = (   
    ("Num1","Num1","Num1","AAAAAQAAAAEAAAAAAw=="),
    ("Num2","Num2","Num2","AAAAAQAAAAEAAAABAw=="),
    ("Num3","Num3","Num3","AAAAAQAAAAEAAAACAw=="),
    ("Num4","Num4","Num4","AAAAAQAAAAEAAAADAw=="),
    ("Num5","Num5","Num5","AAAAAQAAAAEAAAAEAw=="),
    ("Num6","Num6","Num6","AAAAAQAAAAEAAAAFAw=="),
    ("Num7","Num7","Num7","AAAAAQAAAAEAAAAGAw=="),
    ("Num8","Num8","Num8","AAAAAQAAAAEAAAAHAw=="),
    ("Num9","Num9","Num9","AAAAAQAAAAEAAAAIAw=="),
    ("Num0","Num0","Num0","AAAAAQAAAAEAAAAJAw=="),
    ("Num11","Num11","Num11","AAAAAQAAAAEAAAAKAw=="),
    ("Num12","Num12","Num12","AAAAAQAAAAEAAAALAw=="),
    ("Enter","Enter","Enter","AAAAAQAAAAEAAAALAw=="),
    ("GGuide","GGuide","GGuide","AAAAAQAAAAEAAAAOAw=="),
    ("ChannelUp","ChannelUp","ChannelUp","AAAAAQAAAAEAAAAQAw=="),
    ("ChannelDown","ChannelDown","ChannelDown","AAAAAQAAAAEAAAARAw=="),
    ("VolumeUp","VolumeUp","VolumeUp","AAAAAQAAAAEAAAASAw=="),
    ("VolumeDown","VolumeDown","VolumeDown","AAAAAQAAAAEAAAATAw=="),
    ("Mute","Mute","Mute","AAAAAQAAAAEAAAAUAw=="),
    ("TvPower","TvPower","TvPower","AAAAAQAAAAEAAAAVAw=="),
    ("Audio","Audio","Audio","AAAAAQAAAAEAAAAXAw=="),
    ("MediaAudioTrack","MediaAudioTrack","MediaAudioTrack","AAAAAQAAAAEAAAAXAw=="),
    ("Tv","Tv","Tv","AAAAAQAAAAEAAAAkAw=="),
    ("Input","Input","Input","AAAAAQAAAAEAAAAlAw=="),
    ("TvInput","TvInput","TvInput","AAAAAQAAAAEAAAAlAw=="),
    ("TvAntennaCable","TvAntennaCable","TvAntennaCable","AAAAAQAAAAEAAAAqAw=="),
    ("WakeUp","WakeUp","WakeUp","AAAAAQAAAAEAAAAuAw=="),
    ("PowerOff","PowerOff","PowerOff","AAAAAQAAAAEAAAAvAw=="),
    ("Sleep","Sleep","Sleep","AAAAAQAAAAEAAAAvAw=="),
    ("Right","Right","Right","AAAAAQAAAAEAAAAzAw=="),
    ("Left","Left","Left","AAAAAQAAAAEAAAA0Aw=="),
    ("SleepTimer","SleepTimer","SleepTimer","AAAAAQAAAAEAAAA2Aw=="),
    ("Analog2","Analog2","Analog2","AAAAAQAAAAEAAAA4Aw=="),
    ("TvAnalog","TvAnalog","TvAnalog","AAAAAQAAAAEAAAA4Aw=="),
    ("Display","Display","Display","AAAAAQAAAAEAAAA6Aw=="),
    ("Jump","Jump","Jump","AAAAAQAAAAEAAAA7Aw=="),
    ("PicOff","PicOff","PicOff","AAAAAQAAAAEAAAA+Aw=="),
    ("PictureOff","PictureOff","PictureOff","AAAAAQAAAAEAAAA+Aw=="),
    ("Teletext","Teletext","Teletext","AAAAAQAAAAEAAAA\/Aw=="),
    ("Video1","Video1","Video1","AAAAAQAAAAEAAABAAw=="),
    ("Video2","Video2","Video2","AAAAAQAAAAEAAABBAw=="),
    ("AnalogRgb1","AnalogRgb1","AnalogRgb1","AAAAAQAAAAEAAABDAw=="),
    ("Home","Home","Home","AAAAAQAAAAEAAABgAw=="),
    ("Exit","Exit","Exit","AAAAAQAAAAEAAABjAw=="),
    ("PictureMode","PictureMode","PictureMode","AAAAAQAAAAEAAABkAw=="),
    ("Confirm","Confirm","Confirm","AAAAAQAAAAEAAABlAw=="),
    ("Up","Up","Up","AAAAAQAAAAEAAAB0Aw=="),
    ("Down","Down","Down","AAAAAQAAAAEAAAB1Aw=="),
    ("ClosedCaption","ClosedCaption","ClosedCaption","AAAAAgAAAKQAAAAQAw=="),
    ("Component1","Component1","Component1","AAAAAgAAAKQAAAA2Aw=="),
    ("Component2","Component2","Component2","AAAAAgAAAKQAAAA3Aw=="),
    ("Wide","Wide","Wide","AAAAAgAAAKQAAAA9Aw=="),
    ("EPG","EPG","EPG","AAAAAgAAAKQAAABbAw=="),
    ("PAP","PAP","PAP","AAAAAgAAAKQAAAB3Aw=="),
    ("TenKey","TenKey","TenKey","AAAAAgAAAJcAAAAMAw=="),
    ("BSCS","BSCS","BSCS","AAAAAgAAAJcAAAAQAw=="),
    ("Ddata","Ddata","Ddata","AAAAAgAAAJcAAAAVAw=="),
    ("Stop","Stop","Stop","AAAAAgAAAJcAAAAYAw=="),
    ("Pause","Pause","Pause","AAAAAgAAAJcAAAAZAw=="),
    ("Play","Play","Play","AAAAAgAAAJcAAAAaAw=="),
    ("Rewind","Rewind","Rewind","AAAAAgAAAJcAAAAbAw=="),
    ("Forward","Forward","Forward","AAAAAgAAAJcAAAAcAw=="),
    ("DOT","DOT","DOT","AAAAAgAAAJcAAAAdAw=="),
    ("Rec","Rec","Rec","AAAAAgAAAJcAAAAgAw=="),
    ("Return","Return","Return","AAAAAgAAAJcAAAAjAw=="),
    ("Blue","Blue","Blue","AAAAAgAAAJcAAAAkAw=="),
    ("Red","Red","Red","AAAAAgAAAJcAAAAlAw=="),
    ("Green","Green","Green","AAAAAgAAAJcAAAAmAw=="),
    ("Yellow","Yellow","Yellow","AAAAAgAAAJcAAAAnAw=="),
    ("SubTitle","SubTitle","SubTitle","AAAAAgAAAJcAAAAoAw=="),
    ("CS","CS","CS","AAAAAgAAAJcAAAArAw=="),
    ("BS","BS","BS","AAAAAgAAAJcAAAAsAw=="),
    ("Digital","Digital","Digital","AAAAAgAAAJcAAAAyAw=="),
    ("Options","Options","Options","AAAAAgAAAJcAAAA2Aw=="),
    ("Media","Media","Media","AAAAAgAAAJcAAAA4Aw=="),
    ("Prev","Prev","Prev","AAAAAgAAAJcAAAA8Aw=="),
    ("Next","Next","Next","AAAAAgAAAJcAAAA9Aw=="),
    ("DpadCenter","DpadCenter","DpadCenter","AAAAAgAAAJcAAABKAw=="),
    ("CursorUp","CursorUp","CursorUp","AAAAAgAAAJcAAABPAw=="),
    ("CursorDown","CursorDown","CursorDown","AAAAAgAAAJcAAABQAw=="),
    ("CursorLeft","CursorLeft","CursorLeft","AAAAAgAAAJcAAABNAw=="),
    ("CursorRight","CursorRight","CursorRight","AAAAAgAAAJcAAABOAw=="),
    ("ShopRemoteControlForcedDynamic","ShopRemoteControlForcedDynamic","ShopRemoteControlForcedDynamic","AAAAAgAAAJcAAABqAw=="),
    ("FlashPlus","FlashPlus","FlashPlus","AAAAAgAAAJcAAAB4Aw=="),
    ("FlashMinus","FlashMinus","FlashMinus","AAAAAgAAAJcAAAB5Aw=="),
    ("AudioQualityMode","AudioQualityMode","AudioQualityMode","AAAAAgAAAJcAAAB7Aw=="),
    ("DemoMode","DemoMode","DemoMode","AAAAAgAAAJcAAAB8Aw=="),
    ("Analog","Analog","Analog","AAAAAgAAAHcAAAANAw=="),
    ("Mode3D","Mode3D","Mode3D","AAAAAgAAAHcAAABNAw=="),
    ("DigitalToggle","DigitalToggle","DigitalToggle","AAAAAgAAAHcAAABSAw=="),
    ("DemoSurround","DemoSurround","DemoSurround","AAAAAgAAAHcAAAB7Aw=="),
    ("*AD","*AD","*AD","AAAAAgAAABoAAAA7Aw=="),
    ("AudioMixUp","AudioMixUp","AudioMixUp","AAAAAgAAABoAAAA8Aw=="),
    ("AudioMixDown","AudioMixDown","AudioMixDown","AAAAAgAAABoAAAA9Aw=="),
    ("Tv_Radio","Tv_Radio","Tv_Radio","AAAAAgAAABoAAABXAw=="),
    ("SyncMenu","SyncMenu","SyncMenu","AAAAAgAAABoAAABYAw=="),
    ("Hdmi1","Hdmi1","Hdmi1","AAAAAgAAABoAAABaAw=="),
    ("Hdmi2","Hdmi2","Hdmi2","AAAAAgAAABoAAABbAw=="),
    ("Hdmi3","Hdmi3","Hdmi3","AAAAAgAAABoAAABcAw=="),
    ("Hdmi4","Hdmi4","Hdmi4","AAAAAgAAABoAAABdAw=="),
    ("TopMenu","TopMenu","TopMenu","AAAAAgAAABoAAABgAw=="),
    ("PopUpMenu","PopUpMenu","PopUpMenu","AAAAAgAAABoAAABhAw=="),
    ("OneTouchTimeRec","OneTouchTimeRec","OneTouchTimeRec","AAAAAgAAABoAAABkAw=="),
    ("OneTouchView","OneTouchView","OneTouchView","AAAAAgAAABoAAABlAw=="),
    ("DUX","DUX","DUX","AAAAAgAAABoAAABzAw=="),
    ("FootballMode","FootballMode","FootballMode","AAAAAgAAABoAAAB2Aw=="),
    ("iManual","iManual","iManual","AAAAAgAAABoAAAB7Aw=="),
    ("Netflix","Netflix","Netflix","AAAAAgAAABoAAAB8Aw=="),
    ("Assists","Assists","Assists","AAAAAgAAAMQAAAA7Aw=="),
    ("ActionMenu","ActionMenu","ActionMenu","AAAAAgAAAMQAAABLAw=="),
    ("Help","Help","Help","AAAAAgAAAMQAAABNAw=="),
    ("TvSatellite","TvSatellite","TvSatellite","AAAAAgAAAMQAAABOAw=="),
    ("WirelessSubwoofer","WirelessSubwoofer","WirelessSubwoofer","AAAAAgAAAMQAAAB+Aw=="),
)
