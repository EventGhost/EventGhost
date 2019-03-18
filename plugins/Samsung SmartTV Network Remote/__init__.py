"""<rst>
Adds actions to control the Samsung Smart TVs over the newtork

|

**TV IP Address** - the IP address of your TV. You can see it under 
*Menu > Network > Network Status*

**Port** - the port used to send commands. Usualy the port is 55000

**Connection timeout** - use this to control the connection timeout 
in seconds. You can use this to check is the TV powered on or not

**Remote control name** - the name that will appear in your TV when 
allowing it

**TV model** - fill this with your exact TV model (like UE50ES6710)

When the first command is sent to the TV, you will see a prompt on 
the TV to allow the remote. You can remote the remote later from the 
TV menu.

Each remote is identified by your **MAC address** and the 
"**Remote control name**"

This is now a Multi TV Controller You have the Plugin Config Panel which is
a global settings dialog you also have the ability to go into each action
and change the settings in there which will be device specific.

example: you can copy an action to 2 different locations in the tree and have
2 different sets of ip addresses ports remote names and model numbers.

because of this design there is no need to multiload the plugin.

"""



import eg

eg.RegisterPlugin(
    name = "Samsung Smart TV Network Remote",
    guid='{50FC5231-F557-4AE8-97DF-6C0173B21A8D}',
    author = "Georgi Krastev",
    version = "0.0.2",
    kind = "external",
    description = __doc__,
    createMacrosOnAdd = True
)


import socket
import base64
import time, datetime
from types import ClassType
from uuid import getnode as get_mac

class Text:
    TCPBox = "TCP/IP Settings"
    HostText = "IP Address: "
    PortText = "Port: "
    TVBox = "TV Setings"
    RemoteText = "Remote Name: "
    ModelText = "TV Model: "
    TimeoutBox = "Timeout Settings"
    TimeoutText = "TimeOut: "
    CustomBox = "Custom Remote Button"
    CustomText = "Button: "
    ButtonBox = "Remote Buttons"
    ButtonText = "Button Name: "
    class MyKey:
        name = "Send Custom Key"
        description = "Send a custom remote control button"
    class SendKey:
        name = "Send Key"
        description = "Send a remote control button"


class SamsungSmartTVRemote(eg.PluginBase):

    text = Text

    def __init__(self):

        self.CONNECTION = CONNECTION(self)

        self.AddActionsFromList(ACTION)
        self.AddAction(SendKey)
        self.AddAction(MyKey)
            
    def __start__(self, host, port, remote, tvmodel, timeout):

        self.timeout = timeout

        self.CONNECTION.Default(host, port, remote, tvmodel)
    
    def Configure(self, host=False, port=55000, remote=False, tvmodel=False, timeout=1):

        text = self.text
        panel = eg.ConfigPanel()

        host,port,remote,tvmodel = self.CONNECTION.Config(host,port,remote,tvmodel)

        st1 = panel.TextCtrl(host)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(remote)
        st4 = panel.TextCtrl(tvmodel)
        st5 = panel.SpinIntCtrl(timeout, max=10)

        eg.EqualizeWidths((st1, st2, st3, st4, st5))

        box1 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.HostText, st1),
                                (text.PortText, st2)
                                )
        box2 = panel.BoxedGroup(
                                text.TVBox,
                                (text.RemoteText, st3),
                                (text.ModelText, st4)
                                )
        box3 = panel.BoxedGroup(
                                text.TimeoutBox,
                                (text.TimeoutText, st5)
                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            (box3, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue()
                            )

    def sendKey(self, skey, appstring):

        mess3 = chr(0x00)+chr(0x00)+chr(0x00) \
                  +chr(len(base64.b64encode(skey))) \
                  +chr(0x00)+base64.b64encode(skey);
        part3 = chr(0x00)+chr(len(appstring))+chr(0x00) \
                  +appstring+chr(len(mess3))+chr(0x00)+mess3
        self.sock.send(part3)

        return True


    def socketInit(self, host, port, remote, tvmodel):
        
        myip = socket.gethostbyname(socket.gethostname())
       
        mac = iter(hex(get_mac())[3:14])
        mymac = '-'.join(a+b for a,b in zip(mac, mac))
        
        appstring = "iphone..iapp.samsung"
        
        tvappstring = "iphone." + tvmodel + ".iapp.samsung"
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.timeout)
        try:
          sock.connect((host, port))
        except:
          #eg.PrintTraceback()
          self.PrintError("SamsungSmartTV: Unable to connect (TV off?)!: "+host+", "+str(port))
          return False

        ipencoded = base64.b64encode(myip)
        macencoded = base64.b64encode(mymac)
        mess1 = chr(0x64)+chr(0x00)+chr(len(ipencoded))+chr(0x00) \
                +ipencoded+chr(len(macencoded))+chr(0x00)+macencoded \
                +chr(len(base64.b64encode(remotename)))+chr(0x00) \
                +base64.b64encode(remotename)
        part1 = chr(0x00)+chr(len(appstring))+chr(0x00)+appstring \
                +chr(len(mess1))+chr(0x00)+mess1

        sock.send(part1)
   
        mess2 = chr(0xc8)+chr(0x00)
        part2 = chr(0x00)+chr(len(appstring))+chr(0x00)+appstring \
                +chr(len(mess2))+chr(0x00)+mess2

        sock.send(part2)
        self.sock = sock
        return True

    def DoCommand(self, cmd, host, port, remote, tvmodel):

        errorText = "SamsungSmartTV: Missing "

        host, port, remote, tvmodel = self.CONNECTION.Check(host, port, remote, tvmodel)

        if not host: errorText += "IP Address"
        if not port: errorText += "Port Number"
        if not remote: errorText += "Remote Name"
        if not tvmodel: errorText += "TV Model"

        if errorText != "SamsungSmartTV: Missing ":
            eg.PrintError(errorText)
            return False

        if self.socketInit(host, port, remote, tvmodel):
            tvappstring = "iphone." + tvmodel + ".iapp.samsung"
            return self.sendKey(cmd, tvappstring)
        else:
            return False

class MyKey(eg.ActionBase):

    text = Text

    def __call__(self, button, host=False, port=False, remote=False, tvmodel=False):

        self.plugin.DoCommand(button, host, port, remote, tvmodel)

    def Configure(self, button="", host="", port=0, remote="", tvmodel=""):

        text = self.text
        panel = eg.ConfigPanel()

        host,port,remote,tvmodel = self.plugin.CONNECTION.Config(host,port,remote,tvmodel)

        st1 = panel.TextCtrl(host)
        st2 = panel.TextCtrl(host)
        st3 = panel.SpinIntCtrl(port, max=65535)
        st4 = panel.TextCtrl(remote)
        st5 = panel.TextCtrl(tvmodel)

        eg.EqualizeWidths((st1, st2, st3, st4, st5))

        box1 = panel.BoxedGroup(
                                text.CustomBox,
                                (text.CustomText, st1)
                                )

        box2 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.HostText, st2),
                                (text.PortText, st3)
                                )
        box3 = panel.BoxedGroup(
                                text.TVBox,
                                (text.RemoteText, st4),
                                (text.ModelText, st5)

                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            (box3, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue()
                            )


class SendKey(eg.ActionBase):

    text = Text

    def __call__(self, button, host=False, port=False, remote=False, tvmodel=False):

        for CommandGroup in ACTION:
            for Command in CommandGroup[4]:
                if button == Command[2]:
                    return self.plugin.DoCommand(Command[4], host, port, remote, tvmodel)

    def Configure(self, button="Empty", host="", port=0, remote="", tvmodel=""):

        text = self.text
        panel = eg.ConfigPanel()
        choices = []

        host,port,remote,tvmodel = self.plugin.CONNECTION.Config(host,port,remote,tvmodel)

        st1 = wx.Choice(parent=panel, pos=(10,10))
        st2 = panel.TextCtrl(host)
        st3 = panel.SpinIntCtrl(port, max=65535)
        st4 = panel.TextCtrl(remote)
        st5 = panel.TextCtrl(tvmodel)

        for CommandGroup in ACTION:
            for Command in CommandGroup[4]:
                choices.append(Command[2])

        st1.AppendItems(items=choices)

        if choices.count(button)==0:
            st1.Select(n=0)
        else:
            st1.SetSelection(int(choices.index(button)))

        eg.EqualizeWidths((st1, st2, st3, st4, st5))

        box1 = panel.BoxedGroup(
                                text.ButtonBox,
                                (text.ButtonText, st1)
                                )
        box2 = panel.BoxedGroup(
                                text.TCPBox,
                                (text.HostText, st2),
                                (text.PortText, st3)
                                )
        box3 = panel.BoxedGroup(
                                text.TVBox,
                                (text.RemoteText, st4),
                                (text.ModelText, st5)
                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND),
                            (box3, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetStringSelection(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue(),
                            st5.GetValue()
                            )


class SendButFunc(eg.ActionBase):

    def __call__(self, host=False, port=False, remote=False, tvmodel=False):

        return self.plugin.DoCommand(self.value, host, port, remote, tvmodel)

    def Configure(self, host="", port=0, remote="", tvmodel=""):

        panel = eg.ConfigPanel()

        host,port,remote,tvmodel = self.plugin.CONNECTION.Config(host,port,remote,tvmodel)
        
        st1 = panel.TextCtrl(host)
        st2 = panel.SpinIntCtrl(port, max=65535)
        st3 = panel.TextCtrl(remote)
        st4 = panel.TextCtrl(tvmodel)

        eg.EqualizeWidths((st1, st2, st3, st4))

        box1 = panel.BoxedGroup(
                                'TCP/IP Settings',
                                ('Host Name: ', st1),
                                ('Port: ', st2)
                                )
        box2 = panel.BoxedGroup(
                                'TV Settings',
                                ('Remote Name: ', st3),
                                ('TV Model: ', st4)

                                )
        panel.sizer.AddMany([
                            (box1, 0, wx.EXPAND),
                            (box2, 0, wx.EXPAND)
                            ])

        while panel.Affirmed():
            panel.SetResult(
                            st1.GetValue(),
                            st2.GetValue(),
                            st3.GetValue(),
                            st4.GetValue()
                            )

class CONNECTION():

    def __init__(self, plugin):

        self.plugin = plugin
        self.host = False
        self.port = False
        self.remote = False
        self.tvmodel = False

    def Default(self, host, port, remote, tvmodel):

        errorText = "SamsungSmartTV: Missing "

        self.host,self.port,self.remote,self.tvmodel = self.Check(host,port,remote,tvmodel)

        if not self.host: errorText += "IP Address"
        if not self.port: errorText += "Port Number"
        if not self.remote: errorText += "Remote Name"
        if not self.tvmodel: errorText += "TV Model"

        if errorText != "SamsungSmartTV: Missing ":
            eg.PrintError(errorText)

    def Config(self, host, port, remote, tvmodel):

        host,port,remote,tvmodel = self.Check(host,port,remote,tvmodel)

        host = host if host and host != "" \
                else self.host if self.host and self.host != "" \
                else "999.999.999.999"
        port = port if port and port != 0 \
                else self.port if self.port and self.port != 0 \
                else 55000
        remote = remote if remote and remote != "" \
                else self.remote if self.remote and self.remote != ""\
                else "Remote Name"
        tvmodel = tvmodel if tvmodel and tvmodel != "" \
                else self.tvmodel if self.tvmodel and self.tvmodel != ""\
                else "TV Model #"

        return host, port, remote, tvmodel

    def Check(self, host, port, remote, tvmodel):

        host = host if host and host != "" and host != "999.999.999.999" \
                else self.host if self.host and self.host != "" and self.host != "999.999.999.999" \
                else False
        port = port if port and port != 0 \
                else self.port if self.port and self.port != 0 \
                else False
        remote = remote if remote and remote != "" and remote != "Remote Name" \
                else self.remote if self.remote and self.remote != "" and self.remote != "Remote Name" \
                else False
        tvmodel = tvmodel if tvmodel and tvmodel != "" and tvmodel != "TV Model #" \
                else self.tvmodel if self.tvmodel and self.tvmodel != "" and self.tvmodel != "TV Model #" \
                else False
        return host, port, remote, tvmodel

ACTION = (
(eg.ActionGroup, 'Power', 'Power Keys', 'Power Keys ',(
  (SendButFunc, 'fnKEY_POWEROFF', 'Power OFF', 'Power OFF', 'KEY_POWEROFF'),
  )),
(eg.ActionGroup, 'Input', 'Input Keys', 'Input Keys ',(
  (SendButFunc, 'fnKEY_COMPONENT1', 'Component 1', 'Component 1', 'KEY_COMPONENT1'),
  (SendButFunc, 'fnKEY_COMPONENT2', 'Component 2', 'Component 2', 'KEY_COMPONENT2'),
  (SendButFunc, 'fnKEY_AV1', 'AV 1', 'AV 1', 'KEY_AV1'),
  (SendButFunc, 'fnKEY_AV2', 'AV 2', 'AV 2', 'KEY_AV2'),
  (SendButFunc, 'fnKEY_AV3', 'AV 3', 'AV 3', 'KEY_AV3'),
  (SendButFunc, 'fnKEY_SVIDEO1', 'S Video 1', 'S Video 1', 'KEY_SVIDEO1'),
  (SendButFunc, 'fnKEY_SVIDEO2', 'S Video 2', 'S Video 2', 'KEY_SVIDEO2'),
  (SendButFunc, 'fnKEY_SVIDEO3', 'S Video 3', 'S Video 3', 'KEY_SVIDEO3'),
  (SendButFunc, 'fnKEY_HDMI1', 'HDMI 1', 'HDMI 1', 'KEY_HDMI1'),
  (SendButFunc, 'fnKEY_HDMI2', 'HDMI 2', 'HDMI 2', 'KEY_HDMI2'),
  (SendButFunc, 'fnKEY_HDMI3', 'HDMI 3', 'HDMI 3', 'KEY_HDMI3'),
  (SendButFunc, 'fnKEY_HDMI4', 'HDMI 4', 'HDMI 4', 'KEY_HDMI4')
  )),
(eg.ActionGroup, 'Numbers', 'Number Keys', 'Number Keys ',(
  (SendButFunc, 'fnKEY_1', 'Key1', 'Key1', 'KEY_1'), 
  (SendButFunc, 'fnKEY_2', 'Key2', 'Key2', 'KEY_2'), 
  (SendButFunc, 'fnKEY_3', 'Key3', 'Key3', 'KEY_3'), 
  (SendButFunc, 'fnKEY_4', 'Key4', 'Key4', 'KEY_4'), 
  (SendButFunc, 'fnKEY_5', 'Key5', 'Key5', 'KEY_5'), 
  (SendButFunc, 'fnKEY_6', 'Key6', 'Key6', 'KEY_6'), 
  (SendButFunc, 'fnKEY_7', 'Key7', 'Key7', 'KEY_7'), 
  (SendButFunc, 'fnKEY_8', 'Key8', 'Key8', 'KEY_8'), 
  (SendButFunc, 'fnKEY_9', 'Key9', 'Key9', 'KEY_9'), 
  (SendButFunc, 'fnKEY_0', 'Key0', 'Key0', 'KEY_0')
  )),
(eg.ActionGroup, 'Misc', 'Misc Keys', 'Misc Keys ',(
  (SendButFunc, 'fnKEY_MENU', 'Menu', 'Menu', 'KEY_MENU'),
  (SendButFunc, 'fnKEY_INFO', 'Info', 'Info', 'KEY_INFO'), 
  (SendButFunc, 'fnKEY_PANNEL_CHDOWN', '3D', '3D', 'KEY_PANNEL_CHDOWN')
  )),
(eg.ActionGroup, 'Channel', 'Channel Keys', 'Channel Keys ',(
  (SendButFunc, 'fnKEY_CHUP', 'ChannelUp', 'ChannelUp', 'KEY_CHUP'), 
  (SendButFunc, 'fnKEY_CHDOWN', 'ChannelDown', 'ChannelDown', 'KEY_CHDOWN') 
  )),
(eg.ActionGroup, 'Volume', 'Volume Keys', 'Volume Keys ',(
  (SendButFunc, 'fnKEY_VOLUP', 'VolUp', 'VolUp', 'KEY_VOLUP'),
  (SendButFunc, 'fnKEY_VOLDOWN', 'VolDown', 'VolDown', 'KEY_VOLDOWN'), 
  (SendButFunc, 'fnKEY_MUTE', 'Mute', 'Mute', 'KEY_MUTE')
  )),
(eg.ActionGroup, 'Direction', 'Direction Keys', 'Direction Keys ',(
  (SendButFunc, 'fnKEY_UP', 'Up', 'Up', 'KEY_UP'), 
  (SendButFunc, 'fnKEY_DOWN', 'Down', 'Down', 'KEY_DOWN'), 
  (SendButFunc, 'fnKEY_LEFT', 'Left', 'Left', 'KEY_LEFT'), 
  (SendButFunc, 'fnKEY_RIGHT', 'Right', 'Right', 'KEY_RIGHT'),
  (SendButFunc, 'fnKEY_RETURN', 'Return', 'Return', 'KEY_RETURN'),
  (SendButFunc, 'fnKEY_ENTER', 'Enter', 'Enter', 'KEY_ENTER'),
  (SendButFunc, 'fnKEY_PANNEL_ENTER', 'Panel Enter', 'Panel Enter', 'KEY_PANNEL_ENTER')
  )),
(eg.ActionGroup, 'Media', 'Media Keys', 'Media Keys ',(
  (SendButFunc, 'fnKEY_REWIND', 'Rewind', 'Rewind', 'KEY_REWIND'),
  (SendButFunc, 'fnKEY_STOP', 'Stop', 'Stop', 'KEY_STOP'),
  (SendButFunc, 'fnKEY_PLAY', 'Play', 'Play', 'KEY_PLAY'),
  (SendButFunc, 'fnKEY_FF', 'FastForward', 'FastForward', 'KEY_FF'),
  (SendButFunc, 'fnKEY_REC', 'Record', 'Record', 'KEY_REC'),
  (SendButFunc, 'fnKEY_PAUSE', 'Pause', 'Pause', 'KEY_PAUSE')
  )),
(eg.ActionGroup, 'Extended', 'Extended Keys', 'Extended Keys ',(
  (SendButFunc, 'fnKEY_PRECH', 'Pre-Ch', 'Pre-Ch', 'KEY_PRECH'),
  (SendButFunc, 'fnKEY_GREEN', 'Green', 'Green', 'KEY_GREEN'),
  (SendButFunc, 'fnKEY_YELLOW', 'Yellow', 'Yellow', 'KEY_YELLOW'),
  (SendButFunc, 'fnKEY_CYAN', 'Cyan', 'Cyan', 'KEY_CYAN'),
  (SendButFunc, 'fnKEY_ADDDEL', 'Add/Del', 'Add/Del', 'KEY_ADDDEL'),
  (SendButFunc, 'fnKEY_SOURCE', 'Source', 'Source', 'KEY_SOURCE'),
  (SendButFunc, 'fnKEY_PIP_ONOFF', 'PIP', 'PIP', 'KEY_PIP_ONOFF'),
  (SendButFunc, 'fnKEY_PIP_SWAP', 'PIPSwap', 'PIPSwap', 'KEY_PIP_SWAP'),
  (SendButFunc, 'fnKEY_PLUS100', 'Plus100', 'Plus100', 'KEY_PLUS100'),
  (SendButFunc, 'fnKEY_CAPTION', 'Ad/Subt.', 'Ad/Subt.', 'KEY_CAPTION'),
  (SendButFunc, 'fnKEY_PMODE', 'PictureMode', 'PictureMode', 'KEY_PMODE'),
  (SendButFunc, 'fnKEY_TTX_MIX', 'Teletext', 'Teletext', 'KEY_TTX_MIX'),
  (SendButFunc, 'fnKEY_TV', 'TV', 'TV', 'KEY_TV'),
  (SendButFunc, 'fnKEY_PICTURE_SIZE', 'PictureFormat', 'PictureFormat', 'KEY_PICTURE_SIZE'),
  (SendButFunc, 'fnKEY_AD', 'AD/Subt.', 'AD/Subt.', 'KEY_AD'),
  (SendButFunc, 'fnKEY_PIP_SIZE', 'PIPSize', 'PIPSize', 'KEY_PIP_SIZE'),
  (SendButFunc, 'fnKEY_PIP_CHUP', 'PIPChannelUp', 'PIPChannelUp', 'KEY_PIP_CHUP'),
  (SendButFunc, 'fnKEY_PIP_CHDOWN', 'PIPChannelDown', 'PIPChannelDown', 'KEY_PIP_CHDOWN'),
  (SendButFunc, 'fnKEY_ANTENA', 'AntenaTV', 'AntenaTV', 'KEY_ANTENA'),
  (SendButFunc, 'fnKEY_AUTO_PROGRAM', 'AutoProgram', 'AutoProgram', 'KEY_AUTO_PROGRAM'),
  (SendButFunc, 'fnKEY_ASPECT', 'PictureFormat', 'PictureFormat', 'KEY_ASPECT'),
  (SendButFunc, 'fnKEY_TOPMENU', 'Support', 'Support', 'KEY_TOPMENU'),
  (SendButFunc, 'fnKEY_DTV', 'DigitalTV', 'DigitalTV', 'KEY_DTV'),
  (SendButFunc, 'fnKEY_FAVCH', 'Favorites', 'Favorites', 'KEY_FAVCH'),
  (SendButFunc, 'fnKEY_TOOLS', 'Tools', 'Tools', 'KEY_TOOLS'),
  (SendButFunc, 'fnKEY_LINK', 'Link', 'Link', 'KEY_LINK'),
  (SendButFunc, 'fnKEY_SLEEP', 'SleepTimer', 'SleepTimer', 'KEY_SLEEP'),
  (SendButFunc, 'fnKEY_TURBO', 'SocialTV', 'SocialTV', 'KEY_TURBO'),
  (SendButFunc, 'fnKEY_CH_LIST', 'ChannelList', 'ChannelList', 'KEY_CH_LIST'),
  (SendButFunc, 'fnKEY_RED', 'Red', 'Red', 'KEY_RED'),
  (SendButFunc, 'fnKEY_HOME', 'Home', 'Home', 'KEY_HOME'),
  (SendButFunc, 'fnKEY_ESAVING', 'EnergySaving', 'EnergySaving', 'KEY_ESAVING'),
  (SendButFunc, 'fnKEY_CONTENTS', 'SmartTV', 'SmartTV', 'KEY_CONTENTS'),
  (SendButFunc, 'fnKEY_VCR_MODE', 'VCRmode', 'VCRmode', 'KEY_VCR_MODE'),
  (SendButFunc, 'fnKEY_CATV_MODE', 'CATVmode', 'CATVmode', 'KEY_CATV_MODE'),
  (SendButFunc, 'fnKEY_DSS_MODE', 'DSSmode', 'DSSmode', 'KEY_DSS_MODE'),
  (SendButFunc, 'fnKEY_TV_MODE', 'TVmode', 'TVmode', 'KEY_TV_MODE'),
  (SendButFunc, 'fnKEY_DVD_MODE', 'DVDmode', 'DVDmode', 'KEY_DVD_MODE'),
  (SendButFunc, 'fnKEY_STB_MODE', 'STBmode', 'STBmode', 'KEY_STB_MODE'),
  (SendButFunc, 'fnKEY_ZOOM_MOVE', 'KEY_ZOOM_MOVE', 'KEY_ZOOM_MOVE', 'KEY_ZOOM_MOVE'),
  (SendButFunc, 'fnKEY_CLOCK_DISPLAY', 'ClockDisplay', 'ClockDisplay', 'KEY_CLOCK_DISPLAY'),
  (SendButFunc, 'fnKEY_SETUP_CLOCK_TIMER', 'SetupClock', 'SetupClock', 'KEY_SETUP_CLOCK_TIMER'),
  (SendButFunc, 'fnKEY_HDMI', 'HDMI', 'HDMI', 'KEY_HDMI'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_SMALL', 'PictureModeDynamic', 'PictureModeDynamic', 'KEY_AUTO_ARC_PIP_SMALL'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_WIDE', 'HDMI2', 'HDMI2', 'KEY_AUTO_ARC_PIP_WIDE'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_RIGHT_BOTTOM', 'HDMI3', 'HDMI3', 'KEY_AUTO_ARC_PIP_RIGHT_BOTTOM'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_SOURCE_CHANGE', 'BluetoohPair', 'BluetoohPair', 'KEY_AUTO_ARC_PIP_SOURCE_CHANGE'),
  (SendButFunc, 'fnKEY_EXT9', 'PictureModeMovie', 'PictureModeMovie', 'KEY_EXT9'),
  (SendButFunc, 'fnKEY_EXT10', 'PictureModeStandard', 'PictureModeStandard', 'KEY_EXT10'),
  (SendButFunc, 'fnKEY_EXT14', 'PictureSize_3:4', 'PictureSize_3:4', 'KEY_EXT14'),
  (SendButFunc, 'fnKEY_EXT15', 'PictureSize_16:9', 'PictureSize_16:9', 'KEY_EXT15'),
  (SendButFunc, 'fnKEY_EXT20', 'HDMI1', 'HDMI1', 'KEY_EXT20'),
  (SendButFunc, 'fnKEY_EXT23', 'AV', 'AV', 'KEY_EXT23'),
  (SendButFunc, 'fnKEY_AUTO_ARC_C_FORCE_AGING', 'Fam. Story', 'Fam. Story', 'KEY_AUTO_ARC_C_FORCE_AGING'),
  (SendButFunc, 'fnKEY_AUTO_ARC_CAPTION_ENG', 'History', 'History', 'KEY_AUTO_ARC_CAPTION_ENG'),
  (SendButFunc, 'fnKEY_AUTO_ARC_USBJACK_INSPECT', 'Camera', 'Camera', 'KEY_AUTO_ARC_USBJACK_INSPECT'),
  (SendButFunc, 'fnKEY_DTV_SIGNAL', 'Search', 'Search', 'KEY_DTV_SIGNAL'),
  (SendButFunc, 'fnKEY_CONVERGENCE', 'InternetBrowser', 'InternetBrowser', 'KEY_CONVERGENCE')
  )),
(eg.ActionGroup, 'Other', 'Other Keys', 'Other Keys ',(
  (SendButFunc, 'fnKEY_MAGIC_CHANNEL', 'KEY_MAGIC_CHANNEL', 'KEY_MAGIC_CHANNEL', 'KEY_MAGIC_CHANNEL'),
  (SendButFunc, 'fnKEY_PIP_SCAN', 'KEY_PIP_SCAN', 'KEY_PIP_SCAN', 'KEY_PIP_SCAN'),
  (SendButFunc, 'fnKEY_DEVICE_CONNECT', 'KEY_DEVICE_CONNECT', 'KEY_DEVICE_CONNECT', 'KEY_DEVICE_CONNECT'),
  (SendButFunc, 'fnKEY_HELP', 'KEY_HELP', 'KEY_HELP', 'KEY_HELP'),
  (SendButFunc, 'fnKEY_11', 'KEY_11', 'KEY_11', 'KEY_11'),
  (SendButFunc, 'fnKEY_12', 'KEY_12', 'KEY_12', 'KEY_12'),
  (SendButFunc, 'fnKEY_FACTORY', 'KEY_FACTORY', 'KEY_FACTORY', 'KEY_FACTORY'),
  (SendButFunc, 'fnKEY_3SPEED', 'KEY_3SPEED', 'KEY_3SPEED', 'KEY_3SPEED'),
  (SendButFunc, 'fnKEY_RSURF', 'KEY_RSURF', 'KEY_RSURF', 'KEY_RSURF'),
  (SendButFunc, 'fnKEY_GAME', 'KEY_GAME', 'KEY_GAME', 'KEY_GAME'),
  (SendButFunc, 'fnKEY_QUICK_REPLAY', 'KEY_QUICK_REPLAY', 'KEY_QUICK_REPLAY', 'KEY_QUICK_REPLAY'),
  (SendButFunc, 'fnKEY_STILL_PICTURE', 'KEY_STILL_PICTURE', 'KEY_STILL_PICTURE', 'KEY_STILL_PICTURE'),
  (SendButFunc, 'fnKEY_INSTANT_REPLAY', 'KEY_INSTANT_REPLAY', 'KEY_INSTANT_REPLAY', 'KEY_INSTANT_REPLAY'),
  (SendButFunc, 'fnKEY_FF_', 'KEY_FF_', 'KEY_FF_', 'KEY_FF_'),
  (SendButFunc, 'fnKEY_GUIDE', 'KEY_GUIDE', 'KEY_GUIDE', 'KEY_GUIDE'),
  (SendButFunc, 'fnKEY_REWIND_', 'KEY_REWIND_', 'KEY_REWIND_', 'KEY_REWIND_'),
  (SendButFunc, 'fnKEY_ANGLE', 'KEY_ANGLE', 'KEY_ANGLE', 'KEY_ANGLE'),
  (SendButFunc, 'fnKEY_RESERVED1', 'KEY_RESERVED1', 'KEY_RESERVED1', 'KEY_RESERVED1'),  
  (SendButFunc, 'fnKEY_ZOOM1', 'KEY_ZOOM1', 'KEY_ZOOM1', 'KEY_ZOOM1'),
  (SendButFunc, 'fnKEY_PROGRAM', 'KEY_PROGRAM', 'KEY_PROGRAM', 'KEY_PROGRAM'),
  (SendButFunc, 'fnKEY_BOOKMARK', 'KEY_BOOKMARK', 'KEY_BOOKMARK', 'KEY_BOOKMARK'),
  (SendButFunc, 'fnKEY_DISC_MENU', 'KEY_DISC_MENU', 'KEY_DISC_MENU', 'KEY_DISC_MENU'),
  (SendButFunc, 'fnKEY_PRINT', 'KEY_PRINT', 'KEY_PRINT', 'KEY_PRINT'),
  (SendButFunc, 'fnKEY_SUB_TITLE', 'KEY_SUB_TITLE', 'KEY_SUB_TITLE', 'KEY_SUB_TITLE'),
  (SendButFunc, 'fnKEY_CLEAR', 'KEY_CLEAR', 'KEY_CLEAR', 'KEY_CLEAR'),
  (SendButFunc, 'fnKEY_VCHIP', 'KEY_VCHIP', 'KEY_VCHIP', 'KEY_VCHIP'),
  (SendButFunc, 'fnKEY_REPEAT', 'KEY_REPEAT', 'KEY_REPEAT', 'KEY_REPEAT'),
  (SendButFunc, 'fnKEY_DOOR', 'KEY_DOOR', 'KEY_DOOR', 'KEY_DOOR'),
  (SendButFunc, 'fnKEY_OPEN', 'KEY_OPEN', 'KEY_OPEN', 'KEY_OPEN'),
  (SendButFunc, 'fnKEY_WHEEL_LEFT', 'KEY_WHEEL_LEFT', 'KEY_WHEEL_LEFT', 'KEY_WHEEL_LEFT'),
  (SendButFunc, 'fnKEY_POWER', 'KEY_POWER', 'KEY_POWER', 'KEY_POWER'),
  (SendButFunc, 'fnKEY_DMA', 'KEY_DMA', 'KEY_DMA', 'KEY_DMA'),
  (SendButFunc, 'fnKEY_FM_RADIO', 'KEY_FM_RADIO', 'KEY_FM_RADIO', 'KEY_FM_RADIO'),
  (SendButFunc, 'fnKEY_DVR_MENU', 'KEY_DVR_MENU', 'KEY_DVR_MENU', 'KEY_DVR_MENU'),
  (SendButFunc, 'fnKEY_MTS', 'KEY_MTS', 'KEY_MTS', 'KEY_MTS'),
  (SendButFunc, 'fnKEY_PCMODE', 'KEY_PCMODE', 'KEY_PCMODE', 'KEY_PCMODE'),
  (SendButFunc, 'fnKEY_TTX_SUBFACE', 'KEY_TTX_SUBFACE', 'KEY_TTX_SUBFACE', 'KEY_TTX_SUBFACE'),
  (SendButFunc, 'fnKEY_DNIe', 'KEY_DNIe', 'KEY_DNIe', 'KEY_DNIe'),
  (SendButFunc, 'fnKEY_SRS', 'KEY_SRS', 'KEY_SRS', 'KEY_SRS'),
  (SendButFunc, 'fnKEY_CONVERT_AUDIO_MAINSUB', 'KEY_CONVERT_AUDIO_MAINSUB', 'KEY_CONVERT_AUDIO_MAINSUB', 'KEY_CONVERT_AUDIO_MAINSUB'),
  (SendButFunc, 'fnKEY_MDC', 'KEY_MDC', 'KEY_MDC', 'KEY_MDC'),
  (SendButFunc, 'fnKEY_SEFFECT', 'KEY_SEFFECT', 'KEY_SEFFECT', 'KEY_SEFFECT'),
  (SendButFunc, 'fnKEY_DVR', 'KEY_DVR', 'KEY_DVR', 'KEY_DVR'),
  (SendButFunc, 'fnKEY_LIVE', 'KEY_LIVE', 'KEY_LIVE', 'KEY_LIVE'),
  (SendButFunc, 'fnKEY_PERPECT_FOCUS', 'KEY_PERPECT_FOCUS', 'KEY_PERPECT_FOCUS', 'KEY_PERPECT_FOCUS'),
  (SendButFunc, 'fnKEY_WHEEL_RIGHT', 'KEY_WHEEL_RIGHT', 'KEY_WHEEL_RIGHT', 'KEY_WHEEL_RIGHT'),
  (SendButFunc, 'fnKEY_CALLER_ID', 'KEY_CALLER_ID', 'KEY_CALLER_ID', 'KEY_CALLER_ID'),
  (SendButFunc, 'fnKEY_SCALE', 'KEY_SCALE', 'KEY_SCALE', 'KEY_SCALE'),
  (SendButFunc, 'fnKEY_MAGIC_BRIGHT', 'KEY_MAGIC_BRIGHT', 'KEY_MAGIC_BRIGHT', 'KEY_MAGIC_BRIGHT'),
  (SendButFunc, 'fnKEY_DVI', 'KEY_DVI', 'KEY_DVI', 'KEY_DVI'),
  (SendButFunc, 'fnKEY_W_LINK', 'KEY_W_LINK', 'KEY_W_LINK', 'KEY_W_LINK'),
  (SendButFunc, 'fnKEY_DTV_LINK', 'KEY_DTV_LINK', 'KEY_DTV_LINK', 'KEY_DTV_LINK'),
  (SendButFunc, 'fnKEY_APP_LIST', 'KEY_APP_LIST', 'KEY_APP_LIST', 'KEY_APP_LIST'),
  (SendButFunc, 'fnKEY_BACK_MHP', 'KEY_BACK_MHP', 'KEY_BACK_MHP', 'KEY_BACK_MHP'),
  (SendButFunc, 'fnKEY_ALT_MHP', 'KEY_ALT_MHP', 'KEY_ALT_MHP', 'KEY_ALT_MHP'),
  (SendButFunc, 'fnKEY_DNSe', 'KEY_DNSe', 'KEY_DNSe', 'KEY_DNSe'),
  (SendButFunc, 'fnKEY_RSS', 'KEY_RSS', 'KEY_RSS', 'KEY_RSS'),
  (SendButFunc, 'fnKEY_ENTERTAINMENT', 'KEY_ENTERTAINMENT', 'KEY_ENTERTAINMENT', 'KEY_ENTERTAINMENT'),
  (SendButFunc, 'fnKEY_ID_INPUT', 'KEY_ID_INPUT', 'KEY_ID_INPUT', 'KEY_ID_INPUT'),
  (SendButFunc, 'fnKEY_ID_SETUP', 'KEY_ID_SETUP', 'KEY_ID_SETUP', 'KEY_ID_SETUP'),
  (SendButFunc, 'fnKEY_ANYNET', 'KEY_ANYNET', 'KEY_ANYNET', 'KEY_ANYNET'),
  (SendButFunc, 'fnKEY_POWERON', 'KEY_POWERON', 'KEY_POWERON', 'KEY_POWERON'),
  (SendButFunc, 'fnKEY_ANYVIEW', 'KEY_ANYVIEW', 'KEY_ANYVIEW', 'KEY_ANYVIEW'),
  (SendButFunc, 'fnKEY_MS', 'KEY_MS', 'KEY_MS', 'KEY_MS'),
  (SendButFunc, 'fnKEY_MORE', 'KEY_MORE', 'KEY_MORE', 'KEY_MORE'),
  (SendButFunc, 'fnKEY_PANNEL_POWER', 'KEY_PANNEL_POWER', 'KEY_PANNEL_POWER', 'KEY_PANNEL_POWER'),
  (SendButFunc, 'fnKEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP', 'KEY_PANNEL_CHUP'),
  (SendButFunc, 'fnKEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP', 'KEY_PANNEL_VOLUP'),
  (SendButFunc, 'fnKEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW', 'KEY_PANNEL_VOLDOW'),
  (SendButFunc, 'fnKEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER', 'KEY_PANNEL_ENTER'),
  (SendButFunc, 'fnKEY_PANNEL_MENU', 'KEY_PANNEL_MENU', 'KEY_PANNEL_MENU', 'KEY_PANNEL_MENU'),
  (SendButFunc, 'fnKEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE', 'KEY_PANNEL_SOURCE'),
  (SendButFunc, 'fnKEY_ZOOM2', 'KEY_ZOOM2', 'KEY_ZOOM2', 'KEY_ZOOM2'),
  (SendButFunc, 'fnKEY_PANORAMA', 'KEY_PANORAMA', 'KEY_PANORAMA', 'KEY_PANORAMA'),
  (SendButFunc, 'fnKEY_4_3', 'KEY_4_3', 'KEY_4_3', 'KEY_4_3'),
  (SendButFunc, 'fnKEY_16_9', 'KEY_16_9', 'KEY_16_9', 'KEY_16_9'),
  (SendButFunc, 'fnKEY_DYNAMIC', 'KEY_DYNAMIC', 'KEY_DYNAMIC', 'KEY_DYNAMIC'),
  (SendButFunc, 'fnKEY_STANDARD', 'KEY_STANDARD', 'KEY_STANDARD', 'KEY_STANDARD'),
  (SendButFunc, 'fnKEY_MOVIE1', 'KEY_MOVIE1', 'KEY_MOVIE1', 'KEY_MOVIE1'),
  (SendButFunc, 'fnKEY_CUSTOM', 'KEY_CUSTOM', 'KEY_CUSTOM', 'KEY_CUSTOM'),
  (SendButFunc, 'fnKEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET', 'KEY_AUTO_ARC_RESET'),
  (SendButFunc, 'fnKEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON', 'KEY_AUTO_ARC_LNA_ON'),
  (SendButFunc, 'fnKEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF', 'KEY_AUTO_ARC_LNA_OFF'),
  (SendButFunc, 'fnKEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK', 'KEY_AUTO_ARC_ANYNET_MODE_OK'),
  (SendButFunc, 'fnKEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START', 'KEY_AUTO_ARC_ANYNET_AUTO_START'),
  (SendButFunc, 'fnKEY_AUTO_FORMAT', 'KEY_AUTO_FORMAT', 'KEY_AUTO_FORMAT', 'KEY_AUTO_FORMAT'),
  (SendButFunc, 'fnKEY_DNET', 'KEY_DNET', 'KEY_DNET', 'KEY_DNET'),
  (SendButFunc, 'fnKEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON', 'KEY_AUTO_ARC_CAPTION_ON'),
  (SendButFunc, 'fnKEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF', 'KEY_AUTO_ARC_CAPTION_OFF'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE', 'KEY_AUTO_ARC_PIP_DOUBLE'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE', 'KEY_AUTO_ARC_PIP_LARGE'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP', 'KEY_AUTO_ARC_PIP_LEFT_TOP'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP', 'KEY_AUTO_ARC_PIP_RIGHT_TOP'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM', 'KEY_AUTO_ARC_PIP_LEFT_BOTTOM'),
  (SendButFunc, 'fnKEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE', 'KEY_AUTO_ARC_PIP_CH_CHANGE'),
  (SendButFunc, 'fnKEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS', 'KEY_AUTO_ARC_AUTOCOLOR_SUCCESS'),
  (SendButFunc, 'fnKEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL', 'KEY_AUTO_ARC_AUTOCOLOR_FAIL'),
  (SendButFunc, 'fnKEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT', 'KEY_AUTO_ARC_JACK_IDENT'),
  (SendButFunc, 'fnKEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE', 'KEY_NINE_SEPERATE'),
  (SendButFunc, 'fnKEY_ZOOM_IN', 'KEY_ZOOM_IN', 'KEY_ZOOM_IN', 'KEY_ZOOM_IN'),
  (SendButFunc, 'fnKEY_ZOOM_OUT', 'KEY_ZOOM_OUT', 'KEY_ZOOM_OUT', 'KEY_ZOOM_OUT'),
  (SendButFunc, 'fnKEY_MIC', 'KEY_MIC', 'KEY_MIC', 'KEY_MIC'),
  (SendButFunc, 'fnKEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR', 'KEY_AUTO_ARC_CAPTION_KOR'),
  (SendButFunc, 'fnKEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR', 'KEY_AUTO_ARC_ANTENNA_AIR'),
  (SendButFunc, 'fnKEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE', 'KEY_AUTO_ARC_ANTENNA_CABLE'),
  (SendButFunc, 'fnKEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE', 'KEY_AUTO_ARC_ANTENNA_SATELLITE'),
  (SendButFunc, 'fnKEY_EXT1', 'KEY_EXT1', 'KEY_EXT1', 'KEY_EXT1'),
  (SendButFunc, 'fnKEY_EXT2', 'KEY_EXT2', 'KEY_EXT2', 'KEY_EXT2'),
  (SendButFunc, 'fnKEY_EXT3', 'KEY_EXT3', 'KEY_EXT3', 'KEY_EXT3'),
  (SendButFunc, 'fnKEY_EXT4', 'KEY_EXT4', 'KEY_EXT4', 'KEY_EXT4'),
  (SendButFunc, 'fnKEY_EXT5', 'KEY_EXT5', 'KEY_EXT5', 'KEY_EXT5'),
  (SendButFunc, 'fnKEY_EXT6', 'KEY_EXT6', 'KEY_EXT6', 'KEY_EXT6'),
  (SendButFunc, 'fnKEY_EXT7', 'KEY_EXT7', 'KEY_EXT7', 'KEY_EXT7'),
  (SendButFunc, 'fnKEY_EXT8', 'KEY_EXT8', 'KEY_EXT8', 'KEY_EXT8'),
  (SendButFunc, 'fnKEY_EXT11', 'KEY_EXT11', 'KEY_EXT11', 'KEY_EXT11'),
  (SendButFunc, 'fnKEY_EXT12', 'KEY_EXT12', 'KEY_EXT12', 'KEY_EXT12'),
  (SendButFunc, 'fnKEY_EXT13', 'KEY_EXT13', 'KEY_EXT13', 'KEY_EXT13'),
  (SendButFunc, 'fnKEY_EXT16', 'KEY_EXT16', 'KEY_EXT16', 'KEY_EXT16'),
  (SendButFunc, 'fnKEY_EXT17', 'KEY_EXT17', 'KEY_EXT17', 'KEY_EXT17'),
  (SendButFunc, 'fnKEY_EXT18', 'KEY_EXT18', 'KEY_EXT18', 'KEY_EXT18'),
  (SendButFunc, 'fnKEY_EXT19', 'KEY_EXT19', 'KEY_EXT19', 'KEY_EXT19'),
  (SendButFunc, 'fnKEY_EXT21', 'KEY_EXT21', 'KEY_EXT21', 'KEY_EXT21'),
  (SendButFunc, 'fnKEY_EXT22', 'KEY_EXT22', 'KEY_EXT22', 'KEY_EXT22'),
  (SendButFunc, 'fnKEY_EXT24', 'KEY_EXT24', 'KEY_EXT24', 'KEY_EXT24'),
  (SendButFunc, 'fnKEY_EXT25', 'KEY_EXT25', 'KEY_EXT25', 'KEY_EXT25'),
  (SendButFunc, 'fnKEY_EXT26', 'KEY_EXT26', 'KEY_EXT26', 'KEY_EXT26'),
  (SendButFunc, 'fnKEY_EXT27', 'KEY_EXT27', 'KEY_EXT27', 'KEY_EXT27'),
  (SendButFunc, 'fnKEY_EXT28', 'KEY_EXT28', 'KEY_EXT28', 'KEY_EXT28'),
  (SendButFunc, 'fnKEY_EXT29', 'KEY_EXT29', 'KEY_EXT29', 'KEY_EXT29'),
  (SendButFunc, 'fnKEY_EXT30', 'KEY_EXT30', 'KEY_EXT30', 'KEY_EXT30'),
  (SendButFunc, 'fnKEY_EXT31', 'KEY_EXT31', 'KEY_EXT31', 'KEY_EXT31'),
  (SendButFunc, 'fnKEY_EXT32', 'KEY_EXT32', 'KEY_EXT32', 'KEY_EXT32'),
  (SendButFunc, 'fnKEY_EXT33', 'KEY_EXT33', 'KEY_EXT33', 'KEY_EXT33'),
  (SendButFunc, 'fnKEY_EXT34', 'KEY_EXT34', 'KEY_EXT34', 'KEY_EXT34'),
  (SendButFunc, 'fnKEY_EXT35', 'KEY_EXT35', 'KEY_EXT35', 'KEY_EXT35'),
  (SendButFunc, 'fnKEY_EXT36', 'KEY_EXT36', 'KEY_EXT36', 'KEY_EXT36'),
  (SendButFunc, 'fnKEY_EXT37', 'KEY_EXT37', 'KEY_EXT37', 'KEY_EXT37'),
  (SendButFunc, 'fnKEY_EXT38', 'KEY_EXT38', 'KEY_EXT38', 'KEY_EXT38'),
  (SendButFunc, 'fnKEY_EXT39', 'KEY_EXT39', 'KEY_EXT39', 'KEY_EXT39'),
  (SendButFunc, 'fnKEY_EXT40', 'KEY_EXT40', 'KEY_EXT40', 'KEY_EXT40'),
  (SendButFunc, 'fnKEY_EXT41', 'KEY_EXT41', 'KEY_EXT41', 'KEY_EXT41')
  ))
)
